# T-005 — Paquete piloto A1: Agente documental básico

Estado: DEV / Borrador  
Entidad: Nortiqa Lab exclusively  
Factory: `SYS-NL-AGENT-FACTORY-001`  
Package ID: `DOC-AGENT-A1`  
Autonomy: A1 (asistido; sin herramientas de escritura externas en este paquete)

## Objetivo

Producir un paquete reproducible de agente documental: ficha, prompt, controles, 10 casos de prueba e inventario — sin deploy, sin secretos, sin PROD.

## Entregables

| Archivo | Rol |
|---------|-----|
| `ficha.md` | Identidad y límites |
| `prompt.md` | Prompt operativo |
| `controls.md` | Controles y prohibiciones |
| `tests.md` | 10 casos de prueba |
| `inventory-entry.json` | Entrada para inventario Factory |

## Criterio de cierre T-005

1. `anti_dupe.py` → `ALLOW_PILOT` para este pedido.
2. Los cinco archivos existen y son coherentes.
3. Ningún archivo pide acceso a PROD, secretos o cruces de entidad.
4. Resultado registrado en handoff / Notion Factory.

## No incluido

- Runtime n8n
- Escritura a Notion canon PROD
- Credenciales
- T-006 (A2 gastro)
