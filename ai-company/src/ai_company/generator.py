"""Generator: reads company-registry.yaml, produces OpenCode agent .md files.

Supports template selection based on agent type and multi-format output.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

# Tool name mapping: registry names → OpenCode 1.18.4 names
_TOOL_MAP: dict[str, str] = {
    "execute": "bash",
    "edit": "write",
    "web_search": "webfetch",
    "code_interpreter": "bash",
    "delegate": "task",
}

# Template selection mapping
_TEMPLATE_MAP = {
    "executive": "executive.md.j2",
    "department": "department.md.j2",
    "specialist": "specialist.md.j2",
    "board": "board.md.j2",
    "workflow": "workflow.md.j2",
    "config": "config.md.j2",
    "agent": "agents/agent.md.j2",  # Legacy format
    "default": "base.md.j2",
}


class AgentGenerator:
    """Single-source generator that reads company-registry.yaml and produces agent .md files."""

    def __init__(
        self,
        registry_path: str = "company-registry.yaml",
        templates_dir: str = "templates",
        output_dir: str = ".opencode/agents",
    ) -> None:
        self.registry_path = Path(registry_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)

        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            keep_trailing_newline=True,
            autoescape=False,
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_template(self, agent_type: str = "default") -> Any:
        """Get the appropriate template for an agent type."""
        template_name = _TEMPLATE_MAP.get(agent_type, _TEMPLATE_MAP["default"])
        return self.env.get_template(template_name)

    @staticmethod
    def _normalize_tools(tools: list[str]) -> list[str]:
        """Normalize tool names from registry format to OpenCode 1.18.4 format."""
        return [_TOOL_MAP.get(t, t) for t in tools]

    def validate_generated(self) -> list[dict[str, str]]:
        """Validate all generated agent files for OpenCode 1.18.4 compliance.

        Returns list of {file, error} dicts. Empty list means all valid.
        """
        errors: list[dict[str, str]] = []
        if not self.output_dir.exists():
            return [{"file": "*", "error": "Output directory does not exist"}]

        for filepath in sorted(self.output_dir.glob("*.md")):
            content = filepath.read_text(encoding="utf-8")
            if not content.startswith("---"):
                errors.append({"file": filepath.name, "error": "No YAML frontmatter"})
                continue

            parts = content.split("---", 2)
            if len(parts) < 3:
                errors.append({"file": filepath.name, "error": "Malformed frontmatter"})
                continue

            try:
                frontmatter = yaml.safe_load(parts[1])
            except yaml.YAMLError as e:
                errors.append({"file": filepath.name, "error": f"YAML parse error: {e}"})
                continue

            if not isinstance(frontmatter, dict):
                errors.append({"file": filepath.name, "error": "Frontmatter is not a dict"})
                continue

            # Required fields
            for field in ("description", "mode", "tools"):
                if field not in frontmatter:
                    errors.append({"file": filepath.name, "error": f"Missing field: {field}"})

            # Forbidden fields
            for field in ("name", "permission"):
                if field in frontmatter:
                    errors.append({"file": filepath.name, "error": f"Forbidden field: {field}"})

            # Mode validation
            mode = frontmatter.get("mode")
            if mode and mode not in ("primary", "subagent"):
                errors.append({"file": filepath.name, "error": f"Invalid mode: {mode!r}"})

        return errors

    def load_registry(self) -> dict[str, Any]:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path.absolute()}")
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def generate_all(self) -> list[Path]:
        """Run full generation. Returns list of generated file paths."""
        data = self.load_registry()
        if isinstance(data, list):
            agents = data
            company_name = "AI Company"
        else:
            agents = data.get("company", {}).get("agents", [])
            company_name = data.get("company", {}).get("name", "AI Company")

        logger.info("Generating %d agents for %s", len(agents), company_name)

        generated: list[Path] = []
        for agent in agents:
            agent_type = agent.get("type", "default")
            template = self._get_template(agent_type)
            # Normalize tools to OpenCode 1.18.4 format
            raw_tools = agent.get("tools", [])
            if isinstance(raw_tools, list):
                agent["tools"] = self._normalize_tools(raw_tools)
            rendered = template.render(company=company_name, **agent)
            out_file = self.output_dir / f"{agent['id']}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)
            logger.debug("Wrote: %s (type=%s)", out_file, agent_type)

        logger.info("Generation complete: %d agents.", len(generated))
        return generated

    def generate_from_registry(self, registry: Any) -> list[Path]:
        """Generate agent files from a CompanyRegistry model."""
        generated: list[Path] = []

        # Generate executive agents
        for ex in registry.executives:
            template = self._get_template("executive")
            rendered = template.render(
                company=registry.company.name,
                id=ex.id,
                name=ex.name or ex.id,
                title=ex.title,
                description=ex.mission,
                mission=ex.mission,
                department=ex.department,
                reports_to=ex.reports_to,
                responsibilities=ex.responsibilities,
                decision_rights=ex.decision_rights,
                tools=ex.tools,
                agent_type="Executive",
            )
            out_file = self.output_dir / f"{ex.id}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)

        # Generate department agents
        for dept in registry.departments:
            template = self._get_template("department")
            rendered = template.render(
                company=registry.company.name,
                id=dept.id,
                name=dept.name,
                description=dept.mission,
                mission=dept.mission,
                executive=dept.executive,
                reports_to=dept.executive,
                headcount_target=dept.headcount_target,
                agent_type="Department",
            )
            out_file = self.output_dir / f"dept_{dept.id}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)

        # Generate specialist agents
        for spec in registry.specialists:
            template = self._get_template("specialist")
            rendered = template.render(
                company=registry.company.name,
                id=spec.id,
                name=spec.name or spec.id,
                description=spec.mission,
                mission=spec.mission,
                department=spec.department,
                reports_to=spec.reports_to,
                responsibilities=spec.responsibilities,
                tools=spec.tools,
                seniority=spec.seniority.value,
                agent_type="Specialist",
            )
            out_file = self.output_dir / f"spec_{spec.id}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)

        # Generate board member agents
        for bm in registry.board:
            template = self._get_template("board")
            rendered = template.render(
                company=registry.company.name,
                id=bm.id,
                name=bm.name or bm.id,
                description=bm.role,
                role=bm.role,
                expertise=bm.expertise,
                responsibilities=bm.responsibilities,
                term_start=bm.term_start,
                term_end=bm.term_end,
                agent_type="Board",
            )
            out_file = self.output_dir / f"board_{bm.id}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)

        logger.info("Generated %d agent files from registry.", len(generated))
        return generated
