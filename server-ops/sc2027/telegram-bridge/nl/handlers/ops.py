"""Enumerated staging-safe OPS actions."""

from __future__ import annotations

import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import List, Sequence, Tuple

DEFAULT_TARGETS: Sequence[Tuple[str, int]] = (
    ("https://nortiqalab.com/", 200),
    ("https://api.nortiqalab.com/health", 200),
    ("https://n8n.nortiqalab.com/", 200),
    ("https://mcp.nortiqalab.com/", 401),
    ("https://flow.nortiqalab.com/", 200),
)


@dataclass
class HealthResult:
    ok: bool
    lines: List[str]


def public_health(
    targets: Sequence[Tuple[str, int]] = DEFAULT_TARGETS,
    timeout: float = 10.0,
) -> HealthResult:
    lines: List[str] = []
    ok_all = True
    for url, expected in targets:
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:  # noqa: BLE001 — surface any network failure
            ok_all = False
            lines.append(f"ERR {url} ({e.__class__.__name__})")
            continue
        match = code == expected
        ok_all = ok_all and match
        mark = "OK" if match else "FAIL"
        lines.append(f"{mark} {code} (expect {expected}) {url}")
    return HealthResult(ok=ok_all, lines=lines)


def try_staging_script(script_path: str) -> Tuple[bool, str]:
    """Optional host script runner — disabled unless path exists and executable intent is explicit.

    This helper only reports presence; it does not execute arbitrary shell from chat.
    """
    from pathlib import Path

    p = Path(script_path)
    if p.is_file():
        return True, f"script present: {p}"
    return False, f"script missing: {p}"


def unit_is_active(unit: str = "sc2027-telegram-agent.service") -> str:
    try:
        proc = subprocess.run(
            ["systemctl", "is-active", unit],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return (proc.stdout or proc.stderr or "unknown").strip()
    except Exception:
        return "unavailable-here"
