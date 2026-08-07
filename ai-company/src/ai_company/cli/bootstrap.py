"""CLI command for developer machine bootstrap."""

from __future__ import annotations

from typing import Any, Optional

import typer
from rich.console import Console
from rich.table import Table

from ai_company.bootstrap import DEFAULT_ENV_FILE, DevBootstrap

app = typer.Typer(help="Prepare a new developer machine (idempotent)")
console = Console()


@app.callback(invoke_without_command=True)
def bootstrap_callback(ctx: typer.Context) -> None:
    """Run the bootstrap when invoked without a subcommand."""
    if ctx.invoked_subcommand is None:
        _execute(project_root=None, env_file=DEFAULT_ENV_FILE, json_output=False)


@app.command()
def run(
    project_root: Optional[str] = typer.Option(
        None, "--project-root", help="Project root (auto-detected if omitted)"
    ),
    env_file: str = typer.Option(
        DEFAULT_ENV_FILE, "--env-file", help="Environment file relative to project root"
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON summary"),
) -> None:
    """Install deps, create the venv, sync with uv, and verify the toolchain."""
    _execute(project_root=project_root, env_file=env_file, json_output=json_output)


def _execute(project_root: Optional[str], env_file: str, json_output: bool) -> None:
    """Run the bootstrap and render results."""
    bootstrap = DevBootstrap(project_root=project_root, env_file=env_file)
    summary = bootstrap.run()

    if json_output:
        console.print_json(data=summary)
    else:
        _render(summary)

    if not summary["ok"]:
        raise typer.Exit(1)


def _render(summary: dict[str, Any]) -> None:
    """Print a human-readable bootstrap summary."""
    console.print(f"[bold blue]Developer machine bootstrap[/bold blue] — {summary['project_root']}")

    table = Table(title="Bootstrap Summary")
    table.add_column("Step", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Message")

    for step in summary["steps"]:
        if step["severity"] == "ok":
            status = "[green]OK[/green]"
        elif step["severity"] == "warn":
            status = "[yellow]WARN[/yellow]"
        else:
            status = "[red]FAIL[/red]"
        table.add_row(step["name"], status, step["message"])

    console.print(table)

    if summary["errors"]:
        console.print(
            f"[bold red]{summary['errors']} error(s), {summary['warnings']} warning(s)[/bold red]"
        )
    else:
        console.print("[bold green]Bootstrap complete — machine ready.[/bold green]")
