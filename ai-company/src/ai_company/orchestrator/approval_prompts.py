"""Prompt templates for the 5-tier approval system.

Each tier has:
- A system prompt for the LLM to classify tool actions into tiers
- A notification template for human approvers
- An escalation template for timeouts

Usage
-----
    >>> from ai_company.orchestrator.approval_prompts import build_notification
    >>> msg = build_notification(2, {"tool": "write", "args": {"path": "src/main.py"}})
"""

from __future__ import annotations

from typing import Any

# The tier_rules module is used indirectly via the prompt builder functions;
# the imports are kept for downstream convenience.
from ai_company.orchestrator.tier_rules import (  # noqa: F401
    ApprovalTier,
    classify_tool_action,
    get_tier_config,
)

# ---------------------------------------------------------------------------
# Tier classification prompt
# ---------------------------------------------------------------------------

TIER_CLASSIFICATION_PROMPT = """\
You are an approval-tier classifier for an AI agent hierarchy. Your job is to \
determine which of five approval tiers an agent's tool action belongs to.

The five tiers are:

Tier 0 (Auto-Approve):
- Read-only tools: read, list, grep, glob, search, ping, view
- No human approval needed
- Action executes immediately

Tier 1 (Notify):
- Low-risk writes: config file edits, documentation changes, template changes
- Auto-approved, but humans are notified
- Paths: config/, docs/, .github/, *.md, *.rst, *.txt, *.cfg, *.ini, *.toml

Tier 2 (Single Approver):
- Code changes, test execution, model training, file creation/modification in src/
- One human must approve
- Paths: src/, tests/, app/, lib/, api/, requirements files

Tier 3 (Two-Person Rule):
- Production deployments, database schema changes, infrastructure changes
- Two humans must approve
- Paths: deploy/, terraform/, k8s/, Dockerfile, scripts/deploy
- Commands: docker push, kubectl apply, terraform apply, npm publish

Tier 4 (CEO Only):
- Financial transactions, legal actions, security changes, secrets management
- CEO must approve
- Paths: secrets/, security/, audit/, legal/, compliance/
- Commands: rm -rf /, drop/create/alter database, sql delete

Rules for classification:
1. Start with the tool's default tier (read/list/grep = 0, write/edit = 2, etc.)
2. Escalate by path: sensitive paths escalate to 4, production paths to 3, code paths to 2
3. Escalate by command: dangerous commands escalate to 4, production commands to 3
4. Consider agent seniority: executives may auto-approve tiers <= 2
5. Consider task context: high-risk or critical tasks demand stricter tiers
6. The final tier is the highest of all applicable tiers.

Respond with the tier number only (0-4)."""

# ---------------------------------------------------------------------------
# Per-tier notification templates
# ---------------------------------------------------------------------------

TIER_NOTIFICATIONS: dict[int, str] = {
    0: """\
[Auto-Approved] Tier 0 action completed.
Tool: {tool}
Args: {args_summary}
Agent: {agent_id}
This action required no human approval and has been executed automatically.""",
    #
    1: """\
[Notification] Tier 1 action approved and executed.
Action: {action_description}
Tool: {tool}
Args: {args_summary}
Agent: {agent_id}
This was a low-risk write that was auto-approved. No action required from you.""",
    #
    2: """\
[Approval Required] Tier 2 - Single Approver
Action: {action_description}
Tool: {tool}
Args: {args_summary}
Agent: {agent_id}
Requested at: {timestamp}
Expires at: {expires_at}

Please review and respond:
- Approve: ai-company approval approve {request_id} --by "<your-name>"
- Reject:  ai-company approval reject {request_id} --by "<your-name>" --notes "<reason>"

If no response within {timeout_minutes} minutes, this request will be escalated.""",
    #
    3: """\
[Approval Required] Tier 3 - Two-Person Rule
Action: {action_description}
Tool: {tool}
Args: {args_summary}
Agent: {agent_id}
Requested at: {timestamp}
Expires at: {expires_at}

This action requires TWO approvers. Each approver must independently review and approve.

To approve as approver 1:
  ai-company approval approve {request_id} --by "<your-name>"
To approve as approver 2 (after approver 1):
  ai-company approval approve {request_id} --by "<your-name>"

To reject:
  ai-company approval reject {request_id} --by "<your-name>" --notes "<reason>"

If no response within {timeout_minutes} minutes, this request will be escalated.""",
    #
    4: """\
[Approval Required] Tier 4 - CEO Only
Action: {action_description}
Tool: {tool}
Args: {args_summary}
Agent: {agent_id}
Requested at: {timestamp}
Expires at: {expires_at}

This action requires CEO approval.

To approve:
  ai-company approval approve {request_id} --by "ceo" --notes "<notes>"
To reject:
  ai-company approval reject {request_id} --by "ceo" --notes "<reason>"

If no response within {timeout_minutes} minutes, this request will be escalated.""",
}

# ---------------------------------------------------------------------------
# Escalation templates
# ---------------------------------------------------------------------------

ESCALATION_TEMPLATES: dict[int, str] = {
    2: """\
[Escalation] Tier 2 approval request has TIMED OUT.
Request ID: {request_id}
Action: {action_description}
Tool: {tool}
Agent: {agent_id}
Requested at: {timestamp}
Timeout: {timeout_minutes} minutes

The assigned approver did not respond in time. This request is now escalated to {escalated_to}.

{escalated_to}, please review and respond:
- Approve: ai-company approval approve {request_id} --by "<your-name>"
- Reject:  ai-company approval reject {request_id} --by "<your-name>" --notes "<reason>"
""",
    #
    3: """\
[Escalation] Tier 3 approval request has TIMED OUT.
Request ID: {request_id}
Action: {action_description}
Tool: {tool}
Agent: {agent_id}
Requested at: {timestamp}
Timeout: {timeout_minutes} minutes

The required two-person approval was not completed in time. This request is now \
escalated to {escalated_to}.

{escalated_to}, please review and respond:
- Approve: ai-company approval approve {request_id} --by "<your-name>" [requires 2 approvers]
- Reject:  ai-company approval reject {request_id} --by "<your-name>" --notes "<reason>"
- Delegate: assign a secondary approver to unblock this request
""",
    #
    4: """\
[Escalation] Tier 4 CEO approval request has TIMED OUT.
Request ID: {request_id}
Action: {action_description}
Tool: {tool}
Agent: {agent_id}
Requested at: {timestamp}
Timeout: {timeout_minutes} minutes

The CEO did not respond in time. This request is now escalated to {escalated_to}.

{escalated_to}, this action requires CEO-level authority. Options:
- Approve as CEO deputy: ai-company approval approve {request_id} --by "<your-name>"
- Reject: ai-company approval reject {request_id} --by "<your-name>" --notes "<reason>"
- Re-escalate to Board of Directors for final decision
""",
}

# ---------------------------------------------------------------------------
# Dashboard summary prompt
# ---------------------------------------------------------------------------

DASHBOARD_SUMMARY_PROMPT = """\
You are the approval dashboard summariser. Your job is to provide a concise overview \
of the current approval queue for human operators.

Structure your response in this format:

  # Approval Dashboard

  ## Summary
  - Total pending: {total_pending}
  - Tier 4 (CEO): {tier_4_count}
  - Tier 3 (Two-Person): {tier_3_count}
  - Tier 2 (Single Approver): {tier_2_count}
  - Tier 1 (Notify-only): {tier_1_count}

  ## Urgent Actions
  {urgent_items}

  ## Escalated Items
  {escalated_items}

  ## Recommendations
  {recommendations}

Rules:
- Highlight items that are close to their timeout SLA.
- Highlight Tier 4 and Tier 3 items first.
- If an item has been pending for more than 50% of its SLA, flag it as "at risk".
- If an item has exceeded its SLA, flag it as "overdue".
- Keep each item summary to 1-2 lines.

Input data:
{queue_data}"""


# ---------------------------------------------------------------------------
# Helpers for building prompt strings
# ---------------------------------------------------------------------------


def _summarise_args(args: dict[str, Any], max_chars: int = 120) -> str:
    """Build a human-readable summary of tool arguments.

    Parameters
    ----------
    args:
        The tool arguments dictionary.
    max_chars:
        Maximum length of the summary before truncation.

    Returns
    -------
    str
        A compact representation of the arguments.
    """
    parts: list[str] = []
    for key, value in args.items():
        if isinstance(value, str):
            # Truncate long strings individually.
            v = value if len(value) <= 80 else value[:77] + "..."
            parts.append(f"{key}={v}")
        elif isinstance(value, (int, float, bool)):
            parts.append(f"{key}={value}")
        elif isinstance(value, list):
            parts.append(f"{key}=[{len(value)} items]")
        elif isinstance(value, dict):
            parts.append(f"{key}={{{len(value)} keys}}")
        else:
            parts.append(f"{key}={type(value).__name__}")

    summary = ", ".join(parts)
    if len(summary) > max_chars:
        summary = summary[: max_chars - 3] + "..."
    return summary


def build_tier_classification_prompt(
    tool: str,
    args: dict[str, Any],
    context: dict[str, Any],
) -> str:
    """Build a prompt to classify a tool action into an approval tier.

    The prompt includes the tool name, the arguments, and any relevant
    task context (seniority, risk level) for the LLM to use.

    Parameters
    ----------
    tool:
        The tool name (e.g. ``read``, ``write``, ``execute``).
    args:
        The arguments dict for the tool action.
    context:
        Task context (e.g. ``{"seniority": "mid", "risk_level": "low"}``).

    Returns
    -------
    str
        A complete prompt for the LLM classifier.
    """
    args_summary = _summarise_args(args)
    seniority = context.get("seniority", "unknown")
    risk_level = context.get("risk_level", "unknown")

    return f"""\
{TIER_CLASSIFICATION_PROMPT}

Input:
- Tool: {tool}
- Args: {args_summary}
- Agent seniority: {seniority}
- Task risk level: {risk_level}

Tier (0-4):"""


def build_notification(tier: int, request: dict[str, Any]) -> str:
    """Build a human-readable notification for an approval request.

    Parameters
    ----------
    tier:
        The approval tier number (0-4).
    request:
        A dictionary with keys: ``request_id``, ``tool``, ``args``, ``agent_id``,
        ``action_description``, ``timestamp``, ``expires_at``, and optionally
        ``timeout_minutes``.

    Returns
    -------
    str
        A formatted notification string for the human approver.

    Raises
    ------
    KeyError
        If no notification template is registered for the given tier.
    """
    template = TIER_NOTIFICATIONS.get(tier)
    if template is None:
        msg = f"No notification template registered for tier {tier}"
        raise KeyError(msg)

    args_summary = _summarise_args(request.get("args", {}))
    timeout_minutes = request.get("timeout_minutes", 0)

    return template.format(
        tool=request.get("tool", "unknown"),
        args_summary=args_summary,
        agent_id=request.get("agent_id", "unknown"),
        action_description=request.get("action_description", "No description provided"),
        request_id=request.get("request_id", "unknown"),
        timestamp=request.get("timestamp", "unknown"),
        expires_at=request.get("expires_at", "unknown"),
        timeout_minutes=timeout_minutes,
    )


def build_escalation(
    tier: int,
    request: dict[str, Any],
    timeout_minutes: int,
    escalated_to: str = "chief-of-staff",
) -> str:
    """Build an escalation message when an approval request times out.

    Parameters
    ----------
    tier:
        The approval tier number (2-4).
    request:
        A dictionary with keys: ``request_id``, ``tool``, ``args``, ``agent_id``,
        ``action_description``, ``timestamp``.
    timeout_minutes:
        The timeout duration in minutes.
    escalated_to:
        The agent or person to whom the request is escalated.

    Returns
    -------
    str
        A formatted escalation message.

    Raises
    ------
    KeyError
        If no escalation template is registered for the given tier.
    """
    template = ESCALATION_TEMPLATES.get(tier)
    if template is None:
        msg = f"No escalation template registered for tier {tier}"
        raise KeyError(msg)

    args_summary = _summarise_args(request.get("args", {}))

    return template.format(
        request_id=request.get("request_id", "unknown"),
        action_description=request.get("action_description", "No description provided"),
        tool=request.get("tool", "unknown"),
        args_summary=args_summary,
        agent_id=request.get("agent_id", "unknown"),
        timestamp=request.get("timestamp", "unknown"),
        timeout_minutes=timeout_minutes,
        escalated_to=escalated_to,
    )
