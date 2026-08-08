"""Sprint 4 T015 — every CLI command and subcommand renders help without errors.

Walks the full command tree via ``--help`` output (the Typer/rich format uses
a ``┌─ Commands ─...┐`` box with ``│ name  description`` rows) and verifies
that every reachable command exits 0 and prints a Usage section.
"""

from __future__ import annotations

import functools

import pytest
from typer.testing import CliRunner

from ai_company.cli.main import app

runner = CliRunner()


def _parse_commands(help_text: str) -> list[str]:
    """Extract command names from a Typer/rich help table.

    The box format produced by this CLI's Typer version is::

        ┌─ Commands ───────────────────────────────────────────────────┐
        │ sop               View Standard Operating Procedures.        │
        │ sync-registry     Sync agent-registry.json from YAML         │
        │                   (source of truth).                         │
        └──────────────────────────────────────────────────────────────┘

    Continuation rows have 2+ spaces after the box character and are skipped.
    """
    cmds: list[str] = []
    in_commands = False
    for line in help_text.splitlines():
        stripped = line.strip()
        if "Commands" in stripped and stripped.startswith(("┌", "┏")):
            in_commands = True
            continue
        if not in_commands:
            continue
        if stripped.startswith(("└", "┗", "╰")):
            break
        if stripped.startswith("│"):
            rest = stripped[1:]
            # Continuation row: name column is blank -> 2+ leading spaces.
            if len(rest) - len(rest.lstrip(" ")) > 1:
                continue
            name = rest.strip().split(None, 1)[0] if rest.strip() else ""
            if name and not name.startswith("-"):
                cmds.append(name)
    return cmds


@functools.lru_cache(maxsize=1)
def _command_tree() -> tuple[list[list[str]], list[list[str]]]:
    """BFS the help tree once.

    Returns ``(leaf_paths, all_paths)`` where each path is e.g.
    ``["orchestrator", "scheduler", "add"]``.
    """
    leaves: list[list[str]] = []
    all_paths: list[list[str]] = []
    frontier: list[list[str]] = [[]]
    while frontier:
        path = frontier.pop()
        all_paths.append(path)
        result = runner.invoke(app, [*path, "--help"])
        sub = _parse_commands(result.stdout)
        if not sub:
            leaves.append(path)
            continue
        for cmd in sub:
            frontier.append([*path, cmd])
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
