# Runbook — Public health checks (no SSH)

Run from any agent with network. Non-destructive.

```bash
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://api.nortiqalab.com/health
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://n8n.nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://mcp.nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://nortiqalab.com/login
```

Expected (historical):

| URL | Expect |
|-----|--------|
| site `/` | 200 |
| api `/health` | 200 |
| n8n `/` | 200 |
| mcp `/` | 401 |
| `/login` | may still be landing until portal install |

Record status codes in the handoff. Do not POST credentials in automated checks unless Gio explicitly ordered a controlled auth test with non-production users.

## ERP-Nortiqa-Lab stack (separate VPS)

Also run when the brief involves Odoo / Metabase / ERP-host n8n:

```bash
./agents/scripts/erp-nortiqa-lab-healthcheck.sh
```

Details: `agents/runbooks/erp-nortiqa-lab-health.md` and readiness checklist `agents/runbooks/erp-nortiqa-lab-readiness.md`.
