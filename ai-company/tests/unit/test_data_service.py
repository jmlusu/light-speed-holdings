"""Tests for the SQLite-first read-through data service (S1.3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.dashboard.data_service import (
    get_all_tasks,
    get_cost_summary,
    get_kpi_history,
)
from ai_company.data import AuditStore, CostAnalytics, KPIPipeline, TaskStore
from ai_company.data.database import Database


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """A freshly initialised temporary database."""
    database = Database(tmp_path / "test.db")
    database.init_schema()
    yield database
    database.close()


def _seed_inbox(db: Database, tmp_path: Path) -> None:
    """Seed two tasks (one completed) via the legacy JSON importer."""
    inbox = [
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
    path = tmp_path / "inbox.json"
    path.write_text(json.dumps(inbox), encoding="utf-8")
    assert TaskStore(db).import_json(path) == 2


class TestGetAllTasks:
    def test_returns_none_when_database_empty(self, db: Database) -> None:
        assert get_all_tasks(database=db) is None

    def test_returns_tasks_when_populated(self, db: Database, tmp_path: Path) -> None:
        _seed_inbox(db, tmp_path)
        tasks = get_all_tasks(database=db)
        assert tasks is not None
        assert len(tasks) == 2
        assert {t["id"] for t in tasks} == {"task-1", "task-2"}

    def test_returns_none_when_database_unusable(self) -> None:
        assert get_all_tasks(database=None) is None


class TestGetCostSummary:
    def test_returns_none_when_no_cost_records(self, db: Database) -> None:
        assert get_cost_summary(database=db) is None

    def test_returns_spend_and_per_agent_from_sqlite(self, db: Database, tmp_path: Path) -> None:
        _seed_inbox(db, tmp_path)
        CostAnalytics(db).record_usage(
            model="gpt-x",
            provider="opencode",
            agent_name="cto",
            task_id="task-1",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=1.5,
        )
        CostAnalytics(db).record_usage(
            model="gpt-x",
            provider="opencode",
            agent_name="cfo",
            task_id="task-2",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.5,
        )

        summary = get_cost_summary(database=db)
        assert summary is not None
        assert summary["total_spent"] == pytest.approx(2.0)
        assert summary["completed_tasks"] == 1
        assert summary["total_tasks"] == 2
        assert summary["avg_cost_per_task"] == pytest.approx(2.0)

        by_agent = {a["agent"]: a for a in summary["per_agent_costs"]}
        assert by_agent["cto"]["total_cost"] == pytest.approx(1.5)
        assert by_agent["cfo"]["total_cost"] == pytest.approx(0.5)
        assert len(summary["cost_trend"]) == 1


class TestGetKpiHistory:
    def test_returns_none_when_no_entries(self, db: Database) -> None:
        assert get_kpi_history("engineering", database=db) is None

    def test_returns_entries_when_populated(self, db: Database) -> None:
        snapshot = {
            "collected_at": "2026-08-07T00:00:00+00:00",
            "departments": {
                "engineering": {
                    "kpis": {
                        "budget_utilization": {
                            "current": 5.6,
                            "target": 90.0,
                            "unit": "%",
                            "status": "ok",
                        }
                    }
                }
            },
        }
        assert KPIPipeline(db).ingest_snapshot(snapshot) == 1

        entries = get_kpi_history("engineering", database=db)
        assert entries is not None
        assert entries[0]["department"] == "engineering"
        assert entries[0]["kpi_key"] == "budget_utilization"
        assert entries[0]["current"] == pytest.approx(5.6)
        assert entries[0]["target"] == pytest.approx(90.0)

    def test_kpi_key_filter(self, db: Database) -> None:
        snapshot = {
            "departments": {
                "finance": {
                    "kpis": {
                        "budget_utilization": {"current": 1.0, "unit": "%"},
                        "cost_per_task": {"current": 2.0, "unit": "$"},
                    }
                }
            }
        }
        KPIPipeline(db).ingest_snapshot(snapshot)

        filtered = get_kpi_history("finance", "cost_per_task", database=db)
        assert filtered is not None
        assert len(filtered) == 1
        assert filtered[0]["kpi_key"] == "cost_per_task"


def test_audit_import_round_trip(db: Database, tmp_path: Path) -> None:
    """AuditStore import feeds the same schema the data service reads."""
    audit_file = tmp_path / "audit.jsonl"
    audit_file.write_text(
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
    assert AuditStore(db).import_jsonl(audit_file) == 1
    events = AuditStore(db).read_all()
    assert len(events) == 1
    assert events[0].metadata.get("cost") == 0.25
