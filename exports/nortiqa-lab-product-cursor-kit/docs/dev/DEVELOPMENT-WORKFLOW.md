# Development Workflow — product/ops repo

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

```text
Solicitud → diagnóstico → inspección → propuesta → implementación mínima
→ pruebas → revisión → auditoría → ratificación → eventual PROD
```

OPS promote path: follow `server-ops/sc2027/promote-staging-to-prod.md` only with gates (`NL-OPS` + Gio).

## Visión de plataforma (DEV)

Mirrored from org kit: [`NORTIQA-VANGUARD.md`](./NORTIQA-VANGUARD.md) · [`GEN5-MISSION-CONTROL.md`](./GEN5-MISSION-CONTROL.md) · [`GEN5-MISSION-COMPILER-DRY-RUN.md`](./GEN5-MISSION-COMPILER-DRY-RUN.md).

```bash
python3 tools/mission-compiler/compile.py --self-test
```
