"""Tests for the doctor diagnostics module."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from ai_company.doctor.checks import (
    CheckResult,
    check_agent_files,
    check_cost_tracker,
    check_dependencies,
    check_disk_space,
    check_inbox_health,
    check_llm_providers,
    check_memory_engine,
    check_python_version,
    run_all_checks,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Change to a temporary directory so file-based checks don't touch real files."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


# ---------------------------------------------------------------------------
# CheckResult dataclass
# ---------------------------------------------------------------------------


class TestCheckResult:
    def test_default_details(self):
        r = CheckResult(name="x", passed=True, message="ok")
        assert r.details == {}
        assert r.severity == "info"

    def test_custom_details(self):
        r = CheckResult(name="x", passed=True, message="ok", details={"a": 1})
        assert r.details["a"] == 1


# ---------------------------------------------------------------------------
# check_python_version
# ---------------------------------------------------------------------------


class TestCheckPythonVersion:
    def test_returns_check_result(self):
        result = check_python_version()
        assert isinstance(result, CheckResult)
        assert result.name == "Python Version"

    def test_passes_on_3_12_plus(self):
        result = check_python_version()
        if sys.version_info >= (3, 12):
            assert result.passed is True
            assert result.severity == "ok"
        else:
            assert result.passed is False

    def test_details_contain_expected(self):
        result = check_python_version()
        assert "expected" in result.details
        assert result.details["expected"] == ">=3.12"


# ---------------------------------------------------------------------------
# check_dependencies
# ---------------------------------------------------------------------------


class TestCheckDependencies:
    def test_returns_check_result(self):
        result = check_dependencies()
        assert isinstance(result, CheckResult)
        assert result.name == "Dependencies"

    def test_counts_installed(self):
        result = check_dependencies()
        assert "/" in result.message  # e.g. "7/7 installed"

    def test_missing_listed_in_details(self):
        result = check_dependencies()
        assert "missing" in result.details
        assert "installed" in result.details
        assert isinstance(result.details["missing"], list)


# ---------------------------------------------------------------------------
# check_agent_files
# ---------------------------------------------------------------------------


class TestCheckAgentFiles:
    def test_no_directory(self, tmp_workspace: Path):
        result = check_agent_files()
        assert result.passed is False
        assert result.severity == "error"
        assert "not found" in result.message.lower()

    def test_empty_directory(self, tmp_workspace: Path):
        agents_dir = tmp_workspace / ".opencode" / "agents"
        agents_dir.mkdir(parents=True)
        result = check_agent_files()
        assert result.passed is False
        assert result.severity == "warning"
        assert "0 agent files" in result.message

    def test_with_files(self, tmp_workspace: Path):
        agents_dir = tmp_workspace / ".opencode" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "ceo.md").write_text("test", encoding="utf-8")
        (agents_dir / "cto.md").write_text("test", encoding="utf-8")
        result = check_agent_files()
        assert result.passed is True
        assert "2 agent files" in result.message
        assert result.details["count"] == 2


# ---------------------------------------------------------------------------
# check_inbox_health
# ---------------------------------------------------------------------------


class TestCheckInboxHealth:
    def test_no_inbox(self, tmp_workspace: Path):
        result = check_inbox_health()
        assert result.passed is True
        assert "clean slate" in result.message

    def test_valid_empty(self, tmp_workspace: Path):
        opencode = tmp_workspace / ".opencode"
        opencode.mkdir()
        (opencode / "inbox.json").write_text("[]", encoding="utf-8")
        result = check_inbox_health()
        assert result.passed is True
        assert result.details["total"] == 0

    def test_valid_with_tasks(self, tmp_workspace: Path):
        opencode = tmp_workspace / ".opencode"
        opencode.mkdir()
        tasks = [
            {"id": "t1", "status": "pending"},
            {"id": "t2", "status": "in_progress"},
            {"id": "t3", "status": "pending"},
        ]
        (opencode / "inbox.json").write_text(
            json.dumps(tasks), encoding="utf-8"
        )
        result = check_inbox_health()
        assert result.passed is True
        assert result.details["pending"] == 2
        assert result.details["in_progress"] == 1
        assert result.details["total"] == 3

    def test_invalid_json(self, tmp_workspace: Path):
        opencode = tmp_workspace / ".opencode"
        opencode.mkdir()
        (opencode / "inbox.json").write_text("NOT JSON", encoding="utf-8")
        result = check_inbox_health()
        assert result.passed is False
        assert "Invalid JSON" in result.message


# ---------------------------------------------------------------------------
# check_memory_engine
# ---------------------------------------------------------------------------


class TestCheckMemoryEngine:
    def test_initializes_ok(self, tmp_workspace: Path):
        result = check_memory_engine()
        assert isinstance(result, CheckResult)
        assert result.name == "Memory Engine"
        # Should succeed if MemoryStore can init
        assert isinstance(result.details, dict)

    def test_stats_returned(self, tmp_workspace: Path):
        result = check_memory_engine()
        # details should contain memory type counts
        if result.passed:
            for mem_type in ("episodic", "semantic", "procedural",
                             "relational", "temporal", "aggregate"):
                assert mem_type in result.details


# ---------------------------------------------------------------------------
# check_disk_space
# ---------------------------------------------------------------------------


class TestCheckDiskSpace:
    def test_returns_check_result(self):
        result = check_disk_space()
        assert isinstance(result, CheckResult)
        assert result.name == "Disk Space"

    def test_has_free_gb(self):
        result = check_disk_space()
        assert "free_gb" in result.details
        assert "total_gb" in result.details
        assert isinstance(result.details["free_gb"], float)

    def test_message_format(self):
        result = check_disk_space()
        assert "GB free" in result.message


# ---------------------------------------------------------------------------
# check_cost_tracker
# ---------------------------------------------------------------------------


class TestCheckCostTracker:
    def test_no_log(self, tmp_workspace: Path):
        result = check_cost_tracker()
        assert result.passed is True
        assert "No cost log" in result.message

    def test_with_log(self, tmp_workspace: Path):
        results_dir = tmp_workspace / "results"
        results_dir.mkdir()
        log_file = results_dir / "cost_log.jsonl"
        log_file.write_text(
            '{"model":"gpt-4","cost":0.01}\n{"model":"gpt-4","cost":0.02}\n',
            encoding="utf-8",
        )
        result = check_cost_tracker()
        assert result.passed is True
        assert result.details["record_count"] == 2


# ---------------------------------------------------------------------------
# check_llm_providers
# ---------------------------------------------------------------------------


class TestCheckLLMProviders:
    def test_returns_check_result(self):
        result = check_llm_providers()
        assert isinstance(result, CheckResult)
        assert result.name == "LLM Providers"

    def test_providers_in_details(self):
        result = check_llm_providers()
        assert "ollama" in result.details
        assert "openai" in result.details
        assert "anthropic" in result.details

    def test_key_status(self):
        result = check_llm_providers()
        # Without env vars, providers should report no_key (which is acceptable)
        for provider in ("openai", "anthropic"):
            assert result.details[provider]["status"] in ("ok", "no_key")

    @patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test", "ANTHROPIC_API_KEY": "sk-ant-test"})
    def test_all_keys_set(self):
        result = check_llm_providers()
        assert result.details["openai"]["status"] == "ok"
        assert result.details["anthropic"]["status"] == "ok"

    @patch.dict("os.environ", {"OLLAMA_HOST": "http://localhost:11434"})
    @patch("httpx.get", side_effect=Exception("connection refused"))
    def test_ollama_unreachable(self, _mock_get):
        result = check_llm_providers()
        assert result.details["ollama"]["status"] == "unreachable"


# ---------------------------------------------------------------------------
# run_all_checks
# ---------------------------------------------------------------------------


class TestRunAllChecks:
    def test_returns_all_checks(self):
        results = run_all_checks()
        assert len(results) >= 14  # 6 original + 8 new

    def test_all_are_check_result(self):
        results = run_all_checks()
        for r in results:
            assert isinstance(r, CheckResult)

    def test_all_have_names(self):
        results = run_all_checks()
        names = [r.name for r in results]
        assert len(names) == len(set(names)), "Duplicate check names found"

    def test_expected_names_present(self):
        results = run_all_checks()
        names = {r.name for r in results}
        expected = {
            "Registry File",
            "Registry Valid",
            "Models Import",
            "MessageBus",
            "OpenCode Directory",
            "Company Configs",
            "Python Version",
            "Dependencies",
            "Agent Files",
            "Inbox",
            "Memory Engine",
            "Disk Space",
            "Cost Tracker",
            "LLM Providers",
        }
        assert expected.issubset(names), f"Missing: {expected - names}"
