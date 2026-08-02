#!/usr/bin/env python3
"""F2 DEV API for LLA SC aportes — stdlib only, simulation-first."""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from campaign_rules import evaluate, load_json, validate_intent_amount  # noqa: E402
from db import (  # noqa: E402
    connect,
    create_intent,
    create_mandate,
    list_receipts,
    update_mandate_status,
)
from mp_adapter import MercadoPagoAdapter  # noqa: E402

CONFIG = load_json(ROOT / "config" / "app.json")
CAMPAIGNS = load_json(ROOT / "data" / "campaigns.json")
DESTINATIONS = load_json(ROOT / "data" / "destinations.json")


def json_bytes(data: dict | list, code: int = 200) -> tuple[int, bytes]:
    return code, json.dumps(data, ensure_ascii=False).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "LLA-SC-Aportes-F2/0.2"

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send(self, code: int, body: bytes, content_type: str = "application/json") -> None:
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send(204, b"")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/health"}:
            code, body = json_bytes(
                {
                    "ok": True,
                    "service": "lla-sc-aportes-f2",
                    "payments_enabled": bool(CONFIG.get("payments_enabled")),
                    "psp_mode": (CONFIG.get("psp") or {}).get("mode"),
                }
            )
            return self._send(code, body)
        if path == "/v1/campaigns/active":
            qs = parse_qs(urlparse(self.path).query)
            destination = (qs.get("destination") or [None])[0]
            now = (qs.get("now") or [None])[0]
            return self._send(*json_bytes(evaluate(CAMPAIGNS, now=now, destination_id=destination)))
        if path == "/v1/destinations":
            visible = [
                d
                for d in DESTINATIONS.get("destinations") or []
                if d.get("ui_visible") is not False and not d.get("electoral_circuit")
            ]
            return self._send(*json_bytes({"destinations": visible}))
        if path == "/v1/receipts":
            with connect() as conn:
                return self._send(*json_bytes({"receipts": list_receipts(conn)}))
        if path == "/v1/config":
            safe = {
                "payments_enabled": CONFIG.get("payments_enabled"),
                "currency": CONFIG.get("currency"),
                "disclaimer": CONFIG.get("disclaimer"),
                "psp": {
                    "primary": (CONFIG.get("psp") or {}).get("primary"),
                    "mode": (CONFIG.get("psp") or {}).get("mode"),
                },
            }
            return self._send(*json_bytes(safe))
        self._send(*json_bytes({"error": "not_found", "path": path}, 404))

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
        except json.JSONDecodeError:
            return self._send(*json_bytes({"error": "invalid_json"}, 400))

        if path == "/v1/intents":
            return self._create_intent(payload)
        if path == "/v1/mandates":
            return self._create_mandate(payload)
        if path.startswith("/v1/mandates/") and path.endswith("/pause"):
            mid = path.split("/")[3]
            return self._mandate_status(mid, "paused")
        if path.startswith("/v1/mandates/") and path.endswith("/cancel"):
            mid = path.split("/")[3]
            return self._mandate_status(mid, "cancelled")
        if path == "/v1/checkout":
            return self._checkout(payload)
        if path == "/v1/webhooks/mercadopago":
            return self._webhook(payload)
        self._send(*json_bytes({"error": "not_found", "path": path}, 404))

    def _create_intent(self, payload: dict) -> None:
        required = ["name", "email", "amount_cents", "destination_id", "mode"]
        missing = [k for k in required if k not in payload]
        if missing:
            return self._send(*json_bytes({"error": "missing_fields", "fields": missing}, 400))
        ev = evaluate(CAMPAIGNS, destination_id=payload.get("destination_id"))
        validation = validate_intent_amount(int(payload["amount_cents"]), ev)
        if not validation["ok"]:
            return self._send(*json_bytes({"error": "invalid_amount", **validation}, 400))
        if not payload.get("consent"):
            return self._send(*json_bytes({"error": "consent_required"}, 400))
        payload = {
            **payload,
            "campaign_ids": ev.get("applied_campaign_ids") or [],
            "amount_before_campaign_cents": (ev.get("suggested_base_cents") or [None])[0],
            "currency": ev.get("currency", "ARS"),
        }
        with connect() as conn:
            result = create_intent(conn, payload)
        result["payments_enabled"] = bool(CONFIG.get("payments_enabled"))
        result["checkout_allowed"] = False
        result["evaluation"] = {
            "display_amounts_cents": ev["display_amounts_cents"],
            "applied_campaign_ids": ev["applied_campaign_ids"],
        }
        self._send(*json_bytes(result, 201))

    def _create_mandate(self, payload: dict) -> None:
        required = ["name", "email", "amount_cents", "destination_id"]
        missing = [k for k in required if k not in payload]
        if missing:
            return self._send(*json_bytes({"error": "missing_fields", "fields": missing}, 400))
        if not payload.get("consent"):
            return self._send(*json_bytes({"error": "consent_required"}, 400))
        ev = evaluate(CAMPAIGNS, destination_id=payload.get("destination_id"))
        validation = validate_intent_amount(int(payload["amount_cents"]), ev)
        if not validation["ok"]:
            return self._send(*json_bytes({"error": "invalid_amount", **validation}, 400))
        with connect() as conn:
            result = create_mandate(conn, payload)
        result["payments_enabled"] = False
        result["psp_subscription_created"] = False
        self._send(*json_bytes(result, 201))

    def _mandate_status(self, mandate_id: str, status: str) -> None:
        try:
            with connect() as conn:
                result = update_mandate_status(conn, mandate_id, status)
        except KeyError:
            return self._send(*json_bytes({"error": "mandate_not_found"}, 404))
        except ValueError as exc:
            return self._send(*json_bytes({"error": str(exc)}, 400))
        self._send(*json_bytes({"mandate": result}))

    def _checkout(self, payload: dict) -> None:
        adapter = MercadoPagoAdapter(CONFIG)
        intent = {"id": payload.get("intent_id"), "amount_cents": payload.get("amount_cents")}
        result = adapter.create_checkout(intent)
        code = 409 if not result.ok else 200
        self._send(
            *json_bytes(
                {
                    "ok": result.ok,
                    "mode": result.mode,
                    "message": result.message,
                    "psp_ref": result.psp_ref,
                    "checkout_url": result.checkout_url,
                    "details": result.details,
                },
                code,
            )
        )

    def _webhook(self, payload: dict) -> None:
        adapter = MercadoPagoAdapter(CONFIG)
        result = adapter.handle_webhook(payload)
        # Acknowledge without mutating money state while disabled
        self._send(
            *json_bytes(
                {
                    "ok": False,
                    "ignored": True,
                    "mode": result.mode,
                    "message": result.message,
                },
                202,
            )
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args(argv)
    if CONFIG.get("payments_enabled"):
        print("REFUSING TO START: payments_enabled must be false in this DEV package", file=sys.stderr)
        return 2
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"LLA SC aportes F2 API on http://{args.host}:{args.port} (payments_enabled=false)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nshutdown")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
