"""Unit tests for ResponseCache — file-based LLM response caching."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from ai_company.llm.response_cache import ResponseCache


class TestResponseCache:
    """Cache hit/miss and TTL behavior."""

    def test_miss_on_empty_cache(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache")
        result = cache.get("sys", "usr", "model-a", 0.0)
        assert result is None

    def test_set_and_get(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache")
        cache.set("sys", "usr", "model-a", 0.0, "hello", tokens_used=100, cost_usd=0.001)
        hit = cache.get("sys", "usr", "model-a", 0.0)
        assert hit is not None
        assert hit.content == "hello"
        assert hit.tokens_saved == 100
        assert hit.cost_saved == pytest.approx(0.001)

    def test_miss_on_different_model(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache")
        cache.set("sys", "usr", "model-a", 0.0, "hello")
        assert cache.get("sys", "usr", "model-b", 0.0) is None

    def test_miss_on_different_temperature(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache")
        cache.set("sys", "usr", "model-a", 0.0, "hello")
        assert cache.get("sys", "usr", "model-a", 0.7) is None

    def test_ttl_expiry(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache", ttl_seconds=1)
        cache.set("sys", "usr", "model-a", 0.0, "hello")
        # Manually backdate the file mtime to simulate expiry.
        cached_file = list((tmp_path / "cache").glob("*.json"))[0]
        old_time = time.time() - 10
        cached_file.touch()
        import os

        os.utime(cached_file, (old_time, old_time))
        assert cache.get("sys", "usr", "model-a", 0.0) is None

    def test_clear(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache")
        cache.set("s1", "u1", "m", 0.0, "a")
        cache.set("s2", "u2", "m", 0.0, "b")
        removed = cache.clear()
        assert removed == 2
        assert cache.get("s1", "u1", "m", 0.0) is None

    def test_eviction_under_size_pressure(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache", max_size_mb=0.001)  # ~1KB
        # Write several entries to exceed the limit.
        for i in range(10):
            cache.set(f"sys{i}", f"usr{i}", "m", 0.0, f"content-{i}" * 50)
        files = list((tmp_path / "cache").glob("*.json"))
        # Some entries should have been evicted.
        assert len(files) < 10

    def test_stats(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache")
        assert cache.stats["entries"] == 0
        cache.set("s", "u", "m", 0.0, "x")
        assert cache.stats["entries"] == 1

    def test_corrupt_cache_file_returns_none(self, tmp_path: Path) -> None:
        cache = ResponseCache(cache_dir=tmp_path / "cache")
        cache.set("sys", "usr", "model-a", 0.0, "hello")
        cached_file = list((tmp_path / "cache").glob("*.json"))[0]
        cached_file.write_text("NOT JSON", encoding="utf-8")
        assert cache.get("sys", "usr", "model-a", 0.0) is None
