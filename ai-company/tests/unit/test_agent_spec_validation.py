"""Tests for PRE-08B — AgentContext.validate() and 'agents validate' CLI command.

Covers:
  - AgentContext.validate() field checks
  - parse_agent_spec() returning empty/invalid specs
  - CLI 'agents validate' command
"""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ai_company.executor.context import AgentContext, parse_agent_spec


runner = CliRunner()


# ── AgentContext.validate() ─────────────────────────────────────────


class TestAgentContextValidate:
    def test_valid_context(self) -> None:
        ctx = AgentContext(
            name="lead-backend",
            role="Lead Backend Engineer",
            type="Specialist",
            department="Technology",
            reports_to="cto",
            mission="Build and maintain backend systems.",
            responsibilities=["Develop APIs", "Review code"],
            tools=["read", "write"],
            permission="Execute",
        )
        errors = ctx.validate()
        assert errors == []

    def test_empty_name(self) -> None:
        ctx = AgentContext(
            name="",
            role="Agent",
            type="Specialist",
            mission="Do stuff.",
            responsibilities=["A"],
            tools=["read"],
            permission="Execute",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("name" in e.lower() for e in errors)

    def test_whitespace_name(self) -> None:
        ctx = AgentContext(
            name="   ",
            role="Agent",
            type="Specialist",
            mission="Do stuff.",
            responsibilities=["A"],
            tools=["read"],
            permission="Execute",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("name" in e.lower() for e in errors)

    def test_invalid_type(self) -> None:
        ctx = AgentContext(
            name="agent",
            role="Agent",
            type="Manager",
            mission="Do stuff.",
            responsibilities=["A"],
            tools=["read"],
            permission="Execute",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("type" in e.lower() for e in errors)

    def test_empty_type(self) -> None:
        ctx = AgentContext(
            name="agent",
            role="Agent",
            type="",
            mission="Do stuff.",
            responsibilities=["A"],
            tools=["read"],
            permission="Execute",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("type" in e.lower() for e in errors)

    def test_empty_mission(self) -> None:
        ctx = AgentContext(
            name="agent",
            role="Agent",
            type="Specialist",
            mission="",
            responsibilities=["A"],
            tools=["read"],
            permission="Execute",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("mission" in e.lower() for e in errors)

    def test_empty_tools(self) -> None:
        ctx = AgentContext(
            name="agent",
            role="Agent",
            type="Specialist",
            mission="Do stuff.",
            responsibilities=["A"],
            tools=[],
            permission="Execute",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("tools" in e.lower() for e in errors)

    def test_empty_permission(self) -> None:
        ctx = AgentContext(
            name="agent",
            role="Agent",
            type="Specialist",
            mission="Do stuff.",
            responsibilities=["A"],
            tools=["read"],
            permission="",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("permission" in e.lower() for e in errors)

    def test_empty_responsibilities(self) -> None:
        ctx = AgentContext(
            name="agent",
            role="Agent",
            type="Specialist",
            mission="Do stuff.",
            responsibilities=[],
            tools=["read"],
            permission="Execute",
            reports_to="cto",
        )
        errors = ctx.validate()
        assert any("responsibilities" in e.lower() for e in errors)

    def test_empty_reports_to(self) -> None:
        ctx = AgentContext(
            name="agent",
            role="Agent",
            type="Specialist",
            mission="Do stuff.",
            responsibilities=["A"],
            tools=["read"],
            permission="Execute",
            reports_to="",
        )
        errors = ctx.validate()
        assert any("reports" in e.lower() for e in errors)

    def test_multiple_errors(self) -> None:
        ctx = AgentContext(
            name="",
            role="Agent",
            type="Invalid",
            mission="",
        )
        errors = ctx.validate()
        # Should have at least: name, type, mission, tools, permission, responsibilities, reports_to
        assert len(errors) >= 5

    def test_valid_board_type(self) -> None:
        ctx = AgentContext(
            name="board-chair",
            role="Board Chair",
            type="Board",
            mission="Oversee strategy.",
            responsibilities=["Approve budget"],
            tools=["read"],
            permission="ReviewOnly",
            reports_to="board_of_directors",
        )
        errors = ctx.validate()
        assert errors == []

    def test_valid_executive_type(self) -> None:
        ctx = AgentContext(
            name="ceo",
            role="Chief Executive Officer",
            type="Executive",
            mission="Lead the company.",
            responsibilities=["Set strategy"],
            tools=["read", "write", "delegate"],
            permission="Execute",
            reports_to="board_of_directors",
        )
        errors = ctx.validate()
        assert errors == []


# ── parse_agent_spec() returning defaults for malformed specs ───────


class TestParseAgentSpecMalformed:
    def test_missing_file_returns_defaults(self, tmp_path: Path) -> None:
        ctx = parse_agent_spec("nonexistent", str(tmp_path))
        assert ctx.name == "nonexistent"
        assert ctx.type == "Unknown"
        errors = ctx.validate()
        # Should have errors: name is ok, but type is invalid, no mission, etc.
        assert len(errors) > 0

    def test_empty_file_returns_parseable_context(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "empty.md").write_text("", encoding="utf-8")

        ctx = parse_agent_spec("empty", str(agents_dir))
        assert ctx.name == "empty"
        # Empty file → no frontmatter, no sections → most fields empty
        errors = ctx.validate()
        assert len(errors) > 0

    def test_valid_spec_passes_validation(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        spec = """\
---
name: qa-engineer
description: Quality assurance specialist
tools: ["read", "write", "execute"]
mode: subagent
permission:
  read: allow
  write: allow
  bash: allow
---

# QA Engineer

## Identity

Type: Specialist

Department: Quality Assurance

Reports To: qa_lead

---

## Mission

Ensures software quality through testing and automation.

---

## Responsibilities

- Write unit tests
- Run test suites
- Report quality metrics

---

## Operating Guidelines

Quality is everyone's job.
"""
        (agents_dir / "qa-engineer.md").write_text(spec, encoding="utf-8")

        ctx = parse_agent_spec("qa-engineer", str(agents_dir))
        errors = ctx.validate()
        assert errors == []
        assert ctx.type == "Specialist"
        assert ctx.department == "Quality Assurance"


# ── CLI 'agents validate' command ──────────────────────────────────


class TestAgentsValidateCLI:
    def test_validate_command_success(self, tmp_path: Path) -> None:
        from ai_company.cli.agents import app

        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        spec = """\
---
name: test-agent
description: A test agent
tools: ["read"]
mode: subagent
permission:
  read: allow
---

# Test Agent

## Identity

Type: Specialist

Department: Testing

Reports To: lead

---

## Mission

Test things.

---

## Responsibilities

- Run tests

---

## Operating Guidelines

Be thorough.
"""
        (agents_dir / "test-agent.md").write_text(spec, encoding="utf-8")

        result = runner.invoke(
            app,
            ["validate", "--agents-dir", str(agents_dir)],
        )
        assert result.exit_code == 0
        assert "passed" in result.output.lower()
        assert "test-agent" in result.output

    def test_validate_command_failure(self, tmp_path: Path) -> None:
        from ai_company.cli.agents import app

        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        # Spec with missing required fields
        spec = """\
---
name: bad-agent
---

# Bad Agent
"""
        (agents_dir / "bad-agent.md").write_text(spec, encoding="utf-8")

        result = runner.invoke(
            app,
            ["validate", "--agents-dir", str(agents_dir)],
        )
        assert result.exit_code == 1
        assert "FAIL" in result.output

    def test_validate_nonexistent_dir(self, tmp_path: Path) -> None:
        from ai_company.cli.agents import app

        result = runner.invoke(
            app,
            ["validate", "--agents-dir", str(tmp_path / "nope")],
        )
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_validate_empty_dir(self, tmp_path: Path) -> None:
        from ai_company.cli.agents import app

        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        result = runner.invoke(
            app,
            ["validate", "--agents-dir", str(agents_dir)],
        )
        assert result.exit_code == 1
        assert "no agent spec" in result.output.lower()

    def test_validate_multiple_agents(self, tmp_path: Path) -> None:
        from ai_company.cli.agents import app

        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        good_spec = """\
---
name: good-agent
description: Good
tools: ["read"]
mode: subagent
permission:
  read: allow
---

# Good Agent

## Identity

Type: Specialist

Department: Tech

Reports To: lead

---

## Mission

Do good things.

---

## Responsibilities

- Good task

---

## Operating Guidelines

Be good.
"""
        bad_spec = """\
---
name: bad-agent
---

# Bad Agent
"""
        (agents_dir / "good-agent.md").write_text(good_spec, encoding="utf-8")
        (agents_dir / "bad-agent.md").write_text(bad_spec, encoding="utf-8")

        result = runner.invoke(
            app,
            ["validate", "--agents-dir", str(agents_dir)],
        )
        assert result.exit_code == 1  # At least one failure
        assert "good-agent" in result.output
        assert "bad-agent" in result.output
        assert "1 passed" in result.output
        assert "1 failed" in result.output
