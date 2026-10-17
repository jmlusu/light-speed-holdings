"""Durable storage for Marketing Site journey events.

The marketing-site edge function (``api/journey-events.ts``) validates and
rate-limits incoming journey events but previously held them only in an
in-memory buffer that is lost on cold start. This module provides the
server-side durable layer: events are persisted as a JSON list via
:class:`ai_company.store.file_store.FileStore` under the dashboard data
root (``<state base>/dashboard/journey_events.json``), matching the
AlertStore storage convention.

Retention is 400 days to align with the ``marketing_site_events``
retention policy registered in :mod:`ai_company.data.governance`
(owner: cmo, classification: INTERNAL, action: ARCHIVE).
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from ai_company.dashboard.repository import get_state_store
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

# Align with governance policy: 400 days, then ARCHIVE (pruned from hot store).
RETENTION_DAYS = 400
_EVENTS_REL = Path("journey_events.json")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class JourneyEventStore:
    """Persist and query marketing-site journey events.

    Parameters
    ----------
    base_dir:
        Root directory for the event data file. Defaults to the configured
        :class:`StateStore` base (so tests anchored at a temp root never
        write into the real project), mirroring ``AlertStore``.
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        if base_dir is None:
            base_dir = Path(get_state_store().base_dir) / "dashboard"
        self._dir = base_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._store = FileStore(self._dir, backup=False)

    def add(self, events: list[dict[str, Any]]) -> list[str]:
        """Persist a batch of journey events. Returns the assigned ids."""
        if not events:
            return []
        rows = self._read()
        added: list[str] = []
        for raw in events:
            event = dict(raw)
            event["id"] = str(uuid.uuid4())
            event.setdefault("ingested_at", _now_iso())
            rows.append(event)
            added.append(event["id"])
        self._write_pruned(rows)
        return added

    def list_events(
        self,
        event_type: str | None = None,
        route: str | None = None,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """Return events newest-first, optionally filtered."""
        rows = self._read()
        if event_type:
            rows = [e for e in rows if e.get("eventType") == event_type]
        if route:
            rows = [e for e in rows if e.get("route") == route]
        rows.sort(key=lambda e: e.get("timestamp", e.get("ingested_at", "")), reverse=True)
        return rows[:limit]

    def count(self) -> int:
        return len(self._read())

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _read(self) -> list[dict[str, Any]]:
        try:
            return [dict(e) for e in self._store.read_json_list(_EVENTS_REL)]
        except FileNotFoundError:
            return []

    def _write_pruned(self, rows: list[dict[str, Any]]) -> None:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=RETENTION_DAYS)
        kept: list[dict[str, Any]] = []
        for e in rows:
            ts = self._parse_ts(e.get("timestamp")) or self._parse_ts(e.get("ingested_at"))
            if ts is None or ts >= cutoff:
                kept.append(e)
        self._store.write_json(_EVENTS_REL, kept)

    @staticmethod
    def _parse_ts(value: Any) -> datetime | None:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(str(value))
        except (TypeError, ValueError):
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed


_default_store: JourneyEventStore | None = None


def get_journey_event_store() -> JourneyEventStore:
    """Return the shared JourneyEventStore instance (lazily created)."""
    global _default_store
    if _default_store is None:
        _default_store = JourneyEventStore()
    return _default_store
