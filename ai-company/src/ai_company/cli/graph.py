"""Graph engine CLI commands."""

from __future__ import annotations

import typer

from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Graph engine — org chart, decision graphs, knowledge graphs")
console = Console()


@app.command()
def list() -> None:
    """List all available graphs."""
    from ai_company.graph.engine import GraphEngine
    from ai_company.registry import load_registry

    registry = load_registry()
    engine = GraphEngine(registry)
    graphs = engine.list_graphs()

    table = Table(title="Available Graphs")
    table.add_column("Name", style="cyan")
    table.add_column("Nodes", justify="right", style="green")
    table.add_column("Edges", justify="right", style="yellow")

    for g in graphs:
        table.add_row(g["name"], str(g["nodes"]), str(g["edges"]))

    console.print(table)


@app.command()
def show(
    graph_name: str = typer.Argument(..., help="Graph to show (org_chart, decision_graph, workflow_graph, knowledge_graph)"),
) -> None:
    """Show a graph's nodes and edges."""
    from ai_company.graph.engine import GraphEngine
    from ai_company.registry import load_registry

    registry = load_registry()
    engine = GraphEngine(registry)
    graph = engine.get_graph(graph_name)

    if graph is None:
        console.print(f"[red]Graph '{graph_name}' not found[/red]")
        raise typer.Exit(1)

    console.print(f"Graph: [bold]{graph.name}[/bold]")
    console.print(f"  Nodes: {len(graph.nodes)}")
    console.print(f"  Edges: {len(graph.edges)}")

    # Show nodes
    table = Table(title=f"{graph.name} — Nodes")
    table.add_column("ID", style="cyan")
    table.add_column("Label", style="green")
    table.add_column("Type", style="yellow")

    for node in graph.nodes.values():
        table.add_row(node.id, node.label, node.node_type)

    console.print(table)

    # Show edges
    if graph.edges:
        table = Table(title=f"{graph.name} — Edges")
        table.add_column("Source", style="cyan")
        table.add_column("Relationship", style="yellow")
        table.add_column("Target", style="green")

        for edge in graph.edges:
            table.add_row(edge.source, edge.relationship, edge.target)

        console.print(table)


@app.command()
def path(
    graph_name: str = typer.Argument(..., help="Graph name"),
    start: str = typer.Option(..., help="Start node ID"),
    end: str = typer.Option(..., help="End node ID"),
) -> None:
    """Find a path between two nodes."""
    from ai_company.graph.engine import GraphEngine
    from ai_company.registry import load_registry

    registry = load_registry()
    engine = GraphEngine(registry)
    path_result = engine.find_path(graph_name, start, end)

    if path_result is None:
        console.print(f"[red]No path found from '{start}' to '{end}'[/red]")
        raise typer.Exit(1)

    console.print(f"Path from [cyan]{start}[/cyan] to [green]{end}[/green]:")
    console.print(f"  {' -> '.join(path_result)}")
