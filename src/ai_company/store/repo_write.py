"""Guarded repository-file write primitive.

P0 protection against concurrent-session conflicts and silent/unauthorised
overwrites of *agent-authored* files (source, docs, generated agents,
``company/*.yaml``).  These files are currently written via bare
``path.write_text()`` with no lock, no optimistic concurrency and no
ownership — so two concurrent sessions can silently clobber each other.

This module provides a single guarded write path that:

* Acquires the repo's cross-process sidecar lock (``store.file_lock``).
* Optionally enforces **optimistic concurrency** (CAS) on a caller-supplied
  expected content digest — the write is refused with ``conflict=True`` if
  the on-disk content differs from what the caller read.
* Optionally enforces **ownership**: a write to a file claimed by a
  *different active* owner is hard-rejected (``owner_conflict=True``); the
  claimant may always write its own files.
* Writes atomically (temp-then-rename) and snapshots a ``.bak``.
* Returns ``before_hash``/``after_hash`` so callers can record content
  digests in the audit trail (turning silent clobbers into provable events).

ToolRunner, the agent generator, and the CLI imperative stores all funnel
their writes through :func:`write_file`, so all of them inherit lock + CAS +
ownership coverage through one code path.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

from ai_company.store.file_lock import file_lock

logger = logging.getLogger(__name__)

_LOCK_TIMEOUT = 10.0
_LOCK_STALE_AFTER = 30.0


class RepoWriteConflict(Exception):
    """Raised when an optimistic-concurrency write hits a stale expected digest.

    The on-disk content changed since the caller read it.  Callers should
    re-read (or resolve the conflict) rather than overwrite.
    """

    def __init__(self, path: Path, expected: str, actual: str) -> None:
        self.path = path
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"Content of {path} changed since read (expected {expected[:12]}, "
            f"found {actual[:12]}); refusing overwrite."
        )


class RepoWriteOwnerConflict(Exception):
    """Raised when a write targets a file claimed by a different active owner."""

    def __init__(self, path: Path, owner: object) -> None:
        self.path = path
        self.owner = owner
        super().__init__(
            f"File {path} is claimed by another active owner ({owner}); refusing overwrite."
        )


def sha256_digest(path: str | Path) -> str | None:
    """Return the SHA-256 hex digest of *path*'s bytes, or ``None`` if missing.

    An owner/lease registry can store this digest to detect and prove silent
    overwrites.  ``None`` means the file does not exist yet (e.g. a create).
    """
    p = Path(path)
    if not p.exists():
        return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_file(path: str | Path) -> tuple[str | None, str | None]:
    """Read *path* and return ``(content, digest)``.

    ``content`` is ``None`` if the file does not exist; ``digest`` is
    ``None`` for a missing file.  Callers use *digest* as the
    ``expected_digest`` for a later :func:`write_file` to get CAS protection.
    """
    p = Path(path)
    if not p.exists():
        return None, None
    content = p.read_text(encoding="utf-8")
    return content, sha256_digest(p)


def write_file(
    path: str | Path,
    content: str,
    *,
    expected_digest: str | None = None,
    owner: Any = None,
    claimed_by_owner: bool = True,
) -> dict[str, Any]:
    """Write *content* to *path* with lock + optional CAS and ownership checks.

    Args:
        path: Target file (created if missing).
        content: Text to write.
        expected_digest: If provided, the write is refused (409 / conflict)
            when the on-disk content's digest differs.  Pass the digest from
            :func:`read_file` to get optimistic-concurrency protection.
        owner: Identity of the writer (e.g. task/session id).  When set, the
            caller asserts it owns *path*; an ownership registry hook is
            consulted to refuse writing files claimed by a different active
            owner.  See :func:`set_owner_registry`.
        claimed_by_owner: When ``True`` (default), a successful write does
            not itself assert global ownership — used by the ToolRunner which
            manages the claim registry.  Callers that manage ownership at a
            higher level can set this to ``False``.

    Returns:
        A dict::

            {
                "path": str,
                "before_hash": str | None,
                "after_hash": str,
                "conflict": bool,
                "owner_conflict": bool,
            }

        ``conflict`` is ``True`` when the expected digest did not match (the
        file was NOT written).  ``owner_conflict`` is ``True`` when a
        different active owner holds the file (the file was NOT written).
        On either conflict the target file is left untouched.

    Raises:
        RepoWriteConflict: If ``expected_digest`` mismatches (callers using
            the exception API) — alternate to checking ``conflict``.
        FileLockError: If the cross-process lock cannot be acquired.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    lock_resource = target  # sidecar becomes <name>.lock

    with file_lock(lock_resource, timeout=_LOCK_TIMEOUT, stale_after=_LOCK_STALE_AFTER):
        current_digest = sha256_digest(target)

        # Ownership check — refuse if another active owner holds the file.
        if owner is not None and claimed_by_owner:
            owner_conflict = _claim_check(target, owner)
            if owner_conflict:
                return {
                    "path": str(target),
                    "before_hash": current_digest,
                    "after_hash": current_digest,
                    "conflict": False,
                    "owner_conflict": True,
                }

        # Optimistic concurrency — refuse if content changed since read.
        if expected_digest is not None and current_digest != expected_digest:
            raise RepoWriteConflict(target, expected_digest, current_digest or "<missing>")

        _atomic_write_with_backup(target, content)
        after_digest = sha256_digest(target)

        return {
            "path": str(target),
            "before_hash": current_digest,
            "after_hash": after_digest,
            "conflict": False,
            "owner_conflict": False,
        }


def _atomic_write_with_backup(path: Path, content: str) -> None:
    """Atomically write *content* to *path*, snapshotting a ``.bak`` first.

    Mirrors ``FileStore._write_content`` semantics so the last good version
    survives a crash mid-replace.
    """
    from ai_company.utils.file_lock import atomic_write

    if path.exists():
        _copy_backup(path)

    with atomic_write(path) as fh:
        fh.write(content)

    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        _copy_backup(path)


def _copy_backup(path: Path) -> None:
    """Copy *path*'s current bytes to its ``.bak`` sibling."""
    bak = path.with_suffix(path.suffix + ".bak")
    try:
        data = path.read_bytes()
        bak.write_bytes(data)
    except OSError:  # pragma: no cover - best-effort backup
        logger.warning("Failed to write backup for %s", path)


# ---------------------------------------------------------------------------
# Ownership registry (advisory, consumed by ToolRunner / lease).
# ---------------------------------------------------------------------------
#
# ``write_file`` consults an optional in-process callback before writing when
# an ``owner`` is supplied.  The ToolRunner wires this to the task-lease
# ``claimed_files`` registry so a write to a file claimed by a *different
# active* task is hard-rejected.  Default: no registry => no ownership
# enforcement (single-owner paths such as the generator).

_owner_check: Any = None


def set_owner_registry(check: Any) -> None:
    """Install a ``callable(path, owner) -> bool`` ownership guard.

    Return ``True`` to *deny* the write (owner conflict).  ``None`` disables
    the guard (default: no ownership enforcement).
    """
    global _owner_check
    _owner_check = check


def _claim_check(path: Path, owner: Any) -> bool:
    """Return True if a different active owner holds *path* (deny write)."""
    if _owner_check is None:
        return False
    try:
        return bool(_owner_check(path, owner))
    except Exception:  # noqa: BLE001 - a registry failure must not corrupt data
        logger.exception("Ownership registry check failed for %s", path)
        return False
