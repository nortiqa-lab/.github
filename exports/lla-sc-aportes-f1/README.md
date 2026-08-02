# LLA SC — Aportes F1/F2 DEV (simulación)

Estado: DEV / Borrador  
Entidad: **La Libertad Avanza Santa Cruz**  
`payments_enabled`: **false** (enforced; API se niega a arrancar si está true)

Mock + API F2 local con SQLite, adapter Mercado Pago stub, CampaignRules y borradores legales para G1. **No cobra dinero.**

## Arranque local

```bash
cd exports/lla-sc-aportes-f1

# Terminal A — API F2
python3 api/server.py --port 8787

# Terminal B — UI estática
python3 -m http.server 8766
# abrir http://127.0.0.1:8766/web/
```

La UI usa `config.api_base_url` si la API responde; si no, cae a localStorage.

## Validaciones

```bash
python3 tools/campaign_rules.py --self-test
python3 tools/check_package.py
python3 tools/test_api_f2.py
```

## Contenido

| Path | Rol |
|------|-----|
| `web/` | UI mock aportes |
| `api/` | F2 API stdlib + SQLite + MP stub |
| `tools/campaign_rules.py` | Motor + self-test |
| `data/campaigns.json` | Reglas de campaña |
| `legal/` | Borradores G1 (no aprobados) |
| `g1/` | Dossier para asesores (solicitud, preguntas, hallazgos, tracker) |
| `G1-CHECKLIST.md` | Checklist operativo del dictamen |
| `APPLY.md` | Staging LLA sin cobros |

## Gates

Ver `g1/GATES-TRACKER.md` y `docs/dev/lla-sc/ARCH-LLA-SC-PAYMENTS-001.md`.  
No activar PSP hasta G1–G8.
