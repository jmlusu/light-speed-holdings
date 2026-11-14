"""Summarizer caps: 50 KB end-to-end + grep line/match caps (T-04/T-11)."""

from __future__ import annotations

from ai_company.executor.tool_summarizer import _summarize_grep, summarize_tool_result

# --- 50 KB end-to-end cap ---------------------------------------------------------


class TestSummarizerOutputCap:
    def test_huge_read_summary_capped(self) -> None:
        huge = {"path": "notes.txt", "content": "x" * 200_000}
        # max_tokens high enough that _summarize_read returns the full body,
        # so the 50 KB end-to-end cap in summarize_tool_result must bite.
        summary = summarize_tool_result("read", huge, max_tokens=100_000, llm=None)
        assert len(summary.encode("utf-8")) <= 51_200 + 1024
        assert "truncated" in summary.lower()

    def test_small_summary_untouched(self) -> None:
        summary = summarize_tool_result(
            "bash",
            {"command": "ls", "returncode": 0, "stdout": "ok"},
            max_tokens=100,
            llm=None,
        )
        assert "ok" in summary
        assert "truncated" not in summary.lower()


# --- Grep caps --------------------------------------------------------------------


class TestSummarizerGrepCaps:
    def test_long_match_lines_capped(self) -> None:
        result = {
            "pattern": "needle",
            "matches": ["file.txt:1: needle " + "x" * 5_000],
            "total": 1,
        }
        summary = _summarize_grep(result, max_tokens=500, llm=None)
        longest = max(len(line) for line in summary.splitlines())
        assert longest <= 561  # 500 + ellipsis marker slack

    def test_match_cap_footer(self) -> None:
        matches = [f"f{i}.txt:1: hit {i}" for i in range(150)]
        result = {"pattern": "hit", "matches": matches, "total": 150}
        summary = _summarize_grep(result, max_tokens=500, llm=None)
        assert "150" in summary
        assert "narrow" in summary.lower()

    def test_grep_error_unchanged_shape(self) -> None:
        summary = _summarize_grep({"pattern": "x", "error": "boom"}, max_tokens=100, llm=None)
        assert summary.startswith("grep(x) → ERROR:")
