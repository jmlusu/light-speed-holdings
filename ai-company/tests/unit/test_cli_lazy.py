"""Regression tests for the lazy CLI sub-group loader.

Covers:
- Importing the CLI or rendering the root ``--help`` never imports the
  25 lazy sub-app modules.
- Once resolved, the ``dashboard`` placeholder exposes the real group's
  options, callback, and subcommands.
- ``dashboard --help`` renders options owned by the real group.
- Subcommand dispatch through a lazy placeholder still resolves.
"""

from __future__ import annotations

import subprocess
import sys

from typer.main import get_group
from typer.testing import CliRunner

from ai_company.cli.main import app

runner = CliRunner()


def _run_in_fresh_interpreter(code: str) -> str:
    """Run ``code`` in a fresh interpreter and return its stdout."""
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", "-c", code],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout


def test_import_and_root_help_do_not_import_lazy_subapps() -> None:
    """Importing the CLI or rendering the root ``--help`` stays lazy."""
    code = (
        "import sys\n"
        "import ai_company.cli.main\n"
        "def lazy_count():\n"
        "    return sum(m.startswith('ai_company.cli.') for m in sys.modules)\n"
        "print('ai_company.cli.dashboard' in sys.modules)\n"
        "print(lazy_count())\n"
        "from typer.testing import CliRunner\n"
        "result = CliRunner().invoke(ai_company.cli.main.app, ['--help'])\n"
        "print(result.exit_code)\n"
        "print('ai_company.cli.dashboard' in sys.modules)\n"
        "print(lazy_count())\n"
    )
    before, count_before, exit_code, after, count_after = (
        _run_in_fresh_interpreter(code).strip().splitlines()
    )
    assert before == "False"
    assert count_before == "1"  # only ai_company.cli.main itself
    assert exit_code == "0"
    assert after == "False"
    assert count_after == "1"


def test_resolved_dashboard_group_interface() -> None:
    """Once resolved, the placeholder exposes the real group's interface."""
    group = get_group(app)
    dash = group.commands["dashboard"]
    assert {"port", "host", "no_open"} <= {p.name for p in dash.params}
    assert dash.invoke_without_command is True
    assert callable(dash.callback)
    assert {"backfill", "kpi"} <= set(dash.commands)


def test_dashboard_help_lists_real_options_and_subcommands() -> None:
    """``dashboard --help`` renders options owned by the real group."""
    result = runner.invoke(app, ["dashboard", "--help"])
    assert result.exit_code == 0
    assert "--host" in result.output
    assert "--port" in result.output
    assert "--no-open" in result.output
    assert "backfill" in result.output
    assert "kpi" in result.output


def test_dashboard_subcommand_dispatch_resolves() -> None:
    """``dashboard kpi --help`` resolves through the lazy placeholder."""
    result = runner.invoke(app, ["dashboard", "kpi", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output
    assert "show" in result.output
