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
from ai_company.cli.marketing import app as marketing_app
from ai_company.cli.sales import app as sales_app
from ai_company.cli.customer_success import app as customer_success_app
from ai_company.cli.legal import app as legal_app
from ai_company.cli.hr import app as hr_app
from ai_company.cli.specialists import app as specialists_app
from ai_company.cli.orchestrator import app as orchestrator_app
from ai_company.cli.models import app as models_app
from ai_company.cli.dashboard import app as dashboard_app
from ai_company.cli.executor import app as executor_app
from ai_company.cli.company import app as company_app

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
app.add_typer(marketing_app, name="marketing", help="Marketing operations")
app.add_typer(sales_app, name="sales", help="Sales operations")
app.add_typer(customer_success_app, name="customer-success", help="Customer Success operations")
app.add_typer(legal_app, name="legal", help="Legal operations")
app.add_typer(hr_app, name="hr", help="Human Resources operations")
app.add_typer(specialists_app, name="specialists", help="Manage specialist agents")
app.add_typer(orchestrator_app, name="orchestrator", help="Autonomous coordination")
app.add_typer(models_app, name="models", help="Model routing policy")
app.add_typer(dashboard_app, name="dashboard", help="CEO dashboard")
app.add_typer(executor_app, name="executor", help="Autonomous task execution")
app.add_typer(company_app, name="company", help="Bootstrap and manage the AI company")


@app.command()
def generate(
    registry: str = typer.Option(
        "company/agent-registry.json",
        help="Path to the agent registry JSON file",
    ),
) -> None:
    """Regenerate all company files from the single agent registry."""
    from ai_company.generator import AgentGenerator

    gen = AgentGenerator(registry_path=registry)
    results = gen.generate_all()
    typer.echo(f"\nDone: {len(results)} agent files generated.")


@app.command()
def status():
    """Show current company status."""
    typer.echo("AI Company Builder Status")
    typer.echo("========================")
    typer.echo("Company: Light Speed Holdings")
    typer.echo("Status: Active")


if __name__ == "__main__":
    app()

