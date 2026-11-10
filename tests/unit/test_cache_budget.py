"""Tests for the daily cache-read token cap (OpenCode usage DB).

The cap reads the *OpenCode usage* DB (``opencode.db``), never the
``ai_company`` SQLite mirror, and it must fail open: a metrics problem can
never abort a task. These tests cover the threshold ladder, the read-only DB
readers, the plain-text suspension report, and the fail-open paths in both
``CostTracker`` and ``AgentLoop``.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from ai_company.data.cost_analytics import (
    DEFAULT_CACHE_READ_CAP,
    CacheBudgetStatus,
    CostAnalytics,
)
from ai_company.llm import opencode_usage
from ai_company.llm.cost_tracker import CostTracker

DAY = "2026-05-01"


# ── Helpers ─────────────────────────────────────────────────────────


def _day_start_ms(day: str) -> int:
    start = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(start.timestamp() * 1000)


def _make_message_db(path: Path, table: str, rows: list[tuple[str, Any, str]]) -> None:
    """Create a DB with one message-shaped table.

    ``rows`` are ``(id, time_created, data_json)`` triples.
    """
    conn = sqlite3.connect(str(path))
    try:
        if table == "session_message":
            conn.execute(
                f"""CREATE TABLE {table} (
                    id TEXT PRIMARY KEY, session_id TEXT, type TEXT, seq INTEGER,
                    time_created INTEGER, time_updated INTEGER, data TEXT)"""
            )
            for message_id, time_created, data in rows:
                conn.execute(
                    f"INSERT INTO {table} VALUES (?,?,?,?,?,?,?)",
                    (message_id, "ses_1", "assistant", 1, time_created, time_created, data),
                )
        else:
            conn.execute(
                f"""CREATE TABLE {table} (
                    id TEXT PRIMARY KEY, session_id TEXT,
                    time_created INTEGER, time_updated INTEGER, data TEXT)"""
            )
            for message_id, time_created, data in rows:
                conn.execute(
                    f"INSERT INTO {table} VALUES (?,?,?,?,?)",
                    (message_id, "ses_1", time_created, time_created, data),
                )
        conn.commit()
    finally:
        conn.close()


def _make_session_db(path: Path, table: str, sessions: list[dict[str, Any]]) -> None:
    """Create a DB with a ``session_v2`` or legacy ``session`` table."""
    conn = sqlite3.connect(str(path))
    try:
        if table == "session_v2":
            conn.execute(
                """CREATE TABLE session_v2 (
                    id TEXT PRIMARY KEY, agent TEXT, model TEXT, cost REAL,
                    tokens_cache_read INTEGER, time_created INTEGER,
                    time_suspended INTEGER, resume_attempts INTEGER,
                    idle_outcome TEXT)"""
            )
            for s in sessions:
                conn.execute(
                    "INSERT INTO session_v2 VALUES (?,?,?,?,?,?,?,?,?)",
                    (
                        s["id"],
                        s.get("agent", "build"),
                        json.dumps({"id": s.get("model", "gpt-4o"), "providerID": "opencode"}),
                        s.get("cost", 0.0),
                        s.get("tokens_cache_read", 0),
                        s.get("time_created", 1730000000000),
                        s.get("time_suspended"),
                        s.get("resume_attempts", 0),
                        s.get("idle_outcome"),
                    ),
                )
        else:
            # Legacy shape: no suspension columns at all.
            conn.execute(
                """CREATE TABLE session (
                    id TEXT PRIMARY KEY, agent TEXT, model TEXT, cost REAL,
                    tokens_cache_read INTEGER, time_created INTEGER)"""
            )
            for s in sessions:
                conn.execute(
                    "INSERT INTO session VALUES (?,?,?,?,?,?)",
                    (
                        s["id"],
                        s.get("agent", "build"),
                        json.dumps({"id": s.get("model", "gpt-4o"), "providerID": "opencode"}),
                        s.get("cost", 0.0),
                        s.get("tokens_cache_read", 0),
                        s.get("time_created", 1730000000000),
                    ),
                )
        conn.commit()
    finally:
        conn.close()


class _PoisonedDatabase:
    """A ``Database`` stand-in that fails loudly the moment it is touched.

    The cache-read cap must read the OpenCode usage DB. Reverting it to the
    ``ai_company`` SQLite mirror (``self._db``) is the exact regression this
    guards: a ``MagicMock`` would silently absorb that call, a poison object
    turns it into a hard failure.
    """

    def __getattr__(self, name: str) -> Any:
        raise AssertionError(f"cache budget must not read ai_company.db (accessed .{name})")


@pytest.fixture()
def analytics() -> CostAnalytics:
    """A CostAnalytics whose ``_db`` raises if any cap reader touches it."""
    return CostAnalytics(database=_PoisonedDatabase())


# ── Threshold ladder ────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("pct", "expected_level"),
    [
        (0, "ok"),
        (69, "ok"),
        (70, "warn"),
        (84, "warn"),
        (85, "compact"),
        (99, "compact"),
        (100, "block"),
        (120, "block"),
    ],
)
def test_threshold_ladder(
    analytics: CostAnalytics,
    monkeypatch: pytest.MonkeyPatch,
    pct: int,
    expected_level: str,
) -> None:
    """Each stage is reachable and the boundaries land on the right side."""
    used = DEFAULT_CACHE_READ_CAP * pct // 100
    monkeypatch.setattr(
        opencode_usage,
        "cache_read_tokens_for_day",
        lambda day, db_path=None: used,
    )

    status = analytics.check_cache_budget(DAY)

    assert status.level == expected_level
    assert status.used == used
    assert status.cap == DEFAULT_CACHE_READ_CAP
    if expected_level == "ok":
        assert status.reason is None
    else:
        assert status.reason
        assert "%" in status.reason


def test_allowed_is_false_only_for_block() -> None:
    for level in ("ok", "warn", "compact", "block"):
        status = CacheBudgetStatus(level=level, used=1, cap=2, reason=None)
        assert status.allowed is (level != "block")


def test_custom_cap_and_day_are_forwarded(
    analytics: CostAnalytics, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The explicit cap and day reach the usage reader."""
    seen: dict[str, Any] = {}

    def _fake(day: str, db_path: str | Path | None = None) -> int:
        seen["day"] = day
        return 720

    monkeypatch.setattr(opencode_usage, "cache_read_tokens_for_day", _fake)

    status = analytics.check_cache_budget("2026-04-30", cap=1000)

    assert seen["day"] == "2026-04-30"
    assert (status.level, status.used, status.cap) == ("warn", 720, 1000)


def test_cap_reads_opencode_db_not_ai_company_db(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The cap total comes from the OpenCode usage DB, never ``self._db``.

    End-to-end and unpatched at the reader: the OpenCode DB is a real SQLite
    file reached through the default-path resolver, so the total and the
    level are produced by production code. ``_db`` is poisoned, so any
    revert to the ``ai_company`` mirror fails instead of quietly returning a
    mock-derived 0.
    """
    usage_db = tmp_path / "opencode.db"
    start = _day_start_ms(DAY)
    _make_message_db(
        usage_db,
        "message",
        [("msg_cap", start + 1, json.dumps({"tokens": {"cache": {"read": 40_000_000}}}))],
    )
    monkeypatch.setattr(opencode_usage, "default_opencode_db_path", lambda: usage_db)

    status = CostAnalytics(database=_PoisonedDatabase()).check_cache_budget(DAY)

    assert status.used == 40_000_000
    assert status.level == "warn"  # 80% of the 50M default cap


# ── cache_read_tokens_for_day ───────────────────────────────────────


@pytest.mark.parametrize("table", ["message", "session_message"])
def test_cache_read_tokens_for_day_table_variants(tmp_path: Path, table: str) -> None:
    """Both message table names are supported; partial JSON contributes 0."""
    db = tmp_path / "opencode.db"
    start = _day_start_ms(DAY)
    rows = [
        ("msg_a", start + 1, json.dumps({"tokens": {"cache": {"read": 100}}})),
        ("msg_b", start + 2, json.dumps({"tokens": {"cache": {"read": 250}}})),
        # No ``tokens`` key at all.
        ("msg_c", start + 3, json.dumps({"role": "user"})),
        # ``cache`` without ``read``.
        ("msg_d", start + 4, json.dumps({"tokens": {"cache": {"write": 9}}})),
        # Outside the requested UTC day.
        ("msg_e", start - 1, json.dumps({"tokens": {"cache": {"read": 999}}})),
    ]
    _make_message_db(db, table, rows)

    assert opencode_usage.cache_read_tokens_for_day(DAY, db_path=db) == 350


def test_cache_read_tokens_for_day_dedupes_across_both_tables(tmp_path: Path) -> None:
    """A message id present in both tables is counted once, not twice."""
    db = tmp_path / "opencode.db"
    start = _day_start_ms(DAY)
    data = json.dumps({"tokens": {"cache": {"read": 40}}})
    _make_message_db(db, "message", [("msg_dup", start + 1, data)])
    conn = sqlite3.connect(str(db))
    try:
        conn.execute(
            """CREATE TABLE session_message (
                id TEXT PRIMARY KEY, session_id TEXT, type TEXT, seq INTEGER,
                time_created INTEGER, time_updated INTEGER, data TEXT)"""
        )
        conn.execute(
            "INSERT INTO session_message VALUES (?,?,?,?,?,?,?)",
            ("msg_dup", "ses_1", "assistant", 1, start + 1, start + 1, data),
        )
        conn.execute(
            "INSERT INTO session_message VALUES (?,?,?,?,?,?,?)",
            ("msg_new", "ses_1", "assistant", 2, start + 2, start + 2, data),
        )
        conn.commit()
    finally:
        conn.close()

    assert opencode_usage.cache_read_tokens_for_day(DAY, db_path=db) == 80


def test_cache_read_tokens_for_day_missing_db(tmp_path: Path) -> None:
    """A missing DB returns 0 instead of raising."""
    assert opencode_usage.cache_read_tokens_for_day(DAY, db_path=tmp_path / "nope.db") == 0


def test_cache_read_tokens_for_day_invalid_day(tmp_path: Path) -> None:
    """An unparsable day returns 0 instead of raising."""
    db = tmp_path / "opencode.db"
    _make_message_db(db, "message", [])
    assert opencode_usage.cache_read_tokens_for_day("not-a-day", db_path=db) == 0


# ── sessions_exceeding_cache_read ───────────────────────────────────


def test_sessions_exceeding_cache_read_orders_and_filters(tmp_path: Path) -> None:
    db = tmp_path / "opencode.db"
    _make_session_db(
        db,
        "session_v2",
        [
            {"id": "ses_low", "tokens_cache_read": 50, "cost": 0.0},
            {"id": "ses_high", "tokens_cache_read": 900, "cost": 1.25},
            {"id": "ses_mid", "tokens_cache_read": 400, "cost": 0.5, "resume_attempts": 2},
        ],
    )

    result = opencode_usage.sessions_exceeding_cache_read(100, db_path=db)

    assert [entry["session_id"] for entry in result] == ["ses_high", "ses_mid"]
    assert [entry["tokens_cache_read"] for entry in result] == [900, 400]
    top = result[0]
    assert set(top) == {
        "session_id",
        "tokens_cache_read",
        "time_created",
        "time_suspended",
        "resume_attempts",
        "idle_outcome",
        "cost",
        "agent",
        "model",
    }
    assert top["cost"] == pytest.approx(1.25)
    assert top["model"] == "gpt-4o"
    assert result[1]["resume_attempts"] == 2


def test_sessions_exceeding_cache_read_legacy_table_defaults(tmp_path: Path) -> None:
    """A legacy ``session`` table (no suspension columns) still returns all keys."""
    db = tmp_path / "opencode.db"
    _make_session_db(db, "session", [{"id": "ses_old", "tokens_cache_read": 500, "cost": 0.0}])

    result = opencode_usage.sessions_exceeding_cache_read(100, db_path=db)

    assert len(result) == 1
    entry = result[0]
    assert entry["session_id"] == "ses_old"
    assert entry["time_suspended"] is None
    assert entry["idle_outcome"] is None
    assert entry["resume_attempts"] == 0
    assert entry["cost"] == 0.0


def test_sessions_exceeding_cache_read_missing_db(tmp_path: Path) -> None:
    assert opencode_usage.sessions_exceeding_cache_read(0, db_path=tmp_path / "nope.db") == []


# ── suspension_report ───────────────────────────────────────────────


def test_suspension_report_keeps_zero_cost_sessions(
    analytics: CostAnalytics, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A zero-cost session still prints its cost line and separator."""
    sessions = [
        {
            "session_id": "ses_zero",
            "tokens_cache_read": 1_000,
            "time_created": 1730000000000,
            "time_suspended": None,
            "resume_attempts": 0,
            "idle_outcome": None,
            "cost": 0.0,
            "agent": "build",
            "model": "gpt-4o",
        },
        {
            "session_id": "ses_paid",
            "tokens_cache_read": 2_000,
            "time_created": 1730000001000,
            "time_suspended": 1730000002000,
            "resume_attempts": 3,
            "idle_outcome": "completed",
            "cost": 1.25,
            "agent": "plan",
            "model": "gpt-4o-mini",
        },
    ]
    monkeypatch.setattr(
        opencode_usage,
        "sessions_exceeding_cache_read",
        lambda threshold, db_path=None: list(sessions),
    )

    report = analytics.suspension_report(threshold=100)

    assert "ses_zero" in report
    assert "ses_paid" in report
    assert report.count("cost: $0.0000") == 1
    assert report.count("cost: $1.2500") == 1
    # The zero-cost block renders every field, so key-based access (never
    # positional) is proven for a row with no spend and no suspension data.
    assert "  created: 1730000000000" in report
    assert "  suspended: None" in report
    assert "  resume_attempts: 0" in report
    assert "  idle_outcome: None" in report
    assert "  agent: build  model: gpt-4o" in report
    # One separator per session plus the report header separator.
    assert report.count("-" * 66) == 3


def test_suspension_report_empty(analytics: CostAnalytics, monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, Any] = {}

    def _fake(threshold: int, db_path: str | Path | None = None) -> list[dict[str, Any]]:
        seen["threshold"] = threshold
        return []

    monkeypatch.setattr(opencode_usage, "sessions_exceeding_cache_read", _fake)
    report = analytics.suspension_report()
    # ``get_runaway_sessions`` forwards the default cap, not a hardcoded 0.
    assert seen["threshold"] == DEFAULT_CACHE_READ_CAP
    assert "Sessions exceeding threshold: 0" in report
    assert "No session exceeds" in report


# ── CostTracker fail-open ───────────────────────────────────────────


class _RaisingAnalytics:
    def check_cache_budget(self, day: str | None = None) -> Any:
        raise RuntimeError("usage db exploded")


def test_tracker_check_cache_budget_fails_open(tmp_path: Path) -> None:
    tracker = CostTracker(
        results_dir=str(tmp_path / "results"),
        export_path=str(tmp_path / "cost_tracker.json"),
    )
    tracker._cost_analytics = _RaisingAnalytics()  # type: ignore[assignment]

    status = tracker.check_cache_budget()

    assert status.level == "ok"
    assert status.allowed is True
    assert status.used == 0
    assert status.cap == DEFAULT_CACHE_READ_CAP
    assert "cache budget unavailable" in (status.reason or "")


def test_tracker_check_cache_budget_without_analytics(tmp_path: Path) -> None:
    tracker = CostTracker(
        results_dir=str(tmp_path / "results"),
        export_path=str(tmp_path / "cost_tracker.json"),
    )
    assert tracker._cost_analytics is None

    status = tracker.check_cache_budget()

    assert (status.level, status.allowed) == ("ok", True)


def test_tracker_check_cache_budget_delegates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A real analytics verdict passes through and the day is forwarded.

    Uses a real ``CostAnalytics`` (poisoned ``_db``) rather than a stubbed
    return value, so the assertion is about production behaviour and not the
    mock's own ``return_value``.
    """
    seen: dict[str, Any] = {}

    def _fake(day: str, db_path: str | Path | None = None) -> int:
        seen["day"] = day
        return DEFAULT_CACHE_READ_CAP

    monkeypatch.setattr(opencode_usage, "cache_read_tokens_for_day", _fake)
    tracker = CostTracker(
        results_dir=str(tmp_path / "results"),
        export_path=str(tmp_path / "cost_tracker.json"),
    )
    tracker._cost_analytics = CostAnalytics(database=_PoisonedDatabase())

    status = tracker.check_cache_budget("2026-05-01")

    assert seen["day"] == "2026-05-01"
    assert status.level == "block"
    assert status.allowed is False


# ── AgentLoop never aborts on a broken budget check ─────────────────


class _RaisingCacheTracker:
    """Tracker whose cache-budget check raises but whose usual API works."""

    def check_cache_budget(self, day: str | None = None) -> Any:
        raise RuntimeError("metrics backend offline")

    def check_budget(self, task_id: str, proposed_cost: float = 0.0) -> tuple[bool, str]:
        return True, "within budget"

    def estimate_call_cost(
        self, model: str, prompt_tokens: int, estimated_completion_tokens: int = 1000
    ) -> float:
        return 0.0

    def record_usage(self, **kwargs: Any) -> Any:
        return MagicMock(cost_usd=0.0)


class _BlockingCacheTracker(_RaisingCacheTracker):
    """Tracker that reports the daily cap as reached."""

    def check_cache_budget(self, day: str | None = None) -> CacheBudgetStatus:
        return CacheBudgetStatus(level="block", used=10, cap=10, reason="cap reached")


class _CompactCacheTracker(_RaisingCacheTracker):
    """Tracker reporting a log-only stage, which must never stop a task."""

    def check_cache_budget(self, day: str | None = None) -> CacheBudgetStatus:
        return CacheBudgetStatus(level="compact", used=90, cap=100, reason="compaction advised")


def _make_loop(tmp_path: Path, tracker: Any) -> Any:
    from ai_company.executor.agent_loop import AgentLoop, LoopConfig
    from ai_company.executor.tool_runner import ToolRunner
    from ai_company.llm.providers.base import ChatResponse

    provider = MagicMock()
    provider.is_available.return_value = True
    provider.chat.return_value = ChatResponse(
        content=json.dumps(
            {"thought": "no tools needed", "plan": [], "result": "Done.", "done": True}
        ),
        model="test-model",
        provider="mock",
        usage={"prompt_tokens": 10, "completion_tokens": 5},
    )
    route = MagicMock(provider="mock_provider", model="test-model", tier="standard")
    client = MagicMock()
    client.router.resolve.return_value = route
    client.router.resolve_with_complexity.return_value = route
    client.router.resolve_with_fallback.return_value = [route]
    client.router.get_tier.return_value = MagicMock(
        providers=[MagicMock(provider="mock_provider", model="test-model")]
    )
    client.get_provider.return_value = provider
    client.get_breaker.return_value = None

    return AgentLoop(
        llm=client,
        runner=ToolRunner(project_root=tmp_path),
        cost_tracker=tracker,
        config=LoopConfig(max_iterations=3),
    ), provider


def _make_agent() -> Any:
    from ai_company.executor.context import AgentContext

    return AgentContext(
        name="test-agent",
        role="test agent",
        type="Specialist",
        department="Engineering",
        mission="Complete assigned tasks.",
        responsibilities=["Execute tasks"],
        tools=["read", "grep", "list"],
    )


def test_agent_loop_survives_raising_cache_budget(tmp_path: Path) -> None:
    """A raising ``check_cache_budget`` must not escape or stop the task."""
    loop, provider = _make_loop(tmp_path, _RaisingCacheTracker())

    result = loop.run(agent=_make_agent(), user_prompt="What is 2+2?", task_id="task-cache-1")

    assert result.done is True
    assert result.error == ""
    assert provider.chat.call_count == 1


def test_agent_loop_blocks_when_cache_budget_exhausted(tmp_path: Path) -> None:
    """The ``block`` stage returns a LoopResult without calling the LLM."""
    loop, provider = _make_loop(tmp_path, _BlockingCacheTracker())

    result = loop.run(agent=_make_agent(), user_prompt="What is 2+2?", task_id="task-cache-2")

    assert result.done is False
    assert result.iterations == 0
    assert "Cache-read budget exceeded" in result.error
    assert result.final_response == ""
    assert provider.chat.call_count == 0


def test_agent_loop_runs_through_log_only_stage(tmp_path: Path) -> None:
    """``compact``/``warn`` are advisory: the task still reaches the LLM.

    Without this, a gate that treated any status as a block (or any truthy
    ``CacheBudgetStatus``) would pass both the raising and blocking tests.
    """
    loop, provider = _make_loop(tmp_path, _CompactCacheTracker())

    result = loop.run(agent=_make_agent(), user_prompt="What is 2+2?", task_id="task-cache-3")

    assert result.done is True
    assert result.error == ""
    assert provider.chat.call_count == 1
