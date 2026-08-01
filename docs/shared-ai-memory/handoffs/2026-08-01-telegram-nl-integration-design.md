# AI Session Handoff - 2026-08-01 - Telegram ↔ NL-* integration design

## Metadata

- Date: 2026-08-01
- Project: Nortiqa Lab agent channels
- AI actor: NL-ORCH / NL-OPS design (Cursor Cloud)
- Responsible user: Gio
- State: draft ready for review

## Canon Read

- MEM-NL-ROOT-001: unavailable here → bootstrap-draft
- Local kit: `AGENTS.md`, `agents/AUTONOMY.md`, `agents/DISPATCH.md`
- Bot facts provided by Gio (trusted input for this design):
  - `@NortiqaServidorOpsBot` / https://t.me/NortiqaServidorOpsBot
  - code: `/home/deploy/sc2027-staging/telegram-bridge/`
  - unit: `sc2027-telegram-agent.service`
  - manifest: `/home/deploy/sc2027-staging/docs/bots/telegram-bridge.yaml`
  - not in GitHub `nortiqa-lab` working repo

## Assumptions

- No VPS access this turn; design only.
- Bot remains staging-first; prod promote still separate PAO.
- Token never enters git/chat.
- Public Telegram page title observed: `ServidorOpsNortiqaBot` (no useful description beyond contact).

## Work Completed

- Wrote channel design: Telegram as ingress/notify into NL-* roster.
- Defined command → role map (`/orch`, `/ops`, `/build`, `/product`, `/audit`, `/memory`).
- Mapped autonomy green/yellow/red onto bridge behavior.
- Proposed manifest overlay YAML + VPS diff checklist (not applied).
- Added Telegram dispatch runbook + LAUNCH/README pointers.

## Files or Pieces Changed

- `agents/channels/TELEGRAM.md`
- `agents/channels/telegram-bridge.manifest.proposed.yaml`
- `agents/channels/telegram-bridge.proposed-diff.md`
- `agents/runbooks/telegram-dispatch.md`
- `agents/README.md`
- `agents/LAUNCH.md`
- `docs/shared-ai-memory/handoffs/2026-08-01-telegram-nl-integration-design.md`

## Verification

- Commands run: public `t.me/NortiqaServidorOpsBot` fetch (title only); no VPS SSH; no token use
- Result: design package complete in-repo
- Limitations: could not read live `telegram-bridge.yaml` or service state on SC2027

## Blockers

- Human review of proposed routing/autonomy
- Staging apply (later): merge manifest, sync `nl-kit`, add router modules, set allowlist env, restart staging unit
- Still no privileged login-portal / prod promote from chat

## Risks

- Existing bridge code shape unknown; module paths in proposed diff are illustrative and need adapt-on-read
- If allowlist missing when enabling NL router, risk of open commands — keep allowlist_only=true as hard requirement
- Ollama draft replies can drift from tools; prefer enumerated OPS tools for `/ops`

## Next Safe Step

Gio reviews `agents/channels/TELEGRAM.md` + proposed YAML; if approved, schedule a **staging-only** change window to merge manifest and add router against the live `telegram-bridge/` tree (still no prod).
