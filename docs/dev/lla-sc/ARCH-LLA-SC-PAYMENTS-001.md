# ARCH-LLA-SC-PAYMENTS-001 — Arquitectura de aportes, cobros y condiciones periódicas

Estado: DEV / Borrador

No es documentación oficial. No autoriza cobros reales.
Requiere: dictamen legal-contable-fiscal-datos + ratificación Gio + tesorería LLA SC
antes de cualquier medio de pago en producción.

```text
ENTIDAD: La Libertad Avanza — Santa Cruz (LLA SC)
DOMINIO CANÓNICO: llasantacruz.com.ar
PORTAL SUGERIDO: portal.llasantacruz.com.ar
CRUCE AUTORIZADO: Gio 2026-08-02 — diseñar arquitectura de pagos desde la web LLA SC.
AISLAMIENTO: secretos, cuentas bancarias, datos de aportantes y ops DNS LLA
≠ Nortiqa Lab / Valent / ERP / SC2027 product stack.
ROL NORTIQA: proveedor de diseño/desarrollo (si se confirma); no titular de fondos.
```

| Campo | Valor |
|-------|--------|
| Fecha | 2026-08-02 |
| Actor | Cursor / `NL-BUILDER` |
| Fuentes | Investigación financiamiento LLA; `PROD-NQ-COMUNIDAD-POLITICA-001`; `DOM-LLA-SC-001` |
| Bench orquestación | Payments plugins marketplace = **No usar** (ratificado) |

---

## 0. Distinción evidencia

| Tipo | Contenido |
|------|-----------|
| **Hecho** | Investigación Notion: no lanzar cobros recurrentes todavía; cuenta partidaria, tesorero, trazabilidad y dictamen previo son obligatorios. Dominio `llasantacruz.com.ar` registrado. PSP no elegido. |
| **Inferencia** | “Descuentos periódicos” en contexto político deben modelarse como **condiciones temporales de aporte** (monto sugerido / campaña), no como cupones e-commerce que creen contraprestación comercial. |
| **Recomendación** | Arquitectura por capas abajo; PSP primario **Mercado Pago** (AR); Chargebee/Airwallex/Circle/1inch fuera de MVP. |

---

## 1. Objetivo

Permitir desde la web institucional LLA SC:

1. **Aporte único** con comprobante.
2. **Aporte recurrente** (autorización mensual) con pausa/cancelación simple.
3. **Condiciones periódicas** (campañas: monto reducido temporal, montos sugeridos, destinos).
4. **Trazabilidad** aportante → medio → destino → rendición.
5. **Sin** vender cargos, influencia ni beneficios políticos por dinero.

---

## 2. Gates legales (hard stop de implementación)

No activar cobros hasta checklist verde:

| # | Gate | Owner |
|---|------|-------|
| G1 | Dictamen electoral + contable + fiscal + datos personales | Asesores LLA / Gio |
| G2 | Personería y facultades distrito Santa Cruz validadas | Conducción / tesorería |
| G3 | Cuenta bancaria partidaria + responsable económico | Tesorería |
| G4 | Política de aportantes permitidos/prohibidos | Legal |
| G5 | Términos, privacidad, consentimiento datos sensibles | Legal + producto |
| G6 | Calificación jurídica de cada “nivel” (aporte vs servicio) | Legal |
| G7 | Ambiente staging PSP con plata de prueba | Tech |
| G8 | Ratificación Gio para go-live | Gio |

**Hasta G1–G8:** solo mock/sandbox; UI puede existir en “modo simulación”.

---

## 3. Arquitectura lógica (capas)

```text
[Web LLA SC — portal.llasantacruz.com.ar]
        │
        ▼
[Capa Experiencia]  aporte UX, campañas, perfil, comprobantes
        │
        ▼
[Capa Dominio Aportes]  Intent · Mandate · Ledger · CampaignRules
        │
        ├─► [Identity & KYC-lite]  identidad mínima aportante
        ├─► [Compliance]          listas prohibidas, límites, flags
        ├─► [PSP Adapter]         Mercado Pago (primario) · stub otros
        └─► [Ops / Tesorería]     conciliación, exportación, rendición
```

### 3.1 Principio de calificación

| Concepto UX | Modelo interno | Riesgo |
|-------------|----------------|--------|
| “Aporte solidario” | `contribution` voluntario | Bajo si sin contraprestación |
| “Membresía premium con beneficios” | evitar en MVP | Alto (servicio / influencia) |
| “Descuento 20% este mes” | `campaign_rule` sobre monto sugerido | Medio — revisar legal |
| “Suscripción a contenidos pagos” | fuera de MVP aportes | Alto fiscal |

Regla: el dinero **no** compra rol, cargo, voto interno ni acceso político privilegiado (`PROD-NQ-COMUNIDAD-POLITICA-001`).

---

## 4. Modelo de dominio (mínimo)

### 4.1 Entidades

| Entidad | Campos clave |
|---------|--------------|
| `Person` | id, nombre, DNI/CUIT opcional fase2, email, teléfono, localidad, consentimientos |
| `ContributionIntent` | id, person_id, type=`one_time\|recurring`, amount_cents, currency=`ARS`, destination, campaign_id?, status |
| `RecurringMandate` | id, person_id, amount_cents, period=`monthly`, next_charge_at, status=`active\|paused\|cancelled`, psp_ref |
| `CampaignRule` | id, code, window `[start,end]`, rule_type, params, legal_review_status |
| `LedgerEntry` | id, intent_id, psp_payment_id, amount_gross, amount_net, fees, status, settled_at |
| `Receipt` | id, ledger_id, number, pdf/html ref, issued_at |
| `Destination` | `general`, `territorial:<sede>`, `project:<id>`, `electoral` (circuito separado) |

### 4.2 Máquina de estados — Intent

```text
draft → ready → checkout_created → authorized
     → captured → receipt_issued → reconciled
     ↘ failed / cancelled / refunded
```

### 4.3 Máquina — Mandate recurrente

```text
proposed → consented → active ⇄ paused → cancelled
active → charge_attempt → (captured | soft_fail | hard_fail)
```

---

## 5. Lógica de “descuentos periódicos” (Campaign Rules)

No implementar cupones estilo e-commerce sin dictamen. Modelo permitido en DEV:

| `rule_type` | Comportamiento | Ejemplo |
|-------------|----------------|---------|
| `suggested_amount_override` | Reemplaza montos sugeridos en UI durante ventana | Agosto: sugeridos 2k/5k/10k |
| `amount_cap` | Tope máximo aceptado en campaña | Max 50k en evento X |
| `amount_floor` | Mínimo | Min 1000 ARS |
| `percent_reduction_on_suggested` | Reduce % sobre sugeridos (no sobre “precio de producto”) | −20% sobre sugeridos por 30 días |
| `destination_boost` | Destaca destino territorial/proyecto | Sede Río Turbio |
| `pause_recurring_promo` | Mensaje para pausar sin fricción | Baja en 1 click |

### 5.1 Motor de evaluación

```text
input: base_suggested[], now, person?, destination?
rules = active CampaignRules where legal_review_status=approved_for_staging|prod
apply in priority order → output: display_amounts[], labels[], disclaimers[]
```

**Disclaimer obligatorio en UI** cuando hay reducción temporal:

> Condición promocional de aporte voluntario. No implica membresía, cargo ni beneficio político.

### 5.2 Lo que NO va en MVP

- Cashback
- Puntos / gamificación por monto
- Beneficios premium por pagar más
- Cripto (1inch) / stablecoins
- Suscripción SaaS Chargebee

---

## 6. Flujo web (UX)

### 6.1 Aporte único

1. `/aportar` — monto (sugerido o libre) + destino + campaña visible.
2. Identidad mínima + consentimientos.
3. Checkout PSP (redirect o brick).
4. Webhook → ledger → comprobante.
5. `/comprobantes` en perfil.

### 6.2 Aporte mensual

1. `/aportar/mensual` — monto + destino.
2. Texto claro de autorización recurrente + baja.
3. Tokenización / suscripción PSP.
4. Mandate `active`; cargos periódicos.
5. Usuario puede **pausar / modificar / cancelar** sin fricción.

### 6.3 Campaña periódica

1. Admin crea `CampaignRule` (DEV→staging→prod con G1).
2. Banner en home/aportes con ventana de fechas.
3. Motor aplica montos; ledger guarda `campaign_id` para auditoría.

---

## 7. Arquitectura técnica propuesta

### 7.1 Superficie web

| Pieza | Propuesta DEV |
|-------|----------------|
| Dominio | `llasantacruz.com.ar` / `portal.llasantacruz.com.ar` |
| CMS / app | A definir (WP vs app propia); **módulo aportes** desacoplado |
| TLS | Nginx + cert (ops LLA; ver DEC DNS) |

### 7.2 Backend aportes (servicio dedicado)

```text
lla-sc-contributions (API)
  POST /v1/intents
  POST /v1/mandates
  POST /v1/mandates/:id/pause|cancel
  GET  /v1/receipts
  POST /v1/webhooks/mercadopago
  GET  /v1/campaigns/active
  admin: CRUD campaigns (role-gated)
```

### 7.3 PSP Adapter

| Adapter | Prioridad | Uso |
|---------|-----------|-----|
| `MercadoPagoAdapter` | P0 | Checkout Pro / Suscripciones AR |
| `BankTransferManualAdapter` | P1 | CBU partidario + conciliación manual |
| `StripeAdapter` | P3 | Solo si hay caso no-AR; no MVP |
| Chargebee / Airwallex / Circle / 1inch | **Descartar MVP** | Bench orquestación + fit legal AR |

### 7.4 Datos y seguridad

- DB propia LLA (PostgreSQL) — **no** mezclar con Nortiqa Odoo/Postgres prod.
- Secretos PSP solo en vault/env del host LLA.
- Datos políticos = sensibles (Ley 25.326): minimización, consentimiento, acceso/rectificación/baja.
- Webhooks firmados; idempotencia por `psp_payment_id`.
- Logs sin PAN/CVV; token PSP opaco.

### 7.5 Integraciones

| Sistema | Rol |
|---------|-----|
| Web pública | UI |
| n8n (opcional, cuenta LLA) | Notificaciones, conciliación asistida — **no** decidir compliance solo |
| Tesorería export | CSV/Excel periodico para rendición |
| QGIS / mapa | Destinos territoriales (fase 2; ver producto comunidad) |

---

## 8. Descuentos / condiciones — API conceptual

```json
{
  "campaign_id": "camp_2026_ago_solidario",
  "rule_type": "percent_reduction_on_suggested",
  "params": { "percent": 20, "suggested_base": [2000, 5000, 10000] },
  "window": { "start": "2026-08-01", "end": "2026-08-31" },
  "legal_review_status": "pending",
  "disclaimer_key": "aporte_voluntario_sin_contraprestacion"
}
```

Evaluación:

```text
display = suggested_base * (1 - percent/100)
persist on Intent: amount_cents, campaign_id, amount_before_campaign_cents
```

---

## 9. Roles y permisos

| Rol | Puede |
|-----|-------|
| Visitante | Ver info aportes |
| Aportante | Crear intent/mandate, ver comprobantes, pausar/cancelar |
| Admin campaña | CRUD campaigns en staging |
| Tesorería | Export, conciliación, marcas reconciled |
| Compliance | Flags, bloqueos aportantes |
| Superadmin LLA | Go-live config (post G8) |

Nortiqa agentes: **solo DEV docs/código en repos autorizados**; sin acceso a ledger prod.

---

## 10. Plan de implementación (sin cobros reales)

| Fase | Entregable | Cobros |
|------|------------|--------|
| F0 | Este ARCH + gates G1–G8 checklist | No |
| F1 | UI mock + CampaignRules en memoria/JSON | Simulado |
| F2 | API + DB staging + MP sandbox | Plata de prueba |
| F3 | Conciliación + comprobantes + export tesorería | Sandbox |
| F4 | Dictámenes cerrados + go-live limitado | Sí, post G8 |
| F5 | Recurrente + campañas periódicas prod | Sí |

---

## 11. Relación con producto Nortiqa

`PROD-NQ-COMUNIDAD-POLITICA-001` describe la plataforma amplia (mapa, afiliación, etc.).  
Este ARCH es el **submódulo financiero de aportes** para la web LLA SC:

- Puede vivir como módulo embebido en esa plataforma **o** como microservicio consumido por el portal.
- Proveedor de pago = TBD en producto; aquí se fija **recomendación técnica MP** sujeta a legal.

---

## 12. Riesgos

| Riesgo | Mitigación |
|--------|------------|
| Cobrar antes de dictamen | Gates G1–G8; flag `payments_enabled=false` |
| Recalificación como servicio | Evitar beneficios; disclaimers; legal review campaigns |
| Cuenta personal | Solo cuenta partidaria |
| Mezcla Nortiqa/LLA datos | DB/host/secretos separados |
| Plugin marketplace Payments | No usar (bench ratificado) |
| Descuento = influencia | Prohibido en reglas de negocio |

---

## 13. Decisiones DEV registradas

1. PSP MVP: Mercado Pago (sandbox primero).
2. “Descuentos periódicos” = `CampaignRule`, no cuponera comercial.
3. Recurrente con baja 1-click.
4. Destino electoral = circuito separado desde día 0 en modelo (aunque UI lo oculte al inicio).
5. Sin cripto / Chargebee / Airwallex en MVP.
6. Sin cobros hasta gates.

---

## 14. Próximo paso (uno)

Cerrar **G1** (dictamen legal-contable-fiscal-datos) mientras tech arma F1 mock UI + motor `CampaignRule` en staging sin PSP real.
