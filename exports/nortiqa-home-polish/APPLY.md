# APPLY — port del polish al tema WP (humano / OPS)

Estado: DEV / Borrador

**Restricción de esta sesión:** avanzar documentación y dry-run **sin modificar la web**
(ni `nortiqalab.com`, ni assets visuales del paquete).

## Hecho (fact)

- Home prod = tema `nortiqa-lab` en VPS detrás de `https://nortiqalab.com/`.
- Paquete versionable: este directorio (`exports/nortiqa-home-polish/`).
- Diff de copy: [`COPY-DIFF.md`](./COPY-DIFF.md).
- Jerarquía: [`SECTION-HIERARCHY.md`](./SECTION-HIERARCHY.md).

## Dry-run local (sin deploy) — cualquiera

```bash
cd exports/nortiqa-home-polish
python3 scripts/check_package.py
python3 -m unittest discover -s tests -p 'test_*.py'
# Preview opcional (solo localhost; no es prod):
# python3 -m http.server 8765
```

Criterio dry-run OK: exit 0 en check + 9/9 tests.

## Checklist OPS (cuando Gio autorice tocar el tema)

> Zona roja hasta autorización explícita. Comandos siguientes son **documentación**, no ejecución automática.

1. **Backup tema** en el host (ruta real a confirmar en VPS):
   ```bash
   # PENDIENTE DE VALIDACIÓN — path típico WP; confirmar antes
   sudo -u <wp-user> tar -C /var/www/<site>/wp-content/themes \
     -czf ~/backups/nortiqa-lab-theme-$(date -u +%Y%m%dT%H%M%SZ).tgz nortiqa-lab
   ```
2. **Diff conceptual** en staging/copia local del tema:
   - Markup: `front-page.php` (u home template) ↔ `index.html` del paquete
   - Copy: filas de `COPY-DIFF.md`
   - CSS: append `polish.css` → `style.css`; bump Version
   - JS: `assets/nav.js` ya alineado; no requiere cambio salvo regresión
3. **No** editar prod a ciegas: preferir copia staging del tema o child-theme temporal.
4. Tras port: health público read-only
   ```bash
   curl -sS -o /dev/null -w "%{http_code}\n" https://nortiqalab.com/
   ```
5. Smoke visual: hero eyebrow, badges, roadmap stage, mobile nav.
6. Rollback = restaurar tarball del paso 1.

## Alternativa producto-repo

`giovanyalbea-dotcom/nortiqa-lab` `site/site/index.html` está desalineado/corrupto (sin tags HTML).
No es el home prod. Solo espejar si Gio lo pide aparte.

## No hacer desde agent Cloud

- Editar VPS / tema live
- Nginx reload, DNS, secretos
- Declarar PROD / oficial
- Merge a `main` sin política Gio

## Gate de cierre

| Gate | Owner |
|------|--------|
| Ratificar copy/jerarquía | Gio |
| Auditoría draft (opcional) | NL-AUDITOR / ARCHITECT-001 |
| Privileged theme write | NL-OPS + Gio |
| Merge PR kit | Gio / política repo |
