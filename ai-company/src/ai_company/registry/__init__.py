"""Registry — loads, validates, and resolves the full company configuration."""

from __future__ import annotations

from pathlib import Path

from ai_company.models import CompanyRegistry
from ai_company.registry.loader import RegistryLoader
from ai_company.registry.parser import RegistryParser
from ai_company.registry.resolver import RegistryResolver
from ai_company.registry.validator import RegistryValidator

__all__ = ["load_registry"]


def load_registry(config_dir: str | Path | None = None) -> CompanyRegistry:
    """Load, parse, resolve, validate, and return the full CompanyRegistry.

    This is the single entry point that replaces the old YAML-based registry.
    """
    base = Path(config_dir) if config_dir else Path("config")

    loader = RegistryLoader(base)
    raw = loader.load_all()

    parser = RegistryParser()
    registry = parser.parse(raw)

    resolver = RegistryResolver()
    resolver.resolve(registry)

    validator = RegistryValidator()
    errors = validator.validate(registry)
    if errors:
        from rich.console import Console

        console = Console()
        console.print("[bold red]Registry validation errors:[/bold red]")
        for err in errors:
            console.print(f"  [red]✗[/red] {err}")
        raise SystemExit(1)

    return registry
