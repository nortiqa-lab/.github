# AI Session Handoff — Cursor visual evidence rule

## Metadata

- Date: 2026-08-02
- Project: Nortiqa Lab (org profile / Cursor config)
- AI actor: `NL-BUILDER` / Cursor Cloud
- Responsible user: Gio
- State: draft / ready for review

## Canon Read

- MEM-NL-ROOT-001: not modified
- Active plans: none for this change
- Applicable OT/PAO: none

## Assumptions

- Gio wants screenshots/short videos as a **general Cursor rule**, not a kit-wide `agents/` policy.
- Artifacts stay outside git by default (`/opt/cursor/artifacts/`).

## Work Completed

- Added `.cursor/rules/80-visual-evidence.mdc` (`alwaysApply: true`)
- Updated `.cursor/README.md` + `docs/dev/CURSOR-OPERATING-GUIDE.md` + CHANGELOG-DEV

## Files or Pieces Changed

- `.cursor/rules/80-visual-evidence.mdc` (new)
- `.cursor/README.md`
- `docs/dev/CURSOR-OPERATING-GUIDE.md`
- `docs/dev/CHANGELOG-DEV.md`
- this handoff

## Verification

- Commands run: path existence for new rule; git status scoped to Cursor/docs only
- Result: rule present; no `agents/` edits
- Limitations: not mirrored into `exports/nortiqa-lab-product-cursor-kit/` (Cursor-only in this org-profile repo per brief)

## Blockers

- None. Optional: Gio may later ask to mirror into product-kit export.

## Risks

- Bajo: agentes pueden sobre-capturar ruido — la regla limita a trabajo visualizable y prohíbe GUI inventada.

## Next Safe Step

- Merge draft PR of the Cursor rule; next visual UI session should attach artifacts under `/opt/cursor/artifacts/`.
