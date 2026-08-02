# Plantilla de redirección Notion → Git

**Usar solo cuando Gio autorice writes en Centro Doc Madre + exista canónico en Git.**

```markdown
# [CÓDIGO] — Migrado a Git

**Estado:** PROD — Migrado a Git  
**Fecha de migración:** YYYY-MM-DD  
**Canónico:** https://github.com/nortiqa-lab/governance/blob/main/docs/[entidad]/[tipo]/[archivo].md  

El contenido operativo vive en GitHub. Esta página se conserva como índice/redirect.

**No borrar** esta página de Notion hasta auditoría de redirects + OK Gio.
```

## Checklist pre-redirect

- [ ] Archivo existe en `governance` `main`
- [ ] PR mergeado
- [ ] Claude auditó lote
- [ ] Gio autorizó write en la página Notion
- [ ] Enlaces internos Notion actualizados o anotados
