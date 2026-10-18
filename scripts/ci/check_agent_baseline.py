"""Human-in-the-loop gate for company-registry.yaml agent roster changes.

The approved roster (every agent id plus the count) is pinned in
company/agent-baseline.json. Any add, remove, or swap of an agent id fails
this check until the CEO-approved baseline is updated in the same PR.

Policy: AGENTS.md section 9.4; docs/architecture/adr/026-single-owner-architecture.md
Run: uv run python scripts/ci/check_agent_baseline.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "company-registry.yaml"
BASELINE_PATH = ROOT / "company" / "agent-baseline.json"

HITL_HINT = (
    "Agent roster differs from the CEO-approved baseline "
    "(company/agent-baseline.json). Adding, removing, or swapping agents "
    "requires Human CEO approval (AGENTS.md 9.4, ADR-026): after approval, "
    "update approved_ids/approved_count/approved_by/approved_date in the "
    "baseline in the same PR. Never edit the baseline alone to silence "
    "this check."
)


def registry_ids() -> list[str]:
    data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    agents = (data.get("company") or {}).get("agents") or []
    ids = []
    for agent in agents:
        agent_id = str((agent or {}).get("id") or "").strip()
        if not agent_id:
            raise SystemExit("::error::company-registry.yaml contains an agent with no id")
        ids.append(agent_id)
    return sorted(ids)


def baseline_ids() -> tuple[set[str], int]:
    data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    approved = {str(x).strip() for x in data.get("approved_ids") or []}
    count = int(data.get("approved_count", -1))
    if count != len(approved):
        raise SystemExit(
            f"::error::{BASELINE_PATH.name} is self-inconsistent: "
            f"approved_count={count} but approved_ids has {len(approved)} entries"
        )
    return approved, count


def main() -> int:
    registry = registry_ids()
    approved, approved_count = baseline_ids()
    dupes = sorted(i for i, c in Counter(registry).items() if c > 1)
    if dupes:
        print("::error::Duplicate agent ids in company-registry.yaml: " + ", ".join(dupes))
        print(HITL_HINT)
        return 1
    added = sorted(set(registry) - approved)
    removed = sorted(approved - set(registry))
    if added or removed:
        print(
            f"::error::Registry ids ({len(registry)}) do not match the "
            f"CEO-approved baseline ({approved_count}). {HITL_HINT}"
        )
        if added:
            print("::error::Not approved (in registry, missing from baseline): " + ", ".join(added))
        if removed:
            print("::error::Approved but missing from registry: " + ", ".join(removed))
        return 1
    if len(registry) != approved_count:
        print(
            f"::error::Ids match but count does not: registry={len(registry)} "
            f"baseline={approved_count}"
        )
        return 1
    print(
        f"OK: {len(registry)} agent ids match the CEO-approved baseline "
        f"(approved {approved_count})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
