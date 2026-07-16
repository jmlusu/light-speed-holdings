"""Context Assembly Engine — parses agent spec cards and builds LLM prompts."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class AgentContext:
    """Parsed representation of an agent's spec card."""

    name: str
    role: str
    type: str  # Board, Executive, Specialist
    department: str = ""
    reports_to: str = ""
    mission: str = ""
    responsibilities: list[str] = field(default_factory=list)
    guidelines: str = ""
    tools: list[str] = field(default_factory=list)
    permission: str = ""  # ReviewOnly, Execute
    description: str = ""
    success_metrics: list[str] = field(default_factory=list)
    operating_principles: list[str] = field(default_factory=list)


def parse_agent_spec(agent_name: str, agents_dir: str = ".opencode/agents") -> AgentContext:
    """Parse an agent's .md spec card into an AgentContext.

    Reads .opencode/agents/{agent_name}.md and extracts:
    - YAML frontmatter → tools, permission, mode
    - Markdown sections → mission, responsibilities, guidelines, etc.
    """
    path = Path(agents_dir) / f"{agent_name}.md"
    if not path.exists():
        return AgentContext(name=agent_name, role=agent_name, type="Unknown")

    content = path.read_text(encoding="utf-8")

    # Parse YAML frontmatter
    frontmatter: dict = {}
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            pass

    # Parse markdown sections
    sections = _parse_sections(content)

    # Extract responsibilities as list
    responsibilities: list[str] = []
    raw_resp = sections.get("responsibilities", "")
    for line in raw_resp.strip().splitlines():
        line = line.strip().lstrip("- ").strip()
        if line:
            responsibilities.append(line)

    # Extract success metrics
    success_metrics: list[str] = []
    raw_sm = sections.get("success metrics", "")
    for line in raw_sm.strip().splitlines():
        line = line.strip().lstrip("- ").strip()
        if line:
            success_metrics.append(line)

    # Extract operating principles
    operating_principles: list[str] = []
    raw_op = sections.get("operating principles", "")
    for line in raw_op.strip().splitlines():
        line = line.strip().lstrip("- ").strip()
        if line:
            operating_principles.append(line)

    # Parse identity section for type, department, reports_to
    identity = sections.get("identity", "")
    agent_type = _extract_field(identity, "Type") or frontmatter.get("type", "Unknown")
    department = _extract_field(identity, "Department") or ""
    reports_to = _extract_field(identity, "Reports To") or ""

    return AgentContext(
        name=agent_name,
        role=frontmatter.get("description", agent_name).split(".")[0] if frontmatter.get("description") else agent_name,
        type=agent_type,
        department=department,
        reports_to=reports_to,
        mission=sections.get("mission", "").strip(),
        responsibilities=responsibilities,
        guidelines=sections.get("operating guidelines", "").strip(),
        tools=frontmatter.get("tools", []),
        permission=frontmatter.get("permission", ""),
        description=frontmatter.get("description", ""),
        success_metrics=success_metrics,
        operating_principles=operating_principles,
    )


def _parse_sections(content: str) -> dict[str, str]:
    """Parse markdown into {section_name: section_content} dict."""
    sections: dict[str, str] = {}
    current_section = ""
    current_content: list[str] = []

    for line in content.splitlines():
        heading_match = re.match(r"^##\s+(.+)$", line)
        if heading_match:
            if current_section:
                sections[current_section] = "\n".join(current_content)
            current_section = heading_match.group(1).strip().lower()
            current_content = []
        elif current_section:
            current_content.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_content)

    return sections


def _extract_field(text: str, field_name: str) -> str:
    """Extract a field value from identity-style text like 'Type: Executive'."""
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith(field_name.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def build_system_prompt(agent: AgentContext) -> str:
    """Build the system prompt from an agent's parsed context.

    Instructs the LLM to respond with structured JSON containing
    a plan (tool steps) and result summary.
    """
    parts = [
        f"You are {agent.role}, a {agent.type} agent at Light Speed Holdings.",
        "",
    ]

    if agent.mission:
        parts.extend(["MISSION:", agent.mission, ""])

    if agent.responsibilities:
        parts.append("RESPONSIBILITIES:")
        for r in agent.responsibilities:
            parts.append(f"- {r}")
        parts.append("")

    if agent.guidelines:
        parts.extend(["OPERATING GUIDELINES:", agent.guidelines, ""])

    if agent.operating_principles:
        parts.append("OPERATING PRINCIPLES:")
        for p in agent.operating_principles:
            parts.append(f"- {p}")
        parts.append("")

    if agent.tools:
        parts.extend([
            "ALLOWED TOOLS:",
            ", ".join(agent.tools),
            "",
        ])

    parts.extend([
        "IMPORTANT RULES:",
        "- You MUST respond with valid JSON only. No markdown, no explanation outside JSON.",
        "- Only use tools from your allowed list.",
        "- For 'write' tool: include the full file content in the 'content' arg.",
        "- For 'execute' tool: include the shell command as a string.",
        "- Be precise and concise. Each step should be self-contained.",
        "- If the task requires no tools, return an empty plan array with your result.",
        "",
        "RESPONSE FORMAT (JSON only):",
        '{',
        '  "plan": [',
        '    {"tool": "read", "args": {"path": "src/example.py"}},',
        '    {"tool": "write", "args": {"path": "src/output.py", "content": "..."}},',
        '    {"tool": "execute", "args": {"command": "pytest tests/"}},',
        '    {"tool": "grep", "args": {"pattern": "def foo", "path": "src/"}},',
        '    {"tool": "list", "args": {"path": "src/"}},',
        '    {"tool": "delegate", "args": {"receiver": "lead-backend", "instruction": "..."}}',
        '  ],',
        '  "result": "Summary of what was accomplished.",',
        '  "artifacts": ["src/output.py"]',
        '}',
    ])

    return "\n".join(parts)


def build_user_prompt(instruction: str, priority: str = "medium") -> str:
    """Build the user prompt from a task instruction and priority."""
    return f"PRIORITY: {priority.upper()}\n\nTASK: {instruction}"
