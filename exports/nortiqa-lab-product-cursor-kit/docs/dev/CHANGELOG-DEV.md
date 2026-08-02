# Changelog DEV — product repo Cursor mirror package

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## 2026-08-02 — Exports refresh (Vanguard / Gen4 / Gen5)

### Added (mirror from org kit)

- `docs/dev/NORTIQA-VANGUARD.md`, `GEN5-MISSION-CONTROL.md`, `GEN5-MISSION-COMPILER-DRY-RUN.md`, `GEN4-WRAPPER-ROOT-CLOSEOUT.md`
- `docs/dev/schemas/mission-contract.v0.json`
- `tools/mission-compiler/` dry-run CLI
- Related 2026-08-02 handoffs

### Changed

- `apply.sh` / `APPLY.md` copy compiler
- Product `AGENTS.md` documents dry-run commands

### Not changed

- Product `.cursor` identity (still `giovanyalbea-dotcom/nortiqa-lab`)
- Remote product repo (apply still human / write grant)


## 2026-08-01 — Package prepared (not yet applied)

- Prepared under `nortiqa-lab/.github/exports/nortiqa-lab-product-cursor-kit/`
- Blocked: `cursor[bot]` push 403 to `giovanyalbea-dotcom/nortiqa-lab`
- Apply via `APPLY.md` with a writable identity
