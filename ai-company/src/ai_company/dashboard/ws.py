"""WebSocket handler for live dashboard updates."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Tracks active WebSocket clients and handles broadcast."""

    def __init__(self) -> None:
        self._connections: list[WebSocket] = []
        self._subscriptions: dict[int, set[str]] = {}  # ws_id → set of topics
        self._lock = asyncio.Lock()

    @property
    def active_count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.append(websocket)
            self._subscriptions[id(websocket)] = set()
        logger.info("WebSocket client connected (%d active)", self.active_count)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            if websocket in self._connections:
                self._connections.remove(websocket)
            self._subscriptions.pop(id(websocket), None)
        logger.info("WebSocket client disconnected (%d active)", self.active_count)

    async def subscribe(self, websocket: WebSocket, topics: list[str]) -> None:
        """Register topic subscriptions for a client."""
        async with self._lock:
            ws_id = id(websocket)
            if ws_id in self._subscriptions:
                self._subscriptions[ws_id].update(topics)
        logger.debug("Client subscribed to topics: %s", topics)

    async def broadcast(self, message: dict[str, Any]) -> list[str]:
        """Send *message* to every connected client.

        If a message has a ``"topic"`` key, only clients subscribed to
        that topic receive it.  Messages without a topic go to everyone.

        Returns a list of client IDs that failed so the caller can decide
        whether to prune them.
        """
        topic = message.get("topic")
        payload = json.dumps(message, default=str)
        failed: list[WebSocket] = []

        async with self._lock:
            snapshot = list(self._connections)
            subs_snapshot = dict(self._subscriptions)

        for ws in snapshot:
            # Topic-based filtering.
            # Clients with an empty subscription set (default, never
            # subscribed) receive *all* messages for backward compatibility.
            if topic is not None:
                ws_topics = subs_snapshot.get(id(ws), set())
                if ws_topics and topic not in ws_topics and "*" not in ws_topics:
                    continue
            try:
                await ws.send_text(payload)
            except Exception:
                logger.warning("Failed to send to client, marking for removal")
                failed.append(ws)

        # Prune dead connections outside the iteration
        if failed:
            async with self._lock:
                for ws in failed:
                    if ws in self._connections:
                        self._connections.remove(ws)
                    self._subscriptions.pop(id(ws), None)

        return [str(id(f)) for f in failed]


# Module-level singleton — importable by other modules for broadcast
manager = ConnectionManager()


# ── WebSocket endpoint ──────────────────────────────────────────────


@router.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket) -> None:
    """Single WebSocket endpoint for live dashboard updates.

    Protocol:
      - Server sends JSON messages (KPI snapshots, alerts, etc.)
      - Client may send ``{"type": "ping"}`` for application-level keepalive;
        server replies with ``{"type": "pong", ...}``.
      - Server also sends WebSocket-level pings via ``websockets`` library
        (handled by FastAPI/Starlette under the hood).
    """
    await manager.connect(websocket)
    try:
        # Send an initial hello so the client knows the connection is live
        await websocket.send_json({
            "type": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_clients": manager.active_count,
        })

        while True:
            # Keep the connection alive and handle client messages
            data = await websocket.receive_json()
            msg_type = data.get("type", "")

            if msg_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            elif msg_type == "subscribe":
                topics = data.get("topics", [])
                await manager.subscribe(websocket, topics)
                await websocket.send_json({
                    "type": "subscribed",
                    "topics": topics,
                })
            elif msg_type == "unsubscribe":
                # Remove specific topics
                topics_to_remove = set(data.get("topics", []))
                async with manager._lock:
                    ws_id = id(websocket)
                    if ws_id in manager._subscriptions:
                        manager._subscriptions[ws_id] -= topics_to_remove
                await websocket.send_json({
                    "type": "unsubscribed",
                    "topics": data.get("topics", []),
                })
            else:
                await websocket.send_json({
                    "type": "error",
                    "detail": f"Unknown message type: {msg_type}",
                })

    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("WebSocket error")
    finally:
        await manager.disconnect(websocket)


# ── Public broadcast helpers ────────────────────────────────────────


async def broadcast_kpi_update(data: dict[str, Any]) -> None:
    """Push a KPI update to all connected dashboard clients."""
    await manager.broadcast({
        "type": "kpi_update",
        "topic": "kpis",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": data,
    })


async def broadcast_alert(alert: dict[str, Any]) -> None:
    """Push an alert / notification to all connected clients."""
    await manager.broadcast({
        "type": "alert",
        "topic": "alerts",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": alert,
    })


async def broadcast_task_update(task: dict[str, Any], event: str = "created") -> None:
    """Push a task lifecycle event to all connected clients.

    Parameters
    ----------
    task:
        The task dict (must be JSON-serialisable).
    event:
        One of ``"created"``, ``"completed"``, ``"failed"``, ``"escalated"``.
    """
    await manager.broadcast({
        "type": "task_update",
        "topic": "tasks",
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": task,
    })


async def broadcast_department_kpis(department: str, kpis: dict[str, Any]) -> None:
    """Push per-department KPI values to subscribed clients."""
    await manager.broadcast({
        "type": "department_kpi",
        "topic": f"department:{department}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "department": department,
        "payload": kpis,
    })


async def broadcast_escalation(escalation: dict[str, Any]) -> None:
    """Push an escalation event to all connected clients."""
    await manager.broadcast({
        "type": "escalation",
        "topic": "escalations",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": escalation,
    })


# ---------------------------------------------------------------------------
# Sync-to-async bridge for MessageBus callback integration
# ---------------------------------------------------------------------------

def make_message_bus_broadcast_callback() -> Any:
    """Create a synchronous broadcast callback suitable for MessageBus.

    The MessageBus ``broadcast_callback`` signature is
    ``(task_dict, event) -> None`` (sync).  This factory creates a closure
    that schedules the async WebSocket broadcast on the running event loop,
    making the integration seamless.

    Returns ``None`` gracefully if no event loop is running (e.g. CLI usage).
    """

    def _sync_callback(task_dict: dict[str, Any], event: str) -> None:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(broadcast_task_update(task_dict, event))
        except RuntimeError:
            # No running event loop — CLI or test context; skip.
            logger.debug("No event loop; WS broadcast skipped for event '%s'", event)

    return _sync_callback
