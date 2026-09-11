"""Shared performance-test fixtures.

Resets dashboard global singletons (bus, StateStore, rate limiter) before
and after every performance test so module-level state from other test
files cannot leak and cause order-dependent flakes.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _reset_dashboard_state():
    """Reset module-level dashboard singletons before/after every perf test."""
    import ai_company.dashboard.api as dash_api
    from ai_company.dashboard.app import app
    from ai_company.dashboard.repository import reset_state_store

    reset_state_store()
    dash_api._bus = None
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()
    yield
    reset_state_store()
    dash_api._bus = None
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()
