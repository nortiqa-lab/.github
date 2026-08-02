"""Entrypoint: process one Telegram text message into an NL contract reply."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from nl.auth import is_authorized
from nl.autonomy import classify_goal
from nl.contracts import format_reply
from nl.handlers import bridge as bridge_handlers
from nl.handlers import ops as ops_handlers
from nl.kit import brief_from_prompt, kit_status
from nl.router import route_message


@dataclass
class ProcessResult:
    ok: bool
    reply: str
    role: str
    zone: str
    authorized: bool


def _handoff_dir() -> Path:
    env = os.environ.get("NL_HANDOFF_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[1] / "handoffs-local"


def maybe_write_handoff(role: str, goal: str, reply: str, zone: str) -> Optional[str]:
    if os.environ.get("NL_HANDOFF_ENABLED", "1") not in {"1", "true", "TRUE", "yes"}:
        return None
    directory = _handoff_dir()
    try:
        directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = directory / f"{stamp}-{role.lower()}.md"
        path.write_text(
            "\n".join(
                [
                    f"# Telegram handoff stub — {stamp}",
                    "",
                    f"- Role: {role}",
                    f"- Zone: {zone}",
                    f"- Goal: {goal or '-'}",
                    "",
                    "## Reply",
                    "",
                    "```",
                    reply.rstrip(),
                    "```",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return str(path)
    except OSError:
        return None


def process_message(
    text: str,
    *,
    user_id: Optional[str] = None,
    chat_id: Optional[str] = None,
    live_health: bool = True,
    skip_auth: bool = False,
) -> ProcessResult:
    if not skip_auth and not is_authorized(user_id=user_id, chat_id=chat_id):
        return ProcessResult(
            ok=False,
            reply="No autorizado.\n",
            role="bridge",
            zone="red",
            authorized=False,
        )

    routed = route_message(text)
    default_role = os.environ.get("NL_DEFAULT_ROLE", "NL-ORCH")

    if routed.kind == "bridge":
        if routed.action == "help":
            body = bridge_handlers.help_reply()
            if routed.goal.startswith("unknown command"):
                body = routed.goal + "\n\n" + body
            reply = format_reply(
                "bridge",
                done="help",
                verify="static",
                next_step="Send /ops health or /orch <goal>",
                extra=body,
            )
            return ProcessResult(True, reply, "bridge", "green", True)

        if routed.action == "status":
            body = bridge_handlers.status_reply()
            kit_ok = kit_status()["ok"]
            reply = format_reply(
                "bridge",
                done="status",
                verify="kit " + ("ok" if kit_ok else "MISSING"),
                blocked="none" if kit_ok else "sync nl-kit",
                next_step="Run sync-nl-kit.sh if kit missing",
                extra=body,
            )
            return ProcessResult(True, reply, "bridge", "green", True)

    role = routed.role or default_role
    goal = routed.goal
    gate = classify_goal(role, goal, routed.action)

    if gate.zone == "red" or (not gate.allow_execute and role == "NL-OPS" and gate.zone != "green"):
        # Still allow non-exec brief for non-OPS below; OPS red/blocked execute path:
        if gate.zone == "red":
            reply = format_reply(
                role,
                done="refused",
                verify="autonomy gate",
                blocked=gate.reason,
                next_step=gate.human_next or "Gio authorization required",
            )
            maybe_write_handoff(role, goal, reply, gate.zone)
            return ProcessResult(True, reply, role, gate.zone, True)

    if role == "NL-OPS" and gate.allow_execute:
        g = (goal or "health").lower()
        if not g or "health" in g or "status" in g:
            if live_health:
                result = ops_handlers.public_health()
                verify = "\n".join(result.lines)
                reply = format_reply(
                    "NL-OPS",
                    done="public health " + ("OK" if result.ok else "DEGRADED"),
                    verify=verify,
                    blocked="none" if result.ok else "investigate failing targets",
                    next_step="If login portal needed: privileged staging install (not from chat)",
                )
            else:
                reply = format_reply(
                    "NL-OPS",
                    done="health skipped (offline mode)",
                    verify="live_health=false",
                    next_step="Re-run with network for live curls",
                )
            maybe_write_handoff(role, goal, reply, gate.zone)
            return ProcessResult(True, reply, role, gate.zone, True)

    # Brief / plan path for ORCH, BUILDER, PRODUCT, AUDITOR, MEMORY, yellow OPS
    extra = brief_from_prompt(role, goal)
    if role == "NL-AUDITOR":
        done = f"gate draft for: {goal or '(empty)'}"
        blocked = "none — advisory only" if gate.zone != "red" else gate.reason
        next_step = "Human confirms APPROVE/BLOCK before privileged work"
    elif role == "NL-MEMORY":
        done = "continuity pointer"
        blocked = "none"
        next_step = "Read latest docs/shared-ai-memory/handoffs on kit/repo"
    elif role == "NL-OPS":
        done = "advice only (not allowlisted execute)"
        blocked = gate.reason
        next_step = gate.human_next or "Use /ops health"
    else:
        done = f"brief prepared for {role}"
        blocked = "execution in Cursor/repo — bridge does not mutate hosts"
        next_step = "Open Cursor on nortiqa-lab/.github with this goal" if goal else "Send a concrete goal"

    reply = format_reply(
        role,
        done=done,
        verify=f"zone={gate.zone}",
        blocked=blocked,
        next_step=next_step,
        extra=extra,
    )
    maybe_write_handoff(role, goal, reply, gate.zone)
    return ProcessResult(True, reply, role, gate.zone, True)


def self_test() -> int:
    # Auth fail-closed
    os.environ.pop("TELEGRAM_ALLOWED_USER_IDS", None)
    os.environ.pop("TELEGRAM_ALLOWED_CHAT_IDS", None)
    denied = process_message("hola", user_id="1", skip_auth=False)
    assert denied.authorized is False

    os.environ["TELEGRAM_ALLOWED_USER_IDS"] = "42"
    help_r = process_message("/help", user_id="42", live_health=False)
    assert "ROLE: bridge" in help_r.reply

    red = process_message("/ops promote to prod", user_id="42", live_health=False)
    assert red.zone == "red"
    assert "BLOCKED:" in red.reply

    orch = process_message("/orch map pending login portal", user_id="42", live_health=False)
    assert orch.role == "NL-ORCH"

    print("self-test: ok")
    return 0


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="NL Telegram bridge processor")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--text", help="Process one message (requires allowlist env or --skip-auth)")
    parser.add_argument("--user-id", default="0")
    parser.add_argument("--skip-auth", action="store_true")
    parser.add_argument("--offline", action="store_true", help="Do not run live health curls")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.text:
        parser.error("--text or --self-test required")

    result = process_message(
        args.text,
        user_id=args.user_id,
        live_health=not args.offline,
        skip_auth=args.skip_auth,
    )
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(result.reply, end="")
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
