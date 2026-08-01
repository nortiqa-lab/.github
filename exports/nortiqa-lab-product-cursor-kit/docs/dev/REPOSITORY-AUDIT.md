# Repository Audit — giovanyalbea-dotcom/nortiqa-lab (mirror prep)

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Metadata

| Field | Value |
|-------|--------|
| Fecha | 2026-08-01 |
| Commit inspeccionado | `f4fc592301bd91afca551b4fcb5859487e44dae9` |
| Inspector | NQ-DEV-IMPLEMENTER / NL-BUILDER |
| Push desde Cloud Agent | **DENIED** (`cursor[bot]` 403) |

## Purpose (evidence)

Working Nortiqa repo: static site, brand assets, Python hero generator, SC2027 ops scripts, shared AI memory docs.

## Stack

HTML · Bash ops · Python 3 · Docker referenced on host · no root Node app manifest

## Gaps addressed by this mirror package

- Missing `.cursor/`
- Missing `agents/` NL-* kit
- Thin Cursor/dev workflow docs

## Risks

- Bot cannot maintain this repo until write access granted
- SC2027 historical naming vs Nortiqa brand
- Full healthcheck scripts require VPS privileges
