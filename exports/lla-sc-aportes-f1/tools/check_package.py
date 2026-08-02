#!/usr/bin/env python3
"""Integrity dry-run for lla-sc-aportes-f1 package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "APPLY.md",
    "G1-CHECKLIST.md",
    "g1/G1-DOSSIER.md",
    "g1/G1-SOLICITUD-DICTAMEN.md",
    "g1/G1-PREGUNTAS.md",
    "g1/G1-HALLAZGOS-PRELIMINARES.md",
    "g1/GATES-TRACKER.md",
    "config/app.json",
    "data/campaigns.json",
    "data/destinations.json",
    "web/index.html",
    "web/app.js",
    "web/campaign-engine.js",
    "web/styles.css",
    "tools/campaign_rules.py",
    "api/server.py",
    "api/db.py",
    "api/mp_adapter.py",
    "api/schema.sql",
    "tools/test_api_f2.py",
    "tools/test_api_f3.py",
    "docs/F3-SCOPE.md",
    "web/tesoreria.html",
    "web/tesoreria.js",
    "legal/DRAFT-terminos-aportes.md",
    "legal/DRAFT-privacidad.md",
    "legal/DRAFT-consentimiento.md",
]


def main() -> int:
    failed = 0
    for rel in REQUIRED:
        path = ROOT / rel
        ok = path.is_file() and path.stat().st_size > 0
        print(("OK" if ok else "FAIL") + ":", rel)
        if not ok:
            failed += 1

    app = json.loads((ROOT / "config/app.json").read_text(encoding="utf-8"))
    pay = bool(app.get("payments_enabled"))
    print(("OK" if not pay else "FAIL") + ":", "payments_enabled is false")
    if pay:
        failed += 1

    # Ensure electoral destination hidden
    dests = json.loads((ROOT / "data/destinations.json").read_text(encoding="utf-8"))
    electoral = [d for d in dests["destinations"] if d.get("electoral_circuit")]
    hidden = all(d.get("ui_visible") is False for d in electoral)
    print(("OK" if electoral and hidden else "FAIL") + ":", "electoral circuit hidden in UI")
    if not (electoral and hidden):
        failed += 1

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
