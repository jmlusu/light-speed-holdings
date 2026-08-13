"""Report-only performance benchmark for LLM failover + token-bucket limiting.

This suite is NOT a CI gate (posture: reported targets, not gates). It measures
the latency surface T2 (failover within 500ms) and T8 (token-bucket limiter +
circuit breaker after 5 failures) touch under ticket #38:

* failover latency — end-to-end ``LLMClient.execute_task`` time when the primary
  provider in the tier chain fails (simulated) and the fallback answers;
* limiter pacing — ``TokenBucket`` grants and refusal latency under load.

Results appear in the pytest-benchmark summary table in the CI log. No latency
assertion is made, so a slow run never fails the build.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from ai_company.llm.providers.base import (
    ChatResponse,
    LLMProvider,
    LLMProviderError,
)
from ai_company.llm.token_bucket import TokenBucket

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture

pytest.importorskip("pytest_benchmark")

_FAILOVER_TARGET_MS = 500  # T2


@pytest.mark.performance
def test_llm_failover_latency_report_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, benchmark: BenchmarkFixture
) -> None:
    """End-to-end execute_task time when the primary provider fails.

    Simulates a realistic slow-fail primary (250ms partial response then
    failure) falling back to an answering secondary. Fresh client per round so
    circuit-breaker state never accumulates across samples.
    """
    from types import SimpleNamespace
    from unittest.mock import MagicMock

    from ai_company.llm.client import LLMClient

    monkeypatch.chdir(tmp_path)
    _setup_model_files(tmp_path)

    good_response = json.dumps({"plan": [], "result": "ok", "artifacts": []})

    def setup() -> tuple[tuple[LLMClient], dict]:
        client = LLMClient(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
        )

        failing = MagicMock(spec=LLMProvider)
        failing.is_available.return_value = True

        def _fail(*_args, **_kwargs):
            time.sleep(0.25)
            raise LLMProviderError("opencode", "simulated 500", status_code=500)

        failing.chat.side_effect = _fail

        good = MagicMock(spec=LLMProvider)
        good.is_available.return_value = True
        good.chat.return_value = ChatResponse(
            content=good_response, model="deepseek-chat", provider="deepseek"
        )
        client._providers = {"opencode": failing, "deepseek": good}
        client.router.resolve = MagicMock(
            return_value=SimpleNamespace(
                tier="standard", provider="deepseek", model="deepseek-chat"
            )
        )
        client.router.get_tier = MagicMock(
            return_value=SimpleNamespace(
                providers=[
                    SimpleNamespace(provider="opencode", model="big-pickle"),
                    SimpleNamespace(provider="deepseek", model="deepseek-chat"),
                ]
            )
        )
        return (client,), {}

    def failover_run(client: LLMClient) -> str:
        result = client.execute_task("test-agent", "do something", max_retries=2)
        return result["result"]

    result = benchmark.pedantic(failover_run, setup=setup, rounds=5, iterations=1)
    assert result == "ok"
    benchmark.extra_info["target_ms"] = _FAILOVER_TARGET_MS
    benchmark.extra_info["simulated_primary_failure_ms"] = 250


@pytest.mark.performance
def test_llm_limiter_throughput_report_only(benchmark: BenchmarkFixture) -> None:
    """TokenBucket grant throughput at a sustained 10 tokens/sec rate."""

    def burst() -> int:
        bucket = TokenBucket(rate=10.0, capacity=10)
        granted = 0
        for _ in range(10):
            if bucket.try_acquire():
                granted += 1
        return granted

    granted = benchmark(burst)
    assert granted == 10
    benchmark.extra_info["capacity"] = 10


@pytest.mark.performance
def test_llm_limiter_refusal_latency_report_only(benchmark: BenchmarkFixture) -> None:
    """Non-blocking refusal latency when the bucket is empty (no sleep)."""

    def refusal() -> bool:
        bucket = TokenBucket(rate=0.0, capacity=0)
        return bucket.try_acquire()

    ok = benchmark(refusal)
    assert ok is False


def _setup_model_files(tmp_path: Path) -> None:
    """Create minimal models.yaml and registry for testing."""
    (tmp_path / "company").mkdir(exist_ok=True)

    models = {
        "providers": {
            "opencode": {
                "backend": "openai_compatible",
                "default_model": "big-pickle",
                "api_base": "https://opencode.ai/api/v1",
            },
            "deepseek": {
                "backend": "openai_compatible",
                "default_model": "deepseek-chat",
                "api_base": "https://api.deepseek.com/v1",
            },
        },
        "tiers": {
            "standard": {
                "description": "Standard",
                "providers": [
                    {"provider": "opencode", "model": "big-pickle"},
                    {"provider": "deepseek", "model": "deepseek-chat"},
                ],
            },
        },
        "routing": [
            {"agent_type": "Specialist", "tier": "standard"},
        ],
    }
    (tmp_path / "company" / "models.yaml").write_text(json.dumps(models), encoding="utf-8")

    registry = [
        {
            "name": "test-agent",
            "role": "Test Agent",
            "type": "Specialist",
            "department": "Test",
            "reportsTo": "ceo",
            "directReports": [],
            "description": "A test agent",
            "tools": ["read", "write"],
            "permission": "Execute",
        },
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )
