# Runbook — Despacho desde Telegram

Bot: [@NortiqaServidorOpsBot](https://t.me/NortiqaServidorOpsBot)  
Design: `agents/channels/TELEGRAM.md`

## When Gio messages the bot

1. Bridge authenticates allowlist.
2. Route command → `NL-*` (default `NL-ORCH`).
3. Apply autonomy zones from `AUTONOMY.md`.
4. Reply with NL output contract.
5. Persist handoff stub on staging docs path.

## Recommended first messages after wiring

```
/help
/status
/ops health
/orch ¿qué queda pendiente del login portal?
/audit ¿puedo promote a prod desde acá?
```

Expect the last one to **BLOCK**.

## If kit mirror missing

Bot should reply that `nl-kit` sync is required from `nortiqa-lab/.github@main`, then stop.

## Versionable kit

Code + apply path: `server-ops/sc2027/telegram-bridge/`  
See `APPLY.md` there. Local:

```bash
cd server-ops/sc2027/telegram-bridge
PYTHONPATH=. python3 -m unittest discover -s tests -v
./sync-nl-kit.sh
PYTHONPATH=. python3 -m nl.service --self-test
```
