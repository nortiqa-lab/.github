# Preguntas para dictamen G1 — Aportes LLA SC

**Fecha:** 2026-08-02  
**Estado:** DEV / Borrador — para completar por asesores  

Leyenda de respuesta sugerida: **Sí / No / Condicionado / No aplica** + fundamento breve + norma o criterio citado.

---

## A. Naturaleza jurídica del aporte

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| A1 | ¿Un “aporte voluntario” online a LLA Santa Cruz es jurídicamente admisible? | | |
| A2 | ¿Se clasifica como donación, aporte partidario, u otra figura? | | |
| A3 | ¿Cambia la figura si el monto es libre vs sugerido con “descuento de campaña”? | | |
| A4 | ¿Puede el partido ofrecer incentivos no políticos (merch, eventos) a cambio del aporte? | | |
| A5 | ¿Está prohibido cualquier incentivo, aunque no sea influencia política? | | |

---

## B. Sujeto receptor y cuentas

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| B1 | ¿Quién debe ser el titular de la cuenta Mercado Pago / banco? | | |
| B2 | ¿Puede usarse una persona humana como intermediaria temporal? | | |
| B3 | ¿Se requiere cuenta a nombre del partido / órgano provincial específico? | | |
| B4 | ¿Hay obligación de cuenta única de campaña en período electoral? | | |
| B5 | ¿Pueden coexistir aportes ordinarios y de campaña en el mismo PSP? | | |

---

## C. Aportantes y límites

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| C1 | ¿Hay montos mínimos/máximos legales por aportante? | | |
| C2 | ¿Se puede aceptar aporte de personas jurídicas? | | |
| C3 | ¿Se puede aceptar aporte de no residentes / extranjeros? | | |
| C4 | ¿Hay categorías prohibidas (contratistas del Estado, etc.)? | | |
| C5 | ¿El aportante debe identificarse (DNI/CUIT) siempre, o solo sobre umbral? | | |
| C6 | ¿Aportes anónimos / seudónimos están permitidos? | | |

---

## D. Campaña electoral vs período ordinario

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| D1 | ¿El formulario propuesto es usable fuera de campaña electoral? | | |
| D2 | ¿En campaña, qué obligaciones extra aplican (topes, reportes, leyendas)? | | |
| D3 | ¿Los `CampaignRule` de “descuento” pueden confundirse con beneficio electoral ilícito? | | |
| D4 | ¿Hay ventana temporal donde los cobros online deben suspenderse? | | |

---

## E. PSP / Mercado Pago

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| E1 | ¿Es admisible Mercado Pago como canal de aportes partidarios? | | |
| E2 | ¿Hay PSP preferidos o prohibidos? | | |
| E3 | ¿Los costos/comisiones del PSP pueden descontarse del aporte? | | |
| E4 | ¿El comprobante MP alcanza como respaldo contable/electoral? | | |
| E5 | ¿Hace falta factura/recibo propio del partido además del PSP? | | |

---

## F. Transparencia y reportes

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| F1 | ¿Qué datos mínimos deben registrarse por aporte? | | |
| F2 | ¿Periodicidad de reportes a órganos electorales / internos? | | |
| F3 | ¿Publicidad de listados de aportantes (umbrales)? | | |
| F4 | ¿Conservación mínima de registros (años)? | | |

---

## G. Textos y UX legal

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| G1 | ¿El disclaimer draft `DRAFT-disclaimer-aporte.md` es suficiente? | | |
| G2 | ¿Qué leyendas son obligatorias en `/aportar`? | | |
| G3 | ¿Hace falta checkbox de aceptación explícita (además del CTA)? | | |
| G4 | ¿Puede decirse “descuento” / “incentivo” en UI, o debe evitarse esa palabra? | | |
| G5 | ¿Texto mínimo de privacidad aceptable para MVP? | | |

---

## H. Datos personales

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| H1 | ¿Base legal del tratamiento (consentimiento / interés legítimo / otra)? | | |
| H2 | ¿Pueden usarse email/teléfono del aportante para comunicación política posterior? | | |
| H3 | ¿Se requiere consentimiento separado para marketing vs aporte? | | |
| H4 | ¿Restricciones si el hosting/PSP procesa datos fuera de AR? | | |
| H5 | ¿Quién es Responsable / Encargado del tratamiento? | | |

---

## I. Impositivo

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| I1 | ¿El aporte está gravado / exento para el partido? | | |
| I2 | ¿El aportante obtiene deducción o beneficio fiscal? | | |
| I3 | ¿Hay retención o percepción aplicable? | | |
| I4 | ¿Obligación de emitir factura electrónica / recibo? | | |
| I5 | ¿Tratamiento de comisiones PSP y chargebacks? | | |

---

## J. Reembolsos, fallos y disputas

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| J1 | ¿Política de reembolso permitida / recomendada? | | |
| J2 | ¿Qué hacer con pagos `authorized` luego disputados (chargeback)? | | |
| J3 | ¿Cómo documentar aportes fallidos o rechazados? | | |

---

## K. Hard stops — confirmación

| ID | Pregunta | Respuesta | Notas |
|----|----------|-----------|-------|
| K1 | ¿Confirmáis el hard stop: no influir/acceso a cambio de dinero? | | |
| K2 | ¿Hay otros hard stops legales no listados en la arquitectura? | | |
| K3 | ¿Podemos publicar el mock `/aportar` sin cobro real mientras se dictamina? | | |

---

## Firma asesores

| Área | Nombre | Fecha | Firma / OK |
|------|--------|-------|------------|
| Jurídico electoral | | | |
| Impositivo | | | |
| Tesorería | | | |
| Datos personales | | | |
| Mesa LLA SC (ratificación política) | | | |
