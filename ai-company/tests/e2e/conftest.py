"""E2E test fixtures and CLI options for Playwright-based dashboard tests.

Provides shared fixtures consumed by all E2E test modules:
    - dashboard_server: base URL string for the running dashboard
    - dashboard_url: alias for dashboard_server (backward compat)

CLI options (``--dashboard-url``/``--dashboard-port``) are registered in the
root ``tests/conftest.py`` so they are recognized before option parsing even
when pytest is invoked without an explicit path (``pytest -m e2e``).
"""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "e2e: End-to-end tests requiring a live browser and server")
    config.addinivalue_line("markers", "slow: Tests that take more than 30 seconds")
    config.addinivalue_line("markers", "timeout(timeout): Set a timeout for individual tests")


@pytest.fixture(scope="session")
def dashboard_server(request: pytest.FixtureRequest) -> str:
    """Return the dashboard base URL for E2E tests.

    Reads from --dashboard-url CLI option, defaults to :8421 (staging).
    Skips the test if the dashboard server is not reachable.
    """
    import socket

    url: str = request.config.getoption("--dashboard-url")
    # Validate that the server is reachable; skip if not
    from urllib.parse import urlparse

    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8421
    try:
        with socket.create_connection((host, port), timeout=2):
            pass
    except OSError:
        pytest.skip(
            f"Dashboard server not reachable at {url}. Start the dashboard or pass --dashboard-url."
        )
    return url


@pytest.fixture()
def dashboard_url(dashboard_server: str) -> str:
    """Alias for dashboard_server — backward compatibility."""
    return dashboard_server
