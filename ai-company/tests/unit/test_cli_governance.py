"""Tests for governance CLI commands (S3-02)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from ai_company.cli.governance import app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_db(tmp_path: Path) -> MagicMock:
    """Create a mock Database for governance tests."""
    db = MagicMock()
    db.table_count.return_value = 10
    db.fetchone.return_value = {"cnt": 0, "oldest": None, "newest": None}
    db.fetchall.return_value = []
    return db


# ---------------------------------------------------------------------------
# Tests: report
# ---------------------------------------------------------------------------

class TestGovernanceReport:

    def test_report_json(self, tmp_path: Path) -> None:
        """governance report --json outputs valid JSON."""
        mock_gov = MagicMock()
        mock_gov.governance_report.return_value = {
            "generated_at": "2026-07-22T00:00:00",
            "tables": {"tasks": {"row_count": 5, "classification": "internal", "owner": "orch", "retention_days": 365, "action": "archive", "records_past_retention": 0}},
            "owners": [],
            "policies": [],
        }

        with patch("ai_company.cli.governance._init_governance", return_value=(MagicMock(), mock_gov)):
            result = runner.invoke(app, ["report", "--json", "-d", str(tmp_path / "fake.db")])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "generated_at" in data
        assert "tables" in data
        assert "owners" in data
        assert "policies" in data


# ---------------------------------------------------------------------------
# Tests: audit-trail
# ---------------------------------------------------------------------------

class TestGovernanceAuditTrail:

    def test_audit_trail_empty(self, tmp_path: Path) -> None:
        """audit-trail with no audit file shows empty message."""
        with patch("ai_company.audit.reader.AuditReader") as MockReader:
            mock_reader = MagicMock()
            mock_reader.read_all.return_value = []
            MockReader.return_value = mock_reader
            result = runner.invoke(app, ["audit-trail"])

        assert result.exit_code == 0
        assert "No audit events found" in result.output

    def test_audit_trail_with_events(self, tmp_path: Path) -> None:
        """audit-trail with mock events displays them."""
        mock_event = MagicMock()
        mock_event.timestamp = "2026-07-22T10:00:00"
        mock_event.event_type.value = "tool_call"
        mock_event.agent_id = "cto"
        mock_event.task_id = "task-001"
        mock_event.detail = "Executed build command"

        with patch("ai_company.audit.reader.AuditReader") as MockReader:
            mock_reader = MagicMock()
            mock_reader.read_all.return_value = [mock_event]
            MockReader.return_value = mock_reader
            result = runner.invoke(app, ["audit-trail"])

        assert result.exit_code == 0
        assert "tool_call" in result.output
        assert "cto" in result.output

    def test_audit_trail_json_output(self, tmp_path: Path) -> None:
        """audit-trail --json outputs valid JSON list."""
        mock_event = MagicMock()
        mock_event.model_dump.return_value = {
            "timestamp": "2026-07-22T10:00:00",
            "event_type": "tool_call",
            "agent_id": "cto",
            "task_id": "t-1",
            "detail": "test",
        }

        with patch("ai_company.audit.reader.AuditReader") as MockReader:
            mock_reader = MagicMock()
            mock_reader.read_all.return_value = [mock_event]
            MockReader.return_value = mock_reader
            result = runner.invoke(app, ["audit-trail", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) == 1

    def test_audit_trail_filter_by_agent(self, tmp_path: Path) -> None:
        """audit-trail --agent filters correctly."""
        with patch("ai_company.audit.reader.AuditReader") as MockReader:
            mock_reader = MagicMock()
            mock_reader.read_by_agent.return_value = []
            MockReader.return_value = mock_reader
            result = runner.invoke(app, ["audit-trail", "--agent", "cto"])

        assert result.exit_code == 0
        mock_reader.read_by_agent.assert_called_once_with("cto")

    def test_audit_trail_filter_by_type(self, tmp_path: Path) -> None:
        """audit-trail --type filters correctly."""
        with patch("ai_company.audit.reader.AuditReader") as MockReader:
            mock_reader = MagicMock()
            mock_reader.read_by_type.return_value = []
            MockReader.return_value = mock_reader
            result = runner.invoke(app, ["audit-trail", "--type", "tool_call"])

        assert result.exit_code == 0
        mock_reader.read_by_type.assert_called_once_with("tool_call")


# ---------------------------------------------------------------------------
# Tests: risk-summary
# ---------------------------------------------------------------------------

class TestGovernanceRiskSummary:

    def test_risk_summary_json(self, tmp_path: Path) -> None:
        """risk-summary --json outputs valid JSON."""
        result = runner.invoke(app, ["risk-summary", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "total_risks" in data
        assert "by_level" in data
        assert "risks" in data
        assert data["total_risks"] > 0

    def test_risk_summary_text(self, tmp_path: Path) -> None:
        """risk-summary text output shows risk levels."""
        result = runner.invoke(app, ["risk-summary"])
        assert result.exit_code == 0
        assert "Risk Register Summary" in result.output
        assert "Total risks:" in result.output

    def test_risk_summary_groups_by_level(self, tmp_path: Path) -> None:
        """risk-summary groups risks by severity level."""
        result = runner.invoke(app, ["risk-summary", "--json"])
        data = json.loads(result.output)
        assert "High" in data["by_level"] or "Medium" in data["by_level"]
