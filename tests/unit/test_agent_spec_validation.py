"""Tests for GAP-019 agent spec validation.

Covers ``AgentContext.validate()`` (severity-aware issue reporting) and the
``ai-company agents validate`` CLI command (summary report, ``--json`` output,
``--agent`` filtering, and non-zero exit on ERROR-severity issues).
"""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ai_company.cli.agents import app
from ai_company.executor.context import Severity, ValidationIssue, parse_agent_spec

runner = CliRunner()

# A fully-populated spec modeled on the generated OpenCode v2 agent cards.
_WELL_FORMED_SPEC = """\
---
name: well-formed
description: A well-formed test agent.
mode: subagent
permission:
  read: allow
  edit: allow
---

# Well Formed

## Identity

Type: Specialist

Department: Engineering

Reports To: cto

---

## Mission

Execute test tasks well.

---

## Responsibilities

- Read files
- Write files

---

## Operating Guidelines

Be thorough and precise.

---

## Success Metrics

- All tasks complete

---

## Operating Principles

- Evidence over opinion
- Automate repetitive work

---
"""

# Missing the critical Mission / Responsibilities sections.
_BROKEN_SPEC = """\
---
name: broken-agent
description: A broken test agent.
mode: subagent
permission:
  read: allow
---

# Broken Agent

## Identity

Type: Specialist

---
"""

# Has Mission + Responsibilities but no tools / permission block.
_NO_TOOLS_SPEC = """\
---
name: no-tools
description: A test agent without tools.
mode: subagent
---

# No Tools

## Identity

Type: Specialist

Department: Engineering

Reports To: cto

---

## Mission

Works without tools.

---

## Responsibilities

- Think deeply

---
"""


def _write_spec(agents_dir: Path, name: str, content: str) -> Path:
    """Write an agent spec card into ``agents_dir`` and return its path."""
    agents_dir.mkdir(parents=True, exist_ok=True)
    path = agents_dir / f"{name}.md"
    path.write_text(content, encoding="utf-8")
    return path


def _issues_by_field(issues: list[ValidationIssue]) -> dict[str, list[ValidationIssue]]:
    """Group validation issues by their target field."""
    grouped: dict[str, list[ValidationIssue]] = {}
    for issue in issues:
        grouped.setdefault(issue.field, []).append(issue)
    return grouped


# ---------------------------------------------------------------------------
# AgentContext.validate()
# ---------------------------------------------------------------------------


class TestValidate:
    def test_well_formed_spec_returns_no_issues(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "well-formed", _WELL_FORMED_SPEC)

        ctx = parse_agent_spec("well-formed", str(agents_dir))
        issues = ctx.validate()

        assert issues == []

    def test_missing_mission_and_responsibilities_are_errors(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "broken-agent", _BROKEN_SPEC)

        ctx = parse_agent_spec("broken-agent", str(agents_dir))
        issues = ctx.validate()
        by_field = _issues_by_field(issues)

        assert by_field["mission"], "expected a mission issue"
        assert by_field["mission"][0].severity is Severity.ERROR

        assert by_field["responsibilities"], "expected a responsibilities issue"
        assert by_field["responsibilities"][0].severity is Severity.ERROR

    def test_missing_tools_is_warning(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "no-tools", _NO_TOOLS_SPEC)

        ctx = parse_agent_spec("no-tools", str(agents_dir))
        issues = ctx.validate()
        by_field = _issues_by_field(issues)

        assert by_field["tools"], "expected a tools issue"
        assert by_field["tools"][0].severity is Severity.WARNING
        assert all(i.severity is not Severity.ERROR for i in issues)

    def test_missing_role_is_warning(self) -> None:
        from ai_company.executor.context import AgentContext

        ctx = AgentContext(name="no-role", role="", type="Specialist")
        issues = ctx.validate()
        by_field = _issues_by_field(issues)

        assert by_field["role"], "expected a role issue"
        assert by_field["role"][0].severity is Severity.WARNING

    def test_unknown_type_is_warning(self) -> None:
        from ai_company.executor.context import AgentContext

        ctx = AgentContext(name="no-type", role="No Type", type="Unknown")
        issues = ctx.validate()
        by_field = _issues_by_field(issues)

        assert by_field["type"], "expected a type issue"
        assert by_field["type"][0].severity is Severity.WARNING


# ---------------------------------------------------------------------------
# CLI: ai-company agents validate
# ---------------------------------------------------------------------------


class TestValidateCli:
    def test_happy_path_all_agents_valid(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "well-formed", _WELL_FORMED_SPEC)

        result = runner.invoke(app, ["validate", "--agents-dir", str(agents_dir)])

        assert result.exit_code == 0, result.output
        assert "Validated: 1" in result.output
        assert "Valid: 1" in result.output
        assert "well-formed" in result.output

    def test_issue_detection_reports_and_exits_nonzero(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "broken-agent", _BROKEN_SPEC)

        result = runner.invoke(app, ["validate", "--agents-dir", str(agents_dir)])

        assert result.exit_code == 1
        assert "ERROR" in result.output
        assert "mission" in result.output
        assert "Valid: 0" in result.output
        assert "Errors: 2" in result.output  # mission + responsibilities

    def test_warning_only_agents_exit_zero(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "no-tools", _NO_TOOLS_SPEC)

        result = runner.invoke(app, ["validate", "--agents-dir", str(agents_dir)])

        assert result.exit_code == 0
        assert "Valid: 1" in result.output
        assert "Warnings:" in result.output

    def test_json_output(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "well-formed", _WELL_FORMED_SPEC)
        _write_spec(agents_dir, "broken-agent", _BROKEN_SPEC)

        result = runner.invoke(app, ["validate", "--json", "--agents-dir", str(agents_dir)])

        assert result.exit_code == 1  # broken-agent has ERROR issues
        data = json.loads(result.output)

        assert data["total_agents"] == 2
        assert data["valid"] == 1
        assert data["invalid"] == 1
        assert data["errors"] == 2
        assert isinstance(data["warnings"], int)
        assert len(data["agents"]) == 2

        by_name = {a["name"]: a for a in data["agents"]}
        assert by_name["well-formed"]["valid"] is True
        assert by_name["well-formed"]["issues"] == []

        broken = by_name["broken-agent"]
        assert broken["valid"] is False
        severities = {i["severity"] for i in broken["issues"]}
        fields = {i["field"] for i in broken["issues"]}
        assert severities == {"ERROR", "WARNING"}
        assert {"mission", "responsibilities"} <= fields

    def test_agent_option_limits_to_single_agent(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        _write_spec(agents_dir, "well-formed", _WELL_FORMED_SPEC)
        _write_spec(agents_dir, "broken-agent", _BROKEN_SPEC)

        result = runner.invoke(
            app, ["validate", "--agent", "well-formed", "--agents-dir", str(agents_dir)]
        )

        assert result.exit_code == 0, result.output
        assert "Validated: 1" in result.output
        assert "broken-agent" not in result.output

    def test_agent_option_missing_file_exits_nonzero(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir(parents=True)

        result = runner.invoke(
            app, ["validate", "--agent", "ghost", "--agents-dir", str(agents_dir)]
        )

        assert result.exit_code == 1
        assert "ghost" in result.output
        assert "ERROR" in result.output

    def test_missing_agents_dir_exits_nonzero(self, tmp_path: Path) -> None:
        result = runner.invoke(app, ["validate", "--agents-dir", str(tmp_path / "nope")])

        assert result.exit_code == 1
        assert "not found" in result.output
