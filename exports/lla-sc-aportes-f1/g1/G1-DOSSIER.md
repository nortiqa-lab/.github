# G1 — Dossier para dictamen conjunto

Estado: DEV / Borrador — **no es dictamen**  
Entidad: La Libertad Avanza — Santa Cruz  
Fecha de armado: 2026-08-02  
Solicitante técnico: Nortiqa (diseño) por autorización Gio  
Autoridad de encargo: Gio / conducción LLA SC

```text
OBJETO DEL DICTAMEN
¿Puede LLA Santa Cruz operar aportes voluntarios únicos y mensuales
desde llasantacruz.com.ar / portal.llasantacruz.com.ar, con condiciones
temporales de monto (CampaignRules), sin contraprestación política,
cumpliendo financiamiento político, fiscalidad y datos personales?
```

## 1. Piezas del expediente

| # | Pieza | Ubicación |
|---|-------|-----------|
| 1 | Este dossier | `g1/G1-DOSSIER.md` |
| 2 | Carta de solicitud | `g1/G1-SOLICITUD-DICTAMEN.md` |
| 3 | Matriz de preguntas | `g1/G1-PREGUNTAS.md` |
| 4 | Hallazgos preliminares (investigación) | `g1/G1-HALLAZGOS-PRELIMINARES.md` |
| 5 | Checklist operativo | `../G1-CHECKLIST.md` |
| 6 | Tracker G1–G8 | `g1/GATES-TRACKER.md` |
| 7 | Arquitectura técnica | repo `docs/dev/lla-sc/ARCH-LLA-SC-PAYMENTS-001.md` |
| 8 | Investigación Notion | [link](https://app.notion.com/p/3ade4fe3bfea8131a603e817cee62d63) |
| 8b | Este dossier en Notion | [🟡 DEV — G1 Dossier](https://app.notion.com/p/3b0e4fe3bfea8132bd44e65c1e4f3a0d) |
| 9 | Producto funcional | Notion `PROD-NQ-COMUNIDAD-POLITICA-001` |
| 10 | Borradores T&C / privacidad / consentimiento | `../legal/DRAFT-*.md` |
| 11 | Mock F1 + API F2 (sin cobros) | `../web/` · `../api/` |
| 12 | Campañas ejemplo | `../data/campaigns.json` |

## 2. Hecho / inferencia / pedido

| Tipo | Contenido |
|------|-----------|
| **Hecho** | Existe investigación Notion (2026-07-30) que concluye: no lanzar cobros recurrentes todavía; hace falta dictamen escrito conjunto. Tech F1/F2 opera con `payments_enabled=false`. |
| **Inferencia** | El diseño propuesto (aporte puro + CampaignRules sin beneficios) reduce riesgo vs “membresía con beneficios”, pero **no reemplaza** dictamen. |
| **Pedido** | Dictamen escrito: aprobar / aprobar con condiciones / rechazar, con textos mínimos para UI y condiciones para G7/G8. |

## 3. Diseño técnico bajo revisión (resumen)

- Aporte único y autorización mensual con baja/pausa 1-click.
- Sin cargos, influencia ni beneficios por monto.
- Condiciones periódicas = cambios de montos sugeridos / floor / cap / highlight de destino — **no** cuponera comercial.
- PSP propuesto: Mercado Pago (sandbox primero), cuenta partidaria.
- Destino electoral modelado pero **oculto** en UI MVP.
- Datos: consentimiento expreso; DB/host/secretos LLA ≠ Nortiqa.

## 4. Estado de cobros

**Prohibido hasta dictamen + gates G2–G8.**  
Stack actual solo simula intents/mandates/receipts.

## 5. Destinatarios sugeridos del dictamen

| Rol | Entrega |
|-----|---------|
| Asesor electoral / abogado financiamiento | Calificación aporte, personería, límites |
| Contador / fiscal | IVA / Ganancias / IIBB / comprobantes |
| Privacidad / datos | Ley 25.326, consentimiento, retención |
| Tesorero / responsable económico LLA SC | Cuenta, conciliación, rendición |
| Gio | Encargo y recepción del dictamen |

## 6. Criterio de cierre G1

G1 queda **verde** solo cuando exista documento escrito que:

1. Responda la matriz `G1-PREGUNTAS.md`.
2. Apruebe o condicione el diseño (incl. CampaignRules).
3. Fije textos o valores para T&C / privacidad / consentimiento.
4. Autorice explícitamente avanzar a G7 (sandbox PSP) o lo condicione.
