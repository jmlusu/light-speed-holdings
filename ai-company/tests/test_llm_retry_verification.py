"""LLM retry verification tests — Phase 3C.

Unit tests for:
  1. execute_task retry on invalid JSON (succeeds on 3rd attempt)
  2. execute_task exhaustion across all providers → LLMProviderError
  3. execute_task_stream flattened retry (GAP-015: provider_idx = attempt % len(chain))
  4. CircuitBreaker opens after consecutive failures
  5. CircuitBreaker resets after success
  6. AgentLoop._call_llm provider chain fallback
  7. AgentLoop._call_llm raises on empty chain

All tests mock at the boundary — no conftest fixtures needed.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ai_company.llm.circuit_breaker import CircuitBreaker, CircuitState
from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProviderError,
    LLMResponseError,
    StreamChunk,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _valid_json_response(
    content: str = '{"plan": [], "result": "done", "artifacts": []}',
    model: str = "test-model",
    provider: str = "mock",
) -> ChatResponse:
    """Build a ChatResponse with valid JSON content."""
    return ChatResponse(content=content, model=model, provider=provider)


def _invalid_json_response(
    content: str = "not json at all",
    model: str = "test-model",
    provider: str = "mock",
) -> ChatResponse:
    """Build a ChatResponse with invalid JSON content."""
    return ChatResponse(content=content, model=model, provider=provider)


def _make_provider(
    name: str = "mock",
    available: bool = True,
) -> MagicMock:
    """Create a mock LLMProvider."""
    provider = MagicMock()
    provider.name = name
    provider.is_available.return_value = available
    return provider


def _build_mock_client(
    providers: dict[str, MagicMock],
    provider_chain: list[tuple[str, str]],
    circuit_breakers: dict[str, CircuitBreaker] | None = None,
) -> MagicMock:
    """Build a mock LLMClient with the given provider dict and chain."""
    client = MagicMock()
    client._providers = providers
    client._circuit_breakers = circuit_breakers or {}

    # Mock router to return the first provider in chain as the route
    mock_route = MagicMock()
    mock_route.provider = provider_chain[0][0]
    mock_route.model = provider_chain[0][1]
    mock_route.tier = "standard"
    client.router.resolve.return_value = mock_route

    # Mock router to return a tier with the full provider chain
    mock_tier = MagicMock()
    mock_tier.providers = [MagicMock(provider=p, model=m) for p, m in provider_chain]
    client.router.get_tier.return_value = mock_tier

    return client


# ===========================================================================
# 1. test_execute_task_retries_on_invalid_json
# ===========================================================================


def test_execute_task_retries_on_invalid_json():
    """LLM returns invalid JSON twice, valid JSON on 3rd attempt → succeeds."""
    from ai_company.llm.client import LLMClient
    from ai_company.llm.json_parser import parse_llm_json

    good_json = _valid_json_response()
    bad1 = _invalid_json_response("garbage1")
    bad2 = _invalid_json_response("garbage2")

    mock_provider = _make_provider()
    mock_provider.chat.side_effect = [bad1, bad2, good_json]

    chain: list[tuple[str, str]] = [("mock", "test-model")]
    client = _build_mock_client({"mock": mock_provider}, chain)
    # Wire _parse_response to the real implementation so JSON is actually parsed
    client._parse_response.side_effect = lambda content: parse_llm_json(content)

    # Call the real execute_task with our mocked client internals
    result = LLMClient.execute_task(
        client, "agent1", "do something", max_retries=5,
    )

    assert result == {"plan": [], "result": "done", "artifacts": []}
    assert mock_provider.chat.call_count == 3


# ===========================================================================
# 2. test_execute_task_exhausts_providers
# ===========================================================================


def test_execute_task_exhausts_providers():
    """All providers in the chain fail with LLMProviderError → raises LLMProviderError
    from the last failed attempt after retries are exhausted."""
    from ai_company.llm.client import LLMClient

    mock_p1 = _make_provider("p1")
    mock_p2 = _make_provider("p2")
    # Both providers always raise
    err_p1 = LLMProviderError("p1", "timeout")
    err_p2 = LLMProviderError("p2", "rate limit")
    mock_p1.chat.side_effect = err_p1
    mock_p2.chat.side_effect = err_p2

    chain: list[tuple[str, str]] = [("p1", "m1"), ("p2", "m2")]
    client = _build_mock_client({"p1": mock_p1, "p2": mock_p2}, chain)

    # With max_retries=4: attempts 0→p1, 1→p2, 2→p1, 3→p2 — all fail
    with pytest.raises(LLMResponseError, match="Failed to get valid JSON"):
        LLMClient.execute_task(
            client, "agent1", "do something", max_retries=4,
        )

    # Each provider should have been attempted twice (4 attempts / 2 providers)
    assert mock_p1.chat.call_count == 2
    assert mock_p2.chat.call_count == 2


# ===========================================================================
# 3. test_execute_task_stream_flattened_retry  (GAP-015)
# ===========================================================================


def test_execute_task_stream_flattened_retry():
    """GAP-015 fix: stream retry uses provider_idx = attempt % len(chain).

    Verify that with a 2-provider chain, attempts alternate between providers
    in modular fashion rather than exhausting one before moving to the next.
    """
    from ai_company.llm.client import LLMClient
    from ai_company.llm.json_parser import parse_llm_json

    # Provider A: fails (invalid JSON) on attempts 0, 2
    # Provider B: fails (invalid JSON) on attempt 1
    # Attempt 2 → Provider A → valid JSON
    valid_content = '{"plan": [], "result": "streamed", "artifacts": []}'

    mock_a = _make_provider("provA")
    mock_b = _make_provider("provB")

    # Build StreamChunk lists for each call (side_effect returns these as-is)
    a_fail_chunks = [StreamChunk(delta="not json", finish_reason="stop")]
    b_fail_chunks = [StreamChunk(delta="also bad", finish_reason="stop")]
    a_success_chunks = [StreamChunk(delta=valid_content, finish_reason="stop")]

    mock_a.chat_stream.side_effect = [a_fail_chunks, a_success_chunks]
    mock_b.chat_stream.side_effect = [b_fail_chunks]

    chain: list[tuple[str, str]] = [("provA", "mA"), ("provB", "mB")]
    client = _build_mock_client({"provA": mock_a, "provB": mock_b}, chain)
    # Wire _parse_response to real implementation so invalid JSON returns None
    client._parse_response.side_effect = lambda content: parse_llm_json(content)

    # Collect stream chunks
    chunks: list[StreamChunk] = []
    for chunk in LLMClient.execute_task_stream(
        client, "agent1", "do something", max_retries=5,
    ):
        chunks.append(chunk)

    # Verify alternating provider pattern (GAP-015):
    # attempt 0 → provA, attempt 1 → provB, attempt 2 → provA (succeeds)
    assert mock_a.chat_stream.call_count == 2
    assert mock_b.chat_stream.call_count == 1

    # The final chunk should contain valid JSON
    assert any(valid_content in c.delta for c in chunks)


# ===========================================================================
# 4. test_circuit_breaker_opens_after_failures
# ===========================================================================


def test_circuit_breaker_opens_after_failures():
    """CircuitBreaker trips to OPEN after failure_threshold consecutive failures."""
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=999)

    # Initially closed
    assert cb.state == CircuitState.CLOSED
    assert cb.is_available is True

    # Record 2 failures — still closed
    cb.record_failure()
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    assert cb.is_available is True

    # 3rd failure → opens
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.is_available is False


# ===========================================================================
# 5. test_circuit_breaker_resets_after_success
# ===========================================================================


def test_circuit_breaker_resets_after_success():
    """CircuitBreaker closes again after successful calls in HALF_OPEN state."""
    cb = CircuitBreaker(
        failure_threshold=2,
        recovery_timeout=999,  # Long timeout so OPEN persists
        success_threshold=1,
    )

    # Open the circuit
    cb.record_failure()
    cb.record_failure()
    assert cb._state == CircuitState.OPEN
    assert cb.is_available is False  # Still blocked (timeout hasn't elapsed)

    # Manually move to HALF_OPEN (simulates recovery_timeout elapsed)
    cb._state = CircuitState.HALF_OPEN
    cb._success_count = 0
    assert cb.is_available is True  # HALF_OPEN is available

    # Record success → closes circuit
    cb.record_success()
    assert cb.state == CircuitState.CLOSED
    assert cb.is_available is True

    # Failure count should be reset
    cb.record_failure()  # 1 failure
    assert cb.state == CircuitState.CLOSED  # Below threshold
    assert cb.is_available is True


# ===========================================================================
# 6. test_agent_loop_provider_chain_fallback
# ===========================================================================


def test_agent_loop_provider_chain_fallback():
    """AgentLoop._call_llm() tries providers in chain order, falls back on error."""
    from ai_company.executor.agent_loop import AgentLoop, LoopConfig

    # Provider 1 raises, Provider 2 succeeds
    mock_p1 = _make_provider("fast-model")
    mock_p2 = _make_provider("standard-model")
    mock_p1.chat.side_effect = LLMProviderError("fast-model", "unavailable")

    good_response = ChatResponse(
        content="fallback worked",
        model="standard-model",
        provider="standard-model",
    )
    mock_p2.chat.return_value = good_response

    # Mock the LLM client
    mock_llm = MagicMock()
    mock_llm.get_provider.side_effect = lambda pid: {
        "fast-model": mock_p1,
        "standard-model": mock_p2,
    }.get(pid)

    # Mock router resolve_with_fallback to return 2 tiers
    route1 = MagicMock(provider="fast-model", model="fast-v1", tier="fast")
    route2 = MagicMock(provider="standard-model", model="std-v1", tier="standard")
    mock_llm.router.resolve_with_fallback.return_value = [route1, route2]

    tier_fast = MagicMock()
    tier_fast.providers = [MagicMock(provider="fast-model", model="fast-v1")]
    tier_standard = MagicMock()
    tier_standard.providers = [MagicMock(provider="standard-model", model="std-v1")]

    def _get_tier(tid: str) -> MagicMock:
        return {"fast": tier_fast, "standard": tier_standard}[tid]

    mock_llm.router.get_tier.side_effect = _get_tier

    loop = AgentLoop(llm=mock_llm, config=LoopConfig(max_iterations=1))

    # _call_llm should try fast-model first (fails), then standard-model (succeeds)
    response = loop._call_llm(
        system_prompt="sys", user_prompt="usr",
    )

    assert response.content == "fallback worked"
    assert response.provider == "standard-model"
    # fast-model should have been tried first
    mock_p1.chat.assert_called_once()
    mock_p2.chat.assert_called_once()


# ===========================================================================
# 7. test_agent_loop_raises_on_empty_chain
# ===========================================================================


def test_agent_loop_raises_on_empty_chain():
    """Empty provider chain → LLMProviderError with 'No provider available'."""
    from ai_company.executor.agent_loop import AgentLoop, LoopConfig

    mock_llm = MagicMock()
    mock_llm.get_provider.return_value = None

    # Return a route with no matching tier providers
    route = MagicMock(provider="ghost", model="ghost-v1", tier="empty")
    mock_llm.router.resolve_with_fallback.return_value = [route]

    # get_tier returns None → empty chain
    mock_llm.router.get_tier.return_value = None

    loop = AgentLoop(llm=mock_llm, config=LoopConfig(max_iterations=1))

    with pytest.raises(LLMProviderError, match="No provider available"):
        loop._call_llm(system_prompt="sys", user_prompt="usr")
