"""Playwright configuration for dashboard E2E tests.

This configures multi-browser testing (Chromium, Firefox, WebKit)
with sensible defaults for CI and local development.

Usage:
    # Install
    pip install pytest-playwright
    playwright install

    # Run all browsers
    pytest tests/e2e/ -v

    # Run specific browser
    pytest tests/e2e/ -v --browser chromium
    pytest tests/e2e/ -v --browser firefox
    pytest tests/e2e/ -v --browser webkit

    # Run with headed mode (visual debugging)
    pytest tests/e2e/ -v --headed

    # Run scroll fix verification only
    pytest tests/e2e/test_scroll_fix_verification.py -v
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Pytest options (used by pytest-playwright)
# ---------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom CLI options for dashboard E2E tests."""
    parser.addoption(
        "--dashboard-port",
        action="store",
        default=None,
        help="Port for dashboard server (auto-detected if not set)",
    )


# ---------------------------------------------------------------------------
# Markers registration
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "e2e: End-to-end tests requiring a live browser and server",
    )
    config.addinivalue_line(
        "markers",
        "slow: Tests that take more than 30 seconds",
    )
