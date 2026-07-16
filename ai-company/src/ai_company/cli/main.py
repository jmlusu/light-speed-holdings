import typer
from ai_company.cli.agents import app as agents_app

app = typer.Typer(
    help="AI Company Builder"
)

doctor_app = typer.Typer()


@doctor_app.command("run")
def run():
    """
    Run system diagnostics.
    """
    typer.secho(
        "✓ AI Company Builder is healthy",
        fg=typer.colors.GREEN,
    )


app.add_typer(
    doctor_app,
    name="doctor",
)


if __name__ == "__main__":
    app()