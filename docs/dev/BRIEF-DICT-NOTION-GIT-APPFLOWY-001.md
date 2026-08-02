Estado: DEV / Borrador

No es documentación oficial. No sustituye un dictamen de Claude.
Requiere que ARCHITECT-001 emita DICT y Gio ratifique.

Fecha: 2026-08-02  
Para: Claude / ARCHITECT-001  
De: Cursor / NL-ORCH (prep)  
Adjuntos locales:  
- `AUDIT-NOTION-GIT-NORMALIZATION-001.md`  
- `PLAN-APPFLOWY-MIGRATION-PREP-001.md`  
- `inventories/notion-git-gap-inventory-2026-08-02.csv`  
- `inventories/INVENTORY-SUMMARY-2026-08-02.md`  
Canon Notion: MEM-NL-ROOT-001, Centro Madre, PLAN-NL-AF-MIG-001, TAREA-NL-GOBERNANZA-ALMACENAMIENTO-001

---

# Brief para dictámenes — Notion → Git + AppFlowy

## Pedido

Emitir **dos** dictámenes (o uno combinado con secciones), ambos en DEV hasta ratificación Gio:

### A) `DICT-NL-NOTION-GIT-001` — Alcance de normalización Git

Preguntas obligatorias:

1. ¿El destino PROD docs = `nortiqa-lab/governance` (matriz almacenamiento) es compatible con `PLAN-NL-GITHUB-001` / `DICT-NL-GITHUB-001`? ¿Confirma supersesión **solo** para documentación PROD?
2. ¿Aprueba el lote P0 del inventario (Manifiesto, PAO, Prompt, Índice Reglas, MEM mirror, checklist)?
3. ¿Cómo resolver duplicados Manifiesto×2 y Prompt×2 (cuál es canónico)?
4. ¿Los repos `infra` / `n8n-workflows` / `queryos` siguen siendo P0 o se difieren?
5. ¿Gen4 (ADR-040, L3, botctl) va a `governance/docs/sc2027` o a product/`infra`?
6. ¿Qué hacer con los ~30 ambiguos DOC-CENT y el folder DEV (~90+)?
7. Resultado: ✅ / ⚠️ condicional / ❌ — con lista exacta autorizada a versionar.

### B) `DICT-NL-AF-MIG-001` — Migración AppFlowy

Responder las 15 preguntas de [PLAN-NL-AF-MIG-001](https://app.notion.com/p/39fe4fe3bfea81718305f6fc12501256) §14, más:

16. ¿Git mirror P0 es **condición previa** al piloto AppFlowy?  
17. ¿Sur Lancer entra en LOTE-001 o se aplaza (entity isolation)?  
18. ¿Self-host AppFlowy en SC2027 vs hosted — requisito de dictamen de infra?  
19. ¿La `TAREA-NL-ORDEN-APPFLOWY-001` debe cerrarse antes del piloto?  
20. Relación con bridge `INT-N8N-APPFLOWY-BRIDGE-001` (no usar webhook para migración documental).

## Hechos verificados (no inventar en contra)

- Notion MCP operativo; MEM-NL-ROOT leído.  
- Org GitHub: solo `.github` + `github.io`. Product thin en `giovanyalbea-dotcom/nortiqa-lab`.  
- `governance` / `infra` / `n8n-workflows` / `queryos`: **ausentes**.  
- Inventario seed: 83 filas; P0=14; EXCLUDE=13; in_git yes≈2.  
- `DICT-NL-GOBERNANZA-ALMACENAMIENTO-001` **no encontrado** como página; solo la TAREA DEV.  
- PLAN-NL-AF-MIG-001 sigue DEV sin dictamen.  
- Contaminación observada: Valent / LLA / Surlancer / personal en árbol Nortiqa.

## Restricciones al dictaminar

- No autorizar escritura masiva Notion/AppFlowy.  
- No mezclar secretos.  
- No declarar PROD.  
- Preferir lotes reversibles (G1 canon → piloto AF 3 docs).

## Formato de salida sugerido

```text
DICT ID:
Resultado: ✅ / ⚠️ / ❌
Hallazgos críticos:
Condiciones:
Alcance autorizado (lista IDs Notion + path Git):
Bloqueos para Gio:
Próximo paso único:
```

## Próximo paso humano tras dictamen

Gio ratifica → crear `nortiqa-lab/governance` → PR lote G1 (P0) → piloto AppFlowy 3 docs.
