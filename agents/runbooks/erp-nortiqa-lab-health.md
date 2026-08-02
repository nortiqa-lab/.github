# Runbook — ERP-Nortiqa-Lab public health (no SSH)

Non-destructive checks for the **Nortiqa Lab ERP stack** on VPS host label
`ERP-Nortiqa-Lab` (`157.90.163.94`).

This is **not** “ERP Gio+Edson” (separate entity). Do not mix contexts.

## Surfaces

| Host | Role |
|------|------|
| `https://erp.nortiqalab.com` | Odoo 18 (UI brand **Nerva**) |
| `https://bi.nortiqalab.com` | Metabase (BI) |
| `https://flow.nortiqalab.com` | n8n on the ERP host |

TLS SAN on this host currently covers: `erp`, `bi`, `flow` (`.nortiqalab.com`).

> Note: `https://n8n.nortiqalab.com` resolves to **SC2027** (`5.161.81.43`), a different VPS. Do not treat it as the ERP-host n8n.

## Commands

```bash
./agents/scripts/erp-nortiqa-lab-healthcheck.sh
```

Or manual:

```bash
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://erp.nortiqalab.com/web/health
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://erp.nortiqalab.com/web/login
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://bi.nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://flow.nortiqalab.com/healthz
curl -sS https://erp.nortiqalab.com/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"version","args":[]},"id":1}'
```

## Expected (healthy)

| Check | Expect |
|-------|--------|
| Odoo `/web/health` | `200` + `{"status": "pass"}` |
| Odoo `/web/login` | `200` (Nerva login) |
| Odoo jsonrpc `version` | `server_serie` `18.0` |
| Metabase `/` | `200` (not paused) |
| flow n8n `/healthz` | `200` + `{"status":"ok"}` |

## Known degraded signals

| Signal | Meaning |
|--------|---------|
| Metabase body `Metabase paused on ERP-Nortiqa-Lab` + `503` | BI container/app paused — unpause on host |
| Odoo login `200` but no operator credentials | Stack up; Nortiqa cannot operate yet |
| Database manager “disabled by administrator” | Expected hardening; not a failure |

Record codes in the session handoff. Do not POST real credentials unless Gio ordered a controlled auth test.
