"""Tests for the AgentGenerator."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_company.generator import AgentGenerator


@pytest.fixture()
def sample_registry(tmp_path: Path) -> Path:
    data = {
        "company": {
            "name": "Test Corp",
            "agents": [
                {
                    "id": "test_exec",
                    "name": "Test Executive",
                    "title": "Executive",
                    "type": "executive",
                    "description": "A test executive agent.",
                    "mission": "Lead testing.",
                    "department": "Testing",
                    "reports_to": "CEO",
                    "direct_reports": ["test_spec"],
                    "responsibilities": ["Run tests"],
                    "guidelines": "Be thorough.",
                    "tools": ["read", "write", "execute", "delegate"],
                },
                {
                    "id": "test_spec",
                    "name": "Test Specialist",
                    "title": "Specialist",
                    "type": "specialist",
                    "description": "A test specialist agent.",
                    "mission": "Write tests.",
                    "department": "Testing",
                    "reports_to": "test_exec",
                    "responsibilities": ["Write tests"],
                    "guidelines": "Cover edge cases.",
                    "tools": ["read"],
                    "seniority": "mid",
                },
            ],
        }
    }
    registry_path = tmp_path / "company-registry.yaml"
    registry_path.write_text(yaml.dump(data), encoding="utf-8")
    return registry_path


@pytest.fixture()
def templates_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "templates"


@pytest.fixture()
def generator(sample_registry: Path, templates_dir: Path, tmp_path: Path) -> AgentGenerator:
    return AgentGenerator(
        registry_path=str(sample_registry),
        templates_dir=str(templates_dir),
        output_dir=str(tmp_path / "agents"),
    )


def test_load_registry(generator: AgentGenerator) -> None:
    data = generator.load_registry()
    agents = data["company"]["agents"]
    assert len(agents) == 2
    assert agents[0]["id"] == "test_exec"


def test_generate_all(generator: AgentGenerator) -> None:
    results = generator.generate_all()
    assert len(results) == 2
    names = {f.name for f in results}
    assert "test_exec.md" in names
    assert "test_spec.md" in names


def test_generate_file_content(generator: AgentGenerator) -> None:
    results = generator.generate_all()
    exec_file = [f for f in results if f.name == "test_exec.md"][0]
    content = exec_file.read_text(encoding="utf-8")
    assert "Test Executive" in content
    assert "Run tests" in content
    assert "mode: subagent" in content
    assert "tools:" in content
    assert "permission:" not in content


def test_tools_boolean_map_read_only(generator: AgentGenerator) -> None:
    results = generator.generate_all()
    spec_file = [f for f in results if f.name == "test_spec.md"][0]
    content = spec_file.read_text(encoding="utf-8")
    assert "write: false" in content
    assert "edit: false" in content
    assert "bash: false" in content
    assert "read: true" in content


def test_tools_boolean_map_full_access(generator: AgentGenerator) -> None:
    results = generator.generate_all()
    exec_file = [f for f in results if f.name == "test_exec.md"][0]
    content = exec_file.read_text(encoding="utf-8")
    assert "write: true" in content
    assert "edit: true" in content
    assert "bash: true" in content
    assert "read: true" in content
