"""Registry-derived company counts — single source of truth for agent/department totals.

All brand/investor templates and generators MUST import counts from here instead of
hardcoding numbers, so marketing materials can never drift from ``company-registry.yaml``.
This mirrors the dashboard's ``_count_registered_agents()`` (dynamic, never hardcoded).

Usage:
    python scripts/company_counts.py            # human-readable table
    python scripts/company_counts.py --json     # machine-readable JSON
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "company-registry.yaml"


def load_agents() -> list[dict]:
    with open(REGISTRY_PATH, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return list(data["company"]["agents"])


def company_counts() -> dict:
    agents = load_agents()
    by_department = Counter(a["department"] for a in agents if a.get("department"))
    by_type = Counter(a.get("type", "UNSPECIFIED") for a in agents)
    return {
        "agents": len(agents),
        "departments": len(by_department),
        "department_names": sorted(by_department),
        "agents_by_department": dict(by_department),
        "agents_by_type": dict(by_type),
        "board_agents": by_type.get("board", 0),
        "operating_agents": len(agents) - by_type.get("board", 0),
        "technology_agents": by_department.get("Technology", 0),
    }


def main() -> None:
    counts = company_counts()
    if "--json" in sys.argv[1:]:
        print(json.dumps(counts, indent=2, sort_keys=True))
        return
    print(f"agents:           {counts['agents']}")
    print(f"departments:      {counts['departments']}")
    print(f"board seats:      {counts['board_agents']}")
    print(f"operating agents: {counts['operating_agents']}")
    print(f"technology dept:  {counts['technology_agents']}")
    print("by department:")
    for name, count in counts["agents_by_department"].items():
        print(f"  {name}: {count}")
    print("by type:")
    for name, count in counts["agents_by_type"].items():
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
