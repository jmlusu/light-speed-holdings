"""Tests for the session read-dedup skeleton (P1-3 hot-file storm)."""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from ai_company.executor.read_cache import SessionReadCache


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


class TestSessionReadCache:
    def test_miss_then_hit(self, tmp_path: Path) -> None:
        cache = SessionReadCache()
        f = tmp_path / "AGENTS.md"
        _write(f, "hello")
        assert cache.get(str(f), step=1) is None
        cache.put(str(f), "hello", step=1)
        hit = cache.get(str(f), step=2)
        assert hit is not None
        assert hit.path == str(f.resolve())
        assert hit.ref_step == 1
        pointer = hit.pointer()
        assert pointer["cached"] is True
        assert "unchanged since step 1" in str(pointer["note"])

    def test_mtime_change_misses(self, tmp_path: Path) -> None:
        cache = SessionReadCache()
        f = tmp_path / "notes.txt"
        _write(f, "version one content with padding to ensure size changes cleanly")
        cache.put(str(f), f.read_text(encoding="utf-8"), step=1)
        assert cache.get(str(f), step=2) is not None
        # Rewrite with different size; force a distinct mtime.
        _write(f, "version two -- different length payload altogether")
        os.utime(f, (time.time() + 2, time.time() + 2))
        assert cache.get(str(f), step=3) is None

    def test_size_change_misses_even_with_same_mtime(self, tmp_path: Path) -> None:
        cache = SessionReadCache()
        f = tmp_path / "a.txt"
        _write(f, "12345")
        st_before = f.stat()
        cache.put(str(f), "12345", step=1)
        _write(f, "1234567890")
        os.utime(f, ns=(st_before.st_atime_ns, st_before.st_mtime_ns))
        assert cache.get(str(f), step=2) is None

    def test_lru_evicts_oldest(self, tmp_path: Path) -> None:
        cache = SessionReadCache(max_entries=2)
        paths = []
        for i in range(3):
            p = tmp_path / f"f{i}.txt"
            _write(p, f"content {i}")
            paths.append(p)
            cache.put(str(p), f"content {i}", step=i)
        assert len(cache) == 2
        assert cache.get(str(paths[0]), step=9) is None  # evicted
        assert cache.get(str(paths[2]), step=9) is not None

    def test_invalidate_and_missing_file(self, tmp_path: Path) -> None:
        cache = SessionReadCache()
        f = tmp_path / "gone.txt"
        _write(f, "x")
        cache.put(str(f), "x", step=1)
        f.unlink()
        # Vanished file: never serve a cached answer for it.
        assert cache.get(str(f), step=2) is None
        assert SessionReadCache().get(str(tmp_path / "never-existed.txt"), 1) is None

    def test_reset_clears(self, tmp_path: Path) -> None:
        cache = SessionReadCache()
        f = tmp_path / "a.txt"
        _write(f, "data")
        cache.put(str(f), "data", step=1)
        assert len(cache) == 1
        cache.reset()
        assert len(cache) == 0

    def test_invalid_max_entries(self) -> None:
        with pytest.raises(ValueError):
            SessionReadCache(max_entries=0)
