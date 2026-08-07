"""Tests for dashboard agent analytics — Sprint 3, item 1.

Covers the SQLite-first read-through for ``/api/agents/performance`` and
``/api/agents/{name}/performance`` (backed by
:class:`~ai_company.data.AgentPerformanceAnalytics`) plus the file-derived
fallback that keeps the endpoints non-blank before a backfill has run.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from ai_company.models.task import Task

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture()
def setup_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolated StateStore + empty database singleton for dashboard tests."""
    from ai_company.dashboard.repository import get_state_store, reset_state_store
    from ai_company.data import reset_database

    monkeypatch.chdir(tmp_path)
    reset_state_store()
    reset_database()
    get_state_store(tmp_path)

    (tmp_path / "company").mkdir(parents=True)
    registry = [
        {
            "name": "chief-of-staff",
            "role": "Chief of Staff",
            "type": "executive",
            "department": "Executive",
            "reportsTo": "human-ceo",
            "directReports": [],
            "description": "Coordinates all departments",
        },
        {
            "name": "lead-engineering",
            "role": "Lead Engineer",
            "type": "specialist",
            "department": "Engineering",
            "reportsTo": "chief-of-staff",
            "directReports": [],
            "description": "Leads engineering efforts",
        },
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")

    yield tmp_path

    reset_database()


def _seed_file_tasks(tmp_path: Path) -> None:
    """Write recent tasks to the legacy inbox for file-fallback tests."""
    now = datetime.now(timezone.utc)
    tasks = [
        {
            "id": "f1",
            "sender_id": "chief-of-staff",
            "receiver_id": "lead-engineering",
            "status": "completed",
            "created_at": (now - timedelta(hours=3)).isoformat(),
            "completed_at": (now - timedelta(hours=2, minutes=30)).isoformat(),
        },
        {
            "id": "f2",
            "sender_id": "chief-of-staff",
            "receiver_id": "lead-engineering",
            "status": "completed",
            "created_at": (now - timedelta(hours=2)).isoformat(),
            "completed_at": (now - timedelta(hours=1, minutes=45)).isoformat(),
        },
        {
            "id": "f3",
            "sender_id": "chief-of-staff",
            "receiver_id": "lead-engineering",
            "status": "failed",
            "created_at": (now - timedelta(hours=1)).isoformat(),
            "completed_at": (now - timedelta(minutes=50)).isoformat(),
        },
    ]
    (tmp_path / ".opencode" / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")


def _seed_sqlite(db) -> None:
    """Insert tasks / audit events / cost records (mirrors test_data_pipeline)."""
    from ai_company.data.database import Database

    assert isinstance(db, Database)
    now = datetime.now(timezone.utc)

    task_rows = [
        (
            "t1",
            "alice",
            "bob",
            "completed",
            now - timedelta(hours=3),
            now - timedelta(hours=2, minutes=30),
        ),
        (
            "t2",
            "alice",
            "bob",
            "completed",
            now - timedelta(hours=2),
            now - timedelta(hours=1, minutes=45),
        ),
        ("t3", "alice", "bob", "failed", now - timedelta(hours=1), now - timedelta(minutes=50)),
        (
            "t4",
            "charlie",
            "bob",
            "completed",
            now - timedelta(minutes=45),
            now - timedelta(minutes=25),
        ),
    ]
    for tid, sender, receiver, status, created, completed in task_rows:
        task = Task(
            id=tid,
            sender_id=sender,
            receiver_id=receiver,
            status=status,
            created_at=created.isoformat(),
            completed_at=completed.isoformat(),
        )
        db.execute(
            """INSERT INTO tasks (id, sender_id, receiver_id, status, created_at, completed_at, raw_json)
               VALUES (?,?,?,?,?,?,?)""",
            (
                tid,
                sender,
                receiver,
                status,
                created.isoformat(),
                completed.isoformat(),
                task.model_dump_json(),
            ),
        )

    audit_rows = [
        (
            "a1",
            "tool_call",
            "bob",
            "t1",
            (now - timedelta(hours=2, minutes=55)).isoformat(),
            "read",
            "info",
        ),
        (
            "a2",
            "tool_call",
            "bob",
            "t1",
            (now - timedelta(hours=2, minutes=50)).isoformat(),
            "write",
            "info",
        ),
        ("a3", "error", "bob", "t3", (now - timedelta(minutes=55)).isoformat(), None, "error"),
    ]
    for eid, etype, agent, tid, ts, tool, sev in audit_rows:
        db.execute(
            """INSERT INTO audit_events
               (event_id, timestamp, event_type, agent_id, task_id, tool, args, result, metadata, severity)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (eid, ts, etype, agent, tid, tool, "{}", "{}", "{}", sev),
        )

    cost_rows = [
        (
            (now - timedelta(hours=2, minutes=55)).isoformat(),
            "gpt-4o",
            "openai",
            "bob",
            "t1",
            100,
            50,
            0.01,
        ),
        (
            (now - timedelta(minutes=55)).isoformat(),
            "gpt-4o",
            "openai",
            "bob",
            "t3",
            200,
            100,
            0.02,
        ),
    ]
    for ts, model, prov, agent, tid, pt, ct, cost_val in cost_rows:
        db.execute(
            """INSERT INTO cost_records
               (timestamp, model, provider, agent_name, task_id,
                prompt_tokens, completion_tokens, cost_usd, iteration, metadata)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (ts, model, prov, agent, tid, pt, ct, cost_val, 1, "{}"),
        )

    db.commit()


# ── /api/agents/performance — file fallback ───────────────────────


class TestAgentPerformanceFileFallback:
    def test_returns_full_shape_with_empty_files(self, setup_data: Path) -> None:
        resp = client.get("/api/agents/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "files"
        assert data["period_days"] == 30
        assert data["total_tasks"] == 0
        assert {"name", "total_received", "completion_rate"} <= set(data["agents"][0])
        assert data["leaderboard"] == []
        assert data["model_usage"] == []
        assert data["task_durations"]["count"] == 0
        assert data["error_analysis"]["failed_tasks_by_agent"] == []

    def test_derives_leaderboard_from_inbox(self, setup_data: Path) -> None:
        _seed_file_tasks(setup_data)
        resp = client.get("/api/agents/performance")
        data = resp.json()
        assert data["source"] == "files"
        assert data["total_tasks"] == 3

        by_agent = {row["agent_id"]: row for row in data["leaderboard"]}
        assert by_agent["lead-engineering"]["tasks_received"] == 3
        assert by_agent["lead-engineering"]["tasks_completed"] == 2
        assert by_agent["lead-engineering"]["tasks_failed"] == 1
        assert by_agent["lead-engineering"]["completion_rate_pct"] == 66.67
        assert by_agent["chief-of-staff"]["tasks_sent"] == 3
        assert data["task_durations"]["count"] == 3
        assert data["task_durations"]["avg_seconds"] > 0

    def test_days_filter_excludes_old_tasks(self, setup_data: Path) -> None:
        old = datetime.now(timezone.utc) - timedelta(days=90)
        (setup_data / ".opencode" / "inbox.json").write_text(
            json.dumps(
                [
                    {
                        "id": "old",
                        "sender_id": "chief-of-staff",
                        "receiver_id": "lead-engineering",
                        "status": "completed",
                        "created_at": old.isoformat(),
                        "completed_at": (old + timedelta(minutes=30)).isoformat(),
                    }
                ]
            ),
            encoding="utf-8",
        )
        resp = client.get("/api/agents/performance", params={"days": 30})
        assert resp.status_code == 200
        assert resp.json()["total_tasks"] == 1
        assert resp.json()["leaderboard"] == []


# ── /api/agents/performance — SQLite-first path ────────────────────


class TestAgentPerformanceSQLite:
    def test_returns_analytics_from_sqlite(self, setup_data: Path) -> None:
        from ai_company.data import init_database

        db = init_database(setup_data / "analytics.db")
        _seed_sqlite(db)

        resp = client.get("/api/agents/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "sqlite"
        assert data["total_tasks"] == 4
        assert data["agents_with_tasks"] == 0  # registry agents have no tasks

        by_agent = {row["agent_id"]: row for row in data["leaderboard"]}
        assert by_agent["bob"]["tasks_received"] == 4
        assert by_agent["bob"]["completion_rate_pct"] == 75.0
        assert by_agent["bob"]["error_events"] == 1

        assert data["model_usage"] == [
            {
                "model": "gpt-4o",
                "provider": "openai",
                "agent_name": "bob",
                "calls": 2,
                "prompt_tokens": 300,
                "completion_tokens": 150,
                "cost_usd": 0.03,
            }
        ]
        errors = {
            e["event_type"]: e["count"] for e in data["error_analysis"]["error_events_by_agent"]
        }
        assert errors == {"error": 1}
        assert data["error_analysis"]["failed_tasks_by_agent"] == [{"agent_id": "bob", "count": 1}]

    def test_empty_database_falls_back_to_files(self, setup_data: Path) -> None:
        resp = client.get("/api/agents/performance")
        assert resp.status_code == 200
        assert resp.json()["source"] == "files"


# ── /api/agents/{name}/performance ────────────────────────────────


class TestAgentPerformanceDetail:
    def test_file_fallback(self, setup_data: Path) -> None:
        _seed_file_tasks(setup_data)
        resp = client.get("/api/agents/lead-engineering/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "files"
        assert data["agent_id"] == "lead-engineering"
        assert data["tasks_received"] == 3
        assert data["tasks_completed"] == 2

    def test_file_fallback_zeroed_for_unknown_agent(self, setup_data: Path) -> None:
        resp = client.get("/api/agents/never-heard-of/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "files"
        assert data["agent_id"] == "never-heard-of"
        assert data["tasks_received"] == 0

    def test_sqlite_path(self, setup_data: Path) -> None:
        from ai_company.data import init_database

        db = init_database(setup_data / "analytics.db")
        _seed_sqlite(db)

        resp = client.get("/api/agents/bob/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "sqlite"
        assert data["tasks_received"] == 4
        assert data["tasks_completed"] == 3
        assert data["tasks_failed"] == 1
        assert data["cost"]["llm_calls"] == 2

    def test_sqlite_no_data_for_agent_falls_back(self, setup_data: Path) -> None:
        from ai_company.data import init_database

        db = init_database(setup_data / "analytics.db")
        _seed_sqlite(db)

        resp = client.get("/api/agents/chief-of-staff/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "files"
        assert data["agent_id"] == "chief-of-staff"


# ── data_service read-through accessors ───────────────────────────


class TestDataServiceAccessors:
    def test_report_none_when_database_empty(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_agent_performance_report

        assert get_agent_performance_report() is None

    def test_report_returns_full_report_when_seeded(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_agent_performance_report
        from ai_company.data import init_database

        db = init_database(setup_data / "analytics.db")
        _seed_sqlite(db)

        report = get_agent_performance_report()
        assert report is not None
        assert report["leaderboard"][0]["agent_id"] == "bob"
        assert report["model_usage"][0]["model"] == "gpt-4o"

    def test_summary_none_for_missing_agent(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_agent_performance_summary

        assert get_agent_performance_summary("ghost") is None
