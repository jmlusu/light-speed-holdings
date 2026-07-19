"""Tests for the KPI analytics module (history, trends, alerts, summary)
and the KPI data retention module (policy, cleanup, archive).
"""

from __future__ import annotations

import gzip
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from ai_company.dashboard.analytics import (
    AlertEngine,
    AlertRule,
    KPIHistoryStore,
    compute_summary,
    compute_trends,
)
from ai_company.dashboard.retention import RetentionEngine, RetentionPolicy


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def temp_storage_dir() -> Path:
    """Provide a temporary directory for the history store."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def store(temp_storage_dir: Path) -> KPIHistoryStore:
    """Return a KPIHistoryStore backed by a temp directory."""
    return KPIHistoryStore(storage_dir=temp_storage_dir / "kpi_history")


@pytest.fixture
def sample_snapshot() -> dict:
    """A realistic KPI snapshot resembling collect_all_kpis() output."""
    return {
        "collected_at": "2026-07-19T12:00:00",
        "departments": {
            "engineering": {
                "department": "engineering",
                "collected_at": "2026-07-19T12:00:00",
                "kpis": {
                    "task_completion_rate": {"current": 92.5, "target": 95, "unit": "%", "status": "below_target"},
                    "failure_rate": {"current": 3.0, "target": 0, "unit": "%", "status": "above_target"},
                    "pending_tasks": {"current": 5, "target": None, "unit": "count", "status": "info"},
                    "completed_tasks": {"current": 42, "target": None, "unit": "count", "status": "info"},
                    "open_escalations": {"current": 2, "target": 0, "unit": "count", "status": "above_target"},
                },
            },
            "hr": {
                "department": "hr",
                "collected_at": "2026-07-19T12:00:00",
                "kpis": {
                    "headcount": {"current": 150, "target": 160, "unit": "count", "status": "below_target"},
                    "satisfaction": {"current": 4.2, "target": 4.5, "unit": "score", "status": "below_target"},
                },
            },
        },
    }


@pytest.fixture
def older_snapshot() -> dict:
    """An older snapshot for trend testing."""
    return {
        "collected_at": "2026-07-19T11:00:00",
        "departments": {
            "engineering": {
                "department": "engineering",
                "collected_at": "2026-07-19T11:00:00",
                "kpis": {
                    "task_completion_rate": {"current": 88.0, "target": 95, "unit": "%", "status": "below_target"},
                    "failure_rate": {"current": 5.0, "target": 0, "unit": "%", "status": "above_target"},
                    "pending_tasks": {"current": 10, "target": None, "unit": "count", "status": "info"},
                    "completed_tasks": {"current": 30, "target": None, "unit": "count", "status": "info"},
                    "open_escalations": {"current": 3, "target": 0, "unit": "count", "status": "above_target"},
                },
            },
        },
    }


# ===========================================================================
# KPIHistoryStore — Snapshot storage and retrieval
# ===========================================================================


class TestKPIHistoryStore:
    """Tests for KPIHistoryStore — storing and retrieving KPI snapshots."""

    def test_store_snapshot_returns_count(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """Storing a snapshot returns the number of KPI entries stored."""
        count = store.store_snapshot(sample_snapshot)
        # engineering has 5 KPIs, hr has 2 = 7
        assert count == 7

    def test_get_history_returns_entries(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """Stored entries can be retrieved by department."""
        store.store_snapshot(sample_snapshot)
        entries = store.get_history("engineering")
        assert len(entries) == 5
        assert all(e.department == "engineering" for e in entries)

    def test_get_history_filter_by_kpi(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """Filtering by kpi_key returns only matching entries."""
        store.store_snapshot(sample_snapshot)
        entries = store.get_history("engineering", kpi_key="failure_rate")
        assert len(entries) == 1
        assert entries[0].kpi_key == "failure_rate"
        assert entries[0].current == 3.0

    def test_get_history_empty_department(self, store: KPIHistoryStore) -> None:
        """Unknown department returns an empty list."""
        assert store.get_history("nonexistent") == []

    def test_get_latest_after_multiple_snapshots(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """get_latest returns only the most recent snapshot entries."""
        older = dict(sample_snapshot)
        older["collected_at"] = "2026-07-19T10:00:00"
        store.store_snapshot(older)
        store.store_snapshot(sample_snapshot)

        latest = store.get_latest("engineering")
        assert len(latest) == 5
        assert all(e.timestamp == "2026-07-19T12:00:00" for e in latest)

    def test_get_latest_filter_kpi(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """get_latest with kpi_key returns only that KPI from the latest snapshot."""
        store.store_snapshot(sample_snapshot)
        latest = store.get_latest("engineering", kpi_key="task_completion_rate")
        assert len(latest) == 1
        assert latest[0].kpi_key == "task_completion_rate"
        assert latest[0].current == 92.5

    def test_list_departments(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """Storing snapshots makes departments discoverable."""
        store.store_snapshot(sample_snapshot)
        depts = store.list_departments()
        assert "engineering" in depts
        assert "hr" in depts

    def test_count_entries(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """count_entries returns the total stored entries for a department."""
        store.store_snapshot(sample_snapshot)
        assert store.count_entries("engineering") == 5
        assert store.count_entries("hr") == 2

    def test_clear_department(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """Clearing a department removes only its entries."""
        store.store_snapshot(sample_snapshot)
        removed = store.clear("engineering")
        assert removed == 5
        assert store.get_history("engineering") == []
        assert store.count_entries("hr") == 2

    def test_clear_all(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """Clearing all departments removes all entries."""
        store.store_snapshot(sample_snapshot)
        removed = store.clear()
        assert removed == 7
        assert store.list_departments() == []

    def test_store_multiple_snapshots_accumulates(self, store: KPIHistoryStore, older_snapshot: dict,
                                                    sample_snapshot: dict) -> None:
        """Multiple store calls accumulate entries."""
        store.store_snapshot(older_snapshot)
        store.store_snapshot(sample_snapshot)
        assert store.count_entries("engineering") == 10  # 5 + 5

    def test_history_limit(self, store: KPIHistoryStore, older_snapshot: dict, sample_snapshot: dict) -> None:
        """The limit parameter caps returned entries."""
        store.store_snapshot(older_snapshot)
        store.store_snapshot(sample_snapshot)
        entries = store.get_history("engineering", limit=3)
        assert len(entries) <= 3

    def test_history_since_filter(self, store: KPIHistoryStore, older_snapshot: dict,
                                   sample_snapshot: dict) -> None:
        """Filtering by since returns only entries at or after that timestamp."""
        store.store_snapshot(older_snapshot)
        store.store_snapshot(sample_snapshot)
        entries = store.get_history("engineering", since="2026-07-19T11:30:00")
        assert all(e.timestamp >= "2026-07-19T11:30:00" for e in entries)
        # Only the second snapshot qualifies
        assert len(entries) == 5

    def test_store_empty_department(self, store: KPIHistoryStore) -> None:
        """Storing a snapshot with no departments returns 0."""
        count = store.store_snapshot({"collected_at": "now", "departments": {}})
        assert count == 0


# ===========================================================================
# Trend Analysis
# ===========================================================================


class TestTrendAnalysis:
    """Tests for compute_trends."""

    def test_trend_computes_changes(self, store: KPIHistoryStore, older_snapshot: dict,
                                     sample_snapshot: dict) -> None:
        """Trends compute correct absolute and percentage changes."""
        store.store_snapshot(older_snapshot)
        store.store_snapshot(sample_snapshot)

        trends = compute_trends(store, "engineering")

        # Build lookup
        by_key = {t.kpi_key: t for t in trends}

        # task_completion_rate: 92.5 vs 88.0 → +4.5, +5.11%
        tcr = by_key["task_completion_rate"]
        assert tcr.current_value == 92.5
        assert tcr.previous_value == 88.0
        assert tcr.absolute_change == 4.5
        assert tcr.percentage_change is not None
        assert abs(tcr.percentage_change - 5.11) < 0.1
        assert tcr.direction == "up"

        # failure_rate: 3.0 vs 5.0 → -2.0, -40.0%
        fr = by_key["failure_rate"]
        assert fr.current_value == 3.0
        assert fr.previous_value == 5.0
        assert fr.absolute_change == -2.0
        assert fr.percentage_change == -40.0
        assert fr.direction == "down"

        # pending_tasks: 5 vs 10 → -5, -50%
        pt = by_key["pending_tasks"]
        assert pt.current_value == 5
        assert pt.previous_value == 10
        assert pt.absolute_change == -5.0
        assert pt.percentage_change == -50.0

    def test_trend_with_single_snapshot(self, store: KPIHistoryStore, sample_snapshot: dict) -> None:
        """Only one snapshot returns empty trends (need at least 2)."""
        store.store_snapshot(sample_snapshot)
        assert compute_trends(store, "engineering") == []

    def test_trend_with_no_data(self, store: KPIHistoryStore) -> None:
        """No data returns empty list."""
        assert compute_trends(store, "engineering") == []

    def test_trend_filter_by_kpi_keys(self, store: KPIHistoryStore, older_snapshot: dict,
                                       sample_snapshot: dict) -> None:
        """Specific kpi_keys filter works."""
        store.store_snapshot(older_snapshot)
        store.store_snapshot(sample_snapshot)
        trends = compute_trends(store, "engineering", kpi_keys=["failure_rate"])
        assert len(trends) == 1
        assert trends[0].kpi_key == "failure_rate"

    def test_trend_flat_values(self, store: KPIHistoryStore) -> None:
        """Identical values produce a 'flat' direction."""
        snap1 = {
            "collected_at": "2026-07-19T10:00:00",
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": "2026-07-19T10:00:00",
                    "kpis": {
                        "uptime": {"current": 99.9, "target": 99.5, "unit": "%", "status": "on_track"},
                    },
                },
            },
        }
        snap2 = {
            "collected_at": "2026-07-19T11:00:00",
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": "2026-07-19T11:00:00",
                    "kpis": {
                        "uptime": {"current": 99.9, "target": 99.5, "unit": "%", "status": "on_track"},
                    },
                },
            },
        }
        store.store_snapshot(snap1)
        store.store_snapshot(snap2)
        trends = compute_trends(store, "engineering")
        assert len(trends) == 1
        assert trends[0].direction == "flat"
        assert trends[0].absolute_change == 0.0

    def test_trend_previous_is_zero(self, store: KPIHistoryStore) -> None:
        """When previous is 0, percentage_change is None."""
        snap1 = {
            "collected_at": "2026-07-19T10:00:00",
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": "2026-07-19T10:00:00",
                    "kpis": {
                        "new_metric": {"current": 0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        }
        snap2 = {
            "collected_at": "2026-07-19T11:00:00",
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": "2026-07-19T11:00:00",
                    "kpis": {
                        "new_metric": {"current": 10, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        }
        store.store_snapshot(snap1)
        store.store_snapshot(snap2)
        trends = compute_trends(store, "engineering")
        assert trends[0].percentage_change is None


# ===========================================================================
# Alert Rules Engine
# ===========================================================================


class TestAlertEngine:
    """Tests for AlertEngine — rule management and evaluation."""

    def test_add_rule(self) -> None:
        """Rules can be added and listed."""
        engine = AlertEngine()
        rule = AlertRule(name="test_rule", department="engineering", kpi_key="failure_rate",
                         operator="gt", threshold=5.0)
        engine.add_rule(rule)
        assert len(engine.list_rules()) == 1
        assert engine.list_rules()[0].name == "test_rule"

    def test_add_rules(self) -> None:
        """Multiple rules can be added at once."""
        engine = AlertEngine()
        rules = [
            AlertRule(name="r1", department="*", kpi_key="failure_rate", operator="gt", threshold=5.0),
            AlertRule(name="r2", department="engineering", kpi_key="completion_rate", operator="lt", threshold=90.0),
        ]
        engine.add_rules(rules)
        assert len(engine.list_rules()) == 2

    def test_remove_rule(self) -> None:
        """Rules can be removed by name."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(name="test_rule", department="*", kpi_key="x", operator="gt", threshold=1))
        assert engine.remove_rule("test_rule") is True
        assert engine.list_rules() == []

    def test_remove_nonexistent_rule(self) -> None:
        """Removing a nonexistent rule returns False."""
        engine = AlertEngine()
        assert engine.remove_rule("no_such_rule") is False

    def test_clear_rules(self) -> None:
        """clear_rules removes all rules."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(name="r1", department="*", kpi_key="x", operator="gt", threshold=1))
        engine.add_rule(AlertRule(name="r2", department="*", kpi_key="y", operator="lt", threshold=10))
        engine.clear_rules()
        assert engine.list_rules() == []

    def test_evaluate_triggers_alert(self) -> None:
        """A rule with a breached threshold fires an alert."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="High failure rate",
            department="engineering",
            kpi_key="failure_rate",
            operator="gt",
            threshold=2.0,
            severity="warning",
        ))

        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {
                        "failure_rate": {"current": 5.0, "unit": "%"},
                    },
                },
            },
        }
        alerts = engine.evaluate(snapshot)
        assert len(alerts) == 1
        assert alerts[0].rule_name == "High failure rate"
        assert alerts[0].current_value == 5.0
        assert alerts[0].threshold == 2.0
        assert alerts[0].severity == "warning"

    def test_evaluate_no_alert_when_below_threshold(self) -> None:
        """When value is within threshold, no alert fires."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="High failure rate",
            department="engineering",
            kpi_key="failure_rate",
            operator="gt",
            threshold=2.0,
        ))

        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {
                        "failure_rate": {"current": 1.0, "unit": "%"},
                    },
                },
            },
        }
        assert engine.evaluate(snapshot) == []

    def test_evaluate_wildcard_department(self) -> None:
        """A rule with department='*' applies to all departments."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Any failures",
            department="*",
            kpi_key="failure_rate",
            operator="gt",
            threshold=0,
        ))

        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {"failure_rate": {"current": 2.0, "unit": "%"}},
                },
                "hr": {
                    "kpis": {"failure_rate": {"current": 0, "unit": "%"}},
                },
            },
        }
        alerts = engine.evaluate(snapshot)
        assert len(alerts) == 1
        assert alerts[0].department == "engineering"

    def test_disabled_rule_does_not_fire(self) -> None:
        """Disabled rules are skipped during evaluation."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Disabled rule",
            department="engineering",
            kpi_key="failure_rate",
            operator="gt",
            threshold=0,
            enabled=False,
        ))
        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {"failure_rate": {"current": 5.0, "unit": "%"}},
                },
            },
        }
        assert engine.evaluate(snapshot) == []

    def test_multiple_rules_multiple_fires(self) -> None:
        """Multiple breached rules all fire alerts."""
        engine = AlertEngine()
        engine.add_rules([
            AlertRule(name="High failure", department="engineering", kpi_key="failure_rate",
                      operator="gt", threshold=1),
            AlertRule(name="Low completion", department="engineering", kpi_key="task_completion_rate",
                      operator="lt", threshold=90),
        ])
        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {
                        "failure_rate": {"current": 5.0, "unit": "%"},
                        "task_completion_rate": {"current": 80.0, "unit": "%"},
                    },
                },
            },
        }
        alerts = engine.evaluate(snapshot)
        assert len(alerts) == 2

    def test_rule_with_lte_operator(self) -> None:
        """The lte operator works correctly."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Low uptime",
            department="engineering",
            kpi_key="uptime",
            operator="lte",
            threshold=99.0,
        ))
        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {"uptime": {"current": 98.5, "unit": "%"}},
                },
            },
        }
        alerts = engine.evaluate(snapshot)
        assert len(alerts) == 1

    def test_rule_with_eq_operator_fires_on_match(self) -> None:
        """The eq operator fires when value equals threshold."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Exactly zero",
            department="engineering",
            kpi_key="failed_tasks",
            operator="eq",
            threshold=0,
        ))
        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {"failed_tasks": {"current": 0, "unit": "count"}},
                },
            },
        }
        alerts = engine.evaluate(snapshot)
        assert len(alerts) == 1

    def test_rule_with_eq_operator_no_fire_on_mismatch(self) -> None:
        """The eq operator does not fire when value differs."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Exactly zero",
            department="engineering",
            kpi_key="failed_tasks",
            operator="eq",
            threshold=0,
        ))
        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {"failed_tasks": {"current": 1, "unit": "count"}},
                },
            },
        }
        alerts = engine.evaluate(snapshot)
        assert len(alerts) == 0

    def test_missing_kpi_no_error(self) -> None:
        """Evaluation handles missing KPIs gracefully."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="NonExistent KPI",
            department="engineering",
            kpi_key="no_such_kpi",
            operator="gt",
            threshold=0,
        ))
        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {"existing_kpi": {"current": 1, "unit": "count"}},
                },
            },
        }
        assert engine.evaluate(snapshot) == []

    def test_save_and_load_rules(self, temp_storage_dir: Path) -> None:
        """Rules can be persisted to file and loaded back."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Persisted rule",
            department="*",
            kpi_key="failure_rate",
            operator="gt",
            threshold=5.0,
            severity="critical",
        ))

        rules_file = temp_storage_dir / "alert_rules.json"
        engine.save_rules_to_file(rules_file)
        assert rules_file.exists()

        # Load into a fresh engine
        engine2 = AlertEngine()
        count = engine2.load_rules_from_file(rules_file)
        assert count == 1
        assert engine2.list_rules()[0].name == "Persisted rule"
        assert engine2.list_rules()[0].threshold == 5.0

    def test_load_rules_nonexistent_file(self) -> None:
        """Loading from a nonexistent file returns 0."""
        engine = AlertEngine()
        count = engine.load_rules_from_file(Path("/nonexistent/rules.json"))
        assert count == 0

    def test_alert_message_format(self) -> None:
        """Alert includes a well-formatted message string."""
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Test",
            department="engineering",
            kpi_key="failure_rate",
            operator="gt",
            threshold=2.0,
            severity="critical",
        ))
        snapshot = {
            "departments": {
                "engineering": {
                    "kpis": {"failure_rate": {"current": 5.0, "unit": "%"}},
                },
            },
        }
        alerts = engine.evaluate(snapshot)
        assert "CRITICAL" in alerts[0].message
        assert "Test" in alerts[0].message
        assert "5.0" in alerts[0].message


# ===========================================================================
# Summary Statistics
# ===========================================================================


class TestSummaryStatistics:
    """Tests for compute_summary — daily/weekly/monthly rollups."""

    def test_daily_summary(self, store: KPIHistoryStore) -> None:
        """Daily summary computes min/max/mean/count correctly."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%dT")
        for hour, val in [(8, 88.0), (9, 92.0), (10, 95.0), (11, 91.0)]:
            store.store_snapshot({
                "collected_at": f"{today}{hour:02d}:00:00",
                "departments": {
                    "engineering": {
                        "department": "engineering",
                        "collected_at": f"{today}{hour:02d}:00:00",
                        "kpis": {
                            "completion": {"current": val, "target": 95, "unit": "%", "status": "info"},
                        },
                    },
                },
            })

        summaries = compute_summary(store, "engineering", period="daily")
        assert len(summaries) == 1
        s = summaries[0]
        assert s.kpi_key == "completion"
        assert s.min_value == 88.0
        assert s.max_value == 95.0
        assert s.mean_value == pytest.approx(91.5, abs=0.01)
        assert s.count == 4
        assert s.unit == "%"

    def test_summary_empty_store(self, store: KPIHistoryStore) -> None:
        """Empty store returns empty list."""
        assert compute_summary(store, "engineering") == []

    def test_summary_no_entries_in_period(self, store: KPIHistoryStore) -> None:
        """No entries in the current period returns empty list."""
        yesterday = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        store.store_snapshot({
            "collected_at": yesterday,
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": yesterday,
                    "kpis": {
                        "completion": {"current": 90.0, "target": 95, "unit": "%", "status": "info"},
                    },
                },
            },
        })
        assert compute_summary(store, "engineering") == []

    def test_summary_filter_kpi_keys(self, store: KPIHistoryStore) -> None:
        """Filtering by kpi_keys returns only those KPIs."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%dT")
        store.store_snapshot({
            "collected_at": f"{today}12:00:00",
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": f"{today}12:00:00",
                    "kpis": {
                        "a": {"current": 10.0, "target": None, "unit": "count", "status": "info"},
                        "b": {"current": 20.0, "target": None, "unit": "count", "status": "info"},
                        "c": {"current": 30.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })
        summaries = compute_summary(store, "engineering", kpi_keys=["a", "c"])
        assert len(summaries) == 2
        assert {s.kpi_key for s in summaries} == {"a", "c"}

    def test_invalid_period_raises(self, store: KPIHistoryStore) -> None:
        """An unknown period string raises ValueError."""
        # Need at least one entry so the function reaches period logic
        store.store_snapshot({
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "kpis": {
                        "dummy": {"current": 1.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })
        with pytest.raises(ValueError, match="Unknown period"):
            compute_summary(store, "engineering", period="yearly")  # type: ignore[arg-type]


# ===========================================================================
# Retention Policy & Cleanup
# ===========================================================================


class TestRetentionPolicy:
    """Tests for RetentionPolicy validation."""

    def test_default_policy(self) -> None:
        """Default policy has 90 days with archiving enabled."""
        policy = RetentionPolicy()
        assert policy.max_days == 90
        assert policy.archive_enabled is True
        assert policy.archive_dir is not None

    def test_custom_policy(self) -> None:
        """Custom values are set correctly."""
        policy = RetentionPolicy(max_days=30, archive_enabled=False, archive_dir=Path("/tmp/archive"))
        assert policy.max_days == 30
        assert policy.archive_enabled is False
        assert policy.archive_dir == Path("/tmp/archive")

    def test_invalid_max_days(self) -> None:
        """max_days must be >= 1."""
        with pytest.raises(ValueError, match="max_days must be >= 1"):
            RetentionPolicy(max_days=0)


class TestRetentionEngine:
    """Tests for RetentionEngine — cleanup and archive."""

    def test_cleanup_removes_expired_entries(self, store: KPIHistoryStore) -> None:
        """Entries older than max_days are removed during cleanup."""
        # Store an entry timestamped before the retention window
        old_ts = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat()
        store.store_snapshot({
            "collected_at": old_ts,
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": old_ts,
                    "kpis": {
                        "old_metric": {"current": 1.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })

        # Store a recent entry
        recent_ts = datetime.now(timezone.utc).isoformat()
        store.store_snapshot({
            "collected_at": recent_ts,
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": recent_ts,
                    "kpis": {
                        "recent_metric": {"current": 10.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })

        # Also store entries for a second department to ensure it's not affected
        store.store_snapshot({
            "collected_at": old_ts,
            "departments": {
                "hr": {
                    "department": "hr",
                    "collected_at": old_ts,
                    "kpis": {
                        "headcount": {"current": 100, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })

        policy = RetentionPolicy(max_days=30, archive_enabled=False)
        engine = RetentionEngine(store, policy)
        archived, deleted = engine.cleanup()

        assert archived == 0  # archiving is disabled
        assert deleted == 2  # old engineering entry + hr entry (both expired)

        # Verify only the recent entry remains
        remaining = store.get_history("engineering")
        assert len(remaining) == 1
        assert remaining[0].kpi_key == "recent_metric"

        # HR had only old entries, should be empty
        assert store.get_history("hr") == []

    def test_cleanup_no_expired_entries(self, store: KPIHistoryStore) -> None:
        """No removal happens when all entries are within the retention window."""
        store.store_snapshot({
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "kpis": {
                        "completion": {"current": 90.0, "target": 95, "unit": "%", "status": "info"},
                    },
                },
            },
        })

        policy = RetentionPolicy(max_days=90, archive_enabled=False)
        engine = RetentionEngine(store, policy)
        archived, deleted = engine.cleanup()
        assert archived == 0
        assert deleted == 0
        assert store.count_entries("engineering") == 1

    def test_archive_creates_compressed_file(self, store: KPIHistoryStore, temp_storage_dir: Path) -> None:
        """Archiving writes a gzip-compressed JSON file."""
        store.store_snapshot({
            "collected_at": (datetime.now(timezone.utc) - timedelta(days=100)).isoformat(),
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": (datetime.now(timezone.utc) - timedelta(days=100)).isoformat(),
                    "kpis": {
                        "old_metric": {"current": 42.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })

        archive_dir = temp_storage_dir / "archive"
        policy = RetentionPolicy(max_days=30, archive_enabled=True, archive_dir=archive_dir)
        engine = RetentionEngine(store, policy)
        archived, deleted = engine.cleanup()

        assert archived == 1

        # Verify the archive file exists
        archives = list(archive_dir.glob("engineering_archive_*.json.gz"))
        assert len(archives) == 1

        # Read back to verify content
        with gzip.open(archives[0], "rt", encoding="utf-8") as fh:
            records = json.load(fh)
        assert len(records) == 1
        assert records[0]["kpi_key"] == "old_metric"
        assert records[0]["current"] == 42.0

    def test_archive_department(self, store: KPIHistoryStore, temp_storage_dir: Path) -> None:
        """archive_department archives and removes all entries for a department."""
        store.store_snapshot({
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "kpis": {
                        "m1": {"current": 1.0, "target": None, "unit": "count", "status": "info"},
                        "m2": {"current": 2.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })

        archive_dir = temp_storage_dir / "archive"
        policy = RetentionPolicy(archive_dir=archive_dir)
        engine = RetentionEngine(store, policy)

        archived = engine.archive_department("engineering")
        assert archived == 2
        assert store.get_history("engineering") == []

    def test_stats(self, store: KPIHistoryStore) -> None:
        """stats returns correct counts and policy info."""
        store.store_snapshot({
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "kpis": {
                        "m1": {"current": 1.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })

        old_ts = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat()
        store.store_snapshot({
            "collected_at": old_ts,
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": old_ts,
                    "kpis": {
                        "old_m1": {"current": 99.0, "target": None, "unit": "count", "status": "info"},
                    },
                },
            },
        })

        engine = RetentionEngine(store, RetentionPolicy(max_days=30, archive_enabled=False))
        stats = engine.stats()

        assert stats["policy"]["max_days"] == 30
        assert "engineering" in stats["departments"]
        assert stats["departments"]["engineering"]["entries"] == 2
        assert stats["departments"]["engineering"]["expired"] == 1
        assert stats["total_entries"] == 2
        assert stats["expired_entries"] == 1

    def test_update_policy(self, store: KPIHistoryStore) -> None:
        """update_policy replaces the current policy."""
        engine = RetentionEngine(store, RetentionPolicy(max_days=90))
        assert engine.policy.max_days == 90

        engine.update_policy(RetentionPolicy(max_days=7))
        assert engine.policy.max_days == 7


# ===========================================================================
# Integration tests
# ===========================================================================


class TestIntegration:
    """End-to-end integration tests combining analytics and retention."""

    def test_full_pipeline(self, store: KPIHistoryStore) -> None:
        """Store → trend → alert → cleanup pipeline works end-to-end."""
        # 1. Store two snapshots
        older = {
            "collected_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
                    "kpis": {
                        "completion": {"current": 80.0, "target": 95, "unit": "%", "status": "below_target"},
                    },
                },
            },
        }
        newer = {
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "departments": {
                "engineering": {
                    "department": "engineering",
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "kpis": {
                        "completion": {"current": 85.0, "target": 95, "unit": "%", "status": "below_target"},
                    },
                },
            },
        }
        store.store_snapshot(older)
        store.store_snapshot(newer)

        # 2. Compute trend
        trends = compute_trends(store, "engineering")
        assert len(trends) == 1
        assert trends[0].direction == "up"

        # 3. Evaluate alerts
        engine = AlertEngine()
        engine.add_rule(AlertRule(
            name="Completion below target",
            department="engineering",
            kpi_key="completion",
            operator="lt",
            threshold=90.0,
            severity="warning",
        ))
        alerts = engine.evaluate(newer)
        assert len(alerts) == 1
        assert alerts[0].kpi_key == "completion"

        # 4. Daily summary
        summaries = compute_summary(store, "engineering", period="daily")
        assert len(summaries) == 1
        assert summaries[0].mean_value == 82.5

        # 5. Retention cleanup (no expired entries with default policy)
        policy = RetentionPolicy(max_days=90, archive_enabled=False)
        retention_engine = RetentionEngine(store, policy)
        archived, deleted = retention_engine.cleanup()
        assert archived == 0
        assert deleted == 0

        # 6. Verify data survives cleanup
        assert store.count_entries("engineering") == 2
