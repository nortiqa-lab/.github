# Development Workflow — Nortiqa Lab (org kit)

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## End-to-end flow

```text
Solicitud
→ diagnóstico
→ inspección
→ propuesta
→ implementación mínima
→ pruebas
→ revisión
→ auditoría
→ ratificación
→ eventual paso a PROD
```

## Step detail

### 1. Solicitud

Capture goal, user, constraints. Default entity: **Nortiqa Lab**. Default role if unnamed: `NL-ORCH`.

### 2. Diagnóstico

Identify: real problem, objective, scope, impact, complexity, risk, components, other-agent dependencies. Classify mode (`INSPECT`…`RECOVERY`) and autonomy zone (green/yellow/red).

### 3. Inspección

Read related files, config, tests (if any), dependencies, docs, latest handoff. **No invent** endpoints, secrets, or infra.

### 4. Propuesta

Define minimal functional solution, files to touch, risks, tests, rollback path. Pause for Gio only on red-zone items.

### 5. Implementación mínima

Small reversible diffs; match existing architecture; security controls; update affected docs.

### 6. Pruebas

Follow `docs/dev/TESTING-CHECKLIST.md` and `.cursor/rules/40-testing-and-validation.mdc`.

### 7. Revisión

Diff review: scope, secrets, entity isolation, contradictions.

### 8. Auditoría

Submit to Claude / ARCHITECT-001 posture (`NL-AUDITOR` gates). Output remains **draft** until ratificación.

### 9. Ratificación

**Gio** only. Agents do not self-declare official/PROD.

### 10. Eventual PROD

`NL-OPS` with gates; never during pure Cursor-config tasks.

## Collaboration with other assistants

| Actor | Lane |
|-------|------|
| ChatGPT / KNOW-001 | Design & draft preparation |
| Claude / ARCHITECT-001 | Architecture audit / gates |
| Cursor / NQ-DEV-IMPLEMENTER | Implement & verify (`NL-BUILDER`) |
| Copilot / others | Assist within same rules; no second canon |

Handoffs: `docs/shared-ai-memory/handoffs/`.

## Visión de plataforma (DEV)

Arquitectura objetivo a largo plazo (no implementación): [`NORTIQA-VANGUARD.md`](./NORTIQA-VANGUARD.md) — contratos de misión, células, simulación, evidencia, Gen5→Gen10.

Gen5 Mission Control (schema + estados + cierre): [`GEN5-MISSION-CONTROL.md`](./GEN5-MISSION-CONTROL.md) · [`schemas/mission-contract.v0.json`](./schemas/mission-contract.v0.json).
