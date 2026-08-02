# Inventario de migración — lote 1

Estado: DEV / Borrador  
Fecha: 2026-08-02  
Fuente: prompt KNOW-001 ajustado + búsqueda Notion MCP

No es documentación oficial. Requiere auditoría Claude / ratificación Gio.

## Convención de columnas

- **Estado Notion:** evidenciado en título/metadata al buscar
- **Acción:** `migrar` | `esperar` | `preguntar Gio` | `stub`

## Nortiqa Lab → `docs/nortiqa-lab/`

| Código | Destino | Estado Notion (evidencia) | Acción |
|---|---|---|---|
| DICT-NL-GOBERNANZA-ALMACENAMIENTO-001 | dictamenes/ | **No encontrado** como página (2026-08-02) | stub DEV + pedir URL a Gio |
| DICT-NL-NORMA-AGENTES-001 | dictamenes/ | Existe `DICT-NL-NORMA-AGENTES-001-CLAUDE` | migrar cuando repo privado exista |
| DICT-NL-VISION-FUSION-001 | dictamenes/ | Referenciado; ejecución DEV separada | verificar página PROD antes de migrar |
| DICT-NL-GITHUB-001 | dictamenes/ | EMITIDO — Aprobado por Gio | migrar (canónico) |
| DICT-NL-LAPTOP-COMPRA-001 | dictamenes/ | No confirmado en búsqueda rápida | preguntar / inventariar KNOW-001 |
| DICT-NL-AUDIT-GDRIVE-GIO-001 | dictamenes/ | No confirmado en búsqueda rápida | preguntar / inventariar KNOW-001 |
| REGLA-NL-VERACIDAD-TOTAL-001 | governance/ | ✅ página encontrada | migrar |
| REGLA-NL-ESCALADA-TEMATICA-001 | governance/ | ✅ página encontrada | migrar |
| REGLA-DEV-DICTAMEN-CLAUDE-001 | governance/ | No confirmado en búsqueda rápida | preguntar / inventariar |
| GOV-NL-ORG-001 | governance/ | Referenciado ampliamente; página canónica a confirmar | preguntar / inventariar |

## Prefijos ambiguos → Gio

| Código | Motivo |
|---|---|
| DICT-KAGE-ITACHI-001 | Sin prefijo de entidad claro |
| LOG-NL-VALENT-EVO-001 | Prefijo NL + nombre Valent |

## SC2027 → `docs/sc2027/`

| Código | Destino | Estado Notion | Acción |
|---|---|---|---|
| PLAN-SC2027-PLATAFORMA-TRABAJO-MVP-001 | planes/ | 🟡 DEV / Borrador | **esperar** (no es PROD) |

## LLA Santa Cruz → `docs/lla-santa-cruz/`

| Código | Destino | Estado | Acción |
|---|---|---|---|
| LLA-SANTA-CRUZ-SITE-AUDITORIA-20260802 | auditorias/ | No hallado en Notion ni en `nortiqa-lab/.github` | preguntar path fuente a Gio |

## Valent Capital → `docs/valent-capital/`

Inventario de docs **ratificados** pendiente (KNOW-001). No migrar cuerpos a este org-profile.

## Transversal → `docs/transversal/`

Ninguno confirmado en lote 1.

## Redirects Notion

**Bloqueado** hasta autorización Gio + PAO/OT. Plantilla lista en `templates/notion-redirect.md`.

## Preguntas abiertas a Gio

1. URL/texto de DICT-NL-GOBERNANZA-ALMACENAMIENTO-001
2. Confirmación supersesión parcial vs PLAN-NL-GITHUB-001 (solo docs PROD)
3. Ubicación DICT-KAGE-ITACHI-001 y LOG-NL-VALENT-EVO-001
4. ¿SC2027 carpeta operativa o entidad peer?
5. Path de LLA-SANTA-CRUZ-SITE-AUDITORIA-20260802.md
6. Autorización writes redirect Centro Doc Madre
7. Crear repo `nortiqa-lab/governance` (bot sin `createRepository`)
