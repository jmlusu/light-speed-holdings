"""Queue for platform-ready Pharos publish artifacts.

The publish queue is the "buy-side rail" for LinkedIn / Substack: content is
formatted into a platform-ready artifact, recorded here, and (optionally)
mirrored to the agent task store so an operator or agent can review and post.
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

DEFAULT_QUEUE_DIR = "results/pharos"
DEFAULT_QUEUE_FILE = "publish_queue.json"

# Platform identifiers the queue accepts. Formatters in formats.py cover
# linkedin and substack today; the set is explicit so unknown rails fail early.
KNOWN_PLATFORMS = frozenset({"linkedin", "substack"})

_UTC = timezone.utc


def _utc_now() -> str:
    return datetime.now(_UTC).isoformat()


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "item"


def _normalize_body(body: Any) -> str:
    """Collapse any input shape into a flat string for storage."""
    if isinstance(body, str):
        return body
    if isinstance(body, (dict, list)):
        return json.dumps(body, sort_keys=True)
    return str(body)


class PublishRecord:
    """One platform-ready publish artifact in the queue."""

    __slots__ = (
        "id",
        "platform",
        "title",
        "body",
        "status",
        "created_at",
        "external_url",
        "notes",
    )

    def __init__(
        self,
        *,
        id: str,
        platform: str,
        title: str,
        body: str,
        status: str = "queued",
        created_at: str | None = None,
        external_url: str = "",
        notes: str = "",
    ) -> None:
        self.id = id
        self.platform = platform
        self.title = title
        self.body = body
        self.status = status
        self.created_at = created_at or _utc_now()
        self.external_url = external_url
        self.notes = notes

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "platform": self.platform,
            "title": self.title,
            "body": self.body,
            "status": self.status,
            "created_at": self.created_at,
            "external_url": self.external_url,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PublishRecord":
        return cls(**data)


class PublishQueue:
    """FileStore-backed queue of publish artifacts.

    Records live in a single JSON file (``results/pharos/publish_queue.json``
    by default) so the queue survives restarts and is readable by the
    dashboard/KPI layer. Optional ``mirror_to_bus`` sends a ``pharos-publish``
    task through the agent message bus so the publish intent is visible to the
    executor loop.
    """

    def __init__(
        self,
        queue_dir: str | Path | None = None,
        *,
        queue_file: str = DEFAULT_QUEUE_FILE,
    ) -> None:
        self.queue_dir = Path(queue_dir) if queue_dir is not None else Path(DEFAULT_QUEUE_DIR)
        self.queue_file = queue_file
        self._store = FileStore(self.queue_dir, backup=True)
        self._records: list[PublishRecord] = []
        self._load()

    def _load(self) -> None:
        self._records = []
        data = self._store.read_json(self.queue_file)
        if isinstance(data, list):
            for raw in data:
                if isinstance(raw, dict):
                    try:
                        self._records.append(PublishRecord.from_dict(raw))
                    except Exception:  # noqa: BLE001 - a bad record must not break the queue
                        logger.warning("Skipping invalid publish record: %r", raw)
        self._records.sort(key=lambda r: r.created_at)

    def _save(self) -> None:
        payload = [r.to_dict() for r in self._records]
        self._store.write_json(self.queue_file, payload)

    def enqueue(
        self,
        platform: str,
        title: str,
        body: Any,
        *,
        bus: Any | None = None,
        external_url: str = "",
        notes: str = "",
    ) -> PublishRecord:
        """Add a platform-ready artifact to the queue.

        ``platform`` must be in KNOWN_PLATFORMS. When ``bus`` is provided the
        record is mirrored as a ``pharos-publish`` task so the intent flows
        through the normal agent inbox.
        """
        platform = platform.lower()
        if platform not in KNOWN_PLATFORMS:
            raise ValueError(f"Unknown publish platform: {platform!r}")

        record = PublishRecord(
            id=f"pub-{_slugify(platform)}-{uuid.uuid4().hex[:8]}",
            platform=platform,
            title=title,
            body=_normalize_body(body),
            external_url=external_url,
            notes=notes,
        )
        self._records.append(record)
        self._save()

        if bus is not None:
            try:
                from ai_company.models.task import Task

                bus.send_task(
                    Task(
                        id=record.id,
                        name=f"Publish '{record.title}' to {platform}",
                        sender_id="publish-queue",
                        receiver_id="content_creator",
                        instruction=(
                            f"Review and publish the queued artifact '{record.title}' "
                            f"to {platform}. Queue record: {record.id} (status={record.status})."
                        ),
                        tags=["pharos-publish", f"publish:{platform}"],
                    )
                )
            except Exception:  # noqa: BLE001 - bus mirror is best-effort
                logger.warning("Failed to mirror publish record %s to bus", record.id)

        logger.info("Enqueued publish %s (%s): %r", record.id, platform, record.title)
        return record

    def list(self, *, status: str | None = None) -> list[PublishRecord]:
        if status is None:
            return list(self._records)
        return [r for r in self._records if r.status == status]

    def get(self, record_id: str) -> PublishRecord | None:
        return next((r for r in self._records if r.id == record_id), None)

    def mark_posted(
        self,
        record_id: str,
        *,
        external_url: str = "",
        notes: str = "posted",
    ) -> PublishRecord | None:
        record = self.get(record_id)
        if record is None:
            return None
        record.status = "posted"
        record.external_url = external_url
        record.notes = notes
        self._save()
        return record

    def mark_failed(self, record_id: str, *, notes: str = "failed") -> PublishRecord | None:
        record = self.get(record_id)
        if record is None:
            return None
        record.status = "failed"
        record.notes = notes
        self._save()
        return record

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for record in self._records:
            counts[record.status] = counts.get(record.status, 0) + 1
        counts["total"] = len(self._records)
        return counts

    def clear(self) -> None:
        self._records = []
        self._save()


__all__ = [
    "DEFAULT_QUEUE_DIR",
    "DEFAULT_QUEUE_FILE",
    "KNOWN_PLATFORMS",
    "PublishQueue",
    "PublishRecord",
]
