"""Prometheus /metrics families for org-health + page-load (wayfinder #171).

Covers the runtime record functions, the band-transition counter, the
``/metrics`` exposition output for the new families, and the dashboard
page-load latency middleware.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import ai_company.dashboard.monitoring as monitoring_module
from ai_company.dashboard.app import create_app
from ai_company.dashboard.monitoring import (
    _render_prometheus_text,
    record_org_band_transition,
    record_org_breaker_trip,
    record_org_scoring,
    record_page_load,
)


@pytest.fixture(autouse=True)
def _fresh_metric_state() -> None:
    """Reset the wayfinder #171 metric stores between tests."""
    monitoring_module._org_component_stats.clear()
    monitoring_module._org_band_transitions.clear()
    monitoring_module._org_last_band = None
    monitoring_module._page_load_stats.clear()


def test_record_org_scoring_accumulates() -> None:
    record_org_scoring("task_success_rate", 0.5, ok=True)
    record_org_scoring("task_success_rate", 1.5, ok=True)
    record_org_scoring("error_rate", 0.25, ok=False)

    stats = monitoring_module._org_component_stats
    assert stats["task_success_rate"]["count"] == 2.0
    assert stats["task_success_rate"]["duration_sum"] == 2.0
    assert stats["task_success_rate"]["duration_last"] == 1.5
    assert stats["task_success_rate"]["failures"] == 0.0
    assert stats["task_success_rate"]["up"] == 1.0
    assert stats["error_rate"]["failures"] == 1.0
    assert stats["error_rate"]["up"] == 0.0


def test_record_org_breaker_trip_increments() -> None:
    record_org_breaker_trip("task_success_rate")
    record_org_breaker_trip("task_success_rate")
    assert monitoring_module._org_component_stats["task_success_rate"]["trips"] == 2.0


def test_band_transition_counts_only_real_changes() -> None:
    record_org_band_transition("green")
    record_org_band_transition("green")  # same band -> no transition
    record_org_band_transition("red")
    record_org_band_transition("amber")
    assert monitoring_module._org_band_transitions == {
        ("green", "red"): 1,
        ("red", "amber"): 1,
    }
    assert monitoring_module._org_last_band == "amber"


def test_render_includes_org_health_and_page_load_families() -> None:
    record_org_scoring("task_success_rate", 0.5, ok=True)
    record_org_scoring("error_rate", 0.25, ok=False)
    record_org_breaker_trip("error_rate")
    record_org_band_transition("green")
    record_org_band_transition("green")
    record_org_band_transition("red")
    record_page_load("/tasks", 0.1)
    record_page_load("/", 0.05)

    body = _render_prometheus_text()
    assert (
        'ai_company_org_health_component_scoring_count_total{component="task_success_rate"} 1'
        in body
    )
    assert (
        "ai_company_org_health_component_scoring_duration_sum_seconds{"
        'component="task_success_rate"} 0.500000' in body
    )
    assert (
        "ai_company_org_health_component_scoring_duration_last_seconds{"
        'component="task_success_rate"} 0.500000' in body
    )
    assert (
        'ai_company_org_health_component_scoring_failures_total{component="error_rate"} 1' in body
    )
    assert 'ai_company_org_health_component_breaker_trips_total{component="error_rate"} 1' in body
    assert 'ai_company_org_health_component_up{component="task_success_rate"} 1' in body
    assert 'ai_company_org_health_component_up{component="error_rate"} 0' in body
    assert 'ai_company_org_health_band{band="red"} 1' in body
    assert (
        'ai_company_org_health_band_transitions_total{previous="green",destination="red"} 1' in body
    )
    assert 'ai_company_dashboard_page_load_count_total{route="/"} 1' in body
    assert 'ai_company_dashboard_page_load_duration_last_seconds{route="/tasks"} 0.100000' in body
    for family in (
        "ai_company_org_health_component_scoring_count_total",
        "ai_company_org_health_component_scoring_duration_sum_seconds",
        "ai_company_org_health_band",
        "ai_company_dashboard_page_load_count_total",
    ):
        assert f"# TYPE {family} " in body


def test_page_load_middleware_records_only_html_requests() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    stats = monitoring_module._page_load_stats
    assert stats["/"]["count"] == 1.0
    assert stats["/"]["duration_last"] > 0.0

    client.get("/health")  # JSON, not a page load
    client.post("/api/v1/bootstrap-token")
    assert set(stats) == {"/"}
