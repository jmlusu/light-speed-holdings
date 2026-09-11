"""Shared unit-test fixtures.

Resets dashboard global singletons between tests so module-level state
(bus, StateStore, rate limiter) cannot leak across test modules and cause
order-dependent flakes. This is the deterministic-isolation fix for the
dashboard suite.
"""

from __future__ import annotations

from pathlib import Path

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


def _inject_isolated_memory_store(memory_base: Path) -> None:
    """Point the memory integration at an empty, per-test store.

    Services default to ``init_memory("memory")``, which loads and rebuilds
    the vector index over the real (98MB) corpus — tens of seconds per test.
    Injecting an empty MemoryStore makes ``get_store()`` return truthy so the
    heavy ``init_memory`` path is skipped entirely; tests that exercise memory
    explicitly still call ``init_memory`` on their own tmp dirs.
    """
    from ai_company.memory import integration as mem_mod
    from ai_company.memory.engine import MemoryStore

    mem_mod._store = MemoryStore(base_dir=str(memory_base))
    mem_mod._vector_store = None


def patch_local_only_httpx(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make ``httpx.get`` fail fast and provider ``httpx.Client`` construction free.

    LLM tests run with ``OMNIROUTE_API_KEY`` set in the environment, so
    ``LLMClient._init_providers`` would otherwise do a real 3s gateway ping.
    Provider ``httpx.Client(...)`` construction is also heavy (~0.6s each on
    Windows) and is never actually exercised — tests replace ``_providers``
    with mocks. Stub both so LLM-heavy suites stay hermetic and fast.
    """
    import httpx

    def _refuse(*args: object, **kwargs: object) -> None:
        raise httpx.ConnectError("Connection refused")

    monkeypatch.setattr("httpx.get", _refuse)

    class _LocalOnlyClient:
        """Cheap stand-in for ``httpx.Client``: no real connection attempts.

        Provider construction in ``LLMClient.__init__`` builds one client per
        provider (~0.6s each on Windows via the TLS backend). Every test either
        replaces ``_providers`` with mocks or patches ``_client`` directly, so
        the real transport is never exercised.
        """

        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

        def get(self, *args: object, **kwargs: object) -> None:
            raise httpx.ConnectError("Connection refused")

        def post(self, *args: object, **kwargs: object) -> None:
            raise httpx.ConnectError("Connection refused")

        def stream(self, *args: object, **kwargs: object) -> None:
            raise httpx.ConnectError("Connection refused")

        def close(self) -> None:
            pass

        def __enter__(self) -> "_LocalOnlyClient":
            return self

        def __exit__(self, *args: object) -> None:
            pass

    monkeypatch.setattr("ai_company.llm.providers.openai_compatible.httpx.Client", _LocalOnlyClient)
    monkeypatch.setattr("ai_company.llm.providers.ollama.httpx.Client", _LocalOnlyClient)


@pytest.fixture(autouse=True)
def _reset_dashboard_state(tmp_path: Path, tmp_path_factory: pytest.TempPathFactory):
    """Reset module-level dashboard singletons before/after every unit test."""
    from ai_company.dashboard.app import app

    _reset_shared_singletons()
    # Use a scratch dir OUTSIDE tmp_path so tests that create ``tmp_path/memory``
    # (learning monitoring, migrate) or count files under tmp_path (tool_runner
    # list_directory) are unaffected.
    _inject_isolated_memory_store(tmp_path_factory.mktemp("unit-memory") / "memory")
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()
    yield
    _reset_shared_singletons()
    if hasattr(app.state, "limiter"):
        app.state.limiter._hits.clear()
