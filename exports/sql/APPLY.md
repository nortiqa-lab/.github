# APPLY — SQL inventory/tasks (staging only)

**Do not run against production without Gio + OPS.**

```bash
psql "$DATABASE_URL" -f migrations/003_nl_agentes_tareas.sql
psql "$DATABASE_URL" -f seed/001_nl_agentes_tareas_seed.sql
```

Verify:
```sql
SELECT agent_id, status, maturity_q, git_manifest_path FROM nl_agentes_inventario ORDER BY agent_id;
SELECT task_id, status, title FROM nl_tareas;
```

Rollback (staging only):
```sql
DROP TABLE IF EXISTS nl_tareas;
DROP TABLE IF EXISTS nl_agentes_inventario;
```
