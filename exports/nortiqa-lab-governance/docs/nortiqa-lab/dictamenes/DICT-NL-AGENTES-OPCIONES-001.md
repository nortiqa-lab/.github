# DICT-NL-AGENTES-OPCIONES-001 — 9 Decisiones Agent Router System

**Estado:** Mirror seed Git — fuente Notion  
**Tipo:** Dictamen de opciones (ratificación Gio por decisión)  
**Auditor:** Claude (ARCHITECT-001)  
**Fecha:** 2026-07-05  
**Fuente Notion:** https://app.notion.com/p/394e4fe3bfea81ce8b19e5842280ccbb  

> Mirror resumido. Canon vivo en Notion hasta redirect. No borrar Notion.

## Contexto

Agent Router System — 9 decisiones de implementación sobre PAO-NL-AGENTES-MULTIMODELO-001.

## Recomendaciones Claude (por decisión)

| # | Tema | Recomendación |
|---|------|---------------|
| 1 | Comunicación inter-agente | D — Hybrid (MQ + API fallback) |
| 2 | Dónde vive el Router | A — Contenedor Docker dedicado |
| 3 | Service discovery | C — Tabla PostgreSQL + polling |
| 4 | Criterio de routing | C — Least-loaded |
| 5 | Autorización agent↔agent | B — ACL en BD |
| 6 | Logging/auditoría | D — Audit table + Prometheus |
| 7 | Fallos | D — Retry + Circuit Breaker + Failover |
| 8 | Health | D — Heartbeat + /health + Prometheus |
| 9 | Escalamiento | B ahora → C (K8s) futuro |

## Ruta Fase 0 (pilot)

Decisiones 1–8 core+reliability; decisión 9 solo LB. Resultado: Router con ~8 agentes max, auditoría y failover.
