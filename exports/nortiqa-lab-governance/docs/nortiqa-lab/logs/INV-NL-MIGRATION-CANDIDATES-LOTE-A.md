# INV-NL-MIGRATION-CANDIDATES — Lote A (Nortiqa Lab)

**Fecha:** 2026-08-02  
**Estado:** DEV inventario — no implica migración masiva  
**Regla:** solo migrar ratificados/PROD o referenciados activamente

| Código | URL Notion | Estado aparente | Carpeta destino | Acción lote |
|--------|------------|-----------------|-----------------|-------------|
| DICT-NL-NORMA-AGENTES-001-CLAUDE | https://app.notion.com/p/3a0e4fe3bfea810385a5f889fcd1b134 | DICTAMEN formal | dictamenes/ | **Mirror seed hecho** |
| REGLA-NL-VERACIDAD-TOTAL-001 | https://app.notion.com/p/39ae4fe3bfea815c9b59cd007026d075 | Regla (ratif Gio pendiente en doc) | governance/ | **Mirror seed hecho** |
| REGLA-NL-ESCALADA-TEMATICA-001 | (mirror local) | Regla | governance/ | **Mirror seed hecho** |
| DICT-NL-GITHUB-001 | https://app.notion.com/p/380e4fe3bfea8168a074cb86c1aff55a | Aprobado Gio | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-EXEC-GATE-001-CLAUDE | https://app.notion.com/p/391e4fe3bfea81f580dbce348345d979 | VIGENTE (ratif Gio en texto) | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-DOC-CENT-001-CLAUDE | https://app.notion.com/p/391e4fe3bfea81f18431efcd8027f28b | Aprobada | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-KNOW-001-CLAUDE | https://app.notion.com/p/357e4fe3bfea817c9c26dddfdbf81fbc | Aprobada c/ajustes | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-AGENTES-OPCIONES-001 | https://app.notion.com/p/394e4fe3bfea81ce8b19e5842280ccbb | Opciones | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-SERVIDOROPS-001-CLAUDE | https://app.notion.com/p/382e4fe3bfea81409970c05af02cfeab | Aprob. condicional | dictamenes/ | **Mirror seed hecho** |
| DICT-NL-MEDICION-TOKENS-OBLIGATORIA-001 | https://app.notion.com/p/39be4fe3bfea812c9dfae6fb07690ecb | Pendiente ratif Gio | dictamenes/ | Mirror + disclaimer |
| DICT-NL-GOBERNANZA-ALMACENAMIENTO-001 | — | **No encontrado en Notion** | dictamenes/ | Bloqueado — pedir URL a Gio |
| DICT-NL-VISION-FUSION-001 | solo vía DEV/LOG | Ratificado 09-07; página DICT canónica **no encontrada** | dictamenes/ | Bloqueado — pedir URL |
| GOV-NL-ORG-001 | referenciado, página no indexada | Canon base | governance/ | Bloqueado — pedir URL |
| REGLA-DEV-DICTAMEN-CLAUDE-001 | buscar | ? | governance/ | Confirmar |
| DICT-NL-LAPTOP-COMPRA-001 | buscar | ? | dictamenes/ | No encontrado |
| DICT-NL-AUDIT-GDRIVE-GIO-001 | buscar | ? | dictamenes/ | No encontrado |
| OT-NL-DMAIC-001 cierre | https://app.notion.com/p/352e4fe3bfea8175b08af2fc075742ad | Cerrada AJUSTAR | logs/ o planes/ | Mirror opcional post-audit |
| ÍNDICE-NL-AGENTES-PROYECTOS-001 | https://app.notion.com/p/393e4fe3bfea814bb842f0ad4980469e | Operativo (Notion) | → **SQL inventory** | Seed SQL aparte |
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

## Avance 2026-08-02

| Hito | Estado |
|------|--------|
| Fase 0 seed estructura | Hecho |
| Lot A mirrors (10+) | Hecho (resúmenes) |
| Lot B inventario | Hecho — ver `INV-NL-MIGRATION-CANDIDATES-LOTE-B.md` |
| SQL schema+seed | Hecho; validate via `exports/sql/validate_local.py` |
| Pack script para repo remoto | `scripts/pack-for-remote.sh` |
| Repo `nortiqa-lab/governance` | **Bloqueado** — Gio debe crearlo |
| Redirects / deletes Notion | **No** — sin autorización |

**Repo remoto:** creación bloqueada para `cursor[bot]` (Resource not accessible). Gio debe crearlo.


## Avance 2026-08-02 (Fase 0.3)

| Hito | Estado |
|------|--------|
| Consolida PR #15 (apply.sh, gitkeeps, stub DICT almacenamiento) | Hecho en este branch |
| Stubs GOV-NL-ORG / VISION-FUSION | Hecho (sin URL canónica) |
| Mirrors KNOW-002 + IDENTITY-RATIF | Hecho |
| Repo remoto governance | **Aún no existe** |
| PR #15 | Preferir cerrar tras merge #16 (duplicado/conflicto) |
