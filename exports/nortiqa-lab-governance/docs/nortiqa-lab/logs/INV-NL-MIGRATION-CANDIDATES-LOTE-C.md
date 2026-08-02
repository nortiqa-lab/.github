# INV-NL-MIGRATION-CANDIDATES — Lote C (cierre gaps Lot A + LLA/Valent)

**Fecha:** 2026-08-02  
**Estado:** DEV inventario — Fase 0.3  
**Regla:** solo migrar ratificados/PROD; no masivo sin Gio

## Gaps Lot A — resultado de búsqueda Notion (2026-08-02)

| Código pedido | Hallazgo | Acción |
|---|---|---|
| DICT-NL-VISION-FUSION-001 | Ratificado vía LOG; página DICT no indexada | Stub + mirror LOG hechos |
| DICT-NL-GOBERNANZA-ALMACENAMIENTO-001 | Stub DEV Notion + seed | Esperar texto canónico Gio |
| GOV-NL-ORG-001 | Solo referencias; página no indexada | **Bloqueado** — pedir URL Gio |
| REGLA-DEV-DICTAMEN-CLAUDE-001 | No encontrada | **Bloqueado** — pedir URL o confirmar deprecada |
| DICT-NL-LAPTOP-COMPRA-001 | No existe con ese código. Existe `PLAN-NL-HW-PORTATIL-001` (DEV) | No migrar (DEV). Renombrar/emitir DICT si Gio quiere |
| DICT-NL-AUDIT-GDRIVE-GIO-001 | No existe. Relacionados DEV: PLAN-GIO-DRIVE-PC-001, PLAN-PERSONAL-DRIVE-HP-001 | No migrar (DEV) |

## LLA Santa Cruz

| Código | Hallazgo | Acción |
|---|---|---|
| LLA-SANTA-CRUZ-SITE-AUDITORIA-20260802 | No en Notion ni en este repo | Pedir path `.md` fuente a Gio |
| ESTANDAR-ORG-LLA-SC-001 | Aprobado (visual organigramas) | Inventariar para lote LLA post-repo privado — **no copiar cuerpo aquí** |

## Valent Capital

Sin inventario Gio de docs ratificados → carpeta vacía. No migrar.

## SC2027

| Nota | Fuente |
|---|---|
| Listado de entidades separadas en LOG-NL-SESION incluye **SC2027** como peer | LOG 2026-07-09 |
| Kit Cursor aún describe SC2027 como host VPS | `AGENTS.md` / rules |
| Discrepancia documentada — Gio aclara si carpeta = entidad peer o solo ops | Pregunta abierta |

## PLAN-SC2027-PLATAFORMA-TRABAJO-MVP-001

Sigue **DEV/Borrador** → no migrar.

## Redirects Notion

Plantillas listas. **No aplicadas** sin autorización Gio + PAO/OT.
