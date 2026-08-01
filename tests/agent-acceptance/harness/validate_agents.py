#!/usr/bin/env python3
"""Validate .github/agents/*.agent.md structure and governance separation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    EVALUATOR_ALLOWED_STATUSES,
    PLACEHOLDER_OWNERS,
    REQUIRED_GOVERNANCE,
    ROLE_FORBIDDEN_TOOLS,
    ROLE_REQUIRED_TOOLS,
    ROOT,
    UNIVERSAL_PROHIBITIONS,
    VALID_STATUSES,
    AgentManifest,
    ensure_dirs,
    load_all_agents,
    RESULTS_DIR,
)


def check_manifest(agent: AgentManifest) -> list[dict]:
    findings: list[dict] = []

    def fail(code: str, msg: str) -> None:
        findings.append({"level": "error", "code": code, "message": msg, "agent": agent.name or agent.path.name})

    def warn(code: str, msg: str) -> None:
        findings.append({"level": "warning", "code": code, "message": msg, "agent": agent.name or agent.path.name})

    for issue in agent.issues:
        fail("parse", issue)

    fm = agent.frontmatter
    required_fields = [
        "name",
        "description",
        "version",
        "owner",
        "status",
        "role",
        "scope",
        "tools",
        "prohibitions",
        "governance_refs",
        "separation",
    ]
    for field in required_fields:
        if field not in fm:
            fail("missing_field", f"Missing required frontmatter field: {field}")

    if not agent.name:
        fail("name", "name must be non-empty")
    elif not str(agent.name).startswith("nl-"):
        warn("name_prefix", "Preferred name prefix is nl-")

    version = str(fm.get("version", ""))
    if not version or version in {"0", "TODO", "tbd"}:
        fail("version", "version must be a non-placeholder semver-like string")

    if agent.owner in PLACEHOLDER_OWNERS:
        fail("owner_placeholder", f"owner is placeholder/empty: {agent.owner!r}")
    elif agent.owner != "gio":
        fail("owner", f"owner must be 'gio' for Nortiqa staging candidates; got {agent.owner!r}")

    if agent.status not in VALID_STATUSES:
        fail("status", f"status must be one of {sorted(VALID_STATUSES)}; got {agent.status!r}")
    elif agent.status not in EVALUATOR_ALLOWED_STATUSES:
        fail(
            "status_premature",
            f"status={agent.status!r} requires Gio; acceptance candidates must be draft|reviewed",
        )

    role = agent.role
    if role not in ROLE_REQUIRED_TOOLS:
        fail("role", f"Unknown or unsupported role: {role!r}")
    else:
        tools = set(agent.tools)
        missing = ROLE_REQUIRED_TOOLS[role] - tools
        if missing:
            fail("tools_missing", f"Role {role} missing required tools: {sorted(missing)}")
        forbidden = ROLE_FORBIDDEN_TOOLS[role] & tools
        if forbidden:
            fail("tools_incompatible", f"Role {role} has incompatible tools: {sorted(forbidden)}")

    scope = fm.get("scope") or {}
    if not isinstance(scope, dict):
        fail("scope", "scope must be a mapping with read/write lists")
    else:
        for key in ("read", "write"):
            if key not in scope:
                fail("scope", f"scope.{key} is required")
            elif not isinstance(scope[key], list):
                fail("scope", f"scope.{key} must be a list")
        if role in {"inspector", "tester", "code-reviewer", "security-reviewer"}:
            write = scope.get("write") or []
            # readonly roles may write only results/drafts
            for path in write:
                p = str(path)
                if "results" not in p and ".drafts" not in p:
                    fail("scope_write", f"Readonly-ish role {role} has non-results write path: {p}")
        if role == "inspector" and (scope.get("write") or []):
            fail("scope_write", "inspector must have empty scope.write")

    missing_univ = UNIVERSAL_PROHIBITIONS - agent.prohibitions
    if missing_univ:
        fail("prohibitions", f"Missing universal prohibitions: {sorted(missing_univ)}")

    refs = fm.get("governance_refs") or []
    if not isinstance(refs, list):
        fail("governance_refs", "governance_refs must be a list")
    else:
        refset = {str(r) for r in refs}
        missing_refs = REQUIRED_GOVERNANCE - refset
        if missing_refs:
            fail("governance_refs", f"Missing governance refs: {sorted(missing_refs)}")
        for ref in refs:
            path = ROOT / str(ref)
            if not path.exists():
                fail("governance_ref_missing", f"Referenced path does not exist: {ref}")

    sep = fm.get("separation") or {}
    if not isinstance(sep, dict):
        fail("separation", "separation must be a mapping")
    else:
        for key in ("technical_dictamen", "institutional_approval", "production_authority"):
            if key not in sep:
                fail("separation", f"separation.{key} is required")
        if sep.get("institutional_approval") is True:
            fail(
                "separation_institutional",
                "institutional_approval must be false in manifest; only Gio approves",
            )
        if sep.get("production_authority") is True:
            fail(
                "separation_production",
                "production_authority must be false; production is out of acceptance scope",
            )
        if role in {"inspector", "tester", "code-reviewer", "security-reviewer"}:
            if sep.get("technical_dictamen") is not True:
                fail("separation_dictamen", f"{role} must set technical_dictamen: true")

    # Ambiguous permission language in body
    body_l = agent.body.lower()
    if "auto-approve" in body_l or "autoaprove" in body_l or "me autoapruebo" in body_l:
        fail("ambiguous_approval", "Body suggests auto-approval")
    if "production-approved" in body_l and "cannot" not in body_l and "reserved" not in body_l:
        warn("body_production", "Body mentions production-approved; ensure it is clearly forbidden")

    return findings


def verdict_for(findings: list[dict]) -> str:
    errors = [f for f in findings if f["level"] == "error"]
    warnings = [f for f in findings if f["level"] == "warning"]
    if errors:
        return "RECHAZADO"
    if warnings:
        return "APTO CON OBSERVACIONES"
    return "APTO PARA RATIFICACIÓN DE STAGING"


def main() -> int:
    ensure_dirs()
    agents = load_all_agents()
    report = {
        "validator": "validate_agents.py",
        "agents_dir": str(ROOT / ".github" / "agents"),
        "count": len(agents),
        "agents": [],
        "ok": True,
    }

    if not agents:
        report["ok"] = False
        report["error"] = "No *.agent.md files found"
        out = RESULTS_DIR / "validation.json"
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 1

    exit_code = 0
    for agent in agents:
        findings = check_manifest(agent)
        v = verdict_for(findings)
        # Validation-only technical gate; institutional status stays draft until Gio.
        entry = {
            "file": str(agent.path.relative_to(ROOT)),
            "name": agent.name,
            "role": agent.role,
            "owner": agent.owner,
            "status": agent.status,
            "validation_verdict": v,
            "findings": findings,
        }
        report["agents"].append(entry)
        if any(f["level"] == "error" for f in findings):
            exit_code = 1
            report["ok"] = False
        print(f"[VALIDATE] {agent.name or agent.path.name}: {v} ({len(findings)} findings)")

    out = RESULTS_DIR / "validation.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
