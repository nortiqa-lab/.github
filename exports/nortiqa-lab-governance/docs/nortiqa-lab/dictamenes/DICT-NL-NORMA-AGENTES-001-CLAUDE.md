# DICT-NL-NORMA-AGENTES-001-CLAUDE — Norma transversal de cualificación de agentes y bots

**Estado:** DICTAMEN FORMAL — Centro Doc Madre  
**Emisor:** Claude — ARCHITECT-001  
**Autoridad final:** Gio  
**Fecha:** 2026-07-17  
**Fuente Notion (canónica hasta redirect):** https://app.notion.com/p/3a0e4fe3bfea810385a5f889fcd1b134  
**Mirror Git seed:** 2026-08-02  

---

## VEREDICTO

**APROBADO CON CONDICIONES CRÍTICAS (C1–C5)**

Norma obligatoria para agentes activos, en prueba y futuros.  
Migración PROD / cambios bases protegidas / activación BOT-012: **bloqueados** hasta cierre C1–C5.

## Capas aprobadas

- 16 dimensiones de cualificación
- Separación rol vs personalidad vs personaje
- Orientación ideológica condicional + no herencia entre entidades
- Protocolo **DEV → AUDIT → RATIF → PROD**

## Condiciones críticas

| ID | Tema | Status al emitir |
|----|------|------------------|
| C1 | Inventario maestro y estado real | Bloqueador |
| C2 | Servidor destino + auth infra | Bloqueador |
| C3 | Cierre condiciones BOT-012 | Bloqueador |
| C4 | Matriz ideológica | Importante pre-PROD |
| C5 | Aislamiento multi-entidad | Importante pre-migración |

## Nota de mirror

Espejo resumido para bootstrap del repo `governance`.  
Antes de redirect Notion → Git, exportar el dictamen completo 1:1 y auditar paridad.
