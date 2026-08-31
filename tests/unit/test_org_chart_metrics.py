"""Contract tests for the rich org-chart metrics + risk.

Covers :func:`ai_company.graph.engine.compute_org_metrics` /
:func:`ai_company.graph.engine.org_chart_summary` (pure functions) and the
``GET /api/v1/org-chart?include_metrics=true`` endpoint, which attaches
per-node ``metrics``/``risk`` and exposes an ``X-Org-Summary`` header while
preserving the bare-list response shape for backward compatibility.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from ai_company.graph.engine import compute_org_metrics, org_chart_summary

client = TestClient(app, raise_server_exceptions=False)


def _agent(name: str, reports_to: str = "", **extra: Any) -> dict[str, Any]:
    base = {
        "name": name,
        "role": "Member",
        "type": "specialist",
        "department": "engineering",
        "reports_to": reports_to,
    }
    base.update(extra)
    return base


def _task(
    agent: str,
    status: str,
    *,
    age_days: float = 1.0,
    **extra: Any,
) -> dict[str, Any]:
    created = datetime.now(timezone.utc) - timedelta(days=age_days)
    task = {
        "id": f"t-{agent}-{status}-{id(extra)}",
        "sender_id": agent,
        "receiver_id": "other",
        "status": status,
        "created_at": created.isoformat(),
        "updated_at": created.isoformat(),
    }
    task.update(extra)
    return task


class TestComputeOrgMetrics:
    def test_capacity_active_over_work(self) -> None:
        agents = [_agent("alice")]
        tasks = [
            _task("alice", "in_progress", age_days=1),
            _task("alice", "in_progress", age_days=1),
            _task("alice", "pending", age_days=1),
        ]
        out = compute_org_metrics(agents, tasks)
        metrics = out["alice"]["metrics"]
        assert metrics["active"] == 2
        assert metrics["queued"] == 1
        assert metrics["completed"] == 0
        assert metrics["capacity"] == 66.7  # 2 / (2+1) * 100

    def test_completed_and_empty_work(self) -> None:
        agents = [_agent("bob")]
        tasks = [_task("bob", "completed", age_days=1)]
        out = compute_org_metrics(agents, tasks)
        metrics = out["bob"]["metrics"]
        assert metrics["completed"] == 1
        assert metrics["active"] == 0
        assert metrics["queued"] == 0
        # No active+queued -> capacity 0.0 (not NaN/div0).
        assert metrics["capacity"] == 0.0

    def test_utilization_trend(self) -> None:
        agents = [_agent("carol")]
        tasks = [
            _task("carol", "completed", age_days=1),  # recent week
            _task("carol", "completed", age_days=10),  # prior week
        ]
        out = compute_org_metrics(agents, tasks)
        # recent=1, prior=1 -> stable.
        assert out["carol"]["metrics"]["utilization_trend"] == "stable"

        tasks_up = [_task("carol", "completed", age_days=1)] * 2
        out_up = compute_org_metrics(agents, tasks_up)
        assert out_up["carol"]["metrics"]["utilization_trend"] == "up"

    def test_unknown_agent_zeroed(self) -> None:
        out = compute_org_metrics([_agent("dave")], [])
        assert out["dave"]["metrics"]["active"] == 0
        assert out["dave"]["metrics"]["queued"] == 0
        assert out["dave"]["metrics"]["capacity"] == 0.0


class TestRisk:
    def test_low_risk_with_reports_skills_tenure(self) -> None:
        agents = [
            _agent(
                "lead",
                "ceo",
                type="executive",
                skills=["a", "b", "c"],
                since="2015-01-01T00:00:00+00:00",
            ),
            _agent("r1", "lead"),
            _agent("r2", "lead"),
            _agent("r3", "lead"),
        ]
        out = compute_org_metrics(agents, [])
        assert out["lead"]["risk"]["succession_risk"] == "low"
        assert out["lead"]["risk"]["direct_reports"] == 3
        assert out["lead"]["risk"]["bus_factor"] == 3
        assert out["lead"]["risk"]["unique_skills"] == 3
        assert out["lead"]["risk"]["tenure"] == "senior"

    def test_high_risk_solo(self) -> None:
        agents = [_agent("solo", "ceo", type="executive")]
        out = compute_org_metrics(agents, [])
        assert out["solo"]["risk"]["succession_risk"] == "high"
        assert out["solo"]["risk"]["bus_factor"] == 0
        assert out["solo"]["risk"]["tenure"] == "unknown"


class TestOrgChartSummary:
    def test_summary_totals_and_span(self) -> None:
        agents = [
            _agent("ceo", "", type="executive"),
            _agent("lead", "ceo", type="executive"),
            _agent("spec", "lead", type="specialist"),
        ]
        metrics = compute_org_metrics(agents, [])
        summary = org_chart_summary(agents, metrics)
        assert summary["total_agents"] == 3
        assert summary["executives"] == 2
        assert summary["specialists"] == 1
        # spans: ceo has 1, lead has 1, spec has 0 -> avg 0.67
        assert summary["avg_span_of_control"] == 0.67


class TestOrgChartEndpoint:
    def test_default_is_bare_list_no_metrics(self) -> None:
        resp = client.get("/api/v1/org-chart")
        assert resp.status_code == 200
        chart = resp.json()
        assert isinstance(chart, list)
        assert "metrics" not in chart[0] or chart[0].get("metrics") is None

    def test_include_metrics_attaches_metrics_and_risk(self) -> None:
        resp = client.get("/api/v1/org-chart", params={"include_metrics": "true"})
        assert resp.status_code == 200
        chart = resp.json()
        assert isinstance(chart, list) and len(chart) >= 1

        fields = set()

        def visit(node: dict) -> None:
            fields.add(node.get("name"))
            assert node.get("metrics") is not None
            assert node.get("risk") is not None
            assert "capacity" in node["metrics"]
            assert "succession_risk" in node["risk"]
            for child in node.get("children", []):
                visit(child)

        for root in chart:
            visit(root)

        # Response header carries the aggregate summary.
        assert "X-Org-Summary" in resp.headers
        summary = json.loads(resp.headers["X-Org-Summary"])
        # Summary covers the full registry (incl. orphans outside the CEO
        # subtree), so it is a superset of the reachable tree.
        assert summary["total_agents"] >= len(fields)
        assert "avg_span_of_control" in summary
