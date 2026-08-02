# Testing Checklist — nortiqa-lab/.github

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Scope note

This repository has **no application test runner**. Checks below match the detected stack (Markdown kit + Git + optional public health GETs).

## A. Pre-change

- [ ] `git status --short` reviewed; unrelated changes preserved
- [ ] Current branch identified (prefer feature branch over bare `main`)
- [ ] Role / mode / risk declared
- [ ] Latest handoff skimmed if present

## B. Content / structure (this repo)

- [ ] New/changed paths referenced in docs actually exist
- [ ] No duplicate conflicting canon files introduced
- [ ] Draft banner present on new `docs/dev/*` files
- [ ] Entity isolation preserved (no Valent/ERP/client contamination)
- [ ] Role mapping consistent (`NL-*` kit preserved; external labels mapped)
- [ ] `.cursor/rules/*.mdc` have YAML frontmatter (`description` / `alwaysApply`)

## C. Security

- [ ] Diff contains no secrets, tokens, private keys, or `.env` values
- [ ] No credentialed URLs with embedded secrets
- [ ] Handoff has no secrets

## D. Optional public health (read-only)

From `agents/runbooks/ops-public-health.md` — only if network allowed and task needs it:

- [ ] `https://nortiqalab.com/` → expect 200
- [ ] `https://api.nortiqalab.com/health` → expect 200
- [ ] `https://n8n.nortiqalab.com/` → expect 200
- [ ] `https://mcp.nortiqalab.com/` → expect 401

Do **not** treat health GETs as license to change production.

## D2. Telegram NL bridge kit (this repo)

```bash
cd server-ops/sc2027/telegram-bridge
PYTHONPATH=. python3 -m unittest discover -s tests -v
./sync-nl-kit.sh
PYTHONPATH=. python3 -m nl.service --self-test
./apply-staging.sh   # dry-run only unless APPLY=1 on staging host
```

- [ ] Unit tests pass
- [ ] `sync-nl-kit.sh` completes
- [ ] `--self-test` ok
- [ ] No token / allowlist secrets committed

## E. Product repo (when applicable)

Mark all as `PENDIENTE DE VALIDACIÓN` until discovered in `giovanyalbea-dotcom/nortiqa-lab`:

- [ ] Install command — `PENDIENTE DE VALIDACIÓN`
- [ ] Unit / integration tests — `PENDIENTE DE VALIDACIÓN`
- [ ] Lint / format — `PENDIENTE DE VALIDACIÓN`
- [ ] Staging deploy checks — `PENDIENTE DE VALIDACIÓN`

## F. Completion

- [ ] Commands run listed with results
- [ ] Failures classified: pre-existing vs introduced
- [ ] Task not marked done if introduced checks fail
- [ ] One next safe step recorded
