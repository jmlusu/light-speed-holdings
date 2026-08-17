"""Unit tests for SuspendStore — persist/restore agent loop state on HITL park.

Verifies:
- save() creates a JSON file in the suspended_states directory
- load() restores the full SuspendedState
- delete() removes the file
- sweep_expired() removes files older than the retention window
- Corrupt files are treated as missing (no crash)
- Size cap truncates oldest conversation history entries
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from ai_company.orchestrator.suspend_store import (
    SuspendStore,
    SuspendedState,
    _truncate_history,
)


@pytest.fixture
def store(tmp_path: Path) -> SuspendStore:
    """Create a SuspendStore rooted in a per-test temp directory."""
    return SuspendStore(state_dir=str(tmp_path / "suspended"), retain_days=30)


def _make_state(task_id: str = "task-1", iterations: int = 3) -> SuspendedState:
    """Build a test SuspendedState with realistic conversation history."""
    history = ["Initial prompt"]
    for i in range(iterations):
        history.append(f"Tool result iteration {i}")
        history.append(f"Feedback iteration {i}")
    return SuspendedState(
        task_id=task_id,
        conversation_history=history,
        iterations_completed=iterations,
        tool_results=[
            {"step": 1, "tool": "bash", "status": "ok", "iteration": 1},
            {"step": 2, "tool": "read", "status": "ok", "iteration": 2},
        ],
        total_prompt_tokens=1500,
        total_completion_tokens=800,
        total_cost_usd=0.015,
        agent_name="test-agent",
        priority="high",
    )


# ── Save / Load ─────────────────────────────────────────────────


def test_save_and_load(tmp_path: Path, store: SuspendStore) -> None:
    state = _make_state("t-save")
    store.save("t-save", state)

    loaded = store.load("t-save")
    assert loaded is not None
    assert loaded.task_id == "t-save"
    assert loaded.iterations_completed == 3
    assert len(loaded.conversation_history) == 7  # 1 initial + 3*2 feedback
    assert loaded.total_prompt_tokens == 1500
    assert loaded.agent_name == "test-agent"


def test_load_missing_returns_none(store: SuspendStore) -> None:
    assert store.load("nonexistent") is None


def test_load_corrupt_returns_none(tmp_path: Path, store: SuspendStore) -> None:
    """A corrupt JSON file should be treated as missing, not crash."""
    state_dir = Path(store._dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "corrupt.json").write_text("NOT VALID JSON {{{")

    assert store.load("corrupt") is None


def test_save_overwrites_existing(tmp_path: Path, store: SuspendStore) -> None:
    """Saving the same task_id twice overwrites the first state."""
    state1 = _make_state("t-overwrite", iterations=2)
    store.save("t-overwrite", state1)

    state2 = _make_state("t-overwrite", iterations=5)
    store.save("t-overwrite", state2)

    loaded = store.load("t-overwrite")
    assert loaded is not None
    assert loaded.iterations_completed == 5


# ── Delete ──────────────────────────────────────────────────────


def test_delete_removes_file(tmp_path: Path, store: SuspendStore) -> None:
    store.save("t-delete", _make_state("t-delete"))
    assert store.load("t-delete") is not None

    store.delete("t-delete")
    assert store.load("t-delete") is None


def test_delete_nonexistent_is_noop(store: SuspendStore) -> None:
    """Deleting a non-existent state should not crash."""
    store.delete("nonexistent")


# ── Sweep ───────────────────────────────────────────────────────


def test_sweep_expired_removes_old_files(tmp_path: Path) -> None:
    store = SuspendStore(state_dir=str(tmp_path / "swept"), retain_days=1)

    # Create an old file (2 days ago)
    old_state = _make_state("old-task")
    old_state.parked_at = datetime.now(timezone.utc) - timedelta(days=2)
    store.save("old-task", old_state)

    # Create a fresh file
    store.save("new-task", _make_state("new-task"))

    removed = store.sweep_expired()
    assert removed == 1
    assert store.load("old-task") is None
    assert store.load("new-task") is not None


def test_sweep_expired_with_zero_retention(store: SuspendStore) -> None:
    """Retention of 0 disables sweep."""
    store.save("t", _make_state("t"))
    removed = store.sweep_expired(retain_days=0)
    assert removed == 0


def test_sweep_expired_empty_dir(store: SuspendStore) -> None:
    """Sweep on an empty directory returns 0."""
    removed = store.sweep_expired()
    assert removed == 0


# ── List ────────────────────────────────────────────────────────


def test_list_parked(store: SuspendStore) -> None:
    store.save("t-a", _make_state("t-a"))
    store.save("t-b", _make_state("t-b"))

    parked = store.list_parked()
    assert sorted(parked) == ["t-a", "t-b"]


def test_list_parked_empty(store: SuspendStore) -> None:
    assert store.list_parked() == []


# ── Size cap / truncation ──────────────────────────────────────


def test_truncate_history_keeps_first_and_recent() -> None:
    """Truncation preserves the first entry and as many recent entries as fit."""
    history = ["Initial prompt"]
    for i in range(100):
        history.append(f"Entry {i} with some content to fill bytes")

    truncated = _truncate_history(history, max_bytes=500)
    # First entry always kept
    assert truncated[0] == "Initial prompt"
    # Fewer entries than original
    assert len(truncated) < len(history)
    # Recent entries preserved
    assert truncated[-1] == history[-1]


def test_truncate_history_empty() -> None:
    assert _truncate_history([], max_bytes=100) == []


def test_truncate_history_single_entry() -> None:
    result = _truncate_history(["only one"], max_bytes=100)
    assert result == ["only one"]


# ── File format ─────────────────────────────────────────────────


def test_saved_file_is_valid_json(tmp_path: Path, store: SuspendStore) -> None:
    """The saved file should be well-formed JSON with expected fields."""
    state = _make_state("t-json")
    store.save("t-json", state)

    file_path = Path(store._dir) / "t-json.json"
    assert file_path.exists()

    data = json.loads(file_path.read_text())
    assert data["task_id"] == "t-json"
    assert data["iterations_completed"] == 3
    assert "conversation_history" in data
    assert "parked_at" in data


# ── SuspendedState model ───────────────────────────────────────


def test_suspended_state_default_values() -> None:
    state = SuspendedState(task_id="t-default")
    assert state.conversation_history == []
    assert state.iterations_completed == 0
    assert state.tool_results == []
    assert state.total_prompt_tokens == 0
    assert state.total_cost_usd == 0.0
    assert state.parked_at.tzinfo is not None  # UTC-aware


def test_suspended_state_ensures_utc() -> None:
    """Naive parked_at should be normalized to UTC."""
    state = SuspendedState(task_id="t-naive", parked_at=datetime(2026, 1, 1))
    assert state.parked_at.tzinfo is not None
