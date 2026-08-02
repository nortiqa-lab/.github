# Jerarquía final propuesta — home NORTIQA

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Fecha: 2026-08-02  
Baseline: home vivo WP tema `nortiqa-lab` (CSS ver ~0.5.4 / header 0.5.1)

## Lectura adversarial (post-pasada)

| Criterio | Antes (vivo) | Después (este paquete) |
|----------|--------------|------------------------|
| Ruido “demo/MVP/prototipo” | Alto en badges y roadmap | Bajo; “en preparación” / piloto |
| Credibilidad institucional | Media-alta | Más alta, sin gritar borrador |
| Separación pública / interna | Implícita | Explícita (`data-layer` + nota arquitectura) |
| NORTIQA como firma | Nav + footer + Nortiqa OS en strip | Firma técnica; no segundo héroe |
| Hero budget | Strip de 5 capacidades en 1er viewport | Strip movido a Enfoque |

## Orden de secciones

1. **Hero** — Una composición: firma NORTIQA (header), un headline, un lead, un CTA primario + enlace secundario quieto, plano visual emergente. Eyebrow: `Capa pública · En preparación`.
2. **01 Enfoque** — Una tesis. Principios. Strip de líneas de trabajo (post-hero).
3. **02 Capacidades** — Contenido demostrativo público; estados calmados (PILOTO / EN PREPARACIÓN / MODULAR).
4. **03 Método** — Proceso antes que IA; paso 03 renombrado a “Primera versión usable”.
5. **04 Arquitectura** — Capa interna; NQ CORE como firma técnica.
6. **05 Aplicaciones** — Cinco verticales, una frase cada una.
7. **06 Hoja de ruta** — “De la preparación al despliegue”; etapa actual sin MVP/prototipo.
8. **07 Conversemos** — CTA único claro + mail.
9. **Footer** — Firma NORTIQA + marcador de capa pública.

## Qué no va en el primer viewport

- Filas de capacidades / stats
- Badges de producto
- Roadmap o partners
- Explicaciones de “esto es un prototipo”

## Decisión pendiente (Gio)

Si la capa pública debe inclinarse **más producto/operación** (catálogo, CTAs de tool),
reabrir sección 02 y el strip; hoy queda subordinada a la lectura institucional.
