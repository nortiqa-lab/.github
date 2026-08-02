# telegram-bridge NL kit (staging drop-in)

Status: **versionable staging kit** — not live on the VPS until applied  
Bot: [@NortiqaServidorOpsBot](https://t.me/NortiqaServidorOpsBot)  
Host target (out of git): `/home/deploy/sc2027-staging/telegram-bridge/`  
Unit: `sc2027-telegram-agent.service`

This package implements the NL-* router/autonomy/contracts/ops handlers described in:

- `agents/channels/TELEGRAM.md`
- `agents/channels/telegram-bridge.manifest.proposed.yaml`

It does **not** include the Telegram token. It does **not** deploy itself.

## What you get

| Path | Purpose |
|------|---------|
| `nl/` | Pure Python modules: route → gate → handle → format |
| `sync-nl-kit.sh` | Mirror `AGENTS.md` + `agents/` prompts into `nl-kit/` |
| `apply-staging.sh` | Dry-run by default; copies kit onto staging host path when `APPLY=1` |
| `env.example` | Allowlist + paths (no secrets) |
| `tests/` | Offline unit tests (no network required except optional ops live check) |

## Local verify (safe)

```bash
cd server-ops/sc2027/telegram-bridge
python3 -m unittest discover -s tests -v
./sync-nl-kit.sh
python3 -m nl.service --self-test
```

## Staging apply (human on VPS)

See `APPLY.md`. Requires Gio + staging window. Never prod from this kit.
