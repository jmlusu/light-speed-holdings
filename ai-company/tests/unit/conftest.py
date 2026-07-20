"""Shared unit-test fixtures.

Resets dashboard global singletons between tests so module-level state
(bus, StateStore) cannot leak across test modules and cause order-dependent
flakes. This is the deterministic-isolation fix for the dashboard suite.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _reset_dashboard_state():
    """Reset module-level dashboard singletons before/after every unit test."""
    import ai_company.dashboard.api as dash_api
    from ai_company.dashboard.repository import reset_state_store

    reset_state_store()
    dash_api._bus = None
    yield
    reset_state_store()
    dash_api._bus = None
