Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Fecha: 2026-08-02  
Actor: Cursor / `NL-AUDITOR` posture + `NL-MEMORY` inventory  
Entidad: **Nortiqa Lab únicamente**  
Canon leído: MEM-NL-ROOT-001, Centro Doc Madre, DICT-NL-GITHUB-REPOS-001, GOV-NL-DOCUMENTACION-CANONICA-001 (DEV), PAO-NL-DOC-CENT-001 clasificación (241 docs), PLAN-NL-AF-MIG-001  

---

# AUD-NL-NOTION-GIT-001 — Auditoría Notion → Git (normalización)

## 1. Resultado ejecutivo

Notion concentra el canon y ~241+ documentos operativos clasificados; Git apenas refleja el **kit de agentes** (`nortiqa-lab/.github`) y un **product/ops thin** (`giovanyalbea-dotcom/nortiqa-lab`). La normalización no es “subir todo Notion a Git”: es definir **qué debe ser versionable**, en **qué repo**, con **qué estado**, sin contaminar entidades.

**Hallazgo rector (hecho):** los documentos madre (Manifiesto, PAO, Índice Reglas, Prompt Maestro, dictámenes, planes GitHub, Gen4 staging) **no** están espejados como archivos en los repos accesibles.

## 2. Mapa Notion (hechos observados)

### 2.1 Raíz canónica

| Pieza | URL / ID | Notas |
|-------|----------|-------|
| Nortiqa Lab (home) | https://app.notion.com/p/346e4fe3bfea80868179f9ad305dda58 | Contenedor |
| Centro de Documentación Madre | https://app.notion.com/p/350e4fe3bfea81648421c2a3e09e2a5c | Piezas protegidas + cientos de DICT/PAO/ops |
| MEM-NL-ROOT-001 | https://app.notion.com/p/382e4fe3bfea818aacfad4f9793a697f | Punto de entrada IA |
| Manifiesto | https://app.notion.com/p/34ae4fe3bfea816c8895f3c4d5a32e03 (+ duplicado `…a2f8cd2f766766ae`) | **Duplicado detectado** |
| Prompt Maestro | https://app.notion.com/p/34ae4fe3bfea8128a102fd32bc8920aa (+ duplicado) | **Duplicado detectado** |
| Índice Maestro Reglas | https://app.notion.com/p/350e4fe3bfea815eaaaafc8ad3657ce2 | Madre vigente |
| DB-NL-KNOW-001 | https://app.notion.com/p/2124a237c3a64c90afb38415ce4b48c4 | Base conocimiento (MEM-NL-ROOT) |
| PLAN-NL-GITHUB-001 | https://app.notion.com/p/380e4fe3bfea81a7b086f3071d2f5e2b | Rector Git |
| DICT-NL-GITHUB-REPOS-001 | https://app.notion.com/p/395e4fe3bfea8149a652dca28f38d73f | Repos planeados; ratificado 2026-07-06 |
| GOV-NL-DOCUMENTACION-CANONICA-001 | https://app.notion.com/p/3afe4fe3bfea816180b4e2a2a8f97fdc | **DEV** — política anti-duplicación |
| PAO-NL-DOC-CENT-001 tabla | https://app.notion.com/p/391e4fe3bfea8195bc81f742045d34d8 | **241 docs** clasificados (corte 2026-06-22) |

### 2.2 Volumen y deuda documental (inferencia desde DOC-CENT)

Del análisis de 241 docs (no re-contado página a página en esta sesión):

| Categoría | ~N | Implicancia Git |
|-----------|----|-----------------|
| DICT oficiales | ~42 | Versionar **vigentes** + índice; históricos en archive/ |
| PAO sin dictamen | ~18 | No subir como “oficial”; listar gaps |
| REG/LOG | ~38 | Selectivo (incidentes / cierres críticos) |
| Instrucciones antiguas | ~31 | Mayoría **no** a Git (deprecated) |
| Borradores | ~28 | Solo si siguen activos (DEV/) |
| Ambiguos | ~30 | Gate humano antes de cualquier mirror |
| Artefactos DB/matriz | ~32 | Schema + export CSV; no dump ciego |

### 2.3 Contaminación / aislamiento (riesgo alto)

En Centro Madre / home aparecen piezas **fuera de Nortiqa Lab puro** o de frontera dudosa:

- LOG-NL-VALENT-EVO-001 (Valent)
- DICT-NL-ERP-ODOO-001 (Nortiqa + LLA Santa Cruz)
- DOC-VAL-CV-001 / REG-NL-CV-EXEC (Valent CV)
- Convenio Nortiqa–Surlancer (DEV)
- Prompt organigrama LLA Santa Cruz

**Regla de auditoría:** excluir de Git Nortiqa salvo autorización explícita de Gio + decisión documentada de cruce.

## 3. Mapa Git (hechos)

| Repo | Contenido versionable relevante | Gap vs Notion |
|------|----------------------------------|---------------|
| `nortiqa-lab/.github` | `AGENTS.md`, `agents/*` kit, `docs/dev/*`, handoffs, `.cursor/rules` | Sin Manifiesto/PAO/Índice/DICT/ADR series |
| `giovanyalbea-dotcom/nortiqa-lab` | Thin AGENTS, `docs/server-ops`, `server-ops/sc2027/*`, 1 decisión DEC-NL-OLLAMA | Sin kit agentes; sin Gen4; sin AppFlowy |
| `nortiqa-lab/nortiqa-lab.github.io` | Solo `index.html` | N/A |
| Repos DICT (`infra`, `n8n-workflows`, `queryos`, `sc2027-app`) | **No existen** en org (lista gh: 2 repos) | Fase 0 de DICT-NL-GITHUB-REPOS-001 incompleta |

**Gen 4 / botctl / ADR-040 / L3:** evidenciado en VPS staging + closeout DEV en kit; **ausente** del product GitHub.

**AppFlowy:** presente en Notion (PLAN + INT bridge); **0** menciones en Git accesible.

## 4. Modelo de normalización propuesto (recomendación)

Tres capas (compatible con GOV-NL-DOCUMENTACION-CANONICA-001 DEV y DICT-NL-GITHUB-REPOS-001):

```text
L0 Canon operativo IAs     → nortiqa-lab/.github  (o futuro docs-canon privado)
L1 Código / ops producto   → repos por producto (infra, n8n-workflows, queryos, sc2027…)
L2 Memoria de sesión       → docs/shared-ai-memory/handoffs (ya existe; no sustituye Notion)
```

### 4.1 Qué SÍ subir a Git (prioridad P0–P2)

| Prioridad | Pieza Notion | Destino Git propuesto | Forma |
|-----------|--------------|------------------------|-------|
| **P0** | MEM-NL-ROOT-001 (mirror resumido + links) | `.github/docs/canon/MEM-NL-ROOT-001.md` | Mirror controlado, no reemplaza Notion hasta AppFlowy |
| **P0** | Manifiesto (canónico único) | `.github/docs/canon/MANIFIESTO.md` | Resolver duplicado Notion primero |
| **P0** | Índice Maestro Reglas | `.github/docs/canon/INDICE-REGLAS-IA.md` | Markdown |
| **P0** | Protocolo PAO (si página madre identificada) | `.github/docs/canon/PROTOCOLO-PAO.md` | Markdown |
| **P0** | Prompt Maestro (canónico único) | `.github/docs/canon/PROMPT-MAESTRO.md` | Resolver duplicado |
| **P0** | SHARED_RULES/AUTONOMY ya en kit | mantener | Ya versionado |
| **P1** | DICT-NL-GITHUB-001 + DICT-NL-GITHUB-REPOS-001 + PLAN-NL-GITHUB-001/002 | `.github/docs/canon/github/` | Markdown |
| **P1** | DICT-NL-MEM-001, DICT-NL-SERVIDOROPS-001, DICT-NL-NORMA-AGENTES-001 | `.github/docs/canon/dictamenes/` | Solo vigentes |
| **P1** | Gen4: ADR-040, L3, manifiesto bot, `sc2027-botctl` | product repo o `infra`/`sc2027-app` | Código + docs desde VPS |
| **P1** | INT-N8N-APPFLOWY-BRIDGE-001 + OpenAPI VPS | `n8n-workflows` o `.github/docs/integrations/` | Sin secretos |
| **P1** | GOV-NL-DOCUMENTACION-CANONICA-001 | `.github/docs/dev/` hasta ratificación | Ya hay política alineada en rules |
| **P2** | Índice de DICT/PAO vigentes (tabla) | `.github/docs/canon/INDEX.md` | Metadatos + URL Notion/AppFlowy |
| **P2** | Incidentes críticos (ej. SC2027 2026-07-04) | `infra` o product `docs/server-ops/` | Selectivo |
| **P2** | Export CSV de DB-NL-KNOW (sanitizado) | repo privado `knowledge` o `queryos` | Sin PII/secretos |

### 4.2 Qué NO subir (o solo con gate)

- Bandeja DOC-CENT operativa (instrucciones ChatGPT, tandas, autorizaciones efímeras)
- Duplicados / DEPRECATED / vacíos
- Cualquier Valent / LLA / ERP Gio+Edson / personal
- Secretos, `.env`, tokens, project-ids sensibles en claro
- Bases Notion con relaciones complejas sin reconstrucción (mejor CSV + schema)
- Comentarios / historial de actividad Notion

## 5. Plan de auditoría (ejecutable)

### Fase A — Inventario vivo (read-only)

1. Export Notion Markdown+CSV (workspace o árbol Nortiqa Lab) → backup offline.
2. Generar inventario maestro CSV con columnas:  
   `id, title, url, type, entity, status, owner, last_edited, git_target, migrate_action, notes`
3. Cruzar con tabla DOC-CENT 241 + Centro Madre actual (delta post 2026-06-22).
4. Marcar duplicados (Manifiesto×2, Prompt×2, etc.).
5. Separar entity tags: `NL` / `VALENT` / `LLA` / `SURLANCER` / `PERSONAL` / `AMBIGUOUS`.

### Fase B — Gap Git vs Canon

1. Checklist P0: ¿existe archivo en Git? sí/no/parcial.
2. Repos DICT-NL-GITHUB-REPOS: crear o rechazar con PAO (hoy faltan).
3. Pull desde VPS de Gen4 + AppFlowy OpenAPI (sin secretos).
4. Emitir matriz gap (plantilla §7).

### Fase C — Dictamen de alcance

1. Claude emite DICT (sugerido: `DICT-NL-NOTION-GIT-001`) sobre alcance P0/P1.
2. Gio ratifica repos destino + exclusiones de entidad.
3. Solo entonces PRs de mirror (draft).

### Fase D — Ejecución por lotes (post-ratificación)

| Lote | Contenido | Repo |
|------|-----------|------|
| G1 | Canon P0 (5 docs madre) | `.github` |
| G2 | GitHub plans/dictámenes | `.github` |
| G3 | Gen4 + botctl desde staging | product/`infra` |
| G4 | n8n exports + AppFlowy bridge docs | `n8n-workflows` |
| G5 | Índice DICT vigentes | `.github` |

Cada lote: PR draft → audit → merge humano.

## 6. Criterios de “normalizado”

- [ ] Un Manifiesto / un Prompt Maestro (sin duplicados vivos)
- [ ] MEM-NL-ROOT mirror en Git apunta a mismos IDs vigentes
- [ ] Índice Reglas + PAO protocol versionados
- [ ] Kit agentes = única fuente de roles `NL-*` (ya casi)
- [ ] Gen4 artefactos fuera del VPS-only
- [ ] 0 secretos en Git
- [ ] 0 cruces de entidad en repos `nortiqa-lab`
- [ ] Inventario CSV versionado con owner + estado
- [ ] Repos DICT creados o formalmente diferidos

## 7. Plantilla de matriz gap (usar en ejecución)

```csv
notion_id,title,entity,status_notion,in_git,git_path,priority,action,blocker
382e4fe3…,MEM-NL-ROOT-001,NL,canon,no,,P0,mirror,
34ae4fe3…,Manifiesto,NL,canon,no,,P0,mirror+dedupe,duplicate_page
…,
```

## 8. Relación con AppFlowy

Esta auditoría **alimenta** la migración AppFlowy (ver `PLAN-APPFLOWY-MIGRATION-PREP-001.md`):

- Git = respaldo versionable + fuente para agentes/CI.
- AppFlowy = espacio operativo humano diario (post-piloto).
- Notion = canon actual hasta cutover; luego archivo/read-only.

No migrar a AppFlowy lo que aún no está inventariado y clasificado.

## 9. Riesgos

| Nivel | Riesgo |
|-------|--------|
| Crítico | Subir material Valent/LLA a org Nortiqa |
| Alto | Declarar mirror Git como “oficial” sin Gio |
| Alto | Duplicar Manifiesto/Prompt y versionar el wrong one |
| Medio | Repos planeados inexistentes → presión a meter todo en `.github` |
| Medio | Gen4 solo en VPS → pérdida ante wipe |
| Bajo | Ruido DOC-CENT (tandas) saturando inventario |

## 10. Próximo paso (uno)

Gio autoriza **Fase A**: export Notion (Markdown+CSV) del árbol Nortiqa Lab + confirma exclusiones de entidad; Claude emite dictamen de alcance P0.
