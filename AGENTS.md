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

If Gio gives a goal without naming a role, default to **`NL-ORCH`** and self-dispatch using `agents/DISPATCH.md`.

Solo operation contract: `agents/AUTONOMY.md`.  
Copy-paste launch prompts: `agents/prompts/`.  
Runbooks: `agents/runbooks/`.

## Protected pieces

Do not create, edit, replace, or reorganize protected Notion roots, mother documents, dictamens, PAOs, OTs, or official databases unless Gio explicitly authorizes it and the applicable PAO/OT exists.

Allowed without extra authorization:

- Read canon and summarize it.
- Create local drafts in `.drafts/` (gitignored).
- Update versionable files in this repository when requested or when clearly in scope.
- Propose checklists, handoffs, schemas, and implementation plans.
- Open/update PRs for reversible work inside autonomy bounds.

## Session startup checklist

1. Identify role (`NL-*`) or assume `NL-ORCH`.
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
