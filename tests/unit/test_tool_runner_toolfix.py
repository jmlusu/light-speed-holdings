"""Integration tests: ToolRunner P1 wiring (T-01..T-09).

Covers edit pre-flight, schema fail-fast, PowerShell lint, egress/allowlist
deny audit, output caps, grep backend fallback, webfetch retry, and the
depth-limit direct-execution fallback — through ``run_plan`` (the public
entry point), not internals.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.executor.tool_runner import ToolRunner


@pytest.fixture()
def runner(tmp_path: Path) -> ToolRunner:
    r = ToolRunner(project_root=tmp_path)
    r._sleep = lambda _d: None  # no real backoff waits
    return r


# --- Edit pre-flight (T-01) ----------------------------------------------------


class TestEditPreflightWiring:
    def test_edit_replace_once(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("hello world\n", encoding="utf-8")
        results = runner.run_plan(
            [
                {
                    "tool": "edit",
                    "args": {"path": "a.txt", "oldString": "world", "newString": "there"},
                }
            ]
        )
        assert results[0]["status"] == "ok"
        assert (tmp_path / "a.txt").read_text(encoding="utf-8").strip() == "hello there"

    def test_edit_noop_rejected_locally(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("hello\n", encoding="utf-8")
        results = runner.run_plan(
            [
                {
                    "tool": "edit",
                    "args": {"path": "a.txt", "oldString": "hello", "newString": "hello"},
                }
            ]
        )
        assert results[0]["status"] == "error"
        # Rejected locally by schema validation (no-op old == new).
        assert "no-op" in results[0]["error"].lower()

    def test_edit_not_found_rejected(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("hello\n", encoding="utf-8")
        results = runner.run_plan(
            [
                {
                    "tool": "edit",
                    "args": {"path": "a.txt", "oldString": "missing", "newString": "x"},
                }
            ]
        )
        assert results[0]["status"] == "error"
        assert results[0]["error_code"] == "EDIT_NOT_FOUND"

    def test_edit_ambiguous_rejected(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("x\nx\n", encoding="utf-8")
        results = runner.run_plan(
            [
                {
                    "tool": "edit",
                    "args": {"path": "a.txt", "oldString": "x", "newString": "y"},
                }
            ]
        )
        assert results[0]["status"] == "error"
        assert results[0]["error_code"] == "EDIT_AMBIGUOUS"

    def test_edit_content_overwrite_still_works(self, runner: ToolRunner, tmp_path: Path) -> None:
        results = runner.run_plan(
            [{"tool": "edit", "args": {"path": "new.txt", "content": "fresh"}}]
        )
        assert results[0]["status"] == "ok"
        assert (tmp_path / "new.txt").read_text(encoding="utf-8") == "fresh"

    def test_edit_filepath_alias(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("alpha\n", encoding="utf-8")
        results = runner.run_plan(
            [
                {
                    "tool": "edit",
                    "args": {"filePath": "a.txt", "oldString": "alpha", "newString": "beta"},
                }
            ]
        )
        assert results[0]["status"] == "ok"


# --- Schema fail-fast (T-02) ----------------------------------------------------


class TestSchemaFailFastWiring:
    def test_null_filepath_rejected_before_dispatch(self, runner: ToolRunner) -> None:
        results = runner.run_plan([{"tool": "read", "args": {"path": None}}])
        assert results[0]["status"] == "error"
        assert "path" in results[0]["error"].lower()

    def test_missing_command_rejected(self, runner: ToolRunner) -> None:
        results = runner.run_plan([{"tool": "bash", "args": {}}])
        assert results[0]["status"] == "error"

    def test_missing_pattern_rejected(self, runner: ToolRunner) -> None:
        results = runner.run_plan([{"tool": "grep", "args": {"path": "."}}])
        assert results[0]["status"] == "error"


# --- PowerShell pre-flight (T-05) -------------------------------------------------


class TestPowershellPreflightWiring:
    def test_negative_select_blocked(self, runner: ToolRunner) -> None:
        results = runner.run_plan([{"tool": "bash", "args": {"command": "Select-Object -Last -5"}}])
        assert results[0]["status"] == "error"
        assert "POWERSHELL_ANTIPATTERN" in results[0]["error"]

    def test_and_operator_blocked(self, runner: ToolRunner) -> None:
        results = runner.run_plan([{"tool": "bash", "args": {"command": "cd foo && git status"}}])
        assert results[0]["status"] == "error"


# --- Permission-deny audit (T-09) + output cap (T-11) ------------------------------


class TestDenyAuditAndCaps:
    def test_path_escape_emits_audit_event(self, runner: ToolRunner, tmp_path: Path) -> None:
        import ai_company.executor.tool_runner as tr

        seen: list[object] = []
        original = tr.log_permission_deny
        tr.log_permission_deny = lambda *a, **kw: seen.append(a)  # type: ignore[assignment]
        try:
            results = runner.run_plan(
                [{"tool": "read", "args": {"path": "../../etc/passwd"}}],
                task_id="t1",
                agent_id="a1",
            )
        finally:
            tr.log_permission_deny = original  # type: ignore[assignment]
        assert results[0]["status"] == "error"
        assert seen, "path-escape deny must emit a PERMISSION_DENIED audit event"

    def test_allowlist_deny_emits_audit_event(self, runner: ToolRunner) -> None:
        import ai_company.executor.tool_runner as tr

        seen: list[object] = []
        original = tr.log_permission_deny
        tr.log_permission_deny = lambda *a, **kw: seen.append(a)  # type: ignore[assignment]
        try:
            results = runner.run_plan(
                [{"tool": "bash", "args": {"command": "rm -rf /"}}],
                task_id="t2",
                agent_id="a2",
            )
        finally:
            tr.log_permission_deny = original  # type: ignore[assignment]
        assert results[0]["status"] == "error"
        assert seen, "allowlist deny must emit a PERMISSION_DENIED audit event"

    def test_large_read_capped(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "big.txt").write_text("x" * 100_000, encoding="utf-8")
        results = runner.run_plan([{"tool": "read", "args": {"path": "big.txt"}}])
        assert results[0]["status"] == "ok"
        assert len(results[0]["content"].encode()) <= 51_200 + 512

    def test_binary_read_rejected(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "bin.dat").write_bytes(b"\x00\x01\x02" + b"x" * 100)
        results = runner.run_plan([{"tool": "read", "args": {"path": "bin.dat"}}])
        assert results[0]["status"] == "error"
        assert results[0]["error_code"] == "BINARY"


# --- Grep fallback + caps (T-03/T-04) ----------------------------------------------


class TestGrepWiring:
    def test_grep_finds_pattern(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("def foo():\n    pass\n", encoding="utf-8")
        results = runner.run_plan([{"tool": "grep", "args": {"pattern": "def foo"}}])
        assert results[0]["status"] == "ok"
        assert len(results[0]["matches"]) >= 1
        assert "backend" in results[0]

    def test_grep_long_line_truncated(self, runner: ToolRunner, tmp_path: Path) -> None:
        (tmp_path / "long.txt").write_text(("needle " + "x" * 5_000) + "\n", encoding="utf-8")
        results = runner.run_plan([{"tool": "grep", "args": {"pattern": "needle"}}])
        assert results[0]["status"] == "ok"
        assert all(len(m) <= 501 + 30 for m in results[0]["matches"])


# --- Webfetch retry (T-07) --------------------------------------------------------


class TestWebfetchRetryWiring:
    def test_429_then_success(self, runner: ToolRunner) -> None:
        script = iter(
            [
                {"error": "HTTP 429: Too Many Requests", "http_status": 429},
                {"error": "HTTP 429: Too Many Requests", "http_status": 429},
                {"url": "https://example.com", "content": "hello"},
            ]
        )
        runner._fetch_once = MagicMock(side_effect=lambda _url: next(script))  # type: ignore[method-assign]
        results = runner.run_plan([{"tool": "webfetch", "args": {"url": "https://example.com"}}])
        assert results[0]["status"] == "ok"
        assert results[0]["content"] == "hello"
        assert results[0]["attempts"] == 3

    def test_persistent_429_classified(self, runner: ToolRunner) -> None:
        runner._fetch_once = MagicMock(  # type: ignore[method-assign]
            return_value={"error": "HTTP 429: Too Many Requests", "http_status": 429}
        )
        results = runner.run_plan([{"tool": "webfetch", "args": {"url": "https://example.com"}}])
        assert results[0]["status"] == "error"
        assert results[0]["error_code"] == "RATE_LIMITED"
        assert results[0]["attempts"] == 3


# --- Depth-limit fallback (T-06) ----------------------------------------------------


class TestDepthFallbackWiring:
    def test_task_depth_error_result_becomes_direct(self, runner: ToolRunner) -> None:
        runner._execute_tool = MagicMock(  # type: ignore[method-assign]
            return_value={"error": "Subagent depth limit reached (1)"}
        )
        results = runner.run_plan(
            [
                {
                    "tool": "task",
                    "args": {"receiver": "lead-backend", "instruction": "build api"},
                }
            ],
            agent_id="chief-of-staff",
        )
        assert results[0]["status"] == "ok"
        assert results[0]["action"] == "execute_directly"
        assert results[0]["error_code"] == "DEPTH_LIMIT"

    def test_task_depth_exception_becomes_direct(self, runner: ToolRunner) -> None:
        def _boom(*args: object, **kwargs: object) -> object:
            raise RuntimeError("Subagent depth limit reached (1)")

        runner._execute_tool = _boom  # type: ignore[method-assign]
        results = runner.run_plan(
            [
                {
                    "tool": "task",
                    "args": {"receiver": "lead-backend", "instruction": "build api"},
                }
            ],
            agent_id="chief-of-staff",
        )
        assert results[0]["status"] == "ok"
        assert results[0]["fallback"] == "direct_execution"
