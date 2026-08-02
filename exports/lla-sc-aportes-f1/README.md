# LLA SC — Aportes F1 (simulación)

Estado: DEV / Borrador  
Entidad: **La Libertad Avanza Santa Cruz**  
`payments_enabled`: **false** (hard-coded en `config/app.json`)

Mock punta a punta de `/aportar` con motor CampaignRules (descuentos/condiciones periódicas), aportes únicos/mensuales simulados y checklist G1. **No cobra dinero.**

## Arranque local

```bash
cd exports/lla-sc-aportes-f1
python3 -m http.server 8765
# abrir http://127.0.0.1:8765/web/
```

## Validaciones

```bash
python3 tools/campaign_rules.py --self-test
python3 tools/check_package.py
```

## Contenido

| Path | Rol |
|------|-----|
| `web/` | UI mock aportes |
| `tools/campaign_rules.py` | Motor + self-test |
| `data/campaigns.json` | Reglas de campaña |
| `G1-CHECKLIST.md` | Paquete para dictamen legal |
| `APPLY.md` | Cómo llevar a staging LLA (sin cobros) |

## Gates

Ver `ARCH-LLA-SC-PAYMENTS-001`. F1 = fase mock. No activar PSP hasta G1–G8.
