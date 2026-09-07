"""Archify diagram CLI — generate, validate, deliver, compare.

Regenerates Archify JSON IR documents from the registry, validates them against
the bundled Archify renderer, and renders (or diffs) self-contained HTML
artifacts into ``docs/diagrams/``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from ai_company.paths import get_project_root

app = typer.Typer(help="Archify diagrams — generate, validate, compare, deliver from the registry")
console = Console()

# diagram type -> the quality profile its generated source is authored for.
_DIAGRAM_QUALITY: dict[str, str] = {
    "architecture": "standard",
    "workflow": "showcase",
    "sequence": "showcase",
    "dataflow": "showcase",
}

# diagram type -> default generated JSON filename under docs/diagrams/.
_DIAGRAM_FILE: dict[str, str] = {
    "architecture": "architecture.json",
    "workflow": "hiring.workflow.json",
    "sequence": "hiring.sequence.json",
    "dataflow": "hiring.dataflow.json",
}

_DIAGRAMS_DIR = Path("docs/diagrams")


def _diagrams_dir() -> Path:
    return get_project_root() / _DIAGRAMS_DIR


@app.command()
def generate(
    scope: str = typer.Option(
        "leadership",
        help="Architecture scope: leadership (exec + board) or full (all agents)",
    ),
) -> None:
    """Regenerate the default Archify JSON IR set from the registry."""
    if scope not in ("leadership", "full"):
        console.print(f"[red]Invalid scope '{scope}'; expected leadership or full[/red]")
        raise typer.Exit(1)

    from ai_company.archify.converter import generate_specs
    from ai_company.registry import load_registry

    registry = load_registry()
    specs = generate_specs(registry, scope=scope)
    out_dir = _diagrams_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    table = Table(title="Generated Archify JSON IR")
    table.add_column("Type", style="cyan")
    table.add_column("File", style="green")

    written: list[Path] = []
    for spec in specs:
        target = out_dir / spec.json_name
        target.write_text(json.dumps(spec.data, indent=2) + "\n", encoding="utf-8")
        written.append(target)
        table.add_row(spec.diagram_type, str(target))

    console.print(table)
    console.print(f"[green]Wrote {len(written)} diagram source(s) to {out_dir}[/green]")


@app.command()
def validate(
    diagram_type: str = typer.Argument(..., help="architecture | workflow | sequence | dataflow"),
    file: str = typer.Argument("", help="JSON IR source (default: docs/diagrams/<type>.json)"),
    quality: str = typer.Option(None, help="Override quality profile (standard | showcase)"),
) -> None:
    """Validate a JSON IR source against the Archify renderer."""
    from ai_company.archify import ArchifyError, ArchifyNotAvailable
    from ai_company.archify import validate as archify_validate

    if diagram_type not in _DIAGRAM_QUALITY:
        console.print(f"[red]Unknown diagram type '{diagram_type}'[/red]")
        raise typer.Exit(1)

    source = Path(file) if file else (_diagrams_dir() / _DIAGRAM_FILE[diagram_type])
    if not source.exists():
        console.print(f"[red]Source not found: {source}[/red]")
        raise typer.Exit(1)

    effective = quality or _DIAGRAM_QUALITY[diagram_type]
    try:
        receipt = archify_validate(diagram_type, source, quality=effective)
    except ArchifyNotAvailable as exc:  # pragma: no cover - env-dependent
        console.print(f"[yellow]{exc}[/yellow]")
        raise typer.Exit(2) from None
    except ArchifyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from None

    _print_receipt(receipt, source, effective)
    if not receipt.get("ok"):
        raise typer.Exit(1)


@app.command()
def deliver(
    diagram_type: str = typer.Argument(..., help="architecture | workflow | sequence | dataflow"),
    file: str = typer.Argument("", help="JSON IR source (default: docs/diagrams/<type>.json)"),
    output_html: str = typer.Option(
        "",
        "--output",
        "-o",
        help="Output HTML path (default: docs/diagrams/<type>.html)",
    ),
    quality: str = typer.Option(None, help="Override quality profile (standard | showcase)"),
    open_html: bool = typer.Option(False, "--open", help="Open the artifact in a browser"),
) -> None:
    """Render + validate a JSON IR source to a self-contained HTML artifact."""
    from ai_company.archify import ArchifyError, ArchifyNotAvailable
    from ai_company.archify import deliver as archify_deliver

    if diagram_type not in _DIAGRAM_QUALITY:
        console.print(f"[red]Unknown diagram type '{diagram_type}'[/red]")
        raise typer.Exit(1)

    source = Path(file) if file else (_diagrams_dir() / _DIAGRAM_FILE[diagram_type])
    if not source.exists():
        console.print(f"[red]Source not found: {source}[/red]")
        raise typer.Exit(1)

    out = (
        Path(output_html)
        if output_html
        else (_diagrams_dir() / _DIAGRAM_FILE[diagram_type].replace(".json", ".html"))
    )
    effective = quality or _DIAGRAM_QUALITY[diagram_type]
    try:
        receipt = archify_deliver(diagram_type, source, out, quality=effective, open_html=open_html)
    except ArchifyNotAvailable as exc:  # pragma: no cover - env-dependent
        console.print(f"[yellow]{exc}[/yellow]")
        raise typer.Exit(2) from None
    except ArchifyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from None

    artifact = receipt.get("artifact") or {}
    console.print(f"[green]Delivered {out} ({_fmt_bytes(artifact.get('bytes', 0))}[/green])")
    if not receipt.get("ok"):
        _print_receipt(receipt, source, effective)
        raise typer.Exit(1)


@app.command()
def compare(
    diagram_type: str = typer.Argument(..., help="architecture | workflow | sequence | dataflow"),
    base_file: str = typer.Argument(..., help="Baseline JSON IR source"),
    head_file: str = typer.Argument(..., help="Candidate JSON IR source"),
    output_html: str = typer.Option(
        "",
        "--output",
        "-o",
        help="Output comparison HTML (default: docs/diagrams/compare-<type>.html)",
    ),
    open_html: bool = typer.Option(False, "--open", help="Open the comparison in a browser"),
) -> None:
    """Render a Before/Delta/After comparison HTML from two validated snapshots."""
    from ai_company.archify import ArchifyError, ArchifyNotAvailable
    from ai_company.archify import compare as archify_compare

    out = Path(output_html) if output_html else (_diagrams_dir() / f"compare-{diagram_type}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt = archify_compare(
            diagram_type, Path(base_file), Path(head_file), out, open_html=open_html
        )
    except ArchifyNotAvailable as exc:  # pragma: no cover - env-dependent
        console.print(f"[yellow]{exc}[/yellow]")
        raise typer.Exit(2) from None
    except ArchifyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from None

    console.print(f"[green]Wrote comparison artifact to {out}[/green]")
    if not receipt.get("ok"):
        raise typer.Exit(1)


def _print_receipt(receipt: dict[str, Any], source: Path, quality: str) -> None:
    """Render a compact validation receipt summary."""
    ok = receipt.get("ok")
    status = "[green]PASS[/green]" if ok else "[red]FAIL[/red]"
    console.print(f"{status}  {source}  ({quality})")

    checks = receipt.get("checks") or []
    failed_checks = [c for c in checks if not c.get("ok")]
    if failed_checks:
        table = Table(title="Failed checks")
        table.add_column("Check", style="yellow")
        table.add_column("Detail", style="white")
        for check in failed_checks:
            detail = check.get("details") or []
            table.add_row(str(check.get("name", "")), "; ".join(map(str, detail[:3])))
        console.print(table)
    else:
        console.print(f"[dim]{len(checks)}/9 checks passed[/dim]")


def _fmt_bytes(n: int) -> str:
    if n >= 1 << 20:
        return f"{n / (1 << 20):.1f} MiB"
    if n >= 1 << 10:
        return f"{n / (1 << 10):.1f} KiB"
    return f"{n} B"
