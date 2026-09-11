"""Tests for the Searchable Execution Timeline — data layer and API endpoints."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.data.audit_store import AuditStore
from ai_company.data.database import Database


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database with schema."""
    database = Database(tmp_path / "test_timeline.db")
    database.init_schema()
    yield database
    database.close()


@pytest.fixture
def store(db: Database) -> AuditStore:
    """Create an AuditStore backed by the test database."""
    return AuditStore(db)


def _make_event(
    event_id: str = "evt-1",
    event_type: AuditEventType = AuditEventType.TOOL_CALL,
    agent_id: str = "cto",
    task_id: str = "task-1",
    tool: str = "bash",
    severity: str = "info",
    timestamp: str = "2026-08-26T12:00:00Z",
    args: dict | None = None,
    result: dict | None = None,
) -> AuditEvent:
    """Helper to create an AuditEvent."""
    return AuditEvent(
        event_id=event_id,
        event_type=event_type,
        agent_id=agent_id,
        task_id=task_id,
        tool=tool,
        severity=severity,
        timestamp=timestamp,
        args=args or {"command": "git status"},
        result=result or {"output": "On branch main"},
        metadata={},
    )


class TestAuditStoreSearchWithFilters:
    """Tests for AuditStore.search_with_filters()."""

    def test_empty_db_returns_empty(self, store: AuditStore) -> None:
        """Empty database returns empty results."""
        events, count = store.search_with_filters()
        assert events == []
        assert count == 0

    def test_returns_all_events_when_no_filters(self, store: AuditStore) -> None:
        """No filters returns all events."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", agent_id="cto"),
                _make_event(event_id="evt-2", agent_id="hr"),
            ]
        )
        events, count = store.search_with_filters()
        assert count == 2
        assert len(events) == 2

    def test_filter_by_agent_id(self, store: AuditStore) -> None:
        """Filtering by agent_id returns only matching events."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", agent_id="cto"),
                _make_event(event_id="evt-2", agent_id="hr"),
                _make_event(event_id="evt-3", agent_id="cto"),
            ]
        )
        events, count = store.search_with_filters(agent_id="cto")
        assert count == 2
        assert all(e["agent_id"] == "cto" for e in events)

    def test_filter_by_event_type(self, store: AuditStore) -> None:
        """Filtering by event_type returns only matching events."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", event_type=AuditEventType.TOOL_CALL),
                _make_event(event_id="evt-2", event_type=AuditEventType.ERROR),
            ]
        )
        events, count = store.search_with_filters(event_type="error")
        assert count == 1
        assert events[0]["event_type"] == "error"

    def test_filter_by_severity(self, store: AuditStore) -> None:
        """Filtering by severity returns only matching events."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", severity="info"),
                _make_event(event_id="evt-2", severity="error"),
            ]
        )
        events, count = store.search_with_filters(severity="error")
        assert count == 1

    def test_limit(self, store: AuditStore) -> None:
        """Limit caps the number of returned events while total_count reflects all."""
        store.write_batch([_make_event(event_id=f"evt-{i}") for i in range(10)])
        events, count = store.search_with_filters(limit=3)
        assert count == 10
        assert len(events) == 3

    def test_filter_by_task_id(self, store: AuditStore) -> None:
        """Filtering by task_id returns only matching events."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", task_id="task-a"),
                _make_event(event_id="evt-2", task_id="task-b"),
                _make_event(event_id="evt-3", task_id="task-a"),
            ]
        )
        events, count = store.search_with_filters(task_id="task-a")
        assert count == 2
        assert all(e["task_id"] == "task-a" for e in events)

    def test_filter_by_tool(self, store: AuditStore) -> None:
        """Filtering by tool returns only matching events."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", tool="bash"),
                _make_event(event_id="evt-2", tool="grep"),
            ]
        )
        events, count = store.search_with_filters(tool="grep")
        assert count == 1
        assert events[0]["tool"] == "grep"

    def test_combined_filters(self, store: AuditStore) -> None:
        """Multiple filters are applied conjunctively."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", agent_id="cto", severity="info"),
                _make_event(event_id="evt-2", agent_id="cto", severity="error"),
                _make_event(event_id="evt-3", agent_id="hr", severity="info"),
            ]
        )
        events, count = store.search_with_filters(agent_id="cto", severity="info")
        assert count == 1
        assert events[0]["event_id"] == "evt-1"

    def test_time_range_filters(self, store: AuditStore) -> None:
        """from_time and to_time filter events within a time window."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", timestamp="2026-08-20T10:00:00Z"),
                _make_event(event_id="evt-2", timestamp="2026-08-25T10:00:00Z"),
                _make_event(event_id="evt-3", timestamp="2026-08-28T10:00:00Z"),
            ]
        )
        events, count = store.search_with_filters(
            from_time="2026-08-22T00:00:00Z",
            to_time="2026-08-27T00:00:00Z",
        )
        assert count == 1
        assert events[0]["event_id"] == "evt-2"

    def test_cursor_pagination(self, store: AuditStore) -> None:
        """Cursor-based pagination returns events with timestamp <= cursor event.

        The cursor is inclusive: the event at the cursor timestamp is included
        in the next page.  The caller must skip the cursor event client-side
        (standard keyset-pagination convention).
        """
        store.write_batch(
            [
                _make_event(event_id="evt-1", timestamp="2026-08-20T10:00:00Z"),
                _make_event(event_id="evt-2", timestamp="2026-08-25T10:00:00Z"),
                _make_event(event_id="evt-3", timestamp="2026-08-28T10:00:00Z"),
            ]
        )
        # First page (ordered DESC): evt-3, evt-2
        events1, count = store.search_with_filters(limit=2)
        assert count == 3
        assert len(events1) == 2
        assert events1[0]["event_id"] == "evt-3"
        assert events1[1]["event_id"] == "evt-2"

        # Use cursor (evt-2) to get next page — inclusive, so returns
        # evt-2 and evt-1 (both have timestamp <= evt-2's timestamp).
        cursor = events1[-1]["event_id"]
        events2, count2 = store.search_with_filters(limit=2, cursor=cursor)
        # total_count reflects rows matching the cursor filter (<= cursor_ts)
        assert count2 == 2
        # evt-2 (cursor) is included again — caller skips it client-side
        assert {e["event_id"] for e in events2} == {"evt-2", "evt-1"}


class TestAuditStoreGetTaskTrace:
    """Tests for AuditStore.get_task_trace()."""

    def test_returns_events_for_task(self, store: AuditStore) -> None:
        """get_task_trace returns all events for a given task in chronological order."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", task_id="t1", timestamp="2026-08-26T10:00:00Z"),
                _make_event(event_id="evt-2", task_id="t2", timestamp="2026-08-26T10:01:00Z"),
                _make_event(event_id="evt-3", task_id="t1", timestamp="2026-08-26T10:02:00Z"),
            ]
        )
        events = store.get_task_trace("t1")
        assert len(events) == 2
        assert events[0]["event_id"] == "evt-1"
        assert events[1]["event_id"] == "evt-3"

    def test_returns_empty_for_unknown_task(self, store: AuditStore) -> None:
        """get_task_trace returns empty list for unknown task."""
        events = store.get_task_trace("nonexistent")
        assert events == []


class TestAuditStoreGetAgentActivity:
    """Tests for AuditStore.get_agent_activity()."""

    def test_returns_events_for_agent(self, store: AuditStore) -> None:
        """get_agent_activity returns events for a specific agent."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", agent_id="cto"),
                _make_event(event_id="evt-2", agent_id="hr"),
                _make_event(event_id="evt-3", agent_id="cto"),
            ]
        )
        events = store.get_agent_activity("cto")
        assert len(events) == 2
        assert all(e["agent_id"] == "cto" for e in events)

    def test_filters_by_event_type(self, store: AuditStore) -> None:
        """get_agent_activity filters by event_type."""
        store.write_batch(
            [
                _make_event(event_id="evt-1", agent_id="cto", event_type=AuditEventType.TOOL_CALL),
                _make_event(event_id="evt-2", agent_id="cto", event_type=AuditEventType.ERROR),
            ]
        )
        events = store.get_agent_activity("cto", event_type="error")
        assert len(events) == 1
        assert events[0]["event_type"] == "error"

    def test_respects_limit(self, store: AuditStore) -> None:
        """get_agent_activity respects the limit parameter."""
        store.write_batch([_make_event(event_id=f"evt-{i}", agent_id="cto") for i in range(10)])
        events = store.get_agent_activity("cto", limit=3)
        assert len(events) == 3


class TestAuditStoreTimelineStats:
    """Tests for AuditStore.get_timeline_stats()."""

    def test_empty_stats(self, store: AuditStore) -> None:
        """Empty database returns empty aggregation dicts."""
        stats = store.get_timeline_stats()
        assert stats["by_event_type"] == {}
        assert stats["by_agent"] == {}
        assert stats["by_severity"] == {}

    def test_stats_aggregation(self, store: AuditStore) -> None:
        """Stats correctly aggregate counts by type, agent, and severity."""
        store.write_batch(
            [
                _make_event(
                    event_id="evt-1",
                    event_type=AuditEventType.TOOL_CALL,
                    agent_id="cto",
                    severity="info",
                ),
                _make_event(
                    event_id="evt-2",
                    event_type=AuditEventType.TOOL_CALL,
                    agent_id="hr",
                    severity="info",
                ),
                _make_event(
                    event_id="evt-3",
                    event_type=AuditEventType.ERROR,
                    agent_id="cto",
                    severity="error",
                ),
            ]
        )
        stats = store.get_timeline_stats()
        assert stats["by_event_type"]["tool_call"] == 2
        assert stats["by_event_type"]["error"] == 1
        assert stats["by_agent"]["cto"] == 2
        assert stats["by_agent"]["hr"] == 1
        assert stats["by_severity"]["info"] == 2
        assert stats["by_severity"]["error"] == 1

    def test_stats_with_time_range(self, store: AuditStore) -> None:
        """Stats respect time range filters."""
        store.write_batch(
            [
                _make_event(
                    event_id="evt-1",
                    event_type=AuditEventType.TOOL_CALL,
                    agent_id="cto",
                    timestamp="2026-08-20T10:00:00Z",
                ),
                _make_event(
                    event_id="evt-2",
                    event_type=AuditEventType.ERROR,
                    agent_id="cto",
                    timestamp="2026-08-28T10:00:00Z",
                ),
            ]
        )
        stats = store.get_timeline_stats(
            from_time="2026-08-25T00:00:00Z",
            to_time="2026-08-30T00:00:00Z",
        )
        assert stats["by_event_type"] == {"error": 1}
        assert stats["time_range"]["from"] == "2026-08-25T00:00:00Z"
        assert stats["time_range"]["to"] == "2026-08-30T00:00:00Z"

    def test_stats_time_range_fields(self, store: AuditStore) -> None:
        """Stats return time_range dict even with no time filters."""
        stats = store.get_timeline_stats()
        assert "time_range" in stats
        assert stats["time_range"]["from"] == ""
        assert stats["time_range"]["to"] == ""


class TestAuditStoreCompactEvents:
    """Tests for AuditStore.compact_events()."""

    def test_compact_returns_zero_when_no_old_events(self, store: AuditStore) -> None:
        """No old events means compact returns 0."""
        store.write(_make_event(timestamp="2026-08-26T12:00:00Z"))
        count = store.compact_events(older_than_days=7)
        assert count == 0

    def test_compact_returns_zero_when_args_short(self, store: AuditStore) -> None:
        """Events with short args are not compacted."""
        store.write(
            _make_event(
                timestamp="2026-08-01T12:00:00Z",
                args={"command": "ls"},
            )
        )
        count = store.compact_events(older_than_days=7)
        assert count == 0


class TestTimelineAPIEndpoints:
    """Tests for the /api/v1/timeline/* FastAPI endpoints.

    Uses TestClient against the real app with DASHBOARD_AUTH_MODE=open (set
    by the root conftest autouse fixture).
    """

    def test_timeline_search_returns_shape(self) -> None:
        """/api/v1/timeline/search returns expected response shape."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/timeline/search")
        assert resp.status_code == 200
        data = resp.json()
        assert "events" in data
        assert "total_count" in data
        assert "cursor" in data
        assert "query_ms" in data

    def test_timeline_returns_shape(self) -> None:
        """/api/v1/timeline returns expected response shape."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/timeline")
        assert resp.status_code == 200
        data = resp.json()
        assert "events" in data
        assert "total_count" in data

    def test_timeline_task_trace_returns_shape(self) -> None:
        """/api/v1/timeline/task/{task_id} returns expected response shape."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/timeline/task/nonexistent")
        assert resp.status_code == 200
        data = resp.json()
        assert "events" in data

    def test_timeline_agent_returns_shape(self) -> None:
        """/api/v1/timeline/agent/{agent_id} returns expected response shape."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/timeline/agent/nonexistent")
        assert resp.status_code == 200
        data = resp.json()
        assert "events" in data

    def test_timeline_stats_returns_shape(self) -> None:
        """/api/v1/timeline/stats returns expected response shape."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/timeline/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "by_event_type" in data
        assert "by_agent" in data
        assert "by_severity" in data
        assert "time_range" in data

    def test_timeline_search_with_query_param(self) -> None:
        """/api/v1/timeline/search?q=test&limit=10 works and returns query_ms."""
        from fastapi.testclient import TestClient

        from ai_company.dashboard.app import app

        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/v1/timeline/search?q=test&limit=10")
        assert resp.status_code == 200
        data = resp.json()
        assert "query_ms" in data
        assert isinstance(data["query_ms"], (int, float))
