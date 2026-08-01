# Agent acceptance harness (isolated)

Synthetic validation for `.github/agents/*.agent.md` prior to Gio’s staging ratification.

## Safety

- No real secrets, prod services, or shared databases.
- Does not approve or activate agents.
- Uses fixtures under `fixtures/` and writable `sandbox/` + `results/` only.
- Does not write `memory/L3-state.md` (lock fixture is local).

## Commands

```bash
python3 tests/agent-acceptance/harness/validate_agents.py
python3 tests/agent-acceptance/harness/run_acceptance.py
```

Optional dependency: `PyYAML` (recommended).

```bash
pip install pyyaml
```

## Layout

- `fixtures/` — isolated SUT data
- `sandbox/` — ephemeral writes (gitignored optional; reports may keep evidence)
- `harness/` — validator + runner
- `results/` — exact outputs

## Roles covered

Inspector, Implementer, Tester, Code Reviewer, Security Reviewer, Database Migrator.
