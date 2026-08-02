Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Fecha: 2026-08-02  
Actor: Cursor / `NL-ORCH` prep (no ejecuta migración)  
Base existente Notion:  
- [PLAN-NL-AF-MIG-001](https://app.notion.com/p/39fe4fe3bfea81718305f6fc12501256) (DEV, pendiente DICT)  
- [TAREA-NL-ORDEN-APPFLOWY-001](https://app.notion.com/p/39fe4fe3bfea8192a778c80e5bd33358) (estructura pendiente)  
- [INT-N8N-APPFLOWY-BRIDGE-001](https://app.notion.com/p/398e4fe3bfea813b84bffe9558b95dc1) (bridge tareas, ratificado)  
Complemento: `AUDIT-NOTION-GIT-NORMALIZATION-001.md`

---

# Prep de migración Notion → AppFlowy (Nortiqa Lab)

## 1. Postura

**No se migra por volumen.** Se migra capacidad operativa, con:

1. Inventario + aislamiento de entidad (auditoría Git/Notion).  
2. Estructura AppFlowy definida (`TAREA-NL-ORDEN-APPFLOWY-001`).  
3. Piloto técnico (3 docs no críticos) antes de LOTE-001.  
4. Git como espejo versionable en paralelo (P0 canon).  
5. Notion en convivencia controlada hasta cutover.

Este documento **no autoriza** escritura masiva en AppFlowy ni cutover.

## 2. Decisiones previas (checklist Gio)

Tomadas de PLAN-NL-AF-MIG-001 §15 — siguen pendientes salvo evidencia contraria:

- [ ] Relación formal Nortiqa ↔ Sur Lancer aplicable a la migración  
- [ ] AppFlowy = espacio operativo principal (sí/no/parcial)  
- [ ] Fecha de corte para **nuevos** docs en Notion  
- [ ] Duración de convivencia Notion + AppFlowy  
- [ ] Responsables admin AppFlowy + validación documental  
- [ ] 3 procesos “día 1” que deben vivir en AppFlowy  
- [ ] Autorizar piloto de 3 documentos  

**Hard stop de entidad:** no migrar Valent / ERP Gio+Edson / LLA / clientes / personal sin autorización escrita.

## 3. Arquitectura objetivo (recomendación)

```text
                    ┌─────────────────────┐
                    │  Git (canon mirror) │  agentes, CI, backup texto
                    └──────────┬──────────┘
                               │ export/PR
┌──────────────┐      ┌────────▼────────┐      ┌──────────────────┐
│ Notion       │─────►│ Staging import  │─────►│ AppFlowy Cloud   │
│ (canon hoy)  │ MD+CSV│ + limpieza     │      │ (ops diario)     │
└──────────────┘      └────────┬────────┘      └────────┬─────────┘
                               │                        │
                               │                   n8n bridge
                               │                   (tareas)
                               ▼                        ▼
                        Inventario CSV              Postgres/Notion sync
                        (trazabilidad)              (INT existente)
```

- **Fuente de verdad durante transición:** Notion hasta cutover; AppFlowy en “operación piloto”.  
- **Tras cutover:** AppFlowy ops + Git mirror; Notion read-only/archivo.  
- **Secretos:** nunca en AppFlowy ni Git (solo refs a `.env` / BWS).

## 4. Capacidad técnica de import (hechos externos + riesgos)

| Contenido | Import AppFlowy | Acción Nortiqa |
|-----------|-----------------|----------------|
| Páginas MD, headings, listas, code | Bueno | Export Notion MD |
| Tablas simples | Parcial | Revisar post-import |
| Databases / relations / formulas / rollups | Malo / rebuild | CSV + recrear schema |
| Imágenes / archivos | Frágil | Re-adjuntar o object storage |
| Comentarios / activity | No | Descartar o archivar Notion |
| Self-host MinIO presign | Riesgo conocido | Configurar `APPFLOWY_S3_PRESIGNED_URL_ENDPOINT` |

**Inferencia:** el Centro Madre y DB-NL-KNOW no se “importan enteros”; se reconstruyen por lotes.

## 5. Prep técnico (antes del piloto)

### 5.1 Backup

```bash
# En estación Gio (Notion UI):
# Settings → Export all workspace content → Markdown & CSV → include subpages
# Guardar ZIP íntegro sin modificar: backups/notion-export-YYYYMMDDZ.zip
sha256sum backups/notion-export-*.zip | tee backups/notion-export.sha256
```

### 5.2 Inventario

- Generar CSV de auditoría (§7 de AUDIT-NOTION-GIT…).  
- Filtrar `entity=NL` y `action∈{migrate,summarize,rewrite}`.  
- Congelar lista del piloto (3 docs) + LOTE-001.

### 5.3 AppFlowy Cloud (self-host o hosted)

Verificar (evidencia pendiente en esta sesión — marcar PENDIENTE DE VALIDACIÓN):

- [ ] Instancia alcanzable (URL)  
- [ ] Auth / usuarios Gio + operadores  
- [ ] Backup de workspace AppFlowy  
- [ ] Import Notion ZIP o MD funciona en **esa** instancia  
- [ ] Límite upload nginx / S3 presign OK  
- [ ] Bridge n8n `POST /webhook/appflowy/create-task` health (sin imprimir token)

### 5.4 Bridge existente

`INT-N8N-APPFLOWY-BRIDGE-001` ya define sync **AppFlowy → tareas**.  
Para migración documental: **no** usar ese webhook; usar import manual/API de páginas.  
OpenAPI en VPS: `/home/deploy/sc2027-staging/docs/appflowy-chatgpt-action-openapi.yaml` → versionar a Git (P1).

## 6. Estructura AppFlowy (cerrar TAREA-NL-ORDEN-APPFLOWY-001)

PLAN propone 00–99. Prep mínima antes de crear páginas reales:

| Nodo | Contenido inicial | Notas |
|------|-------------------|-------|
| 00 Inicio | Home + links MEM mirror | Solo NL |
| 03 Gobernanza | Manifiesto, PAO, Índice Reglas | Protegido lectura |
| 09 Tecnología | Links a Git repos + runbooks | Sin secretos |
| 10 Decisiones | ADR index | |
| 90 Migración en curso | Inventario + lotes | |
| 99 Archivo | Históricos | |

**Entregable faltante:** SOP-NL-ORDEN-APPFLOWY-001 + diagrama (tarea Notion asignada a Codex; ratificación Gio pendiente).

## 7. Secuencia autorizable (post-dictamen)

```text
0. DICT-NL-AF-MIG-001 (Claude) + ratificación Gio
1. Completar TAREA-NL-ORDEN-APPFLOWY-001
2. Backup Notion + inventario CSV en Git (draft)
3. Piloto técnico: 3 docs no críticos → AppFlowy
4. Tests: formato, links, rollback, aislamiento entidad
5. LOTE-001 (15 docs integración) — solo si piloto OK
6. En paralelo G1–G2 mirrors Git (canon P0)
7. Fases 2–7 del PLAN-NL-AF-MIG-001 por demanda
8. Cutover: Notion read-only; AppFlowy ops; Git sync continuo
```

## 8. Piloto técnico propuesto (3 docs)

Elegir **no estratégicos** y 100% Nortiqa:

1. Un runbook ya en Git (`ops-public-health`) reimportado como prueba de round-trip.  
2. Una página DEV no madre (ej. GEN4 closeout o handoff).  
3. Una página corta de índice/link (sin DB).

**Éxito piloto:**

- Jerarquía correcta  
- Sin secretos  
- Rollback documentado  
- Tiempo de import medido  
- Diff humano “aceptable”

## 9. LOTE-001 (no ejecutar aún)

Mantener lista de PLAN-NL-AF-MIG-001 §7 (carta integración, misión/visión, RACI, etc.).  
**Condición:** Sur Lancer scope confirmado por Gio; si el scope se reduce a “solo Nortiqa Lab”, reescribir LOTE-001 sin piezas de integración comercial.

## 10. Trazabilidad mínima por documento migrado

| Campo | Ejemplo |
|-------|---------|
| notion_url | https://app.notion.com/p/… |
| export_path | notion-export/…/Manifiesto.md |
| appflowy_path | 03-Gobernanza/Manifiesto |
| git_path | docs/canon/MANIFIESTO.md |
| action | migrate / summarize / … |
| migrated_at | ISO UTC |
| verified_by | Gio / Claude |

## 11. Qué falta subir a Git **para** la migración (cruce auditoría)

Prioridad migración-enabler:

1. Inventario CSV + esta prep + AUDIT (este PR).  
2. Canon P0 (Manifiesto, Índice, PAO, Prompt, MEM mirror).  
3. PLAN-NL-AF-MIG-001 + TAREA-ORDEN mirror (ya existen en Notion; versionar DEV).  
4. INT bridge OpenAPI (desde VPS).  
5. Crear repos `infra` / `n8n-workflows` si se va a exportar workflows reales.

## 12. Riesgos específicos AppFlowy

| Riesgo | Mitigación |
|--------|------------|
| Replicar desorden Notion | Inventario + estados; lotes pequeños |
| Doble fuente de verdad | Cutover date + Notion freeze |
| Self-host import roto (MinIO) | Probar piloto en la instancia real primero |
| Mezcla Sur Lancer / Valent | Filtro entity en CSV |
| Bridge escribe Notion sin querer | No usar webhook para migración documental |

## 13. Solicitud a ARCHITECT-001

Emitir **DICT-NL-AF-MIG-001** respondiendo las 15 preguntas de PLAN-NL-AF-MIG-001 §14, más:

16. ¿Git mirror P0 es condición previa al piloto AppFlowy?  
17. ¿Sur Lancer entra en LOTE-001 o se aplaza?  
18. ¿AppFlowy self-host en SC2027 vs hosted — decisión de infra?

## 14. Próximo paso (uno)

Gio responde el checklist §2 (aunque sea “piloto solo Nortiqa, Sur Lancer fuera”) y autoriza a Claude el dictamen DICT-NL-AF-MIG-001; en paralelo se completa el export Notion + inventario CSV (Fase A de la auditoría Git).
