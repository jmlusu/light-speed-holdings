"""Unit tests for the hardening config loader."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from ai_company.reliability.config import (
    HARDENING_DEFAULTS,
    get_hardening_value,
    load_hardening_config,
)


def test_defaults_used_when_file_missing(tmp_path: Path) -> None:
    cfg = load_hardening_config(tmp_path)
    assert get_hardening_value(cfg, "org_health.call_timeout_s") == 3.0
    assert get_hardening_value(cfg, "org_health.compute_timeout_s") == 15.0
    assert get_hardening_value(cfg, "org_health.worker_pool_size") == 4
    assert get_hardening_value(cfg, "org_health.dedup_window_s") == 5.0
    assert get_hardening_value(cfg, "org_health.breaker.failure_threshold") == 3
    assert get_hardening_value(cfg, "org_health.breaker.recovery_timeout_s") == 60.0
    assert get_hardening_value(cfg, "org_health.breaker.success_threshold") == 1


def test_missing_key_returns_default(tmp_path: Path) -> None:
    cfg = load_hardening_config(tmp_path)
    assert get_hardening_value(cfg, "daemon.tick.timeout_s", 5.0) == 5.0
    assert get_hardening_value(cfg, "org_health.does_not_exist", "fallback") == "fallback"


def test_file_values_override_defaults_deep_merge(tmp_path: Path) -> None:
    config = tmp_path / "company" / "config" / "hardening.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "org_health:\n  call_timeout_s: 0.25\n  breaker:\n    failure_threshold: 2\n",
        encoding="utf-8",
    )
    cfg = load_hardening_config(tmp_path)
    assert get_hardening_value(cfg, "org_health.call_timeout_s") == 0.25
    assert get_hardening_value(cfg, "org_health.breaker.failure_threshold") == 2
    # Untouched keys keep catalog defaults (deep merge, not replace).
    assert get_hardening_value(cfg, "org_health.breaker.recovery_timeout_s") == 60.0
    assert get_hardening_value(cfg, "org_health.worker_pool_size") == 4


def test_malformed_file_falls_back_to_defaults(tmp_path: Path) -> None:
    config = tmp_path / "company" / "config" / "hardening.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("not: [valid\n", encoding="utf-8")
    cfg = load_hardening_config(tmp_path)
    assert cfg == deepcopy(HARDENING_DEFAULTS)


def test_non_mapping_file_falls_back_to_defaults(tmp_path: Path) -> None:
    config = tmp_path / "company" / "config" / "hardening.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("- just\n- a\n- list\n", encoding="utf-8")
    cfg = load_hardening_config(tmp_path)
    assert cfg == deepcopy(HARDENING_DEFAULTS)
