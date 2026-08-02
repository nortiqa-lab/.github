Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

# RACI — Modelos, roles y superficies de trabajo

Fecha: 2026-08-02  
Alcance: kit Nortiqa Lab + operaciones guiadas (incl. cruce LLA DNS cuando Gio lo autorice)  
Principio: **los modelos son motores reemplazables**; el RACI amarra *quién hace / quién responde*, no la marca del LLM.

## Leyenda

| Código | Significado |
|--------|-------------|
| **R** | Responsible — ejecuta el trabajo |
| **A** | Accountable — dueño del resultado; **uno solo por fila** |
| **C** | Consulted — se consulta antes/durante |
| **I** | Informed — se informa al cerrar / en handoff |

Reglas duras:

1. Exactamente **un A** por fila.
2. Si hay duda de autoridad → **A = Gio**.
3. Zona roja (`AUTONOMY.md`) → A siempre Gio; agentes como máximo R/C con gate.
4. Draft ≠ oficial. Ratificación PROD = Gio.
5. Todo brief/misión/PR/DEV doc sustancial debe declarar RACI (plantilla al final).

---

## 1. Catálogo de actores

### 1.1 Autoridad y roles kit (`NL-*`)

| ID | Actor | Notas |
|----|-------|-------|
| GIO | Gio | Dirección General; A final |
| ORCH | `NL-ORCH` | Clasifica, despacha, consolida |
| AUD | `NL-AUDITOR` / Claude ARCHITECT-001 | Gates, dictamen draft |
| BLD | `NL-BUILDER` / Cursor NQ-DEV-IMPLEMENTER | Implementa, verifica, PR |
| OPS | `NL-OPS` | Health, staging, prepare prod |
| PRD | `NL-PRODUCT` | Superficies públicas |
| MEM | `NL-MEMORY` | Handoffs / continuidad |

### 1.2 Motores / modelos (reemplazables)

| ID | Motor | Uso típico en Nortiqa hoy |
|----|-------|---------------------------|
| GRK | Cursor Grok 4.5 (este cloud agent) | Docs, orquestación, PRs kit, guías |
| CMP | Cursor Composer | Edits multiarchivo rápidos en IDE |
| CLA | Claude (chat / ARCHITECT-001) | Auditoría, arquitectura, gates |
| CCH | Claude Chrome extension | Ejecución UI en el navegador del humano |
| GPT | ChatGPT / KNOW-001 | Diseño, borradores, investigación |
| CDX | Codex | Implementación código en repos producto |
| GEM | Gemini | Alternativa multimodal / investigación |
| GRQ | Groq | Inferencia rápida cuando esté cableada |
| OLL | Ollama local (loopback) | Degradado soberano / privado |

### 1.3 Superficies (no son A)

| ID | Superficie | Rol |
|----|------------|-----|
| NOT | Notion canon | Fuente de verdad cuando reachable |
| GH | GitHub (este kit / product) | Versionado |
| CF | Cloudflare dashboard / API | DNS autoritativo (cuando aplique) |
| NIC | NIC Argentina | Registro / delegación `.ar` |
| VPS | Servidor propio / SC2027 | Alojamiento, Nginx, TLS |

---

## 2. RACI por tipo de trabajo (roles kit)

| Trabajo | GIO | ORCH | AUD | BLD | OPS | PRD | MEM |
|---------|:---:|:----:|:---:|:---:|:---:|:---:|:---:|
| Objetivo / brief inicial | A | R | C | I | I | I | I |
| Clasificación + despacho | A | R | C | I | I | I | I |
| Draft docs / runbooks / PR kit | A | C | C | R | I | C | R |
| Implementación código reversible | A | C | C | R | I | C | I |
| Gate / dictamen draft | A | I | R | C | C | I | I |
| Ratificación oficial / PROD | A/R | I | C | I | C | I | I |
| Health público read-only | A | I | C | I | R | I | I |
| Promote / Nginx / DNS registrar | A | I | C | I | R* | I | I |
| Handoff de sesión | A | C | I | R | R | R | R |
| Cruce de entidad documentado | A | R | C | C | I | I | R |

\*OPS prepara/ejecuta solo con gates; **A permanece Gio**.

---

## 3. RACI por motor (qué modelo usa cada lane)

Convención: el **A** sigue siendo Gio o el rol kit dueño; el motor es **R** (ejecuta) o **C**.

| Lane / tarea | A | R (motor preferido) | C | I | Evitar como R primario |
|--------------|---|---------------------|---|---|------------------------|
| Orquestar pedido ambiguo | GIO | GRK / ORCH | CLA, GPT | MEM | CCH solo |
| Diseño / brainstorm docs | GIO | GPT (KNOW-001) | CLA, GRK | MEM | OPS en prod |
| Auditoría arquitectura / gates | GIO | CLA (ARCHITECT-001) | GRK, GPT | BLD, OPS | CCH |
| Implementar kit Markdown + PR | GIO | GRK / CMP → BLD | CLA | MEM | CCH para git |
| Implementar producto/código | GIO | CDX / CMP → BLD | CLA, GRK | OPS | GPT sin tests |
| Clicks UI (Cloudflare, NIC, paneles) | GIO | CCH (+ humano presente) | GRK (brief) | AUD | GRK sin browser |
| DNS / registrar changes | GIO | Humano o CCH bajo brief | OPS, AUD | MEM | Agente autónomo |
| Dictamen / PAO-OT Notion write | GIO | Humano (+ AUD draft) | CLA | ORCH | Cualquier motor solo |
| Degradado offline / privado | GIO | OLL + scripts locales | GRK offline docs | MEM | Cloud APIs |
| Árbitro crítico (doble check) | GIO | CLA + GRK en paralelo | GPT | AUD | Un solo modelo “votando” |

### 3.1 Matriz compacta motores × capacidad

| Capacidad | GRK | CMP | CLA | CCH | GPT | CDX | GEM | GRQ | OLL |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Orquestación kit | R | C | C | — | C | — | C | — | C |
| Auditoría / gate | C | — | R | — | C | — | C | — | — |
| Draft diseño | C | — | C | — | R | — | C | — | — |
| Edición repo / PR | R | R | C | — | C | R | — | — | — |
| Browser UI | C* | — | C* | R | — | — | — | — | — |
| Runtime prod | — | — | C | — | — | C | — | — | C |
| Privacidad local | — | — | — | — | — | — | — | — | R |

\*GRK/CLA pueden **redactar briefs** para CCH; no controlan el mouse del humano.

---

## 4. RACI — flujo DNS `llasantacruz.com.ar` (cruce autorizado)

| Paso | GIO | GRK (Cursor) | CCH (Claude Chrome) | CLA/AUD | CF | NIC | VPS/Nginx |
|------|:---:|:------------:|:-------------------:|:-------:|:--:|:---:|:---------:|
| Decidir Cloudflare Free (no Hostinger NS) | A | R (doc) | I | C | I | I | I |
| Add domain + plan Free en Cloudflare | A | C (brief) | R | I | R* | — | — |
| Copiar nameservers exactos | A | I | R | I | R* | — | — |
| Delegar NS en NIC Argentina | A | C (texto exacto) | R | C | I | R* | — |
| Crear `A portal` → IP servidor | A | C | R | I | R* | — | C |
| Nginx + TLS en servidor | A | C (runbook) | I | C | I | — | R |
| Verificar `dig` / activación | A | R (check público) | C | I | I | I | I |
| Tocar `nortiqalab.com` DNS | A | — | — | — | — | — | — |

\*Superficie donde ocurre el cambio; **A = Gio**. Casilla vacía / `—` = no participa.  
**Prohibido:** Hostinger NS parking sin zona hPanel; auto-cambio DNS por agente sin Gio.

Estado actual (2026-08-02): dominio aún **NXDOMAIN** públicamente → pasos Add domain / Delegar **pendientes** (R humano o CCH).

---

## 5. RACI — ciclo DEV → PROD (workflow)

| Etapa | GIO | ORCH | AUD/CLA | BLD/GRK/CDX | OPS | MEM |
|-------|:---:|:----:|:-------:|:-----------:|:---:|:---:|
| Solicitud | A | R | I | I | I | I |
| Diagnóstico / inspección | A | R | C | R | C | I |
| Propuesta mínima | A | C | C | R | C | I |
| Implementación | A | I | C | R | I | I |
| Pruebas / verify | A | I | C | R | R | I |
| Auditoría draft | A | I | R | C | C | I |
| Ratificación | A/R | I | C | I | I | I |
| PROD gated | A | I | C | I | R | I |
| Handoff cierre | A | C | I | R | R | R |

---

## 6. Selección rápida “¿qué modelo ahora?”

| Situación | Elegir | RACI mínimo |
|-----------|--------|-------------|
| “Hacelo” en este kit / docs / PR | GRK (Cursor Cloud) | A=GIO, R=GRK/BLD, C=AUD, I=MEM |
| “Auditalo / ¿se puede?” | CLA | A=GIO, R=CLA/AUD, C=BLD, I=ORCH |
| “Diseñá opciones” | GPT | A=GIO, R=GPT, C=CLA, I=BLD |
| “Clickeá Cloudflare/NIC” | CCH + brief de GRK | A=GIO, R=CCH, C=GRK, I=AUD |
| “Codeá en product repo” | CDX/CMP | A=GIO, R=CDX/BLD, C=CLA, I=OPS |
| “Sin internet / secreto local” | OLL + runbooks | A=GIO, R=OLL/OPS, C=AUD, I=MEM |
| Decisión crítica multi-motor | CLA + GRK en paralelo; A=Gio | A=GIO, R=CLA+GRK, C=AUD, I=MEM |

Este run (`cursor-grok-4.5-high-fast`) es **correcto** como R de docs/orquestación/guías; **incorrecto** como R único de clicks UI o cambios de registrar.

---

## 7. Plantilla RACI obligatoria (pegar en briefs / handoffs / PRs)

```markdown
## RACI
| Actividad | A | R | C | I |
|-----------|---|---|---|---|
| <actividad> | Gio | <rol/motor> | <…> | <…> |
```

Checklist de cierre:

- [ ] Un solo A por actividad
- [ ] Zona roja con A=Gio explícito
- [ ] Motor elegido justificado (o “N/A — humano”)
- [ ] Sin cruce de entidad sin autorización documentada

---

## 8. Gobernanza de este documento

- Estado: **DEV / Borrador**
- No renombra el roster `NL-*`
- No declara PROD
- Próxima auditoría: ARCHITECT-001 / `NL-AUDITOR`
- Próxima ratificación: Gio

## Próximo paso recomendado

Usar la §4: CCH ejecuta Add domain Free en Cloudflare; GRK recibe los 2 NS y arma el brief NIC → Delegar.
