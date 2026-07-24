"""Shared unit-test fixtures.

Resets dashboard global singletons between tests so module-level state
(bus, StateStore, rate limiter) cannot leak across test modules and cause
order-dependent flakes. This is the deterministic-isolation fix for the
dashboard suite.
"""

from __future__ import annotations

import gc
import os
import shutil
import tempfile
import time

import pytest


@pytest.fixture(autouse=True)
def _reset_dashboard_state():
    """Reset module-level dashboard singletons before/after every unit test."""
    import ai_company.dashboard.api as dash_api
    from ai_company.dashboard.app import app
    from ai_company.dashboard.repository import reset_state_store, reset_task_backend

    reset_state_store()
    reset_task_backend()
    dash_api._bus = None
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()
    yield
    reset_state_store()
    reset_task_backend()
    dash_api._bus = None
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()


@pytest.fixture(autouse=True)
def _cleanup_gc():
    """Force garbage collection after each test to release file handles.

    On Windows, open file handles lock directories and prevent pytest's
    tmp_path cleanup.  Aggressively collecting after each test ensures
    objects holding CostTracker / FileStore handles are finalized.
    """
    yield
    gc.collect()
    # Brief pause for Windows file-handle release
    if os.name == "nt":
        time.sleep(0.05)