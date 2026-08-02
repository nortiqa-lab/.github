# Runbook — ERP-Nortiqa-Lab readiness for Nortiqa operations

**Estado:** draft (Notion unavailable). Goal: leave the production ERP stack
usable for day-to-day Nortiqa Lab work.

## Scope

In scope (Nortiqa-owned):

- VPS / compose project label: **ERP-Nortiqa-Lab**
- `erp.nortiqalab.com` — Odoo 18 / Nerva
- `bi.nortiqalab.com` — Metabase
- `flow.nortiqalab.com` — n8n (ERP host)

Out of scope unless Gio explicitly authorizes a cross:

- ERP Gio+Edson
- LLA / SC2027 portal (`sc2027.nortiqalab.com`)
- Valent, Surlancer, other clients

## Readiness checklist

### A. Platform up (agent-measurable, no SSH)

- [ ] Odoo health `GET /web/health` → `pass`
- [ ] Odoo login page loads
- [ ] Odoo reports serie `18.0` via jsonrpc/xmlrpc
- [ ] DB manager list denied / disabled (hardening OK)
- [ ] `flow.nortiqalab.com/healthz` → ok
- [ ] Metabase **not** paused (`bi` → 200)

### B. Operator access (human / privileged)

- [ ] At least one Nortiqa admin user can log into Odoo
- [ ] MFA / password policy decided for Gio (+ Edson if applicable)
- [ ] Agent/automation account (if needed) created with least privilege
- [ ] Credentials stored outside git (password manager / sealed secret store)
- [ ] SSH or panel access to `ERP-Nortiqa-Lab` available to Gio for restore/unpause

### C. Company baseline inside Odoo (after login)

- [ ] Company name / logo / localization (AR) set for **Nortiqa Lab**
- [ ] Multi-company isolation verified (no client DBs mixed in)
- [ ] Required apps installed (Accounting, CRM, Project, etc. — Gio list)
- [ ] Chart of accounts / fiscal year opening decided
- [ ] Outgoing mail configured or explicitly deferred
- [ ] Backup schedule verified on host (snapshot + DB dump)

### D. Adjacent stack

- [ ] Metabase unpaused and pointed at approved Odoo/BI warehouse only
- [ ] ERP-host n8n (`flow`) auth enabled; no public unauthenticated webhooks
- [ ] Clarify dual n8n: `flow.nortiqalab.com` (ERP host) vs `n8n.nortiqalab.com` (SC2027)
- [ ] Document which automations belong on which n8n

## Privileged actions (exact asks for Gio)

When agents lack host access, hand these as copy-paste asks:

1. **Unpause Metabase** on host `ERP-Nortiqa-Lab` (panel/Coolify/Dokploy/docker — whichever owns the pause), then re-run:
   `curl -sS -o /dev/null -w "%{http_code}\n" https://bi.nortiqalab.com/`
2. **Provide Odoo admin access** for Nortiqa (or reset admin and store in vault).
3. **Confirm SSH/deploy user** for `157.90.163.94` so OPS can add host-side healthchecks mirroring `server-ops/sc2027`.
4. **Mirror OPS kit** into product repo `giovanyalbea-dotcom/nortiqa-lab` under e.g. `server-ops/erp-nortiqa-lab/` when write access exists.

## Agent lane (green)

- Public health GETs + version probe
- Keep this runbook / bootstrap map accurate
- Handoffs with measured codes
- Draft checklists for post-login company setup

## Agent lane (red — escalate)

- Logging in with production passwords without Gio order
- Changing Odoo production data, users, or apps without authorization
- Unpausing Metabase / docker / nginx without privileged access + Gio gate
- Mixing ERP Gio+Edson or LLA data into this stack
