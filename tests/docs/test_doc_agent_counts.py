"""Doc-count drift guard.

Ensures current-facing documentation never falls behind the live agent count
in ``company-registry.yaml`` (the single source of truth).

Scope rules:
- Excludes ``docs/archive/`` and ``harness/`` (historical change records).
- Excludes historical changelog/log entries that record the count as it was
  at that point in time (see ``HISTORICAL_ALLOWLIST``).
- Excludes ADR-010's 127-agent fan-out load benchmark constant (a capacity
  parameter, not a workforce count claim).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ai_company.registry.loader import load_yaml_cached

REPO_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_AGENT_COUNT = 135

# Current-facing docs that must reference the live agent count.
CURRENT_DOCS = [
    "README.md",
    "CHANGELOG.md",
    ".ai-company/state/CHANGELOG.md",
    "docs/DEVELOPMENT.md",
    "docs/USER-GUIDE.md",
    "docs/STATUS.md",
    "docs/service-catalog-malawi.md",
    "docs/SPRINT9-PHASE1-CORE-ARCHITECTURE.md",
    "docs/ux/CLI-DESIGN.md",
    "docs/ux/DEVELOPER-EXPERIENCE.md",
    "docs/ux/ACCESSIBILITY.md",
]

# Historical changelog/log lines that legitimately record the 127-agent era,
# plus ADR-010's 127-agent load benchmark constant. Keyed by relative path.
HISTORICAL_ALLOWLIST: dict[str, tuple[str, ...]] = {
    "CHANGELOG.md": (
        "all 127 agent cards",
        "All 127 agents deployed",
    ),
    "docs/STATUS.md": (
        "across all 127 agent cards",
        "127 agents / 0 errors",
        "All 127 agents deployed",
        "127-agent fan-out",
    ),
}

STALE_COUNT_RE = re.compile(r"\b127\b\s*(?:AI\s+)?agents?\b|\b127-agent\b")


def _live_agent_count() -> int:
    data = load_yaml_cached(REPO_ROOT / "company-registry.yaml")
    return len(data["company"]["agents"])


def test_registry_agent_count() -> None:
    assert _live_agent_count() == EXPECTED_AGENT_COUNT


def test_generated_artifacts_match_registry_count() -> None:
    count = _live_agent_count()
    agent_files = list((REPO_ROOT / ".opencode" / "agents").glob("*.md"))
    assert len(agent_files) == count
    with (REPO_ROOT / "company" / "agent-registry.json").open(encoding="utf-8") as fh:
        registry_json = json.load(fh)
    json_count = (
        len(registry_json) if isinstance(registry_json, list) else len(registry_json["agents"])
    )
    assert json_count == count


def test_registry_table_header_matches_count() -> None:
    count = _live_agent_count()
    header = (REPO_ROOT / "docs" / "AGENT-REGISTRY-TABLE.md").read_text(encoding="utf-8")
    assert f"> **Total Agents**: {count} across" in header


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
    assert not violations, "Stale '127 agent' references in current-facing docs:\n" + "\n".join(
        violations
    )
