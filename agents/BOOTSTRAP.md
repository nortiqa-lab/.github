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
| Production | `https://nortiqalab.com` |
| API health | `https://api.nortiqalab.com/health` |
| n8n | `https://n8n.nortiqalab.com/` |
| MCP | `https://mcp.nortiqalab.com/` (401 expected) |
| Canon root | Notion `MEM-NL-ROOT-001` |

## Confirmed operating rules (from prior versionable docs)

- Native AI memory ≠ source of truth.
- Notion is canon when available.
- Writing to canon requires PAO/OT + Gio authorization.
- Do not mix Nortiqa / Valent / ERP / Surlancer / clients.
- Ollama on VPS stays private: `http://127.0.0.1:11434`.
- Prefer staging checks before prod changes.

## Known open OPS blockers (as of last handoffs)

- **Generación 4 wrapper root (2026-08-02):** installed + restore point verified — see `docs/dev/GEN4-WRAPPER-ROOT-CLOSEOUT.md`. Residual opcional: restart pilot si hace falta reload de `intent_router.py`. Previews siguen en loopback. No mezclar con A14/E6C/portal.
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
