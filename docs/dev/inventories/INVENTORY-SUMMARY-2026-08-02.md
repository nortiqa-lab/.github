Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Fecha: 2026-08-02  
Fuente CSV: `notion-git-gap-inventory-2026-08-02.csv` (83 filas seed + agregados)  
Nota: DOC-CENT reportó 241 docs; este CSV **no** relista los 241 — prioriza P0/P1 + exclusiones + agregados. Completar con export Notion.

---

# Resumen inventario Notion → Git / AppFlowy

## Destino canónico (matriz almacenamiento)

Según `TAREA-NL-GOBERNANZA-ALMACENAMIENTO-001` (DEV; Gio ratificó matriz):

| Estado | Sistema |
|--------|---------|
| PROD docs | GitHub privado `nortiqa-lab/governance` (carpetas por entidad) |
| DEV / tareas con estado | AppFlowy / Notion |
| Externos + financiero/legal | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |

**Hecho:** el repo `nortiqa-lab/governance` **no existe** aún (org solo tiene `.github` + `github.io`).

## Conteos (seed CSV)

| Priority | N |
|----------|---|
| P0 | 14 |
| P1 | 27 |
| P2 | 27 |
| P3 | 2 |
| EXCLUDE | 13 |

| in_git | N |
|--------|---|
| no | 78 |
| partial | 3 |
| yes | 2 |

## P0 — crear / versionar ya (post-dictamen)

1. Crear repo privado `nortiqa-lab/governance` (+ CODEOWNERS / branch protection — Gio).
2. Mirror canon NL: Manifiesto (dedupe), PAO protocol, Prompt Maestro (dedupe), Índice Reglas, Checklist pre-flujo, MEM-NL-ROOT.
3. Versionar esta tarea de almacenamiento + obtener URL de `DICT-NL-GOBERNANZA-ALMACENAMIENTO-001` (ausente en Notion).
4. Crear repos faltantes de DICT-NL-GITHUB-REPOS **o** diferir formalmente: `infra`, `n8n-workflows`, `queryos`.

## P1 — siguiente oleada

- PLAN/DICT GitHub, MEM, SERVIDOROPS, NORMA-AGENTES, DOC-CENT, IDENTITY.
- AppFlowy: PLAN-AF-MIG, TAREA-ORDEN, INT bridge + OpenAPI VPS.
- SC2027 planes DEV (solo a `docs/sc2027/` si Gio confirma carpeta operativa).
- Gen4 ADR-040/L3/botctl desde VPS.
- DB-NL-KNOW schema + CSV sanitizado.
- GOV-NL-DOCUMENTACION-CANONICA-001.

## Exclusiones / gates

| Entity | Ejemplos | Acción |
|--------|----------|--------|
| VALENT | LOG-NL-VALENT-EVO, PAO Valent, DOC-VAL-CV | EXCLUDE de Git NL |
| LLA | PROMPT-ORG-LLA-SC | EXCLUDE |
| SURLANCER | convenio / fusión / company design | gate Gio |
| PERSONAL | Drive PC/HP Gio | EXCLUDE |
| AMBIGUOUS | ERP-ODOO+LLA, Jairo MVP | gate Gio |

## AppFlowy — mapeo de fase (seed)

| Fase | Uso del inventario |
|------|--------------------|
| F0 | Inventario + backup + repos + estructura (`TAREA-ORDEN`) |
| F1–F2 | Canon NL + gobernanza |
| F3 | Inventarios / DB-KNOW rebuild |
| F4 | Ops n8n |
| F5 | Tecnología / SC2027 selectivo |
| F6 | Histórico útil |
| skip/blocked | Deprecated, entity cross, ambiguos |

## Gaps críticos

1. `DICT-NL-GOBERNANZA-ALMACENAMIENTO-001` página no encontrada — pedir texto/URL a Gio.  
2. Duplicados Manifiesto y Prompt Maestro.  
3. ~30 ambiguos DOC-CENT sin clasificar en este seed.  
4. Folder DEV Propuestas: ~90+ páginas — triage batch pendiente.  
5. Gen4 solo en VPS.

## Próximo paso

Claude usa este resumen + CSV + brief `BRIEF-DICT-NOTION-GIT-APPFLOWY-001.md` para emitir dictámenes de alcance; Gio confirma exclusiones Sur Lancer/SC2027 carpeta.
