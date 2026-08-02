# AI Session Handoff - 2026-08-02 - Telegram bridge NL kit

## Metadata

- Date: 2026-08-02
- Project: Nortiqa Lab / @NortiqaServidorOpsBot
- AI actor: NL-BUILDER / NL-OPS (Cursor Cloud)
- Responsible user: Gio
- State: ready for review / staging-apply pending

## Canon Read

- MEM-NL-ROOT-001: unavailable → bootstrap-draft
- Local: `agents/channels/TELEGRAM.md`, autonomy/dispatch, infra safety rules

## Assumptions

- No VPS SSH this turn; deliver versionable drop-in only
- Existing host bot app remains; we provide `nl.adapter.handle_telegram_text`
- Token never enters git

## Work Completed

- Implemented `server-ops/sc2027/telegram-bridge/` NL layer + tests + sync/apply scripts
- Updated channel docs / LAUNCH / AGENTS pointers / CHANGELOG-DEV
- Ran offline tests + live public health via service CLI

## Files or Pieces Changed

- `server-ops/sc2027/telegram-bridge/**`
- `agents/channels/TELEGRAM.md`
- `agents/channels/telegram-bridge.proposed-diff.md`
- `agents/LAUNCH.md`, `agents/README.md`, `agents/runbooks/telegram-dispatch.md`
- `AGENTS.md`
- `docs/dev/CHANGELOG-DEV.md`
- this handoff

## Verification

- Commands:
  - `PYTHONPATH=. python3 -m unittest discover -s tests -v` → 21 OK
  - `./sync-nl-kit.sh` → complete
  - `python3 -m nl.service --self-test` → ok
  - `python3 -m nl.service --text '/ops health' --user-id 42` with allowlist → public health OK
  - `./apply-staging.sh` → dry-run only
- Limitations: did not restart systemd or edit host manifest

## Blockers

- Human staging window: `APPLY.md` on VPS (copy nl/, merge manifest, allowlist env, wire adapter, restart staging unit)
- Still no privileged login-portal install from chat

## Risks

- Host bot entrypoint shape unknown — adapter call site may need a 3–10 line shim
- Allowlist must be set before enabling adapter or all users get "No autorizado" (fail-closed is intentional)

## Next Safe Step

On staging host, run `APPLY.md` steps 1–9; verify `/help`, `/status`, `/ops health`, and that `/ops promote…` blocks.
