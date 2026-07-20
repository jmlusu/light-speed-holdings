"""Contract & smoke tests for the dashboard StateStore (regression lock).

These tests pin the fixes from the shared-state remediation so the bugs
cannot silently return:

* The StateStore must resolve ``base_dir`` to an absolute path at
  construction time, so a later ``chdir()`` cannot break
  ``relative_to(base)`` (the original P0 crash: ``relative_to('.')``).
* A non-existent ``base_dir`` must still construct and read as empty
  rather than raising at construction.
* Reads of missing files must return the documented default (``[]`` for
  JSON, ``{}`` for YAML) — the symmetry gap that let the DLQ read blow up.
* Forbidden / out-of-root paths must be rejected (GAP-011 defence).

Author: qa_automation_engineer (owned by test_engineering_lead).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.dashboard.repository import (
    StateStore,
    StateStoreError,
    configure_state_store,
    get_state_store,
    reset_state_store,
)


@pytest.fixture(autouse=True)
def _reset_singleton() -> None:
    """Keep the module-level singleton from leaking between tests."""
    reset_state_store()
    yield
    reset_state_store()


def test_store_resolves_base_at_construction(tmp_path: Path) -> None:
    """base_dir is stored absolutely, so post-hoc chdir cannot break resolve."""
    target = tmp_path / "data"
    target.mkdir()

    store = StateStore(target)

    # The base is resolved to an absolute path, not a relative "data".
    assert store._base.is_absolute()
    assert store._base.resolve() == target.resolve()


def test_store_survives_chdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Reading a permitted file after chdir must still resolve correctly."""
    target = tmp_path / "root"
    target.mkdir()
    inbox = target / ".opencode"
    inbox.mkdir()
    (inbox / "inbox.json").write_text("[1, 2, 3]", encoding="utf-8")

    store = StateStore(target)
    monkeypatch.chdir(tmp_path)  # move cwd away from the store root

    # Must not raise ValueError/relative_to error after the chdir.
    assert store.read_json(".opencode/inbox.json") == [1, 2, 3]


def test_store_on_nonexistent_base_constructs_and_reads_empty(
    tmp_path: Path,
) -> None:
    """A not-yet-created base_dir must not crash at construction."""
    base = tmp_path / "not_created_yet"

    store = StateStore(base)

    assert isinstance(store, StateStore)
    # Missing permitted JSON defaults to []; missing YAML to {} (when default passed).
    assert store.read_json(".opencode/inbox.json") == []
    assert store.read_yaml("company/departments.yaml", default={}) == {}


def test_missing_json_returns_default_contract(tmp_path: Path) -> None:
    """DLQ-style read of a missing file returns [] — closes the DLQ bug.

    Note: ``read_json`` always falls back to ``[]`` for ``.json`` paths even
    when a different ``default`` is supplied (see repository.read_json), so a
    missing dead-letter queue is ``[]`` rather than ``None``.
    """
    store = StateStore(tmp_path)
    assert store.read_json(".opencode/dead_letter_queue.json", default=[]) == []
    assert store.read_json("orchestrator/cost_tracker.json", default={}) == []


def test_forbidden_path_is_rejected(tmp_path: Path) -> None:
    """Attempts to read outside the allowlist must raise StateStoreError."""
    store = StateStore(tmp_path)

    with pytest.raises(StateStoreError):
        store.read_json("../secrets.json")

    with pytest.raises(StateStoreError):
        store.read_text("etc/passwd")


def test_configure_then_get_returns_same_instance(tmp_path: Path) -> None:
    """get_state_store after configure() returns the configured instance."""
    configured = configure_state_store(tmp_path)
    assert get_state_store() is configured
    assert get_state_store(tmp_path / "other") is configured  # not rebinding


def test_relative_base_construction_is_cwd_independent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Constructing with a relative base resolves against the current cwd."""
    store_dir = tmp_path / "store"
    store_dir.mkdir()
    (store_dir / "company").mkdir()
    (store_dir / "company" / "departments.yaml").write_text(
        "departments: []\n", encoding="utf-8"
    )

    monkeypatch.chdir(tmp_path)
    store = StateStore("store")  # relative, resolved against tmp_path cwd
    assert store.read_yaml("company/departments.yaml", default={}) == {"departments": []}
