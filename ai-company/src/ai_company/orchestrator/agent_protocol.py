"""Agent communication protocol — pub/sub and request/response messaging.

Builds on top of the existing MessageBus to provide:
- Pub/sub: agents can subscribe to topics and receive broadcasts
- Request/response: agent-to-agent synchronous requests with timeout
- Shared context: collaborative task context for multi-agent work

Usage::

    protocol = AgentProtocol(bus=message_bus)

    # Subscribe to a topic
    protocol.subscribe("security.alerts", handler=handle_security_alert)

    # Publish an event
    protocol.publish("security.alerts", payload={"severity": "high", "cve": "..."})

    # Request/response between agents
    response = protocol.request(
        sender="chief-security",
        receiver="lead-backend",
        instruction="Review PR #123 for security issues",
        timeout_seconds=300,
    )
"""

from __future__ import annotations

import logging
import threading
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable

from ai_company.models.task import Task, TaskPriority

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Event types
# ---------------------------------------------------------------------------


@dataclass
class AgentEvent:
    """A pub/sub event published on a topic."""

    id: str
    topic: str
    sender: str
    payload: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    event_type: str = "message"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "sender": self.sender,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
        }


@dataclass
class RequestEnvelope:
    """A synchronous request from one agent to another."""

    request_id: str
    sender: str
    receiver: str
    instruction: str
    priority: str = "medium"
    timeout_seconds: int = 300
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ResponseEnvelope:
    """A response to a synchronous agent request."""

    request_id: str
    sender: str
    status: str  # "completed", "failed", "timeout"
    result: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# Type alias for event handlers
EventHandler = Callable[[AgentEvent], None]


# ---------------------------------------------------------------------------
# Agent communication protocol
# ---------------------------------------------------------------------------


class AgentProtocol:
    """High-level agent communication protocol built on MessageBus.

    Provides pub/sub messaging, request/response patterns, and
    shared context management for multi-agent collaboration.

    Args:
        bus: The underlying MessageBus for task-based communication.
        poll_interval: How often to poll for incoming requests (seconds).
    """

    def __init__(
        self,
        bus: Any = None,
        poll_interval: float = 1.0,
    ) -> None:
        self._bus = bus
        self._poll_interval = poll_interval

        # Pub/sub subscriptions: topic -> list of handlers
        self._subscriptions: dict[str, list[EventHandler]] = defaultdict(list)

        # Request/response tracking
        self._pending_requests: dict[str, RequestEnvelope] = {}
        self._responses: dict[str, ResponseEnvelope] = {}
        self._response_events: dict[str, threading.Event] = {}

        # Shared context store
        self._shared_contexts: dict[str, dict[str, Any]] = {}

        # Event log (in-memory, for debugging)
        self._event_log: list[AgentEvent] = []

        # Lock for thread safety
        self._lock = threading.Lock()

    # ── Pub/Sub ────────────────────────────────────────────────────

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        """Subscribe a handler function to a topic.

        When an event is published on this topic, all registered handlers
        will be called synchronously in registration order.
        """
        with self._lock:
            self._subscriptions[topic].append(handler)
        logger.debug("Handler subscribed to topic '%s'", topic)

    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        """Remove a handler from a topic."""
        with self._lock:
            handlers = self._subscriptions.get(topic, [])
            self._subscriptions[topic] = [h for h in handlers if h is not handler]

    def publish(
        self,
        topic: str,
        sender: str,
        payload: dict[str, Any] | None = None,
        event_type: str = "message",
    ) -> AgentEvent:
        """Publish an event to a topic.

        All registered handlers for the topic (and wildcard '*') will be
        notified. The event is also logged for audit purposes.
        """
        event = AgentEvent(
            id=str(uuid.uuid4()),
            topic=topic,
            sender=sender,
            payload=payload or {},
            event_type=event_type,
        )

        # Notify handlers (wildcard + specific topic)
        handlers = list(self._subscriptions.get(topic, []))
        handlers.extend(self._subscriptions.get("*", []))

        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:
                logger.error(
                    "Handler error on topic '%s': %s", topic, exc,
                    exc_info=True,
                )

        with self._lock:
            self._event_log.append(event)
            # Keep event log bounded
            if len(self._event_log) > 1000:
                self._event_log = self._event_log[-500:]

        logger.info("Published event on '%s' from %s", topic, sender)
        return event

    def get_event_log(
        self,
        topic: str | None = None,
        limit: int = 50,
    ) -> list[AgentEvent]:
        """Get recent events, optionally filtered by topic."""
        with self._lock:
            events = self._event_log
            if topic:
                events = [e for e in events if e.topic == topic]
            return events[-limit:]

    # ── Request / Response ─────────────────────────────────────────

    def request(
        self,
        sender: str,
        receiver: str,
        instruction: str,
        priority: str = "medium",
        timeout_seconds: int = 300,
        context: dict[str, Any] | None = None,
    ) -> ResponseEnvelope:
        """Send a synchronous request from one agent to another.

        Creates a task in the MessageBus and waits for a response via
        a polling mechanism. Blocks the calling thread until the response
        arrives or the timeout is reached.

        Args:
            sender: The requesting agent's ID.
            receiver: The target agent's ID.
            instruction: The task instruction.
            priority: Task priority.
            timeout_seconds: Maximum wait time.
            context: Optional shared context for the request.

        Returns:
            ``ResponseEnvelope`` with the result or a timeout error.
        """
        request_id = str(uuid.uuid4())

        envelope = RequestEnvelope(
            request_id=request_id,
            sender=sender,
            receiver=receiver,
            instruction=instruction,
            priority=priority,
            timeout_seconds=timeout_seconds,
            context=context or {},
        )

        with self._lock:
            self._pending_requests[request_id] = envelope
            event = threading.Event()
            self._response_events[request_id] = event

        # Create task in the MessageBus
        if self._bus is not None:
            try:
                task = Task(
                    id=request_id,
                    sender_id=sender,
                    receiver_id=receiver,
                    instruction=instruction,
                    priority=TaskPriority(priority),
                )
                self._bus.send_task(task)
            except Exception as exc:
                logger.error("Failed to send request task: %s", exc)
                return ResponseEnvelope(
                    request_id=request_id,
                    sender=sender,
                    status="failed",
                    result=f"Failed to send request: {exc}",
                )

        # Wait for response
        event.wait(timeout=timeout_seconds)

        with self._lock:
            response = self._responses.pop(request_id, None)
            self._pending_requests.pop(request_id, None)
            self._response_events.pop(request_id, None)

        if response is None:
            return ResponseEnvelope(
                request_id=request_id,
                sender=sender,
                status="timeout",
                result=f"Request to {receiver} timed out after {timeout_seconds}s",
            )

        return response

    def respond(
        self,
        request_id: str,
        sender: str,
        status: str,
        result: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Send a response to a pending request.

        Called by the receiving agent after completing the requested work.
        Signals the waiting thread to unblock.
        """
        response = ResponseEnvelope(
            request_id=request_id,
            sender=sender,
            status=status,
            result=result,
            metadata=metadata or {},
        )

        with self._lock:
            self._responses[request_id] = response
            event = self._response_events.get(request_id)
            if event:
                event.set()

        logger.info("Response sent for request %s from %s", request_id[:8], sender)

    def get_pending_requests(self, receiver: str | None = None) -> list[RequestEnvelope]:
        """Get pending requests, optionally filtered by receiver."""
        with self._lock:
            requests = list(self._pending_requests.values())
            if receiver:
                requests = [r for r in requests if r.receiver == receiver]
            return requests

    # ── Shared Context ─────────────────────────────────────────────

    def create_context(self, context_id: str, initial: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a shared context for collaborative tasks.

        Shared contexts allow multiple agents to read and update a
        shared state dictionary during multi-step tasks.
        """
        with self._lock:
            self._shared_contexts[context_id] = initial or {}
        logger.info("Created shared context: %s", context_id)
        return self._shared_contexts[context_id]

    def update_context(self, context_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        """Update a shared context with new values.

        Merges the updates into the existing context. Returns the
        updated context, or an empty dict if the context doesn't exist.
        """
        with self._lock:
            if context_id not in self._shared_contexts:
                logger.warning("Context %s not found — creating it", context_id)
                self._shared_contexts[context_id] = {}
            self._shared_contexts[context_id].update(updates)
            return dict(self._shared_contexts[context_id])

    def read_context(self, context_id: str) -> dict[str, Any]:
        """Read a shared context."""
        with self._lock:
            return dict(self._shared_contexts.get(context_id, {}))

    def delete_context(self, context_id: str) -> bool:
        """Delete a shared context."""
        with self._lock:
            if context_id in self._shared_contexts:
                del self._shared_contexts[context_id]
                logger.info("Deleted shared context: %s", context_id)
                return True
            return False

    def list_contexts(self) -> list[str]:
        """List all active shared context IDs."""
        with self._lock:
            return list(self._shared_contexts.keys())
