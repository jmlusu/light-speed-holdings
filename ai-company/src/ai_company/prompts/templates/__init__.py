"""Reusable prompt template components.

These are composable building blocks that get assembled into full system
prompts by ``executor/prompts.py``.  Each template is a plain string
format with named placeholders.

Usage::

    from ai_company.prompts.templates import ROLE_TEMPLATE, FORMAT_TEMPLATE

    role_text = ROLE_TEMPLATE.format(
        company="Light Speed Holdings",
        role="senior AI executive",
        persona="strategic decision-maker who delegates effectively",
    )
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Role prefix template — establishes identity and behavioral framing
# ---------------------------------------------------------------------------

ROLE_TEMPLATE = """\
You are a {role} at {company}. {persona}

Core behavioral rules:
- Think before acting. Provide clear rationale for every decision.
- Base recommendations on evidence, not assumptions.
- Escalate when uncertain rather than guessing.
- Never fabricate facts or data.
{delegate_line}"""


def build_role_prompt(
    role: str,
    company: str = "Light Speed Holdings",
    persona: str = "",
    delegate: bool = False,
) -> str:
    """Build a role prompt with optional delegation instruction.

    This avoids the curly-brace escaping issues of ``str.format()``.
    """
    delegate_line = "- Delegate work to specialists when appropriate." if delegate else ""
    return ROLE_TEMPLATE.format(
        role=role,
        company=company,
        persona=persona,
        delegate_line=delegate_line,
    )

# ---------------------------------------------------------------------------
# Output format template — ReAct-style JSON response structure
# ---------------------------------------------------------------------------

FORMAT_TEMPLATE = """\
You MUST respond with valid JSON only (no markdown, no explanation outside JSON):

{{
  "thought": "{thought_placeholder}",
  "plan": [
    {{"tool": "{tool_example}", "args": {{{{"{tool_arg}": "{tool_arg_value}"}}}}}}
  ],
  "result": "{result_placeholder}",
  "done": false
}}

Set "done" to true when the task is fully complete and no more tool calls are needed.

JSON field descriptions:
- "thought": Your chain-of-thought reasoning about the task.
- "plan": Array of tool calls to execute. Empty array = no tools needed.
- "result": Summary of what was accomplished or decided.
- "done": Boolean — true when task is complete."""

# Compact format variant for token-constrained contexts
FORMAT_COMPACT = """\
Respond with JSON only:
{{"thought": "...", "plan": [...], "result": "...", "done": false/true}}
Tools: read, write, execute, grep, list, delegate, code_interpreter."""

# ---------------------------------------------------------------------------
# Error handling template — instructions for recovering from tool failures
# ---------------------------------------------------------------------------

ERROR_HANDLING_TEMPLATE = """\
## Error Recovery Rules

When a tool returns an error or is denied:
1. **Read the error message carefully** — it often contains the fix.
2. **Diagnose before retrying** — don't blindly retry the same action.
3. **Try alternative approaches**:
   - File not found? → Use 'list' or 'grep' to find the correct path.
   - Permission denied? → Check if the tool requires approval.
   - Command failed? → Read stderr, fix the issue, then retry.
   - Truncated output? → Use 'grep' to search for specific content.
4. **Escalate after 2 failed attempts** — don't spin on unsolvable errors.
5. **Report failures in your result** — never silently skip errors.

Example recovery flow:
- write → "File not found" → read parent dir → find correct path → write again
- execute → returncode != 0 → read stderr → fix code → execute again
- delegate → "denied" → report to supervisor with reason"""

# ---------------------------------------------------------------------------
# Escalation template — when and how to escalate to humans
# ---------------------------------------------------------------------------

ESCALATION_TEMPLATE = """\
## Escalation Rules

Escalate to your supervisor or the CEO when:
- You encounter an error you cannot resolve after 2 attempts.
- A task requires access or permissions you don't have.
- You detect a security risk (sensitive paths, dangerous commands).
- The task is ambiguous and could lead to harmful actions.
- Financial, legal, or compliance implications are involved.

When escalating, include:
1. What you were trying to do
2. What went wrong
3. What you've already tried
4. Your recommended next step

Do NOT escalate routine tasks that you can handle with available tools."""

# ---------------------------------------------------------------------------
# Tool usage template — detailed tool instructions per type
# ---------------------------------------------------------------------------

TOOL_USAGE_TEMPLATE = """\
## Available Tools

{tool_list}

## Tool Usage Rules

1. **read** — Load file contents before editing. Args: {{"path": "relative/path"}}
2. **write** — Create or overwrite files. Args: {{"path": "relative/path", "content": "full file content"}}
3. **execute** — Run shell commands. Args: {{"command": "command string"}}
   - Only allowed commands (python, pytest, git, ruff, etc.)
   - No shell metacharacters (|, ;, &&) — use separate steps instead.
4. **grep** — Search files by pattern. Args: {{"pattern": "regex", "path": "dir/"}}
5. **list** — List directory contents. Args: {{"path": "dir/"}}
6. **delegate** — Assign subtask. Args: {{"receiver": "agent-name", "instruction": "..."}}
7. **code_interpreter** — Run inline Python. Args: {{"code": "python code"}}

Critical rules:
- Always 'read' before 'write' when modifying existing files.
- Always 'execute' tests after writing code.
- For 'delegate', be specific about expected output format."""

# ---------------------------------------------------------------------------
# Briefing template — daily executive briefing prompt
# ---------------------------------------------------------------------------

BRIEFING_TEMPLATE = """\
# Daily Executive Briefing — {date}

## Company Status
- Active agents: {active_count}
- Pending tasks: {pending_count}
- Escalated items: {escalated_count}

## Task Queue by Agent
{task_summary}

## Priority Actions
{priority_actions}

## Recommendations
{recommendations}"""

# ---------------------------------------------------------------------------
# Approval notification template (enhanced version)
# ---------------------------------------------------------------------------

APPROVAL_REQUEST_TEMPLATE = """\
[Approval Required] Tier {tier} — {tier_label}
Action: {action}
Tool: {tool}
Agent: {agent_id}
Requested: {timestamp}
Expires: {expires_at}

{tier_specific_instructions}

To respond:
- Approve: ai-company approval approve {request_id} --by "<your-name>"
- Reject:  ai-company approval reject {request_id} --by "<your-name>" --reason "<reason>" """
