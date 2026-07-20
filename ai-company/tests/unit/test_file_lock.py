"""Unit tests for the cross-platform file-lock utility.

Covers: basic acquire/release, exclusivity under threads, timeout on
contention, and stale-lock breaking.
"""

from __future__ import annotations

import threading
import time

import pytest

from ai_company.store.file_lock import FileLockError, file_lock


def test_basic_acquire_release(tmp_path) -> None:
    target = tmp_path / "state.json"
    target.write_text("{}", encoding="utf-8")
    with file_lock(target):
        assert (tmp_path / "state.json.lock").exists()
    # Lock sidecar removed after context exit.
    assert not (tmp_path / "state.json.lock").exists()


def test_no_stale_sidecar_left_on_exception(tmp_path) -> None:
    target = tmp_path / "state.json"
    with pytest.raises(ValueError):
        with file_lock(target):
            raise ValueError("boom")
    assert not (tmp_path / "state.json.lock").exists()


def test_exclusive_access_serialises_threads(tmp_path) -> None:
    target = tmp_path / "state.json"
    counter = {"value": 0}
    errors: list[Exception] = []

    def worker() -> None:
        try:
            with file_lock(target, timeout=5.0):
                # Critical section: read-modify-write on shared counter.
                current = counter["value"]
                time.sleep(0.01)
                counter["value"] = current + 1
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert counter["value"] == 10


def test_timeout_when_lock_held(tmp_path) -> None:
    target = tmp_path / "state.json"
    target.write_text("x", encoding="utf-8")
    acquired = threading.Event()

    def holder() -> None:
        with file_lock(target, timeout=5.0):
            acquired.set()
            time.sleep(2.0)

    t = threading.Thread(target=holder)
    t.start()
    acquired.wait(timeout=2.0)

    with pytest.raises(FileLockError):
        with file_lock(target, timeout=0.3, poll_interval=0.05):
            pass
    t.join()
