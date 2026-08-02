Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

# nortiqa-lab/governance — seed

Paquete semilla para el repo privado **`nortiqa-lab/governance`** (aún no creado en GitHub).

## Matriz de almacenamiento (ratificada por Gio — vía TAREA)

| Estado | Sistema |
|--------|---------|
| PROD (docs ratificados) | Este repo GitHub |
| DEV / tareas con estado | AppFlowy / Notion |
| Externos + financiero/legal | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |

## Supersesión vs PLAN-NL-GITHUB-001

`PLAN-NL-GITHUB-001` separa entidades por **repositorio** para código/datos/secretos.

**Para documentación PROD:** un único repo `governance` con **carpetas por entidad** + CODEOWNERS.  
Código, datos y secretos **siguen** en repos separados por entidad.

> Pendiente: página Notion `DICT-NL-GOBERNANZA-ALMACENAMIENTO-001` (texto oficial). Stub DEV en `docs/nortiqa-lab/dictamenes/`.

## Árbol

```text
docs/
├── nortiqa-lab/     # entidad Nortiqa Lab
├── valent-capital/  # Valent — solo docs Valent ratificados
├── sc2027/          # etiqueta operativa VPS/host (no persona jurídica)
├── lla-santa-cruz/  # LLA — solo con autorización Gio
├── surlancer/       # Sur Lancer — incluido en alcance AppFlowy LOTE (Gio 2026-08-02)
└── transversal/     # solo docs que aplican a todas
```

Cada entidad (salvo transversal) tiene: `dictamenes/`, `auditorias/`, `governance/`, `specs/`, `sops/`, `logs/`, `planes/` (+ `adr/` donde aplica).

## Diagrama de decisión

```text
¿Documento ratificado (PROD)?
├── SÍ → GitHub docs/<entidad>/<tipo>/
└── NO (DEV) → ¿Tarea/seguimiento con estados?
    ├── SÍ → AppFlowy / Notion (DB)
    └── NO → ¿Se comparte con externos?
        ├── SÍ → Google Drive 90_COMPARTIR/POR_ENTIDAD/
        └── NO → AppFlowy / Notion (página)
```

## Naming

`DICT-[ENTIDAD]-xxx-001.md`, `PLAN-…`, `GOV-…`, `ADR-…`  
Si el prefijo de entidad no es claro → **preguntar a Gio** antes de ubicar.

## Aislamiento

- Nunca mezclar contenido de una entidad en la carpeta de otra.
- Secretos / tokens / `.env` **prohibidos** en este repo.
- SC2027 = carpeta operativa de plataforma Nortiqa; no implica entidad legal peer.

## Cómo aplicar (Gio / admin org)

Ver `APPLY.md`.

## Relación con otros repos

| Repo | Rol |
|------|-----|
| `nortiqa-lab/.github` | Kit agentes + docs DEV Cursor |
| `nortiqa-lab/governance` | Docs PROD multi-entidad (este seed) |
| `infra`, `n8n-workflows`, `queryos` | Código/ops (DICT-NL-GITHUB-REPOS) — pendientes |

## Estado

Seed preparado 2026-08-02 por Cursor. No declara el repo como creado ni PROD.
