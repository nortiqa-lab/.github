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
