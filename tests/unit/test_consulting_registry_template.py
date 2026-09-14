"""Tests for the consulting-firm registry template.

The template lives at ``company/registry-templates/consulting-firm/`` and models
a lean, AI-native consultancy on the We Lead Out operating model.  These tests
prove the template is a valid, self-contained firm definition: it loads through
the same ``load_registry`` pipeline as the platform's primary registry and
satisfies the registry-validator checks, so it can be copied to a new project
root and generated from unchanged.
"""

from __future__ import annotations

from pathlib import Path

from ai_company.paths import get_project_root
from ai_company.registry import load_registry
from ai_company.registry.loader import load_yaml_cached

TEMPLATE_CONFIG_DIR = (
    get_project_root() / "company" / "registry-templates" / "consulting-firm" / "config"
)
TEMPLATE_REGISTRY = (
    get_project_root()
    / "company"
    / "registry-templates"
    / "consulting-firm"
    / "company-registry.yaml"
)


def test_template_validates_through_full_registry_pipeline() -> None:
    """The template must load, parse, and validate like a real firm."""
    registry = load_registry(TEMPLATE_CONFIG_DIR)
    assert registry.company.name
    assert registry.company.id == "consulting-firm"
    assert len(registry.executives) >= 4
    assert len(registry.specialists) >= 5
    assert len(registry.board) >= 1
    assert len(registry.workflows) >= 1


def test_template_defines_the_wlo_discovery_to_delivery_team() -> None:
    """The template must include the consulting roles that deliver the model."""
    registry = load_registry(TEMPLATE_CONFIG_DIR)
    exec_ids = {e.id for e in registry.executives}
    spec_ids = {s.id for s in registry.specialists}
    expected_executives = {
        "human_ceo",
        "chief_of_staff",
        "consulting_lead",
        "delivery_lead",
        "sales_lead",
        "client_success_lead",
    }
    expected_specialists = {
        "interview_agent",
        "workflow_mapper",
        "opportunity_identifier",
        "solution_architect",
        "implementation_engineer",
        "proposal_writer",
        "account_manager",
        "qa_lead",
        "support_agent",
    }
    assert expected_executives.issubset(exec_ids)
    assert expected_specialists.issubset(spec_ids)
    # The discovery pipeline reports through the consulting lead.
    for specialist_id in ("interview_agent", "workflow_mapper", "opportunity_identifier"):
        specialist = next(s for s in registry.specialists if s.id == specialist_id)
        assert specialist.reports_to == "consulting_lead"


def test_every_agent_uses_only_registry_tool_vocabulary() -> None:
    """Tool lists must use registry vocabulary that normalizes to the canonical
    OpenCode v2 permission keys. ``code_interpreter`` was removed from the
    vocabulary and must never appear; other ids are rejected at generation
    time rather than mapped."""
    registry_vocabulary = {
        "read",
        "write",
        "execute",
        "grep",
        "list",
        "webfetch",
        "delegate",
        "edit",
        "question",
    }
    raw = load_yaml_cached(TEMPLATE_REGISTRY)
    assert raw is not None
    agents = raw.get("company", {}).get("agents", [])
    assert agents, "template registry must define agents"
    for agent in agents:
        tools = agent.get("tools", [])
        unknown = sorted(set(tools) - registry_vocabulary)
        assert not unknown, f"{agent.get('id')} uses non-registry tools: {unknown}"


def test_template_config_subset_existing_where_needed() -> None:
    """The template ships the minimal config/ subset required by the loader."""
    for rel in (
        Path("departments/departments.yaml"),
        Path("workflows/workflows.yaml"),
        Path("company/company.yaml"),
        Path("company/budget.yaml"),
    ):
        assert (TEMPLATE_CONFIG_DIR / rel).is_file(), f"missing {rel}"
