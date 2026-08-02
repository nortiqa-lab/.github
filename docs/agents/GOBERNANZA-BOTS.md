# Gobernanza de bots / agentes — referencia de aceptación (DRAFT)

**Estado:** draft (bootstrap).  
**Motivo:** `docs/GOBERNANZA-BOTS.md` y Notion `MEM-NL-ROOT-001` no estaban disponibles en este entorno.  
**No reemplaza canon.** Si aparece el documento oficial, esta copia cede.

## Principios

1. Nortiqa Lab only — sin mezcla con Valent / ERP / Surlancer / clientes.
2. Gio es el único autorizador institucional (staging y producción).
3. Dictamen técnico ≠ aprobación institucional ≠ activación en producción.
4. Staging antes que producción; producción exige PAO/OT + plan de promoción aparte.
5. Sin secretos en manifiestos, logs, fixtures ni handoffs.
6. Alcance declarado; escritura fuera de alcance = rechazo.
7. Locks: no operar si hay lock ajeno activo sobre la misma pieza.

## Roles de aceptación (función)

| Rol | Función | Escritura | Producción |
|-----|---------|-----------|------------|
| Inspector | Solo lectura / mapeo | No | No |
| Implementer | Cambio mínimo en fixture/alcance | Sí, acotada | No |
| Tester | Ejecutar pruebas; no corregir código | No (salvo reportes de test) | No |
| Code Reviewer | Dictamen independiente | No | No |
| Security Reviewer | Detección segura; no reproducir secretos | No | No |
| Database Migrator | migrate/rollback solo en DB temporal/fixture | Sí, solo fixture DB | No |

## Herramientas incompatibles (ejemplos)

| Rol | Incompatible |
|-----|--------------|
| Inspector | write, edit, shell destructivo, deploy |
| Tester | edit de código bajo prueba (fix) |
| Code Reviewer | write del código revisado |
| Security Reviewer | echo/exfiltración de secretos; exploits |
| Database Migrator | DB compartida/prod; drop sin rollback path |
| Cualquiera | auto_approve, production_promote sin Gio |

## Prohibiciones universales

- Datos reales / secretos reales / servicios productivos en pruebas
- Modificar bases compartidas
- Autoaprobación
- Operación Git no autorizada (force-push, delete branch remoto, merge a main sin política)
- Comandos destructivos (`rm -rf /`, disk wipe, drop database prod)
- Activar producción desde el flujo de aceptación staging

## Referencias locales

- `AGENTS.md`
- `agents/SHARED_RULES.md`
- `agents/AUTONOMY.md`
- `docs/agents/STATES.md`
- `docs/agents/ACCEPTANCE-PROTOCOL.md`
