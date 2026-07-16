import typer

app = typer.Typer(help="Manage AI agents")


@app.command()
def list():
    """List registered AI agents."""
    typer.echo("")
    typer.echo("Registered Agents")
    typer.echo("-----------------")
    typer.echo("CEO")
    typer.echo("CTO")
    typer.echo("COO")
    typer.echo("CFO")
    typer.echo("HR")