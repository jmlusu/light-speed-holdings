"""
Main CLI entry point for AI Company Builder.
"""

from __future__ import annotations

import typer


def _init_logging() -> None:
    """Configure structured logging once, on first CLI invocation."""
    from ai_company.logging_config import setup_logging

    setup_logging()


app = typer.Typer(
    help="AI Company Builder - Orchestrate AI agent hierarchies",
    callback=_init_logging,
    invoke_without_command=True,
)


@app.callback(invoke_without_command=True)
def _lazy_init() -> None:
    """Ensure logging is configured before any subcommand runs."""
    _init_logging()


from ai_company.cli.agents import app as agents_app  # noqa: E402
from ai_company.cli.board import app as board_app  # noqa: E402
from ai_company.cli.workflows import app as workflows_app  # noqa: E402
from ai_company.cli.memory import app as memory_app  # noqa: E402
from ai_company.cli.executives import app as executives_app  # noqa: E402
from ai_company.cli.departments import app as departments_app  # noqa: E402
from ai_company.cli.doctor import app as doctor_app  # noqa: E402
from ai_company.cli.marketing import app as marketing_app  # noqa: E402
from ai_company.cli.sales import app as sales_app  # noqa: E402
from ai_company.cli.customer_success import app as customer_success_app  # noqa: E402
from ai_company.cli.legal import app as legal_app  # noqa: E402
from ai_company.cli.hr import app as hr_app  # noqa: E402
from ai_company.cli.specialists import app as specialists_app  # noqa: E402
from ai_company.cli.orchestrator import app as orchestrator_app  # noqa: E402
from ai_company.cli.models import app as models_app  # noqa: E402
from ai_company.cli.dashboard import app as dashboard_app  # noqa: E402
from ai_company.cli.executor import app as executor_app  # noqa: E402
from ai_company.cli.company import app as company_app  # noqa: E402
from ai_company.cli.decision import app as decision_app  # noqa: E402
from ai_company.cli.graph import app as graph_app  # noqa: E402
from ai_company.cli.security import app as security_app  # noqa: E402

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
app.add_typer(decision_app, name="decision", help="Decision engine — approvals, risk, trees")
app.add_typer(graph_app, name="graph", help="Graph engine — org chart, knowledge graphs")
app.add_typer(security_app, name="security", help="Security operations — encryption, key rotation")


@app.command()
def sop(
    sop_id: str = typer.Argument("", help="SOP ID to view (e.g. SOP-INCIDENT-001)"),
) -> None:
    """View Standard Operating Procedures."""
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
    """View RACI matrices for workflows."""
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
def status() -> None:
    """Show current company status."""
    typer.echo("AI Company Builder Status")
    typer.echo("========================")
    typer.echo("Company: Light Speed Holdings")
    typer.echo("Status: Active")


if __name__ == "__main__":
    app()
