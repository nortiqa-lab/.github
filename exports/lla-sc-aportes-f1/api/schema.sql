PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS persons (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  consent_at TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS intents (
  id TEXT PRIMARY KEY,
  person_id TEXT NOT NULL,
  mode TEXT NOT NULL CHECK(mode IN ('one_time','recurring')),
  amount_cents INTEGER NOT NULL,
  amount_before_campaign_cents INTEGER,
  currency TEXT NOT NULL DEFAULT 'ARS',
  destination_id TEXT NOT NULL,
  campaign_ids_json TEXT NOT NULL DEFAULT '[]',
  status TEXT NOT NULL,
  psp_ref TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(person_id) REFERENCES persons(id)
);

CREATE TABLE IF NOT EXISTS mandates (
  id TEXT PRIMARY KEY,
  person_id TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'ARS',
  destination_id TEXT NOT NULL,
  period TEXT NOT NULL DEFAULT 'monthly',
  status TEXT NOT NULL CHECK(status IN ('proposed','consented','active','paused','cancelled')),
  next_charge_at TEXT,
  psp_ref TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(person_id) REFERENCES persons(id)
);

CREATE TABLE IF NOT EXISTS ledger (
  id TEXT PRIMARY KEY,
  intent_id TEXT,
  mandate_id TEXT,
  amount_gross_cents INTEGER NOT NULL,
  amount_net_cents INTEGER NOT NULL,
  fees_cents INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL,
  psp_payment_id TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS receipts (
  id TEXT PRIMARY KEY,
  ledger_id TEXT NOT NULL,
  number TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  issued_at TEXT NOT NULL,
  FOREIGN KEY(ledger_id) REFERENCES ledger(id)
);

CREATE TABLE IF NOT EXISTS webhook_events (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  event_id TEXT,
  payload_json TEXT NOT NULL,
  processed_at TEXT NOT NULL,
  result TEXT NOT NULL
);
