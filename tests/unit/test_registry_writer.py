"""Tests for registry/writer.py — the single front door for YAML registry mutation.

Uses small synthetic fixtures in tmp_path (not the real 4k-line registry) so
each test is fast and isolated. The real-registry read-only guardrail lives in
test_registry.py::TestRegistrySync.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_company.registry.sync import verify_sync
from ai_company.registry.writer import set_reports_to

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_YAML = {
    "company": {
        "name": "Test Co",
        "agents": [
            {
                "id": "human_ceo",
                "name": "Human CEO",
                "type": "executive",
                "reports_to": "board",
                "tools": ["read"],
            },
            {
                "id": "chief_of_staff",
                "name": "Chief of Staff",
                "type": "executive",
                "reports_to": "human_ceo",
                "tools": ["read"],
            },
            {
                "id": "cto",
                "name": "CTO",
                "type": "executive",
                "reports_to": "chief_of_staff",
                "tools": ["read"],
            },
            {
                "id": "coo",
                "name": "COO",
                "type": "executive",
                "reports_to": "chief_of_staff",
                "tools": ["read"],
            },
        ],
    }
}


@pytest.fixture
def registry_paths(tmp_path: Path) -> tuple[Path, Path]:
    """Write the sample YAML to tmp_path; return (yaml_path, json_path)."""
    yaml_path = tmp_path / "company-registry.yaml"
    json_path = tmp_path / "agent-registry.json"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(SAMPLE_YAML, f, sort_keys=False)
    return yaml_path, json_path


def _write_json_from_yaml(yaml_path: Path, json_path: Path) -> None:
    """Produce a JSON in sync with the given YAML (used to set up deep-compare tests)."""
    from ai_company.registry.sync import sync_registry

    sync_registry(yaml_path=str(yaml_path), json_path=str(json_path))


# ---------------------------------------------------------------------------
# set_reports_to — happy path
# ---------------------------------------------------------------------------


class TestSetReportsTo:
    def test_happy_path_updates_yaml(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        yaml_path, json_path = registry_paths
        # Avoid invoking the real AgentGenerator (templates/output dirs) in unit tests.
        monkeypatch.setattr(
            "ai_company.generator.AgentGenerator.generate_all",
            lambda self: [],
        )
        _write_json_from_yaml(yaml_path, json_path)

        result = set_reports_to("coo", "cto", yaml_path=yaml_path, json_path=json_path)

        assert result == {"ok": True, "agent": "coo", "reports_to": "cto"}
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        agents = {a["id"]: a for a in data["company"]["agents"]}
        assert agents["coo"]["reports_to"] == "cto"

    def test_accepts_hyphenated_refs(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        yaml_path, json_path = registry_paths
        monkeypatch.setattr(
            "ai_company.generator.AgentGenerator.generate_all",
            lambda self: [],
        )
        _write_json_from_yaml(yaml_path, json_path)

        # Dashboard passes hyphenated names; YAML stores underscored ids.
        result = set_reports_to(
            "chief-of-staff", "human-ceo", yaml_path=yaml_path, json_path=json_path
        )
        assert result["agent"] == "chief-of-staff"
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        agents = {a["id"]: a for a in data["company"]["agents"]}
        assert agents["chief_of_staff"]["reports_to"] == "human_ceo"

    def test_sync_json_updated(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        yaml_path, json_path = registry_paths
        monkeypatch.setattr(
            "ai_company.generator.AgentGenerator.generate_all",
            lambda self: [],
        )
        _write_json_from_yaml(yaml_path, json_path)

        set_reports_to("cto", "coo", yaml_path=yaml_path, json_path=json_path)

        errors = verify_sync(yaml_path=yaml_path, json_path=json_path)
        assert errors == [], f"verify_sync reported drift after write: {errors}"

    def test_virtual_root_accepted(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        yaml_path, json_path = registry_paths
        monkeypatch.setattr(
            "ai_company.generator.AgentGenerator.generate_all",
            lambda self: [],
        )
        _write_json_from_yaml(yaml_path, json_path)

        result = set_reports_to("cto", "__root__", yaml_path=yaml_path, json_path=json_path)
        assert result["reports_to"] == "board"
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        agents = {a["id"]: a for a in data["company"]["agents"]}
        assert agents["cto"]["reports_to"] == "board"


# ---------------------------------------------------------------------------
# set_reports_to — validation failures
# ---------------------------------------------------------------------------


class TestSetReportsToValidation:
    def test_unknown_agent_raises(self, registry_paths: tuple[Path, Path]) -> None:
        yaml_path, json_path = registry_paths
        with pytest.raises(ValueError, match="not found"):
            set_reports_to("nonexistent", "cto", yaml_path=yaml_path, json_path=json_path)

    def test_unknown_manager_raises(self, registry_paths: tuple[Path, Path]) -> None:
        yaml_path, json_path = registry_paths
        with pytest.raises(ValueError, match="not found"):
            set_reports_to("cto", "nonexistent", yaml_path=yaml_path, json_path=json_path)

    def test_self_assign_raises(self, registry_paths: tuple[Path, Path]) -> None:
        yaml_path, json_path = registry_paths
        with pytest.raises(ValueError, match="itself"):
            set_reports_to("cto", "cto", yaml_path=yaml_path, json_path=json_path)

    def test_cycle_raises(self, registry_paths: tuple[Path, Path]) -> None:
        # Setup: chief_of_staff -> human_ceo; cto -> chief_of_staff.
        # Reassigning human_ceo -> cto would create human_ceo -> cto -> chief_of_staff -> human_ceo.
        yaml_path, json_path = registry_paths
        with pytest.raises(ValueError, match="cycle"):
            set_reports_to("human_ceo", "cto", yaml_path=yaml_path, json_path=json_path)

    def test_validation_failure_leaves_yaml_untouched(
        self, registry_paths: tuple[Path, Path]
    ) -> None:
        yaml_path, json_path = registry_paths
        before = yaml_path.read_text(encoding="utf-8")
        with pytest.raises(ValueError):
            set_reports_to("cto", "nonexistent", yaml_path=yaml_path, json_path=json_path)
        assert yaml_path.read_text(encoding="utf-8") == before


# ---------------------------------------------------------------------------
# set_reports_to — rollback on downstream failure
# ---------------------------------------------------------------------------


class TestSetReportsToRollback:
    def test_rollback_when_generate_all_fails(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        yaml_path, json_path = registry_paths
        before = yaml_path.read_text(encoding="utf-8")

        def boom(self):  # noqa: ANN001
            raise RuntimeError("generation exploded")

        monkeypatch.setattr("ai_company.generator.AgentGenerator.generate_all", boom)

        with pytest.raises(RuntimeError, match="generation exploded"):
            set_reports_to("cto", "coo", yaml_path=yaml_path, json_path=json_path)

        # YAML restored to pre-write state.
        assert yaml_path.read_text(encoding="utf-8") == before

    def test_rollback_when_sync_fails(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        yaml_path, json_path = registry_paths
        before = yaml_path.read_text(encoding="utf-8")

        monkeypatch.setattr(
            "ai_company.generator.AgentGenerator.generate_all",
            lambda self: [],
        )

        def boom(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
            raise RuntimeError("sync exploded")

        monkeypatch.setattr("ai_company.registry.sync.sync_registry", boom)

        with pytest.raises(RuntimeError, match="sync exploded"):
            set_reports_to("cto", "coo", yaml_path=yaml_path, json_path=json_path)

        assert yaml_path.read_text(encoding="utf-8") == before


# ---------------------------------------------------------------------------
# verify_sync — deep compare
# ---------------------------------------------------------------------------


class TestVerifySyncDeep:
    def test_detects_field_drift(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A directly-edited JSON reportsTo must be caught by the deep compare."""
        yaml_path, json_path = registry_paths
        monkeypatch.setattr(
            "ai_company.generator.AgentGenerator.generate_all",
            lambda self: [],
        )
        _write_json_from_yaml(yaml_path, json_path)

        # Simulate the old buggy PATCH: mutate JSON only, not YAML.
        import json

        with open(json_path, encoding="utf-8") as f:
            agents = json.load(f)
        for a in agents:
            if a["name"] == "cto":
                a["reportsTo"] = "human_ceo"  # YAML still says chief_of_staff
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(agents, f, indent=2)

        errors = verify_sync(yaml_path=yaml_path, json_path=json_path)
        assert errors, "verify_sync failed to detect field-level drift"
        assert any("reportsTo" in e and "cto" in e for e in errors), errors

    def test_passes_after_set_reports_to(
        self, registry_paths: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        yaml_path, json_path = registry_paths
        monkeypatch.setattr(
            "ai_company.generator.AgentGenerator.generate_all",
            lambda self: [],
        )
        _write_json_from_yaml(yaml_path, json_path)

        set_reports_to("coo", "cto", yaml_path=yaml_path, json_path=json_path)

        errors = verify_sync(yaml_path=yaml_path, json_path=json_path)
        assert errors == [], f"verify_sync reported drift after clean write: {errors}"
