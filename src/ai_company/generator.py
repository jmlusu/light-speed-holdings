"""Generator: reads company-registry.yaml, produces OpenCode agent .md files.

Supports template selection based on agent type and multi-format output.
"""

from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

from ai_company.executor.context import (
    SHARED_STANDARDS_FILENAME,
    Severity,
    parse_agent_spec_content,
)
from ai_company.registry import load_registry
from ai_company.registry.loader import load_yaml_cached
from ai_company.store import repo_write

logger = logging.getLogger(__name__)

# Tool name mapping: registry names → OpenCode v2 permission keys
# Legacy aliases (websearch, edit) are kept so older
# registries still normalize to the same permission keys as their canonical
# counterparts (web_search, write).
_TOOL_MAP: dict[str, str] = {
    "execute": "bash",
    "edit": "edit",
    "write": "edit",
    "web_search": "webfetch",
    "websearch": "webfetch",
    "delegate": "task",
    "question": "question",
    "read": "read",
    "grep": "grep",
    "list": "list",
}

# Template selection mapping
_TEMPLATE_MAP = {
    "executive": "executive.md.j2",
    "department": "department.md.j2",
    "specialist": "specialist.md.j2",
    "board": "board.md.j2",
    "workflow": "workflow.md.j2",
    "config": "config.md.j2",
    "agent": "agents/agent.md.j2",  # OpenCode v2 permission format
    "default": "base.md.j2",
}


class AgentGenerator:
    """Single-source generator that reads company-registry.yaml and produces agent .md files."""

    def __init__(
        self,
        registry_path: str = "company-registry.yaml",
        templates_dir: str = "templates",
        output_dir: str = ".opencode/agents",
        table_path: str = "docs/AGENT-REGISTRY-TABLE.md",
    ) -> None:
        self.registry_path = Path(registry_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.table_path = Path(table_path)

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

    def _write_shared_standards(self) -> Path:
        """Write the shared standards doc next to the agents directory.

        Agent cards reference ``../operating-standards.md`` instead of
        duplicating the Operating Principles block inline. Returns the
        destination path.
        """
        src = self.templates_dir / "agents" / "operating-standards.md"
        dest = self.output_dir.parent / SHARED_STANDARDS_FILENAME
        if src.exists():
            repo_write.write_file(dest, src.read_text(encoding="utf-8"))
        else:
            logger.warning(
                "Shared standards template not found: %s (skipping %s)",
                src,
                dest,
            )
        return dest

    @staticmethod
    def _normalize_tools(tools: list[str]) -> list[str]:
        """Normalize tool names from registry format to OpenCode v2 permission keys."""
        return [_TOOL_MAP.get(t, t) for t in tools]

    @staticmethod
    def _build_permission(tools: list[str]) -> dict[str, str]:
        """Build an OpenCode permission block from registry tool names.

        Only granted tools are included, each mapped to ``allow``.
        """
        keys = sorted({_TOOL_MAP.get(tool, tool) for tool in tools})
        return {key: "allow" for key in keys}

    def validate_generated(self) -> list[dict[str, str]]:
        """Validate all generated agent files for OpenCode v2 compliance.

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

            # Required fields (OpenCode v2 shape)
            for field in ("description", "mode", "permission"):
                if field not in frontmatter:
                    errors.append({"file": filepath.name, "error": f"Missing field: {field}"})

            # Forbidden fields (deprecated in the v2 format)
            for field in ("tools",):
                if field in frontmatter:
                    errors.append({"file": filepath.name, "error": f"Forbidden field: {field}"})

            # Mode validation
            mode = frontmatter.get("mode")
            if mode and mode not in ("primary", "subagent"):
                errors.append({"file": filepath.name, "error": f"Invalid mode: {mode!r}"})

            # Permission validation: dict of tool → allow/ask/deny
            permission = frontmatter.get("permission")
            if permission is not None and not isinstance(permission, dict):
                errors.append({"file": filepath.name, "error": "permission must be a dict"})
            elif isinstance(permission, dict):
                for tool, action in permission.items():
                    if isinstance(action, str) and action not in ("allow", "ask", "deny"):
                        errors.append(
                            {
                                "file": filepath.name,
                                "error": f"Invalid permission action for {tool!r}: {action!r}",
                            }
                        )

        return errors

    def validate_naming(self) -> list[dict[str, str]]:
        """Validate that all generated agent filenames use hyphens, not underscores.

        Returns list of {file, error} dicts. Empty list means all valid.
        """
        errors: list[dict[str, str]] = []
        if not self.output_dir.exists():
            return [{"file": "*", "error": "Output directory does not exist"}]

        for filepath in sorted(self.output_dir.glob("*.md")):
            stem = filepath.stem
            if "_" in stem:
                errors.append(
                    {
                        "file": filepath.name,
                        "error": f"Filename contains underscores: use '{stem.replace('_', '-')}' instead",
                    }
                )

        return errors

    def load_registry(self) -> dict[str, Any] | list[Any]:
        """Load registry from the local YAML file (for backward compatibility with tests)."""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path.absolute()}")
        data = load_yaml_cached(self.registry_path)
        if data is None:
            raise ValueError(f"Registry is empty: {self.registry_path}")
        return data

    def generate_all(self, clean: bool = True, use_full_registry: bool = False) -> list[Path]:
        """Run full generation. Returns list of generated file paths.

        Args:
            clean: Whether to clean output directory before generation.
            use_full_registry: If True, use the full validated registry pipeline (CompanyRegistry model).
                If False (default), use the local registry YAML file for backward compatibility.
        """
        if clean and self.output_dir.exists():
            for existing in self.output_dir.glob("*.md"):
                existing.unlink()

        if use_full_registry:
            # Load validated registry through the full pipeline (loader -> parser -> resolver -> validator)
            registry = load_registry()
            return self.generate_from_registry(registry)
        else:
            # Use local registry YAML file (backward compatible)
            return self._generate_from_local_registry()

    def _generate_from_local_registry(self) -> list[Path]:
        """Generate from local registry YAML (original behavior)."""
        self._write_shared_standards()
        data = self.load_registry()
        if isinstance(data, list):
            agents = data
            company_name = "AI Company"
        else:
            agents = data.get("company", {}).get("agents", [])
            company_name = data.get("company", {}).get("name", "AI Company")

        logger.info("Generating %d agents for %s", len(agents), company_name)

        generated: list[Path] = []
        rendered_specs: list[tuple[str, str]] = []
        for agent in agents:
            agent_type = agent.get("type", "default")
            template = self._get_template(agent_type)
            # Normalize tools to OpenCode v2 permission keys and build permission block
            raw_tools = agent.get("tools", [])
            if isinstance(raw_tools, list):
                agent["tools"] = self._normalize_tools(raw_tools)
                agent["permission"] = self._build_permission(raw_tools)
            rendered = template.render(company=company_name, **agent)
            safe_id = agent["id"].replace("_", "-")
            out_file = self.output_dir / f"{safe_id}.md"
            repo_write.write_file(out_file, rendered)
            generated.append(out_file)
            rendered_specs.append((safe_id, rendered))
            logger.debug("Wrote: %s (type=%s)", out_file, agent_type)

        logger.info("Generation complete: %d agents.", len(generated))

        # Keep docs/AGENT-REGISTRY-TABLE.md in sync (CI drift check verifies).
        table_path = self.generate_agent_table(output_path=str(self.table_path))
        logger.info("Generated agent registry table: %s", table_path)

        # Validate generated agents against the in-memory rendered content
        # (avoids re-reading all generated files from disk).
        shared_standards = self.output_dir.parent / SHARED_STANDARDS_FILENAME
        validation_errors = self._validate_generated_agents(rendered_specs, shared_standards)
        if validation_errors:
            logger.warning("Agent validation found issues:")
            for err in validation_errors:
                logger.warning("  %s", err)
        else:
            logger.info("All generated agents passed validation.")

        return generated

    def _department_order(self) -> list[str]:
        """Canonical department display order from ``company/departments.yaml``."""
        order: list[str] = []
        depts_path = Path("company/departments.yaml")
        if depts_path.exists():
            data = load_yaml_cached(depts_path)
            if isinstance(data, dict):
                for dept in data.get("departments", []):
                    name = dept.get("name")
                    if name:
                        order.append(name)
        return order

    @staticmethod
    def _display_reports_to(reports_to: Any) -> str:
        """Render the reports-to column value for the registry table."""
        if not reports_to:
            return "None"
        if reports_to == "human_ceo":
            return "CEO"
        if reports_to == "board":
            return "Board"
        return f"`{str(reports_to).replace('_', '-')}`"

    @staticmethod
    def _display_direct_reports(direct_reports: Any) -> str:
        """Render the direct-reports column value for the registry table."""
        if not direct_reports:
            return "None"
        ids = [f"`{str(rid).replace('_', '-')}`" for rid in direct_reports]
        return ", ".join(ids)

    @staticmethod
    def _display_responsibilities(responsibilities: Any) -> str:
        """Render the responsibilities column value for the registry table."""
        if not responsibilities:
            return "None"
        if isinstance(responsibilities, str):
            return responsibilities
        parts: list[str] = []
        for resp in responsibilities:
            if isinstance(resp, dict):
                parts.extend(f"{key}: {value}" for key, value in resp.items())
            else:
                parts.append(str(resp))
        return "; ".join(parts)

    def generate_agent_table(self, output_path: str = "docs/AGENT-REGISTRY-TABLE.md") -> Path:
        """Generate a markdown agent registry table grouped by department.

        Reads the registry (source of truth), groups agents by department in
        the canonical order from ``company/departments.yaml`` (departments not
        listed there are appended alphabetically), and renders a per-department
        table with a global agent numbering. Wired into :meth:`generate_all`
        so ``docs/AGENT-REGISTRY-TABLE.md`` stays in sync and the CI drift
        check verifies it. Returns the written path.
        """
        dest = Path(output_path)
        registry = load_registry()
        # Combine all agent types from the validated registry
        all_agents = []
        for ex in registry.executives:
            agent_dict = {
                "id": ex.id,
                "name": ex.name or ex.id,
                "department": ex.department,
                "reports_to": ex.reports_to,
                "direct_reports": [],
                "responsibilities": ex.responsibilities,
            }
            all_agents.append(agent_dict)
        for spec in registry.specialists:
            agent_dict = {
                "id": spec.id,
                "name": spec.name or spec.id,
                "department": spec.department,
                "reports_to": spec.reports_to,
                "direct_reports": [],
                "responsibilities": spec.responsibilities,
            }
            all_agents.append(agent_dict)
        for bm in registry.board:
            agent_dict = {
                "id": bm.id,
                "name": bm.name or bm.id,
                "department": "Board",
                "reports_to": "",
                "direct_reports": [],
                "responsibilities": bm.responsibilities,
            }
            all_agents.append(agent_dict)
        company_name = registry.company.name

        agents = all_agents
        groups: dict[str, list[dict[str, Any]]] = {}
        for agent in agents:
            dept = str(agent.get("department") or "Unassigned")
            groups.setdefault(dept, []).append(agent)

        order = self._department_order()
        ordered_depts = [dept for dept in order if dept in groups]
        ordered_depts += sorted(dept for dept in groups if dept not in order)

        lines = [
            f"# Agent Registry — {company_name}",
            "",
            "> **Source**: `company-registry.yaml`",
            f"> **Total Agents**: {len(agents)} across {len(groups)} departments",
            f"> **Generated**: {datetime.datetime.now(datetime.timezone.utc).date().isoformat()}",
            "",
            "---",
            "",
        ]

        number = 0
        for dept in ordered_depts:
            dept_agents = sorted(groups[dept], key=lambda a: str(a.get("id", "")))
            count = len(dept_agents)
            label = "agent" if count == 1 else "agents"
            lines.append(f"## {dept} ({count} {label})")
            lines.append("")
            lines.append(
                "| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |"
            )
            lines.append(
                "|---|----------|-----------|------------|----------------|-----------------|"
            )
            for agent in dept_agents:
                number += 1
                lines.append(
                    "| {n} | `{aid}` | {name} | {reports} | {direct} | {resp} |".format(
                        n=number,
                        aid=str(agent.get("id", "")).replace("_", "-"),
                        name=str(agent.get("name", "")),
                        reports=self._display_reports_to(agent.get("reports_to")),
                        direct=self._display_direct_reports(agent.get("direct_reports")),
                        resp=self._display_responsibilities(agent.get("responsibilities")),
                    )
                )
            lines.append("")

        dest.parent.mkdir(parents=True, exist_ok=True)
        repo_write.write_file(dest, "\n".join(lines).rstrip() + "\n")
        logger.info("Wrote agent registry table: %s (%d agents)", dest, len(agents))
        return dest

    def _validate_generated_agents(
        self,
        specs: list[tuple[str, str]],
        shared_standards_path: Path | None = None,
    ) -> list[str]:
        """Validate generated agent specs for required fields.

        Each spec is a ``(agent_name, rendered_content)`` pair so validation
        runs against the in-memory render instead of re-reading the generated
        files from disk. Runs ``AgentContext.validate()`` on every spec,
        logging each WARNING-severity issue at warning level and each
        ERROR-severity issue at error level ("log loudly"). Returns a list of
        ERROR-severity messages (empty list means no blocking issues).
        Generation itself never fails on validation output; callers decide how
        to surface the errors.

        ``shared_standards_path`` points at the shared standards doc written by
        :meth:`_write_shared_standards`, so cards that reference Operating
        Principles instead of inlining them still resolve during validation.
        """
        errors: list[str] = []
        for agent_name, content in specs:
            context = parse_agent_spec_content(
                content, agent_name, shared_standards_path=shared_standards_path
            )
            issues = context.validate()
            for issue in issues:
                if issue.severity is Severity.ERROR:
                    errors.append(f"{agent_name}: {issue.message}")
                    logger.error(
                        "Generated agent '%s' has ERROR-severity spec issue: %s",
                        agent_name,
                        issue.message,
                    )
                else:
                    logger.warning(
                        "Generated agent '%s' has WARNING-severity spec issue: %s",
                        agent_name,
                        issue.message,
                    )
        return errors

    def generate_from_registry(self, registry: Any) -> list[Path]:
        """Generate agent files from a CompanyRegistry model."""
        generated: list[Path] = []
        rendered_specs: list[tuple[str, str]] = []
        self._write_shared_standards()

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
                permission=self._build_permission(ex.tools),
                agent_type="Executive",
            )
            safe_id = ex.id.replace("_", "-")
            out_file = self.output_dir / f"{safe_id}.md"
            repo_write.write_file(out_file, rendered)
            generated.append(out_file)
            rendered_specs.append((safe_id, rendered))

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
            safe_id = dept.id.replace("_", "-")
            out_file = self.output_dir / f"dept-{safe_id}.md"
            repo_write.write_file(out_file, rendered)
            generated.append(out_file)
            rendered_specs.append((f"dept-{safe_id}", rendered))

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
                permission=self._build_permission(spec.tools),
                seniority=spec.seniority.value,
                agent_type="Specialist",
            )
            safe_id = spec.id.replace("_", "-")
            out_file = self.output_dir / f"spec-{safe_id}.md"
            repo_write.write_file(out_file, rendered)
            generated.append(out_file)
            rendered_specs.append((f"spec-{safe_id}", rendered))

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
            safe_id = bm.id.replace("_", "-")
            out_file = self.output_dir / f"board-{safe_id}.md"
            repo_write.write_file(out_file, rendered)
            generated.append(out_file)
            rendered_specs.append((f"board-{safe_id}", rendered))

        logger.info("Generated %d agent files from registry.", len(generated))

        # Validate generated agents against the in-memory rendered content
        shared_standards = self.output_dir.parent / SHARED_STANDARDS_FILENAME
        validation_errors = self._validate_generated_agents(rendered_specs, shared_standards)
        if validation_errors:
            logger.warning("Agent validation found issues:")
            for err in validation_errors:
                logger.warning("  %s", err)
        else:
            logger.info("All generated agents passed validation.")

        return generated
