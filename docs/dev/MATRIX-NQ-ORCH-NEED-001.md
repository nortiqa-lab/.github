# MATRIX-NQ-ORCH-NEED-001 — Necesidad de orquestación por tarea

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

**Fuente:** [`BENCH-NQ-ORCH-001.md`](./BENCH-NQ-ORCH-001.md) §8 (benchmark primero; esta matriz es el extracto operativo).

| Tarea | Primaria | Secundaria | Marketplace Agent Orchestration | Payments plugins |
|-------|----------|------------|----------------------------------|------------------|
| T1 Home polish | Kit / `NL-ORCH`→`NL-BUILDER` | OPS apply | No usar | No usar |
| T2 Aporte LLA | Bloqueado legal | Diseño producto | No usar | No usar |
| T3 Agent Factory | Endurecer Router/Factory DEV | `NL-ORCH` | Observar Arize solo con volumen | No usar |
| T4 Pedido one-line | `NL-ORCH` + kit | Endurecer Gen5 | No usar | No usar |
| T5 Workflows API/jobs | n8n | Humano si riesgo alto | No usar | N/A |
| T6 Misión Gen5 | Gen5 Mission Control | `NL-ORCH` consolida | Observar post-escala | No usar |

**Stack a mantener:** A (kit) + B (n8n).  
**A endurecer:** D (Gen5) + C (Factory DEV).  
**Descartar por ahora:** E (AWS Agents / SageMaker / Arize / Atlan marketplace).

Criterios de trabajo del agente: [`BENCH-NQ-ORCH-001.md`](./BENCH-NQ-ORCH-001.md) §9.
