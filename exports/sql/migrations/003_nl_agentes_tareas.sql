-- DEV seed schema — DO NOT apply to PROD without Gio + OPS
-- Target: PostgreSQL 16 sc2027-staging-db (per REG-NL-SESSION-20260619-001)

BEGIN;

CREATE TABLE IF NOT EXISTS nl_agentes_inventario (
  agent_id          TEXT PRIMARY KEY,
  name              TEXT NOT NULL,
  role_or_function  TEXT,
  family            TEXT,
  entity_id         TEXT NOT NULL DEFAULT 'nortiqa-lab',
  status            TEXT NOT NULL,
  maturity_q        TEXT CHECK (maturity_q IS NULL OR maturity_q IN ('Q0','Q1','Q2','Q3','Q4','Q5')),
  autonomy_level    TEXT,
  owner             TEXT,
  git_manifest_path TEXT,
  notion_url        TEXT,
  version           TEXT,
  last_test_at      TIMESTAMPTZ,
  last_test_result  TEXT,
  notes             TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS nl_tareas (
  task_id           TEXT PRIMARY KEY,
  title             TEXT NOT NULL,
  entity_id         TEXT NOT NULL DEFAULT 'nortiqa-lab',
  status            TEXT NOT NULL DEFAULT 'backlog',
  priority          INT DEFAULT 3,
  assignee          TEXT,
  related_agent_id  TEXT REFERENCES nl_agentes_inventario(agent_id),
  notion_url        TEXT,
  git_pr_url        TEXT,
  due_at            TIMESTAMPTZ,
  definition_of_done TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  closed_at         TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_nl_agentes_entity ON nl_agentes_inventario(entity_id);
CREATE INDEX IF NOT EXISTS idx_nl_agentes_status ON nl_agentes_inventario(status);
CREATE INDEX IF NOT EXISTS idx_nl_tareas_entity ON nl_tareas(entity_id);
CREATE INDEX IF NOT EXISTS idx_nl_tareas_status ON nl_tareas(status);

COMMIT;
