"""Unit tests for reliability timeout/bulkhead primitives."""

from __future__ import annotations

import time

import pytest

from ai_company.reliability.timeout import Bulkhead, call_with_timeout


def test_call_with_timeout_returns_result() -> None:
    assert call_with_timeout(lambda: 42, timeout_s=1.0) == 42


def test_call_with_timeout_raises_on_deadline_exceeded() -> None:
    def slow() -> int:
        time.sleep(0.4)
        return 1

    with pytest.raises(TimeoutError):
        call_with_timeout(slow, timeout_s=0.05)


def test_call_with_timeout_does_not_wait_for_hung_worker() -> None:
    started = time.monotonic()

    def hang() -> int:
        time.sleep(30.0)
        return 1

    with pytest.raises(TimeoutError):
        call_with_timeout(hang, timeout_s=0.05)
    assert time.monotonic() - started < 2.0


def test_bulkhead_call_returns_result() -> None:
    bulkhead = Bulkhead(max_workers=2)
    try:
        assert bulkhead.call(lambda: "ok", timeout_s=1.0) == "ok"
    finally:
        bulkhead.shutdown(wait=False)


def test_bulkhead_call_raises_on_timeout() -> None:
    bulkhead = Bulkhead(max_workers=1)
    try:
        with pytest.raises(TimeoutError):
            bulkhead.call(lambda: time.sleep(30.0), timeout_s=0.05)
    finally:
        bulkhead.shutdown(wait=False)


def test_bulkhead_bounds_concurrency() -> None:
    running: list[bool] = []
    started: list[int] = []

    def worker(flag: list[bool], serial: int) -> None:
        flag.append(True)
        started.append(serial)
        time.sleep(0.15)
        flag.pop()

    bulkhead = Bulkhead(max_workers=2, queue_cap=10)
    try:
        futures = [bulkhead.submit(worker, running, i) for i in range(4)]
        time.sleep(0.2)
        assert len(running) <= 2
        for future in futures:
            future.result(timeout=1.0)
        assert len(started) == 4
    finally:
        bulkhead.shutdown()


def test_bulkhead_drops_oldest_unstarted_call_when_queue_full() -> None:
    """A queued (not yet started) call is shed before an in-flight one."""
    bulkhead = Bulkhead(max_workers=1, queue_cap=2)
    try:
        first = bulkhead.submit(lambda: time.sleep(30.0))  # occupies the worker
        time.sleep(0.05)
        second = bulkhead.submit(lambda: 2)  # queued behind it
        third = bulkhead.submit(lambda: 3)  # queue full -> drops *second*
        assert second.cancelled()
        assert not first.cancelled()
        assert not third.cancelled()
    finally:
        bulkhead.shutdown(wait=False)


def test_submit_after_shutdown_raises() -> None:
    bulkhead = Bulkhead(max_workers=1)
    bulkhead.shutdown(wait=False)
    with pytest.raises(RuntimeError):
        bulkhead.submit(lambda: 1)
