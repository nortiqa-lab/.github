"""Map Telegram text → bridge action or NL-* role."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

ROLE_PREFIX = re.compile(
    r"^(NL-(?:ORCH|AUDITOR|BUILDER|OPS|PRODUCT|MEMORY))\s*:\s*(.*)$",
    re.IGNORECASE | re.DOTALL,
)

COMMANDS = {
    "/help": ("bridge", "help"),
    "/status": ("bridge", "status"),
    "/orch": ("NL-ORCH", None),
    "/ops": ("NL-OPS", None),
    "/build": ("NL-BUILDER", None),
    "/product": ("NL-PRODUCT", None),
    "/audit": ("NL-AUDITOR", None),
    "/memory": ("NL-MEMORY", None),
}

OPS_KEYWORDS = (
    "health",
    "healthcheck",
    "backup",
    "cert",
    "certs",
    "login",
    "staging",
    "promote",
    "nginx",
    "ollama",
)


@dataclass(frozen=True)
class Route:
    kind: str  # bridge | role
    role: Optional[str]
    action: Optional[str]
    goal: str
    raw: str


def _strip_bot_mention(text: str) -> str:
    # "/ops@NortiqaServidorOpsBot health" → "/ops health"
    return re.sub(r"^(/[a-z]+)@[A-Za-z0-9_]+", r"\1", text.strip(), count=1, flags=re.I)


def route_message(text: str, default_role: str = "NL-ORCH") -> Route:
    raw = (text or "").strip()
    if not raw:
        return Route("bridge", None, "help", "", raw)

    cleaned = _strip_bot_mention(raw)

    m = ROLE_PREFIX.match(cleaned)
    if m:
        role = m.group(1).upper()
        goal = (m.group(2) or "").strip()
        return Route("role", role, None, goal, raw)

    if cleaned.startswith("/"):
        parts = cleaned.split(maxsplit=1)
        cmd = parts[0].lower()
        rest = parts[1].strip() if len(parts) > 1 else ""
        if cmd in COMMANDS:
            kind_role, action = COMMANDS[cmd]
            if kind_role == "bridge":
                return Route("bridge", None, action, rest, raw)
            return Route("role", kind_role, None, rest, raw)
        return Route(
            "bridge",
            None,
            "help",
            f"unknown command: {cmd}",
            raw,
        )

    lower = cleaned.lower()
    if any(k in lower for k in OPS_KEYWORDS):
        return Route("role", "NL-OPS", None, cleaned, raw)

    return Route("role", default_role, None, cleaned, raw)
