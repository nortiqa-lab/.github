# Instrucciones para que Gio ratifique staging

**Draft** — evaluación técnica lista; aprobación institucional pendiente.

## Qué se pide ratificar

Los agentes en `.github/agents/*.agent.md` cuyo dictamen técnico sea:

- `APTO PARA RATIFICACIÓN DE STAGING`, o
- `APTO CON OBSERVACIONES` (aceptando las observaciones)

Ver matriz: `docs/agents/RESULTS-MATRIX.md`.

## Qué **no** está hecho

- No hay `approved-staging` ni `active-staging` en manifiestos.
- No se activaron servicios ni se desplegó nada.
- No se tocó producción.
- No se escribió `memory/L3-state.md` (ausente; locks solo en fixture).

## Pasos de ratificación (humano)

1. Revisar `docs/agents/RESULTS-MATRIX.md` y `tests/agent-acceptance/results/acceptance-report.md`.
2. Revisar cada `.github/agents/*.agent.md` (owner, scope, tools, prohibitions).
3. Confirmar que Notion / gobernanza canónica no contradice este draft (cuando el conector esté disponible).
4. Para cada agente aceptado, **Gio** cambia `status:` a `approved-staging` (commit humano o instrucción explícita).
5. Solo después, OPS puede preparar `active-staging` (flags/servicios) con autorización explícita.

## Comando de re-validación post-edición

```bash
python3 tests/agent-acceptance/harness/validate_agents.py
python3 tests/agent-acceptance/harness/run_acceptance.py
```

Si el validador ve `approved-staging` sin contexto humano, fallará a propósito (`status_premature`) en corridas de aceptación automatizadas. Tras ratificar, la aceptación continua debe usar un modo “post-ratification” o excluir ese check — **no implementado aquí a propósito** para evitar autoaprobación.

## Frase sugerida de autorización

> Ratifico staging para: `<lista de agentes>`. Pueden pasar a `approved-staging`. Activación `active-staging` queda para OPS con mi OK aparte.
