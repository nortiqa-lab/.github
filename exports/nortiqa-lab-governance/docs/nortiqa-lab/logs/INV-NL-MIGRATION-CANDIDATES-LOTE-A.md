# INV-NL-MIGRATION-CANDIDATES — Lote A (Nortiqa Lab)

**Fecha:** 2026-08-02  
**Estado:** DEV inventario — no implica migración masiva  
**Regla:** solo migrar ratificados/PROD o referenciados activamente

| Código | URL Notion | Estado aparente | Carpeta destino | Acción lote |
|--------|------------|-----------------|-----------------|-------------|
| DICT-NL-NORMA-AGENTES-001-CLAUDE | https://app.notion.com/p/3a0e4fe3bfea810385a5f889fcd1b134 | DICTAMEN formal | dictamenes/ | **Mirror seed hecho** |
| REGLA-NL-VERACIDAD-TOTAL-001 | https://app.notion.com/p/39ae4fe3bfea815c9b59cd007026d075 | Regla (ratif Gio pendiente en doc) | governance/ | **Mirror seed hecho** |
| DICT-NL-GOBERNANZA-ALMACENAMIENTO-001 | — | **No encontrado en Notion** | dictamenes/ | Bloqueado — pedir URL a Gio |
| DICT-NL-VISION-FUSION-001 | (vía DEV-NL-VISION-FUSION-001) | Ratificado 09-07; página DICT canónica a confirmar | dictamenes/ | Inventariar URL exacta |
| GOV-NL-ORG-001 | buscar | ? | governance/ | Confirmar URL + estado |
| REGLA-DEV-DICTAMEN-CLAUDE-001 | buscar | ? | governance/ | Confirmar |
| REGLA-NL-ESCALADA-TEMATICA-001 | buscar | ? | governance/ | Confirmar |
| DICT-NL-LAPTOP-COMPRA-001 | buscar | ? | dictamenes/ | Verificar existencia |
| DICT-NL-AUDIT-GDRIVE-GIO-001 | buscar | ? | dictamenes/ | Verificar existencia |
| OT-NL-DMAIC-001 cierre | https://app.notion.com/p/352e4fe3bfea8175b08af2fc075742ad | Cerrada AJUSTAR | logs/ o planes/ | Mirror opcional post-audit |
| ÍNDICE-NL-AGENTES-PROYECTOS-001 | https://app.notion.com/p/393e4fe3bfea814bb842f0ad4980469e | Operativo (Notion) | → **SQL inventory** no Git largo plazo | Seed SQL aparte |
| MEM-NL-ROOT-001 | https://app.notion.com/p/382e4fe3bfea818aacfad4f9793a697f | Canon entry | **permanece Notion** | No migrar (índice vivo) |

## Bloqueados (ambigüedad entidad)

| Código | Motivo |
|--------|--------|
| DICT-KAGE-ITACHI-001 | Sin prefijo de entidad |
| LOG-NL-VALENT-EVO-001 | Prefijo NL + nombre Valent |

## No migrar aún

- Páginas DEV/Borrador (`🟡 DEV — …`)
- PLAN-SC2027-PLATAFORMA-TRABAJO-MVP-001 (DEV)
- Contenido Valent / LLA sin inventario Gio
