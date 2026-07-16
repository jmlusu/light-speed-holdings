"""
Doctor CLI commands for system diagnostics.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ai_company.doctor.checks import run_all_checks

console = Console()

app = typer.Typer(invoke_without_command=True, help="Run system diagnostics")


@app.callback(invoke_without_command=True)
def doctor_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        run_diagnostics()


@app.command()
def run():
    """Run full system diagnostics."""
    run_diagnostics()


@app.command()
def check():
    """Run checks and display results."""
    run_diagnostics()


def run_diagnostics():
    checks = run_all_checks()

    table = Table(title="System Health")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Message")

    for check in checks:
        status = "[green]PASS[/green]" if check.passed else "[red]FAIL[/red]"
        table.add_row(check.name, status, check.message)

    console.print(table)

    passed = sum(1 for c in checks if c.passed)
    total = len(checks)

    if passed == total:
        console.print(
            Panel(
                f"[bold green]All {total} checks passed![/bold green]",
                title="Health Status",
            )
        )
    else:
        failed = total - passed
        console.print(
            Panel(
                f"[bold red]{failed} check(s) failed.[/bold red]",
                title="Health Status",
            )
        )
