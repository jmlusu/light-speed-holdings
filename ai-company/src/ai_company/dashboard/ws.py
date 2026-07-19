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
        self._lock = asyncio.Lock()

    @property
    def active_count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.append(websocket)
        logger.info("WebSocket client connected (%d active)", self.active_count)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            if websocket in self._connections:
                self._connections.remove(websocket)
        logger.info("WebSocket client disconnected (%d active)", self.active_count)

    async def broadcast(self, message: dict[str, Any]) -> list[str]:
        """Send *message* to every connected client.

        Returns a list of client IDs that failed so the caller can decide
        whether to prune them.
        """
        payload = json.dumps(message, default=str)
        failed: list[WebSocket] = []

        async with self._lock:
            snapshot = list(self._connections)

        for ws in snapshot:
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
                # Future: topic-based subscriptions
                await websocket.send_json({
                    "type": "subscribed",
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": data,
    })


async def broadcast_alert(alert: dict[str, Any]) -> None:
    """Push an alert / notification to all connected clients."""
    await manager.broadcast({
        "type": "alert",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": alert,
    })
