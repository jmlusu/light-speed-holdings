"""Drift / integrity sweep — surface unrecorded overwrites.

Compares the on-disk SHA-256 of files written through the guarded
:mod:`ai_company.store.repo_write` path against the audit ledger. A mismatch
between the current on-disk digest and the *most recent* recorded
``after_hash`` for that file means the file was silently changed outside the
P0-protected write path (e.g. an uncoordinated write, a manual edit, or a
pre-P0 code path).

This is the Task 8 governance check: it turns a silent clobber into a
provable, surfaced report rather than an invisible race.

Best-effort: it can only detect overwrites of files that the audit ledger
tracks (i.e. files whose latest write went through ``repo_write``). Files
with no audit record are reported separately as "unrecorded" so an operator
can see which writes bypassed the protected path entirely.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

from ai_company.audit.events import AuditEvent
from ai_company.audit.reader import AuditReader
from ai_company.paths import get_audit_path, get_project_root

logger = logging.getLogger(__name__)

# Keys that may carry a file path inside an event's args/result/metadata.
_PATH_KEYS = ("path", "file", "target")
# Keys that may carry the post-write digest inside an event's args/result.
_HASH_KEYS = ("after_hash", "sha256")

# Paths under these directory prefixes are ignored when deriving tracked
# files from the audit ledger: they are runtime/internal state, not
# agent-authored repo files, so drift on them is out of scope.
_IGNORED_DIR_PREFIXES = (
    ".opencode",
    "results",
    "data",
    ".venv",
    "config",
)


def compute_digest(path: str | Path) -> str | None:
    """Return the SHA-256 hex digest of *path*'s bytes, or ``None`` if missing."""
    p = Path(path)
    if not p.exists() or p.is_dir():
        return None
    try:
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _event_path(event: AuditEvent) -> str | None:
    """Return the file path an event refers to, if any."""
    for container in (event.result, event.args, event.metadata):
        if not isinstance(container, dict):
            continue
        for key in _PATH_KEYS:
            val = container.get(key)
            if val:
                return str(val)
    return None


def _event_after_hash(event: AuditEvent) -> str | None:
    """Return the post-write digest recorded on an event, if any."""
    for container in (event.result, event.metadata):
        if not isinstance(container, dict):
            continue
        for key in _HASH_KEYS:
            val = container.get(key)
            if isinstance(val, str) and val:
                return val
    return None


def _is_tracked_relpath(rel: str) -> bool:
    """Return True if the relative path is a repo file worth tracking."""
    rel = rel.replace("\\", "/")
    if not rel or rel.startswith((".", "/")):
        return False
    return not rel.startswith(_IGNORED_DIR_PREFIXES)


def derive_tracked_paths(audit_path: str | Path | None = None) -> list[Path]:
    """Build the set of tracked files from the audit ledger.

    A file is tracked if the ledger contains at least one write event
    (an ``after_hash``/``sha256``) referencing it. Returns resolved,
    absolute ``Path`` objects (relative to the project root).
    """
    project_root = get_project_root()
    tracked: dict[Path, str] = {}

    try:
        events = AuditReader(str(audit_path or get_audit_path())).read_all()
    except Exception:  # noqa: BLE001 - best-effort; caller reports failure
        logger.exception("Unable to read audit trail for drift sweep")
        return []

    for event in events:
        after = _event_after_hash(event)
        if not after:
            continue
        rel = _event_path(event)
        if not rel or not _is_tracked_relpath(rel):
            continue
        # Keep the *latest* recorded after_hash per path.
        tracked[project_root / rel] = after

    return list(tracked.keys())


def run_sweep(
    tracked_paths: list[Path] | None = None,
    audit_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run the drift sweep and return a report.

    Args:
        tracked_paths: Optional explicit list of paths to check. When
            omitted, derived from the audit ledger via
            :func:`derive_tracked_paths`.
        audit_path: Optional override for the audit JSONL file.

    Returns:
        A dict with:
            - ``total_checked``: number of tracked files examined
            - ``mismatches``: list of ``{path, expected_digest, actual_digest}``
            - ``unrecorded``: list of tracks with no audit record (informational)
            - ``audit_entries``: number of audit events read
    """
    project_root = get_project_root()
    if tracked_paths is None:
        tracked_paths = derive_tracked_paths(audit_path)

    try:
        events = AuditReader(str(audit_path or get_audit_path())).read_all()
    except Exception:  # noqa: BLE001 - best-effort
        logger.exception("Unable to read audit trail for drift sweep")
        events = []
    audit_entries = len(events)

    # Build the latest recorded after_hash per resolved path.
    latest: dict[Path, str] = {}
    for event in events:
        after = _event_after_hash(event)
        if not after:
            continue
        rel = _event_path(event)
        if not rel:
            continue
        candidate = Path(rel)
        if not candidate.is_absolute():
            candidate = project_root / candidate
        latest[candidate.resolve()] = after

    mismatches: list[dict[str, str]] = []
    unrecorded: list[dict[str, str]] = []
    checked = 0

    for path in tracked_paths:
        resolved = path.resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists() or resolved.is_dir():
            continue
        checked += 1
        actual = compute_digest(resolved)
        expected = latest.get(resolved)
        if expected is None:
            unrecorded.append(
                {
                    "path": str(resolved),
                    "actual_digest": actual or "(file read error)",
                }
            )
        elif actual != expected:
            mismatches.append(
                {
                    "path": str(resolved),
                    "expected_digest": expected,
                    "actual_digest": actual or "(file read error)",
                }
            )

    return {
        "total_checked": checked,
        "mismatches": mismatches,
        "unrecorded": unrecorded,
        "audit_entries": audit_entries,
    }
