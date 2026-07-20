"""Tests for the SQLite-backed AuditStore."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.data.database import Database
from ai_company.data.audit_store import AuditStore


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database."""
    database = Database(tmp_path / "test_audit.db")
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
    agent_id: str = "agent-1",
    task_id: str = "task-1",
    timestamp: str = "2025-01-15T10:00:00Z",
    **overrides,
) -> AuditEvent:
    """Helper to create an AuditEvent."""
    return AuditEvent(
        event_id=event_id,
        event_type=event_type,
        agent_id=agent_id,
        task_id=task_id,
        timestamp=timestamp,
        **overrides,
    )


class TestAuditStoreWrite:
    """Tests for write operations."""

    def test_write_single_event(self, store: AuditStore) -> None:
        """write() persists a single event."""
        event = _make_event()
        store.write(event)
        assert store.count() == 1

    def test_write_batch(self, store: AuditStore) -> None:
        """write_batch persists multiple events."""
        events = [_make_event(event_id=f"e-{i}") for i in range(5)]
        store.write_batch(events)
        assert store.count() == 5

    def test_write_empty_batch(self, store: AuditStore) -> None:
        """write_batch with empty list is a no-op."""
        store.write_batch([])
        assert store.count() == 0


class TestAuditStoreRead:
    """Tests for read operations."""

    def _seed_events(self, store: AuditStore) -> None:
        """Insert test events for reading."""
        events = [
            _make_event(
                event_id="e1",
                event_type=AuditEventType.TOOL_CALL,
                agent_id="alice",
                task_id="t1",
                timestamp="2025-01-15T10:00:00Z",
                severity="info",
            ),
            _make_event(
                event_id="e2",
                event_type=AuditEventType.TASK_COMPLETED,
                agent_id="bob",
                task_id="t1",
                timestamp="2025-01-15T11:00:00Z",
                severity="info",
            ),
            _make_event(
                event_id="e3",
                event_type=AuditEventType.ERROR,
                agent_id="alice",
                task_id="t2",
                timestamp="2025-01-16T09:00:00Z",
                severity="error",
            ),
        ]
        store.write_batch(events)

    def test_read_all(self, store: AuditStore) -> None:
        """read_all returns all events."""
        self._seed_events(store)
        all_events = store.read_all()
        assert len(all_events) == 3

    def test_read_by_task(self, store: AuditStore) -> None:
        """read_by_task filters correctly."""
        self._seed_events(store)
        events = store.read_by_task("t1")
        assert len(events) == 2

    def test_read_by_agent(self, store: AuditStore) -> None:
        """read_by_agent filters correctly."""
        self._seed_events(store)
        events = store.read_by_agent("alice")
        assert len(events) == 2

    def test_read_by_type(self, store: AuditStore) -> None:
        """read_by_type filters correctly."""
        self._seed_events(store)
        events = store.read_by_type("tool_call")
        assert len(events) == 1
        assert events[0].event_id == "e1"

    def test_read_since(self, store: AuditStore) -> None:
        """read_since returns events at or after the cutoff."""
        self._seed_events(store)
        events = store.read_since("2025-01-16T00:00:00Z")
        assert len(events) == 1
        assert events[0].event_id == "e3"

    def test_read_date_range(self, store: AuditStore) -> None:
        """read_date_range filters within a window."""
        self._seed_events(store)
        events = store.read_date_range(
            "2025-01-15T10:30:00Z", "2025-01-15T11:30:00Z"
        )
        assert len(events) == 1
        assert events[0].event_id == "e2"

    def test_read_by_severity(self, store: AuditStore) -> None:
        """read_by_severity filters correctly."""
        self._seed_events(store)
        events = store.read_by_severity("error")
        assert len(events) == 1

    def test_count_by_type(self, store: AuditStore) -> None:
        """count_by_type returns correct mapping."""
        self._seed_events(store)
        counts = store.count_by_type()
        assert counts["tool_call"] == 1
        assert counts["task_completed"] == 1
        assert counts["error"] == 1

    def test_count_by_agent(self, store: AuditStore) -> None:
        """count_by_agent returns correct mapping."""
        self._seed_events(store)
        counts = store.count_by_agent()
        assert counts["alice"] == 2
        assert counts["bob"] == 1


class TestAuditStoreMigration:
    """Tests for JSONL import/export."""

    def test_import_jsonl(self, store: AuditStore, tmp_path: Path) -> None:
        """import_jsonl loads events from the legacy JSONL format."""
        events = [
            AuditEvent(
                event_id="imp-1",
                event_type=AuditEventType.TOOL_CALL,
                agent_id="agent-x",
                timestamp="2025-01-15T10:00:00Z",
            ),
            AuditEvent(
                event_id="imp-2",
                event_type=AuditEventType.TASK_COMPLETED,
                agent_id="agent-y",
                timestamp="2025-01-15T11:00:00Z",
            ),
        ]
        jsonl_path = tmp_path / "audit.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(e.model_dump()) + "\n")

        count = store.import_jsonl(jsonl_path)
        assert count == 2

    def test_import_jsonl_missing_file(self, store: AuditStore, tmp_path: Path) -> None:
        """import_jsonl handles missing file gracefully."""
        count = store.import_jsonl(tmp_path / "nonexistent.jsonl")
        assert count == 0

    def test_export_jsonl(self, store: AuditStore, tmp_path: Path) -> None:
        """export_jsonl writes events to the legacy format."""
        store.write(_make_event(event_id="exp-1"))
        export_path = tmp_path / "exported.jsonl"
        store.export_jsonl(export_path)

        assert export_path.exists()
        lines = export_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["event_id"] == "exp-1"


class TestAuditStoreArchival:
    """Tests for log rotation / archival."""

    def test_archive_before(self, store: AuditStore, tmp_path: Path) -> None:
        """archive_before moves old events to an archive file."""
        events = [
            _make_event(event_id="old-1", timestamp="2025-01-01T10:00:00Z"),
            _make_event(event_id="old-2", timestamp="2025-01-02T10:00:00Z"),
            _make_event(event_id="new-1", timestamp="2025-06-01T10:00:00Z"),
        ]
        store.write_batch(events)

        archive_path = tmp_path / "archive" / "audit_archive.json"
        archived = store.archive_before("2025-01-15T00:00:00Z", archive_path)
        assert archived == 2

        # Verify archive file
        assert archive_path.exists()
        with open(archive_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 2

        # Verify remaining events
        remaining = store.read_all()
        assert len(remaining) == 1
        assert remaining[0].event_id == "new-1"

    def test_archive_before_no_old_events(self, store: AuditStore, tmp_path: Path) -> None:
        """archive_before returns 0 when no events are old enough."""
        store.write(_make_event(event_id="fresh", timestamp="2025-06-01T10:00:00Z"))
        archived = store.archive_before(
            "2025-01-01T00:00:00Z", tmp_path / "archive.json"
        )
        assert archived == 0
        assert store.count() == 1
