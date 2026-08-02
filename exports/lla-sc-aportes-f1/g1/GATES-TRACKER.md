# Tracker gates G1–G8 — Aportes LLA SC

Estado: DEV / Borrador  
Fecha: 2026-08-02  
Regla: **ningún gate en verde implica cobros reales** hasta que G1–G8 estén verdes y `payments_enabled` se active con autorización explícita.

Leyenda: `🔴` bloqueado · `🟡` en curso / parcial · `🟢` cerrado con evidencia · `⚪` no iniciado

---

## Resumen

| Gate | Tema | Estado | Owner | Evidencia |
|------|------|--------|-------|-----------|
| G1 | Dictamen electoral+contable+fiscal+datos | 🟡 | Asesores / Gio | Dossier `g1/` listo; **falta dictamen firmado** |
| G2 | Personería / facultades distrito SC | ⚪ | Conducción / tesorería | — |
| G3 | Cuenta bancaria partidaria + responsable económico | ⚪ | Tesorería | — |
| G4 | Política aportantes permitidos/prohibidos | ⚪ | Legal | — |
| G5 | Términos + privacidad + consentimiento | 🟡 | Legal + producto | Solo `legal/DRAFT-*.md` (no aprobados) |
| G6 | Calificación aporte vs servicio (niveles/campañas) | 🟡 | Legal | Diseño “aporte puro” propuesto; sin dictamen |
| G7 | Staging PSP (plata de prueba) | 🔴 | Tech | Bloqueado hasta G1 (+ condiciones) |
| G8 | Ratificación Gio go-live | 🔴 | Gio | Bloqueado hasta G1–G7 |

---

## Detalle G1

| Ítem | Estado | Nota |
|------|--------|------|
| Dossier armado | 🟢 | `g1/G1-DOSSIER.md` |
| Carta solicitud | 🟢 | `g1/G1-SOLICITUD-DICTAMEN.md` |
| Matriz preguntas | 🟢 | `g1/G1-PREGUNTAS.md` |
| Hallazgos investigación | 🟢 | `g1/G1-HALLAZGOS-PRELIMINARES.md` (no dictamen) |
| Checklist operativo | 🟢 | `../G1-CHECKLIST.md` |
| Entrega a asesores | ⚪ | Acción Gio / conducción |
| Respuestas escritas | ⚪ | — |
| Conclusión aprobar/condicionar/rechazar | ⚪ | Cierra G1 |
| Textos UI mínimos fijados | ⚪ | Condiciona G5 |

**Criterio verde G1:** documento escrito con conclusión + respuestas a preguntas clave + autorización (o condiciones) para avanzar a sandbox (G7).

---

## Detalle técnico paralelo (no sustituye gates)

| Pieza | Estado |
|-------|--------|
| ARCH pagos | 🟢 DEV publicado |
| F1 mock `/aportar` | 🟢 simulación |
| F2 API + MP stub | 🟢 `payments_enabled=false` hard stop |
| CampaignRules self-test | 🟢 |
| Secretos PSP en git | 🟢 ausentes (correcto) |
| Cobro real / sandbox MP | 🔴 no iniciado |

---

## Log de cambios de estado

| Fecha | Gate | De → A | Nota |
|-------|------|--------|------|
| 2026-08-02 | G1 | ⚪ → 🟡 | Dossier técnico entregable listo; pendiente asesores |
| 2026-08-02 | G5 | ⚪ → 🟡 | Drafts legales creados, no aprobados |
| 2026-08-02 | G6 | ⚪ → 🟡 | Calificación propuesta en ARCH; sin dictamen |
| 2026-08-02 | G7/G8 | — → 🔴 | Explícitamente bloqueados |

---

## Próxima acción humana

1. Gio entrega `g1/` (+ `legal/DRAFT-*`) a asesores.  
2. Asesores completan `G1-PREGUNTAS.md` y firman conclusión.  
3. Actualizar este tracker a 🟢 G1 (o listar condiciones).  
4. Solo entonces planificar G7 (sandbox MP) sin tocar producción.
