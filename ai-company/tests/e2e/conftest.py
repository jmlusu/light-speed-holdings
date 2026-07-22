"""E2E test fixtures and CLI options for Playwright-based dashboard tests.

Provides shared fixtures consumed by all E2E test modules:
    - dashboard_server: base URL string for the running dashboard
    - dashboard_url: alias for dashboard_server (backward compat)

Registers --dashboard-url and --dashboard-port CLI options via pytest_addoption.
"""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom CLI options for dashboard E2E tests."""
    parser.addoption(
        "--dashboard-url",
        action="store",
        default="http://localhost:9420",
        help="Base URL for the dashboard server (default: http://localhost:9420)",
    )
    parser.addoption(
        "--dashboard-port",
        action="store",
        default=None,
        help="Port for dashboard server (auto-detected if not set)",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "e2e: End-to-end tests requiring a live browser and server")
    config.addinivalue_line("markers", "slow: Tests that take more than 30 seconds")
    config.addinivalue_line("markers", "timeout(timeout): Set a timeout for individual tests")


@pytest.fixture(scope="session")
def dashboard_server(request: pytest.FixtureRequest) -> str:
    """Return the dashboard base URL for E2E tests.

    Reads from --dashboard-url CLI option, defaults to :9420 (staging).
    Skips the test if the dashboard server is not reachable.
    """
    import socket

    url: str = request.config.getoption("--dashboard-url")
    # Validate that the server is reachable; skip if not
    from urllib.parse import urlparse

    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 9420
    try:
        with socket.create_connection((host, port), timeout=2):
            pass
    except OSError:
        pytest.skip(
            f"Dashboard server not reachable at {url}. "
            f"Start the dashboard or pass --dashboard-url."
        )
    return url


@pytest.fixture()
def dashboard_url(dashboard_server: str) -> str:
    """Alias for dashboard_server — backward compatibility."""
    return dashboard_server
