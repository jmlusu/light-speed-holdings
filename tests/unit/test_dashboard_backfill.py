"""Tests for the ``dashboard backfill`` CLI command (S1.4)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ai_company.cli.dashboard import app
from ai_company.paths import AI_COMPANY_ROOT_ENV

runner = CliRunner()


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """A fake ai-company project root with legacy telemetry files."""
    root = tmp_path / "fake-ai-company"
    (root / ".opencode").mkdir(parents=True)
    (root / "orchestrator").mkdir(parents=True)
    (root / "results").mkdir(parents=True)
    (root / "dashboard" / "kpi_history").mkdir(parents=True)

    (root / ".opencode" / "inbox.json").write_text(
        json.dumps(
            [
                {
                    "id": "task-1",
                    "name": "First",
                    "sender_id": "ceo",
                    "receiver_id": "cto",
                    "status": "completed",
                },
                {
                    "id": "task-2",
                    "name": "Second",
                    "sender_id": "ceo",
                    "receiver_id": "cfo",
                    "status": "pending",
                },
            ]
        ),
        encoding="utf-8",
    )

    (root / ".opencode" / "audit").write_text(
        json.dumps(
            {
                "event_id": "evt-1",
                "timestamp": "2026-08-07T00:00:00+00:00",
                "event_type": "tool_call",
                "agent_id": "cto",
                "task_id": "task-1",
                "metadata": {"cost": 0.25},
            }
        )
        + "\n",
        encoding="utf-8",
    )

    (root / "orchestrator" / "escalation.yaml").write_text(
        json.dumps(
            {
                "events": [
                    {
                        "task_id": "task-1",
                        "rule_id": "rule-1",
                        "from_agent": "cto",
                        "to_agent": "ceo",
                        "reason": "blocked",
                        "timestamp": "2026-08-07T00:00:00+00:00",
                        "resolved": False,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    (root / "results" / "cost_log.jsonl").write_text(
        json.dumps(
            {
                "timestamp": "2026-08-07T00:00:00+00:00",
                "model": "gpt-x",
                "provider": "opencode",
                "agent_name": "cto",
                "task_id": "task-1",
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "cost_usd": 1.5,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    (root / "dashboard" / "kpi_history" / "engineering_history.ndjson").write_text(
        json.dumps(
            {
                "timestamp": "2026-08-07T00:00:00+00:00",
                "kpi_key": "budget_utilization",
                "current": 5.6,
                "target": 90.0,
                "unit": "%",
                "status": "ok",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return root


def _run_backfill(project_root: Path, db_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Invoke the backfill command anchored at a fake project root."""
    monkeypatch.setenv(AI_COMPANY_ROOT_ENV, str(project_root))
    return runner.invoke(app, ["backfill", "--db-path", str(db_path)])


class TestBackfillCommand:
    def test_backfill_populates_sqlite(
        self, project_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        db_path = tmp_path / "ai_company.db"
        result = _run_backfill(project_root, db_path, monkeypatch)
        assert result.exit_code == 0, result.output

        from ai_company.data.database import Database

        db = Database(db_path)
        assert db.get_schema_version() > 0
        assert db.table_count("tasks") == 2
        assert db.table_count("audit_events") == 1
        assert db.table_count("cost_records") == 1
        assert db.table_count("escalation_events") == 1
        assert db.table_count("kpi_values") == 1
        db.close()

    def test_backfill_is_idempotent(
        self, project_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Order-independence: the SQLite Database singleton is process-wide;
        # reset it so no stale connection/path leaks from an earlier test.
        from ai_company.data import reset_database

        reset_database()

        db_path = tmp_path / "ai_company.db"
        first = _run_backfill(project_root, db_path, monkeypatch)
        assert first.exit_code == 0, first.output
        second = _run_backfill(project_root, db_path, monkeypatch)
        assert second.exit_code == 0, second.output

        from ai_company.data.database import Database

        db = Database(db_path)
        assert db.table_count("tasks") == 2
        assert db.table_count("audit_events") == 1
        assert db.table_count("cost_records") == 1
        assert db.table_count("escalation_events") == 1
        db.close()

    def test_backfill_reports_missing_sources(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        empty_root = tmp_path / "empty"
        empty_root.mkdir()
        db_path = tmp_path / "ai_company.db"
        result = _run_backfill(empty_root, db_path, monkeypatch)
        assert result.exit_code == 0, result.output
        assert "Backfill complete" in result.output
