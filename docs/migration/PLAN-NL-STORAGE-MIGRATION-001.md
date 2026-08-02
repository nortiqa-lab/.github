# PLAN-NL-STORAGE-MIGRATION-001 — Migración híbrida de almacenamiento (DEV)

**Estado:** DEV / Borrador operativo  
**Fecha:** 2026-08-02  
**Entidad:** Nortiqa Lab (lotes Valent/LLA solo con inventario previo + OK Gio)  
**No borra Notion** hasta redirect autorizado.

## Matriz destino (ratificada + híbrido operativo)

| Tipo | Destino | Notas |
|------|---------|-------|
| Docs PROD / dictámenes / reglas | Git → repo privado `nortiqa-lab/governance` | Seed local: `exports/nortiqa-lab-governance/` |
| Definiciones de agentes (prompts/tools) | Git (`.github/agents` / product repo) | Versionable |
| Inventario operativo + tareas runtime | PostgreSQL sc2027 | Seed: `exports/sql/` — **no aplicar a PROD sin Gio** |
| Gobernanza viva / ratificación / DEV | Notion | Redirects cuando Gio autorice |
| Entregables externos | Google Drive `90_COMPARTIR/POR_ENTIDAD/` | Fuera de este lote |

Fuentes: `TAREA-NL-GOBERNANZA-ALMACENAMIENTO-001`, `REG-NL-SESSION-20260619-001`, conversación Gio 2026-08-02.

## Fases

### Fase 0 — Seed (ESTA ENTREGA)
1. Estructura `exports/nortiqa-lab-governance/`
2. Inventario de candidatos Lot A (Nortiqa)
3. Exportar 1–2 reglas/dictámenes ya ratificados como mirror Git
4. Schema SQL `nl_agentes_inventario` + `nl_tareas` + seed de agentes lab
5. Plantilla redirect Notion
6. **No** crear repo remoto si falta permiso; **no** borrar Notion; **no** migrar Valent content

### Fase 1 — Gio crea `nortiqa-lab/governance` + branch protection
Aplicar seed vía `exports/nortiqa-lab-governance/APPLY.md`.

### Fase 2 — Lotes documentales progresivos
Solo PROD/ratificados. PR por lote.

### Fase 3 — SQL en staging VPS
Correr migraciones en `sc2027-staging-db` (OPS privilegiado). Validar QueryOS/Metabase.

### Fase 4 — Redirects Notion
Vaciar+redirect páginas ya canónicas en Git (Gio + PAO/OT). **Nunca delete-first.**

### Fase 5 — Depurar Notion
Eliminar solo duplicados confirmados post-redirect + auditoría Claude.

## Bloqueos abiertos a Gio
1. URL/texto `DICT-NL-GOBERNANZA-ALMACENAMIENTO-001`
2. Crear repo `nortiqa-lab/governance` (privado)
3. Autorizar redirects en Centro Doc Madre
4. Aplicar SQL en staging (credenciales/OPS)
5. Ubicación docs ambiguos (KAGE/ITACHI, LOG-NL-VALENT-EVO)

## Regla anti-mezcla
Nunca copiar contenido Valent / LLA / cliente a carpetas Nortiqa. Carpetas peer existen vacías hasta inventario+OK.
