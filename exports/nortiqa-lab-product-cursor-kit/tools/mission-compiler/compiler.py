"""Heuristic NL → mission-contract.v0 compiler (dry-run only; no side effects)."""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime, timezone
from typing import Any


ENTITY_BLOCK = [
    "valent",
    "erp gio",
    "erp gio+edson",
    "surlancer",
    "vialidad nacional",
    "lla santa cruz",
]

PROD_LIKE = [
    "produccion",
    "producción",
    "production",
    "nginx",
    "dns",
    "reload",
    "reinicia",
    "reiniciá",
    "reiniciar",
    "secret",
    "chmod",
    "migrate",
    "migracion",
    "migración",
    "docker system prune",
    "drop database",
    "promote",
]

OPS_DIAG = [
    "diagnos",
    "por que falla",
    "por qué falla",
    "health",
    "inspeccion",
    "inspección",
    "revisa el estado",
    "status",
]

DOCS_WRITE = [
    "readme",
    "document",
    "docs/",
    "mejorá",
    "mejora",
    "actualizá",
    "actualiza",
    "handoff",
    "changelog",
    "markdown",
    "agrega",
    "añadí",
    "añadi",
]

ANALYZE_ONLY = [
    "explica",
    "qué es",
    "que es",
    "analiza",
    "analizá",
    "resumi",
    "resumí",
    "compará",
    "compara",
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _slugify(text: str, max_len: int = 40) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if not text:
        text = "mission"
    return text[:max_len].strip("-") or "mission"


def _contains_any(hay: str, needles: list[str]) -> bool:
    return any(n in hay for n in needles)


def classify(raw: str) -> dict[str, Any]:
    """Return classification signals used to build the contract."""
    hay = raw.lower()
    signals: list[str] = []

    if _contains_any(hay, ENTITY_BLOCK):
        return {
            "kind": "entity_block",
            "autonomy_level": 0,
            "status": "blocked",
            "risk": "critical",
            "zone": "red",
            "dispatch": "D",
            "signals": ["entity_risk"],
            "write": False,
            "network": "none",
        }

    if _contains_any(hay, PROD_LIKE):
        return {
            "kind": "prod_like",
            "autonomy_level": 5,
            "status": "awaiting_human",
            "risk": "critical",
            "zone": "red",
            "dispatch": "E",
            "signals": ["scope_unclear"] if "staging" not in hay else [],
            "write": False,
            "network": "prod_readonly",
            "human_gate": {
                "id": "hg-prod",
                "when": "before_prod",
                "question": "¿Autorizás ejecución en superficie prod-like? El dry-run no ejecutará nada.",
                "required": True,
                "status": "pending",
                "decided_by": None,
                "decided_at": None,
            },
        }

    if _contains_any(hay, DOCS_WRITE) and not _contains_any(hay, ANALYZE_ONLY):
        return {
            "kind": "docs_write",
            "autonomy_level": 2,
            "status": "planned",
            "risk": "low",
            "zone": "green",
            "dispatch": "C",
            "signals": [],
            "write": True,
            "network": "none",
        }

    if _contains_any(hay, OPS_DIAG):
        return {
            "kind": "ops_diag",
            "autonomy_level": 1,
            "status": "planned",
            "risk": "low",
            "zone": "green",
            "dispatch": "A",
            "signals": [],
            "write": False,
            "network": "public_readonly",
        }

    if _contains_any(hay, ANALYZE_ONLY):
        return {
            "kind": "analyze",
            "autonomy_level": 0,
            "status": "planned",
            "risk": "low",
            "zone": "green",
            "dispatch": "A",
            "signals": [],
            "write": False,
            "network": "none",
        }

    # Ambiguous → conservative draft
    signals.append("ambiguous_intent")
    return {
        "kind": "ambiguous",
        "autonomy_level": 1,
        "status": "draft",
        "risk": "medium",
        "zone": "yellow",
        "dispatch": "B",
        "signals": signals,
        "write": False,
        "network": "none",
        "autonomy_floor": 1,
    }


def compile_request(
    raw_request: str,
    *,
    requester: str = "Gio",
    channel: str = "cursor",
    repo: str = "nortiqa-lab/.github",
) -> dict[str, Any]:
    raw_request = (raw_request or "").strip()
    if not raw_request:
        raise ValueError("raw_request must be non-empty")

    cls = classify(raw_request)
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    slug = _slugify(raw_request)
    mission_id = f"MIS-NL-{day}-{slug}"

    write = bool(cls["write"])
    level = int(cls["autonomy_level"])
    status = cls["status"]
    human_gates = []
    if cls.get("human_gate"):
        human_gates.append(cls["human_gate"])

    if status == "blocked":
        plan = [
            {
                "step": 1,
                "action": "STOP — posible contaminación de entidad; escalar a Gio",
                "owner_role": "NL-AUDITOR",
                "produces": "bloqueo documentado",
                "requires_human": True,
            }
        ]
        rollback = {
            "strategy": "none_readonly",
            "steps": ["no side effects"],
            "restore_point_required": False,
        }
        paths_allowed: list[str] = []
        evidence_kind = "handoff"
        objective = "Bloquear pedido fuera de Nortiqa Lab y escalar"
    elif cls["kind"] == "prod_like":
        plan = [
            {
                "step": 1,
                "action": "Emitir contrato y esperar autorización humana (dry-run: no ejecutar)",
                "owner_role": "NL-ORCH",
                "produces": "gate before_prod",
                "requires_human": True,
            },
            {
                "step": 2,
                "action": "Si se autoriza en runtime futuro: plan OPS con rollback (fuera de este dry-run)",
                "owner_role": "NL-OPS",
                "produces": "plan OPS draft",
                "requires_human": True,
            },
        ]
        rollback = {
            "strategy": "manual",
            "steps": ["restore point + rollback OPS documentado antes de cualquier ejecución"],
            "restore_point_required": True,
        }
        paths_allowed = []
        evidence_kind = "before_after"
        objective = f"Operación prod-like (dry-run only): {raw_request[:160]}"
    elif cls["kind"] == "docs_write":
        plan = [
            {
                "step": 1,
                "action": "Inspeccionar archivos en scope",
                "owner_role": "NL-BUILDER",
                "produces": "diagnóstico",
                "requires_human": False,
            },
            {
                "step": 2,
                "action": "Proponer/aplicar cambio reversible en docs/kit",
                "owner_role": "NL-BUILDER",
                "produces": "diff",
                "requires_human": False,
            },
            {
                "step": 3,
                "action": "Verificar paths y consistencia de enlaces",
                "owner_role": "NL-BUILDER",
                "produces": "test_result",
                "requires_human": False,
            },
        ]
        rollback = {
            "strategy": "git_revert",
            "steps": ["git revert del commit de la misión"],
            "restore_point_required": False,
        }
        paths_allowed = ["docs/", "agents/", "AGENTS.md", "profile/"]
        evidence_kind = "diff"
        objective = f"Cambio documental reversible: {raw_request[:160]}"
    elif cls["kind"] == "ops_diag":
        plan = [
            {
                "step": 1,
                "action": "Lectura de docs/runbooks y health GETs públicos si aplica",
                "owner_role": "NL-OPS",
                "produces": "diagnóstico",
                "requires_human": False,
            }
        ]
        rollback = {
            "strategy": "none_readonly",
            "steps": ["solo lectura"],
            "restore_point_required": False,
        }
        paths_allowed = ["agents/", "docs/", "server-ops/"]
        evidence_kind = "http"
        objective = f"Diagnóstico sin side effects: {raw_request[:160]}"
    else:
        plan = [
            {
                "step": 1,
                "action": "Analizar pedido y completar contrato (sin side effects)",
                "owner_role": "NL-ORCH",
                "produces": "contrato refinable",
                "requires_human": False,
            }
        ]
        rollback = {
            "strategy": "none_readonly",
            "steps": ["solo lectura / análisis"],
            "restore_point_required": False,
        }
        paths_allowed = ["docs/", "agents/"]
        evidence_kind = "handoff"
        objective = f"Análisis / draft: {raw_request[:160]}"

    autonomy_floor = int(cls.get("autonomy_floor", level))
    if cls.get("signals"):
        level = min(level, autonomy_floor)

    files_est = 1 if write else 0
    services_est = 1 if cls["kind"] == "prod_like" else 0

    contract: dict[str, Any] = {
        "schema_version": "mission-contract.v0",
        "mission_id": mission_id,
        "created_at": _now_iso(),
        "entity": "nortiqa-lab",
        "source": {
            "channel": channel,
            "raw_request": raw_request,
            "requester": requester,
            "parent_mission_id": None,
        },
        "objective": objective,
        "success_criteria": [
            {
                "id": "sc1",
                "description": "Contrato válido emitido en dry-run (sin side effects)",
                "observable": "JSON valida contra mission-contract.v0 structural checks",
            }
        ],
        "assumptions": [
            "Dry-run compiler only — does not authorize or perform execution",
            "Heuristic classification v0; refine before privileged work",
        ],
        "scope": {
            "repos": [repo],
            "paths_allowed": paths_allowed,
            "paths_denied": [".env", ".secrets/", "/opt/"],
            "services_allowed": [],
            "data_classes": ["public", "internal"],
            "out_of_scope": [
                "Privileged VPS execution",
                "Notion protected writes",
                "Secret rotation",
                "Non-Nortiqa entities",
            ],
        },
        "risk": {
            "level": cls["risk"],
            "rationale": f"classifier kind={cls['kind']}",
            "blast_radius": {
                "files_estimate": files_est,
                "services_estimate": services_est,
                "reversible": cls["kind"] != "prod_like",
            },
        },
        "autonomy_level": level,
        "autonomy_zone_kit": cls["zone"],
        "dispatch_class": cls["dispatch"],
        "permissions": {
            "read": True,
            "write": write,
            "exec": False,
            "network": cls["network"],
            "secrets": "none",
        },
        "roles": {
            "planner": "NL-ORCH",
            "executor": "NL-BUILDER" if write else "NL-ORCH",
            "tester": "NL-BUILDER",
            "security_reviewer": "NL-AUDITOR",
            "arbiter": "NL-AUDITOR",
            "human_approver": "Gio",
        },
        "plan": plan,
        "rollback": rollback,
        "tests": [
            {
                "id": "t-dry-run",
                "type": "structure",
                "command_or_check": "tools/mission-compiler/compile.py --self-test",
                "expected": "exit 0",
            }
        ],
        "budget": {
            "time_minutes_max": 30 if level <= 2 else 60,
            "tokens_max": 100000,
            "money_usd_max": 0,
            "model_preference": [],
        },
        "evidence_required": [
            {
                "id": "e1",
                "kind": evidence_kind,
                "description": "Evidencia observable acorde al tipo de misión (runtime futuro)",
                "required_for_close": True,
            },
            {
                "id": "e2",
                "kind": "handoff",
                "description": "Handoff o registro de dry-run",
                "required_for_close": True,
            },
        ],
        "human_gates": human_gates,
        "status": status,
        "uncertainty": {
            "score": 0.2 if not cls.get("signals") else 0.6,
            "signals": cls.get("signals") or [],
            "autonomy_floor": autonomy_floor,
        },
        "closeout": None,
        "black_box_ref": None,
    }
    # Attach classifier kind for CLI envelope (not part of schema object).
    contract["__classifier_kind"] = cls["kind"]
    return contract
