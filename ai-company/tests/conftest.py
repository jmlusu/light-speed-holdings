"""Shared test configuration for the ai-company test suite."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _default_dashboard_auth_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default the dashboard to open auth mode for tests.

    Production defaults to fail-closed (``DASHBOARD_AUTH_MODE=api_key``), but
    most tests exercise dashboard behavior without configuring an API key.
    Tests that specifically verify auth must opt back into ``api_key`` mode.
    """
    monkeypatch.setenv("DASHBOARD_AUTH_MODE", "open")
