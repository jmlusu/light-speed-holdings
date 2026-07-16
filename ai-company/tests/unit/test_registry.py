"""Tests for the registry system: loader, parser, resolver, validator."""

from pathlib import Path

import pytest

from ai_company.models import (
    Company,
    CompanyRegistry,
    Executive,
    Department,
    Agent,
    BoardMember,
    Workflow,
    ApprovalEntry,
    RiskMatrixConfig,
    DecisionTreeConfig,
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
        "board": {"members": [{"id": "dir-1", "name": "Alice"}]},
        "committees": {"committees": []},
        "board_meetings": {"meetings": []},
        "voting": {},
        "executives": {
            "executives": [
                {"id": "ceo", "name": "CEO", "title": "Chief Executive Officer"},
                {"id": "cto", "name": "CTO", "title": "Chief Technology Officer", "reports_to": "ceo"},
            ]
        },
        "departments": {
            "departments": [
                {"id": "engineering", "name": "Engineering", "executive": "cto"},
            ]
        },
        "specialists": {
            "specialists": [
                {"id": "dev-1", "name": "Dev", "department": "engineering", "reports_to": "cto"},
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
            "company", "vision", "strategy", "culture", "governance",
            "policies", "kpis", "budget", "board", "committees",
            "board_meetings", "voting", "executives", "departments",
            "specialists", "workflows", "approval_matrix", "risk_matrix",
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
        registry = parser.parse({
            "company": {"id": "x"},
            "board": {"members": [{"id": "b1"}]},
            "budget": {"total_budget": 100},
        })
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("name" in e.lower() for e in errors)

    def test_no_executives_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse({
            "company": {"id": "x", "name": "X"},
            "board": {"members": [{"id": "b1"}]},
            "budget": {"total_budget": 100},
        })
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("executive" in e.lower() for e in errors)

    def test_no_departments_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse({
            "company": {"id": "x", "name": "X"},
            "executives": {"executives": [{"id": "e1"}]},
            "board": {"members": [{"id": "b1"}]},
            "budget": {"total_budget": 100},
        })
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("department" in e.lower() for e in errors)

    def test_invalid_reports_to_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse({
            "company": {"id": "x", "name": "X"},
            "executives": {"executives": [{"id": "e1", "reports_to": "ghost"}]},
            "departments": {"departments": [{"id": "d1", "executive": "e1"}]},
            "board": {"members": [{"id": "b1"}]},
            "budget": {"total_budget": 100},
        })
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("reports_to" in e for e in errors)

    def test_zero_budget_returns_error(self):
        parser = RegistryParser()
        registry = parser.parse({
            "company": {"id": "x", "name": "X"},
            "executives": {"executives": [{"id": "e1"}]},
            "departments": {"departments": [{"id": "d1", "executive": "e1"}]},
            "board": {"members": [{"id": "b1"}]},
            "budget": {"total_budget": 0},
        })
        validator = RegistryValidator()
        errors = validator.validate(registry)
        assert any("budget" in e.lower() for e in errors)
