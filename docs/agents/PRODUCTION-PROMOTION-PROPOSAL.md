# Propuesta — plan de promoción a producción (NO EJECUTAR)

**Estado:** propuesta solamente.  
**No autoriza** cambios en producción. Requiere Gio + PAO/OT.

## Precondiciones

1. Agente en `active-staging` con evidencia de operación estable en staging.
2. Dictamen técnico vigente (re-correr acceptance si cambió el manifiesto).
3. PAO/OT explícitos para promoción.
4. Confirmación de Gio con texto de autorización.
5. Backup/snapshot y plan de rollback OPS documentados.

## Fases propuestas

| Fase | Acción | Actor |
|------|--------|-------|
| P0 | Congelar manifiesto (`tools`/`scope`/`prohibitions`) | Gio |
| P1 | Re-validar acceptance + checklist OPS staging | Tester + OPS |
| P2 | Dictamen AUDITOR (gate) | NL-AUDITOR |
| P3 | `status: production-approved` en manifiesto | **Solo Gio** |
| P4 | Promote controlado + health checks | NL-OPS (privilegios) |
| P5 | Handoff + ventana de observación | MEMORY + OPS |

## Controles

- Sin secretos en logs.
- Sin autoaprobación.
- Sin promote si hay lock activo o drift de gobernanza.
- Rollback ensayado en staging antes de P4.

## Fuera de esta propuesta

- Activación inmediata
- Cambios DNS / Nginx / `.env` sin privilegios
- Mezcla con otras entidades
