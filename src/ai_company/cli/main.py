import typer

from ai_company.cli.doctor import doctor_app

app = typer.Typer(
    name="ai-company",
    help="AI Company Builder",
    add_completion=False,
)

app.add_typer(
    doctor_app,
    name="doctor",
)

if __name__ == "__main__":
    app()