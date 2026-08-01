#!/usr/bin/env python3
"""Shared helpers for Nortiqa agent acceptance harness (draft / isolated)."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - bootstrap without PyYAML
    yaml = None

ROOT = Path(__file__).resolve().parents[3]
AGENTS_DIR = ROOT / ".github" / "agents"
DOCS_AGENTS = ROOT / "docs" / "agents"
RESULTS_DIR = ROOT / "tests" / "agent-acceptance" / "results"
FIXTURES = ROOT / "tests" / "agent-acceptance" / "fixtures"
SANDBOX = ROOT / "tests" / "agent-acceptance" / "sandbox"

VALID_STATUSES = {
    "draft",
    "reviewed",
    "approved-staging",
    "active-staging",
    "production-approved",
}

# Statuses an automated evaluator may set without Gio
EVALUATOR_ALLOWED_STATUSES = {"draft", "reviewed"}

PLACEHOLDER_OWNERS = {
    "",
    "todo",
    "tbd",
    "owner",
    "placeholder",
    "changeme",
    "your-name",
    "n/a",
    "na",
    "unknown",
}

ROLE_REQUIRED_TOOLS: dict[str, set[str]] = {
    "inspector": {"read"},
    "implementer": {"edit"},
    "tester": {"shell_test"},
    "code-reviewer": {"read"},
    "security-reviewer": {"read", "grep"},
    "database-migrator": {"shell_db_fixture"},
}

ROLE_FORBIDDEN_TOOLS: dict[str, set[str]] = {
    "inspector": {"edit", "write", "shell_destructive", "deploy", "shell_db_fixture"},
    "implementer": {"deploy", "shell_destructive", "auto_approve"},
    "tester": {"edit", "deploy", "shell_destructive"},
    "code-reviewer": {"edit", "deploy", "shell_destructive", "shell_db_fixture"},
    "security-reviewer": {"edit", "deploy", "exploit", "secrets_echo", "shell_destructive"},
    "database-migrator": {"deploy", "auto_approve", "exploit"},
}

REQUIRED_GOVERNANCE = {
    "docs/agents/GOBERNANZA-BOTS.md",
    "AGENTS.md",
}

UNIVERSAL_PROHIBITIONS = {
    "production",
    "secrets_echo",
    "destructive",
    "auto_approve",
    "unauthorized_git",
}


@dataclass
class AgentManifest:
    path: Path
    frontmatter: dict[str, Any]
    body: str
    raw: str
    issues: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return str(self.frontmatter.get("name", ""))

    @property
    def role(self) -> str:
        return str(self.frontmatter.get("role", ""))

    @property
    def owner(self) -> str:
        return str(self.frontmatter.get("owner", "")).strip().lower()

    @property
    def status(self) -> str:
        return str(self.frontmatter.get("status", "")).strip()

    @property
    def tools(self) -> list[str]:
        t = self.frontmatter.get("tools") or []
        return [str(x) for x in t]

    @property
    def prohibitions(self) -> set[str]:
        p = self.frontmatter.get("prohibitions") or []
        return {str(x) for x in p}


def _parse_frontmatter_fallback(text: str) -> tuple[dict[str, Any], str]:
    """Minimal YAML-ish parser for our controlled manifests if PyYAML missing."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_raw, body = parts[1], parts[2]
    data: dict[str, Any] = {}
    stack: list[tuple[int, Any, str | None]] = [(0, data, None)]
    pending_key: str | None = None
    pending_indent = 0

    for line in fm_raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()
            pending_key = None

        container = stack[-1][1]

        if stripped.startswith("- "):
            val = stripped[2:].strip().strip('"').strip("'")
            if isinstance(container, list):
                container.append(val)
            elif pending_key is not None and isinstance(stack[-2][1], dict):
                # Should not happen if structure correct
                pass
            continue

        if ":" in stripped:
            key, _, rest = stripped.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == "" or rest == "|" or rest == ">":
                # nested map or list follows
                # peek next — default to dict; list if next is '-'
                container[key] = {}
                stack.append((indent + 2, container[key], key))
                pending_key = key
                pending_indent = indent
            elif rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
                container[key] = [
                    x.strip().strip('"').strip("'")
                    for x in inner.split(",")
                    if x.strip()
                ]
            else:
                val: Any = rest.strip('"').strip("'")
                if val.lower() in {"true", "false"}:
                    val = val.lower() == "true"
                container[key] = val
            continue

    # Convert empty dicts that should be lists by scanning original for "- " children
    # Re-parse with list awareness
    data = {}
    current_list_key: list[str] | None = None
    map_stack: list[tuple[str, dict[str, Any], int]] = [("", data, -1)]
    list_mode_key: str | None = None
    list_mode_indent = -1
    nested_map_key: str | None = None
    nested_map: dict[str, Any] | None = None
    nested_indent = -1

    for line in fm_raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if list_mode_key and indent <= list_mode_indent and not stripped.startswith("-"):
            list_mode_key = None
        if nested_map is not None and indent <= nested_indent and not stripped.startswith("-"):
            nested_map = None
            nested_map_key = None

        target = nested_map if nested_map is not None else data

        if stripped.startswith("- "):
            val = stripped[2:].strip().strip('"').strip("'")
            if list_mode_key:
                if nested_map is not None and list_mode_key in nested_map:
                    if not isinstance(nested_map[list_mode_key], list):
                        nested_map[list_mode_key] = []
                    nested_map[list_mode_key].append(val)
                else:
                    if not isinstance(data.get(list_mode_key), list):
                        data[list_mode_key] = []
                    data[list_mode_key].append(val)
            continue

        if ":" in stripped:
            key, _, rest = stripped.partition(":")
            key = key.strip()
            rest = rest.strip().strip('"').strip("'")
            if rest == "":
                # Could be nested map
                if indent == 0:
                    data[key] = {}
                    nested_map = data[key]
                    nested_map_key = key
                    nested_indent = indent
                    list_mode_key = None
                else:
                    # list-bearing key under nested map
                    assert nested_map is not None
                    nested_map[key] = []
                    list_mode_key = key
                    list_mode_indent = indent
            else:
                val: Any = rest
                if isinstance(val, str) and val.lower() in {"true", "false"}:
                    val = val.lower() == "true"
                if nested_map is not None and indent > nested_indent:
                    nested_map[key] = val
                else:
                    data[key] = val
                    nested_map = None
                    list_mode_key = None
    return data, body.lstrip("\n")


def parse_agent_file(path: Path) -> AgentManifest:
    raw = path.read_text(encoding="utf-8")
    issues: list[str] = []

    # Duplicate frontmatter detection
    if raw.count("\n---\n") + (1 if raw.startswith("---\n") else 0) > 2:
        # more than opening+closing
        fence_count = len(re.findall(r"(?m)^---\s*$", raw))
        if fence_count > 2:
            issues.append(f"duplicate_or_extra_frontmatter_fences:{fence_count}")

    fm: dict[str, Any]
    body: str
    if yaml is not None:
        if not raw.startswith("---"):
            issues.append("missing_frontmatter")
            fm, body = {}, raw
        else:
            parts = re.split(r"(?m)^---\s*$", raw, maxsplit=2)
            if len(parts) < 3:
                issues.append("invalid_frontmatter_fences")
                fm, body = {}, raw
            else:
                try:
                    loaded = yaml.safe_load(parts[1]) or {}
                    if not isinstance(loaded, dict):
                        issues.append("frontmatter_not_mapping")
                        fm = {}
                    else:
                        fm = loaded
                    body = parts[2].lstrip("\n")
                except Exception as exc:  # noqa: BLE001
                    issues.append(f"frontmatter_yaml_error:{exc}")
                    fm, body = {}, raw
    else:
        fm, body = _parse_frontmatter_fallback(raw)
        if not fm:
            issues.append("frontmatter_empty_or_unparsed")

    return AgentManifest(path=path, frontmatter=fm, body=body, raw=raw, issues=issues)


def load_all_agents() -> list[AgentManifest]:
    if not AGENTS_DIR.is_dir():
        return []
    paths = sorted(AGENTS_DIR.glob("*.agent.md"))
    return [parse_agent_file(p) for p in paths]


def redact_secret(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
    tail = value[-4:] if len(value) >= 4 else "****"
    return f"[REDACTED sha256={digest} tail={tail}]"


def ensure_dirs() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SANDBOX.mkdir(parents=True, exist_ok=True)
    (SANDBOX / "db").mkdir(parents=True, exist_ok=True)
