# NORTIQA home polish (DEV)

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Qué es

Pasada visual fina **sección por sección** sobre el home institucional vivo
(`https://nortiqalab.com/`, tema WP `nortiqa-lab` ~0.5.x), versionada aquí
porque este agent corre en `nortiqa-lab/.github` y **no** tiene push al tema
en VPS ni al repo de producto.

## Asunción de dirección

**Capa pública = institucional** (seriedad / bajo construcción), no catálogo
de producto gritando “demo/MVP/prototipo”. La plataforma NORTIQA queda como
**firma técnica** en arquitectura/footer, no como segundo protagonista del hero.

## Contenido

| Archivo | Rol |
|---------|-----|
| `index.html` | Home pulido (estático) |
| `style.base.css` | Snapshot CSS del tema vivo |
| `polish.css` | Overlay de jerarquía / motion / capas |
| `nav.js` | Menú móvil del tema |
| `tests/test_home_content.py` | Contrato de contenido (9 tests) |
| `SECTION-HIERARCHY.md` | Orden y jerarquía propuestos |
| `APPLY.md` | Cómo llevar esto al tema WP / producto |

## Vista local

```bash
cd exports/nortiqa-home-polish
python3 -m http.server 8765
# abrir http://127.0.0.1:8765/
```

## Validación

```bash
python3 -m unittest discover -s exports/nortiqa-home-polish/tests -p 'test_*.py'
git diff --check -- exports/nortiqa-home-polish
```

## No hace

- No despliega a `nortiqalab.com` (OPS / Gio).
- No declara PROD ni oficial.
- No mezcla entidades (Valent / ERP / clientes).
