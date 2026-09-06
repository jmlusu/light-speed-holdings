"""Doc-count drift guard.

Ensures current-facing documentation never falls behind the live agent count
in ``company-registry.yaml`` (the single source of truth).

Scope rules:
- Excludes ``docs/archive/`` and ``harness/`` (historical change records).
- Excludes historical changelog/log entries that record the count as it was
  at that point in time (see ``HISTORICAL_ALLOWLIST``).
- Excludes ADR-010's 127-agent fan-out load benchmark constant (a capacity
  parameter, not a workforce count claim).
- The org chart's per-department headings (e.g. ``## Technology (27 agents)``)
  legitimately repeat each department's headcount and are checked structurally
  against the registry rather than blanket-swept.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ai_company.registry.loader import load_yaml_cached

REPO_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_AGENT_COUNT = 144
EXPECTED_DEPARTMENT_COUNT = 20
EXPECTED_TYPES = {"executive", "specialist", "board"}

# Current-facing docs that must reference the live agent count.
CURRENT_DOCS = [
    "README.md",
    "CHANGELOG.md",
    ".ai-company/state/CHANGELOG.md",
    "docs/DEVELOPMENT.md",
    "docs/USER-GUIDE.md",
    "docs/STATUS.md",
    "docs/ORGANIZATION.md",
    "docs/DEVICE-SETUP.md",
    "docs/CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md",
    "docs/IMPLEMENTATION_SUMMARY.md",
    "docs/CEO-DIRECTIVE-BLUEPRINT-ADOPTION.md",
    "docs/EXECUTIVE_DASHBOARD_V1_STRATEGIC_PLAN.md",
    "docs/API-REFERENCE.md",
    "docs/api/PUSH-NOTIFICATIONS.md",
    "docs/service-catalog-malawi.md",
    "docs/SPRINT9-PHASE1-CORE-ARCHITECTURE.md",
    "docs/ux/CLI-DESIGN.md",
    "docs/ux/DEVELOPER-EXPERIENCE.md",
    "docs/ux/ACCESSIBILITY.md",
    "docs/legal/msa-template.md",
    # Stream D (branding/lightspeed-main-site) docs land in a dedicated PR; the
    # list above is re-extended there, not before, to keep this gate green
    # against the branch's committed contents only.
]

# Historical changelog/log lines that legitimately record earlier agent-era
# counts (127, 131, or the pre-expansion 27 across 7 departments), plus
# ADR-010's 127-agent load benchmark constant. Keyed by relative path.
HISTORICAL_ALLOWLIST: dict[str, tuple[str, ...]] = {
    "CHANGELOG.md": (
        "all 127 agent cards",
        "All 127 agents deployed",
        "27 agents across 7 departments",
        "27 pre-built agent roles across 7 departments",
        "131 agents",
        "7 departments, 28 KPIs",
    ),
    ".ai-company/state/CHANGELOG.md": (
        "131 agents",
        "all 131 agent cards",
    ),
    "docs/STATUS.md": (
        "across all 127 agent cards",
        "127 agents / 0 errors",
        "All 127 agents deployed",
        "127-agent fan-out",
    ),
}

STALE_COUNT_RE = re.compile(
    r"\b(?:27|127|131)\b\+?\s*(?:pre-built\s+)?(?:AI\s+)?agents?\b"
    r"|\b(?:27|127)\s*-\s*agent\b"
    r"|\b84\s+agent definitions?\b"
)

STALE_DEPT_RE = re.compile(r"\b7\s+departments?\b")


def _live_agents() -> list[dict]:
    data = load_yaml_cached(REPO_ROOT / "company-registry.yaml")
    return data["company"]["agents"]


def _live_department_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for agent in _live_agents():
        counts[agent["department"]] = counts.get(agent["department"], 0) + 1
    return counts


def test_registry_agent_count() -> None:
    assert len(_live_agents()) == EXPECTED_AGENT_COUNT


def test_registry_department_count() -> None:
    assert len(_live_department_counts()) == EXPECTED_DEPARTMENT_COUNT


def test_registry_agents_have_valid_types() -> None:
    unknown = [agent["id"] for agent in _live_agents() if agent.get("type") not in EXPECTED_TYPES]
    assert not unknown, f"Agents with missing/invalid type: {unknown}"


def test_generated_artifacts_match_registry_count() -> None:
    count = len(_live_agents())
    agent_files = list((REPO_ROOT / ".opencode" / "agents").glob("*.md"))
    assert len(agent_files) == count
    with (REPO_ROOT / "company" / "agent-registry.json").open(encoding="utf-8") as fh:
        registry_json = json.load(fh)
    json_count = (
        len(registry_json) if isinstance(registry_json, list) else len(registry_json["agents"])
    )
    assert json_count == count


def test_registry_table_header_matches_count() -> None:
    count = len(_live_agents())
    header = (REPO_ROOT / "docs" / "AGENT-REGISTRY-TABLE.md").read_text(encoding="utf-8")
    assert f"> **Total Agents**: {count} across" in header


def test_org_chart_reflects_registry() -> None:
    count = len(_live_agents())
    org_chart = (REPO_ROOT / "company" / "org-chart.md").read_text(encoding="utf-8")
    sections = re.findall(r"^## (.+?) \((\d+) agents?\)$", org_chart, re.M)
    org_counts = {name: int(n) for name, n in sections}
    assert org_counts == _live_department_counts()
    assert sum(org_counts.values()) == count


def test_department_count_claims_in_living_docs() -> None:
    claim = f"{EXPECTED_DEPARTMENT_COUNT} departments"
    for rel in ("README.md", "docs/DEVELOPMENT.md", "docs/ORGANIZATION.md"):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert claim in text, f"{rel} does not claim {claim}"


def test_current_docs_have_no_stale_agent_count() -> None:
    violations: list[str] = []
    for rel in CURRENT_DOCS:
        path = REPO_ROOT / rel
        assert path.exists(), f"Missing current-facing doc: {rel}"
        allow = HISTORICAL_ALLOWLIST.get(rel, ())
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not STALE_COUNT_RE.search(line):
                continue
            if any(fragment in line for fragment in allow):
                continue
            violations.append(f"{rel}:{lineno}: {line.strip()}")
    assert not violations, "Stale agent-count references in current-facing docs:\n" + "\n".join(
        violations
    )


def test_current_docs_have_no_stale_dept_count() -> None:
    violations: list[str] = []
    for rel in CURRENT_DOCS:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        allow = HISTORICAL_ALLOWLIST.get(rel, ())
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not STALE_DEPT_RE.search(line):
                continue
            if any(fragment in line for fragment in allow):
                continue
            violations.append(f"{rel}:{lineno}: {line.strip()}")
    assert not violations, (
        "Stale department-count references in current-facing docs:\n" + "\n".join(violations)
    )
