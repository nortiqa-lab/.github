# G1 — Paquete para dictamen legal / contable / fiscal / datos

Estado: DEV / Borrador  
Entidad: LLA Santa Cruz  
Uso: completar con asesores; **no** es dictamen.

## Pregunta al dictamen

¿Puede LLA Santa Cruz operar una web de aportes voluntarios (únicos y mensuales) con condiciones temporales de monto, desde `llasantacruz.com.ar` / `portal.llasantacruz.com.ar`, cumpliendo Ley 26.215 / 27.504, régimen fiscal aplicable y Ley 25.326?

## Dossier G1 (entregable)

Carpeta `g1/` — armar y entregar a asesores:

| Pieza | Dónde |
|-------|--------|
| Índice del expediente | `g1/G1-DOSSIER.md` |
| Carta de solicitud | `g1/G1-SOLICITUD-DICTAMEN.md` |
| Matriz de preguntas | `g1/G1-PREGUNTAS.md` |
| Hallazgos preliminares | `g1/G1-HALLAZGOS-PRELIMINARES.md` (**no dictamen**) |
| Tracker G1–G8 | `g1/GATES-TRACKER.md` |

## Material adjunto para asesores

| Pieza | Dónde |
|-------|--------|
| Arquitectura | `docs/dev/lla-sc/ARCH-LLA-SC-PAYMENTS-001.md` (repo) / Notion ARCH |
| Investigación previa | Notion — Investigación financiamiento partidario LLA SC |
| Producto funcional | Notion — PROD-NQ-COMUNIDAD-POLITICA-001 |
| Mock F1 (sin cobros) | este paquete `web/` |
| API F2 simulación | este paquete `api/` |
| CampaignRules | `data/campaigns.json` + motor |
| Borradores textos | `legal/DRAFT-*.md` (**no aprobados**) |

## Checklist de respuestas requeridas

- [ ] Calificación de aporte único vs recurrente vs “campaña con monto reducido”
- [ ] ¿La reducción temporal de montos sugeridos es lícita sin contraprestación?
- [ ] Titular de la cuenta recaudadora y facultades del distrito SC
- [ ] Tratamiento de datos sensibles (opinión/afiliación política)
- [ ] Obligaciones de facturación / IVA / IIBB si hubiera recalificación
- [ ] Separación aporte institucional vs fondo electoral
- [ ] Aportantes prohibidos y controles KYC mínimos
- [ ] Texto de Términos + Privacidad + consentimiento
- [ ] Requisitos de comprobante / rendición
- [ ] Autorización explícita para pasar a G7 (PSP sandbox) y G8 (go-live)

## Salida esperada del dictamen

Documento firmado (o dictamen escrito) con: **aprobar / aprobar con condiciones / rechazar**, lista de condiciones, y textos legales mínimos para UI.

## Owner

| Rol | Responsable |
|-----|-------------|
| Conducción / Gio | Encargar y recibir dictamen |
| Asesor electoral | Respuesta normativa |
| Contador / fiscal | Encuadre impositivo |
| Datos personales | Privacidad |
| Tech Nortiqa | Solo implementar post-condiciones |
