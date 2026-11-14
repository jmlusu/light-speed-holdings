"""Token governance + renormalized cache metrics (GO-1/GO-2)."""

from __future__ import annotations

import pytest

from ai_company.data.cost_analytics import CostAnalytics
from ai_company.data.database import Database
from ai_company.llm.cache_metrics import (
    compute_cache_metrics,
    extract_cache_write,
    normalize_provider_usage,
)
from ai_company.llm.cost_tracker import CostTracker
from ai_company.llm.opencode_usage import normalize_message_row, normalize_session_row


@pytest.fixture()
def analytics(tmp_path):
    db = Database(tmp_path / "ai.db")
    db.init_schema()
    return CostAnalytics(db)


def _record(analytics, **kw):
    base = {
        "model": "crouton-alpha-free",
        "provider": "opencode",
        "agent_name": "build",
        "task_id": "ses_1",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cost_usd": 0.0,
        "session_id": "ses_1",
    }
    base.update(kw)
    return analytics.record_usage(**base)


class TestCacheWriteMapping:
    """cache_creation -> tokens_cache_write (reliability P1-1)."""

    def test_synthetic_usage_cache_creation_50(self):
        usage = {"input": 100, "cache_read": 900, "cache_creation": 50}
        # Flat OpenCode-style keys go through normalize_provider_usage.
        assert normalize_provider_usage(usage)["cache_write"] == 50

    def test_anthropic_cache_creation_input_tokens(self):
        assert extract_cache_write({"cache_creation_input_tokens": 123}) == 123

    def test_nested_ephemeral_dict_sums(self):
        usage = {
            "cache_creation": {"ephemeral_5m_input_tokens": 10, "ephemeral_1h_input_tokens": 40}
        }
        assert extract_cache_write(usage) == 50

    def test_opencode_nested_write_still_works(self):
        assert extract_cache_write({"tokens": {"cache": {"write": 7, "read": 9}}}) == 7

    def test_session_row_raw_usage_alias(self):
        rec = normalize_session_row(
            session_id="ses_x",
            agent="build",
            model_raw={"id": "claude-x", "providerID": "anthropic"},
            tokens_input=100,
            tokens_output=10,
            tokens_reasoning=0,
            tokens_cache_read=900,
            tokens_cache_write=0,
            raw_cost=0.0,
            time_created=1730000000000,
            raw_usage={"cache_creation": 50, "cache_read": 900},
        )
        assert rec is not None
        assert rec["cache_write"] == 50
        assert rec["prompt_tokens"] == 150  # input + cache_write

    def test_message_row_cache_creation(self):
        rec = normalize_message_row(
            message_id="m1",
            session_id="ses_1",
            session_agent="build",
            data={
                "modelID": "claude-x",
                "providerID": "anthropic",
                "agent": "build",
                "tokens": {
                    "input": 100,
                    "output": 10,
                    "reasoning": 0,
                    "cache": {"read": 900, "write": 0},
                },
                "cache_creation": 50,
            },
            files_read=0,
            time_created=1730000000000,
        )
        assert rec is not None
        assert rec["cache_write"] == 50
        assert rec["cache_read"] == 900


class TestRenormalizedMetrics:
    def test_cache_read_ratio_and_burn_multiplier(self):
        m = compute_cache_metrics(input_tokens=100, cache_read=900, cache_write=0, output_tokens=10)
        assert m["cache_read_volume"] == 900
        assert m["cache_read_ratio"] == pytest.approx(0.9)
        assert m["burn_multiplier"] == pytest.approx(10.0)
        assert m["cache_write_reported"] is False
        assert m["show_hit_rate_tile"] is False
        assert m["unmetered_banner"] is not None
        assert "writes unmetered" in m["chart_title"]

    def test_hit_rate_tile_shown_when_writes_reported(self):
        m = compute_cache_metrics(input_tokens=100, cache_read=900, cache_write=50)
        assert m["cache_write_reported"] is True
        assert m["show_hit_rate_tile"] is True
        assert m["unmetered_banner"] is None

    def test_zero_input_no_division_by_zero(self):
        m = compute_cache_metrics(input_tokens=0, cache_read=0, cache_write=0)
        assert m["cache_read_ratio"] == 0.0
        assert m["burn_multiplier"] == 0.0

    def test_cost_analytics_cache_metrics(self, analytics):
        _record(analytics, prompt_tokens=100, completion_tokens=10, cache_read=900, cache_write=0)
        m = analytics.cache_metrics()
        assert m["cache_read_volume"] == 900
        assert m["cache_read_ratio"] == pytest.approx(0.9)
        assert m["cache_write_reported"] is False


class TestTokenBudget:
    def test_session_burn_counts_cache_read_at_full_weight(self, analytics):
        _record(analytics, prompt_tokens=100, completion_tokens=10, cache_read=900)
        assert analytics.session_token_total("ses_1") == 1010
        assert analytics.agent_daily_token_total("build") == 1010

    def test_warn_compact_block_thresholds(self, analytics):
        # 70% of 5M = 3.5M warn, 85% = 4.25M compact, 100% = 5M block.
        _record(analytics, prompt_tokens=3_600_000, completion_tokens=0, cache_read=0)
        assert analytics.session_budget_status("ses_1")["level"] == "warn"
        allowed, reason = analytics.check_budget("ses_1")
        assert allowed is True and "warning" in reason.lower()

        _record(analytics, prompt_tokens=700_000, completion_tokens=0, cache_read=0)
        assert analytics.session_budget_status("ses_1")["level"] == "compact"

        _record(analytics, prompt_tokens=800_000, completion_tokens=0, cache_read=0)
        assert analytics.session_budget_status("ses_1")["level"] == "block"
        allowed, reason = analytics.check_budget("ses_1")
        assert allowed is False
        assert "Session token budget exceeded" in reason

    def test_proposed_tokens_block_pre_step(self, analytics):
        allowed, _ = analytics.check_budget("ses_new", proposed_tokens=5_000_001)
        assert allowed is False

    def test_daily_agent_budget_blocks(self, analytics):
        _record(analytics, agent_name="build", prompt_tokens=50_000_001, completion_tokens=0)
        status = analytics.session_budget_status("ses_1", agent_name="build")
        assert status["level"] == "block"
        allowed, reason = analytics.check_budget("ses_1", agent_name="build")
        assert allowed is False

    def test_tighter_gate_wins_token_over_usd(self, analytics):
        # USD budget is None (unlimited) but token cap must still block:
        # free $0 models cannot bypass token governance.
        assert analytics.daily_budget is None
        _record(analytics, prompt_tokens=6_000_000, completion_tokens=0, cost_usd=0.0)
        allowed, reason = analytics.check_budget("ses_1", proposed_cost=0.0)
        assert allowed is False and "token" in reason.lower()

    def test_token_budget_disabled_with_none(self, tmp_path):
        db = Database(tmp_path / "ai.db")
        db.init_schema()
        analytics = CostAnalytics(db, session_token_budget=None, daily_agent_token_budget=None)
        _record(analytics, prompt_tokens=99_000_000, completion_tokens=0)
        allowed, _ = analytics.check_budget("ses_1")
        assert allowed is True

    def test_budget_status_includes_token_utilization(self, analytics):
        _record(analytics, prompt_tokens=1_000_000, completion_tokens=0)
        status = analytics.budget_status(task_id="ses_1")
        assert status["token_budget_utilization"] == pytest.approx(20.0)
        assert status["token_budget_level"] == "ok"

    def test_top_sessions_by_burn(self, analytics):
        _record(analytics, session_id="ses_a", task_id="ses_a", prompt_tokens=10, cache_read=90)
        _record(analytics, session_id="ses_b", task_id="ses_b", prompt_tokens=1000, cache_read=0)
        top = analytics.top_sessions_by_burn()
        assert top[0]["session_id"] == "ses_b"


class TestCostTrackerTokenGate:
    def _tracker(self, tmp_path, **kw):
        return CostTracker(
            results_dir=str(tmp_path / "results"),
            export_path=str(tmp_path / "data" / "orchestrator" / "cost_tracker.json"),
            **kw,
        )

    def test_session_burn_property(self, tmp_path):
        tracker = self._tracker(tmp_path)
        rec = tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="a",
            task_id="t1",
            prompt_tokens=100,
            completion_tokens=10,
            cache_read=900,
            cache_write=50,
        )
        assert rec.session_burn == 1010  # prompt + cache_read + completion

    def test_tracker_blocks_at_session_cap(self, tmp_path):
        tracker = self._tracker(tmp_path, session_token_budget=1000)
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="a",
            task_id="t1",
            prompt_tokens=900,
            completion_tokens=200,
            session_id="s1",
        )
        allowed, reason = tracker.check_budget("t1", session_id="s1", proposed_tokens=1)
        assert allowed is False and "token" in reason.lower()

    def test_tracker_warn_and_compact_levels(self, tmp_path):
        tracker = self._tracker(tmp_path, session_token_budget=1000)
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="a",
            task_id="t1",
            prompt_tokens=750,
            completion_tokens=0,
            session_id="s1",
        )
        assert tracker.session_budget_status("s1")["level"] == "warn"
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="a",
            task_id="t1",
            prompt_tokens=150,
            completion_tokens=0,
            session_id="s1",
        )
        assert tracker.session_budget_status("s1")["level"] == "compact"

    def test_token_accumulators_survive_restart(self, tmp_path):
        tracker = self._tracker(tmp_path)
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="a",
            task_id="t1",
            prompt_tokens=100,
            completion_tokens=10,
            cache_read=900,
            session_id="s1",
        )
        restarted = self._tracker(tmp_path)
        assert restarted._session_tokens["s1"] == 1010
