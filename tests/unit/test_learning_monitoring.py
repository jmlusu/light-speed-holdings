"""Deployment & Monitoring for the continuous-learning pipeline (ticket #232).

Covers:
- the ``AI_COMPANY_LEARNING_ENABLED`` feature-flag gate (rollback switch)
- the new Prometheus learning metric families on ``/metrics``
- the enriched ``/health`` memory-store section (knowledge growth, vector
  index health, last consolidation)
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import ai_company.memory.integration as memory_integration
from ai_company.dashboard.monitoring import _render_prometheus_text
from ai_company.memory.integration import learning_enabled


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset the learning flag and integration singleton between tests."""
    monkeypatch.delenv("AI_COMPANY_LEARNING_ENABLED", raising=False)


def test_learning_enabled_defaults_to_true_without_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AI_COMPANY_LEARNING_ENABLED", raising=False)
    assert learning_enabled() is True


@pytest.mark.parametrize("bad", ["0", "false", "no", "off", "False", "OFF", " 0 "])
def test_learning_enabled_disabled_by_disable_values(monkeypatch, bad) -> None:
    monkeypatch.setenv("AI_COMPANY_LEARNING_ENABLED", bad)
    assert learning_enabled() is False


def test_learning_enabled_any_other_value_enables(monkeypatch) -> None:
    monkeypatch.setenv("AI_COMPANY_LEARNING_ENABLED", "1")
    assert learning_enabled() is True
    monkeypatch.setenv("AI_COMPANY_LEARNING_ENABLED", "true")
    assert learning_enabled() is True
    monkeypatch.setenv("AI_COMPANY_LEARNING_ENABLED", "yes")
    assert learning_enabled() is True


def test_recall_context_is_empty_when_learning_disabled(
    monkeypatch,
    tmp_path: Path,
) -> None:
    # A store is present so any result would mean the gate failed to apply.
    memory_integration.init_memory(base_dir=str(tmp_path / "memory"))
    monkeypatch.setenv("AI_COMPANY_LEARNING_ENABLED", "0")
    assert memory_integration.recall_context("anything", limit=5) == []
    # Enabled again → store returns (empty here, but the guard is off).
    monkeypatch.delenv("AI_COMPANY_LEARNING_ENABLED", raising=False)
    assert memory_integration.recall_context("anything", limit=5) == []
    memory_integration._store = None
    memory_integration._vector_store = None


def test_render_emits_learning_enabled_gauge_even_when_disabled(
    monkeypatch,
    tmp_path: Path,
) -> None:
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)
    monkeypatch.setenv("AI_COMPANY_LEARNING_ENABLED", "0")
    try:
        body = _render_prometheus_text()
        assert "ai_company_learning_enabled 0" in body
        # Snapshot families must NOT appear while disabled.
        assert "ai_company_learning_avg_tokens_per_task" not in body
    finally:
        reset_state_store()


def test_render_emits_learning_families_from_snapshot(tmp_path: Path) -> None:
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)
    # Seed a persisted learning snapshot exactly where monitoring reads it.
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "metrics.json").write_text(
        json.dumps(
            {
                "snapshots": [
                    {
                        "avg_tokens_per_task": 2100.0,
                        "token_trend": "improving",
                        "avg_iterations_per_task": 3.5,
                        "iteration_trend": "stable",
                        "error_rate": 0.1,
                        "error_trend": "improving",
                        "memory_hit_rate": 0.8,
                        "memory_avg_similarity": 0.7,
                        "episodic_count": 4,
                        "semantic_count": 2,
                        "procedural_count": 1,
                        "aggregate_count": 0,
                        "last_consolidation": "2026-01-01T00:00:00+00:00",
                        "entries_pruned_total": 12,
                        "episodic_digested_total": 3,
                        "total_tasks_recorded": 5,
                        "snapshot_timestamp": time.time(),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    try:
        body = _render_prometheus_text()
        assert "ai_company_learning_enabled 1" in body
        assert "ai_company_learning_avg_tokens_per_task 2100.0" in body
        assert "ai_company_learning_token_trend 1" in body  # improving → 1
        assert "ai_company_learning_avg_iterations_per_task 3.5" in body
        assert "ai_company_learning_iteration_trend 0" in body  # stable → 0
        assert "ai_company_learning_error_rate 0.100" in body
        assert "ai_company_learning_error_trend 1" in body
        assert "ai_company_learning_memory_hit_rate 0.800" in body
        assert "ai_company_learning_memory_avg_similarity 0.700" in body
        assert "# TYPE ai_company_learning_entries_pruned_total counter" in body
        assert "ai_company_learning_entries_pruned_total 12" in body
        assert "ai_company_learning_episodic_digested_total 3" in body
        assert "ai_company_learning_tasks_recorded_total 5" in body
        for family in (
            "ai_company_learning_avg_tokens_per_task",
            "ai_company_learning_avg_iterations_per_task",
            "ai_company_learning_error_rate",
            "ai_company_learning_memory_hit_rate",
            "ai_company_learning_tasks_recorded_total",
        ):
            assert f"# TYPE {family} " in body
    finally:
        reset_state_store()


def test_health_reports_learning_section(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from ai_company.dashboard.app import create_app
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    get_state_store(tmp_path)

    # Seed memory dir + a metrics snapshot so last_consolidation resolves.
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "metrics.json").write_text(
        json.dumps(
            {
                "snapshots": [
                    {
                        "avg_tokens_per_task": 900.0,
                        "token_trend": "stable",
                        "avg_iterations_per_task": 2.0,
                        "iteration_trend": "stable",
                        "error_rate": 0.0,
                        "error_trend": "stable",
                        "memory_hit_rate": 0.5,
                        "memory_avg_similarity": 0.6,
                        "total_tasks_recorded": 2,
                        "entries_pruned_total": 0,
                        "episodic_digested_total": 0,
                        "snapshot_timestamp": time.time(),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    try:
        response = TestClient(create_app()).get("/health")
        assert response.status_code == 200
        data = response.json()
        memory_store = data["checks"]["memory_store"]
        assert isinstance(memory_store, dict)
        assert memory_store["learning_enabled"] is True
        assert "by_type" in memory_store
        assert memory_store.get("last_consolidation") is not None
    finally:
        reset_state_store()
