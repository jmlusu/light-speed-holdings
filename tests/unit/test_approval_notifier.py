"""Unit tests for ApprovalNotifier — WebSocket + webhook notifications.

Verifies:
- notify_parked() fires WebSocket broadcast and webhook
- notify_resolved() fires resolution broadcast
- Webhook signing with HMAC-SHA256
- Webhook event filtering
- Best-effort: failures never propagate
"""

from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_company.orchestrator.notifier import ApprovalNotifier


@pytest.fixture
def notifier(tmp_path: Path) -> ApprovalNotifier:
    """Create an ApprovalNotifier with a test webhook config."""
    config_path = tmp_path / "webhooks.yaml"
    config_path.write_text(
        "webhooks:\n"
        "  - url: 'https://example.com/hook'\n"
        "    secret: 'test-secret'\n"
        "    events: ['parked', 'resolved']\n"
        "  - url: 'https://example.com/parked-only'\n"
        "    secret: ''\n"
        "    events: ['parked']\n"
    )
    return ApprovalNotifier(config_path=str(config_path))


@pytest.fixture
def empty_notifier(tmp_path: Path) -> ApprovalNotifier:
    """Notifier with no webhooks configured."""
    config_path = tmp_path / "empty.yaml"
    config_path.write_text("webhooks: []\n")
    return ApprovalNotifier(config_path=str(config_path))


@pytest.fixture
def no_config_notifier(tmp_path: Path) -> ApprovalNotifier:
    """Notifier with a non-existent config file."""
    return ApprovalNotifier(config_path=str(tmp_path / "nonexistent.yaml"))


# ── notify_parked ───────────────────────────────────────────────


def test_notify_parked_fires_webhook(notifier: ApprovalNotifier) -> None:
    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        notifier.notify_parked(
            request_id="hitl-abc",
            task_id="task-1",
            agent_id="agent-1",
            tool="bash",
            description="Execute: rm -rf /",
            tier=4,
        )

        # Should have been called for both webhooks (parked event matches both)
        assert mock_urlopen.call_count == 2


def test_notify_parked_ws_broadcast(notifier: ApprovalNotifier) -> None:
    with (
        patch("ai_company.orchestrator.notifier.urlopen"),
        patch("asyncio.get_running_loop") as mock_loop,
    ):
        mock_loop.return_value.create_task = MagicMock()
        notifier.notify_parked(
            request_id="hitl-abc",
            task_id="task-1",
            agent_id="agent-1",
            tool="bash",
            description="test",
            tier=2,
        )
        # WS broadcast should have been attempted
        mock_loop.return_value.create_task.assert_called()


def test_notify_parked_no_webhooks(empty_notifier: ApprovalNotifier) -> None:
    """No crash when no webhooks are configured."""
    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        empty_notifier.notify_parked(
            request_id="hitl-abc",
            task_id="task-1",
            agent_id="agent-1",
            tool="bash",
            description="test",
        )
        mock_urlopen.assert_not_called()


def test_notify_parked_no_config(no_config_notifier: ApprovalNotifier) -> None:
    """No crash when config file doesn't exist."""
    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        no_config_notifier.notify_parked(
            request_id="hitl-abc",
            task_id="task-1",
            agent_id="agent-1",
            tool="bash",
            description="test",
        )
        mock_urlopen.assert_not_called()


# ── notify_resolved ─────────────────────────────────────────────


def test_notify_resolved_fires_webhook(notifier: ApprovalNotifier) -> None:
    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        notifier.notify_resolved(
            request_id="hitl-abc",
            task_id="task-1",
            decision="approved",
        )

        # Only the first webhook has "resolved" in events
        assert mock_urlopen.call_count == 1


def test_notify_resolved_filters_parked_only_webhook(
    notifier: ApprovalNotifier,
) -> None:
    """The 'parked-only' webhook should NOT receive resolved events."""
    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        notifier.notify_resolved(
            request_id="hitl-abc",
            task_id="task-1",
            decision="rejected",
        )

        # Only 1 webhook (the one with events: ['parked', 'resolved'])
        assert mock_urlopen.call_count == 1
        url = mock_urlopen.call_args[0][0].full_url
        assert "example.com/hook" in url


# ── Webhook signing ────────────────────────────────────────────


def test_webhook_signature_header() -> None:
    """HMAC-SHA256 signature should be included when secret is set."""
    payload = {"event": "parked", "task_id": "task-1"}
    body = json.dumps(payload).encode("utf-8")
    secret = "my-secret"

    expected_sig = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        notifier = ApprovalNotifier.__new__(ApprovalNotifier)
        notifier._config_path = ""
        notifier._webhooks = None

        notifier._post_webhook("https://example.com/hook", payload, secret)

        req = mock_urlopen.call_args[0][0]
        assert req.get_header("X-webhook-signature") == f"sha256={expected_sig}"


def test_webhook_no_signature_without_secret() -> None:
    """No signature header when secret is empty."""
    payload = {"event": "parked"}

    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        notifier = ApprovalNotifier.__new__(ApprovalNotifier)
        notifier._config_path = ""
        notifier._webhooks = None

        notifier._post_webhook("https://example.com/hook", payload, "")

        req = mock_urlopen.call_args[0][0]
        assert req.get_header("X-webhook-signature") is None


# ── Best-effort / error handling ───────────────────────────────


def test_webhook_failure_does_not_propagate(notifier: ApprovalNotifier) -> None:
    """A failing webhook should log a warning, not raise."""
    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = ConnectionError("refused")

        # Should not raise
        notifier.notify_parked(
            request_id="hitl-abc",
            task_id="task-1",
            agent_id="agent-1",
            tool="bash",
            description="test",
        )


def test_ws_failure_does_not_propagate() -> None:
    """A failing WS broadcast should not raise."""
    notifier = ApprovalNotifier.__new__(ApprovalNotifier)
    notifier._config_path = ""
    notifier._webhooks = None

    with patch("asyncio.get_running_loop") as mock_loop:
        mock_loop.side_effect = RuntimeError("no loop")
        # Should not raise (CLI context, no event loop)
        notifier._broadcast_ws({"event": "test"})


# ── Payload shape ──────────────────────────────────────────────


def test_parked_payload_shape(tmp_path: Path) -> None:
    """Verify the webhook payload has all expected fields."""
    config_path = tmp_path / "webhooks.yaml"
    config_path.write_text(
        "webhooks:\n  - url: 'https://example.com/hook'\n    secret: ''\n    events: ['all']\n"
    )
    notifier = ApprovalNotifier(config_path=str(config_path))

    with patch("ai_company.orchestrator.notifier.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        notifier.notify_parked(
            request_id="hitl-123",
            task_id="task-abc",
            agent_id="cto",
            tool="bash",
            description="Execute: terraform apply",
            tier=3,
        )

        req = mock_urlopen.call_args[0][0]
        body = json.loads(req.data.decode("utf-8"))
        assert body["event"] == "parked"
        assert body["request_id"] == "hitl-123"
        assert body["task_id"] == "task-abc"
        assert body["agent_id"] == "cto"
        assert body["tool"] == "bash"
        assert body["tier"] == 3
        assert "timestamp" in body
