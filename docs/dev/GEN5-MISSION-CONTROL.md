# Gen5 — Mission Control (contrato de misión)

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

| Campo | Valor |
|-------|--------|
| Fecha | 2026-08-02 |
| Actor | Cursor / `NL-BUILDER` |
| Padre | [`NORTIQA-VANGUARD.md`](./NORTIQA-VANGUARD.md) |
| Schema machine-readable | [`schemas/mission-contract.v0.json`](./schemas/mission-contract.v0.json) |
| Canon Notion | unavailable — bootstrap usado |
| Runtime | **no implementado** en este repo (solo contrato + reglas) |

## 1. Objetivo de Gen5

Convertir un pedido en lenguaje natural en un **contrato de misión verificable** con:

- objetivo y criterios de éxito observables
- scope autorizado (repos, paths, servicios, clases de datos)
- riesgo, autonomía (0–5) y permisos
- plan, rollback y pruebas
- presupuesto (tiempo / tokens / dinero)
- evidencia obligatoria para cerrar
- gates humanos explícitos
- estados y cierre con significado técnico

Gen5 **no** incluye aún células independientes (Gen6) ni gemelo digital completo (Gen7). Puede preparar campos para ellos (`simulating`, `blast_radius`, roles).

## 2. Principios

1. Sin contrato válido → no hay ejecución con side effects (solo análisis / draft del contrato).
2. El ejecutor no auto-certifica el cierre; hace falta evidencia + postura árbitro/`NL-AUDITOR` cuando el nivel lo exige.
3. Ante incertidumbre, **bajar** `autonomy_level` (nunca subir en silencio).
4. Entity hard-stop: solo `nortiqa-lab`. Señales Valent/ERP/cliente → `blocked` + escalate.
5. Secretos: nunca en el contrato en claro; `permissions.secrets` ≤ `reference_only` salvo gate humano documentado (y aún así sin valores).
6. Capacidad + verificabilidad + control deben avanzar juntos (regla Vanguard).

## 3. Flujo

```text
Pedido humano (raw_request)
    ↓
Compilar intención (assumptions + objective)
    ↓
Contrato draft (status=draft)
    ↓
¿human_gates before_plan/before_execute?
    ↓ sí → awaiting_human
    ↓ no / approved
planned → [simulating opcional] → authorized → executing
    ↓
verifying (evidencia vs evidence_required)
    ↓
closed_verified | failed | rolled_back | blocked | cancelled
```

## 4. Máquina de estados

| Estado | Significado | Side effects |
|--------|-------------|--------------|
| `draft` | Contrato incompleto o no validado contra schema | Ninguno |
| `awaiting_human` | Gate humano pendiente | Ninguno hasta decisión |
| `planned` | Plan + rollback + evidencia definidos | Ninguno |
| `simulating` | Vista previa / blast radius (Gen7 light) | Solo lectura / ensayo |
| `authorized` | Autonomía y gates OK para ejecutar | Listo |
| `executing` | Cambios en curso dentro de scope | Sí, acotados |
| `verifying` | Recolección/chequeo de evidencia | Lectura + checks |
| `blocked` | Hard stop; falta humano/privilegio/canon | Detenido |
| `failed` | No cumplió criterios; rollback evaluado | Posible cleanup |
| `rolled_back` | Rollback aplicado | Estado previo buscado |
| `closed_verified` | Evidencia completa + veredicto no-BLOCK | Cerrado |
| `cancelled` | Abortado por humano o presupuesto | Sin claim de éxito |

### Transiciones permitidas (v0)

```text
draft → awaiting_human | planned | cancelled
awaiting_human → planned | draft | cancelled | blocked
planned → simulating | authorized | awaiting_human | cancelled
simulating → authorized | awaiting_human | planned | blocked | cancelled
authorized → executing | awaiting_human | cancelled
executing → verifying | blocked | failed | rolled_back
verifying → closed_verified | failed | rolled_back | blocked | awaiting_human
failed → rolled_back | cancelled | draft
rolled_back → cancelled | draft
blocked → awaiting_human | cancelled | draft
```

Cualquier otra transición → inválida; registrar en `status_history` y no ejecutar.

## 5. Niveles de autonomía ↔ kit

| Level | Puede | Zone kit (`AUTONOMY.md`) | Gate humano típico |
|------:|-------|---------------------------|--------------------|
| 0 | Responder / analizar | green | no |
| 1 | Inspeccionar / diagnosticar | green | no |
| 2 | Escribir archivos reversibles (staging/docs/kit) | green / yellow | notify en yellow |
| 3 | Operar servicios permitidos + rollback | yellow → red si prod-like | before_execute si riesgo ≥ medium |
| 4 | Migraciones / red / externos | red | before_execute obligatorio |
| 5 | Producción | red | before_prod obligatorio |

**Degradación automática:** si `uncertainty.signals` no vacío, `autonomy_level = min(actual, autonomy_floor)` (default floor = 1).

## 6. Criterios de cierre verificable

Una misión solo puede pasar a `closed_verified` si:

1. Schema válido (`mission-contract.v0`).
2. Todos los `success_criteria` tienen evidencia observable referenciada.
3. Todo `evidence_required` con `required_for_close=true` está satisfecho.
4. Tests declarados en `tests` pasaron (o justificados como N/A con gate humano).
5. `human_gates` con `required=true` están `approved` o `skipped_not_required` solo si el nivel no los exige.
6. Veredicto árbitro ∈ {`approve`, `conditional`} — nunca el mismo actor que `roles.executor` en solitario para level ≥ 2.
7. `closeout.result` ∈ {`success`, `partial`} con lista `evidence_refs`.
8. Confirmación `no_contamination` cuando hubo tests/agentes sobre FS compartido.

**Prohibido:** cerrar por frase conversacional (“listo”, “done”) sin checklist.

## 7. Compilador de intención (reglas v0)

Entrada: `source.raw_request` (+ contexto repo/handoff).

Salida: contrato `draft` o `blocked`.

| Señal en el pedido | Acción del compilador |
|--------------------|------------------------|
| Solo pregunta / explicación | level 0–1, `write=false`, rollback `none_readonly` |
| “mejorá / actualizá docs/README” | level 2, paths docs, evidence=diff+structure |
| “diagnosticá / por qué falla” | level 1, health GETs ok, sin write |
| “reiniciá / nginx / prod / DNS / secretos” | level ≥ 4–5, `awaiting_human`, no ejecutar |
| Entidad no Nortiqa | `blocked` + escalate |
| Scope ambiguo | assumptions explícitas + floor autonomía ↓ |
| Dinero / compra / registrar | red / blocked |

### Mapping DISPATCH

| Dispatch | Autonomy tipica | Notas |
|----------|-----------------|-------|
| A lectura | 0–1 | |
| B draft | 1–2 | |
| C versionable PR | 2 | |
| D Notion protegido | blocked hasta auth Gio+PAO/OT | |
| E VPS | 1 (health) o 5 (prod change) | |

## 8. Ejemplo mínimo (docs kit)

Pedido: “Actualizá el puntero de Vanguard en agents/README si falta.”

```json
{
  "schema_version": "mission-contract.v0",
  "mission_id": "MIS-NL-20260802-vanguard-pointer",
  "created_at": "2026-08-02T00:00:00Z",
  "entity": "nortiqa-lab",
  "source": {
    "channel": "cursor",
    "raw_request": "Actualizá el puntero de Vanguard en agents/README si falta.",
    "requester": "Gio",
    "parent_mission_id": null
  },
  "objective": "Asegurar enlace DEV a NORTIQA-VANGUARD.md desde agents/README.md",
  "success_criteria": [
    {
      "id": "sc1",
      "description": "agents/README.md enlaza docs/dev/NORTIQA-VANGUARD.md",
      "observable": "grep/link resuelve a archivo existente"
    }
  ],
  "assumptions": [
    "Solo repo nortiqa-lab/.github; sin product runtime"
  ],
  "scope": {
    "repos": ["nortiqa-lab/.github"],
    "paths_allowed": ["agents/README.md", "docs/dev/"],
    "paths_denied": [".env", ".secrets/", "/opt/"],
    "services_allowed": [],
    "data_classes": ["public", "internal"],
    "out_of_scope": ["VPS", "Notion writes", "product repo runtime"]
  },
  "risk": {
    "level": "low",
    "rationale": "Markdown reversible en kit",
    "blast_radius": {
      "files_estimate": 1,
      "services_estimate": 0,
      "reversible": true
    }
  },
  "autonomy_level": 2,
  "autonomy_zone_kit": "green",
  "dispatch_class": "C",
  "permissions": {
    "read": true,
    "write": true,
    "exec": false,
    "network": "none",
    "secrets": "none"
  },
  "roles": {
    "planner": "NL-ORCH",
    "executor": "NL-BUILDER",
    "tester": "NL-BUILDER",
    "security_reviewer": "NL-AUDITOR",
    "arbiter": "NL-AUDITOR",
    "human_approver": "Gio"
  },
  "plan": [
    {
      "step": 1,
      "action": "Inspeccionar agents/README.md",
      "owner_role": "NL-BUILDER",
      "produces": "diagnóstico link presente/ausente",
      "requires_human": false
    },
    {
      "step": 2,
      "action": "Añadir o corregir puntero si falta",
      "owner_role": "NL-BUILDER",
      "produces": "diff",
      "requires_human": false
    },
    {
      "step": 3,
      "action": "Verificar path destino existe",
      "owner_role": "NL-BUILDER",
      "produces": "check estructura",
      "requires_human": false
    }
  ],
  "rollback": {
    "strategy": "git_revert",
    "steps": ["git revert del commit de la misión"],
    "restore_point_required": false
  },
  "tests": [
    {
      "id": "t1",
      "type": "structure",
      "command_or_check": "test -f docs/dev/NORTIQA-VANGUARD.md",
      "expected": "exit 0"
    }
  ],
  "budget": {
    "time_minutes_max": 30,
    "tokens_max": 100000,
    "money_usd_max": 0,
    "model_preference": []
  },
  "evidence_required": [
    {
      "id": "e1",
      "kind": "diff",
      "description": "diff de agents/README.md o prueba de no-op justificada",
      "required_for_close": true
    },
    {
      "id": "e2",
      "kind": "test_result",
      "description": "path destino existe (structure check)",
      "required_for_close": true
    }
  ],
  "human_gates": [],
  "status": "planned",
  "uncertainty": {
    "score": 0.1,
    "signals": [],
    "autonomy_floor": 2
  },
  "closeout": null,
  "black_box_ref": null
}
```

## 9. Ejemplo gate humano (prod-like)

Pedido: “Reiniciá nginx en producción.”

- `autonomy_level`: 5  
- `status` inicial tras compile: `awaiting_human`  
- `human_gates`: `before_prod` required  
- `permissions.network`: no `prod_write` hasta approval  
- Sin approval → no `authorized`

## 10. Relación con artefactos existentes

| Artefacto | Rol Gen5 |
|-----------|----------|
| `agents/AUTONOMY.md` | Zona green/yellow/red ↔ levels |
| `agents/DISPATCH.md` | Clase A–E ↔ campos dispatch |
| `docs/shared-ai-memory/handoffs/` | Episodio / evidencia `handoff` |
| `docs/dev/NORTIQA-VANGUARD.md` | Visión padre |
| Product bot / Telegram | Posible `source.channel`; no define el contrato |

## 11. Fuera de alcance Gen5 (esta entrega)

- Parser runtime / bot que emita JSON automáticamente
- Ejecutor que enforcee el schema en el VPS
- Células multi-agente reales (Gen6)
- Simulación con restore de DB (Gen7)
- Benchmark suite (Gen8)
- Límites criptográficos (Gen10)

## 12. Definition of Done — schema Gen5 (docs)

- [x] Schema JSON v0 versionado
- [x] Estados + transiciones documentados
- [x] Criterios de cierre verificable
- [x] Reglas de compilación NL → contrato
- [x] Mapa a `NL-*` / AUTONOMY / DISPATCH
- [x] Ejemplos low-risk y high-risk
- [ ] Auditoría ARCHITECT-001 / `NL-AUDITOR`
- [ ] Ratificación Gio
- [ ] Implementación parser en product repo (siguiente ola)

## 13. Verificación (2026-08-02)

| Check | Resultado |
|-------|-----------|
| JSON schema parse | ver comandos en handoff/PR |
| Paths referenciados | deben existir tras commit |
| Secretos en ejemplos | ninguno |
| Notion | unavailable — draft |
| Prod tocado | no |

## 14. Próximo paso recomendado (uno)

Implementar en el repo de producto un compilador **dry-run** (pedido → JSON contrato + validación schema, sin side effects) y usarlo en Gen4 acceptance flows.
