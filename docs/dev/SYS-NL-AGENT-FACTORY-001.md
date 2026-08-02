# SYS-NL-AGENT-FACTORY-001 — Fábrica de agentes (endurecimiento DEV)

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

| Campo | Valor |
|-------|--------|
| Fecha | 2026-08-02 |
| Actor | Cursor / `NL-BUILDER` |
| Espejo Notion | Sección Factory en 🟡 DEV — Propuestas y Borradores |
| Toolkit | [`tools/agent-factory/`](../../tools/agent-factory/) |
| Relación | Bench orquestación ratificado: endurecer C (Factory) |

## 1. Decisión arquitectónica (sin cambio)

No crear segundo router, tester ni ejecutor. El Factory **coordina** piezas existentes (`NL-ORCH`, Arquitecto, Simulador/Tester, Auditor, Agent Router, Desktop Operator).

## 2. Lógica anti-duplicación (nueva, ejecutable)

```text
pedido → normalize → match inventory →
  BLOCKED_DUPLICATE | ALLOW_PILOT | ALLOW_NEW
```

Implementación: `python3 tools/agent-factory/anti_dupe.py`.

Semillas: Tester, Desktop Operator, Router, DOC-AGENT-A1 piloto.

## 3. T-005 ejecutado en este repo

Bloqueo previo (“cero repos accesibles” vía conector Notion) se **mitiga** usando este org-profile repo como sandbox Factory (solo docs/tools DEV).

| Entregable | Path |
|------------|------|
| Paquete | `tools/agent-factory/packages/DOC-AGENT-A1/` |
| Ficha / prompt / controles / 10 tests / inventory entry | incluidos |
| Self-test anti-dupe | `anti_dupe.py --self-test` |

**Estado T-005:** cerrado a nivel documental+tool en este repo (A1). No implica agente “oficial”.

## 4. T-006

Sigue **bloqueado** (datos sintéticos / entorno A2 no autorizados).

## 5. Flujo operativo endurecido

1. `anti_dupe.py "<pedido>"`
2. Si BLOCKED → reutilizar / consolidar; no crear.
3. Si ALLOW_PILOT / ALLOW_NEW → ensamblar paquete bajo `packages/`.
4. Validar con tests del paquete + Gen5 si hay side effects.
5. Handoff + auditoría Claude antes de cualquier PROD.

## 6. Próximo paso Factory

Registrar resultados T-001/T-005 en Notion Factory y pedir dictamen Claude del toolkit.
