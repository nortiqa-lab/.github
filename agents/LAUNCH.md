# Launch kit — agents that run alone

## Fast path

1. Open a new Cursor Cloud / Agent chat on this repo (`nortiqa-lab/.github`).
2. Paste **one** prompt from `agents/prompts/NL-*.md` (already self-contained).
3. Give a one-line goal.
4. Let it run the solo loop end-to-end.

If you do not pick a role, paste `prompts/NL-ORCH.md` — it self-dispatches.

## Recommended default team for general work

| Goal type | Launch |
|-----------|--------|
| Anything unclear | `NL-ORCH` |
| Code/docs PR | `NL-BUILDER` |
| Site/brand | `NL-PRODUCT` |
| Server/health/promote | `NL-OPS` |
| “Can we touch Notion/prod?” | `NL-AUDITOR` |
| Continuity / close session | `NL-MEMORY` |

## Multi-agent without babysitting

`NL-ORCH` may:

1. Split the goal into ≤3 role briefs.
2. Execute the highest-leverage role itself **or** emit ready-to-paste prompts for siblings.
3. If operating inside one session with subagents, run them sequentially unless truly independent.
4. Consolidate one final handoff.

## Done means

- PR updated or explicit no-op with reason.
- Verification recorded.
- Handoff written under `docs/shared-ai-memory/handoffs/`.
- If blocked, the handoff contains the **exact** Gio/root action needed — not a vague “needs access”.

## Telegram channel (staging bot)

Bot: [@NortiqaServidorOpsBot](https://t.me/NortiqaServidorOpsBot)

Telegram is ingress/notify only.

- Design: `agents/channels/TELEGRAM.md`
- Manifest overlay: `agents/channels/telegram-bridge.manifest.proposed.yaml`
- **Staging kit (code):** `server-ops/sc2027/telegram-bridge/`
- Apply guide: `server-ops/sc2027/telegram-bridge/APPLY.md`
- Runbook: `agents/runbooks/telegram-dispatch.md`

Local verify:

```bash
cd server-ops/sc2027/telegram-bridge
PYTHONPATH=. python3 -m unittest discover -s tests -v
./sync-nl-kit.sh
PYTHONPATH=. python3 -m nl.service --self-test
```

Do not paste tokens into Cursor or git. Production bot promote still needs separate PAO.
