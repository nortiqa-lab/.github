# AI Session Handoff — LLA aportes F2 API DEV

## Metadata

- Date: 2026-08-02
- Project: LLA Santa Cruz (cruce autorizado)
- AI actor: `NL-BUILDER` / Cursor Cloud
- Responsible user: Gio
- State: draft / ready for review

## Work Completed

- API F2: health, campaigns, destinations, intents, mandates pause/cancel, receipts, checkout block, webhook ignore
- SQLite schema + `LLA_APORTES_DB` override
- MP adapter stub (no charges)
- Legal DRAFT texts for G1
- UI wired to API with fallback
- Tests: campaign_rules, check_package, test_api_f2 all OK

## Verification

```bash
cd exports/lla-sc-aportes-f1
python3 tools/campaign_rules.py --self-test
python3 tools/check_package.py
python3 tools/test_api_f2.py
```

## Blockers

- G1 dictamen humano
- G7 sandbox MP credentials (fuera de git) solo post-G1

## Next Safe Step

- Entregar `G1-CHECKLIST.md` + `legal/DRAFT-*.md` a asesores; no implementar Preference API real hasta condiciones escritas.
