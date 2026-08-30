"""ReportStore — queryable read layer over agent-produced reports (C5).

Agents persist their run output under ``results/<name>/`` as one or more JSON
documents (``loop_result.json``) or JSONL shards (``experiments/*.jsonl``).
There was previously no stable, queryable abstraction over these outputs: each
report was read by hand-walking the filesystem, timestamps were stored
inconsistently (mixed naive-UTC and ``Z``-suffixed forms), and there was no
consistent "newest/oldest" rule.

:class:`ReportStore` is a read-only layer that:

* walks a configured root and discovers report bundles (immediate
  subdirectories) and the documents/shards inside them,
* normalizes every timestamp to an aware, absolute ``datetime`` (naive values
  are assumed UTC; ``Z`` is handled) so ordering across mixed formats is
  correct,
* exposes query-based head/tail (``latest`` / ``oldest``) plus filters by name,
  agent and time window.

This module only *reads*; it never writes, so reports written by agents remain
the single source of truth.  The same guarded-write machinery in
``store.repo_write`` is for writer paths and is intentionally not used here.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Field keys we look for inside a document to build the report index.
_TS_KEYS = ("timestamp", "created_at", "time", "ts")
_NAME_KEYS = ("task_id", "name", "id", "experiment_name")
_AGENT_KEYS = ("agent", "agent_name", "agent_id", "sender_id", "receiver_id")
_DONE_KEYS = ("done", "task_completed", "success")
_ERROR_KEYS = ("error",)

_JSON_SUFFIXES = (".json", ".jsonl")


def normalize_timestamp(value: Any) -> datetime | None:
    """Parse *value* into an aware, absolute ``datetime``.

    Supports ISO-8601 documents with or without an explicit offset:

    * naive values (e.g. ``2026-08-13T15:35:42.885519``) are assumed UTC,
    * ``Z``-suffixed values are treated as UTC,
    * explicit offsets are preserved as-is.

    Returns ``None`` for missing, non-string or unparseable values so callers
    can skip or down-rank a report without crashing.
    """
    if value is None or isinstance(value, bool):
        return None
    if not isinstance(value, str):
        # Some producers write epoch seconds; accept ints/floats > 0.
        if isinstance(value, (int, float)) and value > 0:
            return datetime.fromtimestamp(value, tz=timezone.utc)
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _first_present(document: dict[str, Any], keys: Iterable[str]) -> Any:
    for key in keys:
        raw = document.get(key)
        if raw is not None:
            return raw
    return None


@dataclass
class Report:
    """A single indexable report document.

    A *report* corresponds to one JSON document or one JSONL record that
    carries a timestamp.  ``bundle`` is the immediate subdirectory (or root)
    that contains the source file; ``key`` is a stable, JSON-serializable
    identity for the report.
    """

    key: str
    bundle: str
    path: str
    timestamp: datetime | None
    timestamp_value: Any = None
    name: str = ""
    agent: str = ""
    done: bool | None = None
    error: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation (timestamp → ISO)."""
        return {
            "key": self.key,
            "bundle": self.bundle,
            "path": self.path,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "name": self.name,
            "agent": self.agent,
            "done": self.done,
            "error": self.error,
        }


class ReportStore:
    """Read-only, queryable index over report bundles under a root.

    Args:
        root: Directory containing report bundles (e.g. ``results/``).
            A missing root yields an empty store (no error at construction).
    """

    def __init__(self, root: str | Path | None = None) -> None:
        if root is None:
            from ai_company.dashboard.repository import get_state_store

            root = Path(get_state_store().base_dir) / "results"
        self.root = Path(root) if root is not None else Path("")

    def _candidate_files(self, base: Path) -> list[Path]:
        """Return JSON/JSONL files directly under *base* (non-deep)."""
        if not base.is_dir():
            return []
        return sorted(p for p in base.iterdir() if p.is_file() and p.suffix in _JSON_SUFFIXES)

    def _documents(self, base: Path, bundle: str) -> Iterator[Report]:
        """Yield one :class:`Report` per JSON doc / JSONL record under *base*."""
        for path in self._candidate_files(base):
            try:
                payload = _read_documents(path)
            except (OSError, ValueError) as exc:  # noqa: BLE001 - keep scanning
                logger.debug("Skipping unreadable report %s: %s", path, exc)
                continue
            for i, doc in enumerate(payload):
                yield self._build_report(path, bundle, doc, i)

    def _build_report(self, path: Path, bundle: str, doc: dict[str, Any], index: int) -> Report:
        ts_value = _first_present(doc, _TS_KEYS)
        ts = normalize_timestamp(ts_value)
        name = _first_present(doc, _NAME_KEYS)
        agent = _first_present(doc, _AGENT_KEYS)
        done = _first_present(doc, _DONE_KEYS)
        error = _first_present(doc, _ERROR_KEYS)
        name_str = str(name) if not isinstance(name, list) else ""
        agent_str = str(agent) if not isinstance(agent, list) else ""
        key = f"{bundle}:{path.name}:{index}" if index else f"{bundle}:{path.name}"
        return Report(
            key=key,
            bundle=bundle,
            path=str(path),
            timestamp=ts,
            timestamp_value=ts_value,
            name=name_str,
            agent=agent_str,
            done=bool(done) if isinstance(done, (bool, int)) else None,
            error=str(error) if error else "",
            data=doc,
        )

    def reports(self) -> list[Report]:
        """Return every discovered report, sorted newest-first by timestamp.

        Reports without a parseable timestamp sort to the end (stable order
        by key).  A missing root returns ``[]``.
        """
        if not self.root.is_dir():
            return []

        found: list[Report] = []
        # Bundles are immediate subdirectories; also index documents at the root.
        bundles = [b for b in self.root.iterdir() if b.is_dir()]
        for bundle in bundles:
            found.extend(self._documents(bundle, bundle.name))
        found.extend(self._documents(self.root, "."))

        # Newest-first for timestamped reports; undated reports always sort
        # last (stable by key) so they never shadow timestamped ordering.
        dated = [r for r in found if r.timestamp is not None]
        undated = [r for r in found if r.timestamp is None]
        dated.sort(key=lambda r: (r.timestamp, r.key), reverse=True)
        undated.sort(key=lambda r: r.key)
        return dated + undated

    def latest(self, n: int = 10, **filters: Any) -> list[Report]:
        """Return the newest ``n`` reports, after applying *filters*.

        Supported filters: ``bundle``, ``name``, ``agent`` (substring match on
        the respective field).  ``n <= 0`` returns ``[]``.
        """
        all_reports = self.reports()
        filtered = _apply_filters(all_reports, filters)
        return filtered[: n if n > 0 else 0]

    def oldest(self, n: int = 10, **filters: Any) -> list[Report]:
        """Return the oldest ``n`` reports (by timestamp), after filters.

        Reports without a parseable timestamp are treated as the oldest
        (unknown date), so they surface first here — the "sane end" for
        undated records when answering the oldest query.
        """
        if n <= 0:
            return []
        filtered = _apply_filters(self.reports(), filters)
        dated = [r for r in filtered if r.timestamp is not None]
        undated = [r for r in filtered if r.timestamp is None]
        dated.sort(key=lambda r: (r.timestamp, r.key))
        undated.sort(key=lambda r: r.key)
        return (undated + dated)[:n]


def _apply_filters(reports: list[Report], filters: dict[str, Any]) -> list[Report]:
    def matches(r: Report) -> bool:
        for key, value in filters.items():
            if value is None:
                continue
            if key == "bundle" and value not in r.bundle:
                return False
            if key == "name" and value not in r.name:
                return False
            if key == "agent" and value not in r.agent:
                return False
        return True

    return [r for r in reports if matches(r)]


def _read_documents(path: Path) -> list[dict[str, Any]]:
    """Parse *path* into a list of JSON documents.

    ``.jsonl`` files yield one document per non-empty line; ``.json`` files
    yield a single document (or the documents of a top-level JSON array).
    """
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return []
    if path.suffix == ".jsonl":
        docs: list[dict[str, Any]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj, dict):
                docs.append(obj)
        return docs
    obj = json.loads(text)
    if isinstance(obj, list):
        return [o for o in obj if isinstance(o, dict)]
    if isinstance(obj, dict):
        return [obj]
    return []
