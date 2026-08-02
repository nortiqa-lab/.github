# AI Session Handoff - 2026-08-02 - Home polish apply-prep

## Metadata

- Date: 2026-08-02
- Project: Nortiqa Lab
- AI actor: Cursor / `NL-BUILDER` (+ `NL-OPS` docs posture)
- Responsible user: Gio
- State: draft / parked (web untouched)

## Canon Read

- MEM-NL-ROOT-001: unavailable — Notion MCP `needsAuth`
- Bootstrap used

## Assumptions

- Gio ordered advance **without modifying the web** → docs/dry-run/apply prep only.
- Visual package from PR #11 remains frozen (`index.html` / CSS / nav.js not edited this turn).

## Work Completed

1. Read-only probe of WP theme paths on `nortiqalab.com`.
2. Wrote `COPY-DIFF.md` (live → polish string map).
3. Expanded `APPLY.md` with dry-run + privileged gates (documented, not executed).
4. Added `scripts/check_package.py` integrity dry-run.
5. Added `docs/dev/HOME-POLISH-APPLY-READY.md`.

## Files or Pieces Changed

- `exports/nortiqa-home-polish/COPY-DIFF.md` (new)
- `exports/nortiqa-home-polish/APPLY.md`
- `exports/nortiqa-home-polish/README.md`
- `exports/nortiqa-home-polish/scripts/check_package.py` (new)
- `docs/dev/HOME-POLISH-APPLY-READY.md` (new)
- `docs/dev/CHANGELOG-DEV.md`
- this handoff

## Verification

- Commands run:
  - `python3 exports/nortiqa-home-polish/scripts/check_package.py`
  - `python3 -m unittest discover -s exports/nortiqa-home-polish/tests -p 'test_*.py'`
  - read-only curls to theme paths / homepage
- Result: recorded after run in session
- Limitations: cannot list real VPS theme directory; PHP paths inferred

## Blockers

- Live theme write still needs Gio + OPS authorization.
- Exact on-host theme path still `PENDIENTE DE VALIDACIÓN`.

## Risks

- Low: docs drift if live theme changes before apply.
- Medium: apply without backup could be hard to reverse — checklist mandates tarball first.

## Next Safe Step

- When Gio unblocks: run dry-run locally, then OPS backup+port per `APPLY.md` (still no agent auto-deploy).
