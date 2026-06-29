# TheCrew — feed de actualizaciones (público)

Canal de **solo lectura** del que los clientes de **TheCrew** (producto de Velari) tiran sus mejoras y
formas de trabajar (`python soporte/actualizar.py`). **Solo metodología — cero datos de clientes, cero secretos.**

- `manifest.json` — índice: versión + lista de formas (cada una con su `ruta` relativa).
- `formas/` — las formas de trabajar que se publican (la primera: `METODO_VELARI.md`, el método de Velari).

**Publicar una mejora:** edita/añade una forma en `formas/`, súbela al `manifest.json` (sube la `version`) y haz push.
Todos los clientes la reciben en su próximo `actualizar.py`. Uno-a-muchos, sin tocar a ningún cliente.

*Velari · feed de TheCrew · 29-jun-2026.*
