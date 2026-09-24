"""Backfill MANDATORY governance fields into the consulting-firm template registry."""

from __future__ import annotations

from pathlib import Path

import yaml

TEMPLATE = (
    Path(__file__).resolve().parents[4]
    / "company"
    / "registry-templates"
    / "consulting-firm"
    / "company-registry.yaml"
)

GOV_DEFAULTS = {
    "executive": {
        "approval_level": "exec",
        "escalation_path": ["human_ceo", "board"],
    },
    "specialist": {
        "approval_level": "lead",
        "escalation_path": ["cto", "human_ceo"],
    },
    "board": {
        "approval_level": "board",
        "escalation_path": ["board"],
    },
}

HEADER = """# =============================================================================
# Consulting Firm Registry Template
# -----------------------------------------------------------------------------
# A lean, AI-native consultancy modeled on the We Lead Out operating model:
# small expert teams augmented by AI, outcomes over hours, and a delivery
# pipeline of discovery -> proposal -> build -> review -> support.
#
# HOW TO USE
#   1. Copy this directory to the root of a new AI Company Builder project
#      (company-registry.yaml + config/).
#   2. Customize the company details and agent ids/responsibilities.
#   3. Validate:   uv run python -c "from ai_company.registry import load_registry; load_registry('config')"
#   4. Generate:   uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
#
# The agent definitions below follow the same schema as the platform's primary
# company-registry.yaml. Board selection, tools, and model tiers use the
# canonical tool vocabulary (read, write, execute, grep, list, webfetch, task).
#
# MANDATORY governance fields (present on every agent):
#   decision_rights, approval_level, escalation_path, kpis
# =============================================================================
"""


def derive_gov(agent: dict) -> dict:
    aid = str(agent.get("id", ""))
    atype = str(agent.get("type", "specialist"))
    defaults = dict(GOV_DEFAULTS.get(atype, GOV_DEFAULTS["specialist"]))
    if aid == "human_ceo":
        defaults = {"approval_level": "ceo", "escalation_path": ["board"]}
    if aid == "board_chair":
        defaults = {"approval_level": "board", "escalation_path": ["board"]}

    resp = agent.get("responsibilities") or []
    rights = []
    for r in resp:
        rights.append(f"Decides and owns: {str(r).rstrip('.')}")
    if not rights:
        rights = [f"Decides and owns outcomes for {aid.replace('_', '-')} role"]

    name = str(agent.get("name") or aid)
    kpis = [f"{name} delivery quality", f"{name} SLA adherence"]
    return {
        "decision_rights": rights,
        "approval_level": defaults["approval_level"],
        "escalation_path": defaults["escalation_path"],
        "kpis": kpis,
    }


def main() -> int:
    text = TEMPLATE.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    agents = data["company"]["agents"]
    changed = 0
    for agent in agents:
        gov = derive_gov(agent)
        for key, value in gov.items():
            if key not in agent or agent[key] in (None, "", []):
                agent[key] = value
                changed += 1
    out = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=100,
        default_flow_style=False,
    )
    TEMPLATE.write_text(HEADER + out, encoding="utf-8")
    print(f"backfilled {changed} fields across {len(agents)} agents")

    data2 = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    missing = 0
    for agent in data2["company"]["agents"]:
        for field in ("decision_rights", "approval_level", "escalation_path", "kpis"):
            if field not in agent or agent[field] in (None, "", []):
                missing += 1
                print(f"still missing {agent['id']} {field}")
    print(f"missing after {missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
