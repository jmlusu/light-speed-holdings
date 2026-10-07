"""Deterministic project-root and data-root resolution.

The dashboard and its KPI collectors historically resolved the project root
relative to the process working directory (``Path(__file__).resolve().parents[3]``
or ``"."``), which made real operational data invisible depending on where the
server was launched.  This module is the single source of truth for resolving
the ``ai-company`` project root and the runtime data root.

Resolution order for the project root:

1. ``AI_COMPANY_ROOT`` environment variable (explicit override).
2. The nearest ancestor of this package containing a project marker
   (``company-registry.yaml`` or ``pyproject.toml``).
3. The current working directory (last-resort fallback).

The data root defaults to the project root and can be overridden with
``DASHBOARD_DATA_DIR`` for deployments that keep runtime state elsewhere.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

AI_COMPANY_ROOT_ENV = "AI_COMPANY_ROOT"
DASHBOARD_DATA_DIR_ENV = "DASHBOARD_DATA_DIR"

logger = logging.getLogger(__name__)

# Files that uniquely identify the ai-company project root.  The package tree
# walks upward until one of these is found.
_PROJECT_MARKERS = ("company-registry.yaml", "pyproject.toml")


def get_project_root() -> Path:
    """Return the ai-company project root, independent of the CWD.

    Honour ``AI_COMPANY_ROOT`` when set, then walk up from this package looking
    for a project marker, finally falling back to the current working directory.
    """
    env_root = os.environ.get(AI_COMPANY_ROOT_ENV)
    if env_root:
        return Path(env_root).resolve()

    pkg = Path(__file__).resolve().parent
    for candidate in (pkg, *pkg.parents):
        if any((candidate / marker).is_file() for marker in _PROJECT_MARKERS):
            return candidate

    return Path.cwd().resolve()


def get_data_root() -> Path:
    """Return the root that runtime data files live under.

    Defaults to :func:`get_project_root`; override with ``DASHBOARD_DATA_DIR``.
    """
    data_dir = os.environ.get(DASHBOARD_DATA_DIR_ENV)
    if data_dir:
        return Path(data_dir).resolve()
    return get_project_root()


def get_database_path() -> Path:
    """Return the canonical SQLite database path for the data root.

    Anchored at ``data/ai_company.db`` under :func:`get_data_root` so the
    dashboard and the ``backfill`` CLI always share one database regardless
    of the CWD.
    """
    return get_data_root() / "data" / "ai_company.db"


# Legacy runtime-state prefix (D-6) and its relocated home under ``data/``.
LEGACY_STATE_PREFIX = "orchestrator/"
STATE_PREFIX = "data/orchestrator/"


def _migrate_legacy_state(legacy: Path, target: Path) -> bool:
    """Move a legacy ``orchestrator/`` state tree under ``data/orchestrator/``.

    Called opportunistically by :func:`state_path` so existing deployments
    self-migrate on first access. Returns True when it is safe to use the
    relocated path (target exists, migration succeeded, or neither tree
    exists yet) and False when the legacy tree could not be moved (e.g. a
    running daemon holds file locks) — the caller then keeps using the
    legacy location so nothing breaks mid-flight.
    """
    try:
        if not legacy.is_dir():
            return True
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            legacy.rename(target)
            logger.info("Migrated runtime state %s -> %s", legacy, target)
            return True
        # Both trees exist: merge legacy-only entries, leave collisions at the
        # target. If any child cannot move (lock/cross-mount), roll back
        # everything already moved so the legacy tree stays the complete
        # fallback for the False return below.
        moved: list[tuple[Path, Path]] = []
        try:
            for child in legacy.iterdir():
                dest = target / child.name
                if dest.exists():
                    continue
                child.rename(dest)
                moved.append((child, dest))
        except OSError as exc:
            for child, dest in reversed(moved):
                try:
                    dest.rename(child)
                except OSError as rollback_exc:  # pragma: no cover - lock race
                    logger.warning("Rollback of %s failed: %s", dest, rollback_exc)
            logger.warning(
                "Runtime-state merge into %s failed (%s); using legacy path",
                target,
                exc,
            )
            return False
        try:
            legacy.rmdir()  # only succeeds when fully drained
        except OSError:
            logger.warning("Legacy state directory not empty, left in place: %s", legacy)
        return True
    except OSError as exc:
        logger.warning(
            "Runtime-state migration %s -> %s failed (%s); using legacy path",
            legacy,
            target,
            exc,
        )
        return False


def state_path(rel: str | Path, base: str | Path = ".") -> str | Path:
    """Return the post-D-6 location of a runtime-state path under *base*.

    ``orchestrator/...`` inputs map to ``data/orchestrator/...``; paths that
    already start with ``data/orchestrator/`` are returned unchanged
    (idempotent). Every other relative path and every absolute path passes
    through untouched, preserving the input type (``str`` in → ``str`` out,
    ``Path`` in → ``Path`` out).

    On first use the legacy ``orchestrator/`` tree under *base* is renamed
    into ``data/orchestrator/`` (self-migration). If that fails — e.g. a
    running daemon still holds the files open on Windows — the legacy path
    is returned instead so callers keep working against the old location.
    """
    in_is_path = isinstance(rel, Path)
    raw = os.fspath(rel)
    if Path(raw).is_absolute():
        return rel
    norm = raw.replace("\\", "/")
    if norm == "orchestrator" or norm == STATE_PREFIX.rstrip("/"):
        suffix = ""
    elif norm.startswith(LEGACY_STATE_PREFIX):
        suffix = norm[len(LEGACY_STATE_PREFIX) :]
    elif norm.startswith(STATE_PREFIX):
        suffix = norm[len(STATE_PREFIX) :]
    else:
        return rel
    legacy_form = LEGACY_STATE_PREFIX + suffix
    mapped = STATE_PREFIX + suffix
    base_path = Path(base)
    if not _migrate_legacy_state(base_path / "orchestrator", base_path / "data" / "orchestrator"):
        # Degraded (e.g. a running daemon holds the files): keep using the
        # legacy tree so reads and writes still hit the live data.
        return Path(legacy_form) if in_is_path else legacy_form
    return Path(mapped) if in_is_path else mapped


# Canonical audit trail location, relative to the data root. The audit trail
# is a single JSONL file (not a directory) named ``audit`` — historically the
# executor wrote to ``<data root>/.opencode/audit`` while several defaults
# read ``.opencode/audit.jsonl`` (an empty decoy file, ticket #59). All audit
# entry points resolve through :func:`get_audit_path` so they cannot drift
# apart again.
AUDIT_RELATIVE_PATH = Path(".opencode") / "audit"


def get_audit_path() -> Path:
    """Return the canonical audit trail path.

    The audit trail is one JSONL file at ``<data root>/.opencode/audit``.
    AuditWriter, AuditReader and ``init_audit`` all resolve to this path by
    default so event emission and evidence capture always target the same
    file.
    """
    return get_data_root() / AUDIT_RELATIVE_PATH


__all__ = [
    "AI_COMPANY_ROOT_ENV",
    "AUDIT_RELATIVE_PATH",
    "DASHBOARD_DATA_DIR_ENV",
    "LEGACY_STATE_PREFIX",
    "STATE_PREFIX",
    "get_audit_path",
    "get_data_root",
    "get_database_path",
    "get_project_root",
    "state_path",
]
