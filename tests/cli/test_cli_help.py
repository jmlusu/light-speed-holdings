"""Sprint 4 T015 — every CLI command and subcommand renders help without errors.

Walks the full command tree from the compiled click Group (via
``typer.main.get_command``) and invokes ``--help`` on every reachable path,
verifying each exits 0 and prints a Usage section. Walking the compiled tree
is platform-independent (parsing rich's box-drawing output is not: the box
characters vary by terminal/OS, which made the earlier implementation fail on
Linux CI).
"""

from __future__ import annotations

import functools
from typing import Any

import pytest
import typer
from typer.testing import CliRunner

from ai_company.cli.main import app

runner = CliRunner()


@functools.lru_cache(maxsize=1)
def _command_tree() -> tuple[list[list[str]], list[list[str]]]:
    """BFS the compiled click command tree once.

    Returns ``(leaf_paths, all_paths)`` where each path is e.g.
    ``["orchestrator", "scheduler", "add"]``. A path is a leaf when the node
    has no subcommands.
    """
    leaves: list[list[str]] = []
    all_paths: list[list[str]] = []
    frontier: list[tuple[list[str], Any]] = [([], None)]
    while frontier:
        path, node = frontier.pop()
        all_paths.append(path)
        if node is None:
            node = typer.main.get_command(app)
        if getattr(node, "commands", None):
            for name, child in node.commands.items():
                frontier.append(([*path, name], child))
        else:
            leaves.append(path)
    return leaves, all_paths


# The 5 direct commands + 24 sub-apps registered in cli/main.py.
EXPECTED_TOP_LEVEL = [
    "sop",
    "raci",
    "sync-registry",
    "generate",
    "status",
    "agents",
    "board",
    "bootstrap",
    "governance",
    "workflows",
    "memory",
    "executives",
    "departments",
    "doctor",
    "marketing",
    "sales",
    "customer-success",
    "legal",
    "hr",
    "specialists",
    "orchestrator",
    "models",
    "dashboard",
    "executor",
    "company",
    "decision",
    "graph",
    "archify",
    "security",
    "validate",
]


def test_root_help_shows_usage_and_commands() -> None:
    """``ai-company --help`` must exit 0 and expose the Commands section."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout
    assert "Commands" in result.stdout


def test_every_command_renders_help() -> None:
    """Every command/subcommand (leaf or group) renders ``--help`` cleanly."""
    leaves, all_paths = _command_tree()
    failures: list[str] = []
    for path in all_paths:
        label = " ".join(path) or "(root)"
        result = runner.invoke(app, [*path, "--help"])
        if result.exit_code != 0 or "Usage" not in result.stdout:
            failures.append(f"{label}: exit={result.exit_code} usage={'Usage' in result.stdout}")
    assert not failures, f"{len(failures)} command(s) failed --help:\n" + "\n".join(failures)


@pytest.mark.parametrize("cmd", EXPECTED_TOP_LEVEL)
def test_known_top_level_commands_are_registered(cmd: str) -> None:
    """All commands registered in cli/main.py must appear in the tree."""
    leaves, all_paths = _command_tree()
    top_level = {path[0] for path in all_paths if path}
    assert cmd in top_level


def test_leaf_command_count_is_stable() -> None:
    """Guard against accidental command-tree drift."""
    leaves, _ = _command_tree()
    assert len(leaves) >= 100  # observed: 117 leaves across 29 groups
