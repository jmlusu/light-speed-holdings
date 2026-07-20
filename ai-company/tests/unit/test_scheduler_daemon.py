"""Tests for the scheduled-cycle daemon (Scheduler.run_forever)."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import List


from ai_company.orchestrator.scheduler import Scheduler, ScheduledTask


class _FakeBus:
    """Minimal stand-in for MessageBus that records sent tasks."""

    def __init__(self) -> None:
        self.sent: List[object] = []

    def send_task(self, task: object) -> None:
        self.sent.append(task)


class _RecordingSleep:
    """Fake sleep that records how many times and with what interval it's called."""

    def __init__(self) -> None:
        self.calls: List[float] = []

    def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)


def _make_scheduler(tmp_path: Path, due: bool) -> Scheduler:
    """Build a Scheduler backed by a temp config with one task."""
    config_path = tmp_path / "scheduler.yaml"
    scheduler = Scheduler(config_path=str(config_path))
    scheduler.tasks = [
        ScheduledTask(
            id="t1",
            name="Test Cycle Task",
            interval_minutes=60,
            enabled=True,
            next_run=datetime.now() - timedelta(minutes=1) if due else datetime.now() + timedelta(hours=1),
            task_template={"receiver_id": "chief-of-staff", "instruction": "ping"},
        )
    ]
    return scheduler


class TestRunForever:
    def test_max_cycles_bounds_loop(self, tmp_path: Path) -> None:
        scheduler = _make_scheduler(tmp_path, due=True)
        bus = _FakeBus()
        sleep = _RecordingSleep()

        cycles = scheduler.run_forever(bus, interval_seconds=30.0, max_cycles=2, sleep=sleep)

        assert cycles == 2
        # With max_cycles=2, sleep is called once (between cycle 1 and 2).
        assert sleep.calls == [30.0]
        # First cycle had a due task; second cycle the task was rescheduled.
        assert len(bus.sent) == 1

    def test_runs_until_keyboard_interrupt(self, tmp_path: Path) -> None:
        scheduler = _make_scheduler(tmp_path, due=True)
        bus = _FakeBus()

        def _interrupt(_: float) -> None:
            raise KeyboardInterrupt

        cycles = scheduler.run_forever(bus, interval_seconds=10.0, max_cycles=None, sleep=_interrupt)

        # Cycle 1 runs, then sleep raises KeyboardInterrupt -> stop after 1 cycle.
        assert cycles == 1

    def test_interval_respected_via_sleep(self, tmp_path: Path) -> None:
        scheduler = _make_scheduler(tmp_path, due=True)
        bus = _FakeBus()
        sleep = _RecordingSleep()

        scheduler.run_forever(bus, interval_seconds=45.5, max_cycles=3, sleep=sleep)

        # 3 cycles => 2 sleeps, each with the configured interval.
        assert sleep.calls == [45.5, 45.5]

    def test_no_due_tasks_still_counts_cycles(self, tmp_path: Path) -> None:
        scheduler = _make_scheduler(tmp_path, due=False)
        bus = _FakeBus()
        sleep = _RecordingSleep()

        cycles = scheduler.run_forever(bus, interval_seconds=5.0, max_cycles=2, sleep=sleep)

        assert cycles == 2
        assert bus.sent == []
        assert sleep.calls == [5.0]
