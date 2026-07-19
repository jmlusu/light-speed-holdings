"""Tests for the dashboard WebSocket connection manager."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from ai_company.dashboard.ws import ConnectionManager, broadcast_kpi_update, manager


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
