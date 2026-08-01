# Roster v0 — Equipo Nortiqa

Estado: draft para revisión de Gio. No es canon Notion.

```
                    Gio (humano / autorización)
                              |
                         NL-ORCH
                    ______/ | \______
                   /        |        \
            NL-AUDITOR  NL-BUILDER  NL-OPS
                   \        |        /
                    \   NL-PRODUCT  /
                     \      |      /
                      \     |     /
                       NL-MEMORY
```

## Cuándo usar a quién

| Situación | Primario | Apoyo |
|-----------|----------|-------|
| “¿Dónde estamos / qué falta?” | ORCH | MEMORY |
| Cambiar landing / copy / tool UI | PRODUCT | BUILDER |
| PR de scripts/docs/código | BUILDER | ORCH |
| Healthcheck / login portal / promote | OPS | AUDITOR (gate) |
| ¿Se puede tocar Notion / root? | AUDITOR | — |
| Cerrar sesión / dejar continuidad | MEMORY | ORCH |

## Escalamiento a Gio (siempre)

- sudo / root / dueño `sc2027`
- snapshot Hetzner
- rotación de tokens
- PAO/OT / piezas protegidas
- cualquier pedido que cruce a Valent, ERP o cliente

## Promoción a canon

Para volver esto oficial hace falta:

1. Revisión de Gio.
2. Alineación con `AGENTS.md` / `CLAUDE.md` del repo de trabajo.
3. PAO/OT si se escribe en Notion.
