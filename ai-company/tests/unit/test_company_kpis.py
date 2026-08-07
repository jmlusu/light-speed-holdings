"""Contract tests for company-level KPIs vs targets (Sprint 3, item 2).

Covers :func:`ai_company.dashboard.data_service.get_company_kpi_summary` and
the ``GET /api/company-kpis`` endpoint.  The accessor reads
``config/company/kpis.yaml`` for the five company KPIs, computes live
``current`` values for the telemetry-backed KPIs (``KPI-004`` Build Success
Rate, ``KPI-003`` Agent Utilization Rate) from SQLite first and the
``.opencode/inbox.json`` fallback, and keeps every other KPI on its configured
value.

Every KPI entry must expose exactly the contract keys: ``id``, ``name``,
``category``, ``owner``, ``frequency``, ``unit``, ``target``, ``current``,
``status``, ``gap``, ``computed``, ``source``.

Note on ``test_get_company_kpi_summary_defaults_to_real_repo``: the real repo
root holds live telemetry (the shipped ``.opencode/inbox.json``), so the
telemetry-backed KPIs may legitimately be *computed* rather than config-only.
The test therefore asserts the frozen contract rules against the returned
values (status/gap derived from the returned current/target) and checks
config fidelity for the config-backed KPIs, rather than pinning live currents.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest
import yaml
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from ai_company.data.database import Database

client = TestClient(app, raise_server_exceptions=False)

# Real ai-company repo root (tests/unit -> tests -> repo root).  Equivalent to
# ``Path(".").resolve()`` when pytest runs from the repo root, but immune to
# the ``monkeypatch.chdir`` isolation used in the fixture below.
REAL_ROOT = Path(__file__).resolve().parents[2]

# Every KPI entry must carry exactly these keys.
CONTRACT_KEYS = (
    "id",
    "name",
    "category",
    "owner",
    "frequency",
    "unit",
    "target",
    "current",
    "status",
    "gap",
    "computed",
    "source",
)

REAL_KPI_IDS = ("KPI-001", "KPI-002", "KPI-003", "KPI-004", "KPI-005")

# Minimal config fixture used by the file-fallback tests (mirrors the real
# config/company/kpis.yaml entries for these two KPIs).
KPI_001 = {
    "id": "KPI-001",
    "name": "Annual Recurring Revenue",
    "category": "finance",
    "target": 10000000,
    "current": 2500000,
    "unit": "usd",
    "frequency": "monthly",
    "owner": "cfo",
}
KPI_004 = {
    "id": "KPI-004",
    "name": "Build Success Rate",
    "category": "engineering",
    "target": 99.5,
    "current": 97.2,
    "unit": "percent",
    "frequency": "daily",
    "owner": "cto",
}


@pytest.fixture()
def setup_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolated StateStore + reset SQLite singleton for dashboard tests.

    Mirrors ``test_dashboard_agent_analytics.py``: the working directory and
    StateStore are anchored to ``tmp_path`` and the database singleton is
    reset before and after so seeded SQLite data cannot leak into other tests.
    """
    from ai_company.dashboard.repository import get_state_store, reset_state_store
    from ai_company.data import reset_database

    monkeypatch.chdir(tmp_path)
    reset_state_store()
    reset_database()
    get_state_store(tmp_path)

    yield tmp_path

    reset_database()


# ── Helpers ─────────────────────────────────────────────────────────


def _load_real_kpis() -> list[dict[str, Any]]:
    """Return the five company KPIs from the real repo config."""
    config_path = REAL_ROOT / "config" / "company" / "kpis.yaml"
    with open(config_path, encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}
    return list(config.get("kpis", {}).get("company", []))


def _write_kpis_config(root: Path, kpis: list[dict[str, Any]]) -> None:
    """Write ``config/company/kpis.yaml`` under *root*."""
    config_path = root / "config" / "company" / "kpis.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        yaml.safe_dump({"kpis": {"company": kpis}}, sort_keys=False),
        encoding="utf-8",
    )


def _task_rows(completed: int = 0, failed: int = 0, pending: int = 0) -> list[dict[str, Any]]:
    """Build task dicts (``alpha`` -> ``beta``) created within the last day."""
    now = datetime.now(timezone.utc)
    rows: list[dict[str, Any]] = []
    for i, status in enumerate(
        ["completed"] * completed + ["failed"] * failed + ["pending"] * pending,
        start=1,
    ):
        rows.append(
            {
                "id": f"task-{i}",
                "sender_id": "alpha",
                "receiver_id": "beta",
                "status": status,
                "created_at": (now - timedelta(hours=i)).isoformat(),
            }
        )
    return rows


def _write_inbox_tasks(root: Path, tasks: list[dict[str, Any]]) -> None:
    """Write ``.opencode/inbox.json`` under *root* (MessageBus task list)."""
    inbox_dir = root / ".opencode"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    (inbox_dir / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")


def _seed_sqlite_tasks(db: Database) -> None:
    """Insert 6 completed / 2 failed / 2 pending tasks into *db* (in-window)."""
    from ai_company.models.task import Task

    assert isinstance(db, Database)
    now = datetime.now(timezone.utc)
    rows = [
        ("t01", "alpha", "beta", "completed", now - timedelta(hours=6)),
        ("t02", "alpha", "beta", "completed", now - timedelta(hours=5)),
        ("t03", "alpha", "beta", "completed", now - timedelta(hours=4)),
        ("t04", "alpha", "beta", "completed", now - timedelta(hours=3)),
        ("t05", "alpha", "beta", "completed", now - timedelta(hours=2)),
        ("t06", "alpha", "beta", "completed", now - timedelta(hours=1)),
        ("t07", "alpha", "beta", "failed", now - timedelta(hours=7)),
        ("t08", "alpha", "beta", "failed", now - timedelta(hours=8)),
        ("t09", "alpha", "beta", "pending", now - timedelta(hours=9)),
        ("t10", "alpha", "beta", "pending", now - timedelta(hours=10)),
    ]
    for tid, sender, receiver, status, created in rows:
        completed_at = (
            (created + timedelta(minutes=30)).isoformat()
            if status in ("completed", "failed")
            else ""
        )
        task = Task(
            id=tid,
            sender_id=sender,
            receiver_id=receiver,
            status=status,
            created_at=created.isoformat(),
            completed_at=completed_at,
        )
        db.execute(
            """INSERT INTO tasks
               (id, sender_id, receiver_id, status, created_at, completed_at, raw_json)
               VALUES (?,?,?,?,?,?,?)""",
            (
                tid,
                sender,
                receiver,
                status,
                created.isoformat(),
                completed_at,
                task.model_dump_json(),
            ),
        )
    db.commit()


def _count_registered_agents(root: Path) -> int:
    """Count unique agent ids in ``company-registry.yaml``.

    Mirrors the contract: ``executives`` + ``specialists`` +
    ``departments[].agents`` (plus the repo's ``company.agents`` layout), with
    ids deduplicated across containers.
    """
    with open(root / "company-registry.yaml", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        return 0
    agent_ids: set[str] = set()
    for key in ("executives", "specialists"):
        group = data.get(key)
        if isinstance(group, list):
            for entry in group:
                if isinstance(entry, dict) and entry.get("id"):
                    agent_ids.add(str(entry["id"]))
    departments = data.get("departments")
    if isinstance(departments, list):
        for dept in departments:
            if not isinstance(dept, dict):
                continue
            dept_agents = dept.get("agents")
            if isinstance(dept_agents, list):
                for entry in dept_agents:
                    if isinstance(entry, dict) and entry.get("id"):
                        agent_ids.add(str(entry["id"]))
    company = data.get("company")
    if isinstance(company, dict):
        company_agents = company.get("agents")
        if isinstance(company_agents, list):
            for entry in company_agents:
                if isinstance(entry, dict) and entry.get("id"):
                    agent_ids.add(str(entry["id"]))
    return len(agent_ids)


def _expect_status_gap(current: Any, target: Any) -> tuple[str, Any]:
    """Return the contract ``(status, gap)`` for *current*/*target*."""
    if target is None:
        return "info", None
    if not isinstance(current, (int, float)) or not isinstance(target, (int, float)):
        return "info", None
    status = "on_track" if current >= target else "below_target"
    return status, round(target - current, 2)


# ── Accessor: get_company_kpi_summary ───────────────────────────────


class TestCompanyKpiSummary:
    def test_get_company_kpi_summary_defaults_to_real_repo(self, setup_data: Path) -> None:
        """No args resolves the real repo: 5 real KPIs, full contract shape."""
        from ai_company.dashboard.data_service import get_company_kpi_summary

        data = get_company_kpi_summary()
        by_id = {kpi["id"]: kpi for kpi in data["kpis"]}

        assert set(by_id) == set(REAL_KPI_IDS)
        assert data["summary"]["total"] == 5
        for kpi in data["kpis"]:
            assert set(kpi) == set(CONTRACT_KEYS)

        summary = data["summary"]
        assert summary["on_track"] + summary["below_target"] + summary["info"] == summary["total"]

        config_by_id = {kpi["id"]: kpi for kpi in _load_real_kpis()}
        for kpi_id, cfg in config_by_id.items():
            entry = by_id[kpi_id]
            assert entry["target"] == cfg["target"]
            if not entry["computed"]:
                # Config-backed KPIs must report the configured current.
                assert entry["source"] == "config"
                assert entry["current"] == cfg["current"]
            expected_status, expected_gap = _expect_status_gap(entry["current"], entry["target"])
            assert entry["status"] == expected_status
            assert entry["gap"] == expected_gap

    def test_computed_build_success_rate_sqlite(self, setup_data: Path) -> None:
        """Seeded SQLite telemetry drives KPI-004 and KPI-003 currents."""
        from ai_company.dashboard.data_service import get_company_kpi_summary
        from ai_company.data import init_database

        db = init_database(setup_data / "analytics.db")
        _seed_sqlite_tasks(db)

        data = get_company_kpi_summary(project_root=REAL_ROOT)
        by_id = {kpi["id"]: kpi for kpi in data["kpis"]}

        kpi004 = by_id["KPI-004"]
        assert kpi004["current"] == 75.0  # 6 completed / (6 + 2)
        assert kpi004["computed"] is True
        assert kpi004["source"] == "sqlite"
        expected_status, expected_gap = _expect_status_gap(kpi004["current"], kpi004["target"])
        assert kpi004["status"] == expected_status
        assert kpi004["gap"] == expected_gap

        # Seeded tasks all route alpha -> beta, so exactly two agents are active.
        active_agents = 2
        total_registered = _count_registered_agents(REAL_ROOT)
        assert total_registered > 0
        kpi003 = by_id["KPI-003"]
        assert kpi003["current"] == round(active_agents / total_registered * 100, 1)
        assert kpi003["computed"] is True
        assert kpi003["source"] == "sqlite"

    def test_computed_kpis_file_fallback(self, setup_data: Path) -> None:
        """No SQLite -> inbox.json drives KPI-004; KPI-001 stays config-backed."""
        from ai_company.dashboard.data_service import get_company_kpi_summary

        _write_kpis_config(setup_data, [KPI_001, KPI_004])
        _write_inbox_tasks(setup_data, _task_rows(completed=9, failed=1))

        data = get_company_kpi_summary(project_root=setup_data)
        by_id = {kpi["id"]: kpi for kpi in data["kpis"]}

        assert set(by_id) == {"KPI-001", "KPI-004"}

        kpi004 = by_id["KPI-004"]
        assert kpi004["current"] == 90.0  # 9 completed / (9 + 1)
        assert kpi004["computed"] is True
        assert kpi004["source"] == "files"
        expected_status, expected_gap = _expect_status_gap(kpi004["current"], kpi004["target"])
        assert kpi004["status"] == expected_status
        assert kpi004["gap"] == expected_gap

        kpi001 = by_id["KPI-001"]
        assert kpi001["current"] == KPI_001["current"]
        assert kpi001["computed"] is False
        assert kpi001["source"] == "config"

    def test_no_telemetry_falls_back_to_config(self, setup_data: Path) -> None:
        """No inbox -> every KPI reports its config current; statuses still computed."""
        from ai_company.dashboard.data_service import get_company_kpi_summary

        _write_kpis_config(setup_data, _load_real_kpis())

        data = get_company_kpi_summary(project_root=setup_data)
        assert len(data["kpis"]) == 5
        for kpi in data["kpis"]:
            assert kpi["computed"] is False
            assert kpi["source"] == "config"
            expected_status, expected_gap = _expect_status_gap(kpi["current"], kpi["target"])
            assert kpi["status"] == expected_status
            assert kpi["gap"] == expected_gap

    def test_missing_config_returns_empty_shape(self, setup_data: Path) -> None:
        """Empty root -> empty kpis + zero summary, never raises."""
        from ai_company.dashboard.data_service import get_company_kpi_summary

        data = get_company_kpi_summary(project_root=setup_data)

        assert data["kpis"] == []
        assert data["summary"] == {"total": 0, "on_track": 0, "below_target": 0, "info": 0}
        assert data["period_days"] == 30

    def test_window_filter_respects_days(self, setup_data: Path) -> None:
        """A completed task older than the window does not affect KPI-004."""
        from ai_company.dashboard.data_service import get_company_kpi_summary

        _write_kpis_config(setup_data, [KPI_004])
        tasks = _task_rows(completed=6, failed=2)
        tasks.append(
            {
                "id": "old-task",
                "sender_id": "alpha",
                "receiver_id": "beta",
                "status": "completed",
                "created_at": (datetime.now(timezone.utc) - timedelta(days=60)).isoformat(),
            }
        )
        _write_inbox_tasks(setup_data, tasks)

        data = get_company_kpi_summary(project_root=setup_data, days=30)
        kpi004 = {kpi["id"]: kpi for kpi in data["kpis"]}["KPI-004"]

        # 6 completed / 8 in-window tasks -> 75.0; the 60-day-old task is
        # excluded (including it would give 7/9 -> 77.8).
        assert kpi004["current"] == 75.0
        assert kpi004["computed"] is True
        assert kpi004["source"] == "files"


# ── Endpoint: GET /api/company-kpis ─────────────────────────────────


class TestCompanyKpisEndpoint:
    def test_api_endpoint_company_kpis(self, setup_data: Path) -> None:
        resp = client.get("/api/company-kpis")
        assert resp.status_code == 200
        body = resp.json()
        assert body["period_days"] == 30
        assert len(body["kpis"]) == 5  # the 5 real company KPIs
        assert body["summary"]["total"] == 5
        assert set(body["kpis"][0]) == set(CONTRACT_KEYS)

        resp90 = client.get("/api/company-kpis", params={"days": 90})
        assert resp90.status_code == 200
        assert resp90.json()["period_days"] == 90

        resp_bad = client.get("/api/company-kpis", params={"days": 0})
        assert resp_bad.status_code == 422
