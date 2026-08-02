# Home polish — listo para apply (parked)

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Fecha: 2026-08-02  
PR kit: https://github.com/nortiqa-lab/.github/pull/11  
Paquete: `exports/nortiqa-home-polish/`

## Hecho

- Pasada visual fina versionada (estático).
- Tests de contenido 9/9 + `scripts/check_package.py`.
- Copy-diff live→polish documentado (`COPY-DIFF.md`).
- **Web prod no modificada** (`nortiqalab.com` intacto).

## Inferencia

- Apply real = editar tema WP en VPS (`front-page.php` + `style.css` + copy).
- Este repo solo guarda el kit; no es el origen de deploy automático.

## Recomendación

1. Gio revisa preview local cuando quiera.
2. Si aprueba: OPS sigue `exports/nortiqa-home-polish/APPLY.md` (backup → port → smoke → rollback plan).
3. Decisión abierta (no bloquea docs): capa pública más institucional vs más producto.

## No hacer todavía

- Deploy / write al tema live
- Declarar oficial o PROD
