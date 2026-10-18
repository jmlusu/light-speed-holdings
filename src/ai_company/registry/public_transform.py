"""Public allowlist transform — company-registry.yaml → agent-registry.public.json.

Implements PUBLIC_AGENT_REGISTRY_SCHEMA.md §5 (build-time pipeline):
load → count gate → allowlist project → tool normalize → PII scan →
denylist scan → write → self-validate.

Deny by default: only fields on the PUBLIC allowlist reach the sink.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ai_company.paths import get_project_root
from ai_company.registry.loader import load_yaml_cached

logger = logging.getLogger(__name__)

SCHEMA_VERSION = "1.0.0"
DEFAULT_SOURCE = "company-registry.yaml"
DEFAULT_SINK = "src/data/generated/agent-registry.public.json"

CANONICAL_TOOLS: frozenset[str] = frozenset(
    {"read", "edit", "grep", "list", "bash", "webfetch", "task"}
)

TOOL_ALIASES: dict[str, str] = {
    "write": "edit",
    "execute": "bash",
    "delegate": "task",
    "web_search": "webfetch",
    "websearch": "webfetch",
}

FORBIDDEN_TOOL = "code_interpreter"

# Keys that must never appear on any public agent object.
AGENT_DENYLIST: frozenset[str] = frozenset(
    {
        "guidelines",
        "permission",
        "model_tier",
        "approval_level",
        "escalation_path",
        "workflows",
        "inputs",
        "outputs",
        "initialTasks",
        "initialApprovals",
        "initialEscalations",
        "secret",
        "token",
        "api_key",
        "cost",
        "budget",
        "direct_reports",
    }
)

# Structural keys that must never appear anywhere in the public envelope.
STRUCTURAL_DENY: frozenset[str] = frozenset(
    {
        "guidelines",
        "permission",
        "model_tier",
        "approval_level",
        "escalation_path",
        "workflows",
        "inputs",
        "outputs",
        "initialTasks",
        "initialApprovals",
        "initialEscalations",
        "direct_reports",
        "secret",
        "token",
        "api_key",
    }
)

# Value-level patterns: secrets / removed tools must not appear in any string.
VALUE_DENY_PATTERNS: tuple[str, ...] = (
    r"\bDASHBOARD_[A-Z_]+\b",
    r"\b[A-Z0-9_]*API_KEY[A-Z0-9_]*\b",
    r"\bcode_interpreter\b",
    r"\bsk-ant-[A-Za-z0-9-]+\b",
    r"\bghp_[A-Za-z0-9]+\b",
    r"\bAKIA[0-9A-Z]{16}\b",
)

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TYPE_CENSUS = {"executive": 19, "specialist": 64, "board": 7}
EXPECTED_AGENTS = 90
EXPECTED_DEPARTMENTS = 20
ENVELOPE_REQUIRED = (
    "schema_version",
    "generated_at",
    "source",
    "meta",
    "agents",
    "departments",
)


class PublicTransformError(RuntimeError):
    """Raised when the public artifact would violate the allowlist contract."""


def _kebab(value: str) -> str:
    return value.replace("_", "-").lower() if value else ""


def _normalize_type(raw: str) -> str:
    t = (raw or "specialist").strip().lower()
    if t in ("executive", "specialist", "board"):
        return t
    if t in ("ai", "default", "manager"):
        return "specialist"
    if t in ("human", "ceo"):
        return "executive"
    return t if t in TYPE_CENSUS else "specialist"


def normalize_tools(tools: Any) -> list[str]:
    """Remap aliases to canonical 7; hard-fail on code_interpreter; drop unknown."""
    if not isinstance(tools, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for raw in tools:
        if not isinstance(raw, str):
            continue
        name = raw.strip().lower()
        if name == FORBIDDEN_TOOL:
            raise PublicTransformError(
                f"Rejected tool '{FORBIDDEN_TOOL}' (removed vocabulary; not an alias)"
            )
        name = TOOL_ALIASES.get(name, name)
        if name in CANONICAL_TOOLS and name not in seen:
            seen.add(name)
            out.append(name)
    return out


def _load_registry_agents(yaml_path: Path) -> list[dict[str, Any]]:
    data = load_yaml_cached(yaml_path)
    if data is None:
        raise PublicTransformError(f"Registry not found: {yaml_path}")
    agents = data.get("company", {}).get("agents", []) if isinstance(data, dict) else data
    if not isinstance(agents, list):
        raise PublicTransformError("company.agents is not a list")
    return [a for a in agents if isinstance(a, dict)]


def _load_departments(path: Path) -> list[dict[str, Any]]:
    data = load_yaml_cached(path)
    if data is None:
        raise PublicTransformError(f"Departments file not found: {path}")
    if isinstance(data, dict):
        items = data.get("departments", [])
        if isinstance(items, dict):
            # company/config shape: {departments: {id: {...}}}
            result = []
            for did, body in items.items():
                row = dict(body) if isinstance(body, dict) else {}
                row.setdefault("id", did)
                result.append(row)
            return result
        if isinstance(items, list):
            return [d for d in items if isinstance(d, dict)]
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    raise PublicTransformError("Unrecognized departments shape")


def _dept_maps(
    departments: list[dict[str, Any]],
) -> tuple[dict[str, str], dict[str, str]]:
    """Return (id→name, name_lower→id)."""
    by_id: dict[str, str] = {}
    by_name: dict[str, str] = {}
    for d in departments:
        did = str(d.get("id", ""))
        dname = str(d.get("name", did))
        if did:
            by_id[did] = dname
            by_name[dname.lower()] = did
    return by_id, by_name


def _project_agent(
    agent: dict[str, Any],
    *,
    dept_id_by_name: dict[str, str],
    dept_id_by_id: dict[str, str],
) -> dict[str, Any]:
    yaml_id = str(agent.get("id", ""))
    public_id = _kebab(yaml_id)
    name = str(agent.get("name") or yaml_id)
    title = str(agent.get("title") or name)
    description = str(agent.get("description") or agent.get("mission") or "")
    if not description:
        raise PublicTransformError(f"Agent '{yaml_id}' missing description/mission")
    if not public_id:
        raise PublicTransformError("Agent missing id")

    raw_dept = str(agent.get("department") or "")
    if raw_dept in dept_id_by_name:
        department_id = raw_dept
    elif raw_dept.lower() in dept_id_by_name:
        department_id = dept_id_by_name[raw_dept.lower()]
    elif raw_dept in dept_id_by_id:
        department_id = raw_dept
    else:
        # Allow display-only departments that already match an id
        department_id = raw_dept.replace(" ", "_").lower() if raw_dept else ""
    department_display = dept_id_by_id.get(department_id, raw_dept) if department_id else raw_dept
    if not department_display:
        raise PublicTransformError(f"Agent '{yaml_id}' missing department")

    reports_raw = str(agent.get("reports_to") or "")
    reports_to: str | None = _kebab(reports_raw) if reports_raw else None
    if public_id == "board-chair" and not reports_raw:
        reports_to = None

    agent_type = _normalize_type(str(agent.get("type", "specialist")))

    public: dict[str, Any] = {
        "id": public_id,
        "name": name,
        "title": title,
        "type": agent_type,
        "department": department_display,
        "department_id": department_id or _kebab(department_display),
        "reports_to": reports_to,
        "mission": description,
    }

    if yaml_id == "human_ceo":
        public["is_human"] = True

    tools = normalize_tools(agent.get("tools"))
    if tools:
        public["tools"] = tools

    kpis = agent.get("kpis")
    if isinstance(kpis, list) and kpis:
        labels = [str(k) for k in kpis if isinstance(k, str) and k.strip()]
        if labels:
            public["kpi_labels"] = labels

    rights = agent.get("decision_rights")
    if isinstance(rights, list) and rights:
        cleaned = [str(r) for r in rights if isinstance(r, str) and r.strip()]
        if cleaned:
            public["decision_rights"] = cleaned

    resp = agent.get("responsibilities")
    if isinstance(resp, list) and resp:
        cleaned = [str(r) for r in resp if isinstance(r, str) and r.strip()]
        if cleaned:
            public["responsibilities"] = cleaned

    tech = agent.get("technical_domain")
    if isinstance(tech, str) and tech.strip():
        public["technical_domain"] = tech

    # Strip any accidentally copied denylisted keys (defense in depth).
    for bad in list(public.keys()):
        if bad in AGENT_DENYLIST:
            del public[bad]

    return public


def _project_department(d: dict[str, Any]) -> dict[str, Any]:
    did = str(d.get("id", ""))
    if not did:
        raise PublicTransformError("Department missing id")
    return {
        "id": did,
        "name": str(d.get("name") or did),
        "executive": _kebab(str(d.get("executive") or "")),
        "mission": str(d.get("mission") or d.get("description") or ""),
        "budget_category": str(d.get("budget_category") or "operations"),
        "headcount_target": int(d.get("headcount_target") or 0),
    }


def _count_gate(agents: list[dict[str, Any]], departments: list[dict[str, Any]]) -> None:
    if len(agents) != EXPECTED_AGENTS:
        raise PublicTransformError(f"Agent count {len(agents)} != {EXPECTED_AGENTS}")
    if len(departments) != EXPECTED_DEPARTMENTS:
        raise PublicTransformError(f"Department count {len(departments)} != {EXPECTED_DEPARTMENTS}")
    census: dict[str, int] = {"executive": 0, "specialist": 0, "board": 0}
    ids: set[str] = set()
    for a in agents:
        aid = _kebab(str(a.get("id", "")))
        if not aid:
            raise PublicTransformError("Agent missing id in count gate")
        if aid in ids:
            raise PublicTransformError(f"Duplicate agent id: {aid}")
        ids.add(aid)
        t = _normalize_type(str(a.get("type", "specialist")))
        if t not in census:
            raise PublicTransformError(f"Invalid type '{t}' for {aid}")
        census[t] += 1
    if census != TYPE_CENSUS:
        raise PublicTransformError(f"Type census {census} != expected {TYPE_CENSUS}")


def _denylist_scan(envelope: dict[str, Any]) -> None:
    """Deny by default: no structural deny keys; no secret-like values."""

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, val in node.items():
                if key in STRUCTURAL_DENY:
                    raise PublicTransformError(f"Denylisted key '{key}' at {path}")
                walk(val, f"{path}.{key}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{path}[{i}]")
        elif isinstance(node, str):
            for pattern in VALUE_DENY_PATTERNS:
                if re.search(pattern, node):
                    raise PublicTransformError(f"Denylisted value /{pattern}/ at {path}")

    walk(envelope, "$")


def _pii_scan(serialized: str) -> None:
    try:
        from ai_company.security.pii_detector import PIIDetector
    except ImportError:
        logger.warning("pii_detector unavailable; skipping PII scan")
        return
    detector = PIIDetector()
    result = detector.scan(serialized)
    if result.has_pii:
        kinds = sorted(t.value for t in result.pii_types_found)
        raise PublicTransformError(f"PII/content filter hit: {kinds}")


def _self_validate(envelope: dict[str, Any]) -> None:
    missing = [k for k in ENVELOPE_REQUIRED if k not in envelope]
    if missing:
        raise PublicTransformError(f"Envelope missing keys: {missing}")
    meta = envelope.get("meta") or {}
    if "agents" not in meta or "departments" not in meta:
        raise PublicTransformError("Envelope meta missing agents/departments counts")
    agents = envelope["agents"]
    departments = envelope["departments"]
    if not isinstance(agents, list) or not isinstance(departments, list):
        raise PublicTransformError("agents/departments must be arrays")
    if meta["agents"] != len(agents) or meta["departments"] != len(departments):
        raise PublicTransformError("meta counts do not match array lengths")

    required_agent = (
        "id",
        "name",
        "title",
        "type",
        "department",
        "reports_to",
        "mission",
    )
    census = {"executive": 0, "specialist": 0, "board": 0}
    seen_ids: set[str] = set()
    for a in agents:
        for key in required_agent:
            if key not in a:
                raise PublicTransformError(f"PublicAgent missing required '{key}'")
        if a["type"] not in ("executive", "specialist", "board"):
            raise PublicTransformError(f"Invalid type on {a.get('id')}")
        if not KEBAB_RE.match(str(a["id"])):
            raise PublicTransformError(f"Non-kebab id: {a['id']}")
        if a["id"] in seen_ids:
            raise PublicTransformError(f"Duplicate public id: {a['id']}")
        seen_ids.add(a["id"])
        census[a["type"]] += 1
        tools = a.get("tools")
        if tools is not None and (not isinstance(tools, list) or not set(tools) <= CANONICAL_TOOLS):
            raise PublicTransformError(f"Non-canonical tools on {a['id']}: {tools}")
        for bad in AGENT_DENYLIST:
            if bad in a:
                raise PublicTransformError(f"Denylisted key '{bad}' on agent {a['id']}")
        if a["id"] != "board-chair" and not a["reports_to"]:
            raise PublicTransformError(f"Empty reports_to on {a['id']}")
    if census != TYPE_CENSUS:
        raise PublicTransformError(f"Post-validate census {census} != {TYPE_CENSUS}")


def transform_public_registry(
    yaml_path: str | Path | None = None,
    departments_path: str | Path | None = None,
    sink_path: str | Path | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build the public allowlist artifact and write it atomically.

    Idempotent: when ``generated_at`` is omitted, reuses the timestamp from an
    existing sink so two consecutive runs produce byte-identical content.
    """
    root = get_project_root()
    yaml_path = Path(yaml_path) if yaml_path else root / DEFAULT_SOURCE
    departments_path = (
        Path(departments_path) if departments_path else root / "company" / "departments.yaml"
    )
    sink_path = Path(sink_path) if sink_path else root / DEFAULT_SINK

    agents_raw = _load_registry_agents(yaml_path)
    departments_raw = _load_departments(departments_path)

    # Count gate on raw source (pre-projection types).
    _count_gate(agents_raw, departments_raw)

    dept_id_by_id, dept_id_by_name = _dept_maps(departments_raw)

    public_agents = [
        _project_agent(a, dept_id_by_name=dept_id_by_name, dept_id_by_id=dept_id_by_id)
        for a in agents_raw
    ]
    public_departments = [_project_department(d) for d in departments_raw]

    # Preserve prior generated_at for idempotent double-runs.
    if generated_at is None:
        generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        if sink_path.exists():
            try:
                prior = json.loads(sink_path.read_text(encoding="utf-8"))
                prior_ts = prior.get("generated_at")
                if (
                    isinstance(prior_ts, str)
                    and prior_ts
                    and prior.get("agents") == public_agents
                    and prior.get("departments") == public_departments
                ):
                    generated_at = prior_ts
            except (json.JSONDecodeError, OSError):
                pass

    envelope: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "source": DEFAULT_SOURCE,
        "meta": {
            "agents": len(public_agents),
            "departments": len(public_departments),
        },
        "agents": public_agents,
        "departments": public_departments,
    }

    serialized = json.dumps(envelope, indent=2, ensure_ascii=False, sort_keys=False)
    serialized += "\n"

    _denylist_scan(envelope)
    _pii_scan(serialized)
    _self_validate(envelope)

    sink_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = sink_path.with_suffix(sink_path.suffix + ".tmp")
    tmp.write_text(serialized, encoding="utf-8")
    tmp.replace(sink_path)

    logger.info(
        "Wrote public registry: %s (%d agents, %d departments)",
        sink_path,
        len(public_agents),
        len(public_departments),
    )
    return envelope


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    try:
        transform_public_registry()
    except PublicTransformError as exc:
        logger.error("Public transform failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
