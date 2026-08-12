"""CLI command for one-shot project initialization."""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(help="One-shot project initialization (dev setup + generate + company bootstrap)")
console = Console()


@app.callback(invoke_without_command=True)
def init_callback(
    ctx: typer.Context,
    config_dir: str = typer.Option("config", help="Path to config/ directory"),
    registry: str = typer.Option("company-registry.yaml", help="Path to agent registry YAML"),
    skip_dev_setup: bool = typer.Option(
        False, "--skip-dev-setup", help="Skip dev machine bootstrap"
    ),
    skip_generate: bool = typer.Option(False, "--skip-generate", help="Skip agent generation"),
    skip_company_bootstrap: bool = typer.Option(
        False, "--skip-company-bootstrap", help="Skip company bootstrap from config/"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without executing"
    ),
) -> None:
    """Initialize the AI Company project from scratch.

    Runs three phases in sequence:
    1. Dev machine bootstrap (uv, venv, deps, hooks, verify tools)
    2. Generate agents from company-registry.yaml
    3. Company bootstrap from config/ (directories, agents, configs)

    Args:
        config_dir: Path to config/ directory.
        registry: Path to agent registry YAML.
        skip_dev_setup: Skip dev machine bootstrap.
        skip_generate: Skip agent generation.
        skip_company_bootstrap: Skip company bootstrap from config/.
        dry_run: Show what would be done without executing.
    """
    if ctx.invoked_subcommand is not None:
        return

    if dry_run:
        _show_plan(config_dir, registry, skip_dev_setup, skip_generate, skip_company_bootstrap)
        return

    _execute_init(
        config_dir=config_dir,
        registry=registry,
        skip_dev_setup=skip_dev_setup,
        skip_generate=skip_generate,
        skip_company_bootstrap=skip_company_bootstrap,
    )


def _show_plan(
    config_dir: str,
    registry: str,
    skip_dev_setup: bool,
    skip_generate: bool,
    skip_company_bootstrap: bool,
) -> None:
    """Show the initialization plan without executing."""
    from ai_company.registry import load_registry

    console.print("[bold blue]AI Company Initialization Plan[/bold blue]")
    console.print()

    if not skip_dev_setup:
        console.print("[bold]Phase 1: Dev Machine Bootstrap[/bold]")
        console.print("  • Install uv package manager")
        console.print("  • Create .venv virtual environment")
        console.print("  • Sync dependencies (uv sync --extra dev)")
        console.print("  • Install pre-commit hooks")
        console.print("  • Verify Python, Ollama, OpenCode, Git")
        console.print("  • Check required environment variables")
        console.print()

    if not skip_generate:
        console.print("[bold]Phase 2: Agent Generation[/bold]")
        console.print(f"  • Sync agent-registry.json from {registry}")
        console.print("  • Generate OpenCode agent .md files")
        console.print()

    if not skip_company_bootstrap:
        console.print("[bold]Phase 3: Company Bootstrap[/bold]")
        console.print(f"  • Load registry from {config_dir}")
        try:
            reg = load_registry(config_dir)
            console.print(f"  • Company: {reg.company.name}")
            console.print(f"  • Executives: {len(reg.executives)}")
            console.print(f"  • Departments: {len(reg.departments)}")
            console.print(f"  • Specialists: {len(reg.specialists)}")
            console.print(f"  • Workflows: {len(reg.workflows)}")
        except Exception as e:  # noqa: BLE001
            console.print(f"  [yellow]Could not load registry: {e}[/yellow]")
        console.print("  • Create directory structure (memory/, knowledge/, projects/, etc.)")
        console.print("  • Generate agent .md files in .opencode/agents/")
        console.print(
            "  • Generate config YAMLs (company.yaml, org_chart.yaml, workflows.yaml, governance.yaml)"
        )
        console.print()

    console.print("Use [cyan]ai-company init[/cyan] to execute.")


def _execute_init(
    config_dir: str,
    registry: str,
    skip_dev_setup: bool,
    skip_generate: bool,
    skip_company_bootstrap: bool,
) -> None:
    """Execute the full initialization."""
    errors: list[str] = []

    # Phase 1: Dev machine bootstrap
    if not skip_dev_setup:
        console.print("[bold blue]=== Phase 1: Dev Machine Bootstrap ===[/bold blue]")
        try:
            from ai_company.bootstrap import DevBootstrap

            bootstrap = DevBootstrap()
            summary: dict[str, object] = bootstrap.run()
            if not summary.get("ok", False):
                steps = summary.get("steps")
                if isinstance(steps, list):
                    for step in steps:
                        if isinstance(step, dict) and step.get("severity") == "fail":
                            errors.append(f"Dev bootstrap: {step.get('message', '')}")
            console.print("[green]OK[/green] Dev machine bootstrap complete")
        except Exception as e:  # noqa: BLE001
            errors.append(f"Dev bootstrap failed: {e}")
            console.print(f"[red]FAIL[/red] Dev bootstrap failed: {e}")
        console.print()

    # Phase 2: Generate agents
    if not skip_generate:
        console.print("[bold blue]=== Phase 2: Agent Generation ===[/bold blue]")
        try:
            from ai_company.generator import AgentGenerator
            from ai_company.registry.sync import sync_registry as do_sync

            count = do_sync(yaml_path=registry)
            console.print(f"  Synced {count} agents to company/agent-registry.json")

            gen = AgentGenerator(registry_path=registry)
            results = gen.generate_all()
            console.print(f"[green]OK[/green] Generated {len(results)} agent files")
        except Exception as e:  # noqa: BLE001
            errors.append(f"Agent generation failed: {e}")
            console.print(f"[red]FAIL[/red] Agent generation failed: {e}")
        console.print()

    # Phase 3: Company bootstrap
    if not skip_company_bootstrap:
        console.print("[bold blue]=== Phase 3: Company Bootstrap ===[/bold blue]")
        try:
            from ai_company.builder import BootstrapEngine
            from ai_company.registry import load_registry

            reg = load_registry(config_dir)
            engine = BootstrapEngine(config_dir=config_dir)
            bootstrap_summary: dict[str, object] = engine.bootstrap(reg)

            dirs = bootstrap_summary.get("directories")
            agents = bootstrap_summary.get("agents")
            configs = bootstrap_summary.get("configs")
            if isinstance(dirs, list):
                console.print(f"  Directories created: {len(dirs)}")
            if isinstance(agents, list):
                console.print(f"  Agents generated: {len(agents)}")
            if isinstance(configs, list):
                console.print(f"  Configs generated: {len(configs)}")
            console.print("[green]OK[/green] Company bootstrap complete")
        except Exception as e:  # noqa: BLE001
            errors.append(f"Company bootstrap failed: {e}")
            console.print(f"[red]FAIL[/red] Company bootstrap failed: {e}")
        console.print()

    # Summary
    console.print("[bold blue]=== Summary ===[/bold blue]")
    if errors:
        console.print(f"[bold red]{len(errors)} error(s):[/bold red]")
        for err in errors:
            console.print(f"  [red]FAIL[/red] {err}")
        raise typer.Exit(1)
    else:
        console.print("[bold green]Initialization complete![/bold green]")
        console.print()
        console.print("Next steps:")
        console.print("  [cyan]ai-company status[/cyan]          # Show project status")
        console.print("  [cyan]ai-company doctor run[/cyan]      # Run diagnostics")
        console.print(
            "  [cyan]ai-company generate[/cyan]        # Regenerate agents after registry changes"
        )
        console.print(
            "  [cyan]ai-company company run[/cyan]     # Re-run company bootstrap after config changes"
        )
        console.print("  [cyan]uv run pytest[/cyan]              # Run tests")
        console.print("  [cyan]uv run ruff check src/[/cyan]     # Lint")


@app.command()
def status() -> None:
    """Show initialization status."""
    from pathlib import Path

    console.print("[bold blue]AI Company Initialization Status[/bold blue]")
    console.print()

    # Check dev setup
    venv_exists = Path(".venv").exists()
    uv_lock_exists = Path("uv.lock").exists()
    console.print(
        f"  Virtual environment: {'[green]OK[/green]' if venv_exists else '[red]MISSING[/red]'}"
    )
    console.print(
        f"  uv.lock:              {'[green]OK[/green]' if uv_lock_exists else '[red]MISSING[/red]'}"
    )

    # Check generated agents
    agents_dir = Path(".opencode/agents")
    agent_count = len(list(agents_dir.glob("*.md"))) if agents_dir.exists() else 0
    console.print(f"  Generated agents:     {agent_count}")

    # Check company configs
    configs_dir = Path(".opencode/config")
    config_count = len(list(configs_dir.glob("*.yaml"))) if configs_dir.exists() else 0
    console.print(f"  Company configs:      {config_count}")

    # Check registry
    registry_exists = Path("company-registry.yaml").exists()
    console.print(
        f"  company-registry.yaml: {'[green]OK[/green]' if registry_exists else '[red]MISSING[/red]'}"
    )

    console.print()
    if not (venv_exists and uv_lock_exists):
        console.print("Run [cyan]ai-company init[/cyan] to initialize.")
    elif agent_count == 0:
        console.print("Run [cyan]ai-company init --skip-dev-setup[/cyan] to generate agents.")
    elif config_count == 0:
        console.print(
            "Run [cyan]ai-company init --skip-dev-setup --skip-generate[/cyan] to bootstrap company."
        )
    else:
        console.print("[green]Fully initialized.[/green]")


if __name__ == "__main__":
    app()
