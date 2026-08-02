"""SQLite persistence for LLA aportes F2/F3 DEV API."""

from __future__ import annotations

import csv
import io
import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = Path(__file__).resolve().parent / "schema.sql"
DEFAULT_DB = Path(os.environ.get("LLA_APORTES_DB", str(ROOT / "var" / "aportes-f2.sqlite3")))


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, decl: str) -> None:
    cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


def migrate(conn: sqlite3.Connection) -> None:
    """Idempotent schema upgrades for existing DEV DBs."""
    _ensure_column(conn, "ledger", "reconciled_at", "TEXT")
    _ensure_column(conn, "ledger", "reconciled_by", "TEXT")
    _ensure_column(conn, "ledger", "reconciliation_note", "TEXT")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS reconciliation_events (
          id TEXT PRIMARY KEY,
          ledger_id TEXT NOT NULL,
          action TEXT NOT NULL,
          actor TEXT NOT NULL,
          note TEXT,
          created_at TEXT NOT NULL,
          FOREIGN KEY(ledger_id) REFERENCES ledger(id)
        );
        """
    )


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    migrate(conn)
    return conn


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def upsert_person(conn: sqlite3.Connection, name: str, email: str, consent: bool) -> str:
    if not consent:
        raise ValueError("consent_required")
    row = conn.execute(
        "SELECT id FROM persons WHERE lower(email)=lower(?) LIMIT 1", (email,)
    ).fetchone()
    if row:
        return row["id"]
    pid = new_id("per")
    now = utcnow()
    conn.execute(
        "INSERT INTO persons(id,name,email,consent_at,created_at) VALUES(?,?,?,?,?)",
        (pid, name, email, now, now),
    )
    return pid


def create_intent(conn: sqlite3.Connection, payload: dict) -> dict:
    pid = upsert_person(
        conn,
        payload["name"],
        payload["email"],
        bool(payload.get("consent")),
    )
    iid = new_id("int")
    now = utcnow()
    status = "simulated_authorized"
    conn.execute(
        """
        INSERT INTO intents(
          id, person_id, mode, amount_cents, amount_before_campaign_cents,
          currency, destination_id, campaign_ids_json, status, created_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            iid,
            pid,
            payload["mode"],
            int(payload["amount_cents"]),
            payload.get("amount_before_campaign_cents"),
            payload.get("currency", "ARS"),
            payload["destination_id"],
            json.dumps(payload.get("campaign_ids") or []),
            status,
            now,
        ),
    )
    lid = new_id("led")
    conn.execute(
        """
        INSERT INTO ledger(
          id, intent_id, amount_gross_cents, amount_net_cents, fees_cents,
          status, created_at
        ) VALUES (?,?,?,?,?,?,?)
        """,
        (lid, iid, int(payload["amount_cents"]), int(payload["amount_cents"]), 0, "simulated", now),
    )
    rid = new_id("rcp")
    number = f"SIM-{now[:10].replace('-', '')}-{iid[-6:].upper()}"
    receipt_payload = {
        "intent_id": iid,
        "ledger_id": lid,
        "person_name": payload["name"],
        "person_email": payload["email"],
        "amount_cents": int(payload["amount_cents"]),
        "currency": payload.get("currency", "ARS"),
        "mode": payload["mode"],
        "destination_id": payload["destination_id"],
        "campaign_ids": payload.get("campaign_ids") or [],
        "simulation": True,
        "note": "Simulación F2/F3 — no se debitó dinero",
    }
    conn.execute(
        "INSERT INTO receipts(id, ledger_id, number, payload_json, issued_at) VALUES (?,?,?,?,?)",
        (rid, lid, number, json.dumps(receipt_payload, ensure_ascii=False), now),
    )
    conn.commit()
    return {
        "intent_id": iid,
        "person_id": pid,
        "status": status,
        "receipt_id": rid,
        "receipt_number": number,
        "ledger_id": lid,
        "created_at": now,
    }


def create_mandate(conn: sqlite3.Connection, payload: dict) -> dict:
    pid = upsert_person(
        conn,
        payload["name"],
        payload["email"],
        bool(payload.get("consent")),
    )
    mid = new_id("man")
    now = utcnow()
    conn.execute(
        """
        INSERT INTO mandates(
          id, person_id, amount_cents, currency, destination_id, period,
          status, next_charge_at, created_at, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            mid,
            pid,
            int(payload["amount_cents"]),
            payload.get("currency", "ARS"),
            payload["destination_id"],
            "monthly",
            "consented",
            None,
            now,
            now,
        ),
    )
    conn.commit()
    return {
        "mandate_id": mid,
        "person_id": pid,
        "status": "consented",
        "note": "Mandate stored in DEV DB; no PSP subscription created",
        "created_at": now,
    }


def update_mandate_status(conn: sqlite3.Connection, mandate_id: str, status: str) -> dict:
    if status not in {"active", "paused", "cancelled"}:
        raise ValueError("invalid_status")
    now = utcnow()
    cur = conn.execute(
        "UPDATE mandates SET status=?, updated_at=? WHERE id=?",
        (status, now, mandate_id),
    )
    if cur.rowcount == 0:
        raise KeyError("mandate_not_found")
    conn.commit()
    row = conn.execute("SELECT * FROM mandates WHERE id=?", (mandate_id,)).fetchone()
    return dict(row)


def list_receipts(conn: sqlite3.Connection, limit: int = 50) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM receipts ORDER BY issued_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    out = []
    for r in rows:
        item = dict(r)
        item["payload"] = json.loads(item.pop("payload_json"))
        out.append(item)
    return out


def get_receipt(conn: sqlite3.Connection, receipt_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM receipts WHERE id=?", (receipt_id,)).fetchone()
    if not row:
        return None
    item = dict(row)
    item["payload"] = json.loads(item.pop("payload_json"))
    led = conn.execute("SELECT * FROM ledger WHERE id=?", (item["ledger_id"],)).fetchone()
    item["ledger"] = dict(led) if led else None
    return item


def list_ledger(conn: sqlite3.Connection, limit: int = 100, reconciled: str | None = None) -> list[dict]:
    sql = """
      SELECT
        l.*,
        i.mode AS intent_mode,
        i.destination_id,
        i.status AS intent_status,
        p.name AS person_name,
        p.email AS person_email,
        r.id AS receipt_id,
        r.number AS receipt_number
      FROM ledger l
      LEFT JOIN intents i ON i.id = l.intent_id
      LEFT JOIN persons p ON p.id = i.person_id
      LEFT JOIN receipts r ON r.ledger_id = l.id
    """
    params: list = []
    if reconciled == "yes":
        sql += " WHERE l.reconciled_at IS NOT NULL"
    elif reconciled == "no":
        sql += " WHERE l.reconciled_at IS NULL"
    sql += " ORDER BY l.created_at DESC LIMIT ?"
    params.append(limit)
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


def reconcile_ledger(
    conn: sqlite3.Connection,
    ledger_id: str,
    *,
    actor: str,
    note: str | None = None,
    unreconcile: bool = False,
) -> dict:
    row = conn.execute("SELECT * FROM ledger WHERE id=?", (ledger_id,)).fetchone()
    if not row:
        raise KeyError("ledger_not_found")
    now = utcnow()
    if unreconcile:
        conn.execute(
            """
            UPDATE ledger
            SET reconciled_at=NULL, reconciled_by=NULL, reconciliation_note=NULL
            WHERE id=?
            """,
            (ledger_id,),
        )
        action = "unreconcile"
    else:
        conn.execute(
            """
            UPDATE ledger
            SET reconciled_at=?, reconciled_by=?, reconciliation_note=?
            WHERE id=?
            """,
            (now, actor, note, ledger_id),
        )
        action = "reconcile"
    eid = new_id("rec")
    conn.execute(
        """
        INSERT INTO reconciliation_events(id, ledger_id, action, actor, note, created_at)
        VALUES (?,?,?,?,?,?)
        """,
        (eid, ledger_id, action, actor, note, now),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM ledger WHERE id=?", (ledger_id,)).fetchone()
    return {"ledger": dict(updated), "event_id": eid, "action": action}


def treasury_summary(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        """
        SELECT
          COUNT(*) AS entries,
          COALESCE(SUM(amount_gross_cents), 0) AS gross_cents,
          COALESCE(SUM(amount_net_cents), 0) AS net_cents,
          COALESCE(SUM(fees_cents), 0) AS fees_cents,
          SUM(CASE WHEN reconciled_at IS NULL THEN 1 ELSE 0 END) AS pending_reconcile,
          SUM(CASE WHEN reconciled_at IS NOT NULL THEN 1 ELSE 0 END) AS reconciled
        FROM ledger
        """
    ).fetchone()
    return {
        "simulation_only": True,
        "entries": int(row["entries"] or 0),
        "gross_cents": int(row["gross_cents"] or 0),
        "net_cents": int(row["net_cents"] or 0),
        "fees_cents": int(row["fees_cents"] or 0),
        "pending_reconcile": int(row["pending_reconcile"] or 0),
        "reconciled": int(row["reconciled"] or 0),
        "currency": "ARS",
        "note": "Totales de simulación — no representan dinero real",
    }


def treasury_export_csv(conn: sqlite3.Connection) -> str:
    rows = list_ledger(conn, limit=10000)
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=[
            "ledger_id",
            "created_at",
            "status",
            "amount_gross_cents",
            "amount_net_cents",
            "fees_cents",
            "destination_id",
            "intent_mode",
            "person_name",
            "person_email",
            "receipt_number",
            "reconciled_at",
            "reconciled_by",
            "reconciliation_note",
            "psp_payment_id",
            "simulation",
        ],
        extrasaction="ignore",
    )
    writer.writeheader()
    for r in rows:
        writer.writerow(
            {
                "ledger_id": r.get("id"),
                "created_at": r.get("created_at"),
                "status": r.get("status"),
                "amount_gross_cents": r.get("amount_gross_cents"),
                "amount_net_cents": r.get("amount_net_cents"),
                "fees_cents": r.get("fees_cents"),
                "destination_id": r.get("destination_id"),
                "intent_mode": r.get("intent_mode"),
                "person_name": r.get("person_name"),
                "person_email": r.get("person_email"),
                "receipt_number": r.get("receipt_number"),
                "reconciled_at": r.get("reconciled_at") or "",
                "reconciled_by": r.get("reconciled_by") or "",
                "reconciliation_note": r.get("reconciliation_note") or "",
                "psp_payment_id": r.get("psp_payment_id") or "",
                "simulation": "true",
            }
        )
    return buf.getvalue()


def render_receipt_html(receipt: dict, entity_label: str = "LLA Santa Cruz") -> str:
    payload = receipt.get("payload") or {}
    amount_cents = int(payload.get("amount_cents") or 0)
    amount = f"$ {amount_cents / 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ledger = receipt.get("ledger") or {}
    reconciled = ledger.get("reconciled_at") or "—"
    return f"""<!doctype html>
<html lang="es-AR">
<head>
  <meta charset="utf-8" />
  <title>Comprobante {receipt.get("number")}</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 640px; margin: 2rem auto; color: #14212b; }}
    .banner {{ background: #8a4b12; color: #fff; padding: .6rem 1rem; border-radius: 8px; }}
    h1 {{ font-size: 1.4rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    td {{ padding: .4rem 0; border-bottom: 1px solid #ddd; vertical-align: top; }}
    td:first-child {{ color: #556; width: 40%; }}
    .muted {{ color: #666; font-size: .9rem; }}
  </style>
</head>
<body>
  <div class="banner">SIMULACIÓN — no es comprobante fiscal ni débito real</div>
  <h1>Comprobante de aporte — {entity_label}</h1>
  <p class="muted">Borrador DEV. Sujeto a dictamen G1 y procedimientos de tesorería.</p>
  <table>
    <tr><td>Número</td><td>{receipt.get("number")}</td></tr>
    <tr><td>Emitido</td><td>{receipt.get("issued_at")}</td></tr>
    <tr><td>Aportante</td><td>{payload.get("person_name", "—")}</td></tr>
    <tr><td>Email</td><td>{payload.get("person_email", "—")}</td></tr>
    <tr><td>Monto</td><td>{amount} {payload.get("currency", "ARS")}</td></tr>
    <tr><td>Modalidad</td><td>{payload.get("mode", "—")}</td></tr>
    <tr><td>Destino</td><td>{payload.get("destination_id", "—")}</td></tr>
    <tr><td>Intent</td><td>{payload.get("intent_id", "—")}</td></tr>
    <tr><td>Ledger</td><td>{payload.get("ledger_id", receipt.get("ledger_id"))}</td></tr>
    <tr><td>Conciliado</td><td>{reconciled}</td></tr>
  </table>
  <p class="muted">{payload.get("note", "")}</p>
</body>
</html>
"""
