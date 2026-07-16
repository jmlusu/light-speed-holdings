"""Tests for the BootstrapEngine."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.builder import BootstrapEngine, COMPANY_DIRS
from ai_company.models import (
    Agent,
    ApprovalEntry,
    BoardMember,
    Budget,
    Company,
    CompanyRegistry,
    Committee,
    Department,
    Executive,
    RiskMatrixConfig,
    Strategy,
    Vision,
    VotingConfig,
    Workflow,
    WorkflowStep,
)


@pytest.fixture()
def sample_registry() -> CompanyRegistry:
    return CompanyRegistry(
        company=Company(id="test-co", name="Test Company", ceo="human-ceo"),
        vision=Vision(mission="Build great things"),
        strategy=Strategy(),
        executives=[
            Executive(id="ceo", title="CEO", name="CEO"),
            Executive(id="cto", title="CTO", reports_to="ceo", department="engineering"),
        ],
        departments=[
            Department(id="engineering", name="Engineering", executive="cto"),
        ],
        specialists=[
            Agent(id="dev-1", name="Developer", department="engineering", reports_to="cto",
                  tools=["read_file", "write_file"]),
        ],
        board=[
            BoardMember(id="dir-1", name="Alice", role="Chair"),
        ],
        committees=[],
        board_meetings=[],
        voting=VotingConfig(),
        workflows=[
            Workflow(
                id="hiring", name="Hiring", trigger="job_requisition",
                owner="hr", steps=[
                    WorkflowStep(id="s1", name="Post Job", action="Create job posting"),
                    WorkflowStep(id="s2", name="Review", action="Review resumes"),
                ],
            ),
        ],
        approval_matrix=[
            ApprovalEntry(action="budget_over_100k", risk_level="high", sla_hours=48),
        ],
        risk_matrix=RiskMatrixConfig(),
        policies=[],
        kpis=[],
        budget=Budget(total_budget=1000000, currency="USD"),
    )


@pytest.fixture()
def engine(tmp_path: Path) -> BootstrapEngine:
    return BootstrapEngine(
        config_dir="config",
        output_dir=str(tmp_path / ".opencode"),
        templates_dir="templates",
    )


class TestBootstrapEngine:
    def test_create_directories(self, engine: BootstrapEngine):
        dirs = engine._create_directories()
        assert len(dirs) == len(COMPANY_DIRS)
        for d in dirs:
            full = engine.output_dir / d
            assert full.exists(), f"Directory {d} was not created"

    def test_generate_agents(self, engine: BootstrapEngine, sample_registry: CompanyRegistry):
        agents = engine._generate_agents(sample_registry)
        assert len(agents) > 0
        # Should have executive, department, specialist, and board agents
        assert any("ceo" in a for a in agents)
        assert any("cto" in a for a in agents)
        assert any("dev" in a for a in agents)
        assert any("dir" in a for a in agents)

    def test_generate_configs(self, engine: BootstrapEngine, sample_registry: CompanyRegistry):
        configs = engine._generate_configs(sample_registry)
        assert len(configs) == 4
        assert "company.yaml" in configs
        assert "org_chart.yaml" in configs
        assert "workflows.yaml" in configs
        assert "governance.yaml" in configs

        # Verify files exist
        configs_dir = engine.output_dir / "config"
        assert (configs_dir / "company.yaml").exists()
        assert (configs_dir / "org_chart.yaml").exists()

    def test_full_bootstrap(self, engine: BootstrapEngine, sample_registry: CompanyRegistry):
        summary = engine.bootstrap(sample_registry)
        assert summary["company"] == "Test Company"
        assert len(summary["directories"]) == len(COMPANY_DIRS)
        assert len(summary["agents"]) > 0
        assert len(summary["configs"]) == 4
        assert summary["errors"] == []

    def test_bootstrap_idempotent(self, engine: BootstrapEngine, sample_registry: CompanyRegistry):
        """Running bootstrap twice should not fail."""
        engine.bootstrap(sample_registry)
        summary = engine.bootstrap(sample_registry)
        assert summary["errors"] == []

    def test_agent_files_are_valid_markdown(self, engine: BootstrapEngine, sample_registry: CompanyRegistry):
        engine.bootstrap(sample_registry)
        agents_dir = engine.output_dir / "agents"
        for md_file in agents_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{md_file.name} missing YAML frontmatter"
            assert "mode: subagent" in content, f"{md_file.name} missing mode: subagent"

    def test_config_yaml_is_valid(self, engine: BootstrapEngine, sample_registry: CompanyRegistry):
        engine.bootstrap(sample_registry)
        import yaml
        configs_dir = engine.output_dir / "config"
        for yml_file in configs_dir.glob("*.yaml"):
            with open(yml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            assert data is not None, f"{yml_file.name} is empty or invalid YAML"
