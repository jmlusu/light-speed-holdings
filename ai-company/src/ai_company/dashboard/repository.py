"""Centralized state repository for dashboard file I/O (GAP-011 fix).

The dashboard API modules previously performed raw ``open()`` / ``read_text()``
calls scattered across ``api.py``, ``mobile_api.py`` and ``monitoring.py``.
This module introduces a single thin repository — :class:`StateStore` — that
wraps all reads and writes of shared JSON/YAML state (inbox, approvals,
escalations, registry, scheduler, cost tracker, KPI snapshots, device
store, audit log) through the existing atomic :class:`FileStore` abstraction.

Design goals (per task brief — minimal, do NOT rewrite the dashboard):

* Centralize every raw ``open()``/``read_text()`` call behind one layer.
* Use the existing :class:`ai_company.store.file_store.FileStore` for atomic,
  lock-safe persistence (no new dependencies).
* Reject unknown / forbidden paths so a caller cannot read or write an
  arbitrary filesystem location (defence-in-depth on top of GAP-010 authz).
* Keep the public surface small: ``read_json``, ``write_json``,
  ``read_yaml``, ``write_yaml``, ``read_text``, ``exists``.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

# ── Allowlist of state files the dashboard may touch ──────────────────
# Paths are stored relative to the project root (``base_dir``).  Anything
# not in this set is rejected, closing the "forbidden path" gap that raw
# ``open()`` calls left open.
_ALLOWED_REL_PATHS: frozenset[str] = frozenset(
    {
        # Task inbox
        ".opencode/inbox.json",
        # Approval / escalation / scheduler / device stores
        "orchestrator/approvals.yaml",
        "orchestrator/escalation.yaml",
        "orchestrator/scheduler.yaml",
        "orchestrator/devices.yaml",
        # Agent registry & company config
        "company/agent-registry.json",
        "company/departments.yaml",
        "company/models.yaml",
        "company/config/kpis.yaml",
        # Cost & analytics
        "orchestrator/cost_tracker.json",
        # Audit log (read-only usage by dashboard metrics)
        ".opencode/audit.jsonl",
        # Dead-letter queue (read-only health checks)
        ".opencode/dead_letter_queue.json",
        # KPI snapshot directory — prefix match handled separately
    }
)

# Directory prefixes that are permitted (for globbed snapshot reads).
_ALLOWED_PREFIXES: tuple[str, ...] = (
    "orchestrator/kpi_snapshots/",
    "memory/",
)


class StateStoreError(Exception):
    """Raised when a path is not permitted by the :class:`StateStore`."""


class StateStore:
    """Single source of truth for dashboard state I/O.

    Wraps :class:`FileStore` and restricts access to an allowlist of known
    state files.  All JSON/YAML reads and writes from the dashboard API
    should go through this class instead of raw ``open()``.

    Args:
        base_dir: Project root that relative state paths are resolved against.
        backup: Whether to create ``.bak`` copies on write (delegated to
            :class:`FileStore`).
    """

    def __init__(self, base_dir: str | Path = ".", backup: bool = True) -> None:
        # Keep base un-resolved so the store follows the current working
        # directory at call time (important for tests that chdir and for
        # runtime behaviour where the dashboard is launched from the repo
        # root). Absolute paths are still honoured.
        self._base = Path(base_dir)
        self._store = FileStore(self._base, backup=backup)

    # ── Path validation ──────────────────────────────────────────────

    def _resolve(self, rel_path: str | Path) -> tuple[Path, str]:
        """Resolve *rel_path* and ensure it is on the allowlist.

        Returns:
            A tuple of ``(candidate, rel)`` where *candidate* is the absolute
            resolved path and *rel* is the POSIX-style relative path used by
            :class:`FileStore`.

        Raises:
            StateStoreError: If the path is not an allowed state file.
        """
        try:
            candidate = (self._base / rel_path).resolve()
            rel = str(candidate.relative_to(self._base.resolve())).replace("\\", "/")
        except ValueError:
            # Path escapes base_dir (e.g. "../secrets.json") — not permitted.
            raise StateStoreError(f"Path not permitted by StateStore: {rel_path}")

        if rel in _ALLOWED_REL_PATHS:
            return candidate, rel

        # Allow directory-prefix matches (e.g. snapshot globs).
        if any(
            rel == p.rstrip("/") or rel.startswith(p) for p in _ALLOWED_PREFIXES
        ):
            return candidate, rel

        raise StateStoreError(f"Path not permitted by StateStore: {rel}")

    # ── Existence ────────────────────────────────────────────────────

    def exists(self, rel_path: str | Path) -> bool:
        """Return True if the (permitted) path exists."""
        try:
            path, _ = self._resolve(rel_path)
        except StateStoreError:
            return False
        return path.exists()

    # ── JSON helpers ─────────────────────────────────────────────────

    def read_json(self, rel_path: str | Path, default: Any = None) -> Any:
        """Read and parse a JSON file. Returns *default* (``[]`` for json
        by convention) when missing or invalid.

        ``default`` is configurable so callers that historically returned
        ``[]`` for missing JSON or ``{}`` for missing YAML keep working.
        """
        path, rel = self._resolve(rel_path)
        if not path.exists():
            return [] if str(path).endswith("json") else default
        data = self._store.read_json(rel)
        return data if data is not None else default

    def write_json(self, rel_path: str | Path, data: Any) -> None:
        """Atomically write *data* as JSON to a permitted path."""
        _, rel = self._resolve(rel_path)
        self._store.write_json(rel, data)

    # ── YAML helpers ─────────────────────────────────────────────────

    def read_yaml(self, rel_path: str | Path, default: Any = None) -> Any:
        """Read and parse a YAML file. Returns *default* (``{}``) when
        missing or invalid.
        """
        path, rel = self._resolve(rel_path)
        if not path.exists():
            return default
        data = self._store.read_yaml(rel)
        return data if data is not None else default

    def write_yaml(self, rel_path: str | Path, data: Any) -> None:
        """Atomically write *data* as YAML to a permitted path."""
        _, rel = self._resolve(rel_path)
        self._store.write_yaml(rel, data)

    # ── Raw text (audit log lines, etc.) ─────────────────────────────

    def read_text(self, rel_path: str | Path) -> str:
        """Read a file as text. Returns ``""`` when missing."""
        path, _ = self._resolve(rel_path)
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    def read_lines(self, rel_path: str | Path) -> list[str]:
        """Read a text file as a list of stripped non-empty lines."""
        text = self.read_text(rel_path)
        return [ln.strip() for ln in text.splitlines() if ln.strip()]

    # ── Read-only JSON parsing helper for audit-style JSONL ──────────

    def iter_jsonl(self, rel_path: str | Path):
        """Yield parsed dicts from a JSONL file, skipping bad lines."""
        for line in self.read_lines(rel_path):
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

    # ── Snapshot directory (KPI trend globs) ───────────────────────

    def list_snapshot_files(self, pattern: str = "snapshot-*.json") -> list[Path]:
        """List KPI snapshot files (within the allowed prefix only)."""
        snap_dir, _ = self._resolve("orchestrator/kpi_snapshots")
        if not snap_dir.exists():
            return []
        return sorted(snap_dir.glob(pattern))

    def read_snapshot(self, path: Path) -> Any:
        """Read a single KPI snapshot JSON file (must live in the allowed
        snapshot prefix)."""
        rel = str(path.resolve().relative_to(self._base)).replace("\\", "/")
        if not rel.startswith("orchestrator/kpi_snapshots/"):
            raise StateStoreError(f"Path not permitted by StateStore: {rel}")
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None


# ── Module-level singleton ─────────────────────────────────────────────
#
# Option B (explicit config): the singleton is bound explicitly via
# :func:`configure_state_store` at server boot from an env/config value
# (``DASHBOARD_DATA_DIR``). :func:`get_state_store` returns that configured
# store for the lifetime of the process and does NOT re-point at a new root
# when the cwd changes. If never configured, it lazily defaults to "."
# so import-time callers and tests keep working.

_default_store: StateStore | None = None


def configure_state_store(base_dir: str | Path) -> StateStore:
    """Explicitly bind the shared :class:`StateStore` to *base_dir*.

    Call this exactly once at dashboard server boot (e.g. from
    :func:`ai_company.dashboard.app.create_app`) so the store root is set
    from configuration rather than the import-time cwd. Subsequent calls
    re-bind the singleton to a new root (used by tests).

    Returns:
        The newly configured :class:`StateStore`.
    """
    global _default_store
    _default_store = StateStore(base_dir)
    logger.info("StateStore configured with base_dir=%s", _default_store._base)
    return _default_store


def is_state_store_configured() -> bool:
    """Return True if :func:`configure_state_store` has been called."""
    return _default_store is not None


def get_state_store(base_dir: str | Path = ".") -> StateStore:
    """Return the shared, explicitly-configured :class:`StateStore`.

    The store is bound once for the process lifetime via
    :func:`configure_state_store`. If it has not been configured yet this
    returns a lazily-created default rooted at *base_dir* (``"."``) so that
    import-time callers and legacy/test code continue to work without an
    explicit boot step. The base is resolved at construction time, so the
    store is immune to later ``chdir()`` calls.
    """
    global _default_store
    if _default_store is None:
        _default_store = StateStore(base_dir)
    return _default_store


def reset_state_store() -> None:
    """Reset the module-level singleton (used by tests)."""
    global _default_store
    _default_store = None
