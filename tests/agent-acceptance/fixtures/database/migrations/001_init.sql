-- Acceptance-only migration (SQLite fixture)
CREATE TABLE IF NOT EXISTS acceptance_items (
  id INTEGER PRIMARY KEY,
  label TEXT NOT NULL
);
INSERT INTO acceptance_items (id, label) VALUES (1, 'fixture-ok');
