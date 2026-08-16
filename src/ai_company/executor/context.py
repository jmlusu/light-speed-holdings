"""Context Assembly Engine — parses agent spec cards and builds LLM prompts."""

from __future__ import annotations

import contextlib
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# Name of the shared standards doc generated next to the agents directory.
# Agent cards reference this file instead of duplicating the Operating
# Principles block; parsers fall back to it when a card omits the section.
SHARED_STANDARDS_FILENAME = "operating-standards.md"


class Severity(str, Enum):
    """Severity levels for agent spec validation issues."""

    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass(frozen=True)
class ValidationIssue:
    """A single issue found while validating an agent spec.

    Attributes:
        field: The spec field the issue applies to (e.g. ``mission``).
        severity: ERROR (blocking — CI must fail) or WARNING (advisory).
        message: Human-readable description of the problem.
    """

    field: str
    severity: Severity
    message: str


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

    def validate(self) -> list[ValidationIssue]:
        """Validate the agent context for required fields.

        Checks the critical fields (mission, responsibilities, tools, name,
        role, type) plus advisory sections, and returns a list of
        ``ValidationIssue`` objects. Missing mission or responsibilities are
        ERROR-severity; missing tools/role/name/type and advisory sections are
        WARNING-severity. Issues are also surfaced through the logging module so
        malformed specs never degrade silently.
        """
        issues: list[ValidationIssue] = []

        # Critical fields — ERROR if missing: an agent without a mission or
        # responsibilities silently degrades into a generic prompt.
        if not self.mission or not self.mission.strip():
            issues.append(
                ValidationIssue("mission", Severity.ERROR, "Missing required field: mission")
            )
        if not self.responsibilities:
            issues.append(
                ValidationIssue(
                    "responsibilities",
                    Severity.ERROR,
                    "Missing required field: responsibilities (empty list)",
                )
            )

        # Critical fields — WARNING if missing: the spec still works but the
        # agent loses capability or identity context.
        if not self.tools:
            issues.append(
                ValidationIssue(
                    "tools",
                    Severity.WARNING,
                    "Missing required field: tools (empty list)",
                )
            )
        if not self.name or not self.name.strip():
            issues.append(ValidationIssue("name", Severity.WARNING, "Missing required field: name"))
        if not self.role or not self.role.strip():
            issues.append(ValidationIssue("role", Severity.WARNING, "Missing required field: role"))
        if not self.type or self.type == "Unknown":
            issues.append(
                ValidationIssue("type", Severity.WARNING, "Agent type is missing or Unknown")
            )

        # Advisory sections — WARNING if missing.
        if not self.guidelines or not self.guidelines.strip():
            issues.append(
                ValidationIssue("guidelines", Severity.WARNING, "Missing operating guidelines")
            )
        if not self.success_metrics:
            issues.append(
                ValidationIssue("success_metrics", Severity.WARNING, "Missing success metrics")
            )
        if not self.operating_principles:
            issues.append(
                ValidationIssue(
                    "operating_principles",
                    Severity.WARNING,
                    "Missing operating principles",
                )
            )
        if not self.description or not self.description.strip():
            issues.append(ValidationIssue("description", Severity.WARNING, "Missing description"))
        if not self.department:
            issues.append(ValidationIssue("department", Severity.WARNING, "Missing department"))
        if not self.reports_to:
            issues.append(ValidationIssue("reports_to", Severity.WARNING, "Missing reports_to"))

        if issues:
            logger.warning(
                "Agent spec validation found %d issue(s) for %s: %s",
                len(issues),
                self.name or "<unnamed>",
                "; ".join(f"{i.severity.value}:{i.field} - {i.message}" for i in issues),
            )

        return issues


# Reverse map of OpenCode v2 permission keys -> internal executor tool names.
# Emits only the canonical runtime vocabulary (AGENTS.md section 8):
# read, edit, grep, list, bash, webfetch, task. ``websearch`` maps to the
# canonical ``webfetch`` (backward-compatible alias).
_PERMISSION_TO_TOOLS: dict[str, list[str]] = {
    "read": ["read"],
    "edit": ["edit"],
    "bash": ["bash"],
    "grep": ["grep"],
    "list": ["list"],
    "task": ["task"],
    "webfetch": ["webfetch"],
    "websearch": ["webfetch"],
    "question": ["question"],
}


def _derive_tools(frontmatter: dict) -> list[str]:
    """Build the executor tool list from an agent spec's frontmatter.

    OpenCode v2 files express tool access via a ``permission`` block (tool ->
    allow/ask/deny) and omit the legacy ``tools`` list. The executor's prompts
    need the internal tool vocabulary, so we prefer a legacy ``tools`` list when
    present, otherwise derive tools from the ``permission`` block.
    """
    legacy_tools = frontmatter.get("tools")
    if isinstance(legacy_tools, list) and legacy_tools:
        return [str(t) for t in legacy_tools]

    permission = frontmatter.get("permission")
    if not isinstance(permission, dict):
        return []

    tools: list[str] = []
    seen: set[str] = set()
    for key in sorted(permission):
        if permission[key] not in ("allow", "ask"):
            continue
        for tool in _PERMISSION_TO_TOOLS.get(key, [key]):
            if tool not in seen:
                seen.add(tool)
                tools.append(tool)
    return tools


def _derive_permission_str(frontmatter: dict) -> str:
    permission = frontmatter.get("permission", "")
    if isinstance(permission, dict):
        allowed = sorted(k for k, v in permission.items() if v in ("allow", "ask"))
        return ", ".join(allowed) if allowed else ""
    return str(permission) if permission is not None else ""


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
    shared_standards_path = Path(agents_dir).parent / SHARED_STANDARDS_FILENAME
    return parse_agent_spec_content(content, agent_name, shared_standards_path)


def _load_shared_standards(path: str | Path) -> dict[str, str]:
    """Load the shared standards doc's sections, if the file exists."""
    shared_path = Path(path)
    if not shared_path.exists():
        return {}
    try:
        return _parse_sections(shared_path.read_text(encoding="utf-8"))
    except OSError:
        logger.warning("Could not read shared standards doc: %s", shared_path)
        return {}


def parse_agent_spec_content(
    content: str,
    agent_name: str,
    shared_standards_path: str | Path | None = None,
) -> AgentContext:
    """Parse an agent spec card from an already-loaded string into an AgentContext.

    This is the in-memory variant of :func:`parse_agent_spec`; callers that
    already hold the rendered content (e.g. the generator during regeneration)
    use it to avoid re-reading files from disk. It extracts:
    - YAML frontmatter → tools, permission, mode
    - Markdown sections → mission, responsibilities, guidelines, etc.

    When ``shared_standards_path`` is provided, sections the agent card no
    longer duplicates inline (e.g. Operating Principles, now referenced via a
    shared doc) are resolved from that file.
    """
    # Parse YAML frontmatter
    frontmatter: dict = {}
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        with contextlib.suppress(yaml.YAMLError):
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}

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

    # Agent cards now reference the shared standards doc instead of duplicating
    # the Operating Principles block. Fall back to it when the card omits the
    # section so validation and prompt building behave as before.
    if not operating_principles and shared_standards_path is not None:
        shared = _load_shared_standards(shared_standards_path)
        raw_op = shared.get("operating principles", "")
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
        role=frontmatter.get("description", agent_name).split(".")[0]
        if frontmatter.get("description")
        else agent_name,
        type=agent_type,
        department=department,
        reports_to=reports_to,
        mission=sections.get("mission", "").strip(),
        responsibilities=responsibilities,
        guidelines=sections.get("operating guidelines", "").strip(),
        tools=_derive_tools(frontmatter),
        permission=_derive_permission_str(frontmatter),
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
