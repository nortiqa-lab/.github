# Protocolo de despacho — Equipo Nortiqa

## 1. Entrada

Gio (o un agente autorizado) entrega:

- Objetivo en una frase.
- Repo / superficie afectada.
- Restricciones (no tocar VPS, no Notion, deadline blando, etc.).
- Evidencia previa (links, handoffs, PRs).

## 2. Clasificación (`NL-ORCH`)

| Clase | Ejemplo | Roles típicos |
|-------|---------|---------------|
| A — Lectura / síntesis | Mapear estado, resumir canon | ORCH + MEMORY (± AUDITOR) |
| B — Draft local | Propuesta, checklist, mock | BUILDER o PRODUCT + MEMORY |
| C — Cambio versionable | PR en GitHub | BUILDER (± PRODUCT) + ORCH |
| D — Pieza protegida / Notion | Dictamen, PAO, root | AUDITOR only + autorización Gio |
| E — VPS / staging / prod | Healthcheck, login portal, promote | OPS + ORCH (± AUDITOR gate) |

Si la clase no está clara → preguntar a Gio una sola pregunta de desambiguación, no inventar.

## 3. Asignación

- Máximo paralelismo útil: **3 agentes** activos salvo pedido explícito.
- No lanzar `NL-OPS` en paralelo con cambios de prod no relacionados.
- No lanzar `NL-AUDITOR` para “arreglar código”; su rol es gate y dictamen.
- Si aparece contexto Valent/ERP/cliente → **stop** y escalar a Gio.

## 4. Contrato de salida por agente

Cada agente debe devolver:

1. Rol + código (`NL-*`).
2. Canon leído (o “Notion unavailable → bootstrap”).
3. Cambios hechos (paths / URLs).
4. Verificación (comandos + resultado).
5. Bloqueos.
6. Próximo paso seguro (una línea).

Usar la plantilla de handoff del paquete de memoria cuando exista en el repo de trabajo:
`docs/shared-ai-memory/handoff-template.md`.

Copia local de emergencia: [`.drafts/HANDOFF_TEMPLATE.md`](../.drafts/HANDOFF_TEMPLATE.md).

## 5. Consola final (`NL-ORCH`)

Un solo resumen para Gio:

- Objetivo.
- Agentes usados.
- Merge de hechos verificados.
- Riesgos residuales.
- Bloqueos que requieren humano (sudo, snapshot Hetzner, PAO, secretos).
- Siguiente acción recomendada **una sola**.

## 6. Gates que detienen al equipo

- Notion canon conflictivo o root faltante.
- Pedido de mezclar entidades.
- Escritura a prod sin snapshot / healthcheck.
- Pedido de editar documento madre sin OT/PAO.
- Credenciales o tokens en claro en el request.
