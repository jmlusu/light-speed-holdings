"""
Main CLI entry point for AI Company Builder.
"""

import typer

from ai_company.cli.agents import app as agents_app
from ai_company.cli.board import app as board_app
from ai_company.cli.workflows import app as workflows_app
from ai_company.cli.memory import app as memory_app
from ai_company.cli.executives import app as executives_app
from ai_company.cli.departments import app as departments_app
from ai_company.cli.doctor import app as doctor_app

app = typer.Typer(
    help="AI Company Builder - Orchestrate AI agent hierarchies"
)

app.add_typer(agents_app, name="agents", help="Manage AI agents")
app.add_typer(board_app, name="board", help="Manage Board of Directors")
app.add_typer(workflows_app, name="workflows", help="Manage workflows")
app.add_typer(memory_app, name="memory", help="Manage company memory")
app.add_typer(executives_app, name="executives", help="Manage executives")
app.add_typer(departments_app, name="departments", help="Manage departments")
app.add_typer(doctor_app, name="doctor", help="Run system diagnostics")


@app.command()
def status():
    """Show current company status."""
    typer.echo("AI Company Builder Status")
    typer.echo("========================")
    typer.echo("Company: Light Speed Holdings")
    typer.echo("Status: Active")


if __name__ == "__main__":
    app()
