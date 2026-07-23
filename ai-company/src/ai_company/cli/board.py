"""Board of Directors management commands.

Includes board membership management and the Board Directive tracking
system for issuing, tracking, and completing formal board instructions.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import typer
import yaml

app = typer.Typer(help="Manage the Board of Directors")
BOARD_DIR = Path("board")
BOARD_FILE = BOARD_DIR / "board.yaml"

# ── Directives sub-command group ────────────────────────────────────
directives_app = typer.Typer(help="Track and manage Board directives")
app.add_typer(directives_app, name="directives")

DIRECTIVES_FILE = Path("config/board/directives.yaml")


def _load_board() -> dict:
    """Load the board membership data from YAML."""
    if not BOARD_FILE.exists():
        return {"board": []}
    with open(BOARD_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"board": []}


def _save_board(data: dict) -> None:
    """Persist the board membership data to YAML."""
    BOARD_DIR.mkdir(exist_ok=True)
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list() -> None:
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
) -> None:
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
def remove(advisor_id: str = typer.Argument(..., help="Advisor ID to remove")) -> None:
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
def brief() -> None:
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


# ═════════════════════════════════════════════════════════════════════
# Board Directives
# ═════════════════════════════════════════════════════════════════════


def _load_directives() -> dict:
    """Load the directives data from YAML."""
    if not DIRECTIVES_FILE.exists():
        return {"directives": []}
    with open(DIRECTIVES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"directives": []}


def _save_directives(data: dict) -> None:
    """Persist the directives data to YAML."""
    DIRECTIVES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DIRECTIVES_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def _next_directive_id(directives: list[dict]) -> str:
    """Generate the next directive ID (DIR-YYYY-NNN)."""
    year = datetime.now(timezone.utc).year
    max_num = 0
    for d in directives:
        did = d.get("id", "")
        if did.startswith(f"DIR-{year}-"):
            try:
                num = int(did.split("-")[-1])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return f"DIR-{year}-{max_num + 1:03d}"


# ── Directives commands ────────────────────────────────────────────


@directives_app.command("list")
def directives_list() -> None:
    """List all Board directives in a table."""
    data = _load_directives()
    directives = data.get("directives", [])

    if not directives:
        typer.echo("No directives found.")
        return

    typer.echo("")
    typer.echo("Board Directives")
    typer.echo("=" * 80)
    typer.echo(
        f"  {'ID':<16} {'Title':<35} {'Priority':<10} "
        f"{'Owner':<18} {'Status':<12} {'Deadline':<12}"
    )
    typer.echo(
        f"  {'-'*15} {'-'*34} {'-'*9} "
        f"{'-'*17} {'-'*11} {'-'*11}"
    )

    for d in directives:
        did = d.get("id", "?")
        title = d.get("title", "Untitled")
        if len(title) > 34:
            title = title[:31] + "..."
        priority = d.get("priority", "medium")
        owner = d.get("owner", "unassigned")
        if len(owner) > 17:
            owner = owner[:14] + "..."
        status = d.get("status", "pending")
        deadline = d.get("deadline", "none")

        # Status icons
        status_display = {
            "completed": "DONE",
            "in_progress": "WIP",
            "pending": "TODO",
            "overdue": "LATE",
        }.get(status, status)

        typer.echo(
            f"  {did:<16} {title:<35} {priority:<10} "
            f"{owner:<18} {status_display:<12} {deadline:<12}"
        )

    typer.echo("")


@directives_app.command("add")
def directives_add(
    title: str = typer.Option(..., help="Directive title"),
    description: str = typer.Option("", help="Detailed description"),
    issued_by: str = typer.Option("human-ceo", help="Who issued the directive"),
    deadline: str = typer.Option("", help="Deadline (YYYY-MM-DD)"),
    priority: str = typer.Option("medium", help="Priority: critical/high/medium/low"),
    owner: str = typer.Option("unassigned", help="Responsible agent or role"),
    notes: str = typer.Option("", help="Free-form notes"),
) -> None:
    """Add a new Board directive."""
    if priority not in ("critical", "high", "medium", "low"):
        typer.echo(f"Error: Invalid priority '{priority}'. Use: critical, high, medium, low.")
        raise typer.Exit(1)

    data = _load_directives()
    directives = data.get("directives", [])

    new_id = _next_directive_id(directives)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    new_directive = {
        "id": new_id,
        "title": title,
        "description": description,
        "issued_by": issued_by,
        "issued_date": now,
        "deadline": deadline or now,
        "priority": priority,
        "status": "pending",
        "owner": owner,
        "completion_date": None,
        "notes": notes,
    }

    directives.append(new_directive)
    data["directives"] = directives
    _save_directives(data)

    typer.echo(f"Directive '{new_id}' created: {title}")
    typer.echo(f"  Priority: {priority}  Owner: {owner}  Deadline: {deadline or now}")


@directives_app.command("complete")
def directives_complete(
    directive_id: str = typer.Argument(..., help="Directive ID (e.g. DIR-2026-004)"),
    notes: str = typer.Option("", help="Completion notes"),
) -> None:
    """Mark a Board directive as completed."""
    data = _load_directives()
    directives = data.get("directives", [])

    target = None
    for d in directives:
        if d["id"] == directive_id or d["id"].startswith(directive_id):
            target = d
            break

    if target is None:
        typer.echo(f"Error: Directive '{directive_id}' not found.")
        raise typer.Exit(1)

    if target["status"] == "completed":
        typer.echo(f"Directive '{target['id']}' is already completed.")
        return

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    target["status"] = "completed"
    target["completion_date"] = now
    if notes:
        existing_notes = target.get("notes", "")
        target["notes"] = f"{existing_notes}\n{notes}".strip() if existing_notes else notes

    _save_directives(data)
    typer.echo(f"Directive '{target['id']}' marked as completed.")
    typer.echo(f"  Title: {target['title']}")
    typer.echo(f"  Completed: {now}")


@directives_app.command("status")
def directives_status() -> None:
    """Show summary of directive statuses."""
    data = _load_directives()
    directives = data.get("directives", [])

    if not directives:
        typer.echo("No directives found.")
        return

    counts: dict[str, int] = {}
    for d in directives:
        status = d.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1

    total = len(directives)
    typer.echo("")
    typer.echo("Directive Status Summary")
    typer.echo("=" * 40)
    typer.echo(f"  Total directives: {total}")
    typer.echo("")

    for status in ("completed", "in_progress", "pending", "overdue"):
        count = counts.get(status, 0)
        if count > 0:
            icon = {
                "completed": "[DONE]",
                "in_progress": "[WIP ]",
                "pending": "[TODO]",
                "overdue": "[LATE]",
            }.get(status, status)
            typer.echo(f"  {icon} {status:<15} {count}")

    typer.echo("")

    # Show overdue items
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    overdue = [
        d for d in directives
        if d.get("status") not in ("completed",)
        and d.get("deadline", "9999-12-31") < now
    ]
    if overdue:
        typer.echo("  ⚠ Overdue directives:")
        for d in overdue:
            typer.echo(f"    {d['id']}: {d['title']} (deadline: {d['deadline']})")
        typer.echo("")
