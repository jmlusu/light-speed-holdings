"""End-to-end WebSocket integration tests.

Exercises the full pipeline: MessageBus → ConnectionManager → WebSocket clients.

Covers:
  1. MessageBus task lifecycle → WebSocket broadcast (created, completed, failed, escalated)
  2. Topic filtering and subscription management
  3. Connection lifecycle (connect, disconnect, reconnect)
  4. Multi-client broadcast delivery
  5. Error handling and dead-connection pruning
  6. broadcast helpers (kpi, alert, task, department, escalation)
  7. make_message_bus_broadcast_callback sync→async bridge

All tests are isolated via tmp_path and mock external dependencies.  No real
network calls are made.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest

from ai_company.dashboard.ws import (
    ConnectionManager,
    broadcast_alert,
    broadcast_department_kpis,
    broadcast_escalation,
    broadcast_kpi_update,
    broadcast_task_update,
    make_message_bus_broadcast_callback,
    manager,
)
from ai_company.models.task import Task
from ai_company.orchestrator.message_bus import MessageBus


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class RecordingWebSocket:
    """Fake WebSocket that records every message sent."""

    def __init__(self, *, fail_after: int | None = None) -> None:
        self.sent: list[str] = []
        self.accepted = False
        self._fail_after = fail_after

    async def accept(self) -> None:
        self.accepted = True

    async def send_text(self, data: str) -> None:
        if self._fail_after is not None and len(self.sent) >= self._fail_after:
            raise RuntimeError("Simulated connection failure")
        self.sent.append(data)

    async def send_json(self, data: dict[str, Any]) -> None:
        self.sent.append(json.dumps(data, default=str))

    async def receive_json(self) -> dict[str, Any]:
        raise asyncio.CancelledError()

    def last_message(self) -> dict[str, Any]:
        return json.loads(self.sent[-1])

    def messages_of_type(self, msg_type: str) -> list[dict[str, Any]]:
        return [json.loads(m) for m in self.sent if json.loads(m).get("type") == msg_type]


class BlockingWebSocket(RecordingWebSocket):
    """WebSocket whose receive_json blocks until closed."""

    def __init__(self) -> None:
        super().__init__()
        self._closed = asyncio.Event()

    async def receive_json(self) -> dict[str, Any]:
        await self._closed.wait()
        raise asyncio.CancelledError()

    def close(self) -> None:
        self._closed.set()


@pytest.fixture()
def connection_manager() -> ConnectionManager:
    """A fresh ConnectionManager for each test."""
    return ConnectionManager()


@pytest.fixture()
def isolated_bus(tmp_path: Path) -> MessageBus:
    """A MessageBus pointed at a temp directory (no broadcast callback)."""
    return MessageBus(storage_path=str(tmp_path / "inbox.json"))


@pytest.fixture()
def wired_bus(tmp_path: Path) -> tuple[MessageBus, ConnectionManager]:
    """MessageBus wired to a fresh ConnectionManager via the sync→async bridge."""
    mgr = ConnectionManager()
    cb = make_message_bus_broadcast_callback()
    bus = MessageBus(
        storage_path=str(tmp_path / "inbox.json"),
        broadcast_callback=cb,
    )
    return bus, mgr


# ════════════════════════════════════════════════════════════════════════════
# 1. MessageBus → WebSocket → Client pipeline
# ════════════════════════════════════════════════════════════════════════════


class TestMessageBusToWebSocketPipeline:
    """Verify that task lifecycle events flow from MessageBus to WS clients."""

    def test_send_task_broadcasts_created_event(
        self, tmp_path: Path, connection_manager: ConnectionManager
    ) -> None:
        """send_task → broadcast_callback → WS clients receive task_update (created)."""
        events: list[tuple[dict, str]] = []

        def _capture(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=_capture,
        )

        task = Task(
            id="pipeline-1",
            sender_id="human-ceo",
            receiver_id="lead-frontend",
            instruction="Build the dashboard",
        )
        bus.send_task(task)

        assert len(events) == 1
        assert events[0][1] == "created"
        assert events[0][0]["id"] == "pipeline-1"
        assert events[0][0]["instruction"] == "Build the dashboard"

    def test_update_status_broadcasts_completed_event(
        self, tmp_path: Path, connection_manager: ConnectionManager
    ) -> None:
        """update_task_status(completed) → broadcast "completed" to WS."""
        events: list[tuple[dict, str]] = []

        def _capture(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=_capture,
        )
        task = Task(id="t-completed", sender_id="a", receiver_id="b", instruction="x")
        bus.send_task(task)

        result = bus.update_task_status("t-completed", "completed", result="all done")
        assert result is not None
        assert len(events) == 2
        assert events[1][1] == "completed"
        assert events[1][0]["result"] == "all done"

    def test_update_status_broadcasts_failed_event(self, tmp_path: Path) -> None:
        """update_task_status(failed) → broadcast "failed"."""
        events: list[tuple[dict, str]] = []

        def _capture(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=_capture,
        )
        task = Task(id="t-failed", sender_id="a", receiver_id="b", instruction="y")
        bus.send_task(task)
        bus.update_task_status("t-failed", "failed", result="timeout")

        assert len(events) == 2
        assert events[1][1] == "failed"

    def test_update_status_broadcasts_escalated_event(self, tmp_path: Path) -> None:
        """update_task_status(escalated) → broadcast "escalated"."""
        events: list[tuple[dict, str]] = []

        def _capture(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=_capture,
        )
        task = Task(id="t-esc", sender_id="a", receiver_id="b", instruction="z")
        bus.send_task(task)
        bus.update_task_status("t-esc", "escalated")

        assert len(events) == 2
        assert events[1][1] == "escalated"

    def test_update_status_broadcasts_status_changed(self, tmp_path: Path) -> None:
        """Non-terminal status → broadcast "status_changed"."""
        events: list[tuple[dict, str]] = []

        def _capture(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=_capture,
        )
        task = Task(id="t-prog", sender_id="a", receiver_id="b", instruction="p")
        bus.send_task(task)
        bus.update_task_status("t-prog", "in_progress")

        assert len(events) == 2
        assert events[1][1] == "status_changed"

    def test_full_lifecycle_broadcasts_four_events(self, tmp_path: Path) -> None:
        """Full lifecycle: created → in_progress → completed produces 3 events."""
        events: list[tuple[dict, str]] = []

        def _capture(task_dict: dict[str, Any], event: str) -> None:
            events.append((task_dict, event))

        bus = MessageBus(
            storage_path=str(tmp_path / "inbox.json"),
            broadcast_callback=_capture,
        )
        task = Task(id="t-full", sender_id="a", receiver_id="b", instruction="lifecycle")
        bus.send_task(task)
        bus.update_task_status("t-full", "in_progress")
        bus.update_task_status("t-full", "completed", result="done")

        event_types = [e[1] for e in events]
        assert event_types == ["created", "status_changed", "completed"]


# ════════════════════════════════════════════════════════════════════════════
# 2. Topic filtering and subscription
# ════════════════════════════════════════════════════════════════════════════


class TestTopicFiltering:
    """Verify topic-based broadcast filtering in ConnectionManager."""

    @pytest.mark.asyncio
    async def test_unsubscribed_client_receives_all_messages(
        self, connection_manager: ConnectionManager
    ) -> None:
        """A client with no subscriptions receives everything (backward compat)."""
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)

        await connection_manager.broadcast({"type": "kpi", "data": "a"})
        await connection_manager.broadcast({"type": "alert", "data": "b", "topic": "alerts"})

        assert len(ws.sent) == 2

    @pytest.mark.asyncio
    async def test_subscribed_client_receives_matching_topic(
        self, connection_manager: ConnectionManager
    ) -> None:
        """A client subscribed to 'kpis' receives kpi messages."""
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)
        await connection_manager.subscribe(ws, ["kpis"])

        await connection_manager.broadcast({"type": "kpi", "topic": "kpis", "data": 1})
        assert len(ws.sent) == 1
        assert json.loads(ws.sent[0])["type"] == "kpi"

    @pytest.mark.asyncio
    async def test_subscribed_client_filters_non_matching_topics(
        self, connection_manager: ConnectionManager
    ) -> None:
        """A client subscribed to 'kpis' does NOT receive 'alerts' messages."""
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)
        await connection_manager.subscribe(ws, ["kpis"])

        await connection_manager.broadcast({"type": "alert", "topic": "alerts", "data": 1})
        assert len(ws.sent) == 0

    @pytest.mark.asyncio
    async def test_wildcard_subscription_receives_all_topics(
        self, connection_manager: ConnectionManager
    ) -> None:
        """A client subscribed to '*' receives messages on any topic."""
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)
        await connection_manager.subscribe(ws, ["*"])

        await connection_manager.broadcast({"type": "a", "topic": "kpis"})
        await connection_manager.broadcast({"type": "b", "topic": "alerts"})
        await connection_manager.broadcast({"type": "c", "topic": "tasks"})

        assert len(ws.sent) == 3

    @pytest.mark.asyncio
    async def test_multiple_subscriptions(self, connection_manager: ConnectionManager) -> None:
        """A client subscribed to multiple topics receives all matching messages."""
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)
        await connection_manager.subscribe(ws, ["kpis", "alerts"])

        await connection_manager.broadcast({"type": "a", "topic": "kpis"})
        await connection_manager.broadcast({"type": "b", "topic": "alerts"})
        await connection_manager.broadcast({"type": "c", "topic": "tasks"})

        assert len(ws.sent) == 2
        types = [json.loads(m)["type"] for m in ws.sent]
        assert "a" in types
        assert "b" in types
        assert "c" not in types

    @pytest.mark.asyncio
    async def test_topic_filtered_for_different_clients(
        self, connection_manager: ConnectionManager
    ) -> None:
        """Each client only receives messages matching their subscriptions."""
        kpi_client = RecordingWebSocket()
        alert_client = RecordingWebSocket()
        all_client = RecordingWebSocket()

        await connection_manager.connect(kpi_client)
        await connection_manager.connect(alert_client)
        await connection_manager.connect(all_client)

        await connection_manager.subscribe(kpi_client, ["kpis"])
        await connection_manager.subscribe(alert_client, ["alerts"])
        await connection_manager.subscribe(all_client, ["*"])

        await connection_manager.broadcast({"type": "kpi", "topic": "kpis", "data": 1})
        await connection_manager.broadcast({"type": "alert", "topic": "alerts", "data": 2})

        assert len(kpi_client.sent) == 1  # kpi only
        assert len(alert_client.sent) == 1  # alert only
        assert len(all_client.sent) == 2  # both


# ════════════════════════════════════════════════════════════════════════════
# 3. Connection lifecycle (connect, disconnect, reconnect)
# ════════════════════════════════════════════════════════════════════════════


class TestConnectionLifecycle:
    """Verify connect, disconnect, and reconnect behaviour."""

    @pytest.mark.asyncio
    async def test_connect_accepts_websocket(self, connection_manager: ConnectionManager) -> None:
        ws = RecordingWebSocket()
        assert connection_manager.active_count == 0

        await connection_manager.connect(ws)
        assert connection_manager.active_count == 1
        assert ws.accepted is True

    @pytest.mark.asyncio
    async def test_disconnect_removes_client(self, connection_manager: ConnectionManager) -> None:
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)
        assert connection_manager.active_count == 1

        await connection_manager.disconnect(ws)
        assert connection_manager.active_count == 0

    @pytest.mark.asyncio
    async def test_disconnect_idempotent(self, connection_manager: ConnectionManager) -> None:
        """Disconnecting a client not in the set is a no-op."""
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)
        await connection_manager.disconnect(ws)
        await connection_manager.disconnect(ws)  # second call
        assert connection_manager.active_count == 0

    @pytest.mark.asyncio
    async def test_reconnect_new_connection(
        self, connection_manager: ConnectionManager
    ) -> None:
        """A client that disconnects and reconnects appears as a new entry."""
        ws1 = RecordingWebSocket()
        await connection_manager.connect(ws1)
        await connection_manager.disconnect(ws1)
        assert connection_manager.active_count == 0

        ws2 = RecordingWebSocket()
        await connection_manager.connect(ws2)
        assert connection_manager.active_count == 1

        # ws1 should not receive broadcasts anymore
        await connection_manager.broadcast({"type": "test"})
        assert len(ws1.sent) == 0
        assert len(ws2.sent) == 1

    @pytest.mark.asyncio
    async def test_multiple_clients_connect_and_disconnect(
        self, connection_manager: ConnectionManager
    ) -> None:
        ws_a = RecordingWebSocket()
        ws_b = RecordingWebSocket()
        ws_c = RecordingWebSocket()

        await connection_manager.connect(ws_a)
        await connection_manager.connect(ws_b)
        await connection_manager.connect(ws_c)
        assert connection_manager.active_count == 3

        await connection_manager.disconnect(ws_b)
        assert connection_manager.active_count == 2

        await connection_manager.broadcast({"type": "test"})
        assert len(ws_a.sent) == 1
        assert len(ws_b.sent) == 0
        assert len(ws_c.sent) == 1

    @pytest.mark.asyncio
    async def test_subscriptions_cleaned_on_disconnect(
        self, connection_manager: ConnectionManager
    ) -> None:
        """Subscriptions are removed when a client disconnects."""
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)
        await connection_manager.subscribe(ws, ["kpis", "alerts"])
        assert ws in connection_manager._connections

        await connection_manager.disconnect(ws)
        ws_id = id(ws)
        assert ws_id not in connection_manager._subscriptions


# ════════════════════════════════════════════════════════════════════════════
# 4. Multi-client broadcast
# ════════════════════════════════════════════════════════════════════════════


class TestMultiClientBroadcast:
    """Verify that broadcast reaches all connected clients."""

    @pytest.mark.asyncio
    async def test_broadcast_reaches_all_clients(
        self, connection_manager: ConnectionManager
    ) -> None:
        clients = [RecordingWebSocket() for _ in range(5)]
        for ws in clients:
            await connection_manager.connect(ws)

        failures = await connection_manager.broadcast({"type": "event", "n": 42})
        assert failures == []

        for ws in clients:
            assert len(ws.sent) == 1
            msg = json.loads(ws.sent[0])
            assert msg["type"] == "event"
            assert msg["n"] == 42

    @pytest.mark.asyncio
    async def test_broadcast_returns_no_failures_for_healthy_clients(
        self, connection_manager: ConnectionManager
    ) -> None:
        for _ in range(10):
            ws = RecordingWebSocket()
            await connection_manager.connect(ws)

        failures = await connection_manager.broadcast({"msg": "hi"})
        assert failures == []

    @pytest.mark.asyncio
    async def test_broadcast_with_mixed_subscription_states(
        self, connection_manager: ConnectionManager
    ) -> None:
        """Unsubscribed + subscribed clients receive appropriate messages."""
        unsubscribed = RecordingWebSocket()
        kpi_subscribed = RecordingWebSocket()

        await connection_manager.connect(unsubscribed)
        await connection_manager.connect(kpi_subscribed)
        await connection_manager.subscribe(kpi_subscribed, ["kpis"])

        # Topic message: only unsubscribed (backward compat) + kpi_subscribed
        await connection_manager.broadcast({"type": "x", "topic": "kpis"})
        assert len(unsubscribed.sent) == 1
        assert len(kpi_subscribed.sent) == 1

        # Alert topic: only unsubscribed (backward compat)
        await connection_manager.broadcast({"type": "y", "topic": "alerts"})
        assert len(unsubscribed.sent) == 2  # +1
        assert len(kpi_subscribed.sent) == 1  # unchanged


# ════════════════════════════════════════════════════════════════════════════
# 5. Error handling and cleanup
# ════════════════════════════════════════════════════════════════════════════


class TestErrorHandling:
    """Verify dead connection pruning and error resilience."""

    @pytest.mark.asyncio
    async def test_dead_client_pruned_on_broadcast(
        self, connection_manager: ConnectionManager
    ) -> None:
        good = RecordingWebSocket()
        dead = RecordingWebSocket(fail_after=0)  # fails immediately

        await connection_manager.connect(good)
        await connection_manager.connect(dead)
        assert connection_manager.active_count == 2

        failures = await connection_manager.broadcast({"msg": "hello"})

        assert len(failures) == 1
        assert connection_manager.active_count == 1
        assert len(good.sent) == 1

    @pytest.mark.asyncio
    async def test_multiple_dead_clients_pruned(
        self, connection_manager: ConnectionManager
    ) -> None:
        alive = RecordingWebSocket()
        dead1 = RecordingWebSocket(fail_after=0)
        dead2 = RecordingWebSocket(fail_after=0)

        await connection_manager.connect(alive)
        await connection_manager.connect(dead1)
        await connection_manager.connect(dead2)

        failures = await connection_manager.broadcast({"msg": "x"})

        assert len(failures) == 2
        assert connection_manager.active_count == 1
        assert len(alive.sent) == 1

    @pytest.mark.asyncio
    async def test_all_dead_clients_results_in_empty_manager(
        self, connection_manager: ConnectionManager
    ) -> None:
        dead1 = RecordingWebSocket(fail_after=0)
        dead2 = RecordingWebSocket(fail_after=0)

        await connection_manager.connect(dead1)
        await connection_manager.connect(dead2)

        await connection_manager.broadcast({"msg": "boom"})
        assert connection_manager.active_count == 0

    @pytest.mark.asyncio
    async def test_broadcast_after_pruning_only_reaches_survivors(
        self, connection_manager: ConnectionManager
    ) -> None:
        good = RecordingWebSocket()
        dead = RecordingWebSocket(fail_after=0)

        await connection_manager.connect(good)
        await connection_manager.connect(dead)

        await connection_manager.broadcast({"msg": "first"})
        # Now only good is alive
        await connection_manager.broadcast({"msg": "second"})

        assert len(good.sent) == 2  # received both
        assert json.loads(good.sent[1])["msg"] == "second"


# ════════════════════════════════════════════════════════════════════════════
# 6. Broadcast helper functions
# ════════════════════════════════════════════════════════════════════════════


class TestBroadcastHelpers:
    """Verify the module-level broadcast helper functions."""

    @pytest.mark.asyncio
    async def test_broadcast_kpi_update(self, connection_manager: ConnectionManager) -> None:
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)

        # broadcast_kpi_update uses the module-level manager, so we
        # need to temporarily wire it.
        original_mgr_connections = manager._connections
        original_mgr_subs = manager._subscriptions
        try:
            manager._connections = connection_manager._connections
            manager._subscriptions = connection_manager._subscriptions

            await broadcast_kpi_update({"engineering": {"tasks": 10}})

            assert len(ws.sent) == 1
            msg = json.loads(ws.sent[0])
            assert msg["type"] == "kpi_update"
            assert msg["topic"] == "kpis"
            assert "timestamp" in msg
            assert msg["payload"]["engineering"]["tasks"] == 10
        finally:
            manager._connections = original_mgr_connections
            manager._subscriptions = original_mgr_subs

    @pytest.mark.asyncio
    async def test_broadcast_alert(self, connection_manager: ConnectionManager) -> None:
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)

        original_mgr_connections = manager._connections
        original_mgr_subs = manager._subscriptions
        try:
            manager._connections = connection_manager._connections
            manager._subscriptions = connection_manager._subscriptions

            await broadcast_alert({"severity": "high", "message": "CPU spike"})

            assert len(ws.sent) == 1
            msg = json.loads(ws.sent[0])
            assert msg["type"] == "alert"
            assert msg["topic"] == "alerts"
            assert msg["payload"]["severity"] == "high"
        finally:
            manager._connections = original_mgr_connections
            manager._subscriptions = original_mgr_subs

    @pytest.mark.asyncio
    async def test_broadcast_task_update(self, connection_manager: ConnectionManager) -> None:
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)

        original_mgr_connections = manager._connections
        original_mgr_subs = manager._subscriptions
        try:
            manager._connections = connection_manager._connections
            manager._subscriptions = connection_manager._subscriptions

            await broadcast_task_update({"id": "t-1", "status": "completed"}, "completed")

            assert len(ws.sent) == 1
            msg = json.loads(ws.sent[0])
            assert msg["type"] == "task_update"
            assert msg["topic"] == "tasks"
            assert msg["event"] == "completed"
        finally:
            manager._connections = original_mgr_connections
            manager._subscriptions = original_mgr_subs

    @pytest.mark.asyncio
    async def test_broadcast_department_kpis(self, connection_manager: ConnectionManager) -> None:
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)

        original_mgr_connections = manager._connections
        original_mgr_subs = manager._subscriptions
        try:
            manager._connections = connection_manager._connections
            manager._subscriptions = connection_manager._subscriptions

            await broadcast_department_kpis("engineering", {"tasks_completed": 42})

            assert len(ws.sent) == 1
            msg = json.loads(ws.sent[0])
            assert msg["type"] == "department_kpi"
            assert msg["topic"] == "department:engineering"
            assert msg["department"] == "engineering"
            assert msg["payload"]["tasks_completed"] == 42
        finally:
            manager._connections = original_mgr_connections
            manager._subscriptions = original_mgr_subs

    @pytest.mark.asyncio
    async def test_broadcast_escalation(self, connection_manager: ConnectionManager) -> None:
        ws = RecordingWebSocket()
        await connection_manager.connect(ws)

        original_mgr_connections = manager._connections
        original_mgr_subs = manager._subscriptions
        try:
            manager._connections = connection_manager._connections
            manager._subscriptions = connection_manager._subscriptions

            await broadcast_escalation({"task_id": "t-99", "reason": "SLA breach"})

            assert len(ws.sent) == 1
            msg = json.loads(ws.sent[0])
            assert msg["type"] == "escalation"
            assert msg["topic"] == "escalations"
            assert msg["payload"]["task_id"] == "t-99"
        finally:
            manager._connections = original_mgr_connections
            manager._subscriptions = original_mgr_subs

    @pytest.mark.asyncio
    async def test_broadcast_helpers_only_reach_subscribed_clients(
        self, connection_manager: ConnectionManager
    ) -> None:
        """Helpers set a topic; only matching subscribers receive the message."""
        kpi_ws = RecordingWebSocket()
        alert_ws = RecordingWebSocket()
        all_ws = RecordingWebSocket()

        await connection_manager.connect(kpi_ws)
        await connection_manager.connect(alert_ws)
        await connection_manager.connect(all_ws)

        await connection_manager.subscribe(kpi_ws, ["kpis"])
        await connection_manager.subscribe(alert_ws, ["alerts"])
        await connection_manager.subscribe(all_ws, ["*"])

        original_mgr_connections = manager._connections
        original_mgr_subs = manager._subscriptions
        try:
            manager._connections = connection_manager._connections
            manager._subscriptions = connection_manager._subscriptions

            await broadcast_kpi_update({"v": 1})
            await broadcast_alert({"msg": "fire"})

            assert len(kpi_ws.sent) == 1  # kpi only
            assert len(alert_ws.sent) == 1  # alert only
            assert len(all_ws.sent) == 2  # both
        finally:
            manager._connections = original_mgr_connections
            manager._subscriptions = original_mgr_subs


# ════════════════════════════════════════════════════════════════════════════
# 7. make_message_bus_broadcast_callback (sync→async bridge)
# ════════════════════════════════════════════════════════════════════════════


class TestSyncAsyncBridge:
    """Verify the sync→async bridge for MessageBus callback integration."""

    def test_callback_returns_callable(self) -> None:
        cb = make_message_bus_broadcast_callback()
        assert callable(cb)

    def test_callback_schedules_broadcast(self, tmp_path: Path) -> None:
        """When an event loop is running, the callback schedules broadcast_task_update."""
        cb = make_message_bus_broadcast_callback()

        original_connections = manager._connections
        original_subs = manager._subscriptions
        try:
            ws = RecordingWebSocket()
            manager._connections = [ws]
            manager._subscriptions = {id(ws): set()}

            async def _run() -> None:
                cb({"id": "bridge-1", "status": "completed"}, "created")
                # Allow the scheduled task to execute
                await asyncio.sleep(0.05)

            asyncio.new_event_loop().run_until_complete(_run())

            assert len(ws.sent) == 1
            msg = json.loads(ws.sent[0])
            assert msg["type"] == "task_update"
            assert msg["event"] == "created"
        finally:
            manager._connections = original_connections
            manager._subscriptions = original_subs

    def test_callback_graceful_without_event_loop(self) -> None:
        """Without a running event loop, the callback silently skips (CLI context)."""
        cb = make_message_bus_broadcast_callback()
        # Should not raise
        cb({"id": "no-loop"}, "created")


# ════════════════════════════════════════════════════════════════════════════
# 8. End-to-end: MessageBus → broadcast callback → ConnectionManager → clients
# ════════════════════════════════════════════════════════════════════════════


class TestEndToEndPipeline:
    """Full stack: MessageBus write → sync callback → async broadcast → WS clients."""

    @pytest.mark.asyncio
    async def test_task_creation_end_to_end(self, tmp_path: Path) -> None:
        """Creating a task on a wired MessageBus delivers it to connected WS clients."""
        mgr = ConnectionManager()
        ws_client = RecordingWebSocket()
        await mgr.connect(ws_client)

        # Swap the module-level manager's internals
        original_connections = manager._connections
        original_subs = manager._subscriptions
        try:
            manager._connections = mgr._connections
            manager._subscriptions = mgr._subscriptions

            cb = make_message_bus_broadcast_callback()
            bus = MessageBus(
                storage_path=str(tmp_path / "inbox.json"),
                broadcast_callback=cb,
            )

            task = Task(
                id="e2e-1",
                sender_id="human-ceo",
                receiver_id="lead-frontend",
                instruction="Build WebSocket tests",
            )
            bus.send_task(task)
            # Allow the scheduled broadcast task to run
            await asyncio.sleep(0.1)

            assert len(ws_client.sent) >= 1
            # The first message from the connect is NOT the connected hello
            # (we bypassed the endpoint). Find the task_update message.
            task_msgs = [
                json.loads(m)
                for m in ws_client.sent
                if json.loads(m).get("type") == "task_update"
            ]
            assert len(task_msgs) == 1
            assert task_msgs[0]["event"] == "created"
            assert task_msgs[0]["payload"]["id"] == "e2e-1"
        finally:
            manager._connections = original_connections
            manager._subscriptions = original_subs

    @pytest.mark.asyncio
    async def test_task_status_change_end_to_end(self, tmp_path: Path) -> None:
        """Updating task status delivers the event to connected WS clients."""
        mgr = ConnectionManager()
        ws_client = RecordingWebSocket()
        await mgr.connect(ws_client)

        original_connections = manager._connections
        original_subs = manager._subscriptions
        try:
            manager._connections = mgr._connections
            manager._subscriptions = mgr._subscriptions

            cb = make_message_bus_broadcast_callback()
            bus = MessageBus(
                storage_path=str(tmp_path / "inbox.json"),
                broadcast_callback=cb,
            )

            task = Task(id="e2e-2", sender_id="a", receiver_id="b", instruction="test")
            bus.send_task(task)
            await asyncio.sleep(0.05)

            bus.update_task_status("e2e-2", "completed", result="passed")
            await asyncio.sleep(0.1)

            task_msgs = [
                json.loads(m)
                for m in ws_client.sent
                if json.loads(m).get("type") == "task_update"
            ]
            # At least "created" + "completed"
            events = [m["event"] for m in task_msgs]
            assert "created" in events
            assert "completed" in events
        finally:
            manager._connections = original_connections
            manager._subscriptions = original_subs

    @pytest.mark.asyncio
    async def test_topic_filtered_end_to_end(self, tmp_path: Path) -> None:
        """Topic-filtered subscribers only receive relevant events."""
        mgr = ConnectionManager()
        kpi_ws = RecordingWebSocket()
        task_ws = RecordingWebSocket()

        await mgr.connect(kpi_ws)
        await mgr.connect(task_ws)
        await mgr.subscribe(kpi_ws, ["kpis"])
        await mgr.subscribe(task_ws, ["tasks"])

        original_connections = manager._connections
        original_subs = manager._subscriptions
        try:
            manager._connections = mgr._connections
            manager._subscriptions = mgr._subscriptions

            cb = make_message_bus_broadcast_callback()
            bus = MessageBus(
                storage_path=str(tmp_path / "inbox.json"),
                broadcast_callback=cb,
            )

            task = Task(id="e2e-3", sender_id="a", receiver_id="b", instruction="filter")
            bus.send_task(task)
            await asyncio.sleep(0.1)

            task_events = [
                json.loads(m)
                for m in task_ws.sent
                if json.loads(m).get("type") == "task_update"
            ]
            kpi_events = [
                json.loads(m)
                for m in kpi_ws.sent
                if json.loads(m).get("type") == "task_update"
            ]
            assert len(task_events) >= 1
            assert len(kpi_events) == 0  # kpi subscriber doesn't get task events
        finally:
            manager._connections = original_connections
            manager._subscriptions = original_subs

    @pytest.mark.asyncio
    async def test_multi_client_end_to_end(self, tmp_path: Path) -> None:
        """Multiple clients all receive the same task creation event."""
        mgr = ConnectionManager()
        clients = [RecordingWebSocket() for _ in range(3)]
        for ws in clients:
            await mgr.connect(ws)

        original_connections = manager._connections
        original_subs = manager._subscriptions
        try:
            manager._connections = mgr._connections
            manager._subscriptions = mgr._subscriptions

            cb = make_message_bus_broadcast_callback()
            bus = MessageBus(
                storage_path=str(tmp_path / "inbox.json"),
                broadcast_callback=cb,
            )

            task = Task(id="e2e-multi", sender_id="a", receiver_id="b", instruction="all")
            bus.send_task(task)
            await asyncio.sleep(0.1)

            for ws in clients:
                task_msgs = [
                    json.loads(m)
                    for m in ws.sent
                    if json.loads(m).get("type") == "task_update"
                ]
                assert len(task_msgs) >= 1
                assert task_msgs[0]["payload"]["id"] == "e2e-multi"
        finally:
            manager._connections = original_connections
            manager._subscriptions = original_subs

    @pytest.mark.asyncio
    async def test_dead_client_not_breaking_pipeline(self, tmp_path: Path) -> None:
        """A dead client during broadcast does not crash the MessageBus pipeline."""
        mgr = ConnectionManager()
        good = RecordingWebSocket()
        dead = RecordingWebSocket(fail_after=0)

        await mgr.connect(good)
        await mgr.connect(dead)

        original_connections = manager._connections
        original_subs = manager._subscriptions
        try:
            manager._connections = mgr._connections
            manager._subscriptions = mgr._subscriptions

            cb = make_message_bus_broadcast_callback()
            bus = MessageBus(
                storage_path=str(tmp_path / "inbox.json"),
                broadcast_callback=cb,
            )

            # Should not raise despite dead client
            task = Task(id="e2e-dead", sender_id="a", receiver_id="b", instruction="fail")
            bus.send_task(task)
            await asyncio.sleep(0.1)

            # Good client received the event
            task_msgs = [
                json.loads(m)
                for m in good.sent
                if json.loads(m).get("type") == "task_update"
            ]
            assert len(task_msgs) >= 1
            assert mgr.active_count == 1  # dead client pruned
        finally:
            manager._connections = original_connections
            manager._subscriptions = original_subs
