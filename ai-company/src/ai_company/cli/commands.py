import typer

from ai_company.cli.doctor import app as doctor

app = typer.Typer(
    name="ai-company",
    help="AI Company Builder",
    add_completion=False,
)

app.add_typer(
    doctor,
    name="doctor",
    help="Run system diagnostics",
)