"""Shared unit-test fixtures.

Resets dashboard global singletons between tests so module-level state
(bus, StateStore, rate limiter) cannot leak across test modules and cause
order-dependent flakes. This is the deterministic-isolation fix for the
dashboard suite.
"""

from __future__ import annotations

import pytest


def _reset_shared_singletons() -> None:
    """Reset module-level singletons that hold live file paths.

    This is the single choke point for state pollution: StateStore, the
    dashboard bus, the SQLite database, the audit writer and the memory store
    are all rebound lazily on next use, so anything created between tests is
    guaranteed to point at the (test-controlled) data root rather than a
    stale CWD-relative path from an earlier test.
    """
    import ai_company.audit.integration as audit_mod
    import ai_company.dashboard.api as dash_api
    import ai_company.memory.integration as mem_mod
    from ai_company.dashboard.repository import reset_state_store
    from ai_company.data import reset_database
    from ai_company.orchestrator.approval import ApprovalGate

    reset_state_store()
    reset_database()
    dash_api._bus = None
    audit_mod._writer = None
    mem_mod._store = None
    mem_mod._vector_store = None
    ApprovalGate.reset_instance()


@pytest.fixture(autouse=True)
def _reset_dashboard_state():
    """Reset module-level dashboard singletons before/after every unit test."""
    from ai_company.dashboard.app import app

    _reset_shared_singletons()
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()
    yield
    _reset_shared_singletons()
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()
