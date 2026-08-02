# Nortiqa Lab - Shared AI Context

## Rule 0 - Canonical Memory First

Before doing any work in this repository, read the canonical Notion root:

**MEM-NL-ROOT-001 - Raiz de Memoria Canonica**  
https://app.notion.com/p/382e4fe3bfea818aacfad4f9793a697f

Also read `agents/SHARED_RULES.md` and `agents/AUTONOMY.md` when present.

The canonical source of truth is Notion. Local files, chat history, IDE state,
and native AI memory are helpers only.

If Notion is unavailable, continue only with local, reversible work using
`docs/shared-ai-memory/bootstrap-packet.md` or `agents/BOOTSTRAP.md`, and clearly
mark the result as a **draft**.

## Project Context

- Nortiqa Lab is an AI agent factory based in Rio Gallegos, Patagonia.
- This repository contains public/site assets (`site/`), brand assets, support
  scripts (`scripts/`, `server-ops/sc2027/`), and versionable drafts.
- Production apps and staging services live on the VPS (host label SC2027).
- Motto: "Primero funcional. Despues excelente. Siempre: lo mejor o nada."
- Cursor rules: `.cursor/rules/` · DEV docs: `docs/dev/` (draft until audited)
- Org kit home: `https://github.com/nortiqa-lab/.github`

## Context Isolation

Never mix contexts between:

- Nortiqa Lab
- Valent Capital Group
- ERP Gio+Edson
- Surlancer or client-specific projects

No secret, client data, operational token, or internal decision from one entity
may be copied into another entity context.

## Autonomous team (`NL-*`)

| Code | Role |
|------|------|
| `NL-ORCH` | Orchestrator (default if role unnamed) |
| `NL-AUDITOR` | Governance / gates |
| `NL-BUILDER` | Implementation (Cursor / NQ-DEV-IMPLEMENTER maps here) |
| `NL-OPS` | VPS / staging / prod ops |
| `NL-PRODUCT` | Public product surfaces |
| `NL-MEMORY` | Shared memory / handoffs |

Solo contract: `agents/AUTONOMY.md`. Prompts: `agents/prompts/`.

## Commands (evidence-only)

### Installation

```text
PENDIENTE DE VALIDACIÓN
```

No root application dependency manifest found.

### Development

```bash
python3 scripts/generate_hero.py
# Edit site/site/index.html for landing changes

# Gen5 Mission Control dry-run (no side effects; after kit apply)
python3 tools/mission-compiler/compile.py --self-test
```

### Testing / validation

```bash
bash server-ops/sc2027/healthcheck-prod.sh    # intended on VPS
bash server-ops/sc2027/healthcheck-staging.sh # intended on VPS
# Off-host safe subset:
curl -sS -o /dev/null -w "%{http_code}\n" https://nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code}\n" https://api.nortiqalab.com/health
# Gen5 dry-run fixtures (if tools/mission-compiler present)
python3 tools/mission-compiler/compile.py --self-test
```

### Lint and format

```text
PENDIENTE DE VALIDACIÓN
```

## Security rules (summary)

- Never commit or print secrets; `.env*` is gitignored.
- Do not rotate host secrets or expose Ollama/n8n/MCP.
- Full policy: `.cursor/rules/30-security-and-secrets.mdc`.

## Workflow

```text
Solicitud → diagnóstico → inspección → propuesta → implementación mínima
→ pruebas → revisión → auditoría → ratificación (Gio) → eventual PROD
```

## Protected Pieces

Do not create, edit, replace, or reorganize protected Notion roots, mother
documents, dictamens, PAOs, OTs, or official databases unless Gio explicitly
authorizes it and the applicable PAO/OT exists.

Allowed without extra authorization:

- Read canon and summarize it.
- Create local drafts in `.drafts/`.
- Update versionable technical files in this repository when requested.
- Propose checklists, handoffs, schemas, and implementation plans.
- Open/update draft PRs inside autonomy bounds.

## Files requiring caution

| Area | Why |
|------|-----|
| `server-ops/sc2027/*` | Prod/staging ops; gates required |
| Notion roots / PAO / OT | Protected |
| Historical SC2027 naming | Document; do not auto-rename |

## Prohibitions

- Mixing entities; declaring work official/PROD without Gio
- Destructive docker/data ops; force-push discarding foreign work
- Inventing secrets, endpoints, or infra not evidenced

## Session Startup Checklist

1. Read `AGENTS.md` and `CLAUDE.md`.
2. Read MEM-NL-ROOT-001 in Notion when the connector is available.
3. Identify role (`NL-*`) or assume `NL-ORCH`.
4. Check `git status --short` before editing.
5. Keep unrelated user changes intact.
6. If touching VPS/staging, confirm the current operational gate first (`agents/roles/NL-OPS.md`).

## Handoff Rule

Any substantial AI session should leave a short handoff containing:

- Date and actor.
- Canon sources read.
- What changed.
- What was verified.
- What remains blocked.
- Next safest step.

Prefer `docs/shared-ai-memory/handoff-template.md` (also mirrored under the NL kit).
