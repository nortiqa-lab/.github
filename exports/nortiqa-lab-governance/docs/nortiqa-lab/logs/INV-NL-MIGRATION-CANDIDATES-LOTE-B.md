# INV-NL-MIGRATION-CANDIDATES — Lote B (Nortiqa Lab)

**Fecha:** 2026-08-02  
**Estado:** DEV inventario — no migrar hasta cerrar Lot A bloqueados + OK Gio  
**Regla:** PROD/ratificados primero; DEV solo si Gio pide mirror explícito

| Código | URL Notion | Estado aparente | Destino | Acción |
|--------|------------|-----------------|---------|--------|
| DICT-NL-KNOW-001-CLAUDE | https://app.notion.com/p/357e4fe3bfea817c9c26dddfdbf81fbc | Aprobada c/ajustes | dictamenes/ | **Mirror seed hecho** (Lot A.2) |
| DICT-NL-KNOW-002-CLAUDE | https://app.notion.com/p/357e4fe3bfea8129b36eddfc1a1955bd | Dictamen ampliación | dictamenes/ | Pendiente mirror |
| DICT-NL-AGENTES-OPCIONES-001 | https://app.notion.com/p/394e4fe3bfea81ce8b19e5842280ccbb | Opciones (ratif por ítem) | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-SERVIDOROPS-001-CLAUDE | https://app.notion.com/p/382e4fe3bfea81409970c05af02cfeab | Aprob. condicional | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-MEDICION-TOKENS-OBLIGATORIA-001 | https://app.notion.com/p/39be4fe3bfea812c9dfae6fb07690ecb | Pendiente ratif Gio | dictamenes/ | Mirror con disclaimer |
| DICT-NL-QUERYOS-001..007 | varias Centro Madre | Familia Query OS | dictamenes/ | Lote C (paquete) |
| DICT-NL-AUD-UPDT-001/002 | Centro Madre | Familia auditoría | dictamenes/ | Lote C |
| DICT-NL-IDENTITY-001-RATIF | https://app.notion.com/p/391e4fe3bfea812a8e7bc9606d65e119 | Ratificación Identity | dictamenes/ | Pendiente |
| DICT-NL-HOME-AUDIT-20260711-001 | https://app.notion.com/p/39ae4fe3bfea815e912ed1f0ac128352 | Auditoría Home | auditorias/ | Pendiente |
| NDA-NL-001 / PRIV / TOS | legales Notion | Legal | → Drive preferido | No Git salvo Gio |
| CAP-NL-001 | Cap table | Sensible | → Drive | **No migrar a Git público/org profile** |
| GOV-NL-DOCUMENTACION-CANONICA-001 | DEV | DEV | — | No migrar aún |
| GOV-NL-GESTION-CONTEXTO-001 | DEV | DEV | — | No migrar aún |

## Multi-entidad (requiere OK Gio explícito)

| Código | Motivo |
|--------|--------|
| DICT-NL-ERP-ODOO-001 | Nortiqa + LLA Santa Cruz en el mismo dictamen |
| Contenido `valent-capital/` / `lla-santa-cruz/` | Carpetas peer vacías a propósito |

## No migrar

- Páginas `🟡 DEV — …` sin ratificación
- Duplicados de BD KNOW (ver INC-NL-KNOW-001)
- Secretos, tokens, NDA full text a Git org profile
