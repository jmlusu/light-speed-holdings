"""Tests for the AI-CaaS offer definitions in ``config/company/ai_caas_offers.yaml``.

Locks the schema contract (required fields per offer and the four governance
gates) and cross-checks that every agent referenced by the offers actually
exists in the platform registry — so sales and delivery never point at agents
that don't exist.
"""

from __future__ import annotations

from ai_company.paths import get_project_root
from ai_company.registry import load_registry
from ai_company.registry.loader import load_yaml_cached

OFFERS_PATH = get_project_root() / "config" / "company" / "ai_caas_offers.yaml"

REQUIRED_OFFER_FIELDS = {
    "name",
    "slug",
    "agents",
    "currency",
    "risk_level",
    "governance_state",
    "notes",
}

REQUIRED_GOVERNANCE_GATES = {
    "client_onboarding_approval",
    "data_handling_protocol",
    "ethics_review_output",
    "service_level_liability_cap",
}

VALID_RISK_LEVELS = {"low", "medium", "high", "critical"}


def test_offers_file_has_all_required_offers() -> None:
    """The AI-CaaS portfolio must define the three productized plays."""
    raw = load_yaml_cached(OFFERS_PATH)
    assert raw is not None
    offers = raw["offers"]
    assert set(offers) == {"offer_f", "offer_g", "offer_h"}


def test_every_offer_matches_schema() -> None:
    """Every offer must carry the full Malawi-style schema."""
    raw = load_yaml_cached(OFFERS_PATH)
    assert raw is not None
    for key, offer in raw["offers"].items():
        missing = REQUIRED_OFFER_FIELDS - set(offer)
        assert not missing, f"{key} missing fields: {sorted(missing)}"
        assert offer["governance_state"] in {"proposed", "approved", "ratified", "blocked"}
        assert offer["risk_level"].lower() in VALID_RISK_LEVELS
        assert offer["slug"] == key.replace("_", "-")
        assert offer["agents"], f"{key} must list delivery agents"


def test_all_four_governance_gates_present() -> None:
    """Client work is gated on the same four board policies as the Malawi portfolio."""
    raw = load_yaml_cached(OFFERS_PATH)
    assert raw is not None
    gates = raw.get("governance", {})
    assert REQUIRED_GOVERNANCE_GATES.issubset(set(gates))


def test_offer_agents_exist_in_registry() -> None:
    """Each referenced agent (hyphenated in YAML) must resolve to a registry agent."""
    registry = load_registry()
    agent_ids = {a.id for a in registry.executives}
    agent_ids |= {a.id for a in registry.specialists}
    agent_ids |= {a.id for a in registry.board}

    raw = load_yaml_cached(OFFERS_PATH)
    assert raw is not None
    for key, offer in raw["offers"].items():
        for agent in offer["agents"]:
            registry_id = agent.replace("-", "_")
            assert registry_id in agent_ids, f"{key} references unknown agent {agent!r}"


def test_pricing_model_doc_tracks_offers_config() -> None:
    """The pricing-model doc must reference the same offer codes as the config."""
    doc = (get_project_root() / "docs" / "ai-caas-pricing-model.md").read_text(encoding="utf-8")
    raw = load_yaml_cached(OFFERS_PATH)
    assert raw is not None
    for key in raw["offers"]:
        slug = raw["offers"][key]["slug"]
        assert slug in doc, f"doc missing offer section for {slug}"
