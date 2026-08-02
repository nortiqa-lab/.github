# F3 — Alcance DEV (simulación)

Estado: DEV / Borrador  
Fecha: 2026-08-02  
`payments_enabled`: false (sin cambio)

## Incluido

| Pieza | Detalle |
|-------|---------|
| Ledger list | `GET /v1/ledger` |
| Conciliación | `POST /v1/ledger/:id/reconcile` · `/unreconcile` |
| Resumen tesorería | `GET /v1/treasury/summary` |
| Export CSV | `GET /v1/treasury/export.csv` |
| Comprobante JSON/HTML | `GET /v1/receipts/:id` · `/:id.html` |
| UI tesorería | `web/tesoreria.html` |
| Self-test | `tools/test_api_f3.py` |

## Excluido (hard stop)

- Mercado Pago sandbox real / tokens
- `payments_enabled=true`
- Factura AFIP / CAE
- DNS / prod LLA
- Mezcla DB con Nortiqa
- Dictamen G1 (humano)

## Criterio de salida F3 DEV

1. `test_api_f2.py` + `test_api_f3.py` OK  
2. CSV exportable con marca `simulation=true`  
3. HTML de comprobante con banner SIMULACIÓN  
4. Checkout sigue en 409  

## Relación con gates

F3 prepara operadores de tesorería **antes** de G7. No autoriza cobros. G1 sigue pendiente de asesores.
