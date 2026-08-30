"""Integration test: cross-process audit append does not lose events.

The AuditWriter uses a per-process ``threading.Lock`` which serialises
threads sharing one writer instance but not two *processes*. This test
spawns multiple processes that each write to the same audit JSONL through
their own ``AuditWriter``, and asserts that no events are silently dropped
(the process-safe sidecar lock closes G1).
"""

from __future__ import annotations

import json
import multiprocessing
from pathlib import Path

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.writer import AuditWriter


def _worker(audit_path: str, process_id: int, count: int) -> None:
    """Append *count* events from a single process to the shared trail."""
    writer = AuditWriter(path=audit_path)
    for i in range(count):
        writer.write(
            AuditEvent(
                event_type=AuditEventType.TOOL_CALL,
                agent_id=f"proc-{process_id}",
                task_id=f"proc-{process_id}-{i}",
                tool="bash",
                args={"cmd": f"echo {process_id}-{i}"},
                result={"exit_code": 0},
            )
        )


def _run_proc_entry(audit_path: str, process_id: int, count: int) -> None:
    """Top-level entry point for :class:`multiprocessing.Process`."""
    _worker(audit_path, process_id, count)


def test_cross_process_append_no_event_loss(tmp_path: Path) -> None:
    audit_path = tmp_path / "audit.jsonl"
    n_processes = 4
    events_per = 25

    processes = [
        multiprocessing.Process(target=_run_proc_entry, args=(str(audit_path), j, events_per))
        for j in range(n_processes)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join(timeout=120)
        assert p.exitcode == 0, f"process exited {p.exitcode}"

    lines = audit_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == n_processes * events_per

    task_ids = {json.loads(line)["task_id"] for line in lines}
    expected = {f"proc-{j}-{i}" for j in range(n_processes) for i in range(events_per)}
    assert task_ids == expected
