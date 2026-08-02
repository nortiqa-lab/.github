#!/usr/bin/env python3
"""CampaignRules engine for LLA SC aportes F1 (DEV / simulation)."""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "campaigns.json"
CONFIG = ROOT / "config" / "app.json"

ALLOWED_LEGAL = frozenset({"approved_for_staging", "approved_for_prod"})


def parse_day(value: str | date | datetime | None) -> date:
    if value is None:
        return date.today()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def active_campaigns(campaigns: list[dict], now: date) -> list[dict]:
    active = []
    for camp in campaigns:
        if camp.get("legal_review_status") not in ALLOWED_LEGAL:
            continue
        start = parse_day(camp["window"]["start"])
        end = parse_day(camp["window"]["end"])
        if start <= now <= end:
            active.append(camp)
    active.sort(key=lambda c: (-int(c.get("priority", 0)), c.get("campaign_id", "")))
    return active


def evaluate(
    catalog: dict | None = None,
    now: str | date | None = None,
    destination_id: str | None = None,
) -> dict:
    catalog = catalog or load_json(DATA)
    config = load_json(CONFIG)
    day = parse_day(now)
    base = list(catalog.get("suggested_base_cents") or [])
    display = list(base)
    labels: list[str] = []
    disclaimers: list[str] = [config.get("disclaimer", "")]
    applied: list[str] = []
    boosted: list[str] = []
    floor = None
    cap = None

    for camp in active_campaigns(catalog.get("campaigns") or [], day):
        rule = camp.get("rule_type")
        params = camp.get("params") or {}
        cid = camp["campaign_id"]

        if rule == "suggested_amount_override":
            display = list(params.get("suggested_base_cents") or display)
            applied.append(cid)
            labels.append(camp.get("title") or cid)
        elif rule == "percent_reduction_on_suggested":
            pct = float(params.get("percent", 0))
            display = [max(0, int(round(v * (1 - pct / 100.0)))) for v in display]
            applied.append(cid)
            labels.append(camp.get("title") or cid)
        elif rule == "amount_floor":
            floor = int(params.get("floor_cents", 0))
            applied.append(cid)
        elif rule == "amount_cap":
            cap = int(params.get("cap_cents", 0))
            applied.append(cid)
        elif rule == "destination_boost":
            dest = params.get("destination_id")
            if dest:
                boosted.append(dest)
                if destination_id == dest:
                    labels.append(camp.get("title") or cid)
                applied.append(cid)
        elif rule == "pause_recurring_promo":
            labels.append(camp.get("title") or cid)
            applied.append(cid)

    if floor is not None:
        display = [max(floor, v) for v in display]
    if cap is not None:
        display = [min(cap, v) for v in display]

    return {
        "as_of": day.isoformat(),
        "payments_enabled": bool(config.get("payments_enabled")),
        "currency": config.get("currency", "ARS"),
        "suggested_base_cents": base,
        "display_amounts_cents": display,
        "labels": labels,
        "disclaimers": [d for d in disclaimers if d],
        "applied_campaign_ids": applied,
        "boosted_destinations": boosted,
        "floor_cents": floor,
        "cap_cents": cap,
        "simulation_only": not bool(config.get("payments_enabled")),
    }


def validate_intent_amount(amount_cents: int, evaluation: dict) -> dict:
    errors = []
    floor = evaluation.get("floor_cents")
    cap = evaluation.get("cap_cents")
    if amount_cents <= 0:
        errors.append("amount_must_be_positive")
    if floor is not None and amount_cents < floor:
        errors.append("below_floor")
    if cap is not None and amount_cents > cap:
        errors.append("above_cap")
    return {
        "ok": not errors,
        "errors": errors,
        "payments_enabled": evaluation.get("payments_enabled"),
        "checkout_allowed": False
        if not evaluation.get("payments_enabled")
        else not errors,
        "mode": "simulation" if not evaluation.get("payments_enabled") else "live",
    }


def self_test() -> int:
    catalog = load_json(DATA)
    # Mid-campaign August
    ev = evaluate(catalog, now="2026-08-15", destination_id="territorial:rio-turbio")
    failed = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal failed
        print(("OK" if cond else "FAIL") + ":", msg)
        if not cond:
            failed += 1

    check(ev["payments_enabled"] is False, "payments_enabled is false")
    check("camp_2026_ago_solidario" in ev["applied_campaign_ids"], "august campaign applied")
    check("camp_pending_legal" not in ev["applied_campaign_ids"], "pending legal ignored")
    # 20% off then floor 1000 ARS = 100000 cents
    expected = [max(100000, int(round(v * 0.8))) for v in catalog["suggested_base_cents"]]
    expected = [min(5000000, v) for v in expected]
    check(ev["display_amounts_cents"] == expected, f"display amounts {ev['display_amounts_cents']} == {expected}")
    check("territorial:rio-turbio" in ev["boosted_destinations"], "turbio boosted")

    # Outside august window — no percent campaign
    ev2 = evaluate(catalog, now="2026-10-01")
    check("camp_2026_ago_solidario" not in ev2["applied_campaign_ids"], "august campaign off in october")

    intent = validate_intent_amount(50000, ev)
    check(intent["ok"] is False and "below_floor" in intent["errors"], "rejects below floor")
    intent2 = validate_intent_amount(200000, ev)
    check(intent2["ok"] is True and intent2["checkout_allowed"] is False, "sim ok but no checkout")

    return failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--now", default=None, help="YYYY-MM-DD")
    parser.add_argument("--destination", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        failed = self_test()
        return 1 if failed else 0
    result = evaluate(now=args.now, destination_id=args.destination)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
