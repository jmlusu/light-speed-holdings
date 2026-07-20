"""Tests for Option B — explicit StateStore configuration (R2).

The dashboard StateStore singleton must be bound explicitly at boot from a
config/env value rather than silently re-pointing at the import-time cwd.
These tests verify ``configure_state_store`` and the lazy-default behaviour
of ``get_state_store``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.dashboard.repository import (
    StateStore,
    configure_state_store,
    get_state_store,
    is_state_store_configured,
    reset_state_store,
)


@pytest.fixture(autouse=True)
def _clean_singleton() -> None:
    """Ensure the module-level singleton does not leak between tests."""
    reset_state_store()
    yield
    reset_state_store()


def test_configure_points_store_at_given_dir(tmp_path: Path) -> None:
    """After configure_state_store(tmp_path) the store is rooted at tmp_path."""
    store = configure_state_store(tmp_path)

    assert isinstance(store, StateStore)
    assert store._base.resolve() == tmp_path.resolve()
    # get_state_store() returns the same configured instance.
    assert get_state_store() is store
    assert is_state_store_configured() is True


def test_reconfigure_repoints_store(tmp_path: Path) -> None:
    """Calling configure again with a different dir rebinds the singleton."""
    first = tmp_path / "one"
    second = tmp_path / "two"
    first.mkdir()
    second.mkdir()

    store_a = configure_state_store(first)
    assert get_state_store() is store_a

    store_b = configure_state_store(second)
    # A new instance rooted at the new dir, and the singleton now returns it.
    assert store_b is not store_a
    assert get_state_store() is store_b
    assert get_state_store()._base.resolve() == second.resolve()


def test_get_state_store_without_configure_defaults_sensibly(tmp_path: Path) -> None:
    """Without configure, get_state_store lazily defaults to '.' (cwd)."""
    reset_state_store()
    assert is_state_store_configured() is False

    store = get_state_store()

    assert isinstance(store, StateStore)
    assert store._base.resolve() == Path(".").resolve()
    # Subsequent calls return the same lazily-created singleton.
    assert get_state_store() is store
