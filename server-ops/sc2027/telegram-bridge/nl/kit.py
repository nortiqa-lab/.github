"""Load mirrored NL kit files from nl-kit/."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

REQUIRED_RELATIVE = [
    "AGENTS.md",
    "agents/SHARED_RULES.md",
    "agents/AUTONOMY.md",
    "agents/DISPATCH.md",
    "agents/BOOTSTRAP.md",
    "agents/prompts/NL-ORCH.md",
    "agents/prompts/NL-AUDITOR.md",
    "agents/prompts/NL-BUILDER.md",
    "agents/prompts/NL-OPS.md",
    "agents/prompts/NL-PRODUCT.md",
    "agents/prompts/NL-MEMORY.md",
]

ROLE_PROMPT = {
    "NL-ORCH": "agents/prompts/NL-ORCH.md",
    "NL-AUDITOR": "agents/prompts/NL-AUDITOR.md",
    "NL-BUILDER": "agents/prompts/NL-BUILDER.md",
    "NL-OPS": "agents/prompts/NL-OPS.md",
    "NL-PRODUCT": "agents/prompts/NL-PRODUCT.md",
    "NL-MEMORY": "agents/prompts/NL-MEMORY.md",
}


def default_kit_path() -> Path:
    env = os.environ.get("NL_KIT_PATH")
    if env:
        return Path(env)
    # package-relative default after sync-nl-kit.sh
    return Path(__file__).resolve().parents[1] / "nl-kit"


def kit_status(kit_path: Optional[Path] = None) -> Dict[str, object]:
    root = kit_path or default_kit_path()
    missing: List[str] = []
    present: List[str] = []
    for rel in REQUIRED_RELATIVE:
        p = root / rel
        if p.is_file():
            present.append(rel)
        else:
            missing.append(rel)
    return {
        "path": str(root),
        "ok": not missing,
        "present_count": len(present),
        "missing": missing,
    }


def load_role_prompt(role: str, kit_path: Optional[Path] = None) -> Optional[str]:
    rel = ROLE_PROMPT.get(role)
    if not rel:
        return None
    path = (kit_path or default_kit_path()) / rel
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def brief_from_prompt(role: str, goal: str, kit_path: Optional[Path] = None) -> str:
    prompt = load_role_prompt(role, kit_path)
    if not prompt:
        return (
            f"Kit mirror missing prompt for {role}. "
            "Run sync-nl-kit.sh from the versionable package, then retry."
        )
    # Keep Telegram short: first mission/autonomy lines + goal.
    head = []
    for line in prompt.splitlines():
        if line.startswith("#") or line.startswith("##"):
            head.append(line)
        if len(head) >= 6:
            break
    return "\n".join(head) + f"\n\nGOAL: {goal or '(none)'}\n"
