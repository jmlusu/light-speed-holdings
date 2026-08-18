"""Regression tests for ApprovalGate reload idempotency (issue #82).

``reload()`` must replace the in-memory request list with what is on disk —
never append to it.  Before the fix, every reload duplicated every request
already persisted in the YAML, so a single request ballooned on each reload.
"""

from __future__ import annotations

from pathlib import Path

from ai_company.orchestrator.approval import ApprovalGate


def test_reload_does_not_duplicate_requests(tmp_path: Path) -> None:
    config = str(tmp_path / "approvals.yaml")
    gate = ApprovalGate(config_path=config)
    gate.request_approval("req-1", "task-1", "agent-a", "deploy", "Deploy to production")

    gate.reload()
    assert len(gate.list_all()) == 1

    gate.reload()
    assert len(gate.list_all()) == 1
    assert gate.get_request("req-1") is not None


def test_reload_preserves_multiple_requests(tmp_path: Path) -> None:
    config = str(tmp_path / "approvals.yaml")
    gate = ApprovalGate(config_path=config)
    for i in range(3):
        gate.request_approval(f"req-{i}", f"task-{i}", f"agent-{i}", "deploy", f"Deploy {i}")

    gate.reload()
    assert len(gate.list_all()) == 3
