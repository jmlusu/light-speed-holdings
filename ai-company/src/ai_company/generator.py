"""Generator: reads company-registry.yaml, produces OpenCode agent .md files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader


class AgentGenerator:
    """Single-source generator that reads company-registry.yaml and produces agent .md files."""

    def __init__(
        self,
        registry_path: str = "company-registry.yaml",
        templates_dir: str = "templates/agents",
        output_dir: str = ".opencode/agents",
    ) -> None:
        self.registry_path = Path(registry_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)

        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            keep_trailing_newline=True,
        )
        self.template = self.env.get_template("agent.md.j2")
        self.output_dir.mkdir(parents=True, exist_ok=True)

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
            rendered = self.template.render(company=company_name, **agent)
            out_file = self.output_dir / f"{agent['id']}.md"
            out_file.write_text(rendered, encoding="utf-8")
            generated.append(out_file)
            print(f"  Wrote: {out_file}")

        print(f"Generation complete: {len(generated)} agents.")
        return generated
