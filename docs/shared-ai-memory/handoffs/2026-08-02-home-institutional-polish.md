# AI Session Handoff - 2026-08-02 - Home institutional polish

## Metadata

- Date: 2026-08-02
- Project: Nortiqa Lab
- AI actor: Cursor / NQ-DEV-IMPLEMENTER → `NL-BUILDER` (+ posture `NL-PRODUCT`)
- Responsible user: Gio
- State: draft / ready for review

## Canon Read

- MEM-NL-ROOT-001: unavailable — Notion MCP `needsAuth`
- Bootstrap used: `agents/BOOTSTRAP.md`

## Assumptions

- Continued the half-finished home pass described by Gio (demo→en preparación, capas pública/interna, NORTIQA firma técnica).
- Source of the prior `index.html` edit was **not** in cloud-agent transcripts nor pushable product/theme repos; used **live** `nortiqalab.com` WP theme as baseline.
- Direction chosen: capa pública **institucional** (not product-catalog shouting).

## Work Completed

1. Captured live home structure + CSS snapshot.
2. Built `exports/nortiqa-home-polish/` with section-by-section hierarchy polish.
3. Softened MVP/PROTOTIPO/demo tone; kept **contenido demostrativo** contract for tests.
4. Documented apply path to WP theme (human/OPS).

## Files or Pieces Changed

- `exports/nortiqa-home-polish/**` (new)
- `exports/README.md`
- `docs/dev/CHANGELOG-DEV.md`
- this handoff

## Verification

- Commands run:
  - `python3 -m unittest discover -s exports/nortiqa-home-polish/tests -p 'test_*.py'` → **9/9 OK**
  - `git diff --check -- exports/nortiqa-home-polish docs` → **OK**
  - `curl` live baseline `https://nortiqalab.com/` → 200 (read-only)
  - Local preview `python3 -m http.server 8765` + computer-use visual QA → hero institucional; strip fuera del 1er viewport; badges PILOTO / EN PREPARACIÓN
- Limitations: cannot deploy to WP/VPS from this identity; product repo push historically 403

## Blockers

- Gio/OPS must port package into `wp-content/themes/nortiqa-lab/` (or grant theme/product write) for the live site to change.
- Optional Gio decision: if public layer should tilt more **producto/operación**, reopen sección 02.

## Risks

- Medium: static package can drift from live theme until applied.
- Low: Google Fonts CDN used in static preview (theme uses self-hosted woff2 in PROD).

## Next Safe Step

- Open `exports/nortiqa-home-polish/` via local static server, approve hierarchy, then apply to WP theme per `APPLY.md`.
