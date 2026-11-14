"""Hot-file LRU cache, output caps, session-start injection (GO-4)."""

from __future__ import annotations

import time

from ai_company.llm.hot_file_cache import (
    GREP_RESULT_CAP,
    TOOL_OUTPUT_CAP_BYTES,
    SessionHotFileCache,
    build_session_start_injection,
    cap_grep_results,
    cap_tool_output,
)


class TestOutputCaps:
    def test_tool_output_cap_50kb(self):
        text = "x" * (TOOL_OUTPUT_CAP_BYTES + 100)
        capped, truncated = cap_tool_output(text)
        assert truncated is True
        assert len(capped.encode()) <= TOOL_OUTPUT_CAP_BYTES + 120  # + notice

    def test_small_output_not_truncated(self):
        assert cap_tool_output("hello") == ("hello", False)

    def test_grep_cap_50(self):
        results = list(range(200))
        capped, truncated = cap_grep_results(results)
        assert truncated is True
        assert len(capped) == GREP_RESULT_CAP == 50
        capped2, truncated2 = cap_grep_results([1, 2])
        assert truncated2 is False and capped2 == [1, 2]


class TestSessionLRU:
    def test_hit_on_repeat_read_same_mtime(self, tmp_path):
        path = tmp_path / "hot.txt"
        path.write_text("content-v1", encoding="utf-8")
        cache = SessionHotFileCache("ses_1")
        cache.put(path, "content-v1")
        assert cache.get(path) == "content-v1"
        assert cache.hits == 1 and cache.dedup_hit_rate == 1.0

    def test_mtime_invalidation(self, tmp_path):
        path = tmp_path / "hot.txt"
        path.write_text("v1", encoding="utf-8")
        cache = SessionHotFileCache("ses_1")
        cache.put(path, "v1")
        time.sleep(0.02)
        path.write_text("v2-longer", encoding="utf-8")
        # mtime changed -> miss, not stale v1
        assert cache.get(path) is None
        assert cache.invalidations == 1

    def test_explicit_invalidate_after_edit(self, tmp_path):
        path = tmp_path / "hot.txt"
        path.write_text("v1", encoding="utf-8")
        cache = SessionHotFileCache("ses_1")
        cache.put(path, "v1")
        cache.invalidate(path)
        assert cache.get(path) is None

    def test_lru_eviction(self, tmp_path):
        cache = SessionHotFileCache("ses_1", max_entries=2)
        paths = []
        for i in range(3):
            p = tmp_path / f"f{i}.txt"
            p.write_text(str(i), encoding="utf-8")
            paths.append(p)
            cache.put(p, str(i))
        assert len(cache._cache) == 2
        assert cache.get(paths[0]) is None  # evicted (oldest)

    def test_sessions_isolated(self, tmp_path):
        path = tmp_path / "hot.txt"
        path.write_text("v1", encoding="utf-8")
        a = SessionHotFileCache("ses_a")
        b = SessionHotFileCache("ses_b")
        a.put(path, "v1")
        assert b.get(path) is None
        assert b.misses == 1

    def test_stats_shape(self, tmp_path):
        cache = SessionHotFileCache("ses_1")
        stats = cache.stats()
        assert stats["session_id"] == "ses_1"
        assert "dedup_hit_rate" in stats


class TestSessionStartInjection:
    def test_injects_agents_status_registry(self, tmp_path):
        (tmp_path / "AGENTS.md").write_text("# agents", encoding="utf-8")
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "STATUS.md").write_text("# status", encoding="utf-8")
        (tmp_path / "company-registry.yaml").write_text("agents: []", encoding="utf-8")
        injected = build_session_start_injection(tmp_path)
        assert injected["AGENTS.md"] == "# agents"
        assert injected["docs/STATUS.md"] == "# status"
        assert injected["company-registry.yaml"] == "agents: []"

    def test_missing_files_skipped_not_faked(self, tmp_path):
        assert build_session_start_injection(tmp_path) == {}
