"""Tests for the dashboard WebSocket connection manager."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import pytest

from ai_company.dashboard.ws import ConnectionManager, broadcast_kpi_update, broadcast_task_update, manager
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.models.task import Task, TaskStatus
from ai_company.store.file_store import FileStore
from ai_company.executor.loop import Executor

# ── Helpers ─────────────────────────────────────────────────────────


class FakeWebSocket:
    """Minimal mock for a WebSocket connection."""

    def __init__(self) -> None:
        self.sent: list[str] = []
        self.accepted = False
        self.closed = False

    async def accept(self) -> None:
        self.accepted = True

    async def send_text(self, data: str) -> None:
        if self.closed:
            raise RuntimeError("Connection closed")
        self.sent.append(data)

    async def send_json(self, data: dict[str, Any]) -> None:
        import json
        self.sent.append(json.dumps(data, default=str))

    async def receive_json(self) -> dict[str, Any]:
        raise asyncio.CancelledError  # simulates client disconnect


class FailingWebSocket(FakeWebSocket):
    """WebSocket that fails on send (simulates dead client)."""

    async def send_text(self, data: str) -> None:
        raise RuntimeError("Simulated send failure")


# ── ConnectionManager tests ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_connection_manager_tracks_clients() -> None:
    mgr = ConnectionManager()
    ws = FakeWebSocket()

    assert mgr.active_count == 0

    await mgr.connect(ws)
    assert mgr.active_count == 1
    assert ws.accepted is True

    await mgr.disconnect(ws)
    assert mgr.active_count == 0


@pytest.mark.asyncio
async def test_broadcast_sends_to_all() -> None:
    mgr = ConnectionManager()
    ws1 = FakeWebSocket()
    ws2 = FakeWebSocket()

    await mgr.connect(ws1)
    await mgr.connect(ws2)

    failures = await mgr.broadcast({"type": "test", "value": 42})

    assert failures == []
    assert len(ws1.sent) == 1
    assert len(ws2.sent) == 1

    import json

    msg1 = json.loads(ws1.sent[0])
    assert msg1["type"] == "test"
    assert msg1["value"] == 42


@pytest.mark.asyncio
async def test_disconnect_removes_client() -> None:
    mgr = ConnectionManager()
    ws = FakeWebSocket()

    await mgr.connect(ws)
    assert mgr.active_count == 1

    await mgr.disconnect(ws)
    assert mgr.active_count == 0

    # Disconnecting again should not error or go negative
    await mgr.disconnect(ws)
    assert mgr.active_count == 0


@pytest.mark.asyncio
async def test_broadcast_prunes_dead_connections() -> None:
    mgr = ConnectionManager()
    good = FakeWebSocket()
    dead = FailingWebSocket()

    await mgr.connect(good)
    await mgr.connect(dead)
    assert mgr.active_count == 2

    failures = await mgr.broadcast({"msg": "hello"})

    # Good client received the message
    assert len(good.sent) == 1
    # Dead client was pruned
    assert mgr.active_count == 1
    assert len(failures) == 1


@pytest.mark.asyncio
async def test_broadcast_kpi_update_pushes_to_manager() -> None:
    """broadcast_kpi_update() uses the module-level manager singleton."""
    ws = FakeWebSocket()
    await manager.connect(ws)

    try:
        await broadcast_kpi_update({
            "engineering": {"task_completion_rate": {"current": 92.5}},
        })

        assert len(ws.sent) == 1

        import json

        msg = json.loads(ws.sent[0])
        assert msg["type"] == "kpi_update"
        assert "timestamp" in msg
        assert "payload" in msg
        assert msg["payload"]["engineering"]["task_completion_rate"]["current"] == 92.5
    finally:
        await manager.disconnect(ws)


# ── Integration Tests: MessageBus → ConnectionManager ─────────────────


class MockExecutorWebSocket(FakeWebSocket):
    """WebSocket mock that works with the executor's sync→async bridge."""
    
    def __init__(self) -> None:
        super().__init__()
        self._loop = asyncio.get_event_loop()


@pytest.mark.asyncio
async def test_message_bus_broadcast_callback_emits_task_created(tmp_path) -> None:
    """MessageBus.send_task() triggers broadcast_callback which reaches WebSocket clients."""
    # Create a temp inbox
    inbox_path = tmp_path / "inbox.json"
    store = FileStore(tmp_path, backup=False)
    store.write_json("inbox.json", [])
    
    # Track broadcast events
    broadcast_events = []
    
    def capture_broadcast(task_dict: dict, event: str) -> None:
        broadcast_events.append((task_dict, event))
    
    # Create MessageBus with broadcast callback
    bus = MessageBus(storage_path=str(inbox_path), broadcast_callback=capture_broadcast)
    
    # Send a task
    task = Task(
        id="test-task-1",
        sender_id="ceo",
        receiver_id="cto",
        instruction="Test task",
        priority="high",
    )
    bus.send_task(task)
    
    # Verify broadcast was called
    assert len(broadcast_events) == 1
    task_dict, event = broadcast_events[0]
    assert event == "created"
    assert task_dict["id"] == "test-task-1"
    assert task_dict["sender_id"] == "ceo"
    assert task_dict["receiver_id"] == "cto"


@pytest.mark.asyncio
async def test_message_bus_broadcast_callback_emits_task_completed(tmp_path) -> None:
    """MessageBus.update_task_status() triggers broadcast on completion."""
    inbox_path = tmp_path / "inbox.json"
    store = FileStore(tmp_path, backup=False)
    store.write_json("inbox.json", [])
    
    broadcast_events = []
    
    def capture_broadcast(task_dict: dict, event: str) -> None:
        broadcast_events.append((task_dict, event))
    
    bus = MessageBus(storage_path=str(inbox_path), broadcast_callback=capture_broadcast)
    
    task = Task(
        id="test-task-2",
        sender_id="ceo",
        receiver_id="cto",
        instruction="Test task",
        status=TaskStatus.PENDING,
    )
    bus.send_task(task)
    
    # Clear the created event
    broadcast_events.clear()
    
    # Update status to completed
    bus.update_task_status("test-task-2", "completed", result="Done!")
    
    assert len(broadcast_events) == 1
    task_dict, event = broadcast_events[0]
    assert event == "completed"
    assert task_dict["status"] == "completed"
    assert task_dict["result"] == "Done!"


@pytest.mark.asyncio
async def test_message_bus_broadcast_callback_emits_task_failed(tmp_path) -> None:
    """MessageBus.update_task_status() triggers broadcast on failure."""
    inbox_path = tmp_path / "inbox.json"
    store = FileStore(tmp_path, backup=False)
    store.write_json("inbox.json", [])
    
    broadcast_events = []
    
    def capture_broadcast(task_dict: dict, event: str) -> None:
        broadcast_events.append((task_dict, event))
    
    bus = MessageBus(storage_path=str(inbox_path), broadcast_callback=capture_broadcast)
    
    task = Task(
        id="test-task-3",
        sender_id="ceo",
        receiver_id="cto",
        instruction="Test task",
        status=TaskStatus.PENDING,
    )
    bus.send_task(task)
    
    broadcast_events.clear()
    
    # Update status to failed
    bus.update_task_status("test-task-3", "failed", result="Error occurred")
    
    assert len(broadcast_events) == 1
    task_dict, event = broadcast_events[0]
    assert event == "failed"
    assert task_dict["status"] == "failed"


@pytest.mark.asyncio
async def test_message_bus_broadcast_callback_emits_task_escalated(tmp_path) -> None:
    """MessageBus.update_task_status() triggers broadcast on escalation."""
    inbox_path = tmp_path / "inbox.json"
    store = FileStore(tmp_path, backup=False)
    store.write_json("inbox.json", [])
    
    broadcast_events = []
    
    def capture_broadcast(task_dict: dict, event: str) -> None:
        broadcast_events.append((task_dict, event))
    
    bus = MessageBus(storage_path=str(inbox_path), broadcast_callback=capture_broadcast)
    
    task = Task(
        id="test-task-4",
        sender_id="ceo",
        receiver_id="cto",
        instruction="Test task",
        status=TaskStatus.PENDING,
    )
    bus.send_task(task)
    
    broadcast_events.clear()
    
    # Update status to escalated
    bus.update_task_status("test-task-4", "escalated")
    
    assert len(broadcast_events) == 1
    task_dict, event = broadcast_events[0]
    assert event == "escalated"
    assert task_dict["status"] == "escalated"


@pytest.mark.asyncio
async def test_broadcast_task_update_sends_to_websocket_clients() -> None:
    """broadcast_task_update() pushes task events to connected WebSocket clients."""
    ws = FakeWebSocket()
    await manager.connect(ws)
    
    try:
        task_dict = {
            "id": "test-task-ws-1",
            "sender_id": "ceo",
            "receiver_id": "cto",
            "instruction": "Test via WebSocket",
            "status": "completed",
            "result": "All done!",
        }
        
        await broadcast_task_update(task_dict, "completed")
        
        assert len(ws.sent) == 1
        msg = json.loads(ws.sent[0])
        assert msg["type"] == "task_update"
        assert msg["event"] == "completed"
        assert msg["payload"]["id"] == "test-task-ws-1"
        assert msg["payload"]["status"] == "completed"
    finally:
        await manager.disconnect(ws)


@pytest.mark.asyncio
async def test_topic_filtering_works_for_task_updates() -> None:
    """Clients subscribed to specific topics only receive matching broadcasts."""
    # Use a fresh manager for isolation
    mgr = ConnectionManager()
    ws_subscribed_to_tasks = FakeWebSocket()
    ws_subscribed_to_other = FakeWebSocket()
    ws_unsubscribed = FakeWebSocket()
    
    await mgr.connect(ws_subscribed_to_tasks)
    await mgr.connect(ws_subscribed_to_other)
    await mgr.connect(ws_unsubscribed)
    
    # Subscribe to different topics
    await mgr.subscribe(ws_subscribed_to_tasks, ["tasks"])
    await mgr.subscribe(ws_subscribed_to_other, ["alerts"])
    # ws_unsubscribed has empty subscription set (receives all)
    
    task_dict = {
        "id": "topic-test-1",
        "sender_id": "ceo",
        "receiver_id": "cto",
        "instruction": "Test topic filtering",
        "status": "pending",
    }
    
    # Broadcast with topic="tasks" - only ws_subscribed_to_tasks and ws_unsubscribed should receive
    await mgr.broadcast({
        "type": "task_update",
        "topic": "tasks",
        "event": "created",
        "payload": task_dict,
    })
    
    # Subscribed to "tasks" - should receive
    assert len(ws_subscribed_to_tasks.sent) == 1
    # Subscribed to "alerts" only - should NOT receive "tasks" topic
    assert len(ws_subscribed_to_other.sent) == 0
    # Unsubscribed (empty set) - receives ALL messages for backward compatibility
    assert len(ws_unsubscribed.sent) == 1


@pytest.mark.asyncio
async def test_sync_to_async_bridge_works_with_running_event_loop() -> None:
    """The sync→async bridge in Executor._make_broadcast_callback() works when event loop is running."""
    ws = FakeWebSocket()
    await manager.connect(ws)

    try:
        callback = Executor._make_broadcast_callback()
        task_dict = {
            "id": "bridge-test-1",
            "sender_id": "ceo",
            "receiver_id": "cto",
            "instruction": "Test sync-to-async bridge",
            "status": "pending",
        }

        callback(task_dict, "created")
        await asyncio.sleep(0.01)

        assert len(ws.sent) == 1
        msg = json.loads(ws.sent[0])
        assert msg["type"] == "task_update"
        assert msg["payload"]["id"] == "bridge-test-1"
    finally:
        await manager.disconnect(ws)


def test_sync_to_async_bridge_skips_when_no_event_loop() -> None:
    """The sync→async bridge gracefully skips when no event loop is running (CLI context)."""
    # Deliberately NOT async and no @pytest.mark.asyncio — get_running_loop()
    # only raises RuntimeError when called from a synchronous context
    # with no loop running.
    callback = Executor._make_broadcast_callback()

    task_dict = {
        "id": "no-loop-test-1",
        "sender_id": "ceo",
        "receiver_id": "cto",
        "instruction": "Test no-loop skip",
        "status": "pending",
    }

    # Should not raise, even though there's no running event loop.
    callback(task_dict, "created")




@pytest.mark.asyncio
async def test_dead_connection_pruning_on_broadcast_failure() -> None:
    """Broadcast prunes dead WebSocket connections when send fails."""
    # Use fresh manager for isolation
    mgr = ConnectionManager()
    ws_good = FakeWebSocket()
    ws_dead = FailingWebSocket()
    
    await mgr.connect(ws_good)
    await mgr.connect(ws_dead)
    
    assert mgr.active_count == 2
    
    task_dict = {
        "id": "prune-test-1",
        "sender_id": "ceo",
        "receiver_id": "cto",
        "instruction": "Test pruning",
        "status": "pending",
    }
    
    await mgr.broadcast({
        "type": "task_update",
        "topic": "tasks",
        "event": "created",
        "payload": task_dict,
    })
    
    # Good connection should still be there
    assert len(ws_good.sent) == 1
    # Dead connection should be pruned
    assert mgr.active_count == 1
    
    await manager.disconnect(ws_good)


# ── Full Pipeline Tests ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_full_pipeline_message_bus_to_websocket(tmp_path) -> None:
    """End-to-end: MessageBus.send_task → broadcast_callback → ConnectionManager → WebSocket client."""
    inbox_path = tmp_path / "inbox.json"
    store = FileStore(tmp_path, backup=False)
    store.write_json("inbox.json", [])
    
    ws = FakeWebSocket()
    await manager.connect(ws)
    
    broadcast_events = []
    
    def capture_broadcast(task_dict: dict, event: str) -> None:
        broadcast_events.append((task_dict, event))
        # Also push to WebSocket manager (this is what the real callback does)
        import asyncio
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(broadcast_task_update(task_dict, event))
        except RuntimeError:
            pass  # No running loop - skip
    
    bus = MessageBus(storage_path=str(inbox_path), broadcast_callback=capture_broadcast)
    
    # Send task through MessageBus
    task = Task(
        id="e2e-task-1",
        sender_id="ceo",
        receiver_id="cto",
        instruction="E2E test task",
        priority="high",
    )
    bus.send_task(task)
    
    # Allow async tasks to complete
    await asyncio.sleep(0.05)
    
    # Verify WebSocket received the message
    assert len(ws.sent) == 1
    msg = json.loads(ws.sent[0])
    assert msg["type"] == "task_update"
    assert msg["event"] == "created"
    assert msg["payload"]["id"] == "e2e-task-1"
    
    await manager.disconnect(ws)
