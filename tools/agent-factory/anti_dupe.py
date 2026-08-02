#!/usr/bin/env python3
"""Anti-duplication checker for SYS-NL-AGENT-FACTORY-001 (DEV)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "inventory" / "seed.json"

# Too generic alone — must pair with a specific token to count as a match.
GENERIC_TOKENS = frozenset(
    {
        "agente",
        "agent",
        "agents",
        "agentes",
        "bot",
        "nuevo",
        "nueva",
        "crear",
        "sistema",
        "system",
        "operador",
        "operator",
    }
)


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9áéíóúüñ\s\-]+", " ", text)
    text = text.replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def significant_tokens(text: str) -> list[str]:
    return [t for t in normalize(text).split() if len(t) > 2 and t not in GENERIC_TOKENS]


def load_inventory(path: Path = INVENTORY) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def score_match(request: str, component: dict) -> int:
    req = normalize(request)
    req_sig = set(significant_tokens(request))
    haystacks = [component.get("id", ""), component.get("name", "")]
    haystacks.extend(component.get("aliases") or [])
    best = 0
    for item in haystacks:
        n = normalize(item)
        if not n:
            continue
        # Exact / phrase containment only if the haystack has a specific token
        # or is a multi-word specific phrase already in the request.
        sig = significant_tokens(item)
        if not sig:
            continue
        if req == n or (len(n) > 8 and (n in req or req in n)):
            best = max(best, 100)
            continue
        hits = [t for t in sig if t in req_sig or t in req]
        if hits:
            best = max(best, int(70 * len(hits) / len(sig)))
    return best


def check(request: str, inventory: dict | None = None) -> dict:
    inv = inventory or load_inventory()
    matches = []
    for component in inv.get("components", []):
        s = score_match(request, component)
        if s >= 50:
            matches.append({"score": s, **component})
    matches.sort(key=lambda m: m["score"], reverse=True)

    if not matches:
        return {
            "status": "ALLOW_NEW",
            "matched_ids": [],
            "recommendation": "create",
            "matches": [],
            "message": "No inventory match; continue Factory design cycle.",
        }

    top = matches[0]
    decision = top.get("decision")
    if decision in {"reuse", "evaluate_merge", "integrate_later"}:
        return {
            "status": "BLOCKED_DUPLICATE",
            "matched_ids": [m["id"] for m in matches],
            "recommendation": "reuse" if decision == "reuse" else "merge",
            "matches": matches,
            "message": (
                f"Blocked: reuse/consolidate '{top['name']}' ({top['id']}) "
                f"instead of creating a parallel component."
            ),
        }
    if decision == "pilot":
        return {
            "status": "ALLOW_PILOT",
            "matched_ids": [m["id"] for m in matches],
            "recommendation": "create",
            "matches": matches,
            "message": f"Pilot package allowed for '{top['id']}'.",
        }
    return {
        "status": "ALLOW_NEW",
        "matched_ids": [m["id"] for m in matches],
        "recommendation": "create",
        "matches": matches,
        "message": "Match found but decision permits new work; review manually.",
    }


def self_test() -> int:
    inv = load_inventory()
    cases = [
        ("crear un nuevo Agent Tester", "BLOCKED_DUPLICATE"),
        ("agente que opere Windows Docker y servidores", "BLOCKED_DUPLICATE"),
        ("agente documental basico A1", "ALLOW_PILOT"),
        ("agente de irrigacion hidroponica vertical", "ALLOW_NEW"),
    ]
    failed = 0
    for request, expected in cases:
        result = check(request, inv)
        ok = result["status"] == expected
        print(f"{'OK' if ok else 'FAIL'}: {request!r} -> {result['status']} (want {expected})")
        if not ok:
            failed += 1
    return failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="?", help="Natural-language creation request")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args(argv)

    if args.self_test:
        failed = self_test()
        return 1 if failed else 0
    if not args.request:
        parser.error("request required unless --self-test")
    result = check(args.request)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["status"])
        print(result["message"])
        if result["matched_ids"]:
            print("matched:", ", ".join(result["matched_ids"]))
    return 0 if result["status"] != "BLOCKED_DUPLICATE" else 2


if __name__ == "__main__":
    sys.exit(main())
