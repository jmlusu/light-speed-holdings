"""Tests for GAP-011 — dashboard file I/O abstraction via StateStore.

Verifies that reads/writes are routed through a temp directory and that
forbidden / unknown paths are rejected by the allowlist.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.dashboard.repository import (
    StateStore,
    StateStoreError,
    reset_state_store,
)


@pytest.fixture()
def store(tmp_path: Path) -> StateStore:
    """A StateStore rooted at an isolated temp directory."""
    reset_state_store()
    return StateStore(base_dir=tmp_path, backup=False)


def test_write_then_read_json_roundtrip(store: StateStore, tmp_path: Path) -> None:
    """A JSON write is readable back and lands under base_dir."""
    store.write_json("company/agent-registry.json", [{"name": "a"}])
    on_disk = tmp_path / "company" / "agent-registry.json"
    assert on_disk.exists()
    assert store.read_json("company/agent-registry.json") == [{"name": "a"}]


def test_write_yaml_roundtrip(store: StateStore, tmp_path: Path) -> None:
    """A YAML write is readable back and lands under base_dir."""
    store.write_yaml("orchestrator/escalation.yaml", {"events": [{"task_id": "t1"}]})
    on_disk = tmp_path / "orchestrator" / "escalation.yaml"
    assert on_disk.exists()
    assert store.read_yaml("orchestrator/escalation.yaml") == {
        "events": [{"task_id": "t1"}]
    }


def test_missing_json_returns_default(store: StateStore) -> None:
    """Reading a non-existent JSON file returns the supplied default."""
    assert store.read_json("company/agent-registry.json", default=[]) == []


def test_forbidden_absolute_path_rejected(store: StateStore) -> None:
    """An absolute path outside the allowlist must raise StateStoreError."""
    with pytest.raises(StateStoreError):
        store.read_json("/etc/passwd")


def test_forbidden_relative_path_rejected(store: StateStore) -> None:
    """A relative path not on the allowlist must raise StateStoreError."""
    with pytest.raises(StateStoreError):
        store.write_json("../../secrets.json", {"x": 1})


def test_forbidden_path_cannot_escape_base(store: StateStore) -> None:
    """A traversal path targeting real state files is rejected too."""
    with pytest.raises(StateStoreError):
        store.read_text("company/../opencode/inbox.json")


def test_forbidden_path_rejected_on_exists(store: StateStore) -> None:
    """exists() must return False (not raise) for a forbidden path."""
    assert store.exists("orchestrator/../secrets.yaml") is False


def test_snapshot_prefix_allowed(store: StateStore, tmp_path: Path) -> None:
    """Files under the allowed KPI snapshot prefix are readable."""
    snap_dir = tmp_path / "orchestrator" / "kpi_snapshots"
    snap_dir.mkdir(parents=True)
    snap_file = snap_dir / "snapshot-20260101-000000.json"
    snap_file.write_text(json.dumps({"ok": True}), encoding="utf-8")

    files = store.list_snapshot_files()
    assert len(files) == 1
    assert store.read_snapshot(files[0]) == {"ok": True}
