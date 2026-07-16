"""BootstrapEngine — generates the full company from a CompanyRegistry.

This is the core engine that takes a parsed CompanyRegistry and produces:
- All agent .md files in .opencode/agents/
- Company config YAMLs (for downstream tooling)
- Directory structure (memory/, knowledge/, projects/, etc.)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ai_company.generator import AgentGenerator
from ai_company.models import CompanyRegistry
from ai_company.registry import load_registry


# Default directory structure for an AI company
COMPANY_DIRS = [
    "memory/episodic",
    "memory/semantic",
    "memory/procedural",
    "memory/relational",
    "memory/temporal",
    "memory/aggregate",
    "knowledge/base",
    "knowledge/decisions",
    "knowledge/playbooks",
    "projects/active",
    "projects/completed",
    "projects/archived",
    "reports/weekly",
    "reports/quarterly",
    "reports/annual",
    "prompts/system",
    "prompts/task",
    "prompts/few-shot",
    "workflows/definitions",
    "workflows/executions",
    "logs/audit",
    "logs/performance",
]


class BootstrapEngine:
    """Generates a complete AI company from a CompanyRegistry."""

    def __init__(
        self,
        config_dir: str | Path = "config",
        output_dir: str | Path = ".opencode",
        templates_dir: str | Path = "templates",
    ) -> None:
        self.config_dir = Path(config_dir)
        self.output_dir = Path(output_dir)
        self.templates_dir = Path(templates_dir)
        self.agents_dir = self.output_dir / "agents"

    def bootstrap(self, registry: CompanyRegistry | None = None) -> dict[str, Any]:
        """Run full bootstrap. Returns a summary of what was created."""
        if registry is None:
            registry = load_registry(self.config_dir)

        summary: dict[str, Any] = {
            "company": registry.company.name,
            "directories": [],
            "agents": [],
            "configs": [],
            "errors": [],
        }

        # 1. Create directory structure
        summary["directories"] = self._create_directories()

        # 2. Generate agent .md files
        summary["agents"] = self._generate_agents(registry)

        # 3. Generate config YAMLs from registry models
        summary["configs"] = self._generate_configs(registry)

        return summary

    def _create_directories(self) -> list[str]:
        """Create the standard company directory structure."""
        created = []
        for rel_path in COMPANY_DIRS:
            full_path = self.output_dir / rel_path
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(rel_path)
        return created

    def _generate_agents(self, registry: CompanyRegistry) -> list[str]:
        """Generate all agent .md files using the Generator."""
        gen = AgentGenerator(
            registry_path="",  # Not used — we use generate_from_registry
            templates_dir=str(self.templates_dir),
            output_dir=str(self.agents_dir),
        )
        generated = gen.generate_from_registry(registry)
        return [str(f.relative_to(self.agents_dir)) for f in generated]

    def _generate_configs(self, registry: CompanyRegistry) -> list[str]:
        """Generate config YAML files from registry models for downstream use."""
        configs_dir = self.output_dir / "config"
        configs_dir.mkdir(parents=True, exist_ok=True)
        generated = []

        # Company summary
        company_data = {
            "id": registry.company.id,
            "name": registry.company.name,
            "legal_name": registry.company.legal_name,
            "industry": registry.company.industry,
            "ceo": registry.company.ceo,
            "mission": registry.company.mission,
            "vision": registry.company.vision,
            "values": registry.company.values,
        }
        self._write_yaml(configs_dir / "company.yaml", company_data)
        generated.append("company.yaml")

        # Org chart (flattened for downstream tools)
        org_chart = {
            "executives": [
                {"id": e.id, "name": e.name, "title": e.title, "department": e.department, "reports_to": e.reports_to}
                for e in registry.executives
            ],
            "departments": [
                {"id": d.id, "name": d.name, "executive": d.executive}
                for d in registry.departments
            ],
            "specialists": [
                {"id": s.id, "name": s.name, "department": s.department, "reports_to": s.reports_to}
                for s in registry.specialists
            ],
        }
        self._write_yaml(configs_dir / "org_chart.yaml", org_chart)
        generated.append("org_chart.yaml")

        # Workflows summary
        workflows_data = {
            "workflows": [
                {"id": w.id, "name": w.name, "trigger": w.trigger, "owner": w.owner, "steps": len(w.steps)}
                for w in registry.workflows
            ]
        }
        self._write_yaml(configs_dir / "workflows.yaml", workflows_data)
        generated.append("workflows.yaml")

        # Governance summary
        governance_data = {
            "approval_matrix": [
                {"action": a.action, "risk_level": a.risk_level, "sla_hours": a.sla_hours}
                for a in registry.approval_matrix
            ],
            "board_size": len(registry.board),
            "committees": len(registry.committees),
        }
        self._write_yaml(configs_dir / "governance.yaml", governance_data)
        generated.append("governance.yaml")

        return generated

    def _write_yaml(self, path: Path, data: Any) -> None:
        """Write data to a YAML file."""
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
