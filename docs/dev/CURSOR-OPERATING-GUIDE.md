# Cursor Operating Guide — Nortiqa Lab

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Audience

Cursor agents operating as **NQ-DEV-IMPLEMENTER** (kit role **`NL-BUILDER`**) inside `nortiqa-lab/.github`, and sibling roles via `agents/`.

## Boot sequence

1. Read root `AGENTS.md`
2. Read `agents/SHARED_RULES.md` + `agents/AUTONOMY.md`
3. Attempt Notion `MEM-NL-ROOT-001`; else `agents/BOOTSTRAP.md` + **draft**
4. Read latest handoff under `docs/shared-ai-memory/handoffs/`
5. `git status --short`
6. Load `.cursor/rules/` (automatic in Cursor)

## Modes

| Mode | Use |
|------|-----|
| `INSPECT` | Read-only diagnosis |
| `PLAN` | Design without file changes |
| `IMPLEMENT` | Controlled file edits |
| `TEST` | Validations |
| `REVIEW` | Audit of code/config |
| `DOCUMENT` | Docs only |
| `RECOVERY` | Controlled failure recovery |

Announce: `MODE` · `SCOPE` · `RISK` at start of substantial work.

## Task loop

```text
Solicitud → diagnóstico → inspección → propuesta → implementación mínima
  → pruebas → revisión → auditoría → ratificación → eventual PROD
```

Details: `docs/dev/DEVELOPMENT-WORKFLOW.md`

## Authority reminder

Cursor implements and documents. It does **not** ratify or promote to PROD. Gio is final authority; Claude/ARCHITECT-001 provides audit gates aligned with `NL-AUDITOR`.

## Where product code lives

Do not invent app commands in this repo. For application work, open `giovanyalbea-dotcom/nortiqa-lab` and discover its real toolchain.

## Session close

Write a handoff from `docs/shared-ai-memory/handoff-template.md` and list one next safe step.
