"""Tests for the periodic KPI snapshot scheduler (Sprint 2, Item 3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.dashboard.kpis import scheduler as scheduler_module
from ai_company.dashboard.kpis.scheduler import KPISnapshotScheduler, run_snapshot


@pytest.fixture()
def db(tmp_path: Path):
    from ai_company.data.database import Database

    database = Database(tmp_path / "kpi-scheduler.db")
    database.init_schema()
    yield database
    database.close()


@pytest.fixture()
def project_root(tmp_path: Path) -> Path:
    """An empty project root — file reads return zeros, SQLite provides tasks."""
    return tmp_path


def _seed_tasks(db, tmp_path: Path) -> None:
    """Seed tasks so the collected snapshot contains non-zero engineering KPIs."""
    from ai_company.data import TaskStore

    tasks = [
        {"id": "s1", "sender_id": "ceo", "receiver_id": "cto", "status": "completed"},
        {"id": "s2", "sender_id": "ceo", "receiver_id": "cto", "status": "pending"},
    ]
    path = tmp_path / "scheduler-inbox.json"
    path.write_text(json.dumps(tasks), encoding="utf-8")
    assert TaskStore(db).import_json(path) == 2


class TestRunSnapshot:
    def test_returns_zero_without_database(self) -> None:
        assert run_snapshot(database=None) == 0

    def test_collects_and_stores_into_sqlite(self, db, project_root: Path, tmp_path: Path) -> None:
        _seed_tasks(db, tmp_path)
        stored = run_snapshot(database=db, project_root=project_root)
        assert stored > 0

        from ai_company.data import KPIPipeline

        assert KPIPipeline(db).total_entries() == stored
        # Engineering KPIs must reflect the seeded SQLite tasks.
        history = KPIPipeline(db).get_history("engineering", "total_tasks")
        assert history
        assert history[0]["current_value"] == 2


class TestKPISnapshotScheduler:
    def test_takes_snapshot_when_interval_elapsed(
        self, db, project_root: Path, tmp_path: Path
    ) -> None:
        _seed_tasks(db, tmp_path)
        scheduler = KPISnapshotScheduler(
            interval_seconds=60,
            database=db,
            project_root=project_root,
        )
        assert scheduler.run_due(now=1_000.0) > 0

    def test_respects_interval(self, db, project_root: Path, tmp_path: Path) -> None:
        _seed_tasks(db, tmp_path)
        scheduler = KPISnapshotScheduler(
            interval_seconds=60,
            database=db,
            project_root=project_root,
        )
        assert scheduler.run_due(now=100.0) > 0
        # Only 50s later — must not fire again.
        assert scheduler.run_due(now=150.0) == 0
        # 70s after the first run — fires again.
        assert scheduler.run_due(now=170.0) > 0

    def test_disabled_interval_never_fires(self, db, project_root: Path) -> None:
        scheduler = KPISnapshotScheduler(
            interval_seconds=0,
            database=db,
            project_root=project_root,
        )
        assert scheduler.run_due(now=1_000.0) == 0

    def test_reset_forces_next_run(self, db, project_root: Path, tmp_path: Path) -> None:
        _seed_tasks(db, tmp_path)
        scheduler = KPISnapshotScheduler(
            interval_seconds=60,
            database=db,
            project_root=project_root,
        )
        scheduler.run_due(now=100.0)
        assert scheduler.run_due(now=120.0) == 0
        scheduler.reset()
        assert scheduler.run_due(now=130.0) > 0

    def test_never_raises_when_collection_fails(
        self, db, project_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _boom(*args: object, **kwargs: object) -> int:
            raise RuntimeError("collector exploded")

        monkeypatch.setattr(scheduler_module, "run_snapshot", _boom)
        scheduler = KPISnapshotScheduler(
            interval_seconds=60,
            database=db,
            project_root=project_root,
        )
        assert scheduler.run_due(now=1_000.0) == 0


class TestExecutorDaemonWiring:
    def test_builds_snapshot_scheduler_from_executor(self) -> None:
        from types import SimpleNamespace

        from ai_company.executor.daemon import ExecutorDaemon

        executor = SimpleNamespace(database=None)
        daemon = ExecutorDaemon(
            executor_factory=lambda: None,
            kpi_snapshot_interval=120,
        )
        scheduler = daemon._make_snapshot_scheduler(executor)
        assert scheduler is not None
        assert scheduler.interval_seconds == 120
        assert scheduler.database is None

    def test_disabled_interval_skips_scheduler(self) -> None:
        from types import SimpleNamespace

        from ai_company.executor.daemon import ExecutorDaemon

        daemon = ExecutorDaemon(
            executor_factory=lambda: None,
            kpi_snapshot_interval=0,
        )
        assert daemon._make_snapshot_scheduler(SimpleNamespace(database=None)) is None
