# Solicitud de dictamen — Aportes voluntarios LLA Santa Cruz (G1)

**Fecha:** 2026-08-02  
**De:** Giovany Albea — dirección técnica / producto (canal Nortiqa Lab autorizado)  
**Para:** Asesoría jurídica electoral / política · Asesoría impositiva · Tesorería LLA SC · Responsable datos personales  
**Asunto:** Dictamen previo a habilitación de cobros online (`payments_enabled`)  
**Estado del paquete técnico:** DEV / mock + API sin cobro real  
**Urgencia sugerida:** alta para planificación; **no** hay cobros en producción hoy  

---

## 1. Pedido

Solicitamos **dictamen escrito** (puede ser correo formal o memo) que responda las preguntas del archivo `G1-PREGUNTAS.md`, con conclusión clara:

> **¿Se puede habilitar un formulario de aportes voluntarios online con Mercado Pago (u otro PSP) en el dominio `llasantacruz.com.ar` / `portal.llasantacruz.com.ar`, bajo las condiciones técnicas descritas, o qué condiciones/impedimentos aplican?**

Hasta recibir dictamen favorable (o condiciones aceptadas por la mesa), el sistema permanece con:

```json
"payments_enabled": false
```

---

## 2. Qué se está construyendo (hechos)

| Hecho | Detalle |
|-------|---------|
| Entidad | La Libertad Avanza — Santa Cruz (partido / estructura provincial) |
| Superficie | Página pública de aportes + API + webhook PSP |
| Objetivo | Recibir **aportes voluntarios** con montos sugeridos y campañas de incentivo |
| No es | Tienda, membresía SaaS, crowdfunding genérico, venta de bienes |
| PSP propuesto MVP | Mercado Pago (sandbox primero) |
| Descuentos | Reglas de campaña sobre **montos sugeridos**, no cupones tipo e-commerce |
| Influencia política | **No** se ofrece ni se canjea influencia/acceso por aporte |
| Estado técnico | Mock F1 + API F2 DEV; cobro real bloqueado en código |

Arquitectura versionada: `docs/dev/lla-sc/ARCH-LLA-SC-PAYMENTS-001.md`  
Paquete: `exports/lla-sc-aportes-f1/`  

---

## 3. Material adjunto para asesores

1. Este dossier (`g1/`)  
2. Borradores legales `legal/DRAFT-*.md` (**no aprobados**)  
3. Checklist `G1-CHECKLIST.md`  
4. Preguntas `G1-PREGUNTAS.md`  
5. Hallazgos preliminares de investigación Notion `G1-HALLAZGOS-PRELIMINARES.md` (**no son dictamen**)  
6. Capturas del flujo mock (si se entregan por canal seguro)

---

## 4. Decisiones que pedimos por área

### Jurídico / electoral
- Viabilidad legal del cobro online de aportes voluntarios.
- Textos/avisos mínimos obligatorios en UI.
- Restricciones a aportantes (origen de fondos, extranjeros, montos, etc.).
- Relación con campaña electoral vs período ordinario (si aplica distinto).
- Uso de PSP privado vs cuenta bancaria del partido.

### Impositivo / contable
- Tratamiento del aporte (donación / otro).
- Obligaciones de factura / comprobante / retención.
- CUIT / condición frente a IVA / Ganancias del receptor.
- Reportes periódicos recomendados.

### Tesorería / gobernanza interna
- Cuenta receptora autorizada.
- Quién aprueba campañas de incentivo (`CampaignRule`).
- Flujo de conciliación y auditoría.
- Política de reembolsos.

### Datos personales
- Base legal del tratamiento.
- Texto de privacidad / consentimiento.
- Residencia de datos (PSP + hosting).
- Conservación y acceso.

---

## 5. Condiciones técnicas que el dictamen puede asumir

1. No se habilita cobro sin `payments_enabled=true` + secretos fuera de git.  
2. Webhooks firman / validan origen PSP.  
3. Estados: `created → pending → authorized|rejected|refunded|failed`.  
4. UI no promete beneficios políticos.  
5. Logs sin PAN/CVV; tokens PSP no se versionan.  
6. Entidad LLA aislada de Nortiqa Lab / otras entidades.  

---

## 6. Formato de respuesta sugerido

```text
DICTAMEN G1 — Aportes LLA SC
Fecha:
Autores / firmas:
Conclusión: VIABLE CON CONDICIONES | NO VIABLE | VIABLE SIN CONDICIONES
Condiciones (lista numerada):
Respuestas a G1-PREGUNTAS (por ítem):
Textos legales a publicar (adjuntos o referencias):
Bloqueos absolutos (si hay):
Próxima revisión recomendada:
```

---

## 7. Contacto técnico

Canal: Giovany / equipo técnico autorizado.  
No enviar secretos de PSP por este dossier; usar canal seguro de tesorería.
