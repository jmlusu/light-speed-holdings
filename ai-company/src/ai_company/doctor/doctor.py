"""
Doctor module for system diagnostics.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ai_company.doctor.checks import run_all_checks

console = Console()

app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def doctor(ctx: typer.Context):
    """
    Run AI Company diagnostics.
    """
    if ctx.invoked_subcommand is None:
        run_diagnostics()


@app.command()
def run():
    """
    Run full system diagnostics.
    """
    run_diagnostics()


@app.command()
def fix():
    """
    Attempt to auto-fix detected issues.
    """
    console.print("[bold yellow]Auto-fix not yet implemented.[/bold yellow]")


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
