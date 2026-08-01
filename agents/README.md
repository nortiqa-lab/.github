# Nortiqa Lab — Equipo de Agentes (autónomo)

Status: **operational kit v1** (versionable; Notion canon still separate)  
Scope: Nortiqa Lab only

## Qué es esto

Kit para que agentes Cursor/Cloud **arrancen en frío y operen solos**: reglas, autonomía, prompts autocontenidos, runbooks y handoffs.

Gio da un objetivo en una línea. El agente no pide permiso para lo verde.

## Arranque rápido

1. Pegá un prompt de [`prompts/`](./prompts/) **o** dejá que el repo use [`/AGENTS.md`](../AGENTS.md) y asuma `NL-ORCH`.
2. Objetivo en una frase.
3. El agente sigue el solo loop → verifica → deja handoff.

Guía: [`LAUNCH.md`](./LAUNCH.md) · Cold start: [`runbooks/cold-start.md`](./runbooks/cold-start.md)

## Roster

| Código | Rol | Job |
|--------|-----|-----|
| `NL-ORCH` | Orquestador | Clasifica, despacha, consolida |
| `NL-AUDITOR` | Gobernanza | Gates PAO/OT |
| `NL-BUILDER` | Implementación | PRs reversibles |
| `NL-OPS` | Server ops | Health, staging, prepare prod |
| `NL-PRODUCT` | Producto | Superficies públicas |
| `NL-MEMORY` | Memoria | Continuidad |

- Reglas: [`SHARED_RULES.md`](./SHARED_RULES.md)
- Autonomía: [`AUTONOMY.md`](./AUTONOMY.md)
- Bootstrap sin Notion: [`BOOTSTRAP.md`](./BOOTSTRAP.md)
- Despacho: [`DISPATCH.md`](./DISPATCH.md)
- Roles: [`roles/`](./roles/)
- Runbooks: [`runbooks/`](./runbooks/)

## Hard rules (resumen)

1. Canon Notion primero; si no, bootstrap + draft.
2. Aislamiento de entidades.
3. Sin secretos.
4. Piezas protegidas solo con autorización Gio + PAO/OT.
5. Handoff obligatorio al cerrar sesiones sustanciales.
6. No stall: si es verde, ejecutar.

## Relación con otros repos

- Este repo: perfil org + kit autónomo.
- Trabajo/product/ops scripts: `giovanyalbea-dotcom/nortiqa-lab`.
- Prod: VPS SC2027 / `nortiqalab.com`.
