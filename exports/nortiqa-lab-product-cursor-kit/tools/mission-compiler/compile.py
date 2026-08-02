#!/usr/bin/env python3
"""NORTIQA Gen5 Mission Control — dry-run compiler CLI.

Emits a mission-contract.v0 JSON from a natural-language request.
Never executes side effects. Not an authorization to run production work.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from compiler import compile_request  # noqa: E402
from validate import validate_contract  # noqa: E402


SELF_TESTS = [
    (
        "Actualizá el README con un puntero a Vanguard",
        {"status": "planned", "autonomy_level": 2, "write": True},
    ),
    (
        "Explicá qué es Mission Control",
        {"status": "planned", "autonomy_level": 0, "write": False},
    ),
    (
        "Diagnosticá el health de api.nortiqalab.com",
        {"status": "planned", "autonomy_level": 1, "write": False},
    ),
    (
        "Reiniciá nginx en producción",
        {"status": "awaiting_human", "autonomy_level": 5, "write": False},
    ),
    (
        "Mezclá esto con Valent Capital Group",
        {"status": "blocked", "autonomy_level": 0, "write": False},
    ),
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _strip_private(contract: dict) -> tuple[dict, str | None]:
    kind = contract.pop("__classifier_kind", None)
    return contract, kind


def run_self_test() -> int:
    failed = 0
    for raw, expect in SELF_TESTS:
        contract = compile_request(raw, channel="cursor", requester="self-test")
        contract, kind = _strip_private(contract)
        errors = validate_contract(contract)
        write = bool(contract.get("permissions", {}).get("write"))
        ok = (
            not errors
            and contract.get("status") == expect["status"]
            and contract.get("autonomy_level") == expect["autonomy_level"]
            and write == expect["write"]
        )
        mark = "PASS" if ok else "FAIL"
        print(f"{mark}  kind={kind} status={contract.get('status')} level={contract.get('autonomy_level')} write={write}")
        print(f"      request: {raw}")
        if errors:
            for e in errors:
                print(f"      error: {e}")
            failed += 1
        elif not ok:
            print(f"      expected: {expect}")
            failed += 1
    print(f"self-test: {len(SELF_TESTS) - failed}/{len(SELF_TESTS)} passed")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile a natural-language request into a Gen5 mission contract (dry-run)."
    )
    parser.add_argument("request", nargs="?", help="Natural language mission request")
    parser.add_argument("-f", "--file", help="Read request text from file")
    parser.add_argument("--requester", default="Gio")
    parser.add_argument(
        "--channel",
        default="cursor",
        choices=["chat", "telegram", "cursor", "api", "handoff", "other"],
    )
    parser.add_argument("--repo", default="nortiqa-lab/.github")
    parser.add_argument(
        "-o",
        "--output",
        help="Write envelope JSON to this path (default: stdout)",
    )
    parser.add_argument(
        "--contract-only",
        action="store_true",
        help="Emit only the contract object (no envelope)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in classification/validation fixtures",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    raw = args.request
    if args.file:
        raw = Path(args.file).read_text(encoding="utf-8")
    if not raw or not str(raw).strip():
        parser.error("provide REQUEST or --file, or use --self-test")

    try:
        contract = compile_request(
            str(raw),
            requester=args.requester,
            channel=args.channel,
            repo=args.repo,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    contract, kind = _strip_private(contract)
    errors = validate_contract(contract)
    envelope = {
        "dry_run": True,
        "side_effects": "none",
        "compiler": "tools/mission-compiler v0",
        "schema": "docs/dev/schemas/mission-contract.v0.json",
        "repo_root": str(_repo_root()),
        "classifier_kind": kind,
        "valid": not errors,
        "errors": errors,
        "contract": contract,
        "note": (
            "DEV draft dry-run. Valid contract ≠ authorization to execute. "
            "See docs/dev/GEN5-MISSION-CONTROL.md."
        ),
    }

    payload = contract if args.contract_only else envelope
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)

    # Exit 0 if structurally valid; 3 if invalid contract (still printed for inspection).
    if errors and not args.contract_only:
        return 3
    if errors and args.contract_only:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
