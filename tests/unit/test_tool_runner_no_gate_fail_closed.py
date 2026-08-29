"""Fail-closed security test for ToolRunner without a hitl_gate.

Verifies GAP-003/security hardening: when a tool step needs tier-2+ HITL but
NO ``hitl_gate`` was supplied and the action is not preapproved, ``run_plan``
must raise ``HITLParked`` (fail-closed) instead of warning and executing the
tool without any human approval.

Specifically:
- ``HITLParked`` is raised with a ``no_gate_tier_*`` request id.
- The tool is NOT executed — the file it would have written does not exist.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.executor.tool_runner import HITLParked, ToolRunner


@pytest.fixture(autouse=True)
def _anchor_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Anchor DASHBOARD_DATA_DIR so default-constructed MessageBus / AuditWriter
    stay inside the per-test tmp dir instead of the real project dir."""
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))


def test_run_plan_fails_closed_when_no_gate_supplied(tmp_path: Path) -> None:
    """A tier-2 (write) action with no hitl_gate must park, not execute."""
    runner = ToolRunner(project_root=tmp_path)
    target = tmp_path / "should_never_exist.txt"

    with pytest.raises(HITLParked) as exc_info:
        runner.run_plan(
            [{"tool": "write", "args": {"path": str(target), "content": "x"}}],
            hitl_gate=None,
            task_id="t-fail-closed",
            agent_id="junior_dev",
            seniority="",  # empty -> cannot auto-approve tier 2
            non_blocking=True,
        )

    parked = exc_info.value
    assert parked.task_id == "t-fail-closed"
    assert parked.agent_id == "junior_dev"
    assert parked.tool == "write"
    assert parked.tier == 2
    assert parked.request_id.startswith("no_gate_tier_2_")

    # The tool must NOT have executed: the file it would have written is absent.
    assert not target.exists()
