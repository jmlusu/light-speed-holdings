"""Tests for tool_validation helpers (P1 tool fixes T-01/T-02/T-03/T-04/T-05/T-07/T-08/T-11)."""

from __future__ import annotations

import pytest

from ai_company.executor.tool_validation import (
    GREP_MATCH_CAP,
    GREP_RECORD_CAP_BYTES,
    OUTPUT_CAP_BYTES,
    ToolOutputDeduper,
    call_with_retry,
    cap_grep_line,
    check_edit_preflight,
    classify_tool_error,
    compute_backoff_delay,
    content_sha256,
    depth_limit_fallback,
    find_powershell_antipatterns,
    grep_backend,
    is_retryable_error,
    resolve_file_path_arg,
    truncate_to_cap,
    validate_tool_args,
)

# --- Schema fail-fast (T-02) -------------------------------------------------


class TestValidateToolArgs:
    def test_missing_path_rejected(self) -> None:
        ok, msg = validate_tool_args("read", {})
        assert ok is False
        assert "path" in msg
        assert "Expected shape" in msg

    def test_null_path_rejected(self) -> None:
        ok, _ = validate_tool_args("read", {"path": None})
        assert ok is False

    def test_blank_path_rejected(self) -> None:
        ok, _ = validate_tool_args("read", {"path": "   "})
        assert ok is False

    def test_filepath_alias_accepted(self) -> None:
        ok, _ = validate_tool_args("read", {"filePath": "src/main.py"})
        assert ok is True

    def test_null_filepath_alias_rejected(self) -> None:
        ok, _ = validate_tool_args("edit", {"filePath": None})
        assert ok is False

    def test_valid_read_passes(self) -> None:
        ok, _ = validate_tool_args("read", {"path": "a.py"})
        assert ok is True

    def test_missing_command_rejected(self) -> None:
        ok, msg = validate_tool_args("bash", {"command": None})
        assert ok is False
        assert "command" in msg

    def test_missing_pattern_rejected(self) -> None:
        ok, _ = validate_tool_args("grep", {})
        assert ok is False

    def test_edit_noop_rejected(self) -> None:
        ok, msg = validate_tool_args("edit", {"path": "a.py", "oldString": "x", "newString": "x"})
        assert ok is False
        assert "no-op" in msg.lower()


# --- Edit pre-flight (T-01) ---------------------------------------------------


class TestCheckEditPreflight:
    def test_single_match_ok(self) -> None:
        result = check_edit_preflight(
            current_content="a\nfoo\nb\n", old_string="foo", new_string="bar"
        )
        assert result.ok is True
        assert result.replaced_content == "a\nbar\nb\n"
        assert result.match_count == 1

    def test_noop_rejected(self) -> None:
        result = check_edit_preflight(current_content="foo foo", old_string="foo", new_string="foo")
        assert result.ok is False
        assert result.error_code == "NOOP"

    def test_not_found_rejected(self) -> None:
        result = check_edit_preflight(
            current_content="hello world", old_string="missing", new_string="x"
        )
        assert result.ok is False
        assert result.error_code == "EDIT_NOT_FOUND"

    def test_ambiguous_rejected_with_locations(self) -> None:
        result = check_edit_preflight(
            current_content="foo\nx\nfoo\ny\nfoo\n",
            old_string="foo",
            new_string="bar",
        )
        assert result.ok is False
        assert result.error_code == "EDIT_AMBIGUOUS"
        assert result.match_count == 3
        assert result.locations == [1, 3, 5]

    def test_empty_old_rejected(self) -> None:
        result = check_edit_preflight(current_content="abc", old_string="", new_string="x")
        assert result.ok is False
        assert result.error_code == "VALIDATION_REJECTED"


# --- PowerShell pre-flight (T-05) ---------------------------------------------


class TestFindPowershellAntipatterns:
    def test_negative_select_detected(self) -> None:
        hits = find_powershell_antipatterns("Get-ChildItem | Select-Object -Last -30")
        assert [h.pattern for h in hits] == ["select_negative"]

    def test_and_operator_detected(self) -> None:
        hits = find_powershell_antipatterns("cd foo && python main.py")
        assert "double_ampersand" in [h.pattern for h in hits]

    def test_heredoc_detected(self) -> None:
        hits = find_powershell_antipatterns("python << 'PYEOF'")
        assert "bash_heredoc" in [h.pattern for h in hits]

    def test_python3_detected(self) -> None:
        hits = find_powershell_antipatterns("python3 scripts/x.py")
        assert "python3_windows" in [h.pattern for h in hits]

    def test_jq_subexpr_detected(self) -> None:
        hits = find_powershell_antipatterns('gh pr view --jq "state=$(.state)"')
        assert "jq_dollar_subshell" in [h.pattern for h in hits]

    def test_clean_command_passes(self) -> None:
        assert find_powershell_antipatterns("git status") == []
        assert find_powershell_antipatterns("gh pr view --jq '.state'") == []


# --- Retry classification + backoff (T-07/T-08) --------------------------------


class TestClassifyToolError:
    def test_rate_limited_429(self) -> None:
        assert classify_tool_error("HTTP 429 Too Many Requests", 429) == "RATE_LIMITED"
        assert classify_tool_error("rate limit exceeded") == "RATE_LIMITED"

    def test_depth_limit(self) -> None:
        assert classify_tool_error("Subagent depth limit reached (1)") == "DEPTH_LIMIT"
        assert is_retryable_error("Subagent depth limit reached (1)") is False

    def test_user_cancelled_vs_infra_aborted(self) -> None:
        assert classify_tool_error("Task cancelled by user") == "USER_CANCELLED"
        assert classify_tool_error("Tool execution aborted: subagent killed") == "INFRA_ABORTED"
        assert classify_tool_error("aborted") == "INFRA_ABORTED"

    def test_transport_and_target(self) -> None:
        assert classify_tool_error("HTTP 503 Service Unavailable", 503) == "TRANSPORT_ERROR"
        assert classify_tool_error("Fetch failed: Connection refused") == "TARGET_UNREACHABLE"

    def test_bad_request_not_retryable(self) -> None:
        assert classify_tool_error("HTTP 404 Not Found", 404) == "BAD_REQUEST"
        assert is_retryable_error("HTTP 404 Not Found", 404) is False

    def test_retryable_set(self) -> None:
        assert is_retryable_error("HTTP 429", 429) is True
        assert is_retryable_error("HTTP 500", 500) is True
        assert is_retryable_error("Connection refused") is True


class TestComputeBackoffDelay:
    def test_exponential_schedule_bounds(self) -> None:
        import random

        rng = random.Random(42)
        d0 = compute_backoff_delay(0, rng=rng)
        assert 0.5 <= d0 <= 0.5 * 1.25
        rng = random.Random(42)
        d1 = compute_backoff_delay(1, rng=rng)
        assert 2.0 <= d1 <= 2.0 * 1.25
        rng = random.Random(42)
        d2 = compute_backoff_delay(2, rng=rng)
        assert 8.0 <= d2 <= 8.0 * 1.25

    def test_retry_after_floor_wins(self) -> None:
        import random

        d = compute_backoff_delay(0, retry_after=10.0, rng=random.Random(1))
        assert d >= 10.0


class TestCallWithRetry:
    def test_success_after_two_429s(self) -> None:
        calls = {"n": 0}

        def operation() -> dict[str, object]:
            calls["n"] += 1
            if calls["n"] < 3:
                return {"error": "HTTP 429 Too Many Requests", "http_status": 429}
            return {"content": "ok"}

        slept: list[float] = []
        result, attempts, delays = call_with_retry(operation, sleep=slept.append)
        assert result["content"] == "ok"
        assert attempts == 3
        assert len(delays) == 2
        assert len(slept) == 2

    def test_persistent_429_exhausts(self) -> None:
        def operation() -> dict[str, object]:
            return {"error": "HTTP 429 Too Many Requests", "http_status": 429}

        result, attempts, _delays = call_with_retry(
            operation, max_attempts=3, sleep=lambda _d: None
        )
        assert "error" in result
        assert result["error_code"] == "RATE_LIMITED"
        assert attempts == 3

    def test_non_retryable_not_retried(self) -> None:
        n = {"count": 0}

        def operation() -> dict[str, object]:
            n["count"] += 1
            return {"error": "HTTP 404 Not Found", "http_status": 404}

        result, attempts, _ = call_with_retry(operation, sleep=lambda _d: None)
        assert attempts == 1
        assert result["error_code"] == "BAD_REQUEST"
        assert n["count"] == 1


class TestDepthLimitFallback:
    def test_direct_execution_envelope(self) -> None:
        env = depth_limit_fallback(receiver="lead-backend", instruction="build api")
        assert env["action"] == "execute_directly"
        assert env["fallback"] == "direct_execution"
        assert env["error_code"] == "DEPTH_LIMIT"


# --- Output caps + dedup (T-04/T-11) ---------------------------------------------


class TestOutputCaps:
    def test_truncate_small_untouched(self) -> None:
        result = truncate_to_cap("hello")
        assert result.truncated is False
        assert result.text == "hello"

    def test_truncate_large_capped(self) -> None:
        big = "x" * (OUTPUT_CAP_BYTES * 2)
        result = truncate_to_cap(big)
        assert result.truncated is True
        assert len(result.text.encode("utf-8")) <= OUTPUT_CAP_BYTES + 512
        assert "truncated" in result.text

    def test_cap_grep_line(self) -> None:
        assert cap_grep_line("short") == "short"
        long_line = "y" * 600
        capped = cap_grep_line(long_line)
        assert len(capped) <= 501
        huge = "z" * (GREP_RECORD_CAP_BYTES + 10)
        assert cap_grep_line(huge).endswith("[line truncated]")

    def test_deduper_pointer(self) -> None:
        deduper = ToolOutputDeduper()
        assert deduper.check("a.py", content_sha256("hello"), 1) == (False, None)
        is_dup, first = deduper.check("a.py", content_sha256("hello"), 5)
        assert is_dup is True
        assert first == 1
        is_dup2, _ = deduper.check("a.py", content_sha256("changed"), 6)
        assert is_dup2 is False

    def test_resolve_file_path_aliases(self) -> None:
        assert resolve_file_path_arg({"filePath": "x.py"}) == "x.py"
        assert resolve_file_path_arg({"path": "y.py"}) == "y.py"
        assert resolve_file_path_arg({"filePath": None}) is None
        assert resolve_file_path_arg({}) is None

    def test_grep_caps_constants(self) -> None:
        assert GREP_MATCH_CAP == 100
        assert GREP_RECORD_CAP_BYTES == 64 * 1024

    def test_grep_backend_fallback(self) -> None:
        # Never raises; returns one of the three backends.
        assert grep_backend() in ("rg", "git-grep", "python")


class TestPsScripts:
    def test_dev_ps1_checks_rg(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        dev_ps1 = (root / "scripts" / "dev" / "dev.ps1").read_text(encoding="utf-8")
        assert "Ensure-Ripgrep" in dev_ps1
        assert "BurntSushi.ripgrep.MSVC" in dev_ps1
        assert "Get-Command rg" in dev_ps1 or 'Test-CommandExists "rg"' in dev_ps1

    def test_scanner_covers_five_patterns(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        scanner = (root / "scripts" / "maintenance" / "scan-ps-antipatterns.ps1").read_text(
            encoding="utf-8"
        )
        for marker in (
            "select_negative",
            "double_ampersand",
            "bash_heredoc",
            "python3_windows",
            "jq_dollar_subshell",
        ):
            assert marker in scanner

    @pytest.mark.parametrize(
        "command",
        [
            "Get-ChildItem | Select-Object -Last -30",
            "cd foo && git status",
            "python << 'EOF'",
            "python3 x.py",
            'gh pr view --jq "x=$(y)"',
        ],
    )
    def test_each_pattern_in_py_linter_table(self, command: str) -> None:
        # The runtime pre-flight (ps_linter) and the ps scanner share the
        # five §17 patterns; every fixture command must trip at least one.
        assert find_powershell_antipatterns(command) != []
