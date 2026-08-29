"""Org-health hardening wiring tests (wayfinder #170).

Covers the bulkhead timeout, per-component circuit breaker, fail-open caching
(last known-good), the compute deadline, the compute dedup window, and that
clean no-data scoring is unaffected.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import ai_company.dashboard.monitoring as monitoring_module
from ai_company.dashboard.org_health import OrgHealthCalculator


def _write_org_config(root: Path) -> None:
    """A single-component org_health.yaml so the stub scorer is the only input."""
    cfg = root / "config" / "org_health.yaml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        "bands:\n"
        "  green: {min: 80, max: 100}\n"
        "  amber: {min: 50, max: 79}\n"
        "  red: {min: 0, max: 49}\n"
        "components:\n"
        "  - {name: a, weight: 1.0}\n",
        encoding="utf-8",
    )


def _write_hardening(
    root: Path,
    *,
    call_timeout: float = 1.0,
    compute_timeout: float = 5.0,
    dedup: float = 0.0,
    threshold: int = 50,
) -> None:
    cfg = root / "company" / "config" / "hardening.yaml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        "org_health:\n"
        f"  call_timeout_s: {call_timeout}\n"
        f"  compute_timeout_s: {compute_timeout}\n"
        f"  dedup_window_s: {dedup}\n"
        "  worker_pool_size: 4\n"
        "  breaker:\n"
        f"    failure_threshold: {threshold}\n"
        "    recovery_timeout_s: 60.0\n"
        "    success_threshold: 1\n",
        encoding="utf-8",
    )


class StubCalculator(OrgHealthCalculator):
    """Replaces the scorers with a controllable stub."""

    def __init__(
        self,
        root: Path,
        *,
        sleep: float = 0.0,
        fail: bool = False,
        value: float = 90.0,
    ) -> None:
        super().__init__(project_root=root)
        self._sleep = sleep
        self._fail = fail
        self._stub_value = value
        self.stub_calls = 0

    def _scorers(self) -> dict[str, Any]:
        return {comp["name"]: lambda _db: self._stub_scorer() for comp in self._component_defs}

    def _stub_scorer(self) -> float:
        self.stub_calls += 1
        if self._sleep:
            time.sleep(self._sleep)
        if self._fail:
            raise RuntimeError("stub failure")
        return self._stub_value


def test_successful_scoring_is_unaffected(tmp_path: Path) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, threshold=3)
    calc = StubCalculator(tmp_path)
    result = calc.compute()
    assert result.components[0].value == 90.0
    assert result.score == 90
    assert result.band == "green"
    assert calc._get_breaker("a").is_available


def test_slow_scorer_times_out_and_fail_opens_to_none_on_cold_start(
    tmp_path: Path,
) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, call_timeout=0.05, compute_timeout=0.2, threshold=1)
    calc = StubCalculator(tmp_path, sleep=5.0)
    started = time.monotonic()
    result = calc.compute()
    assert time.monotonic() - started < 2.0  # never blocked on the hung scorer
    assert result.components[0].value is None  # cold start -> fail-open None
    assert result.score == 0


def test_timeout_trips_breaker_which_then_rejects_without_calling(
    tmp_path: Path,
) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, call_timeout=0.05, compute_timeout=0.2, threshold=1)
    calc = StubCalculator(tmp_path, sleep=5.0)
    assert calc.compute().components[0].value is None
    assert not calc._get_breaker("a").is_available
    calls_before = calc.stub_calls
    # Breaker open -> subsequent computes fail open without touching the scorer.
    assert calc.compute().components[0].value is None
    assert calc.stub_calls == calls_before


def test_failure_after_first_success_serves_last_known_good(
    tmp_path: Path,
) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, threshold=1)
    calc = StubCalculator(tmp_path, value=90.0)
    assert calc.compute().components[0].value == 90.0

    calc._fail = True
    result = calc.compute()
    assert result.components[0].value == 90.0  # last known-good, not dropped
    assert not calc._get_breaker("a").is_available


def test_scorer_exception_trips_breaker_and_fail_opens(tmp_path: Path) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, threshold=1)
    calc = StubCalculator(tmp_path, fail=True)
    result = calc.compute()
    assert result.components[0].value is None
    assert not calc._get_breaker("a").is_available


def test_compute_deadline_short_circuits_stuck_bulkhead(tmp_path: Path) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, call_timeout=0.05, compute_timeout=0.1, threshold=1)
    calc = StubCalculator(tmp_path, sleep=5.0)
    started = time.monotonic()
    result = calc.compute()
    assert time.monotonic() - started < 1.0
    assert result.components[0].value is None


def test_compute_dedup_window_returns_cached_result(tmp_path: Path) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, dedup=30.0)
    calc = StubCalculator(tmp_path, value=90.0)
    first = calc.compute()
    calc._stub_value = 10.0
    second = calc.compute()  # within the dedup window
    assert second is first
    assert second.components[0].value == 90.0
    assert calc.stub_calls == 1  # scorer ran exactly once


def test_unknown_component_still_returns_none(tmp_path: Path) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path)
    cfg = tmp_path / "config" / "org_health.yaml"
    cfg.write_text(
        "bands:\n"
        "  green: {min: 80, max: 100}\n"
        "  red: {min: 0, max: 49}\n"
        "components:\n"
        "  - {name: nonexistent, weight: 1.0}\n",
        encoding="utf-8",
    )
    calc = OrgHealthCalculator(project_root=tmp_path)
    result = calc.compute()
    assert result.score == 0
    assert result.components[0].value is None


def test_successful_compute_records_scoring_metrics(tmp_path: Path) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path)
    calc = StubCalculator(tmp_path)
    count_before = monitoring_module._org_component_stats.get("a", {}).get("count", 0.0)
    calc.compute()
    stats = monitoring_module._org_component_stats["a"]
    assert stats["count"] >= count_before + 1.0
    assert stats["up"] == 1.0
    assert monitoring_module._org_last_band == "green"


def test_failing_compute_records_failure_and_breaker_trip(tmp_path: Path) -> None:
    _write_org_config(tmp_path)
    _write_hardening(tmp_path, threshold=1)
    calc = StubCalculator(tmp_path, fail=True)
    failures_before = monitoring_module._org_component_stats.get("a", {}).get("failures", 0.0)
    trips_before = monitoring_module._org_component_stats.get("a", {}).get("trips", 0.0)
    result = calc.compute()
    assert result.components[0].value is None
    stats = monitoring_module._org_component_stats["a"]
    assert stats["failures"] >= failures_before + 1.0
    assert stats["trips"] >= trips_before + 1.0
    assert stats["up"] == 0.0
