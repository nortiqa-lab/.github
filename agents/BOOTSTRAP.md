# Bootstrap packet — Notion unavailable

Use when `MEM-NL-ROOT-001` cannot be read. Does **not** replace canon.

## Operating identity

You are working in **Nortiqa Lab**, an AI agent factory based in Río Gallegos, Patagonia.

Guiding principle:

> Primero funcional. Después excelente. Siempre: lo mejor o nada.

## Known public map

| Piece | Location |
|-------|----------|
| Org profile / this kit | `nortiqa-lab/.github` |
| Working repo | `giovanyalbea-dotcom/nortiqa-lab` |
| Public pages | `nortiqa-lab/nortiqa-lab.github.io` |
| Production site (SC2027 VPS) | `https://nortiqalab.com` |
| API health (SC2027) | `https://api.nortiqalab.com/health` |
| n8n (SC2027) | `https://n8n.nortiqalab.com/` |
| MCP (SC2027) | `https://mcp.nortiqalab.com/` (401 expected) |
| ERP Odoo / Nerva (`ERP-Nortiqa-Lab` VPS) | `https://erp.nortiqalab.com/` |
| Metabase BI (ERP VPS) | `https://bi.nortiqalab.com/` |
| n8n on ERP VPS | `https://flow.nortiqalab.com/` |
| Canon root | Notion `MEM-NL-ROOT-001` |

Two Nortiqa VPS labels coexist:

- **SC2027** → `5.161.81.43` (site / api / n8n / mcp; also hosts LLA portal at `sc2027.nortiqalab.com` — keep isolated)
- **ERP-Nortiqa-Lab** → `157.90.163.94` (Odoo + Metabase + `flow` n8n)

ERP ops runbooks: `agents/runbooks/erp-nortiqa-lab-health.md`, `agents/runbooks/erp-nortiqa-lab-readiness.md`.

## Confirmed operating rules (from prior versionable docs)

- Native AI memory ≠ source of truth.
- Notion is canon when available.
- Writing to canon requires PAO/OT + Gio authorization.
- Do not mix Nortiqa / Valent / ERP / Surlancer / clients.
- Ollama on VPS stays private: `http://127.0.0.1:11434`.
- Prefer staging checks before prod changes.

## Known open OPS blockers (as of last handoffs)

- Login portal package ready; install needs root/`sc2027`.
- `/opt/sc2027/.env` permissions hardening needs privileged user.
- Nginx scanner-path hardening needs privileged write.
- Gio confirmation still needed for Hetzner snapshot + token rotation where applicable.
- `/app/` not server-side protected yet.

Treat these as **unverified until re-checked** if more than a few days old.

## Workflow without Notion

1. Read `AGENTS.md`, `SHARED_RULES.md`, `AUTONOMY.md`, role sheet.
2. Read latest local handoff.
3. Execute only green/yellow work.
4. Label outputs draft.
5. Leave handoff + exact next human/privileged step if blocked.
