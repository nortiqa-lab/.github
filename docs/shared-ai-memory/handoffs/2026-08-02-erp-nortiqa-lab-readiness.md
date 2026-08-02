# AI Session Handoff — ERP-Nortiqa-Lab readiness

## Metadata

- Date: 2026-08-02
- Project: Nortiqa Lab
- AI actor: `NL-OPS` (Cursor Cloud)
- Responsible user: Gio
- State: blocked (privileged access + Metabase pause + Odoo credentials)

## Canon Read

- MEM-NL-ROOT-001: unavailable (bootstrap used)
- Active plans: none read
- Applicable OT/PAO: none
- Outputs: **draft**

## Assumptions

- `erp.nortiqalab.com` on host label **ERP-Nortiqa-Lab** (`157.90.163.94`) is Nortiqa-owned production ERP (Odoo 18 / Nerva), distinct from entity “ERP Gio+Edson”.
- Gio asked to continue with production ERP so Nortiqa can operate it.
- SC2027 portal remains LLA’s work platform and stays isolated.

## Work Completed

- Measured ERP stack public health (script + manual).
- Documented dual-VPS map (SC2027 vs ERP-Nortiqa-Lab) in bootstrap/governance/project context.
- Added runbooks + executable healthcheck for ERP-Nortiqa-Lab.
- Clarified isolation: Nortiqa ERP host ≠ ERP Gio+Edson ≠ LLA SC2027 portal.

## Files or Pieces Changed

- `agents/scripts/erp-nortiqa-lab-healthcheck.sh`
- `agents/runbooks/erp-nortiqa-lab-health.md`
- `agents/runbooks/erp-nortiqa-lab-readiness.md`
- `agents/runbooks/ops-public-health.md`
- `agents/BOOTSTRAP.md`, `agents/AUTONOMY.md`, `agents/SHARED_RULES.md`, `agents/roles/NL-OPS.md`
- `AGENTS.md`, `.cursor/rules/00-nortiqa-governance.mdc`, `.cursor/rules/10-project-context.mdc`
- this handoff

## Verification

```text
./agents/scripts/erp-nortiqa-lab-healthcheck.sh
```

Result (2026-08-02 UTC):

| Check | Result |
|-------|--------|
| Odoo `/web/health` | OK (`pass`) |
| Odoo login | OK 200 |
| Odoo serie | OK `18.0` (`18.0-20260630`) |
| flow n8n `/healthz` | OK |
| Metabase `bi` | **FAIL** — `503` body `Metabase paused on ERP-Nortiqa-Lab` |

Also confirmed: DB list denied; default `admin/admin` auth false; no agent credentials in environment; no push access to `giovanyalbea-dotcom/nortiqa-lab` for host-side `server-ops` mirror.

## Blockers

Human/privileged actions required:

1. Unpause Metabase on **ERP-Nortiqa-Lab**, then re-run healthcheck (expect `bi` 200).
2. Provide Nortiqa Odoo admin (or vaulted credentials) so company baseline can be configured.
3. Confirm SSH/panel user for `157.90.163.94` to install host-side OPS kit analogous to `server-ops/sc2027`.
4. Optional: grant write access / apply mirror so product repo gets `server-ops/erp-nortiqa-lab/`.

## Risks

- Dual n8n (`n8n.nortiqalab.com` on SC2027 vs `flow.nortiqalab.com` on ERP host) can confuse automations if not labeled.
- Operating without Metabase leaves BI blind.
- Without admin login, ERP cannot be “operated” beyond uptime checks.

## Next Safe Step

Gio: unpause Metabase on ERP-Nortiqa-Lab and share Odoo admin access path (vault/invite); agent re-runs `./agents/scripts/erp-nortiqa-lab-healthcheck.sh` and continues checklist section C in `agents/runbooks/erp-nortiqa-lab-readiness.md`.
