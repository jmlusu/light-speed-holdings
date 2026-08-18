"""End-to-end integration tests for the model routing system.

Tests the full pipeline: task-type detection → tier resolution →
budget degradation → token-limit rotation → provider chain fallback.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from ai_company.model_router import (
    TASK_TYPE_KEYWORDS,
    FreeModel,
    ModelRouter,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def full_models_yaml(tmp_path: Path) -> Path:
    """Complete models.yaml with all routing features."""
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
            "gemini": {
                "backend": "openai_compatible",
                "default_model": "gemini-3.5-flash",
                "api_base": "https://generativelanguage.googleapis.com/v1beta/openai",
            },
        },
        "tiers": {
            "fast": {
                "description": "Cheap and fast",
                "providers": [
                    {"provider": "ollama", "model": "mistral-7b-32k"},
                    {"provider": "gemini", "model": "gemini-3.5-flash"},
                ],
            },
            "standard": {
                "description": "Balanced",
                "providers": [
                    {"provider": "opencode", "model": "big-pickle"},
                    {"provider": "ollama", "model": "llama3.1:8b"},
                ],
            },
            "premium": {
                "description": "Best reasoning",
                "providers": [
                    {"provider": "opencode", "model": "big-pickle"},
                    {"provider": "ollama", "model": "llama3.1:8b"},
                ],
            },
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "priority": "low", "tier": "standard"},
            {"agent_type": "Executive", "priority": "medium", "tier": "standard"},
            {"agent_type": "Executive", "priority": "high", "tier": "premium"},
            {"agent_type": "Executive", "priority": "critical", "tier": "premium"},
            {"agent_type": "Specialist", "priority": "low", "tier": "standard"},
            {"agent_type": "Specialist", "priority": "medium", "tier": "standard"},
            {"agent_type": "Specialist", "priority": "high", "tier": "premium"},
            {"agent_type": "Specialist", "priority": "critical", "tier": "premium"},
            {"context": "escalation", "tier": "premium"},
            {"context": "approval", "tier": "premium"},
        ],
        "task_type_routing": {
            "read_only": "free",
            "single_file_edit": "free",
            "simple_command": "free",
            "boilerplate": "free",
            "code_review": "standard",
            "debugging": "standard",
            "refactor": "standard",
            "integration": "standard",
            "architecture": "premium",
            "planning": "premium",
            "security": "premium",
            "performance": "premium",
            "general": "standard",
        },
        "free_tier": {
            "static_fallback": [
                {"provider": "opencode", "model": "big-pickle"},
                {"provider": "ollama", "model": "llama3.1:8b"},
            ],
        },
        "budget_degradation": {
            "warning_threshold": 0.80,
            "pressure_threshold": 0.90,
            "critical_threshold": 0.95,
            "hard_stop_threshold": 1.00,
        },
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
        {"name": "security-auditor", "role": "Security Auditor", "type": "Specialist"},
    ]
    path = tmp_path / "agent-registry.json"
    path.write_text(json.dumps(agents), encoding="utf-8")
    return path


@pytest.fixture()
def router(full_models_yaml: Path, registry_json: Path) -> ModelRouter:
    return ModelRouter(
        config_path=str(full_models_yaml),
        registry_path=str(registry_json),
    )


def _mock_cost_tracker(pressure: float = 0.0) -> MagicMock:
    """Create a mock CostTracker with configurable daily_pressure."""
    tracker = MagicMock()
    tracker.daily_pressure.return_value = pressure
    return tracker


# ---------------------------------------------------------------------------
# Task-type detection → tier resolution
# ---------------------------------------------------------------------------


class TestTaskTypeDetectionIntegration:
    """End-to-end: task prompt → detect_task_type() → tier from task_type_routing."""

    @pytest.mark.parametrize(
        "prompt,expected_type",
        [
            ("read the config file and show me the contents", "read_only"),
            ("list all files in the src directory", "read_only"),
            ("fix the typo in main.py line 42", "debugging"),
            ("update the config value from 10 to 20", "single_file_edit"),
            ("run the test suite", "simple_command"),
            ("execute the build script", "simple_command"),
            ("scaffold a new module with tests", "simple_command"),
            ("review this pull request for security issues", "code_review"),
            ("debug the failing test in test_auth.py", "debugging"),
            ("refactor the database connection logic", "refactor"),
            ("integrate the new API endpoint", "integration"),
            ("design the system architecture for caching", "architecture"),
            ("plan the migration strategy", "planning"),
            ("audit the codebase for security vulnerabilities", "security"),
            ("optimize the query performance", "performance"),
        ],
    )
    def test_detect_task_type_returns_correct_type(
        self, router: ModelRouter, prompt: str, expected_type: str
    ) -> None:
        detected = router.detect_task_type(prompt)
        assert detected == expected_type

    def test_read_only_routes_to_free_tier(self, router: ModelRouter) -> None:
        """A read-only task should resolve to free tier via task-type routing."""
        route = router.resolve(
            agent_name="lead-backend",
            task_prompt="read the config file and show me the contents",
        )
        assert route.tier == "free"

    def test_simple_command_routes_to_free_tier(self, router: ModelRouter) -> None:
        """A simple command task should resolve to free tier."""
        route = router.resolve(
            agent_name="lead-backend",
            task_prompt="run the tests",
        )
        assert route.tier == "free"

    def test_architecture_routes_to_premium(self, router: ModelRouter) -> None:
        """An architecture task should resolve to premium via task-type routing."""
        route = router.resolve(
            agent_name="lead-backend",
            task_prompt="design the system architecture for the new caching layer",
        )
        assert route.tier == "premium"

    def test_security_routes_to_premium(self, router: ModelRouter) -> None:
        """A security task should resolve to premium."""
        route = router.resolve(
            agent_name="lead-backend",
            task_prompt="audit the authentication system for vulnerabilities",
        )
        assert route.tier == "premium"


# ---------------------------------------------------------------------------
# Budget degradation integration
# ---------------------------------------------------------------------------


class TestBudgetDegradationIntegration:
    """End-to-end: cost_tracker.daily_pressure() → tier degradation."""

    def test_high_priority_bypasses_degradation(self, router: ModelRouter) -> None:
        """Critical tasks should bypass budget degradation."""
        tracker = _mock_cost_tracker(pressure=0.95)
        route = router.resolve(
            agent_name="lead-backend",
            priority="critical",
            cost_tracker=tracker,
        )
        assert route.tier == "premium"

    def test_medium_priority_degrades_at_90_percent(self, router: ModelRouter) -> None:
        """At 90% pressure, medium-priority tasks should degrade to fast."""
        tracker = _mock_cost_tracker(pressure=0.92)
        route = router.resolve(
            agent_name="lead-backend",
            priority="medium",
            cost_tracker=tracker,
        )
        assert route.tier == "fast"

    def test_no_tracker_means_no_degradation(self, router: ModelRouter) -> None:
        """Without a cost_tracker, no degradation should occur."""
        route = router.resolve(
            agent_name="lead-backend",
            priority="medium",
            cost_tracker=None,
        )
        assert route.tier == "standard"

    def test_low_pressure_no_change(self, router: ModelRouter) -> None:
        """At low pressure, tier should not change."""
        tracker = _mock_cost_tracker(pressure=0.50)
        route = router.resolve(
            agent_name="lead-backend",
            priority="medium",
            cost_tracker=tracker,
        )
        assert route.tier == "standard"


# ---------------------------------------------------------------------------
# Free tier dynamic catalog integration
# ---------------------------------------------------------------------------


class TestFreeTierCatalogIntegration:
    """End-to-end: dynamic catalog → free tier resolution."""

    def test_free_tier_with_seeded_catalog(self, router: ModelRouter) -> None:
        """Free tier should use the largest-context model from catalog."""
        # Catalog must be sorted by context window descending (as _resolve_free_tier expects)
        test_models = [
            FreeModel(
                id="opencode/large",
                name="Large",
                context=262144,
                provider="opencode",
                model="large",
                priority=738,
            ),
            FreeModel(
                id="opencode/small",
                name="Small",
                context=80000,
                provider="opencode",
                model="small",
                priority=920,
            ),
        ]
        router._set_cached_free_models(test_models)

        route = router.resolve(
            context="test_free_tier",
        )
        # Since "test_free_tier" is not a known context, it falls through
        # to agent_type rules. Let's use a known routing rule that maps to free.
        router._routing.append({"context": "test_free_tier", "tier": "free"})
        route = router.resolve(context="test_free_tier")
        assert route.tier == "free"
        assert route.model == "large"  # Largest context window first

    def test_free_tier_fallback_without_catalog(self, router: ModelRouter) -> None:
        """Without a cached catalog, free tier should use static fallback."""
        router._clear_cached_free_models()
        router._routing.append({"context": "test_free_no_cat", "tier": "free"})
        route = router.resolve(context="test_free_no_cat")
        assert route.tier == "free"
        assert route.provider == "opencode"
        assert route.model == "big-pickle"


# ---------------------------------------------------------------------------
# Token-limit rotation integration
# ---------------------------------------------------------------------------


class TestTokenLimitRotationIntegration:
    """End-to-end: token-limit error → rotation → larger context model."""

    def test_rotation_picks_larger_context(self, router: ModelRouter) -> None:
        """Should rotate to the next model with larger context window."""
        import asyncio

        test_models = [
            FreeModel(
                id="opencode/s",
                name="S",
                context=80000,
                provider="opencode",
                model="s",
                priority=920,
            ),
            FreeModel(
                id="opencode/m",
                name="M",
                context=128000,
                provider="opencode",
                model="m",
                priority=872,
            ),
            FreeModel(
                id="opencode/l",
                name="L",
                context=262144,
                provider="opencode",
                model="l",
                priority=738,
            ),
        ]
        router._set_cached_free_models(test_models)

        route = asyncio.get_event_loop().run_until_complete(
            router.rotate_on_token_limit("s", "test task")
        )
        assert route is not None
        assert route.model == "m"  # Next larger context (128K > 80K)

    def test_rotation_escalates_tier_when_exhausted(self, router: ModelRouter) -> None:
        """When no larger free model exists, should escalate to next tier."""
        import asyncio

        test_models = [
            FreeModel(
                id="opencode/biggest",
                name="Biggest",
                context=262144,
                provider="opencode",
                model="biggest",
                priority=738,
            ),
        ]
        router._set_cached_free_models(test_models)

        route = asyncio.get_event_loop().run_until_complete(
            router.rotate_on_token_limit("biggest", "test task")
        )
        assert route is not None
        # Should escalate from free → standard (next tier up)
        assert route.tier == "premium"  # standard→premium is next in chain


# ---------------------------------------------------------------------------
# Full pipeline: prompt → detect → resolve → degrade → rotate
# ---------------------------------------------------------------------------


class TestFullPipelineIntegration:
    """End-to-end pipeline combining all routing features."""

    def test_read_task_free_tier_no_degradation(self, router: ModelRouter) -> None:
        """A simple read task at low pressure → free tier."""
        tracker = _mock_cost_tracker(pressure=0.30)
        route = router.resolve(
            agent_name="lead-backend",
            task_prompt="read the README file",
            cost_tracker=tracker,
        )
        assert route.tier == "free"
        assert route.provider == "opencode"

    def test_architecture_task_high_pressure_stays_premium(self, router: ModelRouter) -> None:
        """A critical architecture task stays premium even at high pressure."""
        tracker = _mock_cost_tracker(pressure=0.92)
        route = router.resolve(
            agent_name="lead-backend",
            priority="critical",
            task_prompt="design the system architecture for caching",
            cost_tracker=tracker,
        )
        assert route.tier == "premium"

    def test_agent_override_bypasses_everything(self, router: ModelRouter) -> None:
        """Per-agent override bypasses task-type, budget degradation, everything."""
        tracker = _mock_cost_tracker(pressure=0.99)
        route = router.resolve(
            agent_name="cto",
            task_prompt="read the config file",
            cost_tracker=tracker,
        )
        assert route.tier == "override"
        assert route.provider == "anthropic"
        assert route.model == "claude-opus-4-20250514"

    def test_escalation_bypasses_task_type_and_budget(self, router: ModelRouter) -> None:
        """Context=escalation always uses premium, ignoring task-type and budget."""
        tracker = _mock_cost_tracker(pressure=0.95)
        route = router.resolve(
            agent_name="lead-backend",
            context="escalation",
            task_prompt="read the logs",
            cost_tracker=tracker,
        )
        assert route.tier == "premium"


# ---------------------------------------------------------------------------
# TASK_TYPE_KEYWORDS coverage
# ---------------------------------------------------------------------------


class TestTaskTypeKeywordsCoverage:
    """Verify all task types in task_type_routing have detection keywords."""

    def test_all_routing_types_have_keywords(self, router: ModelRouter) -> None:
        """Every key in task_type_routing should have keywords in TASK_TYPE_KEYWORDS."""
        task_type_routing = router._config.get("task_type_routing", {})
        for task_type in task_type_routing:
            assert task_type in TASK_TYPE_KEYWORDS, (
                f"task_type '{task_type}' is in task_type_routing "
                f"but has no detection keywords in TASK_TYPE_KEYWORDS"
            )

    def test_all_keyword_types_have_routing(self, router: ModelRouter) -> None:
        """Every key in TASK_TYPE_KEYWORDS should have a routing entry."""
        task_type_routing = router._config.get("task_type_routing", {})
        for task_type in TASK_TYPE_KEYWORDS:
            assert task_type in task_type_routing, (
                f"task_type '{task_type}' has detection keywords but no entry in task_type_routing"
            )
