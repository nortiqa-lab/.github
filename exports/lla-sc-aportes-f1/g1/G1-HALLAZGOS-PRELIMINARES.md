# Hallazgos preliminares — G1 (no es dictamen)

Estado: DEV / Borrador  
Fecha: 2026-08-02  
Fuente primaria: Notion — [Investigación financiamiento partidario LLA SC](https://app.notion.com/p/3ade4fe3bfea8131a603e817cee62d63) (2026-07-30)  
Fuentes secundarias: `ARCH-LLA-SC-PAYMENTS-001`, `PROD-NQ-COMUNIDAD-POLITICA-001`

```text
ADVERTENCIA
Este documento solo distila hechos e inferencias de investigación previa.
NO sustituye dictamen electoral, contable, fiscal ni de datos personales.
NO autoriza cobros. NO es opinión jurídica vinculante.
```

---

## 1. Distinción

| Tipo | Contenido |
|------|-----------|
| **Hecho** | Existe página de investigación (estado: investigación jurídica en curso) con conclusiones preliminares y decisión provisional de no lanzar cobros recurrentes todavía. |
| **Hecho** | El diseño técnico F1/F2 opera con `payments_enabled=false` y no procesa medios reales. |
| **Inferencia** | Un aporte voluntario sin beneficios reduce el riesgo de recalificación comercial respecto de una “suscripción con niveles”, pero sigue requiriendo dictamen. |
| **Recomendación** | Entregar este dossier a asesores y cerrar G1 por escrito antes de G7/G8. |

---

## 2. Conclusiones preliminares confirmadas (investigación)

Destilado fiel de la página Notion (no reinterpretado como ley):

1. La Ley 26.215 contempla financiamiento privado (aportes periódicos, donaciones, etc.), sujeto a régimen aplicable y controles.
2. Cobro recurrente **con beneficios concretos** eleva riesgo de recalificación como prestación de servicios.
3. Origen, identidad, trazabilidad y destino de fondos son centrales; no debería aceptarse dinero anónimo ni cuentas personales ajenas al partido.
4. Personería nacional ≠ autorización automática para que cualquier estructura provincial cobre sin distrito / tesorero / autoridades competentes.
5. Debe separarse financiamiento institucional vs campaña electoral.
6. Pagos/gastos por instrumentos y cuentas habilitadas, con documentación y responsables.
7. Una “suscripción” no es donación por decreto: la calificación depende de la contraprestación.
8. Datos de opinión/afiliación política = datos sensibles → consentimiento expreso, minimización, seguridad, ARCO.
9. Separar en entidad vinculada no elimina reglas de aportantes, trazabilidad, límites y prohibiciones.
10. **Antes del primer cobro:** dictamen escrito conjunto electoral + contable + fiscal + datos.

---

## 3. Riesgos principales (investigación)

| Riesgo | Mitigación técnica ya prevista (DEV) | Pendiente asesor |
|--------|--------------------------------------|------------------|
| Cuenta no autorizada / personal | No se configuran cuentas en repo; gate G3 | Titularidad real |
| Aportantes prohibidos / anónimos | Modelo person + flags; KYC-lite fase2 | Política G4 |
| Confusión comercial vs aporte | Sin merch/beneficios en MVP; CampaignRules solo montos | Calificación G6 |
| Fondos institucionales en campaña | Destination `electoral` separado en modelo; oculto UI MVP | Circuito contable |
| Datos sensibles indebidos | Consent drafts; aislamiento entidad | Textos G5 |
| Influencia / acceso por dinero | Hard stop producto + disclaimer | Confirmación legal K1 |

---

## 4. Fuentes normativas base citadas (investigación)

- Ley 26.215 (financiamiento partidos políticos)
- Ley 27.504 (reforma financiamiento)
- Decreto 936/2010 (reglamentación parcial)
- Ley 25.326 (datos personales)
- Normativa / acordadas Cámara Nacional Electoral (rendiciones y aportes)

**Pendiente de asesores:** matriz artículo por artículo; lista actualizada de aportantes prohibidos y límites; dictamen IVA/Ganancias/IIBB.

---

## 5. Decisión provisional de la investigación (hecho)

> **No lanzar cobros recurrentes todavía.**  
> Viable en términos generales, pero la arquitectura concreta debe definirse antes de medios de pago, niveles de beneficios o entidad operadora.

El paquete F1/F2 alinea con esa decisión: mock + API stub, sin PSP real.

---

## 6. Cómo el diseño actual responde (inferencia técnica)

| Hallazgo investigación | Respuesta de ARCH / F1–F2 |
|------------------------|---------------------------|
| Evitar beneficios que recalifiquen | MVP = aporte puro; sin membresía premium |
| Dictamen previo al cobro | Gates G1–G8; `payments_enabled=false` hard stop |
| Cuenta partidaria | G3; no secretos en git |
| Trazabilidad | Intent → Ledger → Receipt (modelo + SQLite DEV) |
| Datos sensibles | Drafts consentimiento/privacidad (no aprobados) |
| Separación campaña | Destination electoral modelado, no expuesto MVP |
| “Descuentos” riesgosos | Reencuadrados como `CampaignRule` de montos sugeridos |

---

## 7. Entregables aún abiertos (investigación)

- [ ] Matriz artículo por artículo Ley 26.215 / modificatorias  
- [ ] Lista aportantes permitidos / prohibidos / límites  
- [ ] Dictamen fiscal IVA / Ganancias / IIBB  
- [ ] Comparación estructuras: partido directo / entidad vinculada / híbrido  
- [ ] Flujo alta → cobro → validación → registración → devolución → rendición (legal)  
- [ ] Auditoría “abogado del diablo” pre-MVP  

Estos ítems alimentan el cierre de G1; el tech kit no los completa solo.

---

## 8. Qué pedir ahora a los asesores

Usar `G1-SOLICITUD-DICTAMEN.md` + responder `G1-PREGUNTAS.md` con conclusión:

`VIABLE CON CONDICIONES | NO VIABLE | VIABLE SIN CONDICIONES`
