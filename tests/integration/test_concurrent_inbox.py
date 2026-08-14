"""Integration test: concurrent inbox.json mutation with no lost updates.

Spawns many threads that each append a task to the MessageBus inbox and
mutate a task's status concurrently, asserting that no writes are lost and
the JSON remains valid (GAP-002).
"""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Callable

from ai_company.models.task import Task
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.store.file_lock import FileLockError


def _make_task(i: int) -> Task:
    return Task(
        id=f"task-{i}",
        sender_id="ceo",
        receiver_id="worker",
        content=f"work {i}",
        status="pending",
    )


def _retry_op(op: Callable[[], None], errors: list[Exception], label: str) -> None:
    """Run *op*, retrying transient file-lock contention under load.

    The file-backed MessageBus serialises every write through a sidecar
    ``.lock`` file; under heavy concurrent load a thread can occasionally
    exceed the lock timeout and raise :class:`FileLockError`. That is a load
    artifact, not a lost update — the final-state assertions below are the
    real integrity check — so we retry briefly before recording an error.
    """
    for attempt in range(5):
        try:
            op()
            return
        except FileLockError:
            if attempt == 4:
                errors.append(FileLockError(f"{label} failed after retries"))
            time.sleep(0.05 * (attempt + 1))


def test_concurrent_send_and_status_update(tmp_path) -> None:
    inbox = tmp_path / "inbox.json"
    bus = MessageBus(storage_path=str(inbox))

    n_workers = 20
    n_updates_each = 5
    errors: list[Exception] = []

    # Seed one task to update concurrently.
    seed = _make_task(0)
    bus.send_task(seed)

    def sender(worker_id: int) -> None:
        try:
            for i in range(1, n_updates_each + 1):
                _retry_op(
                    lambda wid=worker_id, idx=i: bus.send_task(_make_task(wid * 100 + idx)),
                    errors,
                    f"send {worker_id}:{i}",
                )
        except Exception as exc:  # pragma: no cover - defensive; # noqa: BLE001
            errors.append(exc)

    def status_updater() -> None:
        try:
            for _ in range(n_workers * n_updates_each):
                _retry_op(
                    lambda: bus.update_task_status("task-0", "completed"),
                    errors,
                    "update completed",
                )
                _retry_op(
                    lambda: bus.update_task_status("task-0", "pending"),
                    errors,
                    "update pending",
                )
        except Exception as exc:  # pragma: no cover - defensive; # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=sender, args=(w,)) for w in range(1, n_workers + 1)]
    threads.append(threading.Thread(target=status_updater))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors

    # Validate the file is still valid JSON and all sent tasks are present.
    raw = inbox.read_text(encoding="utf-8")
    data = json.loads(raw)
    ids = {t["id"] for t in data}
    expected = {
        f"task-{w * 100 + i}" for w in range(1, n_workers + 1) for i in range(1, n_updates_each + 1)
    }
    expected.add("task-0")
    assert ids == expected
    assert len(data) == n_workers * n_updates_each + 1


def test_concurrent_acknowledge_no_lost_updates(tmp_path) -> None:
    inbox = tmp_path / "inbox.json"
    bus = MessageBus(storage_path=str(inbox))

    n = 15
    tasks = [_make_task(i) for i in range(n)]
    for t in tasks:
        bus.send_task(t)

    errors: list[Exception] = []

    def ack(agent: str) -> None:
        try:
            for i in range(n):
                bus.acknowledge_task(f"task-{i}", agent)
        except Exception as exc:  # pragma: no cover - defensive; # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=ack, args=(f"a{j}",)) for j in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    for i in range(n):
        t = bus.get_task_by_id(f"task-{i}")
        # At least one agent acknowledged; value must be one of the agents.
        assert t is not None
        assert t.acknowledged_by in {f"a{j}" for j in range(5)}
