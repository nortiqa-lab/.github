#!/usr/bin/env python3
"""Self-contained F2 API tests (starts server subprocess)."""

from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "api" / "server.py"
DB = ROOT / "var" / "aportes-f2-test.sqlite3"
PORT = 8791
BASE = f"http://127.0.0.1:{PORT}"


def http(method: str, path: str, data: dict | None = None) -> tuple[int, dict]:
    body = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as res:
            return res.status, json.loads(res.read().decode("utf-8"))
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
    import os

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

        check(health.get("payments_enabled") is False, "health payments_enabled false")

        code, camps = http("GET", "/v1/campaigns/active?now=2026-08-15&destination=territorial:rio-turbio")
        check(code == 200 and camps.get("simulation_only") is True, "campaigns active simulation")
        check("camp_2026_ago_solidario" in camps.get("applied_campaign_ids", []), "august campaign")

        code, bad = http(
            "POST",
            "/v1/intents",
            {
                "name": "Test",
                "email": "t@example.com",
                "amount_cents": 50000,
                "destination_id": "general",
                "mode": "one_time",
                "consent": True,
            },
        )
        check(code == 400 and bad.get("error") == "invalid_amount", "rejects below floor")

        code, intent = http(
            "POST",
            "/v1/intents",
            {
                "name": "Test Gio",
                "email": "gio.test@example.com",
                "amount_cents": 160000,
                "destination_id": "territorial:rio-turbio",
                "mode": "one_time",
                "consent": True,
            },
        )
        check(code == 201 and intent.get("status") == "simulated_authorized", "creates simulated intent")
        check(intent.get("checkout_allowed") is False, "checkout not allowed")

        code, checkout = http("POST", "/v1/checkout", {"intent_id": intent.get("intent_id"), "amount_cents": 160000})
        check(code == 409 and checkout.get("ok") is False, "checkout blocked")

        code, mandate = http(
            "POST",
            "/v1/mandates",
            {
                "name": "Test Gio",
                "email": "gio.test@example.com",
                "amount_cents": 160000,
                "destination_id": "general",
                "consent": True,
            },
        )
        check(code == 201 and mandate.get("psp_subscription_created") is False, "mandate without PSP")

        mid = mandate["mandate_id"]
        code, paused = http("POST", f"/v1/mandates/{mid}/pause", {})
        check(code == 200 and paused.get("mandate", {}).get("status") == "paused", "pause mandate")

        code, cancelled = http("POST", f"/v1/mandates/{mid}/cancel", {})
        check(code == 200 and cancelled.get("mandate", {}).get("status") == "cancelled", "cancel mandate")

        code, receipts = http("GET", "/v1/receipts")
        check(code == 200 and len(receipts.get("receipts") or []) >= 1, "receipts listed")

        code, wh = http("POST", "/v1/webhooks/mercadopago", {"type": "payment", "data": {"id": "x"}})
        check(code == 202 and wh.get("ignored") is True, "webhook ignored while disabled")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
