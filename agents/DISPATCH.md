# Protocolo de despacho — modo autónomo

## 1. Entrada

Suficiente con:

- Objetivo en una frase de Gio (o brief de otro agente).

Opcional: repo, restricciones, links. Si faltan, asumir Nortiqa + este repo + cambio reversible mínimo.

## 2. Clasificación (`NL-ORCH` o auto)

| Clase | Ejemplo | Roles |
|-------|---------|-------|
| A — Lectura | Mapear estado | ORCH + MEMORY |
| B — Draft | Propuesta/checklist | BUILDER o PRODUCT + MEMORY |
| C — Versionable | PR | BUILDER (± PRODUCT) |
| D — Protegido | Notion root/PAO | AUDITOR → escalate if write |
| E — VPS | Health/promote/login | OPS (± AUDITOR gate) |

Ambiguo → interpretación más segura y reversible; documentar supuesto. Solo preguntar a Gio si entrarías en zona roja.

## 3. Asignación autónoma

- ≤3 roles activos.
- Preferí ejecutar en la misma sesión si el trabajo es chico.
- Si necesitás hermanos: emití prompts listos de `prompts/` y/o invocá subagentes con ese texto.
- `NL-OPS` no en paralelo con promotes no relacionados.
- Contaminación Valent/ERP/cliente → STOP.

## 4. Contrato de salida

1. `ROLE: NL-*`
2. Canon: read | bootstrap-draft
3. DONE
4. VERIFY
5. BLOCKED (acción exacta si aplica)
6. NEXT (una línea)

Handoff file: `docs/shared-ai-memory/handoff-template.md` → guardar en `docs/shared-ai-memory/handoffs/YYYY-MM-DD-<slug>.md`.

## 5. Consola final

Una respuesta a Gio:

- Hechos verificados
- Riesgos
- Blockers humanos exactos
- **Un** próximo paso

## 6. Hard stops

- Mezcla de entidades
- Escritura Notion protegida sin auth
- Promote sin gates
- Secretos en claro
- Pedido fuera de Nortiqa
