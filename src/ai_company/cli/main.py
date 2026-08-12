"""
Main CLI entry point for AI Company Builder.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any, cast

import typer
from typer.core import TyperGroup


def _init_logging() -> None:
    """Configure structured logging once, on first CLI invocation."""
    from ai_company.logging_config import setup_logging

    setup_logging()


def _load_subapp(module: str, attr: str) -> typer.Typer:
    """Import a sub-command module lazily and return its Typer app."""
    import importlib

    return cast(typer.Typer, getattr(importlib.import_module(module), attr))


# name -> (module, app attribute, help text). Imported lazily on first use so
# ``ai-company --help`` / ``ai-company status`` never import every subcommand.
_LAZY_SUB_APPS: dict[str, tuple[str, str, str]] = {
    "agents": ("ai_company.cli.agents", "app", "Manage AI agents"),
    "board": ("ai_company.cli.board", "app", "Manage Board of Directors"),
    "bootstrap": (
        "ai_company.cli.bootstrap",
        "app",
        "Prepare a new developer machine (idempotent)",
    ),
    "governance": (
        "ai_company.cli.governance",
        "app",
        "Data governance — ownership, retention, compliance",
    ),
    "workflows": ("ai_company.cli.workflows", "app", "Manage workflows"),
    "memory": ("ai_company.cli.memory", "app", "Manage company memory"),
    "executives": ("ai_company.cli.executives", "app", "Manage executives"),
    "departments": ("ai_company.cli.departments", "app", "Manage departments"),
    "doctor": ("ai_company.cli.doctor", "app", "Run system diagnostics"),
    "marketing": ("ai_company.cli.marketing", "app", "Marketing operations"),
    "sales": ("ai_company.cli.sales", "app", "Sales operations"),
    "customer-success": ("ai_company.cli.customer_success", "app", "Customer Success operations"),
    "legal": ("ai_company.cli.legal", "app", "Legal operations"),
    "llm": ("ai_company.cli.llm", "app", "LLM usage and cost tracking"),
    "hr": ("ai_company.cli.hr", "app", "Human Resources operations"),
    "specialists": ("ai_company.cli.specialists", "app", "Manage specialist agents"),
    "orchestrator": ("ai_company.cli.orchestrator", "app", "Autonomous coordination"),
    "models": ("ai_company.cli.models", "app", "Model routing policy"),
    "dashboard": ("ai_company.cli.dashboard", "app", "CEO dashboard"),
    "executor": ("ai_company.cli.executor", "app", "Autonomous task execution"),
    "company": ("ai_company.cli.company", "app", "Bootstrap and manage the AI company"),
    "decision": ("ai_company.cli.decision", "app", "Decision engine — approvals, risk, trees"),
    "graph": ("ai_company.cli.graph", "app", "Graph engine — org chart, knowledge graphs"),
    "security": (
        "ai_company.cli.security",
        "app",
        "Security operations — encryption, key rotation",
    ),
    "validate": (
        "ai_company.cli.validate",
        "app",
        "Validate naming conventions and config references",
    ),
    "client": (
        "ai_company.cli.client",
        "app",
        "Client onboarding and engagement management (Malawi portfolio)",
    ),
}


# Attributes that must reflect the real sub-app. Parse/invoke attributes force
# the lazy import; help-formatting attributes forward only once the group is
# already loaded so the root ``--help`` never imports a subcommand.
_LAZY_FORWARD_ATTRS = frozenset(
    {
        "commands",
        "params",
        "callback",
        "invoke_without_command",
        "no_args_is_help",
        "_result_callback",
        "context_settings",
        "epilog",
        "short_help",
        "options_metavar",
        "hidden",
        "deprecated",
        "subcommand_metavar",
        "suggest_commands",
        "rich_markup_mode",
        "rich_help_panel",
    }
)

_LAZY_LOAD_ATTRS = frozenset(
    {
        "commands",
        "params",
        "callback",
        "invoke_without_command",
        "no_args_is_help",
        "_result_callback",
    }
)


class _LazySubGroup(TyperGroup):
    """A TyperGroup placeholder that imports its module on first use.

    The real sub-app is only loaded (and compiled) when its options or
    subcommands are resolved — e.g. when the user runs ``ai-company <sub>
    ...`` or expands the command tree in tests. Until then, cheap attributes
    (name/help) are served from the placeholder itself.
    """

    def __init__(self, *, name: str, help: str | None, loader: Callable[[], typer.Typer]) -> None:
        self._loader = loader
        self._real_group: TyperGroup | None = None
        super().__init__(name=name, commands={}, help=help)

    def _ensure_loaded(self) -> None:
        real = object.__getattribute__(self, "_real_group")
        if real is not None:
            return
        from typer.main import get_group

        loader = object.__getattribute__(self, "_loader")
        object.__setattr__(self, "_real_group", get_group(loader()))

    def __getattribute__(self, name: str) -> Any:
        if name in _LAZY_FORWARD_ATTRS:
            if name in _LAZY_LOAD_ATTRS:
                self._ensure_loaded()
            real = object.__getattribute__(self, "_real_group")
            if real is not None:
                return getattr(real, name)
        return object.__getattribute__(self, name)


class _LazyGroup(TyperGroup):
    """Root group that injects lazy placeholders for every subcommand."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        for name, (module, attr, help_text) in _LAZY_SUB_APPS.items():
            self.add_command(
                _LazySubGroup(name=name, help=help_text, loader=partial(_load_subapp, module, attr))
            )


app = typer.Typer(
    help="AI Company Builder - Orchestrate AI agent hierarchies",
    cls=_LazyGroup,
    callback=_init_logging,
    invoke_without_command=True,
)


@app.callback(invoke_without_command=True)
def _lazy_init() -> None:
    """Ensure logging is configured before any subcommand runs."""
    _init_logging()


@app.command()
def sop(
    sop_id: str = typer.Argument("", help="SOP ID to view (e.g. SOP-INCIDENT-001)"),
) -> None:
    """View Standard Operating Procedures.

    Args:
        sop_id: SOP ID to view (e.g. SOP-INCIDENT-001). Empty lists all SOPs.
    """
    from pathlib import Path

    docs_dir = Path(__file__).parent.parent.parent / "docs"

    if sop_id:
        # Find SOP by ID in markdown frontmatter
        for md_file in docs_dir.glob("sop-*.md"):
            content = md_file.read_text(encoding="utf-8")
            if f"sop_id: {sop_id}" in content:
                typer.echo(content)
                return
        typer.echo(f"SOP '{sop_id}' not found.")
        raise typer.Exit(1)

    # List available SOPs
    sop_files = sorted(docs_dir.glob("sop-*.md"))
    if not sop_files:
        typer.echo("No SOPs found in docs/")
        return

    typer.echo("Available SOPs")
    typer.echo("=" * 50)
    for f in sop_files:
        content = f.read_text(encoding="utf-8")
        title = ""
        sop_id_val = ""
        for line in content.splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.startswith("sop_id:"):
                sop_id_val = line.split(":", 1)[1].strip()
            if title and sop_id_val:
                break
        typer.echo(f"  {sop_id_val or f.stem}: {title or f.name}")
    typer.echo("")
    typer.echo("Usage: ai-company sop SOP-INCIDENT-001")


@app.command()
def raci(
    raci_id: str = typer.Argument("", help="RACI ID to view (e.g. RACI-HIRING-001)"),
) -> None:
    """View RACI matrices for workflows.

    Args:
        raci_id: RACI ID to view (e.g. RACI-HIRING-001). Empty lists all RACIs.
    """
    from pathlib import Path

    docs_dir = Path(__file__).parent.parent.parent / "docs"

    if raci_id:
        for md_file in docs_dir.glob("raci-*.md"):
            content = md_file.read_text(encoding="utf-8")
            if f"raci_id: {raci_id}" in content:
                typer.echo(content)
                return
        typer.echo(f"RACI '{raci_id}' not found.")
        raise typer.Exit(1)

    raci_files = sorted(docs_dir.glob("raci-*.md"))
    if not raci_files:
        typer.echo("No RACI matrices found in docs/")
        return

    typer.echo("Available RACI Matrices")
    typer.echo("=" * 50)
    for f in raci_files:
        content = f.read_text(encoding="utf-8")
        title = ""
        raci_id_val = ""
        for line in content.splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.startswith("raci_id:"):
                raci_id_val = line.split(":", 1)[1].strip()
            if title and raci_id_val:
                break
        typer.echo(f"  {raci_id_val or f.stem}: {title or f.name}")
    typer.echo("")
    typer.echo("Usage: ai-company raci RACI-HIRING-001")


@app.command("sync-registry")
def sync_registry(
    yaml_path: str = typer.Option(
        "company-registry.yaml",
        help="Path to the source-of-truth YAML registry",
    ),
    json_path: str = typer.Option(
        "company/agent-registry.json",
        help="Path to the output JSON registry for the dashboard",
    ),
    verify: bool = typer.Option(
        False,
        "--verify/--no-verify",
        help="Verify sync after writing (check for drift)",
    ),
) -> None:
    """Sync agent-registry.json from company-registry.yaml (source of truth).

    The dashboard, model_router, executor, and other components read from the
    JSON file. This command regenerates it from the authoritative YAML.

    Args:
        yaml_path: Path to the source-of-truth YAML registry.
        json_path: Path to the output JSON registry for the dashboard.
        verify: Verify sync after writing (check for drift).
    """
    from ai_company.registry.sync import sync_registry as do_sync
    from ai_company.registry.sync import verify_sync

    count = do_sync(yaml_path=yaml_path, json_path=json_path)
    typer.echo(f"Synced {count} agents from {yaml_path} to {json_path}")

    if verify:
        errors = verify_sync(yaml_path=yaml_path, json_path=json_path)
        if errors:
            for err in errors:
                typer.echo(f"DRIFT: {err}", err=True)
            raise typer.Exit(1)
        typer.echo("Verification passed: YAML and JSON are in sync.")


@app.command()
def generate(
    registry: str = typer.Option(
        "company-registry.yaml",
        help="Path to the agent registry YAML (source of truth)",
    ),
) -> None:
    """Regenerate all company files from the single agent registry.

    First syncs agent-registry.json from the YAML, then generates
    OpenCode agent .md files.

    Args:
        registry: Path to the agent registry YAML (source of truth).
    """
    from ai_company.generator import AgentGenerator
    from ai_company.registry.sync import sync_registry as do_sync

    # Always sync JSON from YAML first
    count = do_sync(yaml_path=registry)
    typer.echo(f"Synced {count} agents to company/agent-registry.json")

    gen = AgentGenerator(registry_path=registry)
    results = gen.generate_all()
    typer.echo(f"Done: {len(results)} agent files generated.")


@app.command()
def status() -> None:
    """Show current company status."""
    typer.echo("AI Company Builder Status")
    typer.echo("========================")
    typer.echo("Company: Light Speed Holdings")
    typer.echo("Status: Active")


if __name__ == "__main__":
    app()
