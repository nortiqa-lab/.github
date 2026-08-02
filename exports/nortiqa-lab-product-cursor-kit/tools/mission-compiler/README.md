# Mission compiler (Gen5 dry-run)

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Qué hace

Convierte un pedido en lenguaje natural en un **contrato de misión** (`mission-contract.v0`) y lo valida estructuralmente.

**No ejecuta** cambios, comandos privilegiados ni side effects. Un contrato válido ≠ autorización de ejecución.

## Uso

```bash
# Desde la raíz del repo
python3 tools/mission-compiler/compile.py "Actualizá el README con un puntero a Vanguard"

python3 tools/mission-compiler/compile.py --self-test

python3 tools/mission-compiler/compile.py -f tools/mission-compiler/fixtures/docs-readme.txt -o /tmp/mission.json
```

## Salida

Envelope JSON con:

- `dry_run: true`
- `valid` / `errors`
- `contract` (objeto schema v0)
- `classifier_kind`

## Docs

- Schema: `docs/dev/schemas/mission-contract.v0.json`
- Gen5: `docs/dev/GEN5-MISSION-CONTROL.md`
- Visión: `docs/dev/NORTIQA-VANGUARD.md`
