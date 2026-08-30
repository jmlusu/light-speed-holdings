"""Tests for the canonical runtime tool vocabulary and legacy aliases.

Covers the executor/tool_runner dispatch, membership checks, and the
tier_rules classification of the canonical tool set (Sprint 7).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.executor.tool_runner import ToolRunner
from ai_company.orchestrator.tier_rules import (
    TOOL_DEFAULT_TIERS,
    ApprovalTier,
    classify_tool_action,
)

CANONICAL_TOOLS = {"read", "edit", "grep", "list", "bash", "webfetch", "task"}
LEGACY_ALIASES = {"write", "execute", "delegate", "web_search", "websearch"}


class TestToolVocabulary:
    def test_all_tools_contains_canonical_set(self) -> None:
        assert ToolRunner._all_tools() >= CANONICAL_TOOLS

    def test_all_tools_contains_legacy_aliases(self) -> None:
        assert ToolRunner._all_tools() >= LEGACY_ALIASES

    def test_code_interpreter_is_removed(self) -> None:
        assert "code_interpreter" not in ToolRunner._all_tools()

    def test_unknown_tool_returns_error(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=str(tmp_path))
        assert runner._execute_tool("code_interpreter", {})["error"].startswith("Unknown tool")

    def test_legacy_aliases_dispatch_to_canonical_handlers(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        runner = ToolRunner(project_root=str(tmp_path))
        dispatched: list[str] = []

        def handler(tool: str):
            def fn(args: dict, **_kwargs: object) -> dict[str, object]:
                dispatched.append(tool)
                return {"ok": True}

            return fn

        monkeypatch.setattr(runner, "_write", handler("write"))
        monkeypatch.setattr(runner, "_execute", handler("execute"))
        monkeypatch.setattr(runner, "_delegate", handler("delegate"))
        monkeypatch.setattr(runner, "_webfetch", handler("webfetch"))

        assert runner._execute_tool("edit", {}) == {"ok": True}
        assert runner._execute_tool("write", {}) == {"ok": True}
        assert runner._execute_tool("bash", {}) == {"ok": True}
        assert runner._execute_tool("execute", {}) == {"ok": True}
        assert runner._execute_tool("task", {}) == {"ok": True}
        assert runner._execute_tool("delegate", {}) == {"ok": True}
        assert runner._execute_tool("webfetch", {}) == {"ok": True}
        assert runner._execute_tool("web_search", {}) == {"ok": True}
        assert runner._execute_tool("websearch", {}) == {"ok": True}

        assert dispatched == [
            "write",
            "write",
            "execute",
            "execute",
            "delegate",
            "delegate",
            "webfetch",
            "webfetch",
            "webfetch",
        ]

    def test_delegate_alias_flow_through_run_plan(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=str(tmp_path))
        results = runner.run_plan(
            [{"tool": "delegate", "args": {"receiver": "lead-backend", "instruction": "Build API"}}]
        )
        assert results[0]["action"] == "delegate"

    def test_webfetch_rejects_non_http_schemes(self, tmp_path: Path) -> None:
        runner = ToolRunner(project_root=str(tmp_path))
        for url in ("file:///etc/passwd", "javascript:alert(1)", "ftp://example.com/x"):
            result = runner._webfetch({"url": url})
            assert "error" in result


class TestCanonicalTierRules:
    def test_canonical_tools_have_tiers(self) -> None:
        assert TOOL_DEFAULT_TIERS["edit"] == ApprovalTier.SINGLE_APPROVER
        assert TOOL_DEFAULT_TIERS["bash"] == ApprovalTier.SINGLE_APPROVER
        assert TOOL_DEFAULT_TIERS["webfetch"] == ApprovalTier.AUTO_APPROVE
        assert TOOL_DEFAULT_TIERS["task"] == ApprovalTier.NOTIFY

    def test_aliases_share_canonical_tier(self) -> None:
        assert TOOL_DEFAULT_TIERS["edit"] == TOOL_DEFAULT_TIERS["write"]
        assert TOOL_DEFAULT_TIERS["bash"] == TOOL_DEFAULT_TIERS["execute"]
        assert TOOL_DEFAULT_TIERS["webfetch"] == TOOL_DEFAULT_TIERS["web_search"]
        assert TOOL_DEFAULT_TIERS["task"] == TOOL_DEFAULT_TIERS["delegate"]

    def test_bash_command_escalates_on_secret_path(self) -> None:
        result = classify_tool_action("bash", {"command": "cat config/secrets/api_key.txt"})
        assert result == ApprovalTier.CEO_ONLY

    def test_bash_command_escalates_on_dangerous_command(self) -> None:
        result = classify_tool_action("bash", {"command": "rm -rf /"})
        assert result != ApprovalTier.AUTO_APPROVE

    def test_webfetch_is_auto_approved(self) -> None:
        assert classify_tool_action("webfetch", {"url": "https://example.com"}) == (
            ApprovalTier.AUTO_APPROVE
        )
