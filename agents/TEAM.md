# Roster v1 — listo para operar solo

```
                    Gio (red-zone authorizer)
                              |
                         NL-ORCH
                    ______/ | \______
                   /        |        \
            NL-AUDITOR  NL-BUILDER  NL-OPS
                   \        |        /
                    \   NL-PRODUCT  /
                     \      |      /
                       NL-MEMORY
```

Cada nodo tiene prompt autocontenido en `prompts/` + ficha en `roles/` + contrato en `AUTONOMY.md`.

## Matriz rápida

| Situación | Primario |
|-----------|----------|
| Objetivo genérico / “hacelo” | ORCH |
| Landing/copy/brand | PRODUCT |
| Código/docs/PR | BUILDER |
| Health/login/promote | OPS |
| ¿Se puede? / Notion / riesgo | AUDITOR |
| Cerrar/continuar sesión | MEMORY |

RACI extendido (roles + modelos/motores + browser): [`docs/dev/RACI-MODELS-AND-ROLES.md`](../docs/dev/RACI-MODELS-AND-ROLES.md) (**DEV / Borrador**).

## Solo-ready checklist (kit)

- [x] `AGENTS.md` en root
- [x] Shared rules + autonomy + bootstrap
- [x] Prompts con boot + loop + output contract
- [x] Runbooks cold-start / health / public surface
- [x] Handoff template versionable
- [x] Launch guide
- [x] Cursor `.cursor/rules/` + `docs/dev/` (DEV/borrador; pendiente auditoría)

## Escalamiento a Gio

Solo zona roja: privilegios host, snapshots, rotación de tokens, PAO/OT, cruce de entidades, merge policy si aplica.
