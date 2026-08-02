# Autonomy contract — operate without waiting

Goal: agents should finish the job inside their lane, escalate only on hard gates.

## Green zone — do alone (no ask)

All roles may:

- Read this repo, public Nortiqa repos, public URLs.
- Read Notion canon when connector exists.
- Write versionable drafts/docs/code in-scope on a feature branch.
- Commit, push, open/update draft PRs for Nortiqa work in this repo.
- Run read-only checks (`git status`, `curl` health GETs, `gh` read).
- Create/update handoffs under `docs/shared-ai-memory/handoffs/`.
- Self-correct failed checks and retry within scope.

Role-specific green:

| Role | Extra green zone |
|------|------------------|
| `NL-ORCH` | Classify work, write briefs, consolidate, spawn/recommend sibling roles |
| `NL-AUDITOR` | Issue draft gates APPROVE / CONDITIONAL / BLOCK; write draft dictamen notes locally |
| `NL-BUILDER` | Implement reversible code/docs/scripts; fix CI/lint if present |
| `NL-OPS` | Prepare OPS scripts/docs; run non-destructive public health GETs; document exact privileged commands |
| `NL-PRODUCT` | Edit public HTML/copy/brand assets in-repo; mobile/desktop pass notes |
| `NL-MEMORY` | Maintain bootstrap/handoff templates; dedupe memory docs |

## Yellow zone — do, then notify in handoff

- Touching files outside the brief but required to finish (mention why).
- Broad refactors adjacent to the change (keep minimal).
- Updating the agent kit itself while doing another task, if needed for autonomy.

## Red zone — STOP and escalate to Gio

- Any Valent / **ERP Gio+Edson** / client context (Nortiqa-owned `ERP-Nortiqa-Lab` / `erp.nortiqalab.com` is Nortiqa infra — still no client data cross).
- Notion protected writes without explicit authorization text from Gio.
- Production promote / Nginx reload / secret chmod when lacking privileged access.
- Destructive data ops, DB drops, mass user changes.
- Exposing Ollama/n8n/MCP publicly or disabling auth.
- Spending money / buying infra / changing DNS registrars.
- Merging to `main` if Gio policy requires human merge (default: leave PR ready; merge only if Gio already said “merge it” or repo allows bot merge and checks are green).

## Ambiguity policy

If the request is underspecified:

1. Choose the **smallest reversible** interpretation that advances Nortiqa.
2. State the assumption in one line.
3. Execute.
4. Do **not** stall waiting for perfect clarity unless you would enter a red zone.

## Solo loop (every agent)

```
START
  read AGENTS.md + SHARED_RULES + AUTONOMY + role sheet
  read latest relevant handoff
  classify task + confirm green/yellow/red
  if red -> escalate with exact ask
  else execute end-to-end
  verify
  write handoff
  report: done / blocked + next safe step
END
```

## Definition of “listo para operar solo”

An agent is solo-ready when, given only a one-line goal from Gio, it can:

1. Bootstrap without Notion.
2. Stay in Nortiqa context.
3. Finish or hard-stop with a precise human action.
4. Leave a handoff another agent can continue from cold.
