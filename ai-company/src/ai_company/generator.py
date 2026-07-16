"""Generator: reads company-registry.yaml, produces OpenCode agent .md files.

Supports template selection based on agent type and multi-format output.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

# Template selection mapping
_TEMPLATE_MAP = {
    "executive": "executive.md.j2",
    "department": "department.md.j2",
    "specialist": "specialist_v2.md.j2",
    "board": "board_v2.md.j2",
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
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_template(self, agent_type: str = "default") -> Any:
        """Get the appropriate template for an agent type."""
        template_name = _TEMPLATE_MAP.get(agent_type, _TEMPLATE_MAP["default"])
        return self.env.get_template(template_name)

    def load_registry(self) -> dict[str, Any]:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path.absolute()}")
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def generate_all(self) -> list[Path]:
        """Run full generation. Returns list of generated file paths."""
        data = self.load_registry()
        agents = data.get("company", {}).get("agents", [])
        company_name = data.get("company", {}).get("name", "AI Company")

        print(f"Generating {len(agents)} agents for {company_name}...")

        generated: list[Path] = []
        for agent in agents:
            agent_type = agent.get("type", "default")
            template = self._get_template(agent_type)
            rendered = template.render(company=company_name, **agent)
            out_file = self.output_dir / f"{agent['id']}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)
            print(f"  Wrote: {out_file} (type={agent_type})")

        print(f"Generation complete: {len(generated)} agents.")
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
                term_start=bm.term_start,
                term_end=bm.term_end,
                agent_type="Board",
            )
            out_file = self.output_dir / f"board_{bm.id}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)

        print(f"Generated {len(generated)} agent files from registry.")
        return generated
