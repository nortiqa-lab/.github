# Repository Audit — nortiqa-lab/.github

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Metadata

| Field | Value |
|-------|--------|
| Fecha | 2026-08-01 |
| Rama inspeccionada (base) | `main` |
| Commit inspeccionado | `967ae5ce658747e1f53bf49d8e2e2b34b0b6dca5` |
| Rama de trabajo (config) | `cursor/cursor-nortiqa-config-3d56` |
| Auditor agente | NQ-DEV-IMPLEMENTER / NL-BUILDER (Cursor Cloud) |
| Canon Notion | **Unavailable** (MCP `needsAuth`) → bootstrap used; results **draft** |

## Project determination (evidence)

- **Entidad propietaria:** Nortiqa Lab
- **Propósito:** GitHub org profile + autonomous agent team kit
- **Madurez:** Kit v1 operational (versionable); not a runtime application
- **Riesgo del repo:** Bajo–medio (público por diseño; sin secretos en árbol)

## Structure (pre-config)

```text
AGENTS.md
CLAUDE.md
agents/          # kit: rules, autonomy, roles, prompts, runbooks
docs/shared-ai-memory/
profile/README.md
.gitignore
```

No `.cursor/`, no `.github/workflows/`, no Docker, no package manifests.

## Technologies

- Markdown documentation / agent prompts only
- Git + GitHub (remote `nortiqa-lab/.github`)

## Services referenced (documentation map only)

From `agents/BOOTSTRAP.md` / runbooks (not defined as code in this repo):

- `nortiqalab.com`, `api.nortiqalab.com`, `n8n.nortiqalab.com`, `mcp.nortiqalab.com`
- VPS label **SC2027**; paths such as `/opt/sc2027/.env` mentioned as privileged OPS blockers

## Existing configuration

| Piece | Status |
|-------|--------|
| `AGENTS.md` | Present — root AI context |
| `CLAUDE.md` | Present — Claude pointer |
| `agents/*` | Present — autonomous kit v1 |
| Handoffs | Present — 2026-08-01 entries |
| `.cursor/` | Absent before this execution |
| CI/CD | Absent |
| `.env` / secrets in tree | None found |
| `.gitignore` | Excludes `.drafts/`, `.secrets/`, `.env*` |

## Findings

### Facts

1. This is an **org-profile / agent-kit** repository, not the product monorepo.
2. Role system is **`NL-*`** with autonomy green/yellow/red zones.
3. Notion is declared canon; local bootstrap is fallback.
4. Public health checks are documented as curl GETs.

### Inferences

1. Product coding agents in `giovanyalbea-dotcom/nortiqa-lab` may still need this kit linked or mirrored.
2. Host path naming `sc2027` is historical/infra label coexisting with Nortiqa brand.

### Recommendations (priority)

| Priority | Recommendation |
|----------|----------------|
| P0 | Keep Cursor rules integrated with `NL-*` (done in this PR as draft) |
| P1 | Authenticate Notion MCP in agent environments so canon can be live-read |
| P1 | Mirror or submodule/link kit into working product repo when agents code there |
| P2 | Optional: add a minimal markdown link-check script later (not inventing CI now) |
| P2 | Separate normalization plan for SC2027 path naming — do **not** rename blindly |

## Risks

See executive risk list in the session report / `CHANGELOG-DEV.md` companion notes.

### Potential secrets

- **None versioned in tree** at audit time
- Risk: future commits of `.env` — mitigated by `.gitignore`
- Risk: privileged path `/opt/sc2027/.env` on VPS (outside this repo)

## Contradictions / duplications

| Topic | Notes |
|-------|--------|
| Role names | External prompt uses NQ-DEV-IMPLEMENTER / ARCHITECT-001 / KNOW-001; repo uses `NL-*`. **Resolution:** map, do not rename kit. |
| Push policy | Some task templates forbid push; `agents/AUTONOMY.md` allows draft PR push. **Resolution:** follow AUTONOMY unless Gio overrides. |
| SC2027 vs Nortiqa | Infra paths use SC2027; brand is Nortiqa Lab. Document only; no automatic rename. |
| Entity list | Task mentions LLA Santa Cruz / Vialidad Nacional; kit docs emphasize Valent/ERP/Surlancer. Treat all non-Nortiqa as isolated. |

## Technical debt

- No automated validation for broken relative links
- Kit not automatically present in product repo
- OPS blockers remain human/privileged (login portal, env chmod, nginx, snapshots)

## Stack / commands summary

| Category | In this repo |
|----------|----------------|
| Install | N/A (no app deps) — `PENDIENTE DE VALIDACIÓN` for product repo |
| Dev server | N/A |
| Tests | Structure/docs review + optional public health curls |
| Lint/format | None configured |
