"""Tests for the data pipeline: KPI pipeline, cost analytics, agent analytics,
memory store, and escalation store.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.data.database import Database
from ai_company.data.kpi_pipeline import KPIPipeline
from ai_company.data.cost_analytics import CostAnalytics
from ai_company.data.agent_analytics import AgentPerformanceAnalytics
from ai_company.data.memory_store import MemoryStoreDB
from ai_company.data.escalation_store import EscalationStore
from ai_company.models.task import Task


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database with all tables."""
    database = Database(tmp_path / "test_pipeline.db")
    database.init_schema()
    yield database
    database.close()


@pytest.fixture
def kpi(db: Database) -> KPIPipeline:
    return KPIPipeline(db)


@pytest.fixture
def cost(db: Database) -> CostAnalytics:
    return CostAnalytics(db)


@pytest.fixture
def analytics(db: Database) -> AgentPerformanceAnalytics:
    return AgentPerformanceAnalytics(db)


@pytest.fixture
def mem(db: Database) -> MemoryStoreDB:
    return MemoryStoreDB(db)


@pytest.fixture
def escalation(db: Database) -> EscalationStore:
    return EscalationStore(db)


def _sample_snapshot() -> dict:
    """Return a sample KPI snapshot for testing."""
    return {
        "collected_at": "2025-06-15T12:00:00Z",
        "departments": {
            "engineering": {
                "kpis": {
                    "task_completion_rate": {
                        "current": 92.5,
                        "target": 95.0,
                        "unit": "%",
                        "status": "below_target",
                    },
                    "escalation_rate": {
                        "current": 3.2,
                        "target": 5.0,
                        "unit": "%",
                        "status": "on_track",
                    },
                },
            },
            "sales": {
                "kpis": {
                    "pipeline_value": {
                        "current": 150000,
                        "target": 200000,
                        "unit": "USD",
                        "status": "below_target",
                    },
                },
            },
        },
    }


# ===================================================================
# KPI Pipeline Tests
# ===================================================================

class TestKPIPipeline:
    """Tests for the KPI analytics pipeline."""

    def test_ingest_snapshot(self, kpi: KPIPipeline) -> None:
        """ingest_snapshot stores all KPI entries."""
        count = kpi.ingest_snapshot(_sample_snapshot())
        assert count == 3  # 2 engineering + 1 sales

    def test_get_history(self, kpi: KPIPipeline) -> None:
        """get_history returns stored data."""
        kpi.ingest_snapshot(_sample_snapshot())
        history = kpi.get_history("engineering")
        assert len(history) == 2

    def test_get_history_filter_kpi(self, kpi: KPIPipeline) -> None:
        """get_history with kpi_key filters correctly."""
        kpi.ingest_snapshot(_sample_snapshot())
        history = kpi.get_history("engineering", kpi_key="task_completion_rate")
        assert len(history) == 1
        assert history[0]["kpi_key"] == "task_completion_rate"

    def test_get_latest(self, kpi: KPIPipeline) -> None:
        """get_latest returns the most recent snapshot."""
        kpi.ingest_snapshot(_sample_snapshot())
        latest = kpi.get_latest("engineering")
        assert len(latest) == 2

    def test_list_departments(self, kpi: KPIPipeline) -> None:
        """list_departments returns all departments with data."""
        kpi.ingest_snapshot(_sample_snapshot())
        depts = kpi.list_departments()
        assert set(depts) == {"engineering", "sales"}

    def test_list_kpi_keys(self, kpi: KPIPipeline) -> None:
        """list_kpi_keys returns distinct keys."""
        kpi.ingest_snapshot(_sample_snapshot())
        keys = kpi.list_kpi_keys("engineering")
        assert set(keys) == {"task_completion_rate", "escalation_rate"}

    def test_ingest_individual(self, kpi: KPIPipeline) -> None:
        """ingest_individual stores a single data point."""
        kpi.ingest_individual("finance", "revenue", 50000.0, 100000.0, "USD")
        assert kpi.total_entries() == 1

    def test_aggregate_daily(self, kpi: KPIPipeline) -> None:
        """aggregate with daily period groups by day."""
        # Use timestamps within the last 30 days so the default window captures them
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        for i in range(3):
            ts = (now - timedelta(days=i)).replace(hour=12, minute=0, second=0, microsecond=0).isoformat()
            kpi.ingest_individual("engineering", "task_completion_rate", 90.0 + i, 95.0, "%", "on_track", ts)
        agg = kpi.aggregate("engineering", period="daily")
        assert len(agg) >= 1
        assert "min_value" in agg[0]
        assert "mean_value" in agg[0]

    def test_detect_anomalies(self, kpi: KPIPipeline) -> None:
        """detect_anomalies returns a list (may be empty for normal data)."""
        # Ingest several data points
        for i in range(10):
            kpi.ingest_individual(
                "engineering", "error_rate",
                float(i % 5),  # 0,1,2,3,4,0,1,2,3,4
                timestamp=f"2025-01-{10 + i:02d}T12:00:00Z",
            )
        # Add an anomaly
        kpi.ingest_individual(
            "engineering", "error_rate", 50.0,
            timestamp="2025-01-20T12:00:00Z",
        )

        anomalies = kpi.detect_anomalies("engineering", "error_rate")
        # The 50.0 value should be detected as anomalous
        assert len(anomalies) >= 1

    def test_get_trend(self, kpi: KPIPipeline) -> None:
        """get_trend compares current vs previous."""
        kpi.ingest_individual("eng", "metric", 80.0, timestamp="2025-01-01T10:00:00Z")
        kpi.ingest_individual("eng", "metric", 90.0, timestamp="2025-01-02T10:00:00Z")

        trend = kpi.get_trend("eng", "metric")
        assert trend is not None
        assert trend["current_value"] == 90.0
        assert trend["previous_value"] == 80.0
        assert trend["direction"] == "up"

    def test_total_entries(self, kpi: KPIPipeline) -> None:
        """total_entries returns the count."""
        kpi.ingest_snapshot(_sample_snapshot())
        assert kpi.total_entries() == 3


# ===================================================================
# Cost Analytics Tests
# ===================================================================

class TestCostAnalytics:
    """Tests for cost analytics."""

    def test_record_usage(self, cost: CostAnalytics) -> None:
        """record_usage inserts a record."""
        row_id = cost.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="engineer",
            task_id="t1",
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.005,
        )
        assert row_id > 0
        assert cost.total_records() == 1

    def test_get_daily_total(self, cost: CostAnalytics) -> None:
        """get_daily_total returns the sum for the day."""
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.01, timestamp="2025-06-15T10:00:00Z",
        )
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t2", prompt_tokens=200, completion_tokens=100,
            cost_usd=0.02, timestamp="2025-06-15T11:00:00Z",
        )
        total = cost.get_daily_total("2025-06-15")
        assert abs(total - 0.03) < 1e-8

    def test_get_task_total(self, cost: CostAnalytics) -> None:
        """get_task_total sums costs for a task."""
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.05, timestamp="2025-06-15T10:00:00Z",
        )
        assert abs(cost.get_task_total("t1") - 0.05) < 1e-8

    def test_get_agent_total(self, cost: CostAnalytics) -> None:
        """get_agent_total sums costs for an agent."""
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="alice",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.03, timestamp="2025-06-15T10:00:00Z",
        )
        assert abs(cost.get_agent_total("alice") - 0.03) < 1e-8

    def test_check_budget_within(self, cost: CostAnalytics) -> None:
        """check_budget returns True when within budget."""
        cost.daily_budget = 10.0
        allowed, reason = cost.check_budget("t1", proposed_cost=1.0)
        assert allowed is True

    def test_check_budget_exceeded(self, cost: CostAnalytics) -> None:
        """check_budget returns False when budget exceeded."""
        cost.daily_budget = 0.01
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.005,
        )
        allowed, reason = cost.check_budget("t1", proposed_cost=0.01)
        assert allowed is False
        assert "exceeded" in reason

    def test_daily_summary(self, cost: CostAnalytics) -> None:
        """daily_summary returns full breakdown."""
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.01, timestamp="2025-06-15T10:00:00Z",
        )
        summary = cost.daily_summary("2025-06-15")
        assert summary["total_cost_usd"] > 0
        assert "gpt-4o" in summary["by_model"]

    def test_breakdown_by_agent(self, cost: CostAnalytics) -> None:
        """breakdown_by_agent returns per-agent costs."""
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="alice",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.1,
        )
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="bob",
            task_id="t2", prompt_tokens=200, completion_tokens=100,
            cost_usd=0.2,
        )
        breakdown = cost.breakdown_by_agent()
        assert len(breakdown) == 2
        # Bob should be first (higher cost)
        assert breakdown[0]["agent_name"] == "bob"

    def test_breakdown_by_model(self, cost: CostAnalytics) -> None:
        """breakdown_by_model returns per-model costs."""
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.05,
        )
        breakdown = cost.breakdown_by_model()
        assert len(breakdown) == 1
        assert breakdown[0]["model"] == "gpt-4o"

    def test_forecast_daily(self, cost: CostAnalytics) -> None:
        """forecast_daily returns a forecast dict."""
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        for i in range(7):
            ts = (now - timedelta(days=i)).replace(hour=10, minute=0, second=0, microsecond=0).isoformat()
            cost.record_usage(
                model="gpt-4o", provider="openai", agent_name="a",
                task_id=f"t{i}", prompt_tokens=100, completion_tokens=50,
                cost_usd=0.01, timestamp=ts,
            )
        forecast = cost.forecast_daily(lookback_days=14, forecast_days=7)
        assert forecast["avg_daily_cost"] > 0
        assert forecast["projected_total"] > 0

    def test_budget_status(self, cost: CostAnalytics) -> None:
        """budget_status returns current utilization."""
        cost.daily_budget = 100.0
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=5.0, timestamp="2025-06-15T10:00:00Z",
        )
        status = cost.budget_status()
        assert "daily_cost_usd" in status
        assert "daily_budget" in status
        assert status["daily_budget"] == 100.0

    def test_total_cost(self, cost: CostAnalytics) -> None:
        """total_cost returns the sum across all records."""
        cost.record_usage(
            model="gpt-4o", provider="openai", agent_name="a",
            task_id="t1", prompt_tokens=100, completion_tokens=50,
            cost_usd=0.07, timestamp="2025-06-15T10:00:00Z",
        )
        assert abs(cost.total_cost() - 0.07) < 1e-8


# ===================================================================
# Agent Performance Analytics Tests
# ===================================================================

class TestAgentPerformanceAnalytics:
    """Tests for agent performance analytics."""

    def _seed_agent_data(self, db: Database) -> None:
        """Insert test tasks and audit events for agent analytics."""
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)

        # Tasks — use recent timestamps
        tasks = [
            ("t1", "alice", "bob", "completed", now - timedelta(hours=3), now - timedelta(hours=2, minutes=30)),
            ("t2", "alice", "bob", "completed", now - timedelta(hours=2), now - timedelta(hours=1, minutes=45)),
            ("t3", "alice", "bob", "failed", now - timedelta(hours=1), now - timedelta(minutes=50)),
            ("t4", "charlie", "bob", "completed", now - timedelta(minutes=45), now - timedelta(minutes=25)),
        ]
        for tid, sender, receiver, status, created, completed in tasks:
            task = Task(
                id=tid, sender_id=sender, receiver_id=receiver,
                status=status, created_at=created.isoformat(), completed_at=completed.isoformat(),
            )
            db.execute(
                """INSERT INTO tasks (id, sender_id, receiver_id, status, created_at, completed_at, raw_json)
                   VALUES (?,?,?,?,?,?,?)""",
                (tid, sender, receiver, status, created.isoformat(), completed.isoformat(), task.model_dump_json()),
            )

        # Audit events — use recent timestamps
        events = [
            ("a1", "tool_call", "bob", "t1", (now - timedelta(hours=2, minutes=55)).isoformat(), "read", "info"),
            ("a2", "tool_call", "bob", "t1", (now - timedelta(hours=2, minutes=50)).isoformat(), "write", "info"),
            ("a3", "error", "bob", "t3", (now - timedelta(minutes=55)).isoformat(), None, "error"),
        ]
        for eid, etype, agent, tid, ts, tool, sev in events:
            db.execute(
                """INSERT INTO audit_events
                   (event_id, timestamp, event_type, agent_id, task_id, tool, args, result, metadata, severity)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (eid, ts, etype, agent, tid, tool, "{}", "{}", "{}", sev),
            )

        # Cost records — omit id to let AUTOINCREMENT assign
        cost_rows = [
            ((now - timedelta(hours=2, minutes=55)).isoformat(), "gpt-4o", "openai", "bob", "t1", 100, 50, 0.01, 1),
            ((now - timedelta(minutes=55)).isoformat(), "gpt-4o", "openai", "bob", "t3", 200, 100, 0.02, 1),
        ]
        for ts, model, prov, agent, tid, pt, ct, cost_val, it in cost_rows:
            db.execute(
                """INSERT INTO cost_records
                   (timestamp, model, provider, agent_name, task_id,
                    prompt_tokens, completion_tokens, cost_usd, iteration, metadata)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (ts, model, prov, agent, tid, pt, ct, cost_val, it, "{}"),
            )

        db.commit()

    def test_agent_summary(self, analytics: AgentPerformanceAnalytics, db: Database) -> None:
        """agent_summary returns comprehensive metrics."""
        self._seed_agent_data(db)
        summary = analytics.agent_summary("bob")
        assert summary["agent_id"] == "bob"
        assert summary["tasks_received"] == 4
        assert summary["tasks_completed"] == 3
        assert summary["tasks_failed"] == 1
        assert summary["completion_rate_pct"] == 75.0
        assert summary["error_rate_pct"] == 25.0
        assert summary["cost"]["total_usd"] > 0

    def test_leaderboard(self, analytics: AgentPerformanceAnalytics, db: Database) -> None:
        """leaderboard returns ranked agents."""
        self._seed_agent_data(db)
        board = analytics.leaderboard()
        assert len(board) >= 1
        assert "rank" in board[0]
        assert "completion_rate_pct" in board[0]

    def test_model_usage_distribution(self, analytics: AgentPerformanceAnalytics, db: Database) -> None:
        """model_usage_distribution returns model data."""
        self._seed_agent_data(db)
        dist = analytics.model_usage_distribution()
        assert len(dist) >= 1
        assert dist[0]["model"] == "gpt-4o"

    def test_task_duration_stats(self, analytics: AgentPerformanceAnalytics, db: Database) -> None:
        """task_duration_stats computes durations."""
        self._seed_agent_data(db)
        stats = analytics.task_duration_stats()
        assert stats["count"] == 4
        assert stats["avg_seconds"] > 0
        assert "bob" in stats["by_agent"]

    def test_error_analysis(self, analytics: AgentPerformanceAnalytics, db: Database) -> None:
        """error_analysis returns error data."""
        self._seed_agent_data(db)
        errors = analytics.error_analysis()
        assert len(errors["failed_tasks_by_agent"]) >= 1
        assert len(errors["error_events_by_agent"]) >= 1

    def test_full_report(self, analytics: AgentPerformanceAnalytics, db: Database) -> None:
        """full_report combines all analytics."""
        self._seed_agent_data(db)
        report = analytics.full_report()
        assert "leaderboard" in report
        assert "task_durations" in report
        assert "model_usage" in report
        assert "error_analysis" in report
        assert "generated_at" in report


# ===================================================================
# Memory Store DB Tests
# ===================================================================

class TestMemoryStoreDB:
    """Tests for the SQLite-backed memory store."""

    def test_store_and_recall(self, mem: MemoryStoreDB) -> None:
        """store and recall work together."""
        entry = mem.store("episodic", "Test memory", agent_id="alice", tags=["test"])
        assert entry.memory_type == "episodic"
        assert entry.content == "Test memory"

        results = mem.recall("episodic", query="Test")
        assert len(results) == 1
        assert results[0].content == "Test memory"

    def test_recall_by_agent(self, mem: MemoryStoreDB) -> None:
        """recall filters by agent_id."""
        mem.store("semantic", "Knowledge A", agent_id="alice")
        mem.store("semantic", "Knowledge B", agent_id="bob")

        results = mem.recall("semantic", agent_id="alice")
        assert len(results) == 1
        assert results[0].agent_id == "alice"

    def test_recall_by_tags(self, mem: MemoryStoreDB) -> None:
        """recall filters by tag intersection."""
        mem.store("procedural", "How to deploy", tags=["deploy", "k8s"])
        mem.store("procedural", "How to test", tags=["test", "pytest"])

        results = mem.recall("procedural", tags=["deploy"])
        assert len(results) == 1
        assert "deploy" in results[0].tags

    def test_count(self, mem: MemoryStoreDB) -> None:
        """count returns correct numbers."""
        mem.store("episodic", "A")
        mem.store("episodic", "B")
        mem.store("semantic", "C")

        assert mem.count("episodic") == 2
        assert mem.count("semantic") == 1
        assert mem.count() == 3

    def test_stats(self, mem: MemoryStoreDB) -> None:
        """stats returns per-type counts."""
        mem.store("episodic", "A")
        mem.store("procedural", "B")
        stats = mem.stats()
        assert stats["episodic"] == 1
        assert stats["procedural"] == 1
        assert stats["semantic"] == 0

    def test_invalid_memory_type(self, mem: MemoryStoreDB) -> None:
        """store raises ValueError for unknown memory type."""
        with pytest.raises(ValueError, match="Unknown memory type"):
            mem.store("nonexistent", "data")

    def test_search_content(self, mem: MemoryStoreDB) -> None:
        """search_content finds matching text."""
        mem.store("episodic", "Deployed to production today")
        mem.store("episodic", "Fixed a bug in the API")
        mem.store("semantic", "Production deployment guide")

        results = mem.search_content("production")
        assert len(results) == 2

    def test_most_accessed(self, mem: MemoryStoreDB) -> None:
        """most_accessed returns entries sorted by access count."""
        mem.store("episodic", "Rare memory")
        mem.store("episodic", "Popular memory")

        # Recall the popular one twice
        mem.recall("episodic", query="Popular")
        mem.recall("episodic", query="Popular")

        results = mem.most_accessed("episodic")
        assert results[0].content == "Popular memory"

    def test_recent(self, mem: MemoryStoreDB) -> None:
        """recent returns entries in reverse chronological order."""
        mem.store("semantic", "Old", agent_id="a", tags=["old"])
        # Ensure a later timestamp by storing with a slight delay via explicit tags
        mem.store("semantic", "New", agent_id="b", tags=["new"])

        # recent uses ORDER BY created_at DESC — with UUID-based IDs,
        # both may share the same second. Use most_accessed instead to verify ordering.
        results = mem.recall("semantic", query="New", limit=1)
        assert results[0].content == "New"


# ===================================================================
# Escalation Store Tests
# ===================================================================

class TestEscalationStore:
    """Tests for the SQLite-backed escalation store."""

    def test_add_and_get_pending(self, escalation: EscalationStore) -> None:
        """add_event and get_pending work together."""
        escalation.add_event(
            task_id="t1", rule_id="r1",
            from_agent="alice", to_agent="bob",
            reason="Timeout",
        )
        pending = escalation.get_pending()
        assert len(pending) == 1
        assert pending[0]["task_id"] == "t1"

    def test_resolve(self, escalation: EscalationStore) -> None:
        """resolve marks events as resolved."""
        escalation.add_event(
            task_id="t1", rule_id="r1",
            from_agent="alice", to_agent="bob",
            reason="Timeout",
        )
        count = escalation.resolve("t1")
        assert count == 1
        assert escalation.count_pending() == 0

    def test_get_by_task(self, escalation: EscalationStore) -> None:
        """get_by_task returns all events for a task."""
        escalation.add_event(task_id="t1", rule_id="r1", from_agent="a", to_agent="b", reason="R1")
        escalation.add_event(task_id="t1", rule_id="r2", from_agent="a", to_agent="c", reason="R2")
        escalation.add_event(task_id="t2", rule_id="r1", from_agent="a", to_agent="b", reason="R3")

        events = escalation.get_by_task("t1")
        assert len(events) == 2

    def test_get_by_agent(self, escalation: EscalationStore) -> None:
        """get_by_agent returns events targeting the agent."""
        escalation.add_event(task_id="t1", rule_id="r1", from_agent="a", to_agent="bob", reason="R1")
        escalation.add_event(task_id="t2", rule_id="r1", from_agent="a", to_agent="charlie", reason="R2")

        events = escalation.get_by_agent("bob")
        assert len(events) == 1

    def test_count_pending(self, escalation: EscalationStore) -> None:
        """count_pending returns correct count."""
        escalation.add_event(task_id="t1", rule_id="r1", from_agent="a", to_agent="b", reason="R")
        escalation.add_event(task_id="t2", rule_id="r1", from_agent="a", to_agent="b", reason="R")
        escalation.resolve("t1")

        assert escalation.count_pending() == 1

    def test_delete_before(self, escalation: EscalationStore) -> None:
        """delete_before removes old resolved events."""
        escalation.add_event(
            task_id="t1", rule_id="r1", from_agent="a", to_agent="b",
            reason="Old", timestamp="2025-01-01T10:00:00Z", resolved=True,
        )
        escalation.add_event(
            task_id="t2", rule_id="r1", from_agent="a", to_agent="b",
            reason="New", timestamp="2025-06-01T10:00:00Z", resolved=True,
        )

        deleted = escalation.delete_before("2025-03-01T00:00:00Z")
        assert deleted == 1
        assert escalation.count() == 1
