# nortiqa-lab/governance

Estado: DEV / Borrador (seed)

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Repositorio **privado** destinado a documentación **PROD (ratificada)** del ecosistema multi-entidad, según la matriz de almacenamiento autorizada por Gio.

Prompt KNOW-001 (ajustado):  
https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558

## Matriz de almacenamiento

| Estado / tipo | Destino |
|---|---|
| Ratificado (PROD) | Este repo — `docs/[entidad]/[tipo]/` |
| DEV — tarea/seguimiento con estados | AppFlowy / Notion (base de datos) |
| DEV — página de trabajo | AppFlowy / Notion (página) |
| Entregables externos + financieros/legales | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |

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
| `docs/valent-capital/` | Valent Capital Group S.A. |
| `docs/lla-santa-cruz/` | LLA Santa Cruz |
| `docs/sc2027/` | Operativa de plataforma/host SC2027 (no implica persona jurídica) |
| `docs/transversal/` | Docs que aplican por igual a todas las entidades |

**Regla dura:** nunca mezclar documentos de una entidad en la carpeta de otra.  
Si el prefijo de entidad no es claro → preguntar a Gio antes de ubicar.

### Tipos de carpeta (por entidad)

`dictamenes/` · `auditorias/` · `governance/` · `specs/` · `sops/` · `logs/` · `planes/`  
(`adr/` solo en Nortiqa Lab por ahora)

## Naming

Convención existente:

- `DICT-[ENTIDAD]-xxx-001.md`
- `REGLA-[ENTIDAD]-xxx-001.md`
- `GOV-[ENTIDAD]-xxx-001.md`
- `PLAN-[ENTIDAD]-xxx-001.md`
- `AUD-` / `LOG-` / equivalentes según prefijo vigente

## Supersesión vs PLAN-NL-GITHUB-001

`PLAN-NL-GITHUB-001` (canónico vía `DICT-NL-GITHUB-001`) separa entidades por **repositorio** para código, datos y secretos.

**Este modelo supersede esa regla solo para documentación PROD:** un único repo privado con carpetas por entidad + Teams/CODEOWNERS.

Código, datos y secretos **siguen** en repos separados por entidad.

## Control de acceso

- Repo: **private**
- `CODEOWNERS` por carpeta de entidad (ver `.github/CODEOWNERS`)
- Teams de GitHub: Gio completa membresías (`core-founders`, teams por entidad)
- Branch protection en `main`: require PR + review (Gio / admin org)
- Git flow: PRs por lote de migración; no commits directos a `main`

## Criterio de migración

Solo documentos **ratificados/PROD** o referenciados activamente.  
No migración masiva sin aprobación de Gio.

Inventario inicial: [`MIGRATION-INVENTORY.md`](MIGRATION-INVENTORY.md)  
Plantilla redirect Notion: [`templates/notion-redirect.md`](templates/notion-redirect.md)

## Cómo aplicar este seed

Ver [`APPLY.md`](APPLY.md). Este paquete vive en `nortiqa-lab/.github` porque el bot Cloud Agent **no pudo** crear `nortiqa-lab/governance` (403 `createRepository`).

## Gobernanza

- Autoridad final: Gio
- Auditoría: Claude / ARCHITECT-001
- Preparación documental: KNOW-001
- Implementación técnica: NL-BUILDER / Cursor
- Escrituras en Centro Doc Madre (Notion): solo con autorización Gio + PAO/OT
