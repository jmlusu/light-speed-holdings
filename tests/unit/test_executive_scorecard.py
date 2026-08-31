"""Contract tests for the executive health scorecard.

Covers :func:`ai_company.dashboard.data_service.get_executive_scorecard` and
the ``executive_scorecard`` section of ``GET /api/v1/ceo-dashboard``.  The
accessor reads ``kpis.executive`` from ``config/company/kpis.yaml``, computes
each executive KPI's ``current`` from live task telemetry, and reports
``status`` / ``trend`` / ``source`` plus a weighted ``health_score``.
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

client = TestClient(app, raise_server_exceptions=False)

REAL_ROOT = Path(__file__).resolve().parents[2]

REAL_EXEC_IDS = (
    "task_throughput",
    "agent_utilization",
    "cost_efficiency",
    "build_success_rate",
    "escalation_resolution_time",
    "approval_turnaround",
)

EXEC_CONTRACT_KEYS = (
    "id",
    "name",
    "category",
    "owner",
    "unit",
    "frequency",
    "target",
    "current",
    "status",
    "trend",
    "trend_pct",
    "source",
    "higher_is_better",
    "computed_at",
)


@pytest.fixture()
def setup_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    from ai_company.dashboard.repository import get_state_store, reset_state_store
    from ai_company.data import reset_database

    monkeypatch.chdir(tmp_path)
    reset_state_store()
    reset_database()
    get_state_store(tmp_path)

    yield tmp_path

    reset_database()


def _write_exec_config(root: Path, kpis: list[dict[str, Any]]) -> None:
    config_path = root / "config" / "company" / "kpis.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        yaml.safe_dump({"kpis": {"executive": kpis}}, sort_keys=False),
        encoding="utf-8",
    )


def _task_rows(
    *, completed: int = 0, failed: int = 0, pending: int = 0, resolved: int = 0
) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    rows: list[dict[str, Any]] = []
    idx = 0
    for _ in range(completed):
        idx += 1
        rows.append(_base_task(idx, "completed", now))
    for _ in range(failed):
        idx += 1
        rows.append(_base_task(idx, "failed", now))
    for _ in range(pending):
        idx += 1
        rows.append(_base_task(idx, "pending", now))
    for _ in range(resolved):
        idx += 1
        rows.append(_resolved_task(idx, now))
    return rows


def _base_task(idx: int, status: str, now: datetime) -> dict[str, Any]:
    return {
        "id": f"task-{idx}",
        "sender_id": "alpha",
        "receiver_id": "beta",
        "status": status,
        "created_at": (now - timedelta(hours=idx)).isoformat(),
        "updated_at": (now - timedelta(hours=idx) + timedelta(minutes=10)).isoformat(),
    }


def _resolved_task(idx: int, now: datetime) -> dict[str, Any]:
    created = now - timedelta(hours=idx)
    return {
        "id": f"task-{idx}",
        "sender_id": "alpha",
        "receiver_id": "beta",
        "status": "resolved",
        "created_at": created.isoformat(),
        "updated_at": (created + timedelta(minutes=30)).isoformat(),
    }


def _write_inbox_tasks(root: Path, tasks: list[dict[str, Any]]) -> None:
    inbox_dir = root / ".opencode"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    (inbox_dir / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")


def _exec_kpi(
    kpi_id: str,
    target: float,
    *,
    weight: int = 15,
    higher_is_better: bool = True,
) -> dict[str, Any]:
    return {
        "id": kpi_id,
        "name": kpi_id.replace("_", " ").title(),
        "category": "operations",
        "target": target,
        "unit": "percent",
        "frequency": "daily",
        "owner": "coo",
        "weight": weight,
        "higher_is_better": higher_is_better,
    }


class TestGetExecutiveScorecard:
    def test_real_repo_defaults_to_six_kpis(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_executive_scorecard

        data = get_executive_scorecard()
        ids = [kpi["id"] for kpi in data["executive_kpis"]]
        assert ids == list(REAL_EXEC_IDS)
        assert data["summary"]["total"] == 6
        for kpi in data["executive_kpis"]:
            assert set(kpi) == set(EXEC_CONTRACT_KEYS)
            assert kpi["trend"] in ("up", "stable", "down")
            assert kpi["status"] in ("on_track", "attention", "critical", "info")
            assert kpi["source"] in ("real_telemetry", "configured")
        # Health score is 0-100 when any weighted KPI is computed.
        if data["health_score"] is not None:
            assert 0.0 <= data["health_score"] <= 100.0

    def test_build_success_rate_computed_from_tasks(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_executive_scorecard

        _write_exec_config(setup_data, [_exec_kpi("build_success_rate", 99.5)])
        _write_inbox_tasks(setup_data, _task_rows(completed=9, failed=1))

        data = get_executive_scorecard(project_root=setup_data)
        kpis = {kpi["id"]: kpi for kpi in data["executive_kpis"]}

        kpi = kpis["build_success_rate"]
        assert kpi["current"] == 90.0  # 9 / (9+1)
        assert kpi["source"] == "real_telemetry"
        # 90.0 vs 99.5 target -> ratio 0.90 -> attention (0.7..1.0).
        assert kpi["status"] == "attention"

    def test_status_buckets_higher_is_better(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import _executive_status

        assert _executive_status(100.0, 90.0, True)[0] == "on_track"
        assert _executive_status(80.0, 100.0, True)[0] == "attention"
        assert _executive_status(50.0, 100.0, True)[0] == "critical"
        assert _executive_status(None, 100.0, True)[0] == "info"

    def test_status_buckets_lower_is_better(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import _executive_status

        # Lower is better: current below target is on_track.
        assert _executive_status(10.0, 60.0, False)[0] == "on_track"
        assert _executive_status(60.0, 60.0, False)[0] == "on_track"
        # current=80, target=60 -> attainment 60/80=0.75 -> attention.
        assert _executive_status(80.0, 60.0, False)[0] == "attention"
        # current=200, target=60 -> attainment 0.3 -> critical.
        assert _executive_status(200.0, 60.0, False)[0] == "critical"

    def test_health_score_weighted_average(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_executive_scorecard

        _write_exec_config(
            setup_data,
            [
                _exec_kpi("agent_utilization", target=100.0, weight=50),
                _exec_kpi("build_success_rate", target=100.0, weight=50),
            ],
        )
        # agent_utilization with zero registered agents and no window -> None -> excluded.
        # build_success_rate: 9/10 completed but 0 failed -> need failed tasks.
        _write_inbox_tasks(setup_data, _task_rows(completed=8, failed=2))
        data = get_executive_scorecard(project_root=setup_data)
        kpis = {kpi["id"]: kpi for kpi in data["executive_kpis"]}

        # build_success_rate = 80/100 -> attainment 0.8.
        assert kpis["build_success_rate"]["current"] == 80.0
        # agent_utilization has no data (no registry, no window agents are counted as
        # active because sender/receiver exist, but total_registered==0 -> None).
        assert kpis["agent_utilization"]["current"] is None

        # Only the computed KPI contributes -> health_score equals its attainment*100.
        # Weighted: build_success_rate only (agent_utilization has no attainment).
        assert data["health_score"] == 80.0

    def test_trend_reflects_prior_window(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_executive_scorecard

        _write_exec_config(setup_data, [_exec_kpi("task_throughput", 5.0)])
        now = datetime.now(timezone.utc)

        # 8 current-window tasks (within 30d).
        tasks = [
            {
                "id": f"c-{i}",
                "sender_id": "alpha",
                "receiver_id": "beta",
                "status": "completed",
                "created_at": (now - timedelta(hours=i)).isoformat(),
            }
            for i in range(8)
        ]
        # 2 prior-window tasks (31..32 days ago) -> throughput down -75%.
        for i in range(2):
            tasks.append(
                {
                    "id": f"p-{i}",
                    "sender_id": "alpha",
                    "receiver_id": "beta",
                    "status": "completed",
                    "created_at": (now - timedelta(days=31 + i)).isoformat(),
                }
            )
        _write_inbox_tasks(setup_data, tasks)

        data = get_executive_scorecard(project_root=setup_data, days=30)
        kpi = {k["id"]: k for k in data["executive_kpis"]}["task_throughput"]
        assert kpi["current"] == 8.0
        # prior window had 2 -> 8 vs 2 = +300% -> trend up.
        assert kpi["trend"] == "up"
        assert kpi["trend_pct"] == 300.0

    def test_missing_config_returns_empty(self, setup_data: Path) -> None:
        from ai_company.dashboard.data_service import get_executive_scorecard

        data = get_executive_scorecard(project_root=setup_data)
        assert data["executive_kpis"] == []
        assert data["health_score"] is None
        assert data["summary"]["total"] == 0


class TestCeoDashboardEndpoint:
    def test_ceo_dashboard_includes_executive_scorecard(self, setup_data: Path) -> None:
        resp = client.get("/api/v1/ceo-dashboard")
        assert resp.status_code == 200
        body = resp.json()
        scorecard = body["executive_scorecard"]
        assert (
            isinstance(scorecard["health_score"], (float, int)) or scorecard["health_score"] is None
        )
        assert len(scorecard["executive_kpis"]) == 6
        for kpi in scorecard["executive_kpis"]:
            assert kpi["status"] in ("on_track", "attention", "critical", "info")
            assert kpi["trend"] in ("up", "stable", "down")
            assert kpi["source"] in ("real_telemetry", "configured")
