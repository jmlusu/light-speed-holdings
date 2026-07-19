"""
Doctor module for system diagnostics.
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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
    fixes: list[str] = []

    # 1. Ensure .opencode/ directory exists
    opencode_dir = Path(".opencode")
    if not opencode_dir.exists():
        opencode_dir.mkdir(parents=True, exist_ok=True)
        fixes.append("Created .opencode/ directory")

    # 2. Ensure company/ directory exists
    company_dir = Path("company")
    if not company_dir.exists():
        company_dir.mkdir(parents=True, exist_ok=True)
        fixes.append("Created company/ directory")

    # 3. Ensure .opencode/agents/ has generated files
    agents_dir = opencode_dir / "agents"
    if not agents_dir.exists():
        agents_dir.mkdir(parents=True, exist_ok=True)
        fixes.append("Created .opencode/agents/ directory")

    md_files = list(agents_dir.glob("*.md"))
    if not md_files:
        # Try to run the generator
        try:
            from ai_company.generator import AgentGenerator

            gen = AgentGenerator()
            results = gen.generate_all()
            count = len(results)
            if count > 0:
                fixes.append(f"Generated {count} agent files via AgentGenerator")
            else:
                fixes.append("AgentGenerator ran but produced no files (check registry)")
        except Exception as e:
            fixes.append(f"Agent generation failed: {e}")

    # 4. Ensure inbox.json exists
    inbox_path = opencode_dir / "inbox.json"
    if not inbox_path.exists():
        inbox_path.write_text("[]", encoding="utf-8")
        fixes.append("Created empty .opencode/inbox.json")

    # 5. Report results
    if fixes:
        console.print(Panel(
            "[bold green]Fixed:[/bold green]\n" + "\n".join(f"  - {f}" for f in fixes),
            title="Auto-Fix Results",
        ))
    else:
        console.print(Panel(
            "[bold green]No issues found — everything looks good![/bold green]",
            title="Auto-Fix Results",
        ))


def run_diagnostics():
    checks = run_all_checks()

    table = Table(title="System Health")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Message")

    for check in checks:
        if check.passed:
            status = "[green]PASS[/green]"
        elif check.severity == "warning":
            status = "[yellow]WARN[/yellow]"
        else:
            status = "[red]FAIL[/red]"
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
        warnings = sum(1 for c in checks if not c.passed and c.severity == "warning")
        errors = failed - warnings
        parts: list[str] = []
        if errors:
            parts.append(f"[bold red]{errors} error(s)[/bold red]")
        if warnings:
            parts.append(f"[bold yellow]{warnings} warning(s)[/bold yellow]")
        summary = ", ".join(parts)
        console.print(
            Panel(
                f"{summary} detected.",
                title="Health Status",
            )
        )
