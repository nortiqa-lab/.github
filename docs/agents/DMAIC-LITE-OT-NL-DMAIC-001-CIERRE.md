# Cierre piloto — OT-NL-DMAIC-001 (DMAIC-Lite)

**Estado:** CIERRE PROPUESTO (versión local)  
**Fecha:** 2026-08-02  
**OT:** [OT-NL-DMAIC-001](https://app.notion.com/p/352e4fe3bfea8175b08af2fc075742ad)  
**Metodología:** Six Sigma / DMAIC-Lite (Nortiqa) — [canon](https://app.notion.com/p/356e4fe3bfea815aba0ace55954b7204)  
**Actor:** NL-AUDITOR / Cursor Cloud (subrol calidad temporal)  
**Autorización de lab:** Gio — `docs/agents/LAB-AUTHORIZATION.md`  
**Alcance entidades:** Nortiqa Lab only  
**PROD / VPS active-staging:** no tocados  

---

## D — Define

| Ítem | Contenido |
|------|-----------|
| Problema | Altas operativas de agentes sin checklist mínimo medible → riesgo de promover prompts débiles. |
| Proceso | Alta operativa de agentes (manifiesto `.agent.md` + prueba + madurez + inventario). |
| CTQ (críticos para calidad) | (1) ficha técnica (2) prompt base (3) prueba mínima (4) versión (5) estado de madurez (6) inventario/rol |
| Alcance piloto | 6 agentes de aceptación lab (supera el mínimo de 5 altas del OT) |
| No-alcance | SIX-OS-001, SIX-AG-001, PROD, VPS `active-staging`, otras entidades |

---

## M — Measure

### Baseline (v1.0.0, pre-lab intensivo)

| Métrica | Valor |
|---------|-------|
| Prompt quality (`run_lab` body_quality) | 2/10 |
| Lab score | ~32/40 |
| Dictamen lab | APTO CON OBSERVACIONES |
| Secciones obligatorias prompt | faltaban output_contract, refusal_scripts, escalation, lab_posture, examples, non_goals |

### Post-Improve (v1.1.0)

| Métrica | Valor |
|---------|-------|
| Prompt quality | 10/10 (6/6) |
| Lab score | 39–40/40 |
| Acceptance suite | 35/35 PASS |
| Dictamen lab | APTO PARA RATIFICACIÓN DE STAGING (6/6) |

### Checklist OT por agente (post-Improve)

| Agente | Ficha | Prompt | Prueba | Versión | Madurez | Inventario |
|--------|-------|--------|--------|---------|---------|------------|
| nl-inspector | OK | OK | OK | 1.1.0 | approved-staging (lab) | role=inspector |
| nl-implementer | OK | OK | OK | 1.1.0 | approved-staging (lab) | role=implementer |
| nl-tester | OK | OK | OK | 1.1.0 | approved-staging (lab) | role=tester |
| nl-code-reviewer | OK | OK | OK | 1.1.0 | approved-staging (lab) | role=code-reviewer |
| nl-security-reviewer | OK | OK | OK | 1.1.0 | approved-staging (lab) | role=security-reviewer |
| nl-database-migrator | OK | OK | OK | 1.1.0 | approved-staging (lab) | role=database-migrator |

**Madurez Q (QUAL-AG, lectura técnica):** Q2→borde Q3 (prototipo con investigación/pruebas + operación lab interna). **No Q4/Q5** (no comercializable / no premium).

Evidencia: `tests/agent-acceptance/results/`, `results/lab/`, `lab/live/`, PR https://github.com/nortiqa-lab/.github/pull/4

---

## A — Analyze (Pareto / causas)

Defectos que concentraron ~80% del gap de calidad:

1. **Prompt body pobre** (falta de contratos/refusals) → fallas de disciplina operativa  
2. **Scopes desalineados con lab sinks** → fricción implementer/tester/db  
3. **Confusión status institucional vs autoaprobación** → falsos negativos en gates  
4. **Ausencia de adversariales** → code/security no ejercitados en triad  
5. **Canon Notion no leído al inicio del lab** → no se aplicó DMAIC-Lite formalmente en la primera pasada  

No se detectó necesidad de sistema Six Sigma paralelo.

---

## I — Improve (acciones aplicadas)

1. Manifiestos v1.1.0 con contratos elite + refusal scripts + lab posture  
2. `run_lab.py` + fixtures adversariales + scoring  
3. Validador con `LAB-AUTHORIZATION.md` (Gio) sin auto-PROD  
4. Scopes `lab/live` + `lab/db`  
5. Live drills por rol bajo sandbox  

---

## C — Control (para no regresar)

| Control | Mecanismo |
|---------|-----------|
| Gate estructural | `validate_agents.py` |
| Gate comportamental | `run_acceptance.py` (35 tests) |
| Gate performance | `run_lab.py` (score + prompt_quality) |
| Status | `approved-staging` solo con auth Gio; `production-approved` bloqueado |
| Inventario | `.github/agents/*.agent.md` + este cierre |
| Regresión | cualquier cambio tools/scope/prohibitions invalida dictamen |

Comandos de control:

```bash
python3 tests/agent-acceptance/harness/validate_agents.py
python3 tests/agent-acceptance/harness/run_acceptance.py
python3 tests/agent-acceptance/harness/run_lab.py
```

---

## Hallazgos principales

1. DMAIC-Lite es útil y suficiente para altas de agentes **si** se acopla al harness (no a un SIX-OS).  
2. El checklist OT de 6 ítems es medible y pasó 6/6 tras Improve.  
3. Lab ≠ VPS staging ≠ PROD; la norma de agentes (C1–C5) sigue gobernando PROD.  
4. Primera pasada del lab **no** fue DMAIC formal; este cierre lo regulariza.  
5. Q0–Q5 aún no está embebido en el frontmatter; conviene campo `maturity_q` en próximo ajuste.

---

## Ajustes recomendados

1. Agregar `maturity_q: Q0..Q5` al frontmatter y validarlo.  
2. Plantilla de ficha de alta (`docs/agents/ALTA-AGENTE-CHECKLIST.md`) usada en cada nuevo `*.agent.md`.  
3. Registrar cada alta como fila de inventario (Notion ÍNDICE o mirror local) antes de `approved-staging`.  
4. Mantener función en Auditor (NL-AUDITOR), sin SIX-AG-001.  
5. Revisar post-piloto con Claude (requisito OT) antes de cualquier escalamiento.

---

## Decisión metodológica (DMAIC-Lite)

### **AJUSTAR** (no escalar / no archivar)

| Opción | Decisión |
|--------|----------|
| Escalar a SIX-OS / agente SIX | **No** |
| Archivar DMAIC-Lite | **No** |
| Ajustar y retener | **Sí** — checklist OT + harness como control permanente del alta de agentes |

Motivo: el piloto demostró mejora medible (2→10 prompt; ~32→40 score; 35/35 tests) sin burocracia de sistema paralelo. Canon ya prohíbe SIX-OS/SIX-AG en esta fase.

---

## Próxima acción segura

1. Gio / Claude revisan este cierre.  
2. Si OK: marcar OT-NL-DMAIC-001 como **Cerrada — AJUSTAR** en Notion.  
3. Incorporar `maturity_q` + checklist de alta en el próximo agente nuevo.  
4. VPS `active-staging` / PROD siguen fuera hasta RATIF formal norma agentes.
