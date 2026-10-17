"""Regression tests for the lazy `archify` CLI sub-group."""

from __future__ import annotations

import re

from typer.main import get_group
from typer.testing import CliRunner

from ai_company.cli.main import app

runner = CliRunner()

_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    return _ANSI_ESCAPE.sub("", text)


def test_archify_group_registered() -> None:
    group = get_group(app)
    assert "archify" in group.commands


def test_archify_help_lists_commands() -> None:
    result = runner.invoke(app, ["archify", "--help"])
    assert result.exit_code == 0
    output = _strip_ansi(result.output)
    for cmd in ("generate", "validate", "deliver", "compare"):
        assert cmd in output


def test_archify_subcommand_dispatch_resolves() -> None:
    result = runner.invoke(app, ["archify", "validate", "--help"])
    assert result.exit_code == 0
    output = _strip_ansi(result.output)
    assert "architecture" in output
    assert "workflow" in output
