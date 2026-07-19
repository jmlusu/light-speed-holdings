"""Per-agent-type prompt templates for the multi-turn agentic loop.

Builds on the existing ``context.py`` prompt system by adding typed role
prefixes, tool-specific instructions, and response format guidance keyed
to agent type (Executive, Specialist, Board, Department).
"""

from __future__ import annotations

from typing import Any

from ai_company.executor.context import AgentContext


# ---------------------------------------------------------------------------
# Role prefixes — define the "persona" injected per agent type
# ---------------------------------------------------------------------------

ROLE_PREFIXES: dict[str, str] = {
    "Executive": (
        "You are a senior AI executive at Light Speed Holdings. You make "
        "strategic decisions, set priorities, and delegate work to specialists. "
        "Think before acting. Provide clear rationale for every decision."
    ),
    "Specialist": (
        "You are an expert AI specialist at Light Speed Holdings. You execute "
        "tasks with precision using the tools available to you. Focus on "
        "accuracy and completeness. Validate your work before declaring done."
    ),
    "Board": (
        "You are a member of the Board of Directors at Light Speed Holdings. "
        "You provide governance oversight, review high-level strategy, and "
        "ensure ethical standards. Be thorough and consider stakeholder impact."
    ),
    "Department": (
        "You are an AI department head at Light Speed Holdings. You manage "
        "departmental operations, coordinate specialists, and track KPIs. "
        "Be organized, data-driven, and accountable."
    ),
}

_DEFAULT_ROLE_PREFIX = (
    "You are a capable AI agent at Light Speed Holdings. "
    "Use the tools available to complete your task."
)


# ---------------------------------------------------------------------------
# Tool instructions — per-type guidance on how to use tools
# ---------------------------------------------------------------------------

TOOL_INSTRUCTIONS: dict[str, str] = {
    "Executive": (
        "As an executive you can:\n"
        "- Use 'delegate' to assign work to specialists in your department.\n"
        "- Use 'read', 'list', 'grep' to review reports and data.\n"
        "- Use 'write' to produce strategy documents or memos.\n"
        "- Use 'execute' for approved shell commands.\n"
        "Delegation is your primary tool. Break large tasks into smaller "
        "sub-tasks and assign them to the right specialist."
    ),
    "Specialist": (
        "As a specialist you can:\n"
        "- Use 'read' to load files, 'write' to create/update files.\n"
        "- Use 'execute' to run shell commands (tests, builds, scripts).\n"
        "- Use 'grep' and 'list' to search the codebase.\n"
        "- Use 'code_interpreter' to run inline Python snippets.\n"
        "Read before you write. Test after you write. Iterate until the "
        "task is fully complete."
    ),
    "Board": (
        "As a board member you can:\n"
        "- Use 'read' and 'list' to review documents and reports.\n"
        "- Use 'grep' to search for specific information.\n"
        "Board members primarily review and advise. Use read-only tools "
        "to gather information before providing your assessment."
    ),
    "Department": (
        "As a department head you can:\n"
        "- Use all tools: read, write, execute, grep, list, delegate.\n"
        "- Use 'delegate' to assign tasks to specialists in your team.\n"
        "- Use 'read' and 'grep' to monitor progress and KPIs.\n"
        "Coordinate your team effectively and track deliverables."
    ),
}

_DEFAULT_TOOL_INSTRUCTIONS = (
    "You have access to tools: read, write, execute, grep, list, delegate.\n"
    "Use them to complete your task. Read before writing. Test after writing."
)


# ---------------------------------------------------------------------------
# Response format examples — per-type structured output guidance
# ---------------------------------------------------------------------------

RESPONSE_FORMATS: dict[str, str] = {
    "Executive": (
        "You MUST respond with valid JSON only (no markdown, no explanation):\n"
        "{\n"
        '  "thought": "Your reasoning about the task and what needs to happen.",\n'
        '  "plan": [\n'
        '    {"tool": "delegate", "args": {"receiver": "lead-backend", "instruction": "..."}},\n'
        '    {"tool": "read", "args": {"path": "results/report.md"}}\n'
        '  ],\n'
        '  "result": "Summary of what was accomplished or what you decided.",\n'
        '  "done": false\n'
        "}\n"
        "Set \"done\" to true when the task is fully complete and no more tool calls are needed."
    ),
    "Specialist": (
        "You MUST respond with valid JSON only (no markdown, no explanation):\n"
        "{\n"
        '  "thought": "What you observed and what you plan to do next.",\n'
        '  "plan": [\n'
        '    {"tool": "read", "args": {"path": "src/module.py"}},\n'
        '    {"tool": "write", "args": {"path": "src/output.py", "content": "..."}},\n'
        '    {"tool": "execute", "args": {"command": "pytest tests/"}}\n'
        '  ],\n'
        '  "result": "Summary of what was accomplished.",\n'
        '  "done": false\n'
        "}\n"
        "Set \"done\" to true when the task is fully complete and no more tool calls are needed."
    ),
    "Board": (
        "You MUST respond with valid JSON only (no markdown, no explanation):\n"
        "{\n"
        '  "thought": "Your analysis and assessment of the materials reviewed.",\n'
        '  "plan": [\n'
        '    {"tool": "read", "args": {"path": "docs/strategy.md"}}\n'
        '  ],\n'
        '  "result": "Your board-level assessment and recommendations.",\n'
        '  "done": false\n'
        "}\n"
        "Set \"done\" to true when you have completed your review."
    ),
    "Department": (
        "You MUST respond with valid JSON only (no markdown, no explanation):\n"
        "{\n"
        '  "thought": "What you need to do and why.",\n'
        '  "plan": [\n'
        '    {"tool": "delegate", "args": {"receiver": "agent-name", "instruction": "..."}},\n'
        '    {"tool": "read", "args": {"path": "results/status.md"}}\n'
        '  ],\n'
        '  "result": "Summary of departmental status or actions taken.",\n'
        '  "done": false\n'
        "}\n"
        "Set \"done\" to true when the task is fully complete."
    ),
}

_DEFAULT_RESPONSE_FORMAT = (
    "You MUST respond with valid JSON only (no markdown, no explanation):\n"
    "{\n"
    '  "thought": "What you are thinking.",\n'
    '  "plan": [\n'
    '    {"tool": "tool-name", "args": {"arg1": "value1"}}\n'
    '  ],\n'
    '  "result": "Summary of what was done.",\n'
    '  "done": false\n'
    "}\n"
    "Set \"done\" to true when no more tool calls are needed."
)


# ---------------------------------------------------------------------------
# Iteration instructions — fed back to the LLM after each tool round
# ---------------------------------------------------------------------------

def build_iteration_feedback(
    step_results: list[dict[str, Any]],
    iteration: int,
    max_iterations: int,
) -> str:
    """Format tool execution results as a user message for the next LLM call.

    This is the core of the ReAct loop: after tools run, their results are
    serialized back to the LLM as observations it can reason over.
    """
    parts: list[str] = [
        f"=== Tool Execution Results (iteration {iteration}/{max_iterations}) ===",
        "",
    ]

    for i, result in enumerate(step_results):
        tool = result.get("tool", "unknown")
        status = result.get("status", "unknown")
        parts.append(f"Step {i + 1}: {tool} — status: {status}")

        if status == "error":
            parts.append(f"  Error: {result.get('error', 'unknown error')}")
        elif status == "denied":
            parts.append(f"  Denied: {result.get('error', 'human approval denied')}")
        else:
            # Format successful tool outputs concisely
            for key, value in result.items():
                if key in ("step", "tool", "status"):
                    continue
                text = str(value)
                # Truncate very long outputs to avoid token overflow
                if len(text) > 2000:
                    text = text[:2000] + "\n... [truncated]"
                parts.append(f"  {key}: {text}")
        parts.append("")

    parts.extend([
        "Based on these results, decide your next action.",
        "If the task is complete, set \"done\": true and provide your final result.",
        "Otherwise, respond with your next plan of tool calls.",
    ])

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main prompt builder — assembles the full system prompt
# ---------------------------------------------------------------------------

def build_system_prompt_typed(agent: AgentContext) -> str:
    """Build a system prompt using typed role prefixes and tool instructions.

    This is the enhanced version of ``context.build_system_prompt()`` that
    adds role-specific framing, tool guidance, and ReAct-compatible
    response format instructions.

    The prompt tells the LLM to include a ``thought`` field (chain-of-thought
    reasoning), a ``plan`` array of tool calls, a ``result`` summary, and a
    ``done`` boolean — enabling the multi-turn loop in ``AgentLoop``.
    """
    # Resolve agent type (normalize common variants)
    agent_type = agent.type.strip()
    # Map lowercase / common aliases to canonical keys
    type_map: dict[str, str] = {
        "executive": "Executive",
        "specialist": "Specialist",
        "board": "Board",
        "department": "Department",
    }
    canonical = type_map.get(agent_type.lower(), agent_type)

    role_prefix = ROLE_PREFIXES.get(canonical, _DEFAULT_ROLE_PREFIX)
    tool_instructions = TOOL_INSTRUCTIONS.get(canonical, _DEFAULT_TOOL_INSTRUCTIONS)
    response_format = RESPONSE_FORMATS.get(canonical, _DEFAULT_RESPONSE_FORMAT)

    parts: list[str] = [
        f"# {agent.name}",
        "",
        role_prefix,
        "",
    ]

    # Mission
    if agent.mission:
        parts.extend(["## Mission", agent.mission, ""])

    # Responsibilities
    if agent.responsibilities:
        parts.append("## Responsibilities")
        for r in agent.responsibilities:
            parts.append(f"- {r}")
        parts.append("")

    # Operating guidelines
    if agent.guidelines:
        parts.extend(["## Operating Guidelines", agent.guidelines, ""])

    # Operating principles
    if agent.operating_principles:
        parts.append("## Operating Principles")
        for p in agent.operating_principles:
            parts.append(f"- {p}")
        parts.append("")

    # Success metrics
    if agent.success_metrics:
        parts.append("## Success Metrics")
        for m in agent.success_metrics:
            parts.append(f"- {m}")
        parts.append("")

    # Available tools
    if agent.tools:
        parts.extend([
            "## Available Tools",
            ", ".join(agent.tools),
            "",
        ])

    # Tool usage instructions
    parts.extend(["## Tool Usage", tool_instructions, ""])

    # Response format
    parts.extend([
        "## Response Format",
        response_format,
        "",
        "## Rules",
        "- You MUST respond with valid JSON only. No markdown fences, no prose outside JSON.",
        "- Only use tools from your allowed list.",
        "- For 'write' tool: include the full file content in the 'content' arg.",
        "- For 'execute' tool: include the shell command as a string.",
        "- For 'delegate' tool: include 'receiver' (agent name) and 'instruction'.",
        "- Be precise and concise. Each step should be self-contained.",
        "- If you need to see a file's contents before editing, read it first.",
        "- Set \"done\": true ONLY when the task is fully complete.",
    ])

    return "\n".join(parts)


def build_user_prompt_typed(instruction: str, priority: str = "medium") -> str:
    """Build the initial user prompt for a typed agent loop."""
    return (
        f"PRIORITY: {priority.upper()}\n\n"
        f"TASK: {instruction}\n\n"
        "Analyze the task, think through your approach, and respond with your "
        "first set of tool calls (or mark done if no tools are needed)."
    )
