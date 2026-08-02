"""Bridge meta commands: /help /status."""

from __future__ import annotations

from nl.kit import kit_status
from nl.handlers.ops import unit_is_active


HELP_TEXT = """Nortiqa ServidorOps bot — NL ingress

/help
/status
/orch <goal>
/ops <goal>          (try: health)
/build <goal>
/product <goal>
/audit <goal>
/memory
NL-OPS: <goal>       (role prefix)

Telegram is ingress/notify. Red actions are refused.
Token never appears in replies.
"""


def help_reply() -> str:
    return HELP_TEXT.strip() + "\n"


def status_reply() -> str:
    kit = kit_status()
    unit = unit_is_active()
    missing = ", ".join(kit["missing"][:5]) if kit["missing"] else "none"
    return (
        f"unit: {unit}\n"
        f"nl-kit: {kit['path']}\n"
        f"nl-kit ok: {kit['ok']} ({kit['present_count']} files)\n"
        f"missing: {missing}\n"
        f"entity_scope: nortiqa_lab_only\n"
        f"env: staging-oriented\n"
    )
