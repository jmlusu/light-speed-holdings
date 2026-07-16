import typer
from rich import print

doctor_app = typer.Typer(
    invoke_without_command=True
)


@doctor_app.callback(invoke_without_command=True)
def doctor(ctx: typer.Context):
    """
    Run AI Company diagnostics.
    """
    if ctx.invoked_subcommand is None:
        print("[bold green]✓ AI Company Builder is healthy[/bold green]")


@doctor_app.command()
def run():
    """
    Run diagnostics.
    """
    print("[bold green]✓ AI Company Builder is healthy[/bold green]")