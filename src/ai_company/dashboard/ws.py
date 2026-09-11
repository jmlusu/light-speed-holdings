"""WebSocket handler for live dashboard updates."""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import time
from collections import deque
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from ai_company.security.rbac import require_ws_role

logger = logging.getLogger(__name__)

router = APIRouter()

# ── WebSocket hardening knobs (env-configurable, read at point of use) ──


def _max_ws_clients() -> int:
    """Max concurrent WebSocket connections (connection-DoS guard)."""
    return int(os.environ.get("DASHBOARD_MAX_WS_CLIENTS", "200"))


def _max_ws_message_bytes() -> int:
    """Max inbound message size in bytes (memory-DoS guard)."""
    return int(os.environ.get("DASHBOARD_WS_MAX_MESSAGE_BYTES", "65536"))


def _ws_rate_limit() -> tuple[int, float]:
    """(max messages, window seconds) per connection for inbound messages."""
    return (
        int(os.environ.get("DASHBOARD_WS_RATE_LIMIT_MESSAGES", "60")),
        float(os.environ.get("DASHBOARD_WS_RATE_LIMIT_WINDOW_S", "10")),
    )


def _max_ws_idle_seconds() -> float:
    """Max seconds a connection may stay silent before it is reaped (C2).

    Healthy dashboard tabs send an application-level ``ping`` every ~30s
    (``static/js/app.js``), so this timeout only catches half-open or dead
    connections that never close cleanly (e.g. silent network drop, crashed
    tab).  0 disables the idle sweep.
    """
    return float(os.environ.get("DASHBOARD_WS_IDLE_TIMEOUT_S", "600"))


def _ws_sweep_interval() -> float:
    """Seconds between idle-sweep passes over all WebSocket connections.

    The default is a sub-multiple of ``DASHBOARD_WS_HEARTBEAT_INTERVAL_S`` so
    the server heartbeat probe and its pong deadline land within 1-2 passes.
    """
    return float(os.environ.get("DASHBOARD_WS_SWEEP_INTERVAL_S", "15"))


def _ws_heartbeat_interval() -> float:
    """Max silent seconds before the server probes a connection (C2).

    A connection idle for longer than this receives an application-level
    ``{"type": "ping", "source": "server"}`` probe.  ``0`` disables probing.
    """
    return float(os.environ.get("DASHBOARD_WS_HEARTBEAT_INTERVAL_S", "300"))


def _ws_pong_timeout() -> float:
    """Max seconds a probed connection may stay silent before reaping (C2).

    If no inbound message arrives within this window after a server probe was
    sent, the connection is treated as half-open and closed with code ``1008``.
    ``0`` disables probe-based reaping.
    """
    return float(os.environ.get("DASHBOARD_WS_PONG_TIMEOUT_S", "120"))


# ── Topic authorization ────────────────────────────────────────────────

#: Canonical topics exposed by the broadcast helpers.  Clients may only
#: subscribe to these (plus the ``department:<name>`` family and the
#: ``*`` wildcard), preventing subscription to sensitive/unknown channels.
_TOPIC_ALLOWLIST: frozenset[str] = frozenset(
    {
        "kpis",
        "alerts",
        "tasks",
        "escalations",
        "workflows",
        "onboarding",
        "org_health",
        "daemon",
        "timeline",
        "*",
    }
)


def _is_valid_topic(topic: Any) -> bool:
    """True if *topic* is a subscribable channel name."""
    if isinstance(topic, str) and topic in _TOPIC_ALLOWLIST:
        return True
    return isinstance(topic, str) and topic.startswith("department:")


def _valid_topics(topics: list[Any]) -> list[str]:
    """Return only the strings in *topics* that pass the allowlist."""
    return [t for t in topics if _is_valid_topic(t)]


class ConnectionManager:
    """Tracks active WebSocket clients and handles broadcast.

    In addition to connection/subscription bookkeeping, the manager runs an
    idle-sweep background task (C2): connections that stay silent longer than
    ``DASHBOARD_WS_IDLE_TIMEOUT_S`` are closed with code ``1008`` so dead or
    half-open sockets cannot occupy the connection cap forever.  The same
    sweep sends a server-initiated heartbeat probe (``{"type": "ping",
    "source": "server"}``) to connections silent for more than
    ``DASHBOARD_WS_HEARTBEAT_INTERVAL_S``, and reaps connections that stay
    silent for more than ``DASHBOARD_WS_PONG_TIMEOUT_S`` after a probe.
    """

    def __init__(self) -> None:
        self._connections: list[WebSocket] = []
        self._subscriptions: dict[int, set[str]] = {}  # ws_id → set of topics
        self._inbound_timestamps: dict[int, deque[float]] = {}
        self._last_seen: dict[int, float] = {}  # ws_id → monotonic last-activity
        self._probe_sent_at: dict[int, float] = {}  # ws_id → last server ping
        self._probes_sent = 0
        self._lock = asyncio.Lock()
        self._sweep_task: asyncio.Task[None] | None = None
        self._sweeps_run = 0
        self._last_sweep_at = 0.0

    @property
    def active_count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> bool:
        """Accept *websocket* if under the connection cap.

        Returns ``True`` when accepted, ``False`` when rejected (cap hit).
        """
        async with self._lock:
            if self.active_count >= _max_ws_clients():
                await websocket.close(code=1013, reason="Too many connections")
                return False
            await websocket.accept()
            self._connections.append(websocket)
            self._subscriptions[id(websocket)] = set()
            self._last_seen[id(websocket)] = time.monotonic()
        self._ensure_sweep_task()
        logger.info("WebSocket client connected (%d active)", self.active_count)
        return True

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            if websocket in self._connections:
                self._connections.remove(websocket)
            self._subscriptions.pop(id(websocket), None)
            self._inbound_timestamps.pop(id(websocket), None)
            self._last_seen.pop(id(websocket), None)
            self._probe_sent_at.pop(id(websocket), None)
            if not self._connections:
                self._stop_sweeper()
        logger.info("WebSocket client disconnected (%d active)", self.active_count)

    async def subscribe(self, websocket: WebSocket, topics: list[str]) -> None:
        """Register topic subscriptions for a client."""
        async with self._lock:
            ws_id = id(websocket)
            if ws_id in self._subscriptions:
                self._subscriptions[ws_id].update(topics)
        logger.debug("Client subscribed to topics: %s", topics)

    async def unsubscribe(self, websocket: WebSocket, topics: list[str]) -> None:
        """Remove topic subscriptions for a client."""
        async with self._lock:
            ws_id = id(websocket)
            if ws_id in self._subscriptions:
                self._subscriptions[ws_id] -= set(topics)
        logger.debug("Client unsubscribed from topics: %s", topics)

    def _check_rate_limit(self, ws_id: int) -> bool:
        """Enforce per-connection inbound message rate limit (sliding window).

        Returns ``False`` when the connection is over its quota.
        """
        limit, window = _ws_rate_limit()
        now = time.monotonic()
        # Any inbound message counts as activity for the idle sweep and clears
        # any outstanding server heartbeat probe (pong-equivalent).
        self._last_seen[ws_id] = now
        self._probe_sent_at.pop(ws_id, None)
        if limit <= 0:
            return True
        q = self._inbound_timestamps.get(ws_id)
        if q is None:
            q = deque()
            self._inbound_timestamps[ws_id] = q
        while q and now - q[0] > window:
            q.popleft()
        if len(q) >= limit:
            return False
        q.append(now)
        return True

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
            except Exception:  # noqa: BLE001 - connection may drop at any time
                logger.warning("Failed to send to client, marking for removal")
                failed.append(ws)

        # Prune dead connections outside the iteration
        if failed:
            async with self._lock:
                for ws in failed:
                    if ws in self._connections:
                        self._connections.remove(ws)
                    self._subscriptions.pop(id(ws), None)
                    self._last_seen.pop(id(ws), None)
                    self._probe_sent_at.pop(id(ws), None)

        return [str(id(f)) for f in failed]

    # ------------------------------------------------------------------
    # Idle-sweep / liveness (C2)
    # ------------------------------------------------------------------

    def _ensure_sweep_task(self) -> None:
        """Start the background idle-sweep task once, if not already running."""
        if self._sweep_task is not None and not self._sweep_task.done():
            return
        try:
            self._sweep_task = asyncio.get_running_loop().create_task(self._sweep_loop())
        except RuntimeError:
            # No running event loop — CLI/test context; skip.
            logger.debug("No event loop; WS idle sweep skipped")

    def _stop_sweeper(self) -> None:
        """Cancel the background idle-sweep task (last connection dropped)."""
        task = self._sweep_task
        if task is not None and not task.done():
            task.cancel()
        self._sweep_task = None

    async def _sweep_loop(self) -> None:
        """Periodically reap silent connections until none remain."""
        while True:
            try:
                await asyncio.sleep(_ws_sweep_interval())
                await self._idle_sweep_once()
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001 - sweep must never kill the hub
                logger.exception("WebSocket idle sweep error")
            if not self._connections:
                return

    async def _idle_sweep_once(
        self,
        max_idle_s: float | None = None,
        now: float | None = None,
    ) -> list[WebSocket]:
        """Close and remove every connection silent for > *max_idle_s* seconds.

        Returns the reaped connections.  ``max_idle_s`` defaults to the
        ``DASHBOARD_WS_IDLE_TIMEOUT_S`` knob; ``<= 0`` disables the hard idle
        sweep.

        The same pass also runs the server-initiated heartbeat (C2):
        connections silent for longer than ``DASHBOARD_WS_HEARTBEAT_INTERVAL_S``
        receive an application-level ``{"type": "ping", "source": "server"}``
        probe, and connections that stay silent for more than
        ``DASHBOARD_WS_PONG_TIMEOUT_S`` after a probe was sent are reaped with
        code ``1008``.  Any inbound message clears the pending probe, so a probe
        is only ever conclusive for clients that stopped talking (half-open
        sockets, crashed tabs, sliced network links).
        """
        limit = _max_ws_idle_seconds() if max_idle_s is None else max_idle_s
        if limit <= 0:
            return []
        now = time.monotonic() if now is None else now
        hb_interval = _ws_heartbeat_interval()
        pong_timeout = _ws_pong_timeout()
        async with self._lock:
            stale: list[tuple[WebSocket, str]] = []
            for ws in self._connections:
                ws_id = id(ws)
                idle = now - self._last_seen.get(ws_id, now)
                if idle > limit:
                    stale.append((ws, "Idle timeout"))
                    continue
                if hb_interval <= 0 or pong_timeout <= 0:
                    continue
                probe_at = self._probe_sent_at.get(ws_id)
                if probe_at is not None:
                    if now - probe_at > pong_timeout:
                        stale.append((ws, "No heartbeat response"))
                elif idle > hb_interval:
                    payload = json.dumps({"type": "ping", "source": "server"})
                    try:
                        await ws.send_text(payload)
                        self._probe_sent_at[ws_id] = now
                        self._probes_sent += 1
                    except Exception:  # noqa: BLE001 - socket may be gone
                        stale.append((ws, "Heartbeat send failed"))
            for ws, reason in stale:
                with contextlib.suppress(Exception):  # noqa: BLE001 - socket may be gone
                    await ws.close(code=1008, reason=reason)
            for ws, _reason in stale:
                if ws in self._connections:
                    self._connections.remove(ws)
                self._subscriptions.pop(id(ws), None)
                self._inbound_timestamps.pop(id(ws), None)
                self._last_seen.pop(id(ws), None)
                self._probe_sent_at.pop(id(ws), None)
            self._sweeps_run += 1
            self._last_sweep_at = now
        if stale:
            logger.info("WS idle sweep closed %d connection(s)", len(stale))
        return [ws for ws, _reason in stale]

    def stats(self) -> dict[str, Any]:
        """Snapshot of connection health for observability/health endpoints."""
        topic_counts: dict[str, int] = {}
        for subs in self._subscriptions.values():
            for topic in subs:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        return {
            "active_clients": self.active_count,
            "connection_cap": _max_ws_clients(),
            "idle_timeout_s": _max_ws_idle_seconds(),
            "sweep_interval_s": _ws_sweep_interval(),
            "heartbeat_interval_s": _ws_heartbeat_interval(),
            "pong_timeout_s": _ws_pong_timeout(),
            "probes_sent": self._probes_sent,
            "probes_outstanding": len(self._probe_sent_at),
            "sweeps_run": self._sweeps_run,
            "last_sweep_at": self._last_sweep_at,
            "subscribed_topics": topic_counts,
        }


# Module-level singleton — importable by other modules for broadcast
manager = ConnectionManager()


# ── WebSocket endpoint ──────────────────────────────────────────────


def _origin_allowed(websocket: WebSocket) -> bool:
    """Reject cross-site WebSocket handshakes (CSWSH defense).

    A WebSocket request is allowed when it carries no ``Origin`` header
    (non-browser client, e.g. CLI or the test client), when the origin is
    same-host as the ``Host`` header, or when the origin appears in the
    app's CORS allowlist (``app.state.allowed_ws_origins``).
    """
    origin = websocket.headers.get("origin")
    if not origin:
        return True
    try:
        origin_host = urlsplit(origin).hostname
    except ValueError:
        return False
    if not origin_host:
        return False

    host = websocket.headers.get("host", "")
    if host:
        host_name = host.split(":")[0]
        if origin_host.lower() == host_name.lower():
            return True

    allowed: set[str] = set()
    app = getattr(websocket, "app", None)
    if app is not None:
        allowed = getattr(app.state, "allowed_ws_origins", set()) or set()
    return origin in allowed


@router.websocket("/ws/v1/dashboard")
async def dashboard_websocket(websocket: WebSocket) -> None:
    """Single WebSocket endpoint for live dashboard updates.

    Protocol:
      - Server sends JSON messages (KPI snapshots, alerts, etc.)
      - Client may send ``{"type": "ping"}`` for application-level keepalive;
        server replies with ``{"type": "pong", ...}``.
      - Server-initiated heartbeat (C2): connections idle longer than
        ``DASHBOARD_WS_HEARTBEAT_INTERVAL_S`` are probed with
        ``{"type": "ping", "source": "server"}``; clients reply with
        ``{"type": "pong"}``.  Connections that stay silent past
        ``DASHBOARD_WS_PONG_TIMEOUT_S`` after a probe are closed with code
        ``1008``.

    Security (T018 / ticket #11):
      - Cross-site WebSocket hijacking is prevented by an origin check
        before the handshake is accepted: the ``Origin`` header must match
        the request host (same-origin) or be in the app's CORS allowlist
        (``app.state.allowed_ws_origins``).  Non-browser clients that send
        no ``Origin`` header are allowed.
      - Role gate (ADR-012): in ``api_key`` auth mode the handshake must
        carry ``?api_key=`` resolving to at least the ``run`` role, else
        the connection is closed with code ``1008``.  In ``open`` mode
        (loopback-only) the role resolves to ``admin`` and no key is needed.
      - Hardening (GAP): connection cap, bounded inbound message size,
        per-connection rate limiting, a channel/topic allowlist, and an
        idle-sweep + server heartbeat probe (C2) that reaps silent and
        half-open sockets after ``DASHBOARD_WS_IDLE_TIMEOUT_S`` (default
        600s) or a missed probe window (``DASHBOARD_WS_PONG_TIMEOUT_S``,
        default 120s) so they cannot occupy the cap forever.
    """
    if not _origin_allowed(websocket):
        await websocket.close(code=1008, reason="Origin not allowed")
        return
    try:
        client_ip = websocket.client.host if websocket.client else "unknown"
        require_ws_role("run", websocket.query_params.get("api_key"), client_ip)
    except HTTPException:
        await websocket.close(code=1008, reason="Invalid or insufficient API key")
        return
    if not await manager.connect(websocket):
        return
    try:
        # Send an initial hello so the client knows the connection is live
        await websocket.send_json(
            {
                "type": "connected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "active_clients": manager.active_count,
            }
        )

        while True:
            try:
                data = await _receive_bounded(websocket)
            except OSError as exc:
                detail = str(exc)
                logger.warning("Rejecting WS message: %s", detail)
                with contextlib.suppress(Exception):  # noqa: BLE001 - socket may be gone
                    await websocket.send_json({"type": "error", "detail": detail})
                await websocket.close(code=1009, reason=detail[:120])
                break

            if not isinstance(data, dict):
                await websocket.send_json(
                    {"type": "error", "detail": "Message must be a JSON object"}
                )
                continue

            if not manager._check_rate_limit(id(websocket)):
                logger.warning("WebSocket client exceeded inbound rate limit")
                await websocket.send_json({"type": "error", "detail": "Rate limit exceeded"})
                await websocket.close(code=1008, reason="Rate limit exceeded")
                break

            msg_type = data.get("type", "")

            if msg_type == "ping":
                await websocket.send_json(
                    {
                        "type": "pong",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
            elif msg_type == "pong":
                # Reply to a server-initiated heartbeat probe.  ``_check_rate_limit``
                # above already counted it as activity, so there is nothing to do.
                pass
            elif msg_type == "subscribe":
                topics = data.get("topics", [])
                if not isinstance(topics, list):
                    await websocket.send_json({"type": "error", "detail": "topics must be a list"})
                    continue
                # Channel authorization: stick to the allowlist.
                requested: list[str] = [t for t in topics if isinstance(t, str)]
                valid = _valid_topics(requested)
                invalid = [t for t in requested if t not in valid]
                if valid:
                    await manager.subscribe(websocket, valid)
                await websocket.send_json(
                    {
                        "type": "subscribed",
                        "topics": valid,
                        "invalid": invalid,
                        "detail": "Some requested topics were not allowed" if invalid else None,
                    }
                )
            elif msg_type == "unsubscribe":
                topics = data.get("topics", [])
                if not isinstance(topics, list):
                    await websocket.send_json({"type": "error", "detail": "topics must be a list"})
                    continue
                topics_to_remove: list[str] = [t for t in topics if isinstance(t, str)]
                await manager.unsubscribe(websocket, topics_to_remove)
                await websocket.send_json(
                    {
                        "type": "unsubscribed",
                        "topics": topics_to_remove,
                    }
                )
            else:
                await websocket.send_json(
                    {
                        "type": "error",
                        "detail": f"Unknown message type: {msg_type}",
                    }
                )

    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("WebSocket error")
    finally:
        await manager.disconnect(websocket)


async def _receive_bounded(websocket: WebSocket) -> dict[str, Any] | None:
    """Receive and parse one inbound JSON message with a size cap.

    Returns the parsed message dict, or ``None`` when the peer disconnects.

    Raises
    ------
    OSError
        When the message exceeds ``DASHBOARD_WS_MAX_MESSAGE_BYTES`` or is not
        valid JSON (callers must close the socket in this case).
    """
    raw = await websocket.receive()
    if "type" in raw and raw["type"] == "websocket.disconnect":
        raise WebSocketDisconnect(raw.get("code", 1000))

    if "text" in raw and raw["text"] is not None:
        text = raw["text"]
    elif "bytes" in raw and raw["bytes"] is not None:
        text = raw["bytes"].decode("utf-8", errors="replace")
    else:
        raise OSError("Unsupported websocket message")

    if len(text) > _max_ws_message_bytes():
        raise OSError("Message too large")

    try:
        parsed = json.loads(text)
    except ValueError as exc:
        raise OSError("Malformed JSON") from exc
    return parsed if isinstance(parsed, dict) else None


# ── Public broadcast helpers ────────────────────────────────────────


async def _broadcast_event(
    message_type: str,
    topic: str,
    payload: dict[str, Any],
    *,
    data_key: str = "payload",
    extra: dict[str, Any] | None = None,
) -> None:
    """Compose and broadcast a typed WebSocket message.

    The common wire shape is ``{"type", "topic", "timestamp", **extra,
    <data_key>: payload}``.  ``extra`` supplies per-kind fields (e.g.
    ``event``, ``instance_id``, ``department``) while ``data_key`` selects
    whether the body lives under ``payload`` or another key (e.g. ``data``
    for timeline events).  Every broadcast wrapper routes through this one
    builder + :func:`ConnectionManager.broadcast`, so the timestamp and
    dispatch logic live in a single place.
    """
    message: dict[str, Any] = {
        "type": message_type,
        "topic": topic,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        message.update(extra)
    message[data_key] = payload
    await manager.broadcast(message)


async def broadcast_kpi_update(data: dict[str, Any]) -> None:
    """Push a KPI update to all connected dashboard clients."""
    await _broadcast_event("kpi_update", "kpis", data)


async def broadcast_alert(alert: dict[str, Any]) -> None:
    """Push an alert / notification to all connected clients."""
    await _broadcast_event("alert", "alerts", alert)


async def broadcast_task_update(task: dict[str, Any], event: str = "created") -> None:
    """Push a task lifecycle event to all connected clients.

    Parameters
    ----------
    task:
        The task dict (must be JSON-serialisable).
    event:
        One of ``"created"``, ``"completed"``, ``"failed"``, ``"escalated"``.
    """
    await _broadcast_event("task_update", "tasks", task, extra={"event": event})


async def broadcast_department_kpis(department: str, kpis: dict[str, Any]) -> None:
    """Push per-department KPI values to subscribed clients."""
    await _broadcast_event(
        "department_kpi",
        f"department:{department}",
        kpis,
        extra={"department": department},
    )


async def broadcast_escalation(escalation: dict[str, Any]) -> None:
    """Push an escalation event to all connected clients."""
    await _broadcast_event("escalation", "escalations", escalation)


# ---------------------------------------------------------------------------
# Sync-to-async bridge for MessageBus callback integration
# ---------------------------------------------------------------------------


async def broadcast_workflow_update(instance_id: str, event: str, payload: dict[str, Any]) -> None:
    """Push a workflow lifecycle event to subscribed dashboard clients.

    Clients subscribe to the ``"workflows"`` topic to receive these.
    """
    await _broadcast_event(
        "workflow_update",
        "workflows",
        payload,
        extra={"event": event, "instance_id": instance_id},
    )


async def broadcast_onboarding_update(request_id: str, event: str, payload: dict[str, Any]) -> None:
    """Push an onboarding lifecycle event to subscribed dashboard clients.

    Clients subscribe to the ``"onboarding"`` topic to receive these.
    Events: requested, approved, rejected, expired, step_completed.
    """
    await _broadcast_event(
        "onboarding_update",
        "onboarding",
        payload,
        extra={"event": event, "request_id": request_id},
    )


async def broadcast_org_health(data: dict[str, Any]) -> None:
    """Push an org-health score update to all connected dashboard clients.

    Clients subscribe to the ``"org_health"`` topic to receive these.
    """
    await _broadcast_event("org_health_update", "org_health", data)


async def broadcast_daemon_health(data: dict[str, Any]) -> None:
    """Push executor daemon health status to all connected dashboard clients.

    Clients subscribe to the ``"daemon"`` topic to receive these.  The
    payload mirrors the ``/api/v1/daemon/status`` response shape.
    """
    await _broadcast_event("daemon_health", "daemon", data)


async def broadcast_timeline_event(event: dict[str, Any]) -> None:
    """Push new audit events to timeline subscribers."""
    await _broadcast_event("timeline_event", "timeline", event, data_key="data")


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
