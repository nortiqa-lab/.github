# Changelog DEV — Cursor configuration execution

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## 2026-08-02 — Ratificación Gio + Factory T-005 + ARCH pagos LLA SC

### Ratificación operativa (Gio)

- `BENCH-NQ-ORCH-001` / `MATRIX-NQ-ORCH-NEED-001`: Adoptar A+B; endurecer D+C; descartar marketplace E — criterio de trabajo kit (≠ PROD Madre)
- Notion bench actualizado

### Added

- `tools/agent-factory/` — inventario, `anti_dupe.py`, paquete T-005 `DOC-AGENT-A1`
- `docs/dev/SYS-NL-AGENT-FACTORY-001.md`
- `agents/factory/README.md`
- `docs/dev/lla-sc/ARCH-LLA-SC-PAYMENTS-001.md` — aportes, recurrentes, CampaignRules (descuentos periódicos), gates legales
- Notion: Factory endurecido; ARCH-LLA-SC-PAYMENTS-001
- Handoff `docs/shared-ai-memory/handoffs/2026-08-02-ratify-factory-lla-payments.md`

### Authorized entity cross

- Gio autorizó diseño de arquitectura de pagos para web LLA Santa Cruz (documentado; sin cobros reales)

### Not changed

- Cobros reales / PSP prod / DNS LLA / secretos
- Instalación marketplace Payments u Agent Orchestration

## 2026-08-02 — Benchmark orquestación + matriz de necesidad

### Added

- `docs/dev/BENCH-NQ-ORCH-001.md` — benchmark ponderado A–E (kit, n8n, Router/Factory, Gen5, marketplace) vs tareas T1–T6
- `docs/dev/MATRIX-NQ-ORCH-NEED-001.md` — extracto operativo Usar / Endurecer / No usar
- Handoff `docs/shared-ai-memory/handoffs/2026-08-02-orch-benchmark-matrix.md`
- Notion DEV: [BENCH-NQ-ORCH-001](https://app.notion.com/p/3b0e4fe3bfea81b2898be9f367398c54)

### Dictamen DEV (no oficial)

- Adoptar/mantener: `NL-ORCH` + kit + n8n
- Endurecer: Gen5 + Agent Factory DEV
- Descartar por ahora: Cursor marketplace Agent Orchestration
- Payments plugins: no usar hasta dictamen legal LLA

### Not changed

- Producción / VPS / n8n workflows activos
- Instalación de plugins marketplace
- Canon PROD Notion

## 2026-08-02 — Merge stack + exports refresh

### Merged to main

- PR #7 Vanguard vision
- PR #10 Gen5 Mission Control schema
- PR #12 Gen5 mission compiler dry-run
- PR #6 Gen4 wrapper root closeout checklist

### Changed

- `exports/nortiqa-lab-product-cursor-kit/` — refresh agents/docs + embed `tools/mission-compiler`; `apply.sh` copies compiler

### Not changed

- Product repo remote (still no bot push) — Gio runs `APPLY.md` / `apply.sh`
- Host/prod (Gen4 wrapper already closed per #6 evidence)

## 2026-08-02 — Gen5 mission compiler dry-run

### Added

- `tools/mission-compiler/` — CLI Python stdlib: pedido → envelope JSON + validación estructural v0 (`--self-test` 5/5)
- `docs/dev/GEN5-MISSION-COMPILER-DRY-RUN.md`
- Fixtures bajo `tools/mission-compiler/fixtures/`
- Handoff `docs/shared-ai-memory/handoffs/2026-08-02-gen5-mission-compiler-dry-run.md`

### Changed

- `docs/dev/GEN5-MISSION-CONTROL.md` — próximo paso apunta al compiler
- Punteros en `agents/README.md`, `DEVELOPMENT-WORKFLOW.md`, `AGENTS.md` (comando evidencia)

### Not changed

- Product repo (sin push 403) — mirror pendiente vía exports / write grant
- Ejecución privilegiada / Telegram wiring runtime

### Governance

- **DEV / Borrador** — dry-run ≠ autorización

## 2026-08-02 — Gen5 Mission Control (schema DEV)

### Added

- `docs/dev/GEN5-MISSION-CONTROL.md` — estados, cierre verificable, compilador NL→contrato, mapa AUTONOMY/DISPATCH
- `docs/dev/schemas/mission-contract.v0.json` — JSON Schema v0 del contrato de misión
- Handoff `docs/shared-ai-memory/handoffs/2026-08-02-gen5-mission-control-schema.md`

### Changed

- `docs/dev/NORTIQA-VANGUARD.md` — próximo paso apunta al schema Gen5
- `docs/dev/DEVELOPMENT-WORKFLOW.md`, `agents/README.md` — punteros Gen5

### Not changed

- Runtime/parser en product repo, VPS/prod, Notion canon, Gen6+ cells

### Governance

- Estado: **DEV / Borrador** — auditoría + ratificación Gio pendientes

## 2026-08-02 — NORTIQA Vanguard (visión DEV)

### Added

- `docs/dev/NORTIQA-VANGUARD.md` — captura versionable de la visión Gio: plataforma operativa (no multi-modelo chat), arquitectura objetivo, niveles 0–5, células, digital twin, memorias, caja negra, evals, soberanía, roadmap Gen4→Gen10
- Handoff `docs/shared-ai-memory/handoffs/2026-08-02-nortiqa-vanguard-vision.md`

### Changed

- `docs/dev/DEVELOPMENT-WORKFLOW.md` — enlace a visión Vanguard
- `agents/README.md` — puntero DEV a Vanguard (sin renombrar roster)

### Not changed

- Notion canon, VPS/prod, secretos, implementación Gen4+/runtime
- Roles `NL-*` (solo mapeo conceptual en el doc)

### Governance

- Estado: **DEV / Borrador** — requiere auditoría ARCHITECT-001 / `NL-AUDITOR` y ratificación Gio

## 2026-08-01 — Cursor local kit + docs/dev

### Added

- `.cursor/README.md`
- `.cursor/rules/00-nortiqa-governance.mdc`
- `.cursor/rules/10-project-context.mdc`
- `.cursor/rules/20-development-standards.mdc`
- `.cursor/rules/30-security-and-secrets.mdc`
- `.cursor/rules/40-testing-and-validation.mdc`
- `.cursor/rules/50-git-and-version-control.mdc`
- `.cursor/rules/60-documentation-and-traceability.mdc`
- `.cursor/rules/70-infrastructure-safety.mdc`
- `docs/dev/CURSOR-OPERATING-GUIDE.md`
- `docs/dev/REPOSITORY-AUDIT.md`
- `docs/dev/DEVELOPMENT-WORKFLOW.md`
- `docs/dev/TESTING-CHECKLIST.md`
- `docs/dev/CHANGELOG-DEV.md` (this file)
- Session handoff under `docs/shared-ai-memory/handoffs/`

### Changed

- `AGENTS.md` — integrated Cursor rules pointers, command inventory (evidence-only), NQ-DEV-IMPLEMENTER mapping, completion/report format; preserved Rule 0 and `NL-*` roster

### Not changed

- Production systems, secrets, VPS, DNS, Docker (none present), product application code
- Notion canon (unavailable / not written)
- Role kit filenames under `agents/` (mapped, not renamed)

### Session close

- 2026-08-01: Gio ordered session closeout (`cerra todo`). Handoff marked **closed**. PR #3 left open as draft for human merge.

### Follow-up — “hace todo” (same day)

- Merged PR #3 into `main` (`eabc344`)
- Notion MCP still unauthenticated in agent environment (human action)
- Product-repo push blocked (403); added `exports/nortiqa-lab-product-cursor-kit/` apply package

## 2026-08-02 — Generación 4 wrapper root closeout (draft continuity)

### Added

- `docs/dev/GEN4-WRAPPER-ROOT-CLOSEOUT.md` — privileged install command, post-install healthcheck, restore-point gate, loopback preview policy
- `docs/shared-ai-memory/handoffs/2026-08-02-gen4-wrapper-root-closeout.md`

### Changed

- `agents/BOOTSTRAP.md` — open OPS blocker for Gen 4 root wrapper install

### Not changed

- VPS files / systemd / `/usr/local/sbin/sc2027-botctl` (no SSH in this cloud agent)
- Product repo Gen 4 artifacts (not present on GitHub; live on staging host per Codex)
- Notion canon, secrets, DNS, ports (previews remain loopback by design)

### Session state

- **Ready for review (DEV):** Gio installed wrapper (`root:root` 755, sha256 match); restore point `backups/gen4-closeout-20260802T001611Z`; pilot/oauth active `NRestarts=0`. Residual opcional: restart pilot for latest `intent_router.py`.
