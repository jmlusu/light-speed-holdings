"""Unit tests for token counting integration (P1 Sprint 4, item 11.3).

Covers the heuristic token estimator, provider-usage-metadata preference,
CostTracker integration with real token counts, and backward-compatible
replay of old cost_log.jsonl records that lack token fields.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.llm.cost_tracker import CostTracker
from ai_company.llm.providers.base import ChatResponse
from ai_company.llm.token_counter import (
    count_prompt_tokens,
    count_tokens,
    join_prompt,
    usage_from_response,
)

# ── count_tokens heuristic ─────────────────────────────────────────


def test_empty_string_counts_zero() -> None:
    assert count_tokens("") == 0
    assert count_tokens("   \n\t ") == 0


def test_heuristic_magnitude_english() -> None:
    """English text should be roughly 4 chars/token."""
    text = "The quick brown fox jumps over the lazy dog. " * 10  # 450 chars
    tokens = count_tokens(text)
    assert 80 <= tokens <= 160
    assert tokens == pytest.approx(len(text) / 4, rel=0.2)


def test_heuristic_never_zero_for_nonempty() -> None:
    assert count_tokens("hi") >= 1
    assert count_tokens("a") >= 1


def test_heuristic_counts_cjk_chars_individually() -> None:
    """CJK characters cost ~1 token each, not 1 per 4 chars."""
    text = "你好世界"  # 4 CJK chars
    tokens = count_tokens(text, "qwen2.5-coder:14b")
    assert tokens == 4


def test_heuristic_model_family_adjustment() -> None:
    """Model-aware ratios change the estimate for denser tokenizers."""
    text = "word " * 100
    default_tokens = count_tokens(text, "gpt-4o")
    claude_tokens = count_tokens(text, "claude-3-5-sonnet-20241022")
    assert claude_tokens > default_tokens


def test_count_prompt_tokens_joins_system_and_user() -> None:
    system_prompt = "You are a helpful assistant."
    user_prompt = "Summarize this document."
    assert count_prompt_tokens(system_prompt, user_prompt) == count_tokens(
        join_prompt(system_prompt, user_prompt)
    )
    assert count_prompt_tokens("", user_prompt) == count_tokens(user_prompt)
    assert count_prompt_tokens("", "") == 0


# ── usage_from_response (provider metadata vs heuristic) ───────────


def test_usage_from_response_prefers_provider_metadata() -> None:
    response = ChatResponse(
        content="some output",
        model="gpt-4o",
        provider="openai",
        prompt_tokens=123,
        completion_tokens=45,
    )
    usage = usage_from_response(response, "system user", "gpt-4o")
    assert usage.prompt_tokens == 123
    assert usage.completion_tokens == 45
    assert usage.total_tokens == 168


def test_usage_from_response_uses_openai_style_usage_dict() -> None:
    response = ChatResponse(
        content="out",
        model="gpt-4o",
        provider="openai",
        usage={"prompt_tokens": 10, "completion_tokens": 20},
    )
    usage = usage_from_response(response, "", "gpt-4o")
    assert usage.prompt_tokens == 10
    assert usage.completion_tokens == 20
    assert usage.total_tokens == 30


def test_usage_from_response_falls_back_to_heuristic() -> None:
    """Providers without usage metadata get heuristic counts."""
    response = ChatResponse(content="Hello world", model="gpt-4o", provider="openai")
    usage = usage_from_response(response, "system prompt here", "gpt-4o")
    assert usage.prompt_tokens == count_tokens("system prompt here", "gpt-4o")
    assert usage.completion_tokens == count_tokens("Hello world", "gpt-4o")
    assert usage.total_tokens == usage.prompt_tokens + usage.completion_tokens


# ── CostTracker integration ────────────────────────────────────────


def test_cost_tracker_records_real_tokens(tmp_path: Path) -> None:
    tracker = CostTracker(
        results_dir=str(tmp_path / "results"),
        export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
    )
    tracker.record_usage(
        model="gpt-4o-mini",
        provider="openai",
        agent_name="agent-a",
        task_id="task-1",
        prompt_tokens=1000,
        completion_tokens=500,
    )
    record = tracker._records[0]
    assert record.prompt_tokens == 1000
    assert record.completion_tokens == 500
    assert record.total_tokens == 1500

    summary = tracker.get_summary()
    assert summary["total_prompt_tokens"] == 1000
    assert summary["total_completion_tokens"] == 500
    assert summary["total_tokens"] == 1500
    assert summary["call_count"] == 1
    assert summary["total_cost_usd"] > 0


def test_client_record_usage_persists_real_tokens(tmp_path: Path) -> None:
    """LLMClient._record_usage writes real token counts to CostTracker."""
    from ai_company.llm.client import LLMClient

    tracker = CostTracker(
        results_dir=str(tmp_path / "results"),
        export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
    )
    client = LLMClient.__new__(LLMClient)
    client._cost_tracker = tracker

    response = ChatResponse(
        content='{"plan": [], "result": "ok", "artifacts": []}',
        model="gpt-4o",
        provider="openai",
        prompt_tokens=77,
        completion_tokens=13,
    )
    usage = usage_from_response(response, "system user", "gpt-4o")
    client._record_usage(response, "agent-a", "task-1", 1, usage=usage)

    assert tracker._records[0].prompt_tokens == 77
    assert tracker._records[0].completion_tokens == 13
    assert tracker._records[0].cost_usd > 0


def test_client_record_usage_heuristic_fallback(tmp_path: Path) -> None:
    """Without provider metadata, heuristic counts are recorded."""
    from ai_company.llm.client import LLMClient

    tracker = CostTracker(
        results_dir=str(tmp_path / "results"),
        export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
    )
    client = LLMClient.__new__(LLMClient)
    client._cost_tracker = tracker

    response = ChatResponse(
        content='{"plan": [], "result": "ok", "artifacts": []}', model="gpt-4o", provider="openai"
    )
    client._record_usage(
        response,
        "agent-a",
        "task-2",
        1,
        usage=usage_from_response(response, "system user", "gpt-4o"),
    )

    record = tracker._records[0]
    assert record.prompt_tokens == count_tokens("system user", "gpt-4o")
    assert record.completion_tokens == count_tokens(response.content, "gpt-4o")


# ── Backward compatibility ─────────────────────────────────────────


def test_replay_old_log_without_token_fields(tmp_path: Path) -> None:
    """Old cost_log.jsonl records without token fields still load."""
    results = tmp_path / "results"
    results.mkdir(parents=True, exist_ok=True)
    log_path = results / "cost_log.jsonl"
    old_record = {
        "timestamp": "2026-08-01T10:00:00",
        "model": "gpt-4o",
        "provider": "openai",
        "agent_name": "agent-old",
        "task_id": "legacy-task",
        "cost_usd": 0.01,
        "iteration": 1,
        "metadata": {},
    }
    log_path.write_text(json.dumps(old_record) + "\n", encoding="utf-8")

    tracker = CostTracker(
        results_dir=str(results),
        export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
    )
    assert len(tracker._records) == 1
    record = tracker._records[0]
    assert record.task_id == "legacy-task"
    assert record.prompt_tokens == 0
    assert record.completion_tokens == 0
    assert tracker._daily_cost["2026-08-01"] == pytest.approx(0.01)
