# APPLY — LLA SC Aportes F1–F3 (sin cobros)

Estado: DEV / Borrador

## Objetivo

Publicar el mock en un entorno **staging LLA** (o revisión local) con `payments_enabled=false`.

## Precondiciones

1. Cruce de entidad autorizado (Gio — ya documentado para diseño).
2. No usar cuentas/secretos Nortiqa.
3. DNS/hosting LLA según `DOM-LLA-SC-001` / DEC DNS (ops LLA, no este repo).
4. G1 en curso o pendiente — **no** bloquear el mock, sí bloquear cobros.

## Pasos

1. Copiar `exports/lla-sc-aportes-f1/` al host/staging LLA autorizado.
2. Verificar `config/app.json` → `"payments_enabled": false`.
3. Arrancar API: `python3 api/server.py --host 127.0.0.1 --port 8787` (o proxy interno).
4. Ajustar `api_base_url` si el host/puerto difiere.
5. Servir el directorio del paquete (no solo `web/`) para que existan `../config` y `../data`.
6. Abrir `/web/` y probar:
   - montos con campaña agosto (−20% + floor);
   - destino Río Turbio destacado;
   - aporte único/mensual vía API;
   - `POST /v1/checkout` sigue bloqueado;
   - consentimiento obligatorio.
7. Abrir `/web/tesoreria.html`: ledger, conciliar, CSV, comprobante HTML.
8. Entregar `g1/` + `legal/DRAFT-*.md` a asesores.

## Prohibido en este apply

- Setear `payments_enabled=true`
- Conectar Mercado Pago / keys
- Mezclar DB o `.env` de Nortiqa
- Cobrar en producción

## Rollback

Quitar el vhost/staging o restaurar la carpeta anterior. Borrar SQLite local en `var/` si se usó API DEV (gitignored).
