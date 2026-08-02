"""Lightweight structural validator for mission-contract.v0 (stdlib only)."""

from __future__ import annotations

import re
from typing import Any


MISSION_ID_RE = re.compile(r"^MIS-NL-[0-9]{8}-[a-z0-9-]{2,48}$")

REQUIRED_TOP = [
    "schema_version",
    "mission_id",
    "created_at",
    "entity",
    "source",
    "objective",
    "success_criteria",
    "scope",
    "risk",
    "autonomy_level",
    "permissions",
    "plan",
    "rollback",
    "budget",
    "evidence_required",
    "human_gates",
    "status",
]

STATUS_ENUM = {
    "draft",
    "awaiting_human",
    "planned",
    "simulating",
    "authorized",
    "executing",
    "verifying",
    "blocked",
    "failed",
    "rolled_back",
    "closed_verified",
    "cancelled",
}

CHANNEL_ENUM = {"chat", "telegram", "cursor", "api", "handoff", "other"}
RISK_ENUM = {"low", "medium", "high", "critical"}
NETWORK_ENUM = {"none", "public_readonly", "staging", "prod_readonly", "prod_write"}
SECRETS_ENUM = {"none", "reference_only", "use_existing", "rotate_forbidden"}
DATA_CLASSES = {"public", "internal", "secret", "personal", "client"}
EVIDENCE_KINDS = {
    "diff",
    "test_result",
    "before_after",
    "pid_restart",
    "http",
    "functional",
    "screenshot_or_human_accept",
    "no_contamination",
    "handoff",
    "other",
}
ROLLBACK_STRATEGIES = {
    "git_revert",
    "file_restore",
    "service_restart",
    "backup_restore",
    "none_readonly",
    "manual",
}


def _err(path: str, msg: str) -> str:
    return f"{path}: {msg}"


def validate_contract(contract: dict[str, Any]) -> list[str]:
    """Return a list of validation errors (empty means OK for v0 structural checks)."""
    errors: list[str] = []

    if not isinstance(contract, dict):
        return ["$: contract must be an object"]

    for key in REQUIRED_TOP:
        if key not in contract:
            errors.append(_err(key, "required field missing"))

    if contract.get("schema_version") != "mission-contract.v0":
        errors.append(_err("schema_version", "must be 'mission-contract.v0'"))

    if contract.get("entity") != "nortiqa-lab":
        errors.append(_err("entity", "must be 'nortiqa-lab'"))

    mid = contract.get("mission_id")
    if not isinstance(mid, str) or not MISSION_ID_RE.match(mid):
        errors.append(_err("mission_id", "must match MIS-NL-YYYYMMDD-<slug>"))

    if not isinstance(contract.get("objective"), str) or not contract.get("objective"):
        errors.append(_err("objective", "must be non-empty string"))

    status = contract.get("status")
    if status not in STATUS_ENUM:
        errors.append(_err("status", f"invalid status {status!r}"))

    level = contract.get("autonomy_level")
    if not isinstance(level, int) or level < 0 or level > 5:
        errors.append(_err("autonomy_level", "must be int 0..5"))

    source = contract.get("source")
    if not isinstance(source, dict):
        errors.append(_err("source", "must be object"))
    else:
        for k in ("channel", "raw_request", "requester"):
            if k not in source:
                errors.append(_err(f"source.{k}", "required"))
        if source.get("channel") not in CHANNEL_ENUM:
            errors.append(_err("source.channel", "invalid enum"))
        if not isinstance(source.get("raw_request"), str) or not source.get("raw_request"):
            errors.append(_err("source.raw_request", "must be non-empty string"))

    criteria = contract.get("success_criteria")
    if not isinstance(criteria, list) or len(criteria) < 1:
        errors.append(_err("success_criteria", "must be non-empty array"))
    else:
        for i, item in enumerate(criteria):
            if not isinstance(item, dict):
                errors.append(_err(f"success_criteria[{i}]", "must be object"))
                continue
            for k in ("id", "description", "observable"):
                if k not in item or not item[k]:
                    errors.append(_err(f"success_criteria[{i}].{k}", "required non-empty"))

    scope = contract.get("scope")
    if not isinstance(scope, dict):
        errors.append(_err("scope", "must be object"))
    else:
        for k in ("repos", "paths_allowed", "services_allowed", "data_classes", "out_of_scope"):
            if k not in scope:
                errors.append(_err(f"scope.{k}", "required"))
        for dc in scope.get("data_classes") or []:
            if dc not in DATA_CLASSES:
                errors.append(_err("scope.data_classes", f"invalid {dc!r}"))

    risk = contract.get("risk")
    if not isinstance(risk, dict):
        errors.append(_err("risk", "must be object"))
    else:
        if risk.get("level") not in RISK_ENUM:
            errors.append(_err("risk.level", "invalid enum"))
        br = risk.get("blast_radius")
        if not isinstance(br, dict):
            errors.append(_err("risk.blast_radius", "must be object"))
        else:
            for k in ("files_estimate", "services_estimate", "reversible"):
                if k not in br:
                    errors.append(_err(f"risk.blast_radius.{k}", "required"))

    perms = contract.get("permissions")
    if not isinstance(perms, dict):
        errors.append(_err("permissions", "must be object"))
    else:
        for k in ("read", "write", "exec", "network", "secrets"):
            if k not in perms:
                errors.append(_err(f"permissions.{k}", "required"))
        if perms.get("network") not in NETWORK_ENUM:
            errors.append(_err("permissions.network", "invalid enum"))
        if perms.get("secrets") not in SECRETS_ENUM:
            errors.append(_err("permissions.secrets", "invalid enum"))

    plan = contract.get("plan")
    if not isinstance(plan, list) or len(plan) < 1:
        errors.append(_err("plan", "must be non-empty array"))
    else:
        for i, step in enumerate(plan):
            if not isinstance(step, dict):
                errors.append(_err(f"plan[{i}]", "must be object"))
                continue
            for k in ("step", "action", "owner_role", "produces"):
                if k not in step:
                    errors.append(_err(f"plan[{i}].{k}", "required"))

    rollback = contract.get("rollback")
    if not isinstance(rollback, dict):
        errors.append(_err("rollback", "must be object"))
    else:
        if rollback.get("strategy") not in ROLLBACK_STRATEGIES:
            errors.append(_err("rollback.strategy", "invalid enum"))
        if "steps" not in rollback or "restore_point_required" not in rollback:
            errors.append(_err("rollback", "steps and restore_point_required required"))

    budget = contract.get("budget")
    if not isinstance(budget, dict):
        errors.append(_err("budget", "must be object"))
    else:
        for k in ("time_minutes_max", "tokens_max", "money_usd_max"):
            if k not in budget:
                errors.append(_err(f"budget.{k}", "required"))

    evidence = contract.get("evidence_required")
    if not isinstance(evidence, list) or len(evidence) < 1:
        errors.append(_err("evidence_required", "must be non-empty array"))
    else:
        for i, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(_err(f"evidence_required[{i}]", "must be object"))
                continue
            for k in ("id", "kind", "description"):
                if k not in item:
                    errors.append(_err(f"evidence_required[{i}].{k}", "required"))
            if item.get("kind") not in EVIDENCE_KINDS:
                errors.append(_err(f"evidence_required[{i}].kind", "invalid enum"))

    if "human_gates" not in contract or not isinstance(contract.get("human_gates"), list):
        errors.append(_err("human_gates", "must be array"))

    return errors
