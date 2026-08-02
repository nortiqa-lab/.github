# BENCH-NQ-ORCH-001 — Benchmark de orquestación por tarea

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

| Campo | Valor |
|-------|--------|
| ID | `BENCH-NQ-ORCH-001` |
| Categoría | Orquestación / agentes / automatización |
| Fecha evaluación | 2026-08-02 |
| Próxima revisión | 2026-10-01 o ante piloto con >50 corridas/semana |
| Actor | Cursor / `NL-BUILDER` (+ postura `NL-ORCH`) |
| Plantilla | Notion `PLT-NQ-BENCH-TOOLS-001` |
| Canon Notion | leído vía MCP (`MEM-NL-ROOT-001`, `CAT-NQ-TOOLS-001`, `PLAN-NL-SKILLS-IA-001`, Agent Router / n8n) |
| Estado propuesto (capa runtime marketplace) | **Descartar por ahora** |
| Estado propuesto (stack propio) | **Adoptar / seguir endureciendo** |

## 0. Distinción evidencia

| Tipo | Contenido |
|------|-----------|
| **Hecho** | Existen en kit: `NL-ORCH`, `agents/AUTONOMY.md`, n8n público, Gen5 Mission Control + compiler dry-run, Agent Router/Factory en Notion DEV. Búsqueda Notion: Chargebee/Airwallex/Arize/Atlan/AWS Agents **no** indexados. |
| **Inferencia** | Los plugins marketplace que Gio vio en Cursor no se persistieron en Notion; la necesidad real hoy es despacho + workflows + contratos, no un runtime AWS. |
| **Recomendación** | Usar matriz §8; no instalar Agent Orchestration marketplace; aplicar criterios §9 al trabajo del agente. |

---

## 1. Problema y objetivo

**Problema real:** hay varias “orquestaciones” posibles (rol humano, n8n, router, Gen5, marketplace AWS/Arize) y riesgo de sumar herramientas sin caso de uso, o de no usar las que ya existen.

**Usuario afectado:** Gio, `NL-*`, AUDITOR.

**Frecuencia:** diaria (despacho), semanal (automatizaciones), episódica (productos / LLA / home).

**Criterios de éxito del benchmark:**

1. Cada tarea tiene **una** capa primaria de orquestación.
2. No se introduce lock-in cloud sin piloto.
3. Se respeta aislamiento de entidades.
4. El dictamen es accionable en una línea por tarea.

---

## 2. Tareas evaluadas (casos reales)

| ID | Tarea | Entidad | Madurez actual | Qué “orquesta” hace falta |
|----|-------|---------|----------------|---------------------------|
| T1 | Home institutional polish / apply WP | Nortiqa Lab | Paquete parked (PR #11 en otra rama) | Despacho BUILDER→OPS; no multi-agente cloud |
| T2 | Aporte solidario / pagos recurrentes | LLA Santa Cruz (producto Nortiqa posible) | Legal: no cobros; PSP TBD | Flujo legal→producto→PSP; **no** marketplace Payments |
| T3 | Agent Factory / laboratorio agentes | Nortiqa Lab | DEV documental | Coordinar piezas existentes; anti-duplicación |
| T4 | Pedido one-line → ejecución kit | Nortiqa Lab | Operativo en este repo | `NL-ORCH` + autonomía green/yellow/red |
| T5 | Workflows API/webhook/jobs | Nortiqa Lab | n8n Adoptar P0 | Orquestación determinista |
| T6 | Compilar misión verificable (Gen5) | Nortiqa Lab | Contrato + compiler dry-run | Contrato antes de side effects |

---

## 3. Candidatos incluidos

| Código | Candidato | Tipo | Motivo de inclusión |
|--------|-----------|------|---------------------|
| A | `NL-ORCH` + kit `agents/` | Principal (rol) | Ya canon del repo |
| B | n8n | Principal (workflow) | `CAT-NQ-TOOLS-001` Adoptar P0 |
| C | Agent Router / Factory (Notion DEV) | Alternativa interna | Diseñado para fábrica de agentes |
| D | Gen5 Mission Control + `mission-compiler` | Principal emergente | Ya en `main` (docs + tool dry-run) |
| E | Cursor marketplace Agent Orchestration (AWS Agents, SageMaker, Arize, Atlan) | Competidor externo | Pregunta explícita de Gio |
| F | Solo Gio manual | Baseline | Control total, no escala |

**Fuera de alcance de este bench (capa distinta):** plugins Payments (Chargebee/Airwallex/Circle/1inch) — se mencionan solo en T2 como **no candidatos** hasta dictamen legal + PSP AR.

---

## 4. Metodología

| Ítem | Definición |
|------|------------|
| Entorno | Documental + inspección kit/Notion; **sin** instalar plugins marketplace |
| Dataset | T1–T6; fuentes: `AGENTS.md`, `AUTONOMY.md`, `CAT-NQ-TOOLS-001`, `PLAN-NL-SKILLS-IA-001`, investigación LLA financiamiento, Gen5 docs |
| Repeticiones | Una pasada de scoring con pesos fijos; no A/B runtime |
| Equivalencia | Misma tarea, misma escala 1–10, mismos pesos |
| Limitaciones | Sin piloto AWS/Arize; puntuación E es **documental/inferida**. Confianza global del bench: **Media-Alta** para A–D; **Media** para E |

---

## 5. Casos de prueba lógicos (reproducibles)

| ID | Caso | Input | Resultado esperado | Métrica |
|----|------|-------|--------------------|---------|
| T01 | Despacho one-line | “pulí home sin tocar prod” | `NL-ORCH`→`NL-BUILDER`; PR draft; sin prod | Ajuste / fricción |
| T02 | Workflow health | GET públicos | n8n/ops runbook; sin agente cloud | Determinismo |
| T03 | Anti-duplicación factory | “crear Agent Tester nuevo” | Factory/Router bloquea; reutiliza tester | Duplicados evitados |
| T04 | Aporte LLA | “instalar Chargebee skill” | STOP legal + entity; no install | Hard-stop correcto |
| T05 | Misión Gen5 | pedido con riesgo medio | contrato draft + autonomy bajada | Schema válido |
| T06 | Marketplace E | “activar AWS Agents” | Observar/Descartar; sin lock-in | Costo de cambio |

---

## 6. Matriz comparativa (ponderada)

Escala 1–10. Pesos suman 100%.

| Dimensión | Peso | A Kit/ORCH | B n8n | C Router/Factory | D Gen5 | E Marketplace | Evidencia |
|-----------|------|------------|-------|------------------|--------|---------------|-----------|
| Calidad ajuste a tareas actuales | 15 | 9 | 8 | 7 | 8 | 3 | A/D cubren T4/T6; E no mejora T1–T2 |
| Productividad | 12 | 8 | 8 | 6 | 7 | 4 | E añade setup AWS |
| Costo total (bajo = alto score) | 12 | 9 | 8 | 8 | 9 | 3 | E: cuenta cloud + aprendizaje |
| Integración stack Nortiqa | 15 | 9 | 9 | 7 | 8 | 2 | n8n/MCP/GitHub ya cableados |
| Automatización | 10 | 5 | 9 | 6 | 6 | 7 | B gana en jobs; E fuerte en cloud agents |
| Seguridad / gobernanza | 12 | 9 | 7 | 8 | 9 | 4 | Gen5 + AUTONOMY; E amplía superficie |
| Escalabilidad | 8 | 5 | 8 | 7 | 7 | 8 | E escala cloud; prematuro |
| Dependencia (bajo lock-in = alto) | 8 | 9 | 7 | 8 | 9 | 2 | AWS Agents = lock-in |
| Madurez en Nortiqa | 5 | 8 | 8 | 5 | 6 | 1 | E no instalado / no en Notion |
| Valor estratégico 90d | 3 | 7 | 8 | 7 | 9 | 3 | Gen5 alinea Vanguard |
| **Puntaje ponderado** | 100 | **8.05** | **8.05** | **7.00** | **7.85** | **3.71** | Verificado con script local |

### Cálculo (referencia, verificado)

```text
A: 0.15*9+0.12*8+0.12*9+0.15*9+0.10*5+0.12*9+0.08*5+0.08*9+0.05*8+0.03*7 = 8.05
B: 0.15*8+0.12*8+0.12*8+0.15*9+0.10*9+0.12*7+0.08*8+0.08*7+0.05*8+0.03*8 = 8.05
C: 0.15*7+0.12*6+0.12*8+0.15*7+0.10*6+0.12*8+0.08*7+0.08*8+0.05*5+0.03*7 = 7.00
D: 0.15*8+0.12*7+0.12*9+0.15*8+0.10*6+0.12*9+0.08*7+0.08*9+0.05*6+0.03*9 = 7.85
E: 0.15*3+0.12*4+0.12*3+0.15*2+0.10*7+0.12*4+0.08*8+0.08*2+0.05*1+0.03*3 = 3.71
```

---

## 7. Costos (orden de magnitud, sin precios inventados)

| Concepto | A | B | C | D | E |
|----------|---|---|---|---|---|
| Licencia | Incluida en Cursor/humano | Ya operando | Documental | Tool local stdlib | Cuenta AWS + productos |
| Consumo | Tokens sesión | Host n8n existente | Bajo | Tokens compile | Tokens + API Bedrock/etc. |
| Capacitación | Baja (ya en kit) | Media | Media | Media (schema) | Alta |
| Migración | N/A | N/A | Bajo | Bajo | Alto |
| **TCO relativo 90d** | Bajo | Bajo-medio | Bajo | Bajo | Alto |

---

## 8. Matriz de necesidad (derivada del bench)

Leyenda: **Usar** · **Endurecer** · **Observar** · **No usar** · **Bloqueado**

| Tarea | Primaria | Secundaria | Marketplace E | Payments plugins | Notas |
|-------|----------|------------|---------------|------------------|-------|
| T1 Home polish | **Usar A** (`NL-BUILDER` bajo ORCH) | OPS apply checklist | **No usar** | **No usar** | Sin runtime multi-agente |
| T2 Aporte LLA | **Bloqueado** legal | Producto Nortiqa (diseño) | **No usar** | **No usar** | Dictamen electoral/fiscal antes de PSP |
| T3 Agent Factory | **Endurecer C** | A para despacho | **Observar** Arize solo si hay métricas | **No usar** | No crear segundo router |
| T4 Pedido one-line | **Usar A** | **Endurecer D** Gen5 | **No usar** | **No usar** | Compilar misión cuando haya side effects |
| T5 Workflows | **Usar B** n8n | A si hay decisión humana | **No usar** | N/A | Determinista > LLM |
| T6 Misión Gen5 | **Usar D** | A consolida | **Observar** Arize post-escala | **No usar** | Runtime Gen5 aún no implementado |

### Dictamen por candidato

| Candidato | Decisión | Prioridad | Confianza |
|-----------|----------|-----------|-----------|
| A Kit / `NL-ORCH` | **Adoptar** (mantener) | P0 | Alta |
| B n8n | **Adoptar** (mantener) | P0 | Alta |
| C Router / Factory | **Probar / Endurecer en DEV** | P1 | Media |
| D Gen5 Mission Control | **Probar / Endurecer** | P1 | Media-Alta |
| E Marketplace Agent Orchestration | **Descartar por ahora** | P3 | Media |
| F Solo manual | Baseline de emergencia | — | Alta |

**Ganador valor/costo actual:** A + B.  
**Ganador estratégico 90d:** D (contratos) + C (fábrica) sobre E.  
**Mejor ajuste Nortiqa:** no sumar AWS Agents; completar Gen5 + n8n + kit.

---

## 9. Mejores prácticas aplicadas al criterio de trabajo del agente

Estas reglas quedan como **criterio operativo DEV** (no PROD) para sesiones Cursor/`NL-BUILDER`:

1. **Bench antes de instalar** — ninguna skill/plugin marketplace sin ficha + caso T0x + decisión Adoptar/Probar/Observar/Descartar (`PLAN-NL-SKILLS-IA-001` + esta plantilla).
2. **Preferir stack existente** — A/B/D antes que E; no inventar segundo canon ni segundo router.
3. **Una capa primaria por tarea** — ver matriz §8; evitar orquestar lo mismo en tres sistemas.
4. **Hecho / inferencia / recomendación** — separar siempre en docs y handoffs.
5. **Entity hard-stop** — LLA/Valent/ERP no se mezclan con Nortiqa salvo autorización documentada de Gio.
6. **Menor riesgo primero** — inspección git/paths → dry-run → side effects; Gen5: sin contrato válido, sin side effects.
7. **Autonomía AUTONOMY.md** — green ejecuta; red escala con ask exacto; ambigüedad → interpretación mínima reversible.
8. **Evidencia reproducible** — comandos + resultado en handoff; no claim PROD/oficial.
9. **Marketplace = confianza E** hasta auditoría de código (`PLAN-NL-SKILLS` nivel E).
10. **Observabilidad (Arize-clase) solo con volumen** — umbral tentativo: >50 corridas/semana o incidentes de calidad/costo no medibles con logs actuales.

---

## 10. Riesgos y límites

| Riesgo | Control |
|--------|---------|
| Instalar E por moda | Matriz §8 + §9.1 |
| Usar n8n para decisiones de riesgo alto | Human-in-the-loop; Gen5 gates |
| Contaminar LLA con stack Nortiqa payments | STOP T2; dictamen legal |
| Duplicar Factory vs Gen5 vs ORCH | ORCH despacha; Gen5 contrato; Factory fabrica agentes; n8n ejecuta flujos |
| Falsa seguridad documental | Piloto técnico antes de Adoptar P0 nuevo |

**No usar este bench para:** autorizar compras AWS, activar cobros LLA, promover DEV→PROD.

---

## 11. Seguimiento

| Fecha | Puntaje E | Posición stack | Decisión | Próxima revisión |
|-------|-----------|----------------|----------|------------------|
| 2026-08-02 | 3.71 | A/B primarios; D/C endurecer | Descartar E | 2026-10-01 |

---

## 12. Fuentes

| Fuente | Tipo |
|--------|------|
| `agents/AUTONOMY.md`, `agents/roles/NL-ORCH.md`, `AGENTS.md` | Prueba propia / kit |
| Notion `CAT-NQ-TOOLS-001`, `PLAN-NL-SKILLS-IA-001`, `PLT-NQ-BENCH-TOOLS-001` | Documentación canónica DEV |
| Notion investigación financiamiento LLA; `PROD-NQ-COMUNIDAD-POLITICA-001` | Documentación; PSP TBD |
| Notion Agent Router / n8n logs | Evidencia histórica DEV |
| `docs/dev/GEN5-MISSION-CONTROL.md`, `tools/mission-compiler/` | Prueba propia dry-run |
| Scores E (AWS/Arize/Atlan) | Inferencia analista (sin piloto) |

---

## 13. Validación / gobernanza

| Rol | Estado |
|-----|--------|
| Generador | Cursor / `NL-BUILDER` |
| Auditor | Pendiente `NL-AUDITOR` / ARCHITECT-001 |
| Ratificación | Pendiente Gio |
| Estado final | **DEV / Borrador** |

### Próximo paso recomendado (uno)

Endurecer T4 con Gen5: al recibir un pedido con side effects, emitir envelope `mission-compiler` antes de editar — sin instalar marketplace E.
