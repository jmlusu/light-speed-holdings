"""Unit tests for the Marketing Site journey-event durable store.

Covers :class:`ai_company.dashboard.journey_event_store.JourneyEventStore`:
add/id assignment, newest-first listing with filters, persistence across
instances, and retention pruning.  Uses an explicit temp base dir so tests
never touch the real project state.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from ai_company.dashboard.journey_event_store import (
    RETENTION_DAYS,
    JourneyEventStore,
)


def _event(**over: object) -> dict[str, object]:
    base: dict[str, object] = {
        "eventType": "page_view",
        "route": "/",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sessionId": "sess-1",
    }
    base.update(over)
    return base


def test_add_persists_and_assigns_id(tmp_path: Path) -> None:
    store = JourneyEventStore(base_dir=tmp_path)
    ids = store.add([_event()])
    assert len(ids) == 1
    rows = store.list_events()
    assert len(rows) == 1
    assert rows[0]["id"] == ids[0]
    assert rows[0]["ingested_at"]
    # Survives a fresh store instance over the same dir.
    rows2 = JourneyEventStore(base_dir=tmp_path).list_events()
    assert len(rows2) == 1


def test_add_empty_batch_returns_empty(tmp_path: Path) -> None:
    store = JourneyEventStore(base_dir=tmp_path)
    assert store.add([]) == []
    assert store.count() == 0


def test_list_filters_by_type_and_route(tmp_path: Path) -> None:
    store = JourneyEventStore(base_dir=tmp_path)
    store.add(
        [
            _event(eventType="page_view", route="/"),
            _event(eventType="cta_clicked", route="/solutions"),
            _event(eventType="page_view", route="/solutions"),
        ]
    )
    assert len(store.list_events(event_type="page_view")) == 2
    assert len(store.list_events(route="/solutions")) == 2
    assert len(store.list_events(event_type="page_view", route="/solutions")) == 1


def test_list_newest_first_and_limit(tmp_path: Path) -> None:
    store = JourneyEventStore(base_dir=tmp_path)
    old = _event(timestamp=(datetime.now(timezone.utc) - timedelta(hours=2)).isoformat())
    new = _event(timestamp=datetime.now(timezone.utc).isoformat())
    store.add([old, new])
    rows = store.list_events(limit=1)
    assert len(rows) == 1
    assert rows[0]["timestamp"] == new["timestamp"]


def test_retention_prunes_expired_events(tmp_path: Path) -> None:
    store = JourneyEventStore(base_dir=tmp_path)
    expired_ts = (datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS + 1)).isoformat()
    fresh_ts = datetime.now(timezone.utc).isoformat()
    store.add([_event(timestamp=expired_ts), _event(timestamp=fresh_ts)])
    rows = store.list_events()
    assert len(rows) == 1
    assert rows[0]["timestamp"] == fresh_ts


def test_missing_file_returns_empty(tmp_path: Path) -> None:
    store = JourneyEventStore(base_dir=tmp_path)
    assert store.count() == 0
    assert store.list_events() == []
