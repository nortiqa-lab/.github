# Estados de agentes NORTIQA (aceptación)

**Draft** — Canon Notion no leído en esta sesión. Fuente operativa: `AGENTS.md` + `agents/BOOTSTRAP.md`.

## Máquina de estados (separados, no intercambiables)

| Estado | Significado | Quién puede asignarlo |
|--------|-------------|------------------------|
| `draft` | Manifiesto propuesto; no operable en staging ni prod | Agente técnico / PR |
| `reviewed` | Pasó validador + pruebas sintéticas; dictamen técnico emitido | Agente técnico (AUDITOR-shaped) |
| `approved-staging` | Ratificación institucional para operar en staging | **Solo Gio** |
| `active-staging` | Habilitado operativamente en staging (servicio/flags) | **Solo Gio** (+ OPS gated) |
| `production-approved` | Autorización institucional para producción | **Solo Gio** + PAO/OT |

## Separación de funciones (obligatoria)

1. **Dictamen técnico** — resultado de validador/pruebas (`APTO…` / `RECHAZADO`). No implica aprobación.
2. **Aprobación institucional** — acto de Gio que mueve a `approved-staging` o `production-approved`.
3. **Activación operativa** — despliegue/flags que mueven a `active-staging` o producción. Requiere estado previo de aprobación.

Un agente **nunca** puede autoasignarse `approved-staging`, `active-staging` ni `production-approved`.

## Transiciones permitidas

```
draft → reviewed                    (técnica)
reviewed → approved-staging         (Gio)
approved-staging → active-staging   (Gio + OPS)
active-staging → production-approved (Gio + PAO/OT; plan separado)
cualquier estado → draft            (regresión / defecto invalidante)
```

Transiciones prohibidas:

- `draft` → `approved-staging` / `active-staging` / `production-approved`
- `reviewed` → `active-staging` / `production-approved` (salta ratificación)
- autoaprobación por el propio agente evaluado o por el evaluador técnico
