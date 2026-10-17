"""One-shot T003 backfill: add 4 MANDATORY governance fields to all 90 agents.

Fields: decision_rights, approval_level, escalation_path, kpis.
Idempotent: re-running leaves already-populated fields intact (unless force).
Run: uv run python harness/changes/active/scripts/backfill_governance_fields.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

MANDATORY = ("decision_rights", "approval_level", "escalation_path", "kpis")

# Registry display-name -> kpis.yaml id (only where kpis.yaml has coverage).
DEPT_TO_KPI_ID = {
    "Engineering": "engineering",
    "People": "hr",
    "Marketing": "marketing",
    "Sales": "sales",
    "Customer Success": "customer_success",
    "Legal": "legal",
    "Finance": "finance",
    "DevOps": "devops",
}

# Authored fallback KPI labels for depts not covered by kpis.yaml.
FALLBACK_KPIS = {
    "Board": ["Board decision cadence", "Strategic risk oversight", "Fiduciary review completion"],
    "AI Research": ["Model evaluation score", "Research throughput", "Safety eval pass rate"],
    "Business Development": [
        "Partnership pipeline value",
        "Alliance conversion rate",
        "Channel revenue",
    ],
    "Consulting": ["Engagement SLA", "Client NPS", "Billable utilization"],
    "Data": ["Data quality score", "Pipeline uptime", "Catalog coverage"],
    "Executive": ["Company OKR attainment", "Runway months", "Board action completion"],
    "IT": ["System uptime", "Incident MTTR", "Change success rate"],
    "Operations": ["Process cycle time", "SLA adherence", "Cost per workflow"],
    "Pharos": ["Thought-leadership output", "Audience growth", "Inbound citation count"],
    "Product": ["Feature adoption", "Release cadence", "Roadmap attainment"],
    "QA": ["Defect escape rate", "Test coverage", "Gate pass rate"],
    "Security": ["Patch latency", "Control coverage", "Incident response time"],
    "Strategy": ["Initiative milestone rate", "Market signal coverage", "Scenario review cadence"],
    "Technology": ["Platform reliability", "Delivery lead time", "Tech-debt burn-down"],
    "People": ["Hiring cycle time", "Retention rate", "Engagement score"],
    "Engineering": ["Deployment frequency", "Change failure rate", "On-call MTTR"],
    "Marketing": ["Qualified pipeline", "Campaign ROI", "Brand reach"],
    "Sales": ["Pipeline coverage", "Win rate", "ARR growth"],
    "Customer Success": ["Retention rate", "Expansion ARR", "CSAT"],
    "Legal": ["Contract cycle time", "Compliance audit pass", "Risk register closure"],
    "Finance": ["Forecast accuracy", "Burn variance", "Close cycle time"],
    "DevOps": ["Deploy success rate", "Infra cost efficiency", "Recovery time"],
}

# V9 editorial overrides (from handoff): quality policy/gates vs automation/eval.
DECISION_OVERRIDES = {
    "qa_lead": [
        "Owns quality policy: release gates, exit criteria, and go/no-go standards",
        "Approves or blocks releases that fail documented quality gates",
        "Sets defect severity taxonomy and escape-rate thresholds",
    ],
    "test_engineering_lead": [
        "Owns test automation architecture, harness standards, and eval execution",
        "Decides which suites gate CI and how flaky tests are quarantined",
        "Approves tooling choices for automated regression and performance testing",
    ],
}


def find_project_root() -> Path:
    """Walk up until company-registry.yaml is found (script lives under harness/)."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "company-registry.yaml").is_file():
            return parent
    raise SystemExit("Could not locate project root (company-registry.yaml)")


ROOT = find_project_root()
REGISTRY = ROOT / "company-registry.yaml"
KPIS = ROOT / "company" / "config" / "kpis.yaml"
DEPTS = ROOT / "company" / "departments.yaml"


def approval_level(agent: dict) -> str:
    t = (agent.get("type") or "").lower()
    aid = agent.get("id", "")
    if t == "board" or aid.startswith("board_"):
        return "board"
    if aid == "human_ceo" or t in ("human_ceo", "human-ceo"):
        return "ceo"
    if t == "executive":
        return "exec"
    return "lead"


def escalation_path(agent: dict, by_id: dict) -> list[str]:
    """Ordered id chain via reports_to until human_ceo / board terminal.

    Board members and human_ceo terminate at board; specialists walk the
    reporting spine then append human_ceo -> board when not already present.
    """
    aid = agent.get("id", "")
    atype = (agent.get("type") or "").lower()

    if atype == "board":
        if aid == "board_chair" or not agent.get("reports_to"):
            return ["board"]
        chain: list[str] = []
        seen: set[str] = set()
        cur = agent
        while True:
            rid = (cur.get("reports_to") or "").strip()
            if not rid or rid in seen:
                break
            seen.add(rid)
            chain.append(rid)
            if rid == "board_chair" or rid.startswith("board_") or rid == "board":
                break
            nxt = by_id.get(rid)
            if not nxt:
                break
            cur = nxt
        if "board" not in chain:
            chain.append("board")
        return chain

    if aid == "human_ceo":
        return ["board"]

    chain = []
    seen = set()
    cur = agent
    while True:
        rid = (cur.get("reports_to") or "").strip()
        if not rid or rid in seen:
            break
        seen.add(rid)
        chain.append(rid)
        if rid == "human_ceo":
            if "board" not in seen:
                chain.append("board")
            break
        if rid == "board" or rid.startswith("board_"):
            break
        nxt = by_id.get(rid)
        if not nxt:
            break
        cur = nxt

    if not chain:
        return ["human_ceo", "board"]
    if chain[-1] not in ("board", "human_ceo") and not chain[-1].startswith("board_"):
        if "human_ceo" not in chain:
            chain.append("human_ceo")
        if "board" not in chain:
            chain.append("board")
    return chain


def decision_rights(agent: dict) -> list[str]:
    aid = agent.get("id", "")
    if aid in DECISION_OVERRIDES:
        return list(DECISION_OVERRIDES[aid])
    resp = agent.get("responsibilities") or []
    rights: list[str] = []
    for r in resp[:4]:
        r = str(r).strip().rstrip(".")
        if not r:
            continue
        rights.append(f"Decides and owns: {r}")
    if not rights:
        role = (agent.get("name") or agent.get("title") or "this domain").strip()
        rights = [f"Decides day-to-day direction for {role} within department policy"]
    return rights


def kpis_for(agent: dict, kpi_names_by_id: dict[str, list[str]]) -> list[str]:
    dept = agent.get("department") or ""
    kid = DEPT_TO_KPI_ID.get(dept)
    if kid and kpi_names_by_id.get(kid):
        return list(kpi_names_by_id[kid])
    return list(
        FALLBACK_KPIS.get(
            dept, [f"{dept} delivery KPI", f"{dept} quality KPI", f"{dept} cycle-time KPI"]
        )
    )


def load_kpi_names(kpi_doc: dict) -> dict[str, list[str]]:
    """Load kpis.yaml shape: departments.<id>.kpis[].name."""
    out: dict[str, list[str]] = {}
    for did, dval in (kpi_doc.get("departments") or {}).items():
        if not isinstance(dval, dict):
            continue
        for row in dval.get("kpis") or []:
            name = row.get("name") if isinstance(row, dict) else None
            if name:
                out.setdefault(str(did), []).append(str(name))
    return out


def main() -> None:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert isinstance(data, dict) and "company" in data
    agents = data["company"]["agents"]
    assert isinstance(agents, list) and len(agents) == 90, f"expected 90 agents, got {len(agents)}"

    by_id = {a["id"]: a for a in agents if isinstance(a, dict) and a.get("id")}

    kpi_doc = yaml.safe_load(KPIS.read_text(encoding="utf-8")) or {}
    kpi_names_by_id = load_kpi_names(kpi_doc)
    if not kpi_names_by_id:
        raise SystemExit("No KPIs loaded from kpis.yaml")

    dept_ids = {
        d["id"]: d["name"]
        for d in (yaml.safe_load(DEPTS.read_text(encoding="utf-8")) or {}).get("departments", [])
    }
    known_names = set(dept_ids.values())

    filled = {f: 0 for f in MANDATORY}
    for a in agents:
        if not isinstance(a, dict) or not a.get("id"):
            continue
        dept = a.get("department") or ""
        if dept and dept not in known_names and dept not in FALLBACK_KPIS:
            raise SystemExit(f"Unknown department {dept!r} for agent {a['id']}")

        if not a.get("approval_level"):
            a["approval_level"] = approval_level(a)
            filled["approval_level"] += 1
        if not a.get("escalation_path"):
            a["escalation_path"] = escalation_path(a, by_id)
            filled["escalation_path"] += 1
        if not a.get("kpis"):
            a["kpis"] = kpis_for(a, kpi_names_by_id)
            filled["kpis"] += 1
        if not a.get("decision_rights"):
            a["decision_rights"] = decision_rights(a)
            filled["decision_rights"] += 1

    # Final coverage check.
    for a in agents:
        for f in MANDATORY:
            v = a.get(f)
            if v is None or v == "" or v == []:
                raise SystemExit(f"Missing {f} on {a.get('id')}")

    out = yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100
    )
    REGISTRY.write_text(out, encoding="utf-8")
    print(f"Backfilled (new): {filled}")
    print(f"Coverage: {len(agents)}/90 agents on all 4 MANDATORY fields")


if __name__ == "__main__":
    main()
