"""E2E test fixtures for Playwright-based dashboard tests.

Provides shared fixtures consumed by all E2E test modules:
    - dashboard_server: base URL string for the running dashboard
    - dashboard_url: alias for dashboard_server (backward compat)

Configuration (CLI options) is handled by pytest_plugins.py.
"""

from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def dashboard_server(request: pytest.FixtureRequest) -> str:
    """Return the dashboard base URL for E2E tests.

    Reads from --dashboard-url CLI option, defaults to :9420 (staging).
    """
    return request.config.getoption("--dashboard-url")


@pytest.fixture()
def dashboard_url(dashboard_server: str) -> str:
    """Alias for dashboard_server — backward compatibility."""
    return dashboard_server
