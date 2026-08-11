"""Unit tests for GAP-003 tier enforcement in the executor ToolRunner.

These tests verify that tier rules (the 5-tier approval matrix in
``orchestrator.tier_rules``) are enforced by the tool-execution path:

* A low-tier agent (e.g. ``mid`` seniority) attempting a high-tier tool
  (e.g. writing to a sensitive ``secrets`` path) is blocked and routed to
  the HITL gate (``needs_hitl=True``).
* An agent whose seniority authorizes the action's tier passes without
  requiring HITL (``needs_hitl=False``).

Tool side effects are avoided by using ``read`` (auto-approve) for the
passing path and by asserting on the authorization decision dict rather
than executing the gated tool.
"""

from __future__ import annotations

from ai_company.executor.tool_runner import ToolRunner


def test_low_tier_agent_blocked_for_high_tier_tool() -> None:
    """A 'mid' agent writing to a secrets path requires HITL (not authorized)."""
    result = ToolRunner.check_tool_authorization(
        tool_name="write",
        args={"path": "config/secrets.yaml", "content": "x"},
        agent_id="junior_dev",
        seniority="mid",  # max auto-approve tier = 1 (NOTIFY)
        risk_level="medium",
    )

    # Sensitive-path write classifies as Tier 4 (CEO only) -> needs HITL.
    assert result["tier"] == 4
    assert result["needs_hitl"] is True
    assert result["authorized"] is False


def test_authorized_tier_passes_without_hitl() -> None:
    """A 'mid' agent performing an auto-approve read does not need HITL."""
    result = ToolRunner.check_tool_authorization(
        tool_name="read",
        args={"path": "src/main.py"},
        agent_id="mid_dev",
        seniority="mid",
        risk_level="medium",
    )

    # read is Tier 0 (auto-approve) and within the agent's authority.
    assert result["tier"] == 0
    assert result["needs_hitl"] is False
    assert result["authorized"] is True


def test_executive_auto_approves_within_authority() -> None:
    """An 'executive' agent auto-approves a code write within its authority."""
    result = ToolRunner.check_tool_authorization(
        tool_name="write",
        args={"path": "src/app.py", "content": "x"},
        agent_id="ciso",
        seniority="executive",  # max auto-approve tier = 2
        risk_level="medium",
    )

    # Within authority -> de-escalates to NOTIFY (tier 1), no HITL needed.
    assert result["tier"] == 1
    assert result["needs_hitl"] is False
    assert result["authorized"] is True
