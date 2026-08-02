# nortiqa-lab/governance

Estado: DEV / Borrador (seed)

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Repositorio **privado** destinado a documentación **PROD (ratificada)** del ecosistema multi-entidad.

Prompt KNOW-001 (ajustado):  
https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558

## Matriz de almacenamiento

| Estado / tipo | Destino |
|---|---|
| Ratificado (PROD) | Este repo — `docs/[entidad]/[tipo]/` |
| DEV — tarea/seguimiento con estados | AppFlowy / Notion (base de datos) |
| DEV — página de trabajo | AppFlowy / Notion (página) |
| Entregables externos + financieros/legales | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |
| Inventario operativo / tareas runtime | PostgreSQL (ver `exports/sql/` en `.github`) |
| Prompts de agentes | Git product / `.github/agents` |

## Diagrama de decisión

```text
¿El documento está ratificado (PROD)?
├── SÍ → GitHub (docs/[entidad]/[tipo]/)
└── NO (DEV) → ¿Es tarea/seguimiento con estados?
    ├── SÍ → AppFlowy/Notion (base de datos)
    └── NO → ¿Se comparte con externos?
        ├── SÍ → Google Drive (90_COMPARTIR/POR_ENTIDAD/)
        └── NO → AppFlowy/Notion (página)
```

## Entidades / carpetas

| Carpeta | Alcance |
|---|---|
| `docs/nortiqa-lab/` | Nortiqa Lab |
| `docs/valent-capital/` | Valent — vacío hasta inventario Gio |
| `docs/lla-santa-cruz/` | LLA — vacío hasta inventario Gio |
| `docs/sc2027/` | SC2027 — en LOG-NL-SESION-20260709 figura como entidad separada; kit Cursor aún lo trata como host VPS (discrepancia documentada) |
| `docs/transversal/` | Solo docs verdaderamente cross-entity |

**Regla dura:** nunca mezclar documentos de una entidad en la carpeta de otra.  
Si el prefijo de entidad no es claro → preguntar a Gio antes de ubicar.

### Tipos de carpeta (por entidad)

`dictamenes/` · `auditorias/` · `governance/` · `specs/` · `sops/` · `logs/` · `planes/`  
(`adr/` en Nortiqa Lab)

## Naming

- `DICT-[ENTIDAD]-xxx-001.md`
- `REGLA-[ENTIDAD]-xxx-001.md`
- `GOV-[ENTIDAD]-xxx-001.md`
- `PLAN-[ENTIDAD]-xxx-001.md`

## Supersesión vs PLAN-NL-GITHUB-001

`PLAN-NL-GITHUB-001` (vía `DICT-NL-GITHUB-001`) separa entidades por **repositorio** para código, datos y secretos.

**Este modelo supersede esa regla solo para documentación PROD:** un único repo privado con carpetas por entidad + Teams/CODEOWNERS.

Código, datos y secretos **siguen** en repos separados por entidad.

## Control de acceso

- Repo: **private**
- `CODEOWNERS` / `.github/CODEOWNERS` (Gio completa Teams)
- Branch protection en `main`: PR + review
- Git flow: PRs por lote; no commits directos a `main`

## Contenido actual del seed (Nortiqa)

**Dictámenes (mirrors resumidos):** NORMA-AGENTES, GITHUB, EXEC-GATE, DOC-CENT, KNOW-001, AGENTES-OPCIONES, SERVIDOROPS, MEDICION-TOKENS (+ stub/DRAFT almacenamiento).  
**Reglas:** VERACIDAD-TOTAL, ESCALADA-TEMATICA.  
**Inventarios:** Lot A/B/C bajo `docs/nortiqa-lab/logs/`.  
**Specs:** `NOTION-REDIRECT-TEMPLATE.md` (+ `templates/notion-redirect.md`).  
**Pack:** `scripts/pack-for-remote.sh` · `apply.sh`.

Inventario consolidado: [`MIGRATION-INVENTORY.md`](MIGRATION-INVENTORY.md)

## Cómo aplicar

Ver [`APPLY.md`](APPLY.md). El bot no pudo crear el repo remoto (`403 createRepository`).

## Gobernanza

- Autoridad final: Gio
- Auditoría: Claude / ARCHITECT-001
- Preparación: KNOW-001
- Implementación: NL-BUILDER / Cursor
- Redirects Notion Centro Doc Madre: solo con autorización Gio + PAO/OT

No Notion deletes. No cuerpos Valent/LLA en este seed.
