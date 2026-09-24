#!/usr/bin/env python3
"""Add missing MANDATORY fields (workflows, inputs, outputs) to consulting template registry"""

from pathlib import Path

import yaml

REGISTRY_PATH = Path("company/registry-templates/consulting-firm/company-registry.yaml")
BACKUP_PATH = Path("company/registry-templates/consulting-firm/company-registry.yaml.bak")

DEFAULT_WORKFLOWS = {
    "executive": ["company-strategy", "board-reporting", "department-coordination"],
    "specialist": ["task-execution", "status-reporting"],
    "board": ["governance-oversight", "strategic-review"],
}

DEFAULT_INPUTS = {
    "executive": ["department-reports", "board-directives", "market-signals"],
    "specialist": ["task-instructions", "context-documents"],
    "board": ["executive-reports", "audit-findings", "risk-assessments"],
}

DEFAULT_OUTPUTS = {
    "executive": ["strategic-decisions", "resource-allocations", "policy-directives"],
    "specialist": ["task-results", "deliverables", "status-updates"],
    "board": ["governance-decisions", "approvals", "risk-mitigations"],
}


def main():
    with open(REGISTRY_PATH, "r") as f:
        data = yaml.safe_load(f)

    with open(BACKUP_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    print(f"Backup created at {BACKUP_PATH}")

    agents = data.get("company", {}).get("agents", [])
    updated = 0

    for agent in agents:
        agent_type = agent.get("type", "specialist")

        if "workflows" not in agent:
            agent["workflows"] = DEFAULT_WORKFLOWS.get(agent_type, DEFAULT_WORKFLOWS["specialist"])
            updated += 1

        if "inputs" not in agent:
            agent["inputs"] = DEFAULT_INPUTS.get(agent_type, DEFAULT_INPUTS["specialist"])
            updated += 1

        if "outputs" not in agent:
            agent["outputs"] = DEFAULT_OUTPUTS.get(agent_type, DEFAULT_OUTPUTS["specialist"])
            updated += 1

    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True, width=120)

    print(f"Updated {len(agents)} agents with missing fields")
    print(f"Total field additions: {updated}")

    type_counts = {"executive": 0, "specialist": 0, "board": 0}
    for a in agents:
        t = a.get("type", "specialist")
        if t in type_counts:
            type_counts[t] += 1
    print(f"Type census: {type_counts}")


if __name__ == "__main__":
    main()
