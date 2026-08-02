# Nortiqa Lab — Shared AI Context (org profile repo)

## Rule 0 — Canon first, then operate

Before any work:

1. Read this file.
2. Read `agents/SHARED_RULES.md` and `agents/AUTONOMY.md`.
3. Read Notion `MEM-NL-ROOT-001` if a connector is available:  
   https://app.notion.com/p/382e4fe3bfea818aacfad4f9793a697f
4. If Notion is unavailable, use `agents/BOOTSTRAP.md` and mark results as **draft**.

Native AI memory is not a source of truth.

## What this repository is

- GitHub org profile for **nortiqa-lab**.
- Home of the **autonomous agent team kit** under `agents/`.
- Public site profile lives in `profile/README.md`.
- Cursor persistent rules live under `.cursor/rules/` (see `.cursor/README.md`).
- DEV Cursor/workflow docs live under `docs/dev/` (**draft** until audited).

Working product/ops code primarily lives in:
`https://github.com/giovanyalbea-dotcom/nortiqa-lab`

Production services live on VPS SC2027 (`nortiqalab.com`).

## Motto

> Primero funcional. Después excelente. Siempre: lo mejor o nada.

## Context isolation (hard)

Never mix:

- Nortiqa Lab
- Valent Capital Group
- ERP Gio+Edson
- Surlancer or client-specific projects
- Other non-Nortiqa entities (e.g. LLA Santa Cruz, Vialidad Nacional) without explicit Gio authorization and a documented decision

No secret, client data, operational token, or internal decision from one entity may be copied into another.

## Autonomous team

Roster and launch kit: [`agents/README.md`](agents/README.md)

| Code | Role |
|------|------|
| `NL-ORCH` | Orchestrator |
| `NL-AUDITOR` | Governance / gates |
| `NL-BUILDER` | Implementation |
| `NL-OPS` | VPS / staging / prod ops |
| `NL-PRODUCT` | Public product surfaces |
| `NL-MEMORY` | Shared memory / handoffs |

### External label mapping (do not rename the kit)

| External label | Maps to |
|----------------|---------|
| Cursor / NQ-DEV-IMPLEMENTER | `NL-BUILDER` |
| Claude / ARCHITECT-001 | Audit posture aligned with `NL-AUDITOR` |
| ChatGPT / KNOW-001 | Design/docs preparation (not authority) |

Authority final: **Gio**. Agents do not declare work official or promote DEV → PROD.

If Gio gives a goal without naming a role, default to **`NL-ORCH`** and self-dispatch using `agents/DISPATCH.md`.

Solo operation contract: `agents/AUTONOMY.md`.  
Copy-paste launch prompts: `agents/prompts/`.  
Runbooks: `agents/runbooks/`.  
Cursor operating guide: `docs/dev/CURSOR-OPERATING-GUIDE.md`.

## Structure (high level)

```text
AGENTS.md                 # this file
CLAUDE.md                 # Claude-shaped pointer
.cursor/rules/            # Cursor persistent rules
agents/                   # autonomous team kit
docs/shared-ai-memory/    # handoffs
docs/dev/                 # DEV Cursor/dev docs (draft)
profile/README.md         # public org profile
```

## Commands (evidence-only for this repository)

### Installation

```text
PENDIENTE DE VALIDACIÓN
```

No application dependency manifest exists in this repo. For the product repo, discover install commands there before running them.

### Development

```text
# Inspect kit / edit Markdown locally — no app dev server in this repo
git status --short

# Gen5 Mission Control dry-run (no side effects)
python3 tools/mission-compiler/compile.py "Actualizá el README"
python3 tools/mission-compiler/compile.py --self-test
```

Product/runtime development commands: `PENDIENTE DE VALIDACIÓN` in `giovanyalbea-dotcom/nortiqa-lab`.

### Testing / validation (this repo)

```text
# Structure: confirm referenced paths exist
find .cursor agents docs profile tools -type f | sort

# Gen5 compiler fixtures
python3 tools/mission-compiler/compile.py --self-test

# Optional read-only public health (see agents/runbooks/ops-public-health.md)
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://api.nortiqalab.com/health
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://n8n.nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://mcp.nortiqalab.com/
```

Application unit/integration tests: `PENDIENTE DE VALIDACIÓN` (not present here).

### Lint and format

```text
PENDIENTE DE VALIDACIÓN
```

No linter/formatter config is defined in this repository today.

## Security rules (summary)

- Never commit or print secrets; report path + risk only.
- Keep `.env` out of git; `.gitignore` already excludes `.env*` / `.secrets/` / `.drafts/`.
- Do not rotate secrets or change VPS credentials from agent sessions.
- Do not disable auth or expose private services (Ollama/n8n/MCP).
- Full policy: `.cursor/rules/30-security-and-secrets.mdc` + `agents/SHARED_RULES.md`.

## Workflow

```text
Solicitud → diagnóstico → inspección → propuesta → implementación mínima
→ pruebas → revisión → auditoría → ratificación (Gio) → eventual PROD
```

Details: `docs/dev/DEVELOPMENT-WORKFLOW.md`. Autonomy zones: `agents/AUTONOMY.md`.

## Completion criteria

A task is complete only when:

1. Scope matches the brief (no silent prod/entity cross).
2. Validations appropriate to the change were run and recorded.
3. Introduced failures are fixed or explicitly blocking.
4. Docs/handoffs updated when the session is substantial.
5. One next safe step is stated.
6. Nothing is labeled official/PROD without Gio ratification.

## Files requiring caution

| Path / area | Why |
|-------------|-----|
| `AGENTS.md`, `agents/SHARED_RULES.md`, `agents/AUTONOMY.md` | Governance; integrate, do not casually rewrite |
| Notion roots / PAO / OT / dictamens | Protected — Gio + PAO/OT required |
| VPS / `nortiqalab.com` prod surfaces | OPS gates; no drive-by changes |
| `/opt/sc2027/.env` (host, not in git) | Privileged secrets path referenced in bootstrap |
| Historical SC2027 naming | Document discrepancies; do not auto-rename |

## Prohibitions

- Mixing entities or copying secrets/data across contexts
- Declaring changes official / approved / in production
- Destructive infra actions (`docker system prune`, volume wipes, data drops)
- Production promote, DNS, secret rotation without authorization
- Inventing files, services, endpoints, or credentials not evidenced
- Force-push / hard-reset discarding foreign work
- Creating a second memory canon outside Notion + this kit’s handoff path

## Protected pieces

Do not create, edit, replace, or reorganize protected Notion roots, mother documents, dictamens, PAOs, OTs, or official databases unless Gio explicitly authorizes it and the applicable PAO/OT exists.

Allowed without extra authorization:

- Read canon and summarize it.
- Create local drafts in `.drafts/` (gitignored).
- Update versionable files in this repository when requested or when clearly in scope.
- Propose checklists, handoffs, schemas, and implementation plans.
- Open/update PRs for reversible work inside autonomy bounds.

## Session startup checklist

1. Identify role (`NL-*`) or assume `NL-ORCH` (Cursor implementer → `NL-BUILDER`).
2. Read shared rules + autonomy matrix.
3. Read latest handoff under `docs/shared-ai-memory/handoffs/` if present.
4. `git status --short` before editing.
5. Keep unrelated user changes intact.
6. If touching VPS/staging/prod, confirm operational gates in `agents/roles/NL-OPS.md`.

## Session close checklist

Every substantial session MUST leave a handoff using:
`docs/shared-ai-memory/handoff-template.md`

Report:

- What changed
- What was verified
- What could not be verified
- What remains blocked
- Next safe step (one line)

## Final report format (agents)

When finishing substantial work, include:

1. Resultado ejecutivo  
2. Contexto detectado  
3. Archivos creados  
4. Archivos modificados  
5. Validaciones (comandos + resultados)  
6. Riesgos (críticos / altos / medios / bajos)  
7. Elementos no modificados (prod, secretos, servidores, datos)  
8. Próximo paso recomendado (uno)  
9. Estado de gobernanza (`DEV / Borrador` until Gio ratification)
