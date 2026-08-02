"""NL output contract for Telegram replies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class NlReply:
    role: str
    canon: str = "bootstrap-draft"
    done: str = ""
    verify: str = ""
    blocked: str = "none"
    next_step: str = ""
    extra: str = ""

    def format(self, max_chars: int = 3500) -> str:
        lines = [
            f"ROLE: {self.role}",
            f"CANON: {self.canon}",
            f"DONE: {self.done or '-'}",
            f"VERIFY: {self.verify or '-'}",
            f"BLOCKED: {self.blocked or 'none'}",
            f"NEXT: {self.next_step or '-'}",
        ]
        if self.extra:
            lines.append("")
            lines.append(self.extra.strip())
        text = "\n".join(lines).strip() + "\n"
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 24].rstrip() + "\n…(truncated)\n"


def format_reply(
    role: str,
    *,
    done: str = "",
    verify: str = "",
    blocked: str = "none",
    next_step: str = "",
    canon: str = "bootstrap-draft",
    extra: str = "",
    max_chars: int = 3500,
) -> str:
    return NlReply(
        role=role,
        canon=canon,
        done=done,
        verify=verify,
        blocked=blocked,
        next_step=next_step,
        extra=extra,
    ).format(max_chars=max_chars)
