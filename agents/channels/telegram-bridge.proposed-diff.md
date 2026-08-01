# Proposed VPS diff (not applied)

Target host paths are staging-only. Apply only after Gio review + staging change window.  
No production. No token changes required for the NL wiring itself.

## 1) Manifest

File: `/home/deploy/sc2027-staging/docs/bots/telegram-bridge.yaml`

- Merge keys from `agents/channels/telegram-bridge.manifest.proposed.yaml` in this repo.
- Keep existing bot/token/env wiring intact.
- Add `nl_kit`, `routing`, `autonomy`, `runtime.handoff`, `safety` blocks.

## 2) Kit mirror (read-only)

New dir: `/home/deploy/sc2027-staging/telegram-bridge/nl-kit/`

One-time (or cron) sync idea:

```bash
# staging host, as deploy — illustrative only
mkdir -p /home/deploy/sc2027-staging/telegram-bridge/nl-kit
# preferred: git sparse checkout / archive of nortiqa-lab/.github@main
# copy AGENTS.md + agents/ + docs/shared-ai-memory/handoff-template.md
```

Bridge must fail closed with a clear Telegram reply if mirror missing.

## 3) Code additions under `telegram-bridge/`

Proposed new modules (names illustrative):

| Path | Responsibility |
|------|----------------|
| `nl/router.py` | Map commands/free text → `NL-*` |
| `nl/autonomy.py` | Green/yellow/red using allowlists |
| `nl/contracts.py` | Format ROLE/DONE/VERIFY/BLOCKED/NEXT |
| `nl/kit.py` | Load mirrored prompt files |
| `nl/handlers/ops.py` | Enumerated staging-safe actions only |

Minimal behavior change for existing message handler:

1. Auth allowlist (unchanged/enforced).
2. `role = route(message)`.
3. If red → reply blocked + exact next human step.
4. If green OPS allowlisted → run tool → reply contract.
5. Else → build response from role system prompt + user goal (Ollama optional) **or** return a Cursor-ready brief without executing.
6. Persist handoff stub.

## 4) Systemd unit

Unit: `sc2027-telegram-agent.service`

Proposed env additions (values set on host, not in git):

```
TELEGRAM_ALLOWED_USER_IDS=...
TELEGRAM_ALLOWED_CHAT_IDS=...
NL_KIT_PATH=/home/deploy/sc2027-staging/telegram-bridge/nl-kit
NL_HANDOFF_DIR=/home/deploy/sc2027-staging/docs/shared-ai-memory/handoffs
NL_DEFAULT_ROLE=NL-ORCH
```

Restart only after staging validation. Do not touch prod units.

## 5) Verification plan (staging)

1. `/help` → command list.
2. `/status` → unit + kit mirror present + no secrets.
3. `/ops health` → public/staging health evidence.
4. `/audit promote prod` → BLOCK (red), no action.
5. Unknown user → rejected.
6. `/orch resume login portal` → plan + NEXT pointing at privileged install, no auto-run.

## 6) Explicit non-goals

- No `docker.sock` expansion.
- No prod promote from chat.
- No Notion protected writes.
- No commit of token or allowlist IDs into GitHub.
