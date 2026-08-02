# APPLY — llevar el polish al home real

Estado: DEV / Borrador

## Hecho (fact)

- El home de producción se renderiza con el tema WordPress `nortiqa-lab`
  en `https://nortiqalab.com/` (no vive en este repo `.github`).
- Este paquete es el borrador versionable de la pasada fina.

## Inferencia

- El markup del home está en plantillas PHP del tema (p. ej. `front-page.php` /
  partes del theme), no en el bloque Gutenberg de la página “Inicio”
  (esa página tiene columnas residuales vía REST).

## Aplicación recomendada (humana / OPS)

1. Revisar visualmente el estático:
   `python3 -m http.server` dentro de este directorio.
2. Diff conceptual: `index.html` + `polish.css` vs tema en VPS
   (`wp-content/themes/nortiqa-lab/`).
3. Portar copy + estructura al theme; anexar reglas de `polish.css`
   (o mergear) al `style.css` del tema y subir versión.
4. No promover a PROD sin gates OPS + ratificación Gio.

## Alternativa producto-repo

Si se quiere espejo estático en `giovanyalbea-dotcom/nortiqa-lab`:

- Hoy `site/site/index.html` en ese repo aparece **sin tags HTML**
  (solo texto) — tratar como corrupto/desalineado del home WP.
- Aplicar este paquete ahí requiere write access (bot tuvo 403 antes)
  o apply manual por Gio.

## No hacer desde este agent

- Editar archivos en el VPS
- Reload Nginx / deploy WP
- Declarar el cambio en producción
