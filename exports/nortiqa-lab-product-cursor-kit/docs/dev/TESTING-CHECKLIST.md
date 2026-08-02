# Testing Checklist — product/ops repo

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Pre-change

- [ ] `git status --short`
- [ ] Role/mode/risk declared
- [ ] Entity isolation OK

## Content / site / scripts

- [ ] Referenced paths exist
- [ ] No secrets in diff
- [ ] If hero changed: `python3 scripts/generate_hero.py`

## Public health (safe off-host)

- [ ] `nortiqalab.com` → 200
- [ ] `api.nortiqalab.com/health` → 200
- [ ] `n8n.nortiqalab.com` → 200
- [ ] `mcp.nortiqalab.com` → 401

## On-VPS (privileged / environment-dependent)

- [ ] `bash server-ops/sc2027/healthcheck-staging.sh` — only with access
- [ ] `bash server-ops/sc2027/healthcheck-prod.sh` — only with access

## Completion

- [ ] Commands + results recorded
- [ ] Failures classified pre-existing vs introduced
