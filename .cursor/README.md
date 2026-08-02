# Cursor configuration — Nortiqa Lab (org profile)

Estado: **DEV / Borrador** — versionable; no es configuración oficial de PROD.

## Purpose

Persistent project rules for Cursor agents working in `nortiqa-lab/.github`.

This repository is the **GitHub org profile** plus the **autonomous agent team kit**. Product/ops application code lives primarily in `giovanyalbea-dotcom/nortiqa-lab`.

## Layout

```text
.cursor/
├── README.md
└── rules/
    ├── 00-nortiqa-governance.mdc
    ├── 10-project-context.mdc
    ├── 20-development-standards.mdc
    ├── 30-security-and-secrets.mdc
    ├── 40-testing-and-validation.mdc
    ├── 50-git-and-version-control.mdc
    ├── 60-documentation-and-traceability.mdc
    ├── 70-infrastructure-safety.mdc
    └── 80-visual-evidence.mdc   # fotos/videos de trabajo visualizable
```

## Precedence (do not invent a second canon)

1. Notion `MEM-NL-ROOT-001` when reachable
2. Root `AGENTS.md` + `agents/SHARED_RULES.md` + `agents/AUTONOMY.md`
3. These `.cursor/rules/*.mdc` files (Cursor-specific persistence)
4. `agents/BOOTSTRAP.md` when Notion is unavailable (**draft** label required)
5. Session handoffs under `docs/shared-ai-memory/handoffs/`

Native model memory is never source of truth.

## Role mapping

| Cursor / external label | Kit role in this repo |
|-------------------------|------------------------|
| NQ-DEV-IMPLEMENTER | `NL-BUILDER` (implementation lane) |
| ARCHITECT-001 / Claude audit | Align with `NL-AUDITOR` gates |
| KNOW-001 / ChatGPT design | Design/docs prep; not authority |
| Default when role unnamed | `NL-ORCH` via `agents/DISPATCH.md` |

Authority final: **Gio**. Cursor does not declare changes official or promote DEV → PROD.

## Visual evidence

Cursor-only rule `80-visual-evidence.mdc`: when work is visible (UI/mock/demo), leave screenshots and short recordings under `/opt/cursor/artifacts/`, surface them in the reply and draft PR. Not a kit-wide `agents/` policy.

## Related docs

- Operating guide: `docs/dev/CURSOR-OPERATING-GUIDE.md`
- Repo audit: `docs/dev/REPOSITORY-AUDIT.md`
- Agent kit: `agents/README.md`
