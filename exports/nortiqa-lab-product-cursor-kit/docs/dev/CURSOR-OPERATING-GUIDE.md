# Cursor Operating Guide — product/ops repo

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Mirrored package for `giovanyalbea-dotcom/nortiqa-lab`. Org source: `nortiqa-lab/.github`.

## Boot

1. `AGENTS.md` → `agents/SHARED_RULES.md` → `agents/AUTONOMY.md`
2. Notion `MEM-NL-ROOT-001` or bootstrap + **draft**
3. Latest handoff in `docs/shared-ai-memory/handoffs/`
4. `git status --short`
5. `.cursor/rules/` (auto in Cursor)

## Modes

`INSPECT` · `PLAN` · `IMPLEMENT` · `TEST` · `REVIEW` · `DOCUMENT` · `RECOVERY`

## Caution

`server-ops/sc2027/` touches prod/staging posture. Prefer read-only health first. No promote without gates.
