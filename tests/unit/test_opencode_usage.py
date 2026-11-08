"""Tests for OpenCode Desktop usage import (no real-DB writes)."""

from __future__ import annotations

import json
import sqlite3


def _make_db(path, sessions):
    conn = sqlite3.connect(str(path))
    conn.execute(
        """CREATE TABLE session_v2 (
            id TEXT PRIMARY KEY, directory TEXT, agent TEXT,
            model TEXT, tokens_input INTEGER, tokens_output INTEGER,
            tokens_reasoning INTEGER, tokens_cache_read INTEGER,
            tokens_cache_write INTEGER, cost REAL,
            time_created INTEGER, time_updated INTEGER)"""
    )
    for s in sessions:
        conn.execute(
            "INSERT INTO session_v2 VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                s["id"],
                s.get("directory", "C:/Users/jmlus/light-speed-holdings"),
                s.get("agent", "build"),
                json.dumps({"id": s.get("model", "gpt-4o"), "providerID": "opencode"}),
                s.get("tokens_input", 100),
                s.get("tokens_output", 50),
                s.get("tokens_reasoning", 10),
                s.get("tokens_cache_read", 20),
                s.get("tokens_cache_write", 5),
                s.get("cost", 0.0),
                1730000000000,
                1730000000000,
            ),
        )
    conn.commit()
    conn.close()


def test_normalize_prompt_completion_cache_split():
    from ai_company.llm.opencode_usage import normalize_session_row

    rec = normalize_session_row(
        session_id="ses_1",
        agent="build",
        model_raw={"id": "gpt-4o", "providerID": "opencode"},
        tokens_input=100,
        tokens_output=50,
        tokens_reasoning=10,
        tokens_cache_read=999,
        tokens_cache_write=5,
        raw_cost=0.0,
        time_created=1730000000000,
    )
    assert rec is not None
    # prompt = input + cache_write (cache_read never inflates cost)
    assert rec["prompt_tokens"] == 105
    assert rec["completion_tokens"] == 60
    assert rec["cache_read"] == 999
    assert rec["cache_write"] == 5
    assert rec["source"] == "opencode-desktop"
    assert rec["session_id"] == "ses_1"
    assert rec["event_id"] == "ses_ses_1"
    assert rec["task_id"] == "ses_1"


def test_normalize_skips_zero_token_rows():
    from ai_company.llm.opencode_usage import normalize_session_row

    assert (
        normalize_session_row(
            session_id="ses_0",
            agent="build",
            model_raw={"id": "gpt-4o", "providerID": "opencode"},
            tokens_input=0,
            tokens_output=0,
            tokens_reasoning=0,
            tokens_cache_read=0,
            tokens_cache_write=0,
            raw_cost=0.0,
            time_created=1730000000000,
        )
        is None
    )


def test_normalize_free_model_zero_cost():
    from ai_company.llm.opencode_usage import normalize_session_row

    rec = normalize_session_row(
        session_id="ses_free",
        agent="general",
        model_raw={"id": "crouton-alpha-free", "providerID": "opencode"},
        tokens_input=100,
        tokens_output=50,
        tokens_reasoning=0,
        tokens_cache_read=0,
        tokens_cache_write=0,
        raw_cost=0.0,
        time_created=1730000000000,
    )
    assert rec is not None
    assert rec["cost_usd"] == 0.0
    assert rec["cost_source"] == "recomputed"


def test_iter_project_filter(tmp_path):
    from ai_company.llm.opencode_usage import iter_opencode_sessions

    db = tmp_path / "opencode.db"
    _make_db(
        db,
        [
            {"id": "ses_a", "directory": "C:/Users/jmlus/light-speed-holdings"},
            {
                "id": "ses_b",
                "directory": "C:/other/project",
            },
        ],
    )
    rows = list(iter_opencode_sessions(db, project="light-speed-holdings"))
    assert [r["session_id"] for r in rows] == ["ses_a"]


def test_cost_analytics_event_id_dedup(tmp_path):
    from ai_company.data.cost_analytics import CostAnalytics
    from ai_company.data.database import Database

    db = tmp_path / "ai.db"
    database = Database(db)
    database.init_schema()
    analytics = CostAnalytics(database)
    kwargs = {
        "model": "gpt-4o",
        "provider": "opencode",
        "agent_name": "build",
        "task_id": "ses_a",
        "prompt_tokens": 105,
        "completion_tokens": 60,
        "cost_usd": 0.01,
        "source": "opencode-desktop",
        "session_id": "ses_a",
        "event_id": "ses_ses_a",
    }
    assert analytics.record_usage(**kwargs) != 0
    # Second insert with same event_id is a no-op (returns 0, no new row)
    assert analytics.record_usage(**kwargs) == 0
    assert analytics.total_records() == 1


def test_usage_record_source_defaults():
    from ai_company.llm.cost_tracker import UsageRecord

    rec = UsageRecord(
        timestamp="2026-11-08T00:00:00+00:00",
        model="gpt-4o",
        provider="opencode",
        agent_name="build",
        task_id="t1",
        prompt_tokens=1,
        completion_tokens=1,
        cost_usd=0.001,
    )
    assert rec.source == "ai-company-cli"
    assert rec.event_id == ""
    assert rec.cache_read == 0
