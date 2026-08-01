# Exact commands and results — agent lab campaign (DRAFT)

## Lab authorization
Gio: "Te doy permiso para que los pruebes en el laboratorio..." → `docs/agents/LAB-AUTHORIZATION.md`

## Commands

```bash
pip install -q -r tests/agent-acceptance/requirements.txt
python3 tests/agent-acceptance/harness/validate_agents.py
python3 tests/agent-acceptance/harness/run_acceptance.py
python3 tests/agent-acceptance/harness/run_lab.py
```

## Results (post v1.1.0 manifests)

- validate_agents.py → exit 0 (approved-staging under lab auth)
- run_acceptance.py → exit 0 (35/35 after inspector sink fix)
- run_lab.py → exit 0; prompt_quality 10/10; scores 39–40/40
- VPS active-staging: NOT_PERFORMED
- production: FORBIDDEN
