# AI Session Handoff — F3 tesorería simulación LLA SC

## Metadata

- Date: 2026-08-02
- Project: Nortiqa Lab (cruce autorizado → LLA Santa Cruz pagos web)
- AI actor: `NL-BUILDER` / Cursor Cloud
- Responsible user: Gio
- State: draft / ready for review

## Canon Read

- MEM-NL-ROOT-001: Notion connector disponible; no Madre reescrita
- Active plans: ARCH-LLA-SC-PAYMENTS-001; G1 dossier pendiente asesores
- Applicable OT/PAO: ninguno nuevo

## Assumptions

- G1 sigue abierto (humano); F3 no habilita cobros.
- Export CSV / conciliación son herramientas DEV sobre ledger simulado.

## Work Completed

- F3 DEV: ledger, reconcile/unreconcile, treasury summary, CSV export, receipt HTML
- UI `web/tesoreria.html` + self-test `tools/test_api_f3.py`
- Docs: F3-SCOPE, ARCH, README, APPLY, gates tracker, changelog

## Files or Pieces Changed

- `exports/lla-sc-aportes-f1/api/{server.py,db.py,schema.sql}`
- `exports/lla-sc-aportes-f1/web/tesoreria.*` + styles/index
- `exports/lla-sc-aportes-f1/tools/test_api_f3.py` + check_package
- `exports/lla-sc-aportes-f1/docs/F3-SCOPE.md`
- ARCH / CHANGELOG / handoff / Notion (si publicado)

## Verification

- Commands: `campaign_rules --self-test`, `check_package`, `test_api_f2`, `test_api_f3`
- Result: ver PR notes
- Limitations: sin MP sandbox; sin dictamen G1

## Blockers

- Humano: cerrar G1 con asesores antes de G7

## Risks

- Confundir CSV simulado con rendición oficial (mitigado: columna `simulation` + banners)

## Next Safe Step

- Gio entrega dossier G1 a asesores; opcionalmente prueba `web/tesoreria.html` en local. No abrir MP sandbox.
