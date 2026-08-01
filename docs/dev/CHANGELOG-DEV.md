# Changelog DEV — Cursor configuration execution

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## 2026-08-01 — Cursor local kit + docs/dev

### Added

- `.cursor/README.md`
- `.cursor/rules/00-nortiqa-governance.mdc`
- `.cursor/rules/10-project-context.mdc`
- `.cursor/rules/20-development-standards.mdc`
- `.cursor/rules/30-security-and-secrets.mdc`
- `.cursor/rules/40-testing-and-validation.mdc`
- `.cursor/rules/50-git-and-version-control.mdc`
- `.cursor/rules/60-documentation-and-traceability.mdc`
- `.cursor/rules/70-infrastructure-safety.mdc`
- `docs/dev/CURSOR-OPERATING-GUIDE.md`
- `docs/dev/REPOSITORY-AUDIT.md`
- `docs/dev/DEVELOPMENT-WORKFLOW.md`
- `docs/dev/TESTING-CHECKLIST.md`
- `docs/dev/CHANGELOG-DEV.md` (this file)
- Session handoff under `docs/shared-ai-memory/handoffs/`

### Changed

- `AGENTS.md` — integrated Cursor rules pointers, command inventory (evidence-only), NQ-DEV-IMPLEMENTER mapping, completion/report format; preserved Rule 0 and `NL-*` roster

### Not changed

- Production systems, secrets, VPS, DNS, Docker (none present), product application code
- Notion canon (unavailable / not written)
- Role kit filenames under `agents/` (mapped, not renamed)

### Session close

- 2026-08-01: Gio ordered session closeout (`cerra todo`). Handoff marked **closed**. PR #3 left open as draft for human merge.

### Follow-up — “hace todo” (same day)

- Merged PR #3 into `main` (`eabc344`)
- Notion MCP still unauthenticated in agent environment (human action)
- Product-repo push blocked (403); added `exports/nortiqa-lab-product-cursor-kit/` apply package
