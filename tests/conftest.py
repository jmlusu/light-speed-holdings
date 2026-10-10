"""Shared test configuration for the ai-company test suite."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolate_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Anchor the data root at a per-test temp dir.

    Default-constructed ``AuditWriter`` / ``MessageBus`` / ``StateStore``
    instances resolve their paths through ``DASHBOARD_DATA_DIR``
    (``paths.get_data_root``).  Without this, unit tests append synthetic
    events to the canonical ``.opencode/audit`` ledger, polluting the
    studio-scorecard baseline window.  Tests that need a specific root
    override this by setting the env var themselves (their ``setenv``
    runs after this fixture); tests that assert *default* resolution
    must ``delenv`` it (see ``tests/unit/test_paths.py``).
    """
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))


@pytest.fixture(autouse=True)
def _default_dashboard_auth_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default the dashboard to open auth mode for tests.

    Production defaults to fail-closed (``DASHBOARD_AUTH_MODE=api_key``), but
    most tests exercise dashboard behavior without configuring an API key.
    Tests that specifically verify auth must opt back into ``api_key`` mode.
    """
    monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register CLI options for the E2E (Playwright) dashboard tests.

    Defined here (not in ``tests/e2e/conftest.py``) because pytest only
    pre-loads conftest files from the rootdir or explicit path arguments
    before parsing CLI options. Without a path argument (e.g. ``pytest -m
    e2e``) the nested conftest is loaded too late and pytest rejects
    ``--dashboard-url`` as an unrecognized argument.
    """
    parser.addoption(
        "--dashboard-url",
        action="store",
        default="http://localhost:8421",
        help="Base URL for the dashboard server (default: http://localhost:8421)",
    )
    parser.addoption(
        "--dashboard-port",
        action="store",
        default=None,
        help="Port for dashboard server (auto-detected if not set)",
    )
