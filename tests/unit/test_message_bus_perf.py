"""Report-only performance benchmark for the hardened JSON ``MessageBus``.

This suite is NOT a CI gate (posture: reported targets, not gates). It measures
the latency surface T1 (event-driven spec) touches under ticket #34, decision
"keep the file-based bus":

* executor-tick read latency (``MessageBus.get_pending_tasks``) over a 127-task
  inbox — benchmarked with pytest-benchmark (idempotent read path);
* one-shot fan-out claim latency across 127 agent channels — measured once via
  ``benchmark.pedantic(rounds=1)`` on a fresh inbox per round, since ``claim_task``
  mutates state and must not run repeatedly against the same inbox.

Results appear in the pytest-benchmark summary table in the CI log. No latency
assertion is made, so a slow run never fails the build.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from ai_company.models.task import Task
from ai_company.orchestrator.message_bus import MessageBus

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture

pytest.importorskip("pytest_benchmark")

AGENTS = 127


def _populate(bus: MessageBus, n: int) -> None:
    for i in range(n):
        bus.send_task(
            Task(
                id=f"msg-{i}",
                sender_id="orchestrator",
                receiver_id=f"agent-{i}",
                instruction=f"fan-out task {i}",
            )
        )


@pytest.mark.performance
def test_message_bus_read_latency_report_only(tmp_path: Path, benchmark: BenchmarkFixture) -> None:
    """Executor-tick read latency: load + filter a 127-task inbox (idempotent)."""
    bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
    _populate(bus, AGENTS)

    pending = bus.get_pending_tasks()
    assert len(pending) == AGENTS

    result = benchmark(bus.get_pending_tasks)

    # Correctness only — no latency gate.
    assert len(result) == AGENTS
    benchmark.extra_info["agents"] = AGENTS


@pytest.mark.performance
def test_message_bus_claim_fanout_latency_report_only(
    tmp_path: Path, benchmark: BenchmarkFixture
) -> None:
    """One-shot fan-out claim latency across 127 agent channels.

    ``claim_task`` mutates state (pending -> in_progress), so the fresh inbox is
    rebuilt per round via ``pedantic``'s ``setup`` and the call is measured for a
    single round only.
    """

    def setup() -> tuple[tuple[MessageBus], dict]:
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        _populate(bus, AGENTS)
        return (bus,), {}

    def fanout_claim(bus: MessageBus) -> int:
        claimed = 0
        for task in bus.get_pending_tasks():
            if bus.claim_task(task.id, task.receiver_id, lease_seconds=1800):
                claimed += 1
        return claimed

    total = benchmark.pedantic(fanout_claim, setup=setup, rounds=1, iterations=1, warmup_rounds=0)

    # Correctness only — no latency gate.
    assert total == AGENTS
    benchmark.extra_info["agents"] = AGENTS


def _single_send(bus: MessageBus, n: int) -> None:
    for i in range(n):
        bus.send_task(
            Task(
                id=f"msg-{i}",
                sender_id="orchestrator",
                receiver_id=f"agent-{i}",
                instruction=f"fan-out task {i}",
            )
        )


@pytest.mark.performance
def test_message_bus_write_latency_report_only(tmp_path: Path, benchmark: BenchmarkFixture) -> None:
    """Write (send_task) latency p95 across 127 enqueues on a fresh inbox.

    ``send_task`` mutates state (append), so each round gets a fresh bus via
    ``pedantic``'s ``setup``; the benchmark measures the full loop so p95 is
    per-send latency over the batch.
    """

    def setup() -> tuple[tuple[MessageBus], dict]:
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        return (bus,), {}

    def enqueue_batch(bus: MessageBus) -> int:
        _single_send(bus, AGENTS)
        return len(bus.get_all_tasks())

    total = benchmark.pedantic(enqueue_batch, setup=setup, rounds=1, iterations=1, warmup_rounds=0)

    assert total == AGENTS
    benchmark.extra_info["agents"] = AGENTS
    benchmark.extra_info["operation"] = "send_task"


@pytest.mark.performance
def test_message_bus_throughput_report_only(tmp_path: Path, benchmark: BenchmarkFixture) -> None:
    """Sustained throughput (tasks/sec) under a repeating enqueue+claim cycle.

    Measures the full send->claim round-trip cost per task over a 127-task
    batch; throughput is reported as tasks/sec in the benchmark's "ops/s"
    column, so no separate assertion is needed.
    """

    def setup() -> tuple[tuple[MessageBus], dict]:
        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        return (bus,), {}

    def send_and_claim(bus: MessageBus) -> int:
        _single_send(bus, AGENTS)
        claimed = 0
        for task in bus.get_pending_tasks():
            if bus.claim_task(task.id, task.receiver_id, lease_seconds=1800):
                claimed += 1
        return claimed

    total = benchmark.pedantic(send_and_claim, setup=setup, rounds=1, iterations=1, warmup_rounds=0)

    assert total == AGENTS
    benchmark.extra_info["agents"] = AGENTS
    benchmark.extra_info["operation"] = "send+claim"
    benchmark.extra_info["units"] = "tasks/sec"
