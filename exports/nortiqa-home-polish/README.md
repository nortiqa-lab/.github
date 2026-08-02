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
| `index.html` | Home pulido (estático) — **no tocar** salvo nueva pasada visual |
| `style.base.css` | Snapshot CSS del tema vivo |
| `polish.css` | Overlay de jerarquía / motion / capas |
| `nav.js` | Menú móvil del tema |
| `tests/test_home_content.py` | Contrato de contenido (9 tests) |
| `scripts/check_package.py` | Dry-run integridad (sin deploy) |
| `SECTION-HIERARCHY.md` | Orden y jerarquía propuestos |
| `COPY-DIFF.md` | Mapa live → polish para OPS |
| `APPLY.md` | Checklist dry-run + gates OPS |

## Vista local

```bash
cd exports/nortiqa-home-polish
python3 -m http.server 8765
# abrir http://127.0.0.1:8765/
```

## Validación (sin modificar la web)

```bash
python3 exports/nortiqa-home-polish/scripts/check_package.py
python3 -m unittest discover -s exports/nortiqa-home-polish/tests -p 'test_*.py'
git diff --check -- exports/nortiqa-home-polish
```

## No hace

- No despliega a `nortiqalab.com` (OPS / Gio).
- No declara PROD ni oficial.
- No mezcla entidades (Valent / ERP / clientes).
