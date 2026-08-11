"""Tests for the agent communication protocol (pub/sub + request/response)."""

from __future__ import annotations

import threading
import time

from ai_company.orchestrator.agent_protocol import (
    AgentEvent,
    AgentProtocol,
    ResponseEnvelope,
)


def test_agent_event_to_dict() -> None:
    event = AgentEvent(
        id="evt-1",
        topic="security",
        sender="alice",
        payload={"severity": "high"},
        timestamp="2025-01-01T00:00:00",
        event_type="alert",
    )
    data = event.to_dict()
    assert data["id"] == "evt-1"
    assert data["topic"] == "security"
    assert data["sender"] == "alice"
    assert data["payload"] == {"severity": "high"}
    assert data["timestamp"] == "2025-01-01T00:00:00"
    assert data["event_type"] == "alert"


class TestPubSub:
    def test_subscribe_and_publish_notifies_handler(self) -> None:
        protocol = AgentProtocol()
        received: list[AgentEvent] = []

        def handler(event: AgentEvent) -> None:
            received.append(event)

        protocol.subscribe("alerts", handler)
        event = protocol.publish("alerts", sender="sensor", payload={"code": 1})
        assert len(received) == 1
        assert received[0] is event
        assert received[0].sender == "sensor"
        assert received[0].payload == {"code": 1}

    def test_publish_defaults_payload_and_event_type(self) -> None:
        protocol = AgentProtocol()
        event = protocol.publish("topic", sender="alice")
        assert event.payload == {}
        assert event.event_type == "message"

    def test_wildcard_subscription(self) -> None:
        protocol = AgentProtocol()
        received: list[AgentEvent] = []

        def handler(event: AgentEvent) -> None:
            received.append(event)

        protocol.subscribe("*", handler)
        protocol.publish("any.topic", sender="alice")
        assert len(received) == 1

    def test_unsubscribe_stops_notifications(self) -> None:
        protocol = AgentProtocol()
        received: list[AgentEvent] = []

        def handler(event: AgentEvent) -> None:
            received.append(event)

        protocol.subscribe("alerts", handler)
        protocol.unsubscribe("alerts", handler)
        protocol.publish("alerts", sender="sensor")
        assert received == []

    def test_handler_errors_do_not_break_publish(self) -> None:
        protocol = AgentProtocol()

        def bad_handler(event: AgentEvent) -> None:
            raise RuntimeError("boom")

        protocol.subscribe("alerts", bad_handler)
        event = protocol.publish("alerts", sender="sensor")
        assert event.topic == "alerts"

    def test_get_event_log_filters_by_topic(self) -> None:
        protocol = AgentProtocol()
        protocol.publish("alpha", sender="a")
        protocol.publish("beta", sender="b")
        protocol.publish("alpha", sender="a")
        alpha_events = protocol.get_event_log(topic="alpha")
        assert len(alpha_events) == 2
        assert all(e.topic == "alpha" for e in alpha_events)

    def test_get_event_log_limit(self) -> None:
        protocol = AgentProtocol()
        for _ in range(5):
            protocol.publish("t", sender="a")
        assert len(protocol.get_event_log(limit=2)) == 2


class TestRequestResponse:
    def test_request_respond_round_trip(self) -> None:
        protocol = AgentProtocol()

        def responder() -> None:
            deadline = time.time() + 5
            while time.time() < deadline:
                pending = protocol.get_pending_requests()
                if pending:
                    protocol.respond(
                        pending[0].request_id,
                        sender="bob",
                        status="completed",
                        result="all done",
                        metadata={"detail": "ok"},
                    )
                    return
                time.sleep(0.002)

        threading.Thread(target=responder, daemon=True).start()
        response = protocol.request(
            sender="alice",
            receiver="bob",
            instruction="review the PR",
            timeout_seconds=5,
        )
        assert isinstance(response, ResponseEnvelope)
        assert response.status == "completed"
        assert response.result == "all done"
        assert response.metadata == {"detail": "ok"}

    def test_request_times_out(self) -> None:
        protocol = AgentProtocol()
        response = protocol.request(
            sender="alice",
            receiver="bob",
            instruction="do nothing",
            timeout_seconds=0,
        )
        assert response.status == "timeout"
        assert "timed out" in response.result

    def test_request_returns_failed_when_bus_raises(self) -> None:
        class BrokenBus:
            def send_task(self, task) -> None:
                raise RuntimeError("bus down")

        protocol = AgentProtocol(bus=BrokenBus())
        response = protocol.request(
            sender="alice",
            receiver="bob",
            instruction="do the thing",
            timeout_seconds=0,
        )
        assert response.status == "failed"
        assert "bus down" in response.result

    def test_request_sends_task_to_bus(self, tmp_path) -> None:
        from ai_company.orchestrator.message_bus import MessageBus

        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        protocol = AgentProtocol(bus=bus)
        protocol.request(
            sender="alice",
            receiver="bob",
            instruction="persist me",
            timeout_seconds=0,
        )
        tasks = bus.get_all_tasks_raw()
        assert len(tasks) == 1
        assert tasks[0]["receiver_id"] == "bob"
        assert tasks[0]["instruction"] == "persist me"

    def test_get_pending_requests_filters_by_receiver(self) -> None:
        protocol = AgentProtocol()

        def responder() -> None:
            deadline = time.time() + 5
            while time.time() < deadline:
                pending = protocol.get_pending_requests()
                if pending:
                    for req in pending:
                        protocol.respond(
                            req.request_id, sender=req.receiver, status="completed", result="ok"
                        )
                    return
                time.sleep(0.002)

        threading.Thread(target=responder, daemon=True).start()
        protocol.request(sender="alice", receiver="bob", instruction="job 1", timeout_seconds=5)
        assert protocol.get_pending_requests(receiver="bob") == []
        assert protocol.get_pending_requests(receiver="nobody") == []


class TestSharedContext:
    def test_create_read_update_delete(self) -> None:
        protocol = AgentProtocol()
        ctx = protocol.create_context("task-1", {"status": "new"})
        assert ctx == {"status": "new"}
        assert protocol.read_context("task-1") == {"status": "new"}

        updated = protocol.update_context("task-1", {"status": "in_progress"})
        assert updated == {"status": "in_progress"} or updated["status"] == "in_progress"

        assert protocol.delete_context("task-1") is True
        assert protocol.read_context("task-1") == {}

    def test_update_context_creates_missing(self) -> None:
        protocol = AgentProtocol()
        updated = protocol.update_context("ghost", {"a": 1})
        assert updated == {"a": 1}

    def test_delete_missing_context_returns_false(self) -> None:
        protocol = AgentProtocol()
        assert protocol.delete_context("nope") is False

    def test_list_contexts(self) -> None:
        protocol = AgentProtocol()
        protocol.create_context("one")
        protocol.create_context("two")
        assert set(protocol.list_contexts()) == {"one", "two"}
