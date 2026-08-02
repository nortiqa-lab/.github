#!/usr/bin/env python3
"""F3 treasury/receipts API tests (starts server subprocess)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "api" / "server.py"
DB = ROOT / "var" / "aportes-f3-test.sqlite3"
PORT = 8792
BASE = f"http://127.0.0.1:{PORT}"


def http(method: str, path: str, data: dict | None = None) -> tuple[int, dict | str]:
    body = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as res:
            raw = res.read().decode("utf-8")
            ctype = res.headers.get("Content-Type", "")
            if "application/json" in ctype:
                return res.status, json.loads(raw)
            return res.status, raw
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8")
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            parsed = {"raw": payload}
        return exc.code, parsed


def main() -> int:
    if DB.exists():
        DB.unlink()
    env = {
        **os.environ,
        "LLA_APORTES_DB": str(DB),
        "PYTHONPATH": str(ROOT / "api") + os.pathsep + str(ROOT / "tools"),
    }
    proc = subprocess.Popen(
        [sys.executable, str(API), "--port", str(PORT)],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )
    failed = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal failed
        print(("OK" if cond else "FAIL") + ":", msg)
        if not cond:
            failed += 1

    try:
        for _ in range(40):
            try:
                code, health = http("GET", "/health")
                if code == 200:
                    break
            except Exception:
                time.sleep(0.1)
        else:
            print("FAIL: server did not start")
            print(proc.stdout.read() if proc.stdout else "")
            return 1

        check(isinstance(health, dict) and health.get("payments_enabled") is False, "health still disabled")
        check(isinstance(health, dict) and "f3_treasury" in (health.get("features") or []), "f3 feature flag")

        code, intent = http(
            "POST",
            "/v1/intents",
            {
                "name": "Tesorería Test",
                "email": "tesoreria@example.com",
                "amount_cents": 160000,
                "destination_id": "territorial:rio-turbio",
                "mode": "one_time",
                "consent": True,
            },
        )
        check(code == 201 and isinstance(intent, dict), "intent for f3")
        assert isinstance(intent, dict)
        lid = intent["ledger_id"]
        rid = intent["receipt_id"]

        code, ledger = http("GET", "/v1/ledger")
        check(code == 200 and isinstance(ledger, dict) and len(ledger.get("ledger") or []) >= 1, "ledger list")

        code, summary = http("GET", "/v1/treasury/summary")
        check(
            code == 200
            and isinstance(summary, dict)
            and summary.get("simulation_only") is True
            and summary.get("pending_reconcile", 0) >= 1,
            "treasury summary pending",
        )

        code, rec = http(
            "POST",
            f"/v1/ledger/{lid}/reconcile",
            {"actor": "tesorero-dev", "note": "conciliación simulación"},
        )
        check(
            code == 200
            and isinstance(rec, dict)
            and rec.get("action") == "reconcile"
            and rec.get("ledger", {}).get("reconciled_by") == "tesorero-dev",
            "reconcile ledger",
        )

        code, summary2 = http("GET", "/v1/treasury/summary")
        check(
            code == 200 and isinstance(summary2, dict) and summary2.get("reconciled", 0) >= 1,
            "treasury summary reconciled",
        )

        code, unrec = http("POST", f"/v1/ledger/{lid}/unreconcile", {"actor": "tesorero-dev"})
        check(code == 200 and isinstance(unrec, dict) and unrec.get("action") == "unreconcile", "unreconcile")

        code, receipt = http("GET", f"/v1/receipts/{rid}")
        check(code == 200 and isinstance(receipt, dict) and receipt.get("receipt", {}).get("id") == rid, "receipt json")

        code, html = http("GET", f"/v1/receipts/{rid}.html")
        check(
            code == 200
            and isinstance(html, str)
            and "SIMULACIÓN" in html
            and intent["receipt_number"] in html,
            "receipt html",
        )

        code, csv_body = http("GET", "/v1/treasury/export.csv")
        check(
            code == 200
            and isinstance(csv_body, str)
            and "ledger_id" in csv_body
            and "simulation" in csv_body
            and lid in csv_body,
            "treasury csv export",
        )

        code, checkout = http("POST", "/v1/checkout", {"intent_id": intent.get("intent_id")})
        check(code == 409, "checkout still blocked in f3")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
