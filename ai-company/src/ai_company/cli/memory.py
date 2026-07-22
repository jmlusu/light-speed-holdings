"""Memory management commands — now with MemoryEngine integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import typer

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(help="Manage company memory and knowledge base")
console = Console()

# Sub-command group for vector-index operations
vector_index_app = typer.Typer(help="Manage the vector embedding index")
app.add_typer(vector_index_app, name="vector-index")


@app.command("list")
def list_entries(
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
    query: str = typer.Argument("", help="Search query (keyword or semantic)"),
    memory_type: str = typer.Option("all", help="Memory type to search"),
    tags: str = typer.Option("", help="Comma-separated tags to filter by"),
    limit: int = typer.Option(10, help="Max results"),
    semantic: bool = typer.Option(
        False,
        "--semantic",
        "-s",
        help="Use semantic (embedding) search instead of keyword matching",
    ),
) -> None:
    """Search memory entries.

    By default, uses keyword/substring matching.  Pass ``--semantic`` to
    perform embedding-based cosine-similarity search when the vector index
    is available; falls back to keyword search gracefully.
    """
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    # When --semantic is requested, try to enable vector search on the fly
    if semantic and query:
        try:
            _enable_vector_search(store)
        except Exception:
            pass  # Non-fatal: fall back to keyword search

    types_to_search = [memory_type] if memory_type != "all" else [
        "episodic", "semantic", "procedural", "relational", "temporal"
    ]

    all_results: list = []
    for mt in types_to_search:
        if semantic and query:
            # Use recall with use_semantic=True (vector search if available)
            results = store.recall(
                mt,
                query=query,
                tags=tag_list,
                limit=limit,
                use_semantic=True,
            )
        else:
            results = store.recall(mt, query=query, tags=tag_list, limit=limit)
        all_results.extend(results)

    if not all_results:
        mode_label = "semantic" if semantic else "keyword"
        console.print(f"No matching memories found ({mode_label} search).")
        return

    search_label = "Semantic Search Results" if semantic else "Search Results"
    table = Table(title=search_label)
    table.add_column("Type", style="cyan")
    table.add_column("Content")
    table.add_column("Agent")

    for e in all_results[:limit]:
        content_preview = e.content[:60] + "..." if len(e.content) > 60 else e.content
        table.add_row(e.memory_type, content_preview, e.agent_id)

    console.print(table)


@app.command()
def recall(
    memory_type: str = typer.Option(
        "all",
        "--type",
        "-t",
        help="Memory type to recall (episodic, semantic, procedural, relational, temporal, all)",
    ),
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum entries to recall"),
    tags: str = typer.Option("", "--tags", help="Comma-separated tags to filter by"),
) -> None:
    """Recall recent memories, optionally filtered by type and tags.

    Shows the most recent memory entries from the specified type(s),
    ordered by recency.  Useful for quick inspection of what the
    memory store currently holds.
    """
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    types_to_recall = (
        [memory_type] if memory_type != "all"
        else ["episodic", "semantic", "procedural", "relational", "temporal"]
    )

    all_entries: list = []
    for mt in types_to_recall:
        entries = store.recall(mt, tags=tag_list, limit=limit)
        all_entries.extend(entries)

    # Sort by most recent (entries have created_at or similar ordering)
    all_entries = all_entries[:limit]

    if not all_entries:
        console.print(f"No memories found for type '{memory_type}'.")
        return

    table = Table(title=f"Recalled Memories ({len(all_entries)} entries)")
    table.add_column("Type", style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Content")
    table.add_column("Agent")

    for e in all_entries:
        content_preview = e.content[:60] + "..." if len(e.content) > 60 else e.content
        table.add_row(e.memory_type, e.id, content_preview, e.agent_id)

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


# ── Helpers ────────────────────────────────────────────────────────────


def _enable_vector_search(store: Any, base_dir: str = "memory") -> None:
    """Try to enable vector search on the given MemoryStore.

    Imports the embedding engine lazily so the CLI stays responsive even
    when ML dependencies are slow to load.
    """
    from ai_company.memory.engine import MemoryStore as _MS  # noqa: F811

    if not isinstance(store, _MS) or store.has_vector_search:
        return

    try:
        from ai_company.ml.embeddings import EmbeddingEngine

        engine = EmbeddingEngine(
            model_name="all-MiniLM-L6-v2",
            cache_dir=f"{base_dir}/embeddings",
        )
        store.enable_vector_search(
            embedding_engine=engine,
            index_dir=f"{base_dir}/vector_index",
        )
    except Exception:
        pass  # Best-effort; caller falls back to keyword search


# ── stats command ──────────────────────────────────────────────────────


@app.command()
def stats() -> None:
    """Show memory store statistics — counts, sizes, and types.

    Displays a per-type breakdown of stored entries along with aggregate
    totals for quick health assessment of the memory subsystem.
    """
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()
    type_stats = store.stats()
    total = sum(type_stats.values())

    # Compute on-disk sizes for each memory JSON file
    base_dir = store.base_dir
    size_map: dict[str, int] = {}
    total_bytes = 0
    for mem_type in type_stats:
        file_path = base_dir / f"{mem_type}.json"
        if file_path.exists():
            size = file_path.stat().st_size
            size_map[mem_type] = size
            total_bytes += size
        else:
            size_map[mem_type] = 0

    # ── Summary panel ──
    vector_status = "available" if store.has_vector_search else "unavailable"
    summary = (
        f"Total entries: [bold]{total}[/bold]\n"
        f"Disk usage: [bold]{total_bytes:,}[/bold] bytes\n"
        f"Vector search: {vector_status}"
    )
    console.print(Panel(summary, title="Memory Store Summary", border_style="cyan"))

    # ── Per-type table ──
    table = Table(title="Entries by Type")
    table.add_column("Type", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Size", justify="right")

    for mem_type in ("episodic", "semantic", "procedural", "relational", "temporal", "aggregate"):
        count = type_stats.get(mem_type, 0)
        size = size_map.get(mem_type, 0)
        table.add_row(mem_type, str(count), _format_bytes(size))

    console.print(table)


def _format_bytes(n: int) -> str:
    """Human-readable byte size."""
    if n < 1024:
        return f"{n} B"
    elif n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    else:
        return f"{n / (1024 * 1024):.1f} MB"


# ── vector-index rebuild ──────────────────────────────────────────────


@vector_index_app.command("rebuild")
def rebuild_vector_index(
    memory_type: Optional[str] = typer.Option(
        None,
        help="Rebuild index for a single memory type only (default: all types)",
    ),
) -> None:
    """Rebuild the vector embedding index from stored memories.

    Re-encodes every memory entry and persists a fresh vector index to
    ``memory/vector_index/vector_index.json``.
    """
    from ai_company.memory.engine import MemoryStore

    store = MemoryStore()

    # Attempt to enable vector search (which initializes the VectorStore)
    try:
        _enable_vector_search(store)
    except Exception as exc:
        console.print(f"[red]Failed to initialise embedding engine:[/red] {exc}")
        raise typer.Exit(1) from exc

    if not store.has_vector_search:
        console.print(
            "[yellow]Vector search is unavailable — could not build index.[/yellow]\n"
            "Ensure that numpy and sentence-transformers are installed."
        )
        raise typer.Exit(1)

    # Rebuild the index
    indexed = store._vector_store.index_all(memory_type=memory_type)  # type: ignore[union-attr]

    label = memory_type or "all types"
    console.print(
        f"[green]Vector index rebuilt[/green] for {label}: "
        f"[bold]{indexed}[/bold] entries indexed."
    )

    # Show index location
    index_dir: Path = store._vector_store.index_dir  # type: ignore[union-attr]
    index_file = index_dir / "vector_index.json"
    if index_file.exists():
        size = index_file.stat().st_size
        console.print(f"  Index file: {index_file} ({_format_bytes(size)})")
    else:
        console.print(f"  Index dir:  {index_dir}")
