"""Memory management commands — now with MemoryEngine integration."""

from __future__ import annotations

import typer

from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Manage company memory and knowledge base")
console = Console()


@app.command()
def list(
    memory_type: str = typer.Option("all", help="Memory type to list (episodic, semantic, procedural, relational, temporal, aggregate, all)"),
) -> None:
    """List memory entries."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    if memory_type == "all":
        stats = store.stats()
        table = Table(title="Memory Store")
        table.add_column("Type", style="cyan")
        table.add_column("Count", justify="right", style="green")
        for t, c in stats.items():
            table.add_row(t, str(c))
        console.print(table)
    else:
        entries = store.recall(memory_type, limit=20)
        if not entries:
            console.print(f"No {memory_type} memories found.")
            return

        table = Table(title=f"{memory_type.title()} Memories")
        table.add_column("ID", style="cyan")
        table.add_column("Content")
        table.add_column("Agent")
        table.add_column("Tags")

        for e in entries:
            content_preview = e.content[:80] + "..." if len(e.content) > 80 else e.content
            table.add_row(e.id, content_preview, e.agent_id, ", ".join(e.tags))

        console.print(table)


@app.command()
def add(
    memory_type: str = typer.Option(..., help="Memory type (episodic, semantic, procedural, relational, temporal)"),
    content: str = typer.Option(..., help="Memory content"),
    agent_id: str = typer.Option("", help="Agent that created this memory"),
    tags: str = typer.Option("", help="Comma-separated tags"),
) -> None:
    """Add a new memory entry."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    entry = store.store(memory_type, content, agent_id=agent_id, tags=tag_list)
    console.print(f"[green]Stored {memory_type} memory:[/green] {entry.id}")


@app.command()
def search(
    memory_type: str = typer.Option("all", help="Memory type to search"),
    query: str = typer.Option("", help="Search query"),
    tags: str = typer.Option("", help="Comma-separated tags to filter by"),
    limit: int = typer.Option(10, help="Max results"),
) -> None:
    """Search memory entries."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    types_to_search = [memory_type] if memory_type != "all" else [
        "episodic", "semantic", "procedural", "relational", "temporal"
    ]

    all_results = []
    for mt in types_to_search:
        results = store.recall(mt, query=query, tags=tag_list, limit=limit)
        all_results.extend(results)

    if not all_results:
        console.print("No matching memories found.")
        return

    table = Table(title="Search Results")
    table.add_column("Type", style="cyan")
    table.add_column("Content")
    table.add_column("Agent")

    for e in all_results[:limit]:
        content_preview = e.content[:60] + "..." if len(e.content) > 60 else e.content
        table.add_row(e.memory_type, content_preview, e.agent_id)

    console.print(table)


@app.command()
def consolidate(
    memory_type: str = typer.Argument(..., help="Memory type to consolidate"),
) -> None:
    """Create an aggregate summary of a memory type."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    summary = store.consolidate(memory_type)
    console.print(f"[green]Consolidated {memory_type}:[/green]")
    console.print(f"  Entries: {summary['count']}")
    if summary.get("top_tags"):
        console.print(f"  Top tags: {', '.join(f'{t[0]}({t[1]})' for t in summary['top_tags'][:5])}")
    if summary.get("top_agents"):
        console.print(f"  Top agents: {', '.join(f'{a[0]}({a[1]})' for a in summary['top_agents'][:5])}")


@app.command("consolidate-all")
def consolidate_all(
    max_age_days: int = typer.Option(90, help="Max age in days for episodic memories"),
    max_entries: int = typer.Option(2000, help="Max entries per memory type"),
) -> None:
    """Run full memory consolidation: deduplicate, aggregate, and prune."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()

    # Prune first
    pruned = store.prune(
        max_age_days=max_age_days,
        max_entries_per_type=max_entries,
    )
    console.print(f"[yellow]Pruned {pruned} entries[/yellow]")

    # Then consolidate all types
    summary = store.consolidate_all()
    console.print("[green]Consolidation complete:[/green]")
    console.print(f"  Semantic duplicates removed: {summary['semantic_duplicates_removed']}")
    console.print(f"  Aggregates created: {summary['aggregates_created']}")
    console.print(f"  Types processed: {summary['types_processed']}")

    # Show final stats
    stats = store.stats()
    table = Table(title="Memory Store After Consolidation")
    table.add_column("Type", style="cyan")
    table.add_column("Count", justify="right", style="green")
    for t, c in stats.items():
        table.add_row(t, str(c))
    console.print(table)


@app.command()
def prune(
    max_age_days: int = typer.Option(None, help="Remove entries older than N days"),
    max_entries: int = typer.Option(None, help="Cap each type to N entries"),
) -> None:
    """Prune memory entries by age and/or per-type cap."""
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    pruned = store.prune(
        max_age_days=max_age_days,
        max_entries_per_type=max_entries,
    )
    console.print(f"[yellow]Pruned {pruned} entries[/yellow]")
