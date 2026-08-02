#!/usr/bin/env python3
"""Dry-run integrity check for the home polish package (no web deploy)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "index.html",
    "style.base.css",
    "polish.css",
    "nav.js",
    "README.md",
    "APPLY.md",
    "COPY-DIFF.md",
    "SECTION-HIERARCHY.md",
    "tests/test_home_content.py",
]

MUST_CONTAIN = {
    "index.html": [
        "NORTIQA",
        "contenido demostrativo",
        "en preparación",
        'data-layer="public"',
        'data-layer="internal"',
        'id="inicio"',
        'id="productos"',
        'href="polish.css"',
        'href="style.base.css"',
    ],
    "polish.css": [
        "polish-v2",
        ".capability-strip",
        "prefers-reduced-motion",
    ],
}


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing file: {rel}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"empty file: {rel}")

    for rel, needles in MUST_CONTAIN.items():
        text = (ROOT / rel).read_text(encoding="utf-8").lower()
        for needle in needles:
            if needle.lower() not in text:
                errors.append(f"{rel}: missing required marker {needle!r}")

    base = ROOT / "style.base.css"
    if base.is_file() and "Theme Name: Nortiqa Lab" not in base.read_text(encoding="utf-8"):
        errors.append("style.base.css: missing WP theme header")

    if errors:
        print("check_package: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("check_package: OK")
    print(f"  root: {ROOT}")
    print(f"  files: {len(REQUIRED)} required present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
