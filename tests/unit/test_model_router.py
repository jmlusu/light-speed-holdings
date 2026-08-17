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
            "ollama": {
                "backend": "ollama",
                "default_model": "llama3.1:8b",
                "api_base": "http://localhost:11434",
            },
            "openai": {
                "backend": "openai",
                "default_model": "gpt-4o-mini",
                "api_base": "https://api.openai.com/v1",
            },
            "anthropic": {
                "backend": "anthropic",
                "default_model": "claude-sonnet-4-20250514",
                "api_base": "https://api.anthropic.com",
            },
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
        {
            "name": "cto",
            "role": "CTO",
            "type": "Executive",
            "model": "anthropic/claude-opus-4-20250514",
        },
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


def test_provider_rate_limit_parsed(tmp_path: Path) -> None:
    """GAP-038: rate_limit block is surfaced on ProviderConfig."""
    config = {
        "providers": {
            "openai": {
                "backend": "openai_compatible",
                "default_model": "gpt-4o-mini",
                "api_base": "https://api.openai.com/v1",
                "rate_limit": {"rate": 10, "capacity": 5},
            },
            "ollama": {
                "backend": "ollama",
                "default_model": "llama3.1:8b",
                "api_base": "http://localhost:11434",
            },
        },
        "tiers": {},
    }
    models_yaml = tmp_path / "models.yaml"
    models_yaml.write_text(yaml.safe_dump(config), encoding="utf-8")

    router = ModelRouter(config_path=str(models_yaml))
    by_id = {p.id: p for p in router.list_providers()}

    assert by_id["openai"].rate_limit == {"rate": 10, "capacity": 5}
    assert by_id["ollama"].rate_limit == {}


def test_resolve_all_agents(router: ModelRouter) -> None:
    results = router.resolve_all_agents()
    assert len(results) == 3
    assert "cto" in results
    assert "board-finance" in results
    assert "lead-backend" in results


# ── Free tier routing tests ──────────────────────────────────────────


def test_free_tier_uses_dynamic_catalog(router: ModelRouter) -> None:
    """When tier resolves to 'free', should return a model from the catalog."""
    # Pre-seed the cache with test models
    from ai_company.model_router import FreeModel

    test_models = [
        FreeModel(
            id="opencode/big-pickle",
            name="Big Pickle",
            context=200000,
            provider="opencode",
            model="big-pickle",
            priority=800,
        ),
        FreeModel(
            id="opencode/gpt-5-nano",
            name="GPT-5 Nano",
            context=128000,
            provider="opencode",
            model="gpt-5-nano",
            priority=920,
        ),
    ]
    router._set_cached_free_models(test_models)

    # Add a routing rule that maps to free tier
    router._routing.append({"context": "test_free", "tier": "free"})

    route = router.resolve(context="test_free")
    assert route.tier == "free"
    assert route.provider == "opencode"
    assert route.model == "big-pickle"  # Largest context window first


def test_free_tier_falls_back_to_static(router: ModelRouter) -> None:
    """When catalog is not cached, should use static fallback from config."""
    config = {
        "providers": {
            "ollama": {
                "backend": "ollama",
                "default_model": "llama3.1:8b",
                "api_base": "http://localhost:11434",
            },
            "opencode": {
                "backend": "openai_compatible",
                "default_model": "big-pickle",
                "api_base": "https://opencode.ai/zen/v1",
            },
        },
        "tiers": {},
        "routing": [{"context": "test_free", "tier": "free"}],
        "free_tier": {
            "static_fallback": [
                {"provider": "opencode", "model": "big-pickle"},
                {"provider": "ollama", "model": "llama3.1:8b"},
            ],
        },
    }
    import yaml

    path = router.config_path
    path.write_text(yaml.dump(config), encoding="utf-8")
    router._load()

    # Clear the cache
    router._clear_cached_free_models()

    route = router.resolve(context="test_free")
    assert route.tier == "free"
    assert route.provider == "opencode"
    assert route.model == "big-pickle"


# ── Token-limit rotation tests ───────────────────────────────────────


def test_find_free_model(router: ModelRouter) -> None:
    """_find_free_model should locate models by ID or model name."""
    from ai_company.model_router import FreeModel

    test_models = [
        FreeModel(
            id="opencode/big-pickle",
            name="Big Pickle",
            context=200000,
            provider="opencode",
            model="big-pickle",
            priority=800,
        ),
    ]
    router._set_cached_free_models(test_models)

    # Find by full ID
    found = router._find_free_model("opencode/big-pickle")
    assert found is not None
    assert found.name == "Big Pickle"

    # Find by model name
    found = router._find_free_model("big-pickle")
    assert found is not None
    assert found.context == 200000

    # Not found
    found = router._find_free_model("nonexistent")
    assert found is None


def test_rotate_on_token_limit_to_larger_model(router: ModelRouter) -> None:
    """rotate_on_token_limit should rotate to a model with larger context."""
    from ai_company.model_router import FreeModel

    test_models = [
        FreeModel(
            id="opencode/small-model",
            name="Small",
            context=80000,
            provider="opencode",
            model="small-model",
            priority=920,
        ),
        FreeModel(
            id="opencode/large-model",
            name="Large",
            context=200000,
            provider="opencode",
            model="large-model",
            priority=800,
        ),
    ]
    router._set_cached_free_models(test_models)

    import asyncio

    route = asyncio.get_event_loop().run_until_complete(
        router.rotate_on_token_limit("small-model", "test task")
    )
    assert route is not None
    assert route.model == "large-model"
    assert route.tier == "standard"  # 200K context = standard tier


def test_rotate_on_token_limit_no_larger_model(router: ModelRouter) -> None:
    """When no larger model exists, should rotate to next tier up (standard → premium)."""
    from ai_company.model_router import FreeModel

    test_models = [
        FreeModel(
            id="opencode/largest-model",
            name="Largest",
            context=200000,
            provider="opencode",
            model="largest-model",
            priority=800,
        ),
    ]
    router._set_cached_free_models(test_models)

    import asyncio

    route = asyncio.get_event_loop().run_until_complete(
        router.rotate_on_token_limit("largest-model", "test task")
    )
    # Should rotate to next tier up (standard → premium)
    assert route is not None
    assert route.tier == "premium"


# ── Budget degradation tests ─────────────────────────────────────────


def test_budget_degradation_warning_threshold(router: ModelRouter) -> None:
    """At 80% pressure, non-critical tasks should be downgraded."""
    # Add budget_degradation config
    router._config["budget_degradation"] = {
        "warning_threshold": 0.80,
        "pressure_threshold": 0.90,
        "critical_threshold": 0.95,
        "hard_stop_threshold": 1.00,
    }

    # Premium at 80% → standard
    tier = router.get_budget_degradation_tier("premium", 0.85, is_critical=False)
    assert tier == "standard"

    # Fast at 80% → stays fast (already cheap)
    tier = router.get_budget_degradation_tier("fast", 0.85, is_critical=False)
    assert tier == "fast"


def test_budget_degradation_pressure_threshold(router: ModelRouter) -> None:
    """At 90% pressure, non-critical tasks should be forced to fast."""
    router._config["budget_degradation"] = {
        "warning_threshold": 0.80,
        "pressure_threshold": 0.90,
        "critical_threshold": 0.95,
        "hard_stop_threshold": 1.00,
    }

    tier = router.get_budget_degradation_tier("premium", 0.92, is_critical=False)
    assert tier == "fast"


def test_budget_degradation_critical_threshold(router: ModelRouter) -> None:
    """At 95% pressure, non-critical tasks should be forced to free."""
    router._config["budget_degradation"] = {
        "warning_threshold": 0.80,
        "pressure_threshold": 0.90,
        "critical_threshold": 0.95,
        "hard_stop_threshold": 1.00,
    }

    tier = router.get_budget_degradation_tier("premium", 0.97, is_critical=False)
    assert tier == "free"


def test_budget_degradation_critical_bypass(router: ModelRouter) -> None:
    """Critical tasks should bypass budget degradation."""
    router._config["budget_degradation"] = {
        "warning_threshold": 0.80,
        "pressure_threshold": 0.90,
        "critical_threshold": 0.95,
        "hard_stop_threshold": 1.00,
    }

    tier = router.get_budget_degradation_tier("premium", 0.99, is_critical=True)
    assert tier == "premium"


def test_budget_degradation_hard_stop(router: ModelRouter) -> None:
    """At 100% pressure, all non-critical should be forced to free."""
    router._config["budget_degradation"] = {
        "warning_threshold": 0.80,
        "pressure_threshold": 0.90,
        "critical_threshold": 0.95,
        "hard_stop_threshold": 1.00,
    }

    tier = router.get_budget_degradation_tier("premium", 1.0, is_critical=False)
    assert tier == "free"


# ── FreeModel dataclass tests ────────────────────────────────────────


def test_free_model_dataclass() -> None:
    """FreeModel should be a valid dataclass with required fields."""
    from ai_company.model_router import FreeModel

    model = FreeModel(
        id="opencode/test",
        name="Test Model",
        context=100000,
        provider="opencode",
        model="test",
        priority=900,
    )
    assert model.id == "opencode/test"
    assert model.context == 100000
    assert model.priority == 900


# ── TOKEN_LIMIT_PATTERNS tests ───────────────────────────────────────


def test_token_limit_patterns_cover_common_errors() -> None:
    """TOKEN_LIMIT_PATTERNS should match common token limit error messages."""
    from ai_company.model_router import ModelRouter

    test_cases = [
        "Context length exceeded",
        "max_tokens exceeded",
        "Token limit reached",
        "Too many tokens in request",
        "Exceeds maximum context",
        "Context window too small",
        "Maximum context length exceeded",
        "Input too long for model",
        "Prompt too long for processing",
        "Message too long to process",
    ]

    for error_msg in test_cases:
        found = any(pattern in error_msg.lower() for pattern in ModelRouter.TOKEN_LIMIT_PATTERNS)
        assert found, f"Pattern not found for: {error_msg}"
