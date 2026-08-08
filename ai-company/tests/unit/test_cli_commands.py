"""Tests for CLI command registration, help, and smoke execution (Sprint 4 P2 — item 10.2).

Covers:
- ``ai-company --help`` (the main CLI entry).
- ``--help`` for every registered sub-app.
- A sample of commands (``memory stats``, ``governance report``, ``agents list``)
  executed against a temp registry / temp data so no real project data is touched.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from ai_company.cli.main import app

runner = CliRunner()

# Sub-apps required by Sprint 4 P2 (item 10.2). ``security`` is included because
# the sub-app is registered in src/ai_company/cli/main.py.
EXPECTED_SUB_APPS = [
    "agents",
    "board",
    "company",
    "customer-success",
    "dashboard",
    "decision",
    "departments",
    "doctor",
    "executives",
    "governance",
    "graph",
    "hr",
    "legal",
    "marketing",
    "memory",
    "models",
    "orchestrator",
    "sales",
    "specialists",
    "workflows",
    "validate",
    "security",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_minimal_registry(tmp_path: Path) -> None:
    """Write a minimal but valid registry so ``agents list`` can run offline.

    Mirrors the loader contract: ``company-registry.yaml`` (the single source of
    truth for agents) plus the small set of ``config/`` YAML files required by
    the registry validator.
    """
    (tmp_path / "company-registry.yaml").write_text(
        "company:\n"
        "  name: Smoke Test Co\n"
        "  id: smoke-co\n"
        "  agents:\n"
        "    - id: ceo\n"
        "      type: executive\n"
        "      name: CEO\n"
        "      title: Chief Executive\n"
        "      department: Executive\n"
        "      reports_to: board\n"
        "    - id: eng-spec\n"
        "      type: specialist\n"
        "      name: Engineer\n"
        "      department: Engineering\n"
        "      reports_to: ceo\n"
        "    - id: board-a\n"
        "      type: board\n"
        "      name: Board Member A\n"
        "      role: Director\n",
        encoding="utf-8",
    )
    config_company = tmp_path / "config" / "company"
    config_company.mkdir(parents=True, exist_ok=True)
    (config_company / "company.yaml").write_text(
        "company:\n  name: Smoke Test Co\n  id: smoke-co\n", encoding="utf-8"
    )
    (config_company / "budget.yaml").write_text(
        "budget:\n  total_budget: 100000\n", encoding="utf-8"
    )
    config_departments = tmp_path / "config" / "departments"
    config_departments.mkdir(parents=True, exist_ok=True)
    (config_departments / "departments.yaml").write_text(
        "departments:\n  - id: eng\n    name: Engineering\n    executive: ceo\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------


class TestMainHelp:
    """``ai-company --help`` — the root CLI entry."""

    def test_main_help_exits_zero(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

    def test_main_help_describes_company(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert "AI Company Builder" in result.output

    def test_main_help_lists_all_subapps(self) -> None:
        result = runner.invoke(app, ["--help"])
        for name in EXPECTED_SUB_APPS:
            assert name in result.output, f"sub-command '{name}' missing from help"


# ---------------------------------------------------------------------------
# Sub-app registration + help
# ---------------------------------------------------------------------------


class TestSubAppRegistration:
    """Every sub-app is registered and answers ``--help``."""

    def test_all_subapps_registered_programmatically(self) -> None:
        registered = {g.name for g in app.registered_groups}
        for name in EXPECTED_SUB_APPS:
            assert name in registered, f"sub-app '{name}' not registered"

    @pytest.mark.parametrize("sub_app", EXPECTED_SUB_APPS)
    def test_subapp_help(self, sub_app: str) -> None:
        result = runner.invoke(app, [sub_app, "--help"])
        assert result.exit_code == 0, f"{sub_app} --help failed: {result.output}"
        assert result.output.strip() != ""


# ---------------------------------------------------------------------------
# Command smoke tests (isolated from real data)
# ---------------------------------------------------------------------------


class TestCommandSmokeTests:
    """A sample of commands run without crashing against isolated temp data."""

    def test_status_command_runs(self) -> None:
        """The root ``status`` command is side-effect free."""
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Light Speed Holdings" in result.output

    def test_memory_stats_runs(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """``memory stats`` works against an empty temp memory store."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["memory", "stats"])
        assert result.exit_code == 0, result.output
        assert "Memory Store Summary" in result.output

    def test_governance_report_runs(self, tmp_path: Path) -> None:
        """``governance report --json`` works against a temp SQLite database."""
        db = str(tmp_path / "gov.db")
        result = runner.invoke(app, ["governance", "report", "--json", "-d", db])
        assert result.exit_code == 0, result.output
        assert "generated_at" in result.output

    def test_agents_list_runs(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """``agents list`` renders a registry built in a temp directory."""
        _write_minimal_registry(tmp_path)
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["agents", "list"])
        assert result.exit_code == 0, result.output
        assert "Total:" in result.output
        assert "Chief Executive" in result.output

    def test_agents_list_missing_registry_fails_gracefully(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Missing registry produces a clear error instead of a crash."""
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["agents", "list"])
        assert result.exit_code != 0
        assert "Registry not found or invalid" in result.output
