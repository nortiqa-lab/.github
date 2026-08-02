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

**Implemented in-repo** at `server-ops/sc2027/telegram-bridge/` (copy with `apply-staging.sh`).

| Path | Responsibility |
|------|----------------|
| `nl/router.py` | Map commands/free text → `NL-*` |
| `nl/autonomy.py` | Green/yellow/red using allowlists |
| `nl/contracts.py` | Format ROLE/DONE/VERIFY/BLOCKED/NEXT |
| `nl/kit.py` | Load mirrored prompt files |
| `nl/auth.py` | Allowlist fail-closed |
| `nl/adapter.py` | `handle_telegram_text` for existing bot app |
| `nl/handlers/ops.py` | Enumerated public health |
| `nl/handlers/bridge.py` | `/help` `/status` |

Minimal behavior change for existing message handler:

1. Auth allowlist (enforced fail-closed when env empty).
2. `reply = handle_telegram_text(text, user_id=..., chat_id=...)`.
3. Red → blocked + exact next human step.
4. Green OPS health → live curls + contract.
5. Else → Cursor-ready brief from mirrored prompts (no host mutate).
6. Optional handoff stub via `NL_HANDOFF_DIR`.

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
