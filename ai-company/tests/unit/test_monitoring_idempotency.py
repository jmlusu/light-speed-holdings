"""Tests for idempotency / dedup monitoring metrics.

Covers:
- MO-1: Prometheus counters for idempotency violations
- MO-2: /api/dedup-metrics endpoint
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.monitoring import (
    get_metrics,
    inc_metric,
    set_metric,
)


class TestIdempotencyCounters:
    """Verify the idempotency metric keys exist and are incrementable."""

    def test_metrics_has_idempotency_counters(self) -> None:
        """get_metrics() must include all four idempotency counter keys."""
        metrics = get_metrics()
        expected_keys = {
            "idempotency_violations_total",
            "idempotency_key_dedup_total",
            "memory_dedup_total",
            "cost_dedup_total",
        }
        assert expected_keys.issubset(set(metrics.keys())), (
            f"Missing idempotency keys: {expected_keys - set(metrics.keys())}"
        )

    def test_metrics_defaults_are_zero(self) -> None:
        """All idempotency counters should default to 0 on a fresh process."""
        metrics = get_metrics()
        assert metrics["idempotency_violations_total"] == 0
        assert metrics["idempotency_key_dedup_total"] == 0
        assert metrics["memory_dedup_total"] == 0
        assert metrics["cost_dedup_total"] == 0

    def test_inc_metric_increments_idempotency_counter(self) -> None:
        """inc_metric() correctly increments idempotency counters."""
        initial = get_metrics()["idempotency_violations_total"]
        inc_metric("idempotency_violations_total")
        assert get_metrics()["idempotency_violations_total"] == initial + 1

        # Increment by a larger value
        inc_metric("idempotency_violations_total", 5.0)
        assert get_metrics()["idempotency_violations_total"] == initial + 6

    def test_inc_all_dedup_counters(self) -> None:
        """Every dedup counter can be independently incremented."""
        inc_metric("idempotency_key_dedup_total")
        inc_metric("memory_dedup_total")
        inc_metric("cost_dedup_total")

        m = get_metrics()
        assert m["idempotency_key_dedup_total"] >= 1
        assert m["memory_dedup_total"] >= 1
        assert m["cost_dedup_total"] >= 1

    def test_set_metric_works_for_idempotency(self) -> None:
        """set_metric() can directly set an idempotency counter value."""
        set_metric("memory_dedup_total", 42.0)
        assert get_metrics()["memory_dedup_total"] == 42.0


class TestPrometheusIdempotencyMetrics:
    """Verify the Prometheus text output includes idempotency metrics."""

    def test_prometheus_text_includes_idempotency_metrics(self) -> None:
        """The rendered Prometheus text must contain idempotency metric lines."""
        from ai_company.dashboard.monitoring import _render_prometheus_text

        # Reset counters to known state for deterministic output
        set_metric("idempotency_violations_total", 7)
        set_metric("idempotency_key_dedup_total", 3)
        set_metric("memory_dedup_total", 12)
        set_metric("cost_dedup_total", 5)

        text = _render_prometheus_text()

        assert "ai_company_idempotency_violations_total 7" in text
        assert "ai_company_idempotency_key_dedup_total 3" in text
        assert "ai_company_memory_dedup_total 12" in text
        assert "ai_company_cost_dedup_total 5" in text

    def test_prometheus_text_has_help_and_type_for_idempotency(self) -> None:
        """Each idempotency metric must have HELP and TYPE lines."""
        from ai_company.dashboard.monitoring import _render_prometheus_text

        text = _render_prometheus_text()

        for name, help_text in [
            ("ai_company_idempotency_violations_total", "Total tasks skipped due to duplicate ID"),
            ("ai_company_idempotency_key_dedup_total", "Total tasks skipped due to idempotency key match"),
            ("ai_company_memory_dedup_total", "Total memory entries skipped due to content hash dedup"),
            ("ai_company_cost_dedup_total", "Total cost records skipped due to composite key dedup"),
        ]:
            assert f"# HELP {name} {help_text}" in text, f"Missing HELP for {name}"
            assert f"# TYPE {name} counter" in text, f"Missing TYPE for {name}"


class TestDedupMetricsEndpoint:
    """Test the /api/dedup-metrics REST endpoint."""

    @pytest.fixture()
    def client(self, tmp_path: Path) -> TestClient:
        """App with StateStore bound to a temp root."""
        from ai_company.dashboard.app import create_app
        from ai_company.dashboard.repository import configure_state_store, reset_state_store

        reset_state_store()
        inbox = tmp_path / ".opencode"
        inbox.mkdir(parents=True, exist_ok=True)
        (inbox / "inbox.json").write_text("[]", encoding="utf-8")

        configure_state_store(tmp_path)
        app = create_app()
        with TestClient(app) as test_client:
            yield test_client
        reset_state_store()

    def test_dedup_metrics_endpoint(self, client: TestClient) -> None:
        """GET /api/dedup-metrics returns the expected JSON shape."""
        # Seed known values
        set_metric("tasks_total", 100)
        set_metric("idempotency_violations_total", 5)
        set_metric("memory_dedup_total", 3)
        set_metric("cost_dedup_total", 2)

        resp = client.get("/api/dedup-metrics")
        assert resp.status_code == 200

        data = resp.json()
        assert "idempotency" in data
        assert "memory" in data
        assert "cost" in data

        # Idempotency section
        idemp = data["idempotency"]
        assert idemp["total_task_sends"] == 100
        assert idemp["duplicates_prevented"] == 5
        assert idemp["dedup_rate_pct"] == 5.0

        # Memory section
        assert data["memory"]["duplicates_prevented"] == 3

        # Cost section
        assert data["cost"]["duplicates_prevented"] == 2

    def test_dedup_metrics_zero_tasks_no_division_error(self, client: TestClient) -> None:
        """When tasks_total is 0, dedup_rate_pct must be 0 (no ZeroDivisionError)."""
        set_metric("tasks_total", 0)
        set_metric("idempotency_violations_total", 0)
        set_metric("memory_dedup_total", 0)
        set_metric("cost_dedup_total", 0)

        resp = client.get("/api/dedup-metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert data["idempotency"]["dedup_rate_pct"] == 0

    def test_dedup_metrics_rate_calculation(self, client: TestClient) -> None:
        """dedup_rate_pct is correctly computed as a percentage."""
        set_metric("tasks_total", 200)
        set_metric("idempotency_violations_total", 10)
        set_metric("memory_dedup_total", 0)
        set_metric("cost_dedup_total", 0)

        resp = client.get("/api/dedup-metrics")
        assert resp.status_code == 200
        data = resp.json()
        # 10 / 200 * 100 = 5.0
        assert data["idempotency"]["dedup_rate_pct"] == 5.0
