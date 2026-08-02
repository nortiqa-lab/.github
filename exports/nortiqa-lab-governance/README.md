# nortiqa-lab/governance — seed (DEV)

Private governance documentation repo seed.  
**Not official until Gio creates the remote repo, Claude audits, and Gio ratifies.**

## Storage matrix (PROD docs)

| State | System |
|-------|--------|
| PROD ratified docs | This GitHub repo (`docs/[entity]/[type]/`) |
| DEV / tasks with status | Notion or AppFlowy |
| External share + financial/legal packs | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |
| Operational inventory / runtime tasks | PostgreSQL (see `exports/sql/` in `.github` seed) |
| Agent prompt definitions | Git product / `.github/agents` |

## Supersedes PLAN-NL-GITHUB-001?

Only for **PROD documentation placement**: one private `governance` repo with entity folders.  
Code, data, and secrets **remain** in separate entity repos (PLAN-NL-GITHUB-001 still applies there).

## Decision diagram

```
¿Documento ratificado (PROD)?
├── SÍ → GitHub docs/[entidad]/[tipo]/
└── NO (DEV) → ¿Tarea/seguimiento con estados?
    ├── SÍ → Notion/AppFlowy (DB)
    └── NO → ¿Se comparte con externos?
        ├── SÍ → Google Drive
        └── NO → Notion/AppFlowy (página)
```

## Entity folders

| Folder | Meaning |
|--------|---------|
| `nortiqa-lab/` | Nortiqa Lab docs |
| `valent-capital/` | Valent — **empty until Gio inventories** |
| `lla-santa-cruz/` | LLA — **empty until Gio inventories** |
| `sc2027/` | VPS/platform ops label (not a legal peer by default) |
| `transversal/` | Truly cross-entity only |

## Naming

`DICT-[ENTIDAD]-xxx-001.md`, `REGLA-[ENTIDAD]-xxx-001.md`, `GOV-[ENTIDAD]-xxx-001.md`

## Current seed contents (Nortiqa only)

**Dictámenes (mirrors/stubs):** NORMA-AGENTES, GITHUB, EXEC-GATE, DOC-CENT, KNOW-001/002, AGENTES-OPCIONES, SERVIDOROPS, MEDICION-TOKENS, IDENTITY-RATIF, GOBERNANZA-ALMACENAMIENTO (stub), VISION-FUSION (stub).  
**Reglas / gov:** VERACIDAD-TOTAL, ESCALADA-TEMATICA, GOV-NL-ORG (stub).  
**Inventarios:** Lot A + Lot B.  
**Apply:** `apply.sh` (Gio/admin) · `scripts/pack-for-remote.sh` (pack sin create).  
**SQL inventario:** vive en `exports/sql/` del repo `.github`, no aquí.

No Notion deletes. No Valent/LLA content copied. PR canónico: `.github` #16 (supersede #15).
