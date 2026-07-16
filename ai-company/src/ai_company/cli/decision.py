"""Decision engine CLI commands."""

from __future__ import annotations

import typer

from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Decision engine — approval matrix, risk assessment, decision trees")
console = Console()


@app.command()
def evaluate(
    action: str = typer.Argument(..., help="Action to evaluate"),
) -> None:
    """Evaluate whether an action requires approval."""
    from ai_company.decision.engine import DecisionEngine
    from ai_company.registry import load_registry

    registry = load_registry()
    engine = DecisionEngine(registry)
    result = engine.evaluate_action(action)

    console.print(f"Action: [bold]{result['action']}[/bold]")
    console.print(f"Risk level: {result['risk_level']}")
    console.print(f"Requires approval: {result['requires_approval']}")
    if result["approvers"]:
        console.print(f"Approvers: {', '.join(result['approvers'])}")
    console.print(f"SLA: {result['sla_hours']}h")
    console.print(f"Auto-approve: {result['auto_approve']}")


@app.command()
def matrix() -> None:
    """Show the approval matrix."""
    from ai_company.decision.engine import DecisionEngine
    from ai_company.registry import load_registry

    registry = load_registry()
    engine = DecisionEngine(registry)
    actions = engine.list_actions()

    if not actions:
        console.print("No approval matrix entries.")
        return

    table = Table(title="Approval Matrix")
    table.add_column("Action", style="cyan")
    table.add_column("Risk", style="yellow")
    table.add_column("Approvers")
    table.add_column("SLA", justify="right")
    table.add_column("Auto", justify="center")

    for a in actions:
        table.add_row(
            a["action"],
            a["risk_level"],
            ", ".join(a["required_approvals"]) or "-",
            f"{a['sla_hours']}h",
            "Yes" if a["auto_approve"] else "No",
        )

    console.print(table)


@app.command()
def tree(
    start: str = typer.Option("root", help="Starting node ID"),
) -> None:
    """Navigate the decision tree."""
    from ai_company.registry import load_registry

    registry = load_registry()

    if not registry.decision_tree.nodes:
        console.print("No decision tree defined.")
        return

    console.print("Decision Tree:")
    for node in registry.decision_tree.nodes:
        children = ", ".join(node.children) if node.children else "none"
        console.print(f"  [{node.id}] {node.question or node.action} -> {children}")
