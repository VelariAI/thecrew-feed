#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""actualizar.py — RECIBE del proveedor (Velari): mejoras de método (formas) y ARREGLOS del producto.

Tira (pull) de un canal de SOLO LECTURA que controla Velari. NO envia tus datos.
Frontera: el feed solo escribe en archivos del PRODUCTO (dentro de TheCrew); NUNCA toca tus proyectos.

Uso:  python soporte/actualizar.py
"""
import sys
import json
import urllib.request
import datetime
from urllib.parse import urljoin
from pathlib import Path

try:                                  # consola Windows = cp1252; utf-8 para acentos y flechas
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]          # soporte/ -> TheCrew (raiz del producto)
FT = ROOT / "soporte" / "formas_de_trabajar"
FT.mkdir(parents=True, exist_ok=True)
PROV = ROOT / "PROVEEDOR.md"
VER = ROOT / "VERSION.txt"


def cfg(clave):
    try:
        for ln in PROV.read_text(encoding="utf-8-sig").splitlines():
            s = ln.strip()
            if s.lower().startswith(clave.lower() + ":"):
                return s.split(":", 1)[1].strip()
    except Exception:
        pass
    return ""


def bajar(feed, ref):
    with urllib.request.urlopen(urljoin(feed, ref), timeout=25) as r:
        return r.read()


def destino_seguro(rel):
    """Solo rutas relativas DENTRO del kit; nada de absolutas ni '..' (no escapar de TheCrew)."""
    if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
        return None
    p = (ROOT / rel).resolve()
    return p if (p == ROOT or ROOT in p.parents) else None


feed = cfg("FEED_ACTUALIZACIONES")
if not feed or feed.startswith("("):
    print("El canal del proveedor aún no está configurado (PROVEEDOR.md → FEED_ACTUALIZACIONES).")
    raise SystemExit(0)

try:
    with urllib.request.urlopen(feed, timeout=25) as r:
        manifest = json.loads(r.read().decode("utf-8"))
except Exception as e:
    print(f"No pude conectar con el proveedor ({e}). Reintenta luego; sigues trabajando igual.")
    raise SystemExit(0)

remoto = str(manifest.get("version", "?"))
nuevas = arreglos = 0

# 1) FORMAS de trabajar (metodología) -> soporte/formas_de_trabajar/
for f in manifest.get("formas", []):
    nombre, ref = f.get("nombre"), (f.get("ruta") or f.get("url"))
    if not nombre or not ref:
        continue
    dest = FT / nombre
    try:
        c = bajar(feed, ref)
        if (not dest.exists()) or dest.read_bytes() != c:
            dest.write_bytes(c); nuevas += 1; print(f"  + forma: {nombre}")
    except Exception as e:
        print(f"  ! no pude bajar {nombre}: {e}")

# 2) ARREGLOS del producto (archivos corregidos) -> ruta destino dentro del kit
for a in manifest.get("archivos", []):
    destino, ref = a.get("destino"), (a.get("ruta") or a.get("url"))
    if not destino or not ref:
        continue
    p = destino_seguro(destino)
    if p is None:
        print(f"  ! arreglo IGNORADO (ruta no segura): {destino}"); continue
    try:
        c = bajar(feed, ref)
        if (not p.exists()) or p.read_bytes() != c:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(c); arreglos += 1; print(f"  ⚙ arreglo aplicado: {destino}")
    except Exception as e:
        print(f"  ! no pude aplicar {destino}: {e}")

VER.write_text(f"{remoto}  (actualizado {datetime.date.today().isoformat()})", encoding="utf-8")
if nuevas or arreglos:
    print(f"\nVelari te ha mandado: {nuevas} mejora(s) de método + {arreglos} arreglo(s) del producto.")
    msg = manifest.get("mensaje", "")
    if msg:
        print(f'Mensaje del proveedor: "{msg}"')
    if nuevas:
        print("Dile a tu arquitecto: «lee las formas de trabajar nuevas y aplícalas».")
    if arreglos:
        print("Arreglos aplicados al producto. Si algo estaba roto, vuelve a probarlo.")
else:
    print("Estás al día. Nada nuevo del proveedor.")
