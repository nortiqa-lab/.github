Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

**ID:** DICT-NL-GOBERNANZA-ALMACENAMIENTO-001  
**Versión:** 0.1-DEV-STUB  
**Fecha stub:** 2026-08-02  
**Origen:** reconstruido desde `TAREA-NL-GOBERNANZA-ALMACENAMIENTO-001` (Notion)  
**Bloqueo:** al 2026-08-02 la página Notion del DICT ratificado **no fue encontrada**. Gio debe pegar URL/texto canónico y reemplazar este stub.

---

# DICT-NL-GOBERNANZA-ALMACENAMIENTO-001 (stub)

## 1. Objeto

Definir dónde vive cada clase de documento/activo digital de Nortiqa y entidades relacionadas, evitando doble fuente de verdad y mezclas indebidas.

## 2. Matriz (contenido operativo de la TAREA)

| Estado / tipo | Sistema |
|---------------|---------|
| PROD — docs ratificados | GitHub privado `nortiqa-lab/governance` |
| DEV — trabajo / tareas con estado | AppFlowy / Notion |
| Entregables externos + docs financieros/legales | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |

## 3. Relación con PLAN-NL-GITHUB-001

- Código, datos y secretos: repos separados por entidad (PLAN-NL-GITHUB-001 permanece).
- Documentación PROD: **un** repo `governance` con carpetas por entidad + CODEOWNERS.
- Esta regla **no** autoriza mezclar código de entidades distintas en un solo repo de producto.

## 4. Estructura mínima del repo

Ver README del seed. Carpetas: `nortiqa-lab/`, `valent-capital/`, `sc2027/`, `lla-santa-cruz/`, `surlancer/`, `transversal/`.

## 5. SC2027

Etiqueta operativa de VPS/host Nortiqa. Carpeta `docs/sc2027/` por plataforma. No implica persona jurídica peer de Valent/LLA salvo redefinición de Gio.

## 6. Sur Lancer

Incluido en alcance de migración AppFlowy LOTE (afirmación Gio 2026-08-02 “sí a todo”), con carpeta `docs/surlancer/` y **sin** mezclar contenido en `nortiqa-lab/`.

## 7. Controles

- Naming con prefijo de entidad.
- PRs obligatorios a `main`.
- Sin secretos en Git.
- Migración progresiva (solo ratificados/activos).
- Redirects Notion solo con autorización Gio + PAO/OT.

## 8. Condición de validez de este stub

Deja de ser stub cuando:

1. Gio aporta URL/texto del DICT ratificado, **o**
2. Claude emite dictamen que adopta/ajusta este texto y Gio lo ratifica.

Hasta entonces: **DEV / Borrador**.
