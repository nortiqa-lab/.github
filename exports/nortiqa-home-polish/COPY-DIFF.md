# COPY-DIFF — live `nortiqalab.com` → polish package

Estado: DEV / Borrador  
Fecha captura live: 2026-08-02 (GET read-only)

No modifica la web. Es la guía de port de copy para OPS/Gio.

## Hechos

| Superficie | Evidencia |
|------------|-----------|
| Home prod | Tema WP `nortiqa-lab` en `https://nortiqalab.com/` |
| CSS encolado | `style.css?ver=0.5.4` (header archivo dice Version 0.5.1) |
| Nav JS | `assets/nav.js?ver=0.5.2` |
| Markup home | En plantillas del tema (PHP); página WP “Inicio” REST tiene columnas Gutenberg residuales |

## Inventario tema (probe HTTP, sin escritura)

| Path bajo `/wp-content/themes/nortiqa-lab/` | HTTP | Nota |
|--------------------------------------------|------|------|
| `style.css` | 200 | Snapshot = `style.base.css` del paquete |
| `assets/nav.js` | 200 | = `nav.js` del paquete |
| `header.php` / `footer.php` | 200 | Acceso directo no útil (stub/HTML parcial) |
| `front-page.php` / `functions.php` / `index.php` | 500 | Esperable al hit PHP directo; **existen** en servidor |
| `parts/hero.php`, `template-parts/hero.php` | 404 | No publicables / no existen con esos nombres |

**Inferencia:** el home se arma en `front-page.php` (o equivalente) + `header.php`/`footer.php` + CSS/JS del tema. Confirmar en VPS con listado real del directorio del tema.

## Mapa de reemplazo de copy (prioridad)

| # | Live (hoy) | Polish (paquete) | Dónde |
|---|------------|------------------|-------|
| 1 | `Arquitectura · Sistemas vivos · Capacidad emergente` | `En preparación` | Hero eyebrow |
| 2 | CTA secundario `Plataforma` | `Ver el método` → `#metodo` | Hero actions |
| 3 | Capability strip **dentro** del hero | Strip **después** de Enfoque | Estructura |
| 4 | Strip `Nortiqa OS` | `firma NORTIQA` | Capability strip |
| 5 | Nav: Productos / Método / Roadmap | Enfoque / Capacidades / Método / Hoja de ruta | Header |
| 6 | Ancla solo `#productos` etc. | + `#enfoque` `#arquitectura` | IDs |
| 7 | Badge `MVP FUNCIONAL` | `PILOTO` | Card VAL-CV |
| 8 | Badge `PROTOTIPO` | `EN PREPARACIÓN` | Card Query OS |
| 9 | Badge `PILOTOS` | `EN PREPARACIÓN` | Card Agentes |
| 10 | Intro productos sin “contenido demostrativo” | Incluir frase **contenido demostrativo** | §02 |
| 11 | Método paso 03 `Prototipo funcional` | `Primera versión usable` | §03 |
| 12 | Roadmap H2 `Del prototipo al producto` | `De la preparación al despliegue` | §06 |
| 13 | Stage `MVP / Prototipo avanzado` | `En preparación` | §06 |
| 14 | Roadmap 01 `Prototipos funcionales` | `Validación funcional` | §06 |
| 15 | (nuevo) | Nota `Firma técnica NORTIQA` + mención capa interna en párrafo | §04 |

## CSS overlay a portar

Archivo `polish.css` (no reescribe el tema entero):

- Strip fuera del hero
- Tipografía display Space Grotesk en headings
- Motion suave (respeta `prefers-reduced-motion`)
- Estilos `.layer-note`, `.footer-layer`, `.hero-secondary`

**Recomendación:** anexar al final de `style.css` del tema y bump `Version` + query `ver=`.

## Fuera de alcance de este diff

- Contenido de páginas interiores (`/val-cv-intelligence/`, `/contacto/`, etc.)
- Gutenberg de página “Inicio” (limpiar residual = tarea aparte)
- DNS / Nginx / secretos
