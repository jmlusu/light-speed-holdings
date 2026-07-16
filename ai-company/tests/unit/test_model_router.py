"""Tests for the ModelRouter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from ai_company.model_router import ModelRouter


@pytest.fixture()
def models_yaml(tmp_path: Path) -> Path:
    config = {
        "providers": {
            "ollama": {"backend": "ollama", "default_model": "llama3.1:8b", "api_base": "http://localhost:11434"},
            "openai": {"backend": "openai", "default_model": "gpt-4o-mini", "api_base": "https://api.openai.com/v1"},
            "anthropic": {"backend": "anthropic", "default_model": "claude-sonnet-4-20250514", "api_base": "https://api.anthropic.com"},
        },
        "tiers": {
            "fast": {
                "description": "Cheap and fast",
                "providers": [
                    {"provider": "ollama", "model": "llama3.1:8b"},
                    {"provider": "openai", "model": "gpt-4o-mini"},
                ],
            },
            "standard": {
                "description": "Balanced",
                "providers": [
                    {"provider": "openai", "model": "gpt-4o"},
                    {"provider": "anthropic", "model": "claude-sonnet-4-20250514"},
                ],
            },
            "premium": {
                "description": "Best reasoning",
                "providers": [
                    {"provider": "anthropic", "model": "claude-opus-4-20250514"},
                ],
            },
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "priority": "medium", "tier": "standard"},
            {"agent_type": "Executive", "priority": "critical", "tier": "premium"},
            {"agent_type": "Specialist", "priority": "low", "tier": "standard"},
            {"agent_type": "Specialist", "priority": "medium", "tier": "standard"},
            {"agent_type": "Specialist", "priority": "high", "tier": "premium"},
            {"agent_type": "Specialist", "priority": "critical", "tier": "premium"},
            {"context": "escalation", "tier": "premium"},
            {"context": "approval", "tier": "premium"},
        ],
    }
    path = tmp_path / "models.yaml"
    path.write_text(yaml.dump(config), encoding="utf-8")
    return path


@pytest.fixture()
def registry_json(tmp_path: Path) -> Path:
    agents = [
        {"name": "cto", "role": "CTO", "type": "Executive", "model": "anthropic/claude-opus-4-20250514"},
        {"name": "board-finance", "role": "Finance Board Advisor", "type": "Board"},
        {"name": "lead-backend", "role": "Lead Backend Engineer", "type": "Specialist"},
    ]
    path = tmp_path / "agent-registry.json"
    path.write_text(json.dumps(agents), encoding="utf-8")
    return path


@pytest.fixture()
def router(models_yaml: Path, registry_json: Path) -> ModelRouter:
    return ModelRouter(
        config_path=str(models_yaml),
        registry_path=str(registry_json),
    )


def test_board_routes_to_fast_tier(router: ModelRouter) -> None:
    route = router.resolve(agent_name="board-finance")
    assert route.tier == "fast"
    assert route.provider == "ollama"
    assert route.model == "llama3.1:8b"


def test_specialist_routes_to_standard_tier(router: ModelRouter) -> None:
    route = router.resolve(agent_name="lead-backend", priority="medium")
    assert route.tier == "standard"


def test_per_agent_override_wins(router: ModelRouter) -> None:
    route = router.resolve(agent_name="cto")
    assert route.tier == "override"
    assert route.provider == "anthropic"
    assert route.model == "claude-opus-4-20250514"


def test_critical_priority_escalates_to_premium(router: ModelRouter) -> None:
    route = router.resolve(agent_name="lead-backend", priority="critical")
    assert route.tier == "premium"


def test_high_priority_escalates_to_premium(router: ModelRouter) -> None:
    route = router.resolve(agent_name="lead-backend", priority="high")
    assert route.tier == "premium"


def test_escalation_context_uses_premium(router: ModelRouter) -> None:
    route = router.resolve(agent_name="lead-backend", context="escalation")
    assert route.tier == "premium"


def test_approval_context_uses_premium(router: ModelRouter) -> None:
    route = router.resolve(agent_name="lead-backend", context="approval")
    assert route.tier == "premium"


def test_unknown_agent_uses_standard(router: ModelRouter) -> None:
    route = router.resolve(agent_name="nonexistent-agent")
    assert route.tier == "standard"


def test_fallback_when_no_tier_matches(router: ModelRouter) -> None:
    route = router.resolve(agent_type="UnknownType", priority="low")
    assert route.tier == "standard"


def test_list_tiers(router: ModelRouter) -> None:
    tiers = router.list_tiers()
    assert len(tiers) == 3
    ids = {t.id for t in tiers}
    assert ids == {"fast", "standard", "premium"}


def test_list_providers(router: ModelRouter) -> None:
    providers = router.list_providers()
    assert len(providers) == 3
    ids = {p.id for p in providers}
    assert ids == {"ollama", "openai", "anthropic"}


def test_resolve_all_agents(router: ModelRouter) -> None:
    results = router.resolve_all_agents()
    assert len(results) == 3
    assert "cto" in results
    assert "board-finance" in results
    assert "lead-backend" in results
