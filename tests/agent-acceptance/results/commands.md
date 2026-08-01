# Exact commands and results — agent acceptance (DRAFT)

$ pip install -q -r tests/agent-acceptance/requirements.txt
exit 0

$ python3 tests/agent-acceptance/harness/validate_agents.py
[VALIDATE] nl-code-reviewer: APTO PARA RATIFICACIÓN DE STAGING (0 findings)
[VALIDATE] nl-database-migrator: APTO PARA RATIFICACIÓN DE STAGING (0 findings)
[VALIDATE] nl-implementer: APTO PARA RATIFICACIÓN DE STAGING (0 findings)
[VALIDATE] nl-inspector: APTO PARA RATIFICACIÓN DE STAGING (0 findings)
[VALIDATE] nl-security-reviewer: APTO PARA RATIFICACIÓN DE STAGING (0 findings)
[VALIDATE] nl-tester: APTO PARA RATIFICACIÓN DE STAGING (0 findings)
Wrote tests/agent-acceptance/results/validation.json
exit 0

$ python3 tests/agent-acceptance/harness/run_acceptance.py
Tests: 35/35 passed
exit 0

Notes:
- No production calls.
- No memory/L3-state.md writes.
- No institutional approval performed.

# Re-run after status draft→reviewed (technical only)
$ python3 tests/agent-acceptance/harness/validate_agents.py && python3 tests/agent-acceptance/harness/run_acceptance.py
exit 0
