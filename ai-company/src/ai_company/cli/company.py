"""CLI command for bootstrap — generates the full company from config/."""

from __future__ import annotations

from typing import Any

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Bootstrap the AI company from config/")
console = Console()


@app.command()
def run(
    config_dir: str = typer.Option("config", help="Path to config/ directory"),
    output_dir: str = typer.Option(".opencode", help="Output directory for generated files"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be created without writing"),
) -> None:
    """Bootstrap the AI company — generate all agents, configs, and directory structure."""
    from ai_company.builder import BootstrapEngine
    from ai_company.registry import load_registry

    console.print("[bold blue]AI Company Bootstrap[/bold blue]")
    console.print(f"  Config: {config_dir}")
    console.print(f"  Output: {output_dir}")
    console.print()

    # Load and validate registry
    console.print("[bold]Loading registry...[/bold]")
    try:
        registry = load_registry(config_dir)
    except SystemExit:
        console.print("[red]Registry validation failed. Fix errors and try again.[/red]")
        raise typer.Exit(1)

    console.print(f"  Company: {registry.company.name}")
    console.print(f"  Executives: {len(registry.executives)}")
    console.print(f"  Departments: {len(registry.departments)}")
    console.print(f"  Specialists: {len(registry.specialists)}")
    console.print(f"  Workflows: {len(registry.workflows)}")
    console.print()

    if dry_run:
        console.print("[yellow]DRY RUN — no files will be written[/yellow]")
        _show_plan(registry)
        return

    # Run bootstrap
    console.print("[bold]Bootstrapping...[/bold]")
    engine = BootstrapEngine(
        config_dir=config_dir,
        output_dir=output_dir,
    )
    summary = engine.bootstrap(registry)

    # Show results
    _show_results(summary)


def _show_plan(registry: Any) -> None:
    """Show what would be created during bootstrap."""
    table = Table(title="Bootstrap Plan")
    table.add_column("Type", style="cyan")
    table.add_column("Count", style="green")
    table.add_column("Details", style="dim")

    table.add_row("Directories", "24", "memory/*, knowledge/*, projects/*, etc.")
    table.add_row("Executive Agents", str(len(registry.executives)), "")
    table.add_row("Department Agents", str(len(registry.departments)), "")
    table.add_row("Specialist Agents", str(len(registry.specialists)), "")
    table.add_row("Board Agents", str(len(registry.board)), "")
    table.add_row("Config Files", "4", "company, org_chart, workflows, governance")
    console.print(table)


def _show_results(summary: dict) -> None:
    """Show bootstrap results."""
    console.print()
    console.print("[bold green]Bootstrap complete![/bold green]")
    console.print()

    # Directories
    table = Table(title="Directories Created")
    table.add_column("Path", style="cyan")
    for d in summary["directories"]:
        table.add_row(d)
    console.print(table)

    # Agents
    table = Table(title="Agents Generated")
    table.add_column("File", style="cyan")
    for a in summary["agents"]:
        table.add_row(a)
    console.print(table)

    # Configs
    table = Table(title="Configs Generated")
    table.add_column("File", style="cyan")
    for c in summary["configs"]:
        table.add_row(c)
    console.print(table)

    if summary["errors"]:
        console.print("[bold red]Errors:[/bold red]")
        for err in summary["errors"]:
            console.print(f"  [red]✗[/red] {err}")
