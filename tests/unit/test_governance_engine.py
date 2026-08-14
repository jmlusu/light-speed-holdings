"""Contract tests for the data governance / retention engine (Sprint 3, item 3).

Covers the real-SQLite behaviour of :mod:`ai_company.data.governance`:

- retention enforcement (PURGE / ARCHIVE / ANONYMIZE) against isolated temp
  databases seeded with rows past and inside the retention window,
- governance reporting and compliance findings,
- the :class:`~ai_company.data.governance.GovernanceScheduler` time gating,
- the ``GET /api/governance`` dashboard endpoint.

Every test uses a real SQLite ``Database`` created under ``tmp_path`` — never
``MagicMock`` — and resets the module-level singleton so seeded data cannot
leak into other tests.  Retention policies always pass an explicit small
``retention_days`` so the suite never waits on the 365-day defaults.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from ai_company.data import governance as governance_module
from ai_company.data.database import Database
from ai_company.data.governance import DataGovernance, RetentionAction, RetentionPolicy

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture()
def db(tmp_path: Path) -> Database:
    """Isolated temp SQLite database (schema initialised, closed in teardown)."""
    database = Database(tmp_path / "governance.db")
    database.init_schema()
    yield database
    database.close()


@pytest.fixture()
def setup_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolated StateStore + reset SQLite singleton for the endpoint test."""
    from ai_company.dashboard.repository import get_state_store, reset_state_store
    from ai_company.data import reset_database

    monkeypatch.chdir(tmp_path)
    reset_state_store()
    reset_database()
    get_state_store(tmp_path)

    yield tmp_path

    reset_database()


# ── Helpers ─────────────────────────────────────────────────────────


def _ts(days_ago: float, now: datetime | None = None, *, local: bool = False) -> str:
    """ISO-8601 timestamp *days_ago* days before *now* (defaults to now).

    Defaults to UTC-aware — the convention the audit writer uses. Pass
    ``local=True`` for naive-local timestamps, matching the message_bus /
    memory / escalation / cost / kpi writers that back the other governed
    tables. Retention cutoffs are computed per-table in the same convention.
    """
    base = now or (datetime.now() if local else datetime.now(timezone.utc))
    return (base - timedelta(days=days_ago)).isoformat()


def _policy(
    table: str,
    *,
    action: RetentionAction,
    retention_days: int = 1,
    owner: str = "compliance",
    archive_path: str = "",
) -> RetentionPolicy:
    """Build an explicit small-window retention policy (no 365-day waits)."""
    return RetentionPolicy(
        table=table,
        owner=owner,
        retention_days=retention_days,
        action=action,
        archive_path=archive_path,
    )


def _seed_audit_events(
    db: Database,
    *,
    count: int,
    days_old: float,
    id_prefix: str = "evt",
) -> list[str]:
    """Insert *count* audit events *days_old* days old; return their ids."""
    ids: list[str] = []
    for i in range(count):
        eid = f"{id_prefix}-{i}"
        ids.append(eid)
        db.execute(
            """INSERT INTO audit_events
               (event_id, timestamp, event_type, agent_id, task_id, tool,
                args, result, metadata, severity)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                eid,
                _ts(days_old),
                "tool_call",
                "agent-alice",
                "task-1",
                "read",
                "{}",
                "{}",
                "{}",
                "info",
            ),
        )
    db.commit()
    return ids


def _seed_tasks(db: Database, *, old_count: int, new_count: int) -> None:
    """Insert *old_count* tasks past retention + *new_count* fresh tasks."""
    for i in range(old_count):
        db.execute(
            """INSERT INTO tasks (id, sender_id, receiver_id, status, created_at)
               VALUES (?,?,?,?,?)""",
            (f"task-old-{i}", "alpha", "beta", "completed", _ts(days_ago=30, local=True)),
        )
    for i in range(new_count):
        db.execute(
            """INSERT INTO tasks (id, sender_id, receiver_id, status, created_at)
               VALUES (?,?,?,?,?)""",
            (f"task-new-{i}", "alpha", "beta", "pending", _ts(days_ago=0.1, local=True)),
        )
    db.commit()


def _seed_memory_entries(
    db: Database,
    *,
    old_count: int,
    new_count: int,
    days_old: float = 30.0,
) -> None:
    """Insert *old_count* memory entries past retention + *new_count* fresh."""
    for i in range(old_count):
        db.execute(
            """INSERT INTO memory_entries (id, memory_type, content, agent_id, created_at)
               VALUES (?,?,?,?,?)""",
            (
                f"mem-old-{i}",
                "working",
                f"raw-secret-content-{i}",
                f"agent-{i}",
                _ts(days_old, local=True),
            ),
        )
    for i in range(new_count):
        db.execute(
            """INSERT INTO memory_entries (id, memory_type, content, agent_id, created_at)
               VALUES (?,?,?,?,?)""",
            (
                f"mem-new-{i}",
                "working",
                f"fresh-content-{i}",
                f"fresh-agent-{i}",
                _ts(days_ago=0.1, local=True),
            ),
        )
    db.commit()


# ── Engine: PURGE ───────────────────────────────────────────────────


class TestRetentionPurge:
    def test_purge_removes_old_keeps_new(self, db: Database) -> None:
        _seed_audit_events(db, count=1, days_old=30, id_prefix="old")  # past window
        _seed_audit_events(db, count=1, days_old=0.95, id_prefix="new")  # ~23h old

        gov = DataGovernance(
            db,
            policies=[
                _policy("audit_events", action=RetentionAction.PURGE, retention_days=1),
            ],
        )
        result = gov.apply_retention_policies()

        assert result["audit_events"] >= 1
        assert db.table_count("audit_events") == 1
        remaining = db.fetchone("SELECT event_id, timestamp FROM audit_events")
        assert remaining is not None
        assert remaining["event_id"] == "new-0"
        # The surviving row must be newer than the retention cutoff.
        assert remaining["timestamp"] > _ts(days_ago=1)


# ── Engine: ARCHIVE (batched) ──────────────────────────────────────


class TestRetentionArchive:
    def test_archive_exports_and_removes_exact_batch(
        self, db: Database, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _seed_tasks(db, old_count=5, new_count=2)
        # Force the archive loop into 3 batches (2+2+1) — all 5 must survive.
        monkeypatch.setattr(governance_module, "_ARCHIVE_BATCH_SIZE", 2)

        archive_dir = tmp_path / "archives"
        gov = DataGovernance(
            db,
            policies=[
                _policy(
                    "tasks",
                    action=RetentionAction.ARCHIVE,
                    retention_days=1,
                    owner="orchestrator",
                    archive_path=str(archive_dir),
                ),
            ],
        )
        result = gov.apply_retention_policies()

        assert result["tasks"] == 5

        archive_files = sorted(archive_dir.glob("*.json"))
        assert len(archive_files) == 1
        archived = json.loads(archive_files[0].read_text(encoding="utf-8"))
        archived_ids = {row["id"] for row in archived}
        assert archived_ids == {f"task-old-{i}" for i in range(5)}

        assert db.table_count("tasks") == 2
        remaining_ids = {row["id"] for row in db.fetchall("SELECT id FROM tasks")}
        assert remaining_ids == {f"task-new-{i}" for i in range(2)}


# ── Engine: ANONYMIZE ──────────────────────────────────────────────


class TestRetentionAnonymize:
    def test_anonymize_hashes_agent_id_and_content(self, db: Database) -> None:
        _seed_memory_entries(db, old_count=3, new_count=1)

        gov = DataGovernance(
            db,
            policies=[
                _policy(
                    "memory_entries",
                    action=RetentionAction.ANONYMIZE,
                    retention_days=1,
                    owner="data",
                ),
            ],
        )
        result = gov.apply_retention_policies()

        assert result["memory_entries"] == 3

        rows = db.fetchall("SELECT id, agent_id, content FROM memory_entries")
        by_id = {row["id"]: row for row in rows}
        for i in range(3):
            old = by_id[f"mem-old-{i}"]
            assert old["agent_id"].startswith("anon_")
            assert old["agent_id"] != f"agent-{i}"
            assert old["content"].startswith("anon_")
            assert old["content"] != f"raw-secret-content-{i}"

        # Fresh rows inside the retention window must be untouched.
        fresh = by_id["mem-new-0"]
        assert fresh["agent_id"] == "fresh-agent-0"
        assert fresh["content"] == "fresh-content-0"


# ── Reporting & compliance ─────────────────────────────────────────


class TestGovernanceReporting:
    def test_governance_report_and_compliance_reflect_data(self, db: Database) -> None:
        _seed_audit_events(db, count=1, days_old=30)

        gov = DataGovernance(
            db,
            policies=[
                _policy("audit_events", action=RetentionAction.PURGE, retention_days=1),
            ],
        )

        report = gov.governance_report()
        assert {"generated_at", "tables", "owners", "policies"} <= set(report)
        table_stats = report["tables"]["audit_events"]
        assert table_stats["row_count"] >= 1
        assert table_stats["records_past_retention"] >= 1
        assert table_stats["oldest_record"]
        assert report["policies"]

        findings = gov.compliance_check()
        matching = [
            finding
            for finding in findings
            if finding.get("table") == "audit_events" and "retention" in finding.get("finding", "")
        ]
        assert matching


# ── Scheduler ──────────────────────────────────────────────────────


class TestGovernanceScheduler:
    def test_governance_scheduler_interval_gating(self, db: Database) -> None:
        from ai_company.data.governance import GovernanceScheduler

        # memory_entries default policy is PURGE after 730 days — seed a row
        # far past that so a due pass returns a non-empty result dict.
        _seed_memory_entries(db, old_count=1, new_count=0, days_old=800)
        scheduler = GovernanceScheduler(interval_seconds=60, database=db)

        # First call at t=1000 is due → processes the 800-day-old row.
        result = scheduler.run_due(now=1_000.0)
        assert result.get("memory_entries", 0) >= 1

        # 50s later the 60s interval has not elapsed → no pass, empty dict.
        assert scheduler.run_due(now=1_050.0) == {}

        # 100s after the first run → due again. Re-seed so a row is processed.
        _seed_memory_entries(db, old_count=1, new_count=0, days_old=800)
        result = scheduler.run_due(now=1_100.0)
        assert result.get("memory_entries", 0) >= 1

        # reset() forces an immediate pass regardless of the clock.
        _seed_memory_entries(db, old_count=1, new_count=0, days_old=800)
        scheduler.reset()
        result = scheduler.run_due(now=1_101.0)
        assert result.get("memory_entries", 0) >= 1

    def test_governance_scheduler_disabled(self, db: Database) -> None:
        from ai_company.data.governance import GovernanceScheduler

        scheduler = GovernanceScheduler(interval_seconds=0, database=db)
        assert scheduler.run_due(now=1_000.0) == {}
        assert scheduler.run_due(now=9_999.0) == {}

    def test_governance_scheduler_no_database(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from ai_company.data import reset_database
        from ai_company.data.governance import GovernanceScheduler

        reset_database()
        # run_retention falls back to ai_company.data.get_database() — make it
        # resolve to None so the pass is skipped without raising.
        monkeypatch.setattr("ai_company.data.get_database", lambda: None)

        scheduler = GovernanceScheduler(interval_seconds=60, database=None)
        assert scheduler.run_due(now=1_000.0) == {}
        assert scheduler.run_due() == {}


# ── API endpoint ───────────────────────────────────────────────────


class TestGovernanceApiEndpoint:
    def test_api_governance_endpoint(self, setup_data: Path) -> None:
        from ai_company.data import init_database, reset_database

        db = init_database(setup_data / "analytics.db")
        _seed_audit_events(db, count=1, days_old=30)

        resp = client.get("/api/v1/governance")
        assert resp.status_code == 200
        body = resp.json()
        assert body["available"] is True
        assert body["generated_at"]
        assert isinstance(body["tables"], dict)
        assert body["tables"]
        assert isinstance(body["owners"], list)
        assert isinstance(body["policies"], list)
        assert body["policies"]

        # No database → available False with the empty shape.
        reset_database()
        resp = client.get("/api/v1/governance")
        assert resp.status_code == 200
        body = resp.json()
        assert body["available"] is False
        assert not body["tables"]
