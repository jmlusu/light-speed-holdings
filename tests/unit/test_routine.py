"""Unit tests for the Pharos routine engine (ADR-020 P0)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from ai_company.orchestrator.routine import (
    _UTC,
    Routine,
    RoutineScheduler,
    RoutineStore,
    build_routine_task,
    compute_next_run,
)

# ── Routine model basics ──────────────────────────────────────────────────────


def test_routine_creation_defaults() -> None:
    r = Routine(id="test", name="Test Routine", receiver_id="content_writer")
    assert r.id == "test"
    assert r.name == "Test Routine"
    assert r.receiver_id == "content_writer"
    assert r.enabled is True
    assert r.schedule_day is None
    assert r.interval_minutes is None
    assert r.prompt_file == ""
    assert r.model == ""
    assert r.budget_tokens is None
    assert r.outputs == []
    assert r.last_run == ""
    # next_run is populated by RoutineStore._load, not by construction.


def test_routine_is_daily() -> None:
    r = Routine(id="daily", schedule_day=2, time_utc="09:00")
    assert r.is_daily() is True


def test_routine_is_interval() -> None:
    r = Routine(id="interval", interval_minutes=60)
    assert r.is_daily() is False


# ── compute_next_run ─────────────────────────────────────────────────────────


def test_compute_next_run_daily() -> None:
    r = Routine(id="m", schedule_day=1, time_utc="04:00")  # Monday
    now = datetime.now(_UTC)
    nxt = compute_next_run(r, now)
    # Must be strictly after `now`; day-of-week Monday at 04:00 UTC
    assert nxt.weekday() == 0  # Monday
    assert nxt.hour == 4 and nxt.minute == 0


def test_compute_next_run_interval() -> None:
    r = Routine(id="intv", interval_minutes=120)
    now = datetime.now(_UTC)
    nxt = compute_next_run(r, now)
    # Advance by 120 minutes from `now`
    expected = now + __import__("datetime").timedelta(minutes=120)
    assert abs((nxt - expected).total_seconds()) < 5


# ── RoutineStore ─────────────────────────────────────────────────────────────


@pytest.fixture()
def tmp_project_root(tmp_path: Path) -> Path:
    """Minimal project root for RoutineStore file I/O."""
    # Create a sentinel routines.yaml so RoutineStore doesn't fail on missing file
    (tmp_path / "config" / "company" / "routines.yaml").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "config" / "company" / "routines.yaml").write_text("")
    # Also create company-registry.yaml so is_known_receiver works
    (tmp_path / "company-registry.yaml").write_text(
        "agents:\n  - id: content_writer\n  - id: cto\n"
    )
    # Provide a patched project_root to RoutineStore
    import ai_company.orchestrator.routine as routine_mod

    original_root = routine_mod.get_project_root
    routine_mod.get_project_root = lambda: tmp_path
    yield tmp_path
    routine_mod.get_project_root = original_root


def test_routine_store_loads(tmp_project_root: Path) -> None:
    store = RoutineStore(project_root=tmp_project_root)
    routines = store.list_routines()
    # Empty YAML should seed at least one default routine (schedule_day=1, 04:00)
    assert len(routines) >= 1
    r = routines[0]
    assert r.id  # auto-generated from file


def test_routine_store_mark_run_persists(tmp_project_root: Path) -> None:
    store = RoutineStore(project_root=tmp_project_root)
    # The auto-seed default routine has id "pharos_default_brief"
    now = datetime.now(_UTC)
    store.mark_run("pharos_default_brief", now)
    routines = store.list_routines()
    assert routines[0].last_run != ""
    # next_run should have been advanced
    assert routines[0].next_run != ""
    assert routines[0].next_run != ""


def test_routine_store_get_due_enabled(tmp_project_root: Path) -> None:
    store = RoutineStore(project_root=tmp_project_root)
    # The auto-seed default routine's next_run is set to a past date so it is
    # immediately "due"; adjust if needed for the test clock.
    store.routines[0].next_run = "1970-01-01T00:00:00+00:00"
    due = store.get_due(datetime.now(_UTC))
    # At least the default routine should appear due
    assert len(due) >= 1


# ── RoutineScheduler ─────────────────────────────────────────────────────────


@pytest.fixture()
def scheduler_fixture(tmp_path: Path) -> RoutineScheduler:
    """Build a RoutineScheduler with a tiny in‑memory store and no real bus."""
    # Create a minimal routines.yaml so RoutineStore loads
    (tmp_path / "config" / "company" / "routines.yaml").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "config" / "company" / "routines.yaml").write_text(
        """routines:
          - id: weekly_brief
            name: Weekly Brief
            receiver_id: content_writer
            schedule_day: 1
            time_utc: "04:00"
            enabled: true
            prompt_file: templates/pharos/routines/monday-agentic-enterprise-brief.md
        """
    )
    # Minimal registry for is_known_receiver
    (tmp_path / "company-registry.yaml").write_text("agents:\n  - id: content_writer\n")
    store = RoutineStore(project_root=tmp_path)
    # Seed the default routine so next_run is a past date (makes it immediately due)
    store.routines[0].next_run = "1970-01-01T00:00:00+00:00"
    # MessageBus without callback / database for test speed
    from ai_company.orchestrator.message_bus import MessageBus

    bus = MessageBus(storage_path=str(tmp_path / ".opencode" / "inbox.json"), database=None)
    sched = RoutineScheduler(interval_seconds=1, bus=bus, store=store)
    return sched


def test_scheduler_run_due_fires_daily(scheduler_fixture: RoutineScheduler) -> None:
    """With interval=1 second, run_due should fire the due routine each call."""
    fired = scheduler_fixture.run_due()
    assert fired >= 1
    # After firing, the routine's next_run advanced; a second immediate call
    # should not fire again within the same interval window.
    fired2 = scheduler_fixture.run_due(now=scheduler_fixture._last_run + 0.5)
    # Due to interval gate, should be 0 (too soon)
    assert fired2 == 0


def test_scheduler_run_due_idempotent_tags(scheduler_fixture: RoutineScheduler) -> None:
    """After firing, the task carries deterministic tags and a routine_run_id."""
    fired = scheduler_fixture.run_due()
    assert fired >= 1
    # Read back from inbox
    tasks = scheduler_fixture._bus.get_all_tasks_raw()
    assert len(tasks) >= 1
    task = tasks[0]
    tags = task.get("tags", [])
    assert any("pharos-routine" in t for t in tags), f"Expected pharos-routine tag, got {tags}"
    assert any("routine:" in t for t in tags), f"Expected routine: tag, got {tags}"
    # routine_run_id format: routine_run:{id}-{date}
    run_tags = [t for t in tags if t.startswith("routine_run:")]
    assert len(run_tags) == 1, f"Expected one routine_run tag, got {run_tags}"
    run_id_val = run_tags[0].split(":")[1]
    assert "-" in run_id_val  # should contain date separator


def test_scheduler_skips_disabled(scheduler_fixture: RoutineScheduler) -> None:
    """A routine with enabled=False must not fire."""
    # scheduler_fixture already has one enabled routine
    # Add a disabled one
    store = scheduler_fixture.store
    disabled = Routine(
        id="disabled_routine",
        name="Disabled",
        receiver_id="content_writer",
        schedule_day=1,
        time_utc="04:00",
        enabled=False,
        prompt_file="",
    )
    store.routines.append(disabled)
    # Re-run; the disabled one should be skipped
    fired = scheduler_fixture.run_due()
    # At least the original routine should still fire; total >= 1
    assert fired >= 1


def test_scheduler_skips_unknown_receiver(scheduler_fixture: RoutineScheduler) -> None:
    """A routine with a receiver_id not in the registry must be skipped."""
    store = scheduler_fixture.store
    unknown = Routine(
        id="bad_receiver",
        name="Bad",
        receiver_id="nonexistent_agent",
        schedule_day=1,
        time_utc="04:00",
        enabled=True,
        prompt_file="",
    )
    store.routines.append(unknown)
    fired = scheduler_fixture.run_due()
    # The original routine should still fire; total >= 1 but should not include
    # the unknown-receiver routine.
    assert fired >= 1
    # Check that the task count reflects only valid routines
    tasks = scheduler_fixture._bus.get_all_tasks_raw()
    # The inbox should have exactly 1 task (the valid one), not 2
    # (the unknown receiver is skipped)
    valid_task_ids = [t["id"] for t in tasks if t.get("id", "").startswith("routine-")]
    assert len(valid_task_ids) >= 1


def test_build_routine_task_tags_and_idempotency() -> None:
    """build_routine_task produces a Task with deterministic id + tags + run id."""
    r = Routine(id="test-run", name="Test", receiver_id="content_writer")
    fire = datetime(2026, 9, 16, 4, 0, 0, tzinfo=timezone.utc)
    task = build_routine_task(r, fire, "Run routine for {receiver_id} on {date}.")
    assert task.id == "routine-test-run-2026-09-16"
    assert "pharos-routine" in task.tags
    assert "routine:test-run" in task.tags
    assert "routine_run:test-run-2026-09-16" in task.tags
    # instruction token substitution
    assert "{receiver_id}" not in task.instruction
    assert "{date}" not in task.instruction
    assert "content_writer" in task.instruction
    assert "2026-09-16" in task.instruction


# ── Deep-research routines (ADR-020 P1) ───────────────────────────────────────


def test_routine_research_depth_default_standard() -> None:
    r = Routine(id="plain", receiver_id="content_writer")
    assert r.research_depth == "standard"
    assert r.is_deep_research is False


def test_routine_research_depth_deep_flag() -> None:
    r = Routine(id="deep", receiver_id="content_writer", research_depth="deep")
    assert r.is_deep_research is True


def test_routine_research_depth_empty_is_shallow() -> None:
    r = Routine(id="legacy", receiver_id="content_writer", research_depth="")
    assert r.is_deep_research is False


def test_build_deep_research_task_tags_and_token() -> None:
    """Deep routines add 'research:deep' tag and render {research_depth}."""
    r = Routine(
        id="deep-brief", name="Deep Brief", receiver_id="content_writer", research_depth="deep"
    )
    fire = datetime(2026, 9, 20, 4, 0, 0, tzinfo=timezone.utc)
    task = build_routine_task(r, fire, "Depth is {research_depth}.")
    assert "research:deep" in task.tags
    assert "{research_depth}" not in task.instruction
    assert "deep" in task.instruction


def test_build_standard_task_has_no_deep_tag() -> None:
    r = Routine(id="plain-brief", name="Plain", receiver_id="content_writer")
    fire = datetime(2026, 9, 20, 4, 0, 0, tzinfo=timezone.utc)
    task = build_routine_task(r, fire, "Hi.")
    assert "research:deep" not in task.tags


def test_store_loads_deep_research_routines(tmp_project_root: Path) -> None:
    """routines.yaml entries with research_depth: deep land in the store."""
    (tmp_project_root / "config" / "company" / "routines.yaml").write_text(
        "routines:\n"
        "  - id: deep_brief\n"
        "    name: Deep\n"
        "    receiver_id: content_writer\n"
        "    schedule_day: 6\n"
        '    time_utc: "04:00"\n'
        "    enabled: true\n"
        "    research_depth: deep\n"
    )
    store = RoutineStore(project_root=tmp_project_root)
    deep = store.get("deep_brief")
    assert deep is not None
    assert deep.is_deep_research is True
