# Nortiqa Lab — Equipo de Agentes

Status: **draft local / versionable**  
Scope: Nortiqa Lab only  
Canon: Notion `MEM-NL-ROOT-001` (esta carpeta no reemplaza el canon)

## Qué es esto

Paquete operativo para despachar un equipo de IAs con roles claros, límites duros y handoffs obligatorios.

Usar cuando Gio pide trabajo multi-agente, o cuando un orquestador necesita repartir tareas sin mezclar contextos.

## Roster (v0)

| Código | Rol | Job principal | Puede escribir |
|--------|-----|---------------|----------------|
| `NL-ORCH` | Orquestador | Partir trabajo, asignar roles, cerrar handoff | Planes locales, handoffs |
| `NL-AUDITOR` | Gobernanza | Dictámenes, gates PAO/OT, piezas protegidas | Solo con autorización explícita de Gio |
| `NL-BUILDER` | Implementación | Código, sites, scripts, PRs reversibles | Repo / drafts locales |
| `NL-OPS` | Server ops | VPS SC2027, healthchecks, staging→prod | Scripts OPS; prod solo con gate |
| `NL-PRODUCT` | Producto público | Landing, herramientas, UX, copy | Surfaces públicas / drafts |
| `NL-MEMORY` | Memoria compartida | Bootstrap, handoffs, continuidad entre sesiones | Docs de memoria versionables |

Detalle de cada rol: [`roles/`](./roles/).  
Prompts listos para pegar en Cursor Cloud / IDE: [`prompts/`](./prompts/).  
Protocolo de despacho: [`DISPATCH.md`](./DISPATCH.md).

## Reglas del equipo (hard)

1. **Canon first.** Leer `MEM-NL-ROOT-001` si Notion está disponible; si no, bootstrap local y marcar draft.
2. **Aislamiento.** Nortiqa ≠ Valent ≠ ERP Gio+Edson ≠ Surlancer ≠ clientes.
3. **Sin secretos** en chat, Notion ni repo.
4. **Piezas protegidas** solo con autorización de Gio + PAO/OT.
5. **Un rol por sesión** salvo que `NL-ORCH` documente una excepción temporal.
6. **Handoff al cerrar** toda sesión sustancial.

## Cómo despachar (mínimo)

1. Gio da el objetivo.
2. `NL-ORCH` clasifica: lectura / draft local / cambio versionable / cambio protegido / VPS.
3. Se lanza 1 agente por rol necesario con su prompt de `prompts/`.
4. Cada agente deja handoff con la plantilla de memoria compartida.
5. `NL-ORCH` consolida: qué cambió, qué se verificó, qué queda bloqueado, próximo paso seguro.

## Relación con otros repos

- Este repo (`.github`): perfil org + este paquete de equipo.
- Repo de trabajo: `giovanyalbea-dotcom/nortiqa-lab` (`AGENTS.md`, server-ops, site).
- Producción: VPS SC2027 (`nortiqalab.com`).

Este draft debe revisarse contra `AGENTS.md` / `CLAUDE.md` del repo de trabajo antes de promoverse a canon.
