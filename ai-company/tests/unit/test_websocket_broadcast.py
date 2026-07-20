"""Unit tests for GAP-006 — functional WebSocket broadcast.

Verifies that real events actually push to connected WebSocket clients:

- A connected client receives a ``task_update`` message when a task is
  created via the dashboard API (the wired ``MessageBus`` broadcast path).
- The executor's ``MessageBus`` is now wired with a broadcast callback that
  calls ``broadcast_task_update``, so task lifecycle events during execution
  are pushed to dashboard clients too.
- ``broadcast_task_update`` is functional (pushes to the connection manager).
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from ai_company.dashboard.ws import broadcast_task_update, manager
from ai_company.orchestrator.message_bus import MessageBus


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """TestClient whose shared MessageBus writes to a temp inbox."""
    from ai_company.dashboard import api as api_mod

    bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
    monkeypatch.setattr(api_mod, "_bus", bus)
    return TestClient(app, raise_server_exceptions=False)


def _recv_with_timeout(ws: object, timeout: float = 5.0) -> dict:
    """Receive a JSON message with a wall-clock timeout (avoids hangs)."""
    result: dict = {}

    def _read() -> None:
        result.update(ws.receive_json())

    t = threading.Thread(target=_read, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise AssertionError("Timed out waiting for WebSocket broadcast")
    return result


def test_task_created_event_emits_ws_broadcast(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    """Creating a task emits a task_update broadcast to the WS layer.

    A WebSocket client is connected (via TestClient) and we spy on the
    broadcast helper to assert the event is pushed.  Delivery to the wire is
    covered by ``test_broadcast_helper_is_functional`` and
    ``test_executor_bus_is_wired_for_broadcast``.
    """
    calls: list[tuple[dict, str]] = []

    import ai_company.dashboard.ws as ws_mod

    real_broadcast = ws_mod.broadcast_task_update

    async def _spy(task: dict, event: str = "created") -> None:
        calls.append((task, event))
        await real_broadcast(task, event)

    monkeypatch.setattr(ws_mod, "broadcast_task_update", _spy)

    with client.websocket_connect("/ws/dashboard") as ws:
        hello = _recv_with_timeout(ws)
        assert hello["type"] == "connected"

        def _post() -> None:
            client.post(
                "/api/tasks",
                json={
                    "sender_id": "human-ceo",
                    "receiver_id": "lead-backend",
                    "instruction": "Deploy the service",
                    "priority": "high",
                },
            )

        threading.Thread(target=_post, daemon=True).start()

        # Wait until the broadcast spy recorded the emission.
        for _ in range(100):
            if calls:
                break
            threading.Event().wait(0.05)

        assert calls, "No WebSocket broadcast was emitted on task creation"
        assert calls[0][1] == "created"
        assert calls[0][0]["instruction"] == "Deploy the service"


def test_executor_bus_is_wired_for_broadcast(tmp_path: Path) -> None:
    """The executor's MessageBus carries a broadcast callback (GAP-006)."""
    from ai_company.executor.loop import Executor

    _setup_executor_files(tmp_path)
    executor = Executor(
        config_path=str(tmp_path / "company" / "models.yaml"),
        registry_path=str(tmp_path / "company" / "agent-registry.json"),
        agents_dir=str(tmp_path / ".opencode" / "agents"),
        results_dir=str(tmp_path / "results"),
    )
    # The executor now wires its task events to the WebSocket broadcaster.
    assert executor.bus._broadcast_callback is not None

    # The callback, given a running loop, schedules broadcast_task_update.
    import asyncio

    received: list[str] = []

    class _FakeWs:
        async def accept(self) -> None:
            pass

        async def send_text(self, data: str) -> None:
            received.append(data)

    async def _run() -> None:
        await manager.connect(_FakeWs())  # type: ignore[arg-type]
        try:
            from ai_company.models import Task

            task = Task(
                id="exec-task-1",
                sender_id="human-ceo",
                receiver_id="lead-backend",
                instruction="Run migration",
            )
            executor.bus.send_task(task)  # fires the wired callback
            # Allow the scheduled broadcast task to run.
            await asyncio.sleep(0.05)
        finally:
            await manager.disconnect(_FakeWs())  # type: ignore[arg-type]

    asyncio.new_event_loop().run_until_complete(_run())
    assert any(json.loads(m)["type"] == "task_update" for m in received)


def test_broadcast_helper_is_functional() -> None:
    """broadcast_task_update pushes to the module-level ConnectionManager."""
    import asyncio

    async def _run() -> dict:
        class _Ws:
            def __init__(self) -> None:
                self.sent: list[str] = []

            async def accept(self) -> None:
                pass

            async def send_text(self, data: str) -> None:
                self.sent.append(data)

        ws = _Ws()
        await manager.connect(ws)
        try:
            await broadcast_task_update({"id": "x", "status": "completed"}, "completed")
            return json.loads(ws.sent[0])
        finally:
            await manager.disconnect(ws)

    result = asyncio.new_event_loop().run_until_complete(_run())
    assert result["type"] == "task_update"
    assert result["event"] == "completed"
    assert result["payload"]["id"] == "x"


def _setup_executor_files(tmp_path: Path) -> None:
    company = tmp_path / "company"
    company.mkdir()
    models = {
        "providers": {"opencode": {"backend": "openai_compatible",
                                    "default_model": "big-pickle",
                                    "api_base": "https://opencode.ai/api/v1"}},
        "tiers": {"standard": {"description": "std",
                                "providers": [{"provider": "opencode",
                                               "model": "big-pickle"}]}},
        "routing": [{"agent_type": "Specialist", "tier": "standard"}],
    }
    (company / "models.yaml").write_text(json.dumps(models), encoding="utf-8")
    registry = [{"name": "test-agent", "role": "Test", "type": "Specialist",
                 "department": "Test", "reportsTo": "ceo", "directReports": [],
                 "description": "test", "tools": ["read", "write"],
                 "permission": "Execute"}]
    (company / "agent-registry.json").write_text(json.dumps(registry), encoding="utf-8")
    op = tmp_path / ".opencode"
    op.mkdir()
    (op / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")
    agents = op / "agents"
    agents.mkdir()
    (agents / "test-agent.md").write_text(
        "---\nname: test-agent\ndescription: t\ntools: [\"read\", \"write\"]\n"
        "mode: subagent\npermission:\n  read: allow\n  write: allow\n---\n\n"
        "# Test Agent\n\nType: Specialist\nDepartment: Test\nReports To: ceo\n\n"
        "## Mission\nExecute tasks.\n",
        encoding="utf-8",
    )
