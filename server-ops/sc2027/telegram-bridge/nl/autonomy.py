"""Green / yellow / red gates for bridge actions."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Gate:
    zone: str  # green | yellow | red
    reason: str
    allow_execute: bool
    human_next: Optional[str] = None


RED_PATTERNS = (
    (r"\bpromote\b", "promote requires separate PAO / Gio gates"),
    (r"\bprod(uction)?\b.*\b(reload|restart|deploy|chmod|nginx)\b", "production privileged change"),
    (r"\bnginx\b.*\b(reload|restart)\b", "nginx reload is privileged"),
    (r"\bdocker\.sock\b|\bdocker\s+socket\b", "docker.sock work needs separate PAO"),
    (r"\b\.env\b|\btoken\b|\bpassword\b|\bsecret\b", "secrets must not be handled in chat"),
    (r"\bvalent\b|\berp\b|\bsurlancer\b|\bvialidad\b|\blla\b", "cross-entity context blocked"),
    (r"\broot\b|\bsudo\b", "privileged host action"),
    (r"\bdrop\b|\btruncate\b|\bdelete\s+from\b", "destructive data op"),
)

GREEN_OPS = {
    "public_health",
    "status",
    "help",
    "kit_check",
}


def classify_goal(role: Optional[str], goal: str, bridge_action: Optional[str] = None) -> Gate:
    text = f"{role or ''} {bridge_action or ''} {goal or ''}".lower()

    for pattern, reason in RED_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            return Gate(
                zone="red",
                reason=reason,
                allow_execute=False,
                human_next=_red_next(reason, goal),
            )

    if bridge_action in {"help", "status"}:
        return Gate("green", "bridge meta", True)

    if role == "NL-OPS":
        g = (goal or "").lower()
        if not g or "health" in g or "status" in g:
            return Gate("green", "enumerated public/staging health", True)
        if "backup" in g:
            return Gate(
                "yellow",
                "backup may exist as staging script — confirm path on host",
                True,
                human_next="On VPS staging: run ./backup-config.sh only if present under sc2027-staging",
            )
        if "login" in g:
            return Gate(
                "red",
                "login portal install needs privileged nginx/html write",
                False,
                human_next=(
                    "As root/sc2027: run install-login-portal script from "
                    "server-ops/sc2027/login-portal (see prior OPS handoff)"
                ),
            )
        return Gate(
            "yellow",
            "OPS goal not in hard allowlist — advise only",
            False,
            human_next="Rephrase as /ops health or provide an allowlisted staging script name",
        )

    if role == "NL-AUDITOR":
        return Gate("green", "audit/gate only — no host execute", False)

    if role in {"NL-BUILDER", "NL-PRODUCT", "NL-ORCH", "NL-MEMORY"}:
        return Gate(
            "green",
            "return brief/plan only from bridge (no host mutate)",
            False,
        )

    return Gate("yellow", "unknown route", False, human_next="Use /help")


def _red_next(reason: str, goal: str) -> str:
    if "promote" in reason:
        return "Confirm Hetzner snapshot + healthchecks; use promote checklist; separate PAO"
    if "secret" in reason:
        return "Handle secrets only on host env/secret store — never in Telegram"
    if "cross-entity" in reason:
        return "Stay in Nortiqa Lab context only"
    if "login" in (goal or "").lower():
        return "Privileged install on staging host as root/sc2027"
    return "Gio must authorize the privileged/red action explicitly"
