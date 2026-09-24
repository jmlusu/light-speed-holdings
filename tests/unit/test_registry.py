"""Tests for the registry system: loader, parser, resolver, validator."""

from pathlib import Path

import pytest

from ai_company.models import (
    CompanyRegistry,
)
from ai_company.registry.loader import RegistryLoader
from ai_company.registry.parser import RegistryParser
from ai_company.registry.resolver import RegistryResolver
from ai_company.registry.validator import RegistryValidator

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def config_dir() -> Path:
    return Path("config")


@pytest.fixture
def loader(config_dir: Path) -> RegistryLoader:
    return RegistryLoader(config_dir)


def _gov(
    *,
    approval_level: str = "lead",
    decision_rights: list[str] | None = None,
    escalation_path: list[str] | None = None,
    kpis: list[str] | None = None,
) -> dict:
    """Minimal MANDATORY governance fields for fixtures."""
    return {
        "decision_rights": decision_rights or ["Decides and owns: test decision"],
        "approval_level": approval_level,
        "escalation_path": escalation_path or ["cto", "human_ceo"],
        "kpis": kpis or ["Test KPI"],
    }


@pytest.fixture
def sample_raw() -> dict:
    return {
        "company": {"id": "test-co", "name": "Test Company", "industry": "Tech"},
        "vision": {"mission": "Build great things"},
        "strategy": {},
        "culture": {"values": [{"name": "Innovation", "description": "Be bold"}]},
        "governance": {},
        "policies": {"policies": []},
        "kpis": {"kpis": []},
        "budget": {"fiscal_year": 2024, "total_budget": 500000, "currency": "USD"},
        "board": {
            "members": [
                {
                    "id": "dir-1",
                    "name": "Alice",
                    "approval_level": "board",
                    "decision_rights": ["Board fiduciary oversight"],
                    "escalation_path": ["board"],
                    "kpis": ["Board action completion"],
                }
            ]
        },
        "committees": {"committees": []},
        "board_meetings": {"meetings": []},
        "voting": {},
        "executives": {
            "executives": [
                {
                    "id": "ceo",
                    "name": "CEO",
                    "title": "Chief Executive Officer",
                    **_gov(approval_level="ceo", escalation_path=["board"]),
                },
                {
                    "id": "cto",
                    "name": "CTO",
                    "title": "Chief Technology Officer",
                    "reports_to": "ceo",
                    **_gov(approval_level="exec"),
                },
            ]
        },
        "departments": {
            "departments": [
                {"id": "engineering", "name": "Engineering", "executive": "cto"},
            ]
        },
        "specialists": {
            "specialists": [
                {
                    "id": "dev-1",
                    "name": "Dev",
                    "department": "engineering",
                    "reports_to": "cto",
                    **_gov(),
                },
            ]
        },
        "workflows": {"workflows": []},
        "approval_matrix": {"approval_matrix": []},
        "risk_matrix": {},
        "decision_tree": {},
    }


# ---------------------------------------------------------------------------
# Loader tests
# ---------------------------------------------------------------------------


class TestRegistryLoader:
    def test_load_all_returns_dict(self, loader: RegistryLoader):
        raw = loader.load_all()
        assert isinstance(raw, dict)
        assert "company" in raw
        assert "executives" in raw
        assert "departments" in raw

    def test_load_all_has_expected_keys(self, loader: RegistryLoader):
        raw = loader.load_all()
        expected_keys = {
            "company",
            "vision",
            "strategy",
            "culture",
            "governance",
            "policies",
            "kpis",
            "budget",
            "board",
            "committees",
            "board_meetings",
            "voting",
            "executives",
            "departments",
            "specialists",
            "workflows",
            "approval_matrix",
            "risk_matrix",
            "decision_tree",
        }
        assert expected_keys.issubset(raw.keys())

    def test_load_single_company(self, loader: RegistryLoader):
        data = loader.load_single("company")
        assert isinstance(data, dict)
        # company.yaml wraps data under 'company:' key
        assert "company" in data

    def test_load_single_unknown_key_raises(self, loader: RegistryLoader):
        with pytest.raises(KeyError):
            loader.load_single("nonexistent_key")


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestRegistryParser:
    def test_parse_returns_company_registry(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert isinstance(registry, CompanyRegistry)

    def test_parse_company(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert registry.company.id == "test-co"
        assert registry.company.name == "Test Company"
        assert registry.company.industry == "Tech"

    def test_parse_vision(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert registry.vision.mission == "Build great things"

    def test_parse_executives(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert len(registry.executives) == 2
        ceo = next(e for e in registry.executives if e.id == "ceo")
        assert ceo.title == "Chief Executive Officer"

    def test_parse_departments(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert len(registry.departments) == 1
        assert registry.departments[0].id == "engineering"
        assert registry.departments[0].executive == "cto"

    def test_parse_specialists(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert len(registry.specialists) == 1
        assert registry.specialists[0].department == "engineering"

    def test_parse_board(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert len(registry.board) == 1
        assert registry.board[0].id == "dir-1"

    def test_parse_budget(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        assert registry.budget.total_budget == 500000

    def test_parse_empty_data_returns_defaults(self):
        parser = RegistryParser()
        registry = parser.parse({})
        assert registry.company.id == "default"
        assert registry.executives == []
        assert registry.departments == []
        assert registry.specialists == []


# ---------------------------------------------------------------------------
# Resolver tests
# ---------------------------------------------------------------------------


class TestRegistryResolver:
    def test_resolve_runs_without_error(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        resolver = RegistryResolver()
        resolver.resolve(registry)  # Should not raise

    def test_resolve_preserves_data(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        resolver = RegistryResolver()
        resolver.resolve(registry)
        assert len(registry.executives) == 2
        assert len(registry.departments) == 1


# ---------------------------------------------------------------------------
# Validator tests
# ---------------------------------------------------------------------------


class TestRegistryValidator:
    def test_valid_registry_returns_no_errors(self, sample_raw: dict):
        parser = RegistryParser()
        registry = parser.parse(sample_raw)
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert errors == []

    def test_missing_company_name_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x"},
                "board": {"members": [{"id": "b1"}]},
                "budget": {"total_budget": 100},
            }
        )
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("name" in e.lower() for e in errors)

    def test_no_executives_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x", "name": "X"},
                "board": {"members": [{"id": "b1"}]},
                "budget": {"total_budget": 100},
            }
        )
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("executive" in e.lower() for e in errors)

    def test_no_departments_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x", "name": "X"},
                "executives": {"executives": [{"id": "e1"}]},
                "board": {"members": [{"id": "b1"}]},
                "budget": {"total_budget": 100},
            }
        )
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("department" in e.lower() for e in errors)

    def test_invalid_reports_to_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x", "name": "X"},
                "executives": {"executives": [{"id": "e1", "reports_to": "ghost"}]},
                "departments": {"departments": [{"id": "d1", "executive": "e1"}]},
                "board": {"members": [{"id": "b1"}]},
                "budget": {"total_budget": 100},
            }
        )
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("reports_to" in e for e in errors)

    def test_zero_budget_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x", "name": "X"},
                "executives": {"executives": [{"id": "e1"}]},
                "departments": {"departments": [{"id": "d1", "executive": "e1"}]},
                "board": {"members": [{"id": "b1"}]},
                "budget": {"total_budget": 0},
            }
        )
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("budget" in e.lower() for e in errors)


class TestGovernanceMandatoryFields:
    """Fail-fast: 4 MANDATORY fields on every agent (AI_WORKFORCE_90 §5.1)."""

    def test_missing_fields_on_executive_return_errors(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x", "name": "X"},
                "executives": {"executives": [{"id": "e1", "name": "E1"}]},
                "departments": {"departments": [{"id": "d1", "executive": "e1"}]},
                "specialists": {
                    "specialists": [{"id": "s1", "name": "S1", "department": "d1", **_gov()}]
                },
                "board": {"members": [{"id": "b1", **_gov(approval_level="board")}]},
                "budget": {"total_budget": 100},
            }
        )
        errors = RegistryValidator().validate(registry)
        for field in ("decision_rights", "approval_level", "escalation_path", "kpis"):
            assert any("e1" in e and field in e for e in errors), f"missing {field}"

    def test_empty_lists_return_errors(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x", "name": "X"},
                "executives": {
                    "executives": [
                        {
                            "id": "e1",
                            "name": "E1",
                            "decision_rights": [],
                            "approval_level": "exec",
                            "escalation_path": [],
                            "kpis": [],
                        }
                    ]
                },
                "departments": {"departments": [{"id": "d1", "executive": "e1"}]},
                "specialists": {
                    "specialists": [{"id": "s1", "name": "S1", "department": "d1", **_gov()}]
                },
                "board": {"members": [{"id": "b1", **_gov(approval_level="board")}]},
                "budget": {"total_budget": 100},
            }
        )
        errors = RegistryValidator().validate(registry)
        assert any("e1" in e and "decision_rights" in e for e in errors)
        assert any("e1" in e and "escalation_path" in e for e in errors)
        assert any("e1" in e and "kpis" in e for e in errors)

    def test_invalid_approval_level_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse(
            {
                "company": {"id": "x", "name": "X"},
                "executives": {
                    "executives": [
                        {
                            "id": "e1",
                            "name": "E1",
                            "decision_rights": ["r"],
                            "approval_level": "godmode",
                            "escalation_path": ["board"],
                            "kpis": ["k"],
                        }
                    ]
                },
                "departments": {"departments": [{"id": "d1", "executive": "e1"}]},
                "specialists": {
                    "specialists": [{"id": "s1", "name": "S1", "department": "d1", **_gov()}]
                },
                "board": {"members": [{"id": "b1", **_gov(approval_level="board")}]},
                "budget": {"total_budget": 100},
            }
        )
        errors = RegistryValidator().validate(registry)
        assert any("approval_level" in e and "godmode" in e for e in errors)

    def test_all_fields_present_on_all_agents_pass_governance(self, sample_raw: dict):
        registry = RegistryParser().parse(sample_raw)
        errors = RegistryValidator()._check_governance_fields(registry)
        assert errors == []

    def test_real_registry_passes_governance_check(self):
        from ai_company.registry import load_registry

        registry = load_registry()
        errors = RegistryValidator()._check_governance_fields(registry)
        assert errors == [], errors
        total = len(registry.executives) + len(registry.specialists) + len(registry.board)
        assert total == 90


# ---------------------------------------------------------------------------
# Registry Sync guardrail tests
# ---------------------------------------------------------------------------


class TestRegistrySync:
    """Guardrail: YAML registry (source of truth) and JSON registry (dashboard)
    must never drift apart. These tests catch desync regressions."""

    def test_yaml_and_json_agent_count_match(self):
        """The JSON registry must contain exactly as many agents as the YAML."""
        from ai_company.registry.sync import sync_registry, verify_sync

        # First, sync to ensure they match
        count = sync_registry()
        errors = verify_sync()
        assert errors == [], f"YAML/JSON desync detected after sync! Errors: {errors}"
        assert count > 0, "Sync produced zero agents"

    def test_sync_roundtrip_preserves_all_agents(self, tmp_path: Path):
        """Syncing to a temp JSON and reading it back must match the YAML."""
        from ai_company.registry.sync import sync_registry, verify_sync

        json_out = tmp_path / "agent-registry.json"
        count = sync_registry(json_path=json_out)
        errors = verify_sync(json_path=json_out)
        assert errors == [], f"Roundtrip sync drift: {errors}"
        assert count >= 90, f"Expected >= 90 agents, got {count}"

    def test_no_agents_lost_in_sync(self, tmp_path: Path):
        """Every YAML agent ID must appear in the JSON output."""
        import json

        import yaml

        from ai_company.registry.sync import sync_registry

        json_out = tmp_path / "agent-registry.json"
        sync_registry(json_path=json_out)

        with open("company-registry.yaml", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
        yaml_ids = {
            a["id"].replace("_", "-") for a in yaml_data.get("company", {}).get("agents", [])
        }

        with open(json_out, encoding="utf-8") as f:
            json_agents = json.load(f)
        json_names = {a["name"] for a in json_agents}

        missing = yaml_ids - json_names
        assert not missing, f"Agents lost during sync: {missing}"
