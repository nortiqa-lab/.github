# Gen5 — Mission compiler dry-run

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

| Campo | Valor |
|-------|--------|
| Fecha | 2026-08-02 |
| Tool | [`tools/mission-compiler/`](../../tools/mission-compiler/) |
| Schema | [`schemas/mission-contract.v0.json`](./schemas/mission-contract.v0.json) |
| Padre | [`GEN5-MISSION-CONTROL.md`](./GEN5-MISSION-CONTROL.md) |

## Hechos

- Product repo `giovanyalbea-dotcom/nortiqa-lab`: **sin push** para este agente → el dry-run vive en el org kit.
- Implementación: Python 3 stdlib (sin `jsonschema` pip).
- Side effects: **ninguno**.

## Comandos

```bash
python3 tools/mission-compiler/compile.py --self-test
python3 tools/mission-compiler/compile.py "Diagnosticá el health de api.nortiqalab.com"
```

## Clasificador v0 (heurístico)

| Señal | Resultado típico |
|-------|------------------|
| Entidad ajena (Valent/ERP/…) | `blocked`, level 0 |
| Prod-like (nginx/DNS/secrets/…) | `awaiting_human`, level 5 + gate |
| Docs/README/mejorá… | `planned`, level 2, write |
| Diagnóstico/health | `planned`, level 1, read + public_readonly |
| Explica/analiza | `planned`, level 0 |
| Ambiguo | `draft`, level ≤ 1 |

## Límites

- No es LLM compiler; es heurística determinística v0.
- No enforcea ejecución.
- Validación estructural v0 (required + enums clave), no draft/2020-12 completo.
- Mirror a product: Gio aplica vía `exports/` o otorga write al bot.

## Próximo paso

Cerrar Gen4 acceptance en product; opcionalmente copiar `tools/mission-compiler` allí y enganchar Telegram/Cursor como `source.channel` solo en dry-run.
