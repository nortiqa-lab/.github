# Apply NL telegram-bridge kit to staging

**Scope:** staging only (`/home/deploy/sc2027-staging/telegram-bridge/`)  
**Do not** promote to production without separate PAO.  
**Do not** put the bot token in git.

## Preconditions

- Gio approved the design in `agents/channels/TELEGRAM.md`
- Staging change window
- SSH/session as `deploy` (or appropriate staging user)
- Existing `sc2027-telegram-agent.service` already runs the bot

## Steps

1. Get this package onto the host (git clone of `nortiqa-lab/.github`, scp, or rclone).
2. Dry-run:

```bash
cd server-ops/sc2027/telegram-bridge
./apply-staging.sh
```

3. Apply copy:

```bash
APPLY=1 ./apply-staging.sh
```

4. Merge manifest overlay into  
   `/home/deploy/sc2027-staging/docs/bots/telegram-bridge.yaml`  
   using `agents/channels/telegram-bridge.manifest.proposed.yaml`.

5. Add unit env (host secret store / drop-in), values not committed:

```
TELEGRAM_ALLOWED_USER_IDS=<gio-user-id>
TELEGRAM_ALLOWED_CHAT_IDS=<gio-chat-id>
NL_KIT_PATH=/home/deploy/sc2027-staging/telegram-bridge/nl-kit
NL_HANDOFF_DIR=/home/deploy/sc2027-staging/docs/shared-ai-memory/handoffs
NL_DEFAULT_ROLE=NL-ORCH
NL_HANDOFF_ENABLED=1
```

6. Sync kit prompts (from a checkout of this repo on the host, or copy `nl-kit/` already synced locally):

```bash
cd /home/deploy/sc2027-staging/telegram-bridge
# If scripts expect repo root, run sync from the git checkout path instead.
./sync-nl-kit.sh
```

7. Wire one call site in the existing bot app:

```python
from nl.adapter import handle_telegram_text
reply = handle_telegram_text(text, user_id=str(user_id), chat_id=str(chat_id))
```

8. Restart **staging** unit only:

```bash
sudo systemctl restart sc2027-telegram-agent.service
sudo systemctl status sc2027-telegram-agent.service --no-pager
```

9. Verify in Telegram:

```
/help
/status
/ops health
/orch pending login portal
/audit promote to prod
```

Expect `/audit promote…` / `/ops promote…` to **BLOCK**.

## Rollback

- Remove `nl/` import from the bot entrypoint
- Restart unit
- Keep token/env untouched
