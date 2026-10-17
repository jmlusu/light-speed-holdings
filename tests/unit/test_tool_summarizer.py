"""Tests for tool result summarization — error compression and dedupe."""

from __future__ import annotations

from ai_company.executor.tool_summarizer import (
    _MAX_ERROR_CACHE,
    _compress_powershell_error,
    _dedupe_error,
    _error_fingerprints,
    _reset_error_cache,
    _summarize_bash,
    _summarize_generic,
    _summarize_read,
    summarize_tool_result,
)

# ── Sample verbose PowerShell error ──────────────────────────────────

_PS_VERBOSE_ERROR = """\
At C:\\project\\script.ps1:15 char:9
+         throw $_
+         ~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [], RuntimeException
    + FullyQualifiedErrorId : RuntimeException

At line:1 char:1
+ Invoke-BrokenCommand
+ ~~~~~~~~~~~~~~~~~~~
ParameterBindingException: A parameter cannot be found

Call stack:
    at <ScriptBlock>, C:\\project\\script.ps1: line 15
    at Invoke-Command, <ModulePath>: line 3

Traceback (most recent call last):
  File "C:\\project\\main.py", line 42, in <module>
    raise ValueError("bad input")
ValueError: bad input
"""

_PY_TRACEBACK = """\
Traceback (most recent call last):
  File "C:\\Users\\dev\\app.py", line 10, in run
    result = process(data)
  File "C:\\Users\\dev\\app.py", line 25, in process
    raise RuntimeError("disk full")
RuntimeError: disk full
"""


class TestCompressPowerShellError:
    def test_empty_returns_empty(self):
        assert _compress_powershell_error("") == ""

    def test_strips_stack_frames(self):
        result = _compress_powershell_error(_PS_VERBOSE_ERROR)
        assert "Call stack:" not in result
        assert "at line" not in result.lower()
        assert "at <ScriptBlock>" not in result
        assert "ParameterBindingException" in result or "throw" in result

    def test_strips_positional_noise(self):
        result = _compress_powershell_error(_PS_VERBOSE_ERROR)
        assert " char:" not in result
        assert ": line " not in result

    def test_strips_ansi_escapes(self):
        ansi_error = "\x1b[31mError: something broke\x1b[0m"
        result = _compress_powershell_error(ansi_error)
        assert "\x1b[" not in result
        assert "Error: something broke" in result

    def test_line_cap_bounds_output(self):
        long_error = "\n".join(f"error line {i}" for i in range(100))
        result = _compress_powershell_error(long_error, max_chars=10000)
        lines = result.splitlines()
        assert len(lines) <= 12  # hard cap

    def test_respects_max_chars(self):
        long_error = "\n".join(f"error line {i} " + "x" * 60 for i in range(50))
        result = _compress_powershell_error(long_error, max_chars=200)
        assert len(result) <= 200 + len("... [error truncated]")
        assert "[error truncated]" in result

    def test_preserves_essential_error(self):
        result = _compress_powershell_error(_PY_TRACEBACK)
        assert "RuntimeError" in result or "disk full" in result
        assert "Traceback (most recent call last):" not in result


class TestDedupeError:
    def setup_method(self):
        _reset_error_cache()

    def test_first_occurrence_returned_as_is(self):
        err = "ERROR: file not found at path: src/missing.py"
        assert _dedupe_error(err) == err

    def test_repeat_replaced_with_reference(self):
        err = "ERROR: file not found at path: src/missing.py"
        first = _dedupe_error(err)
        second = _dedupe_error(err)
        assert first == err
        assert "repeat of earlier error" in second
        assert second != err

    def test_different_errors_not_deduped(self):
        a = _dedupe_error("ERROR: timeout on request")
        b = _dedupe_error("ERROR: connection refused")
        assert a == "ERROR: timeout on request"
        assert b == "ERROR: connection refused"

    def test_normalized_match_across_paths(self):
        """Same error text with different absolute paths should dedupe."""
        e1 = _dedupe_error("Permission denied at C:\\proj\\a\\file.txt")
        e2 = _dedupe_error("Permission denied at C:\\other\\b\\file.txt")
        assert e1 == "Permission denied at C:\\proj\\a\\file.txt"
        assert "repeat of earlier error" in e2

    def test_repeat_count_increments(self):
        err = "ERROR: disk full on volume C:"
        _dedupe_error(err)
        second = _dedupe_error(err)
        third = _dedupe_error(err)
        assert "#2" in second
        assert "#3" in third

    def test_cache_eviction_fifo(self):
        for i in range(_MAX_ERROR_CACHE):
            _dedupe_error(f"ERROR: unique failure {i}")
        assert len(_error_fingerprints) == _MAX_ERROR_CACHE
        _dedupe_error("ERROR: one more after full")
        assert len(_error_fingerprints) == _MAX_ERROR_CACHE


class TestSummarizeBash:
    def setup_method(self):
        _reset_error_cache()

    def test_error_path_compressed(self):
        result = _summarize_bash(
            {"command": "deploy.ps1", "error": _PS_VERBOSE_ERROR},
            max_tokens=200,
            llm=None,
        )
        assert result.startswith("bash(deploy.ps1) → ERROR:")
        assert "Call stack:" not in result
        assert len(result) < len(_PS_VERBOSE_ERROR)

    def test_stderr_compressed(self):
        result = _summarize_bash(
            {
                "command": "build",
                "returncode": 1,
                "stdout": "",
                "stderr": _PS_VERBOSE_ERROR,
            },
            max_tokens=200,
            llm=None,
        )
        assert "FAILED (exit 1)" in result
        assert "Call stack:" not in result

    def test_success_with_stdout(self):
        result = _summarize_bash(
            {"command": "ls", "returncode": 0, "stdout": "file1\nfile2"},
            max_tokens=100,
            llm=None,
        )
        assert "OK" in result
        assert "file1" in result

    def test_no_output(self):
        result = _summarize_bash(
            {"command": "true", "returncode": 0},
            max_tokens=100,
            llm=None,
        )
        assert "no output" in result


class TestSummarizeRead:
    def setup_method(self):
        _reset_error_cache()

    def test_error_path_compressed(self):
        result = _summarize_read(
            {"path": "src/main.py", "error": _PY_TRACEBACK},
            max_tokens=200,
            llm=None,
        )
        assert result.startswith("read(src/main.py) → ERROR:")
        assert "Traceback (most recent call last):" not in result

    def test_code_file_structured(self):
        code = "import os\n\ndef main():\n    return 0\n\nclass Foo:\n    pass\n"
        result = _summarize_read(
            {"path": "src/app.py", "content": code},
            max_tokens=500,
            llm=None,
        )
        assert "lines" in result
        assert "Key structures:" in result
        assert "def main" in result

    def test_large_text_truncated(self):
        big = "x" * 10000
        result = _summarize_read(
            {"path": "notes.txt", "content": big},
            max_tokens=100,
            llm=None,
        )
        assert "chars total" in result or "[truncated]" in result


class TestSummarizeGeneric:
    def setup_method(self):
        _reset_error_cache()

    def test_error_path_compressed(self):
        result = _summarize_generic(
            {"error": _PS_VERBOSE_ERROR},
            max_tokens=200,
            llm=None,
        )
        assert result.startswith("ERROR:")
        assert "Call stack:" not in result

    def test_success_json(self):
        result = _summarize_generic(
            {"output": "hello", "status": "ok"},
            max_tokens=100,
            llm=None,
        )
        assert "hello" in result


class TestDispatch:
    def setup_method(self):
        _reset_error_cache()

    def test_unknown_tool_uses_generic(self):
        result = summarize_tool_result(
            "unknown_tool",
            {"error": "boom"},
            max_tokens=100,
            llm=None,
        )
        assert result.startswith("ERROR:")

    def test_known_tools_dispatch(self):
        r = summarize_tool_result(
            "bash",
            {"command": "ls", "returncode": 0, "stdout": "ok"},
            max_tokens=100,
            llm=None,
        )
        assert "bash(ls)" in r
