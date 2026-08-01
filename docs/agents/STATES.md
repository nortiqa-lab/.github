# Estados de agentes NORTIQA (aceptación)

**Draft** — Canon Notion no leído en esta sesión. Fuente operativa: `AGENTS.md` + `agents/BOOTSTRAP.md`.

## Máquina de estados (separados, no intercambiables)

| Estado | Significado | Quién puede asignarlo |
|--------|-------------|------------------------|
| `draft` | Manifiesto propuesto; no operable en staging ni prod | Agente técnico / PR |
| `reviewed` | Pasó validador + pruebas sintéticas; dictamen técnico emitido | Agente técnico (AUDITOR-shaped) |
| `approved-staging` | Ratificación institucional para operar en staging/lab | **Solo Gio** (texto explícito) |
| `active-staging` | Habilitado operativamente en staging VPS | **Solo Gio** (+ OPS gated) |
| `production-approved` | Autorización institucional para producción | **Solo Gio** + PAO/OT |

## Laboratorio vs staging VPS

- **Lab runtime** (`tests/agent-acceptance/lab/ACTIVE`): sandbox local autorizado por `LAB-AUTHORIZATION.md`. No implica VPS.
- **`active-staging`**: activación en infraestructura staging real. Sigue requiriendo Gio + OPS; el lab **no** la setea.

## Separación de funciones (obligatoria)

1. **Dictamen técnico** — resultado de validador/pruebas (`APTO…` / `RECHAZADO`). No implica aprobación.
2. **Aprobación institucional** — acto de Gio que mueve a `approved-staging` o `production-approved`.
3. **Activación operativa** — despliegue/flags que mueven a `active-staging` o producción. Requiere estado previo de aprobación.
4. **Lab exercise** — ejecución intensiva en sandbox tras autorización de laboratorio (puede coexistir con `approved-staging` sin VPS).

Un agente **nunca** puede autoasignarse `production-approved`.  
`approved-staging` solo con texto explícito de Gio (p. ej. `LAB-AUTHORIZATION.md` o ratificación formal).

## Transiciones permitidas

```
draft → reviewed                    (técnica)
reviewed → approved-staging         (Gio — incluye auth de lab)
approved-staging → active-staging   (Gio + OPS — VPS only)
approved-staging → lab ACTIVE       (Gio lab auth — sandbox)
active-staging → production-approved (Gio + PAO/OT; plan separado)
cualquier estado → draft            (regresión / defecto invalidante)
```

Transiciones prohibidas:

- `draft` → `approved-staging` / `active-staging` / `production-approved`
- `reviewed` → `active-staging` / `production-approved` (salta ratificación)
- lab ACTIVE → `production-approved`
- autoaprobación de producción por el agente evaluado o el evaluador técnico
