"""
Memory management commands for company knowledge base.
"""

from pathlib import Path
import typer
import yaml

app = typer.Typer(help="Manage company memory and knowledge base")
MEMORY_DIR = Path("memory")
MEMORY_INDEX = MEMORY_DIR / "memory-index.yaml"


def _load_memory_index() -> dict:
    if not MEMORY_INDEX.exists():
        return {"memories": []}
    with open(MEMORY_INDEX, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"memories": []}


def _save_memory_index(data: dict):
    MEMORY_DIR.mkdir(exist_ok=True)
    with open(MEMORY_INDEX, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


@app.command()
def list():
    """List all memory entries."""
    data = _load_memory_index()
    memories = data.get("memories", [])

    if not memories:
        typer.echo("No memory entries found.")
        return

    typer.echo("")
    typer.echo("Company Memory")
    typer.echo("==============")
    for mem in memories:
        typer.echo(f"  {mem['id']}: {mem.get('title', 'Untitled')}")
        typer.echo(f"    Category: {mem.get('category', 'general')}")
        typer.echo(f"    Created: {mem.get('created_at', 'N/A')}")
        typer.echo("")


@app.command()
def add(
    memory_id: str = typer.Argument(..., help="Unique memory ID"),
    title: str = typer.Option(..., help="Memory title"),
    content: str = typer.Option(..., help="Memory content"),
    category: str = typer.Option("general", help="Memory category"),
):
    """Add a new memory entry."""
    data = _load_memory_index()
    memories = data.get("memories", [])

    for mem in memories:
        if mem["id"] == memory_id:
            typer.echo(f"Error: Memory '{memory_id}' already exists.")
            raise typer.Exit(1)

    from datetime import datetime

    new_memory = {
        "id": memory_id,
        "title": title,
        "content": content,
        "category": category,
        "created_at": datetime.now().isoformat(),
    }
    memories.append(new_memory)
    data["memories"] = memories
    _save_memory_index(data)
    typer.echo(f"Memory '{title}' added successfully.")


@app.command()
def get(memory_id: str = typer.Argument(..., help="Memory ID to retrieve")):
    """Retrieve a specific memory entry."""
    data = _load_memory_index()
    memories = data.get("memories", [])

    memory = next((m for m in memories if m["id"] == memory_id), None)
    if not memory:
        typer.echo(f"Error: Memory '{memory_id}' not found.")
        raise typer.Exit(1)

    typer.echo("")
    typer.echo(f"Memory: {memory.get('title', 'Untitled')}")
    typer.echo(f"Category: {memory.get('category', 'general')}")
    typer.echo(f"Created: {memory.get('created_at', 'N/A')}")
    typer.echo("")
    typer.echo(memory.get("content", ""))
    typer.echo("")


@app.command()
def remove(memory_id: str = typer.Argument(..., help="Memory ID to remove")):
    """Remove a memory entry."""
    data = _load_memory_index()
    memories = data.get("memories", [])
    original_len = len(memories)

    data["memories"] = [m for m in memories if m["id"] != memory_id]

    if len(data["memories"]) == original_len:
        typer.echo(f"Error: Memory '{memory_id}' not found.")
        raise typer.Exit(1)

    _save_memory_index(data)
    typer.echo(f"Memory '{memory_id}' removed.")
