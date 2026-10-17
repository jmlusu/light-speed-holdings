"""Tests for the token-bucket rate limiter."""

from __future__ import annotations

import time

from ai_company.llm.token_bucket import TokenBucket


def test_try_acquire_consumes_capacity() -> None:
    bucket = TokenBucket(rate=10.0, capacity=3)
    assert bucket.try_acquire()
    assert bucket.try_acquire()
    assert bucket.try_acquire()
    assert not bucket.try_acquire()


def test_acquire_blocks_until_refill() -> None:
    bucket = TokenBucket(rate=100.0, capacity=1)
    assert bucket.try_acquire()
    start = time.monotonic()
    assert bucket.acquire(timeout=1.0)
    elapsed = time.monotonic() - start
    assert elapsed < 0.5


def test_acquire_times_out_when_empty() -> None:
    bucket = TokenBucket(rate=0.0, capacity=0)
    start = time.monotonic()
    assert not bucket.acquire(timeout=0.1)
    assert time.monotonic() - start >= 0.1


def test_try_acquire_non_blocking_when_empty() -> None:
    bucket = TokenBucket(rate=0.0, capacity=0)
    start = time.monotonic()
    assert not bucket.acquire(timeout=0.0)
    assert time.monotonic() - start < 0.1


def test_refill_restores_tokens_over_time() -> None:
    bucket = TokenBucket(rate=10.0, capacity=5)
    for _ in range(5):
        assert bucket.try_acquire()
    assert not bucket.try_acquire()
    time.sleep(0.3)
    assert bucket.try_acquire()


def test_burst_capped_at_capacity() -> None:
    bucket = TokenBucket(rate=1000.0, capacity=2)
    assert bucket.try_acquire()
    assert bucket.try_acquire()
    assert not bucket.try_acquire()
