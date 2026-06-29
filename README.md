# TheCrew — feed de actualizaciones (público)

Canal de **solo lectura** del que los clientes de **TheCrew** (producto de Velari) tiran mejoras y arreglos
(`python soporte/actualizar.py`). **Solo producto y metodología — cero datos de clientes, cero secretos.**

- `manifest.json` — índice: `version` + `formas` (método) + `archivos` (arreglos del producto).
- `formas/` — formas de trabajar (método). El cliente las recibe en `soporte/formas_de_trabajar/`.
- Archivos de arreglo (scripts/config corregidos) se sirven aquí y se aplican en la ruta `destino` del cliente.

## Publicar una MEJORA de método
Añade/edita una forma en `formas/` → añádela al `manifest.json` (`formas`) → sube `version` → push.

## Publicar un ARREGLO del producto (corregir el funcionamiento en remoto)
1. Sube el archivo corregido a este repo (p.ej. `actualizar.py`, o `fixes/loquesea.py`).
2. En `manifest.json` → `archivos`, añade `{ "destino": "<ruta dentro del kit>", "ruta": "<archivo en este repo>" }`.
   - `destino` DEBE ser una ruta dentro de TheCrew (sin `..`, sin rutas absolutas); el cliente la valida y rechaza lo inseguro.
3. Sube `version` y haz push. Todos los clientes lo aplican en su próximo `actualizar.py`.

Uno-a-muchos · solo lectura · **sin entrar en la máquina de ningún cliente ni ver sus datos.**

*Velari · feed de TheCrew · 29-jun-2026.*
