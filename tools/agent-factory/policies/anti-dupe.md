# Política anti-duplicación — Agent Factory

Estado: DEV / Borrador

## Regla

Antes de crear un agente, workflow o ejecutor nuevo:

1. Normalizar el pedido (minúsculas, sin signos).
2. Buscar en `inventory/seed.json` por `id`, `name`, `aliases`.
3. Si hay match con `decision` ∈ {`reuse`, `evaluate_merge`, `integrate_later`}:
   - **BLOQUEAR** creación paralela.
   - Proponer reutilizar o consolidar el componente existente.
4. Si `decision` = `pilot` y el pedido coincide con el piloto autorizado: permitir solo ese paquete.
5. Si no hay match: continuar ciclo Factory (diseño → ensamble → test → auditoría).

## Salida obligatoria

```text
status: BLOCKED_DUPLICATE | ALLOW_NEW | ALLOW_PILOT
matched_ids: [...]
recommendation: reuse | merge | create
```
