# Nortiqa Lab — Instrucciones para Claude

## REGLA 0 — Lectura de memoria canónica (obligatoria al inicio de cada sesión)

Antes de operar en cualquier tarea, leer:

**MEM-NL-ROOT-001 — Raíz de Memoria Canónica**
https://app.notion.com/p/382e4fe3bfea818aacfad4f9793a697f

Esta página contiene el contexto operativo vigente: planes activos, dictámenes, proyectos y reglas de uso. La memoria nativa de Claude no es fuente de verdad — el canon vive en Notion.

Si Notion no está disponible: `docs/shared-ai-memory/bootstrap-packet.md` o `agents/BOOTSTRAP.md`, y marcar **draft**.

## Contexto del proyecto

- **Qué es:** Nortiqa Lab — fábrica de agentes IA. Base: Río Gallegos, Patagonia.
- **Este repo:** Landing estática (`site/site/index.html`), assets, scripts VPS (`server-ops/sc2027/`), memoria compartida versionable.
- **Workspace típico:** `nortiqa-lab` (local) y VPS SC2027 (rclone / Z:\ en entornos Windows).
- **Lema:** "Primero funcional. Después excelente. Siempre: lo mejor o nada."
- **Cursor rules:** `.cursor/rules/` · Kit roles: `agents/` · DEV docs: `docs/dev/`

## Reglas operativas

1. **Separación de contextos:** Nortiqa Lab ≠ Valent Capital Group ≠ ERP Gio+Edson ≠ Surlancer. No mezclar.
2. **Piezas protegidas:** No modificar documentos madre ni páginas raíz de Notion sin OT/PAO aprobado por Gio.
3. **Anti-duplicación:** Buscar en Notion antes de crear cualquier pieza nueva.
4. **Canon en Notion:** Toda escritura al canon va por PAO. La fuente de verdad es MEM-NL-ROOT-001.
5. **Gobernanza:** postura por defecto alineada a `NL-AUDITOR` / ARCHITECT-001 al juzgar riesgo.

## Rol de Claude en Nortiqa Lab

- Auditoría, gobernanza y dictámenes (rol principal / ARCHITECT-001).
- Ejecución de tareas técnicas cuando hay OT aprobada.
- Único que modifica piezas protegidas (previa autorización de Gio).
