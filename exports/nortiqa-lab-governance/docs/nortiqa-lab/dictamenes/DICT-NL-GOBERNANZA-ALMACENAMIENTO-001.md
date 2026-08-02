# DICT-NL-GOBERNANZA-ALMACENAMIENTO-001

**Estado:** DEV / Borrador (stub) — **NO OFICIAL**  
**Fecha stub:** 2026-08-02  
**Emisor stub:** Cursor / NL-BUILDER  
**Bloqueo:** página Notion canónica **no encontrada** (MCP search). Captura matriz operativa comunicada por Gio.

> También existía `DRAFT-DICT-NL-GOBERNANZA-ALMACENAMIENTO-001.md` (mismo contenido). Este archivo es el nombre canónico del stub.

## Objeto

Política de almacenamiento documental multi-entidad:

- Nortiqa Lab
- Valent Capital Group S.A.
- SC2027 (carpeta operativa / host)
- LLA Santa Cruz

## Matriz (instrucción Gio 2026-08-02)

| Tipo | Destino |
|------|---------|
| Docs ratificados (PROD) | GitHub — `nortiqa-lab/governance` → `docs/[entidad]/[tipo]/` |
| DEV / tareas con estado | AppFlowy / Notion |
| Externos + financieros/legales | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |
| Inventario agentes / tareas runtime | PostgreSQL sc2027 (ver `exports/sql/` en `.github`) |

## Diagrama

```text
¿Ratificado (PROD)?
├── SÍ → GitHub docs/[entidad]/[tipo]/
└── NO → ¿Tarea con estados?
    ├── SÍ → AppFlowy/Notion DB
    └── NO → ¿Externo?
        ├── SÍ → Google Drive
        └── NO → AppFlowy/Notion página
```

## Relación con PLAN-NL-GITHUB-001

Supersede **solo** docs PROD (un repo governance con carpetas). Código/datos/secretos siguen en repos por entidad.

## Pendiente stub → dictamen

- [ ] Texto/URL canónico Gio
- [ ] Dictamen Claude
- [ ] Ratificación Gio
- [ ] Apply a repo `governance`

## Referencias

- https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558  
- DICT-NL-GITHUB-001
