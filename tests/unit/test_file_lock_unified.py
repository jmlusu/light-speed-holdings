"""Regression tests for the unified file-lock implementation.

``ai_company.utils.file_lock`` now delegates its locking to the canonical
:mod:`ai_company.store.file_lock` implementation.  These tests ensure the two
entry points serialize/conflict on the SAME resource path (i.e. they share one
backing lock), and that ``atomic_write`` from the utils module still works.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

from ai_company.store.file_lock import FileLockError as StoreFileLockError
from ai_company.store.file_lock import file_lock as store_file_lock
from ai_company.utils.file_lock import atomic_write, file_lock


def test_utils_and_store_lock_share_same_resource(tmp_path: Path) -> None:
    """Acquiring via one entry point is blocked while the other holds it.

    Both ``utils.file_lock.file_lock`` and ``store.file_lock.file_lock`` must
    contend on the same ``.lock`` sidecar for the same resource path, proving
    there is a single canonical backing implementation.
    """
    target = tmp_path / "state.json"
    acquired = threading.Event()
    errors: list[Exception] = []

    def holder() -> None:
        try:
            # Hold via the utils wrapper.
            with file_lock(target, timeout=5.0):
                acquired.set()
                time.sleep(1.5)
        except Exception as exc:  # pragma: no cover - defensive; # noqa: BLE001
            errors.append(exc)

    t = threading.Thread(target=holder)
    t.start()
    assert acquired.wait(timeout=2.0), "holder never acquired the lock"

    # While the utils wrapper holds it, the store entry point MUST time out.
    with (
        pytest.raises(StoreFileLockError),
        store_file_lock(target, timeout=0.3, poll_interval=0.05),
    ):
        pass
    t.join()
    assert not errors

    # After release, the store entry point can acquire normally.
    with store_file_lock(target, timeout=2.0):
        pass


def test_utils_lock_timeout_matches_store(tmp_path: Path) -> None:
    """The utils wrapper raises the canonical FileLockError on timeout."""
    target = tmp_path / "state.json"
    # The outer lock is held while the inner one (same resource) times out,
    # surfacing the canonical FileLockError raised by the unified backing lock.
    with (
        file_lock(target, timeout=5.0),
        pytest.raises(StoreFileLockError),
        file_lock(target, timeout=0.3, poll_interval=0.05),
    ):
        pass


def test_atomic_write_still_functions(tmp_path: Path) -> None:
    """``atomic_write`` is preserved in utils and still writes atomically."""
    target = tmp_path / "state.json"
    with file_lock(target), atomic_write(target) as f:
        f.write('{"a": 1}')
    assert target.read_text(encoding="utf-8") == '{"a": 1}'
    # No temp residue remains.
    assert list(tmp_path.glob(".state*.tmp")) == []
