"""SQLite persistence for LLA aportes F2 DEV API."""

from __future__ import annotations

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


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
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
        INSERT INTO ledger(id, intent_id, amount_gross_cents, amount_net_cents, fees_cents, status, created_at)
        VALUES (?,?,?,?,?,?,?)
        """,
        (lid, iid, int(payload["amount_cents"]), int(payload["amount_cents"]), 0, "simulated", now),
    )
    rid = new_id("rcp")
    number = f"SIM-{now[:10].replace('-', '')}-{iid[-6:].upper()}"
    receipt_payload = {
        "intent_id": iid,
        "amount_cents": int(payload["amount_cents"]),
        "mode": payload["mode"],
        "destination_id": payload["destination_id"],
        "note": "Simulación F2 — no se debitó dinero",
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


def list_receipts(conn: sqlite3.Connection, limit: int = 20) -> list[dict]:
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
