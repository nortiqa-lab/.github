# Agent Factory toolkit (DEV)

Estado: DEV / Borrador — espejo de `SYS-NL-AGENT-FACTORY-001`.

## Qué hay

| Path | Rol |
|------|-----|
| `inventory/seed.json` | Inventario mínimo anti-dupe |
| `policies/anti-dupe.md` | Regla |
| `anti_dupe.py` | Checker CLI |
| `packages/DOC-AGENT-A1/` | Piloto T-005 (A1 documental) |

## Comandos

```bash
python3 tools/agent-factory/anti_dupe.py --self-test
python3 tools/agent-factory/anti_dupe.py "crear un nuevo Agent Tester"
python3 tools/agent-factory/anti_dupe.py "agente documental basico A1" --json
```

## Límites

- No es runtime de agentes en PROD.
- No reemplaza Notion como canon de fichas.
- No crea segundo router: reutiliza piezas existentes.
