"""Static port-assignment guard (CTO ratification 2026-10-10, G-1).

Asserts the Marketing Site (Vite) / CEO Dashboard (FastAPI) port boundary
encoded in AGENTS.md §12/§13 and docs/organization/cto-ratification-
marketing-site-dashboard-boundary.md. Fails CI if any assignment drifts.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

VITE_DEV_PORT = 1441
VITE_PREVIEW_PORT = 1440
DASHBOARD_PROD_PORT = 8420
DASHBOARD_DEV_PORT = 8421

VITE_PORTS = frozenset({VITE_DEV_PORT, VITE_PREVIEW_PORT})
DASHBOARD_PORTS = frozenset({DASHBOARD_PROD_PORT, DASHBOARD_DEV_PORT})


def _read(relpath: str) -> str:
    path = REPO_ROOT / relpath
    assert path.exists(), f"missing required file: {relpath}"
    return path.read_text(encoding="utf-8")


def test_vite_config_ports() -> None:
    """vite.config.ts: server.port falls back to 1441, preview.port == 1440.

    The dev port may be declared as either a bare literal (`port: 1441`) or a
    cloud-container override with a literal fallback
    (`port: Number(process.env.PORT) || 1441`). Either form must still pin the
    ratified Marketing Site default, so only the fallback literal is asserted.
    """
    content = _read("vite.config.ts")
    server_match = re.search(
        r"server:\s*\{[^}]*?port:\s*(?:Number\(\s*process\.env\.PORT\s*\)\s*\|\|\s*)?(\d+)",
        content,
        re.DOTALL,
    )
    preview_match = re.search(r"preview:\s*\{[^}]*?port:\s*(\d+)", content, re.DOTALL)
    assert server_match, "vite.config.ts: server.port not found"
    assert preview_match, "vite.config.ts: preview.port not found"
    assert int(server_match.group(1)) == VITE_DEV_PORT
    assert int(preview_match.group(1)) == VITE_PREVIEW_PORT


def test_pm2_ports() -> None:
    """ecosystem.config.cjs: vite-dev -> 1441, vite-preview -> 1440."""
    content = _read("ecosystem.config.cjs")
    dev_match = re.search(r'name:\s*"vite-dev".*?port:\s*(\d+)', content, re.DOTALL)
    preview_match = re.search(r'name:\s*"vite-preview".*?port:\s*(\d+)', content, re.DOTALL)
    assert dev_match, "ecosystem.config.cjs: vite-dev port not found"
    assert preview_match, "ecosystem.config.cjs: vite-preview port not found"
    assert int(dev_match.group(1)) == VITE_DEV_PORT
    assert int(preview_match.group(1)) == VITE_PREVIEW_PORT


def test_dashboard_cli_default_port() -> None:
    """dashboard CLI default is 8420 (production)."""
    content = _read("src/ai_company/cli/dashboard.py")
    match = re.search(r"port:\s*int\s*=\s*typer\.Option\((\d+)", content)
    assert match, "dashboard.py: typer.Option port default not found"
    assert int(match.group(1)) == DASHBOARD_PROD_PORT


def test_compose_mappings() -> None:
    """docker-compose.yml: 8420:8420; staging default 8421 -> 8420."""
    prod = _read("docker-compose.yml")
    assert re.search(r'"8420:8420"', prod), "docker-compose.yml: expected host mapping 8420:8420"
    staging = _read("docker-compose.staging.yml")
    assert re.search(r"\$\{STAGING_DASHBOARD_PORT:-8421\}:8420", staging), (
        "docker-compose.staging.yml: expected staging default 8421->8420"
    )


def test_dashboard_and_vite_ports_disjoint() -> None:
    """dashboard_ports ∩ vite_ports == ∅."""
    assert DASHBOARD_PORTS.isdisjoint(VITE_PORTS), f"port collision: {DASHBOARD_PORTS & VITE_PORTS}"


@pytest.mark.parametrize("port", [VITE_DEV_PORT, VITE_PREVIEW_PORT])
def test_dashboard_cli_refuses_marketing_ports(port: int) -> None:
    """G-2: dashboard CLI exits non-zero on Marketing Site ports."""
    from typer.testing import CliRunner

    from ai_company.cli.dashboard import app

    runner = CliRunner()
    result = runner.invoke(app, ["--port", str(port), "--no-open"])
    assert result.exit_code != 0, (
        f"dashboard --port {port} should exit non-zero, got {result.exit_code}"
    )
    assert "Marketing Site" in result.output
