"""
Board of Directors management commands.
"""

from typing import Optional
from pathlib import Path
import typer
import yaml

app = typer.Typer(help="Manage the Board of Directors")
BOARD_DIR = Path("board")
BOARD_FILE = BOARD_DIR / "board.yaml"


def _load_board() -> dict:
    if not BOARD_FILE.exists():
        return {"board": []}
    with open(BOARD_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"board": []}


def _save_board(data: dict):
    BOARD_DIR.mkdir(exist_ok=True)
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list():
    """List all Board of Directors members."""
    data = _load_board()
    advisors = data.get("board", [])

    if not advisors:
        typer.echo("No board members registered.")
        return

    typer.echo("")
    typer.echo("Board of Directors")
    typer.echo("=================")
    for advisor in advisors:
        voting = "Voting" if advisor.get("voting", False) else "Non-voting"
        typer.echo(f"  {advisor['id']}: {advisor['title']} ({voting})")
        typer.echo(f"    Mission: {advisor.get('mission', 'N/A')}")
        typer.echo("")


@app.command()
def add(
    advisor_id: str = typer.Argument(..., help="Unique advisor ID"),
    title: str = typer.Option(..., help="Advisor title"),
    mission: str = typer.Option(..., help="Advisor mission statement"),
    voting: bool = typer.Option(False, help="Whether advisor has voting rights"),
):
    """Add a new Board of Directors member."""
    data = _load_board()
    advisors = data.get("board", [])

    for a in advisors:
        if a["id"] == advisor_id:
            typer.echo(f"Error: Advisor '{advisor_id}' already exists.")
            raise typer.Exit(1)

    new_advisor = {
        "id": advisor_id,
        "title": title,
        "mission": mission,
        "voting": voting,
        "inspirations": [],
    }
    advisors.append(new_advisor)
    data["board"] = advisors
    _save_board(data)
    typer.echo(f"Board member '{title}' added successfully.")


@app.command()
def remove(advisor_id: str = typer.Argument(..., help="Advisor ID to remove")):
    """Remove a Board of Directors member."""
    data = _load_board()
    advisors = data.get("board", [])
    original_len = len(advisors)

    data["board"] = [a for a in advisors if a["id"] != advisor_id]

    if len(data["board"]) == original_len:
        typer.echo(f"Error: Advisor '{advisor_id}' not found.")
        raise typer.Exit(1)

    _save_board(data)
    typer.echo(f"Board member '{advisor_id}' removed.")


@app.command()
def brief():
    """Generate a board briefing with key metrics."""
    data = _load_board()
    advisors = data.get("board", [])

    typer.echo("")
    typer.echo("Board Briefing")
    typer.echo("==============")
    typer.echo(f"Board Size: {len(advisors)} members")
    voting_count = sum(1 for a in advisors if a.get("voting", False))
    typer.echo(f"Voting Members: {voting_count}")
    typer.echo("")
