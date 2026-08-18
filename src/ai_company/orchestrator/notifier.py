"""Outbound notification surface for HITL approval requests.

When the executor parks a task in ``WAITING_APPROVAL`` the notifier fires
a WebSocket broadcast (immediate, dashboard clients) and an optional
HTTP webhook POST (configurable, external systems like Slack or email).

Webhook config lives in ``company/config/webhooks.yaml``.  The notifier
is fire-and-forget: delivery failures are logged but never block the
executor.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG = "company/config/webhooks.yaml"


class ApprovalNotifier:
    """Push notification surface for HITL approval events.

    Args:
        config_path: Path to webhook configuration YAML.
    """

    def __init__(self, config_path: str = _DEFAULT_CONFIG) -> None:
        self._config_path = config_path
        self._webhooks: list[dict[str, Any]] | None = None

    def _load_webhooks(self) -> list[dict[str, Any]]:
        """Load webhook config from disk (cached, reload on each call)."""
        try:
            path = Path(self._config_path)
            if not path.exists():
                return []
            parent = str(path.parent)
            store = FileStore(parent, backup=False)
            data = store.read_yaml(path.name)
            if isinstance(data, dict):
                wh_list = data.get("webhooks", [])
                if isinstance(wh_list, list):
                    return wh_list
        except Exception:  # noqa: BLE001 - config load must never crash
            logger.debug("Failed to load webhook config from %s", self._config_path)
        return []

    def notify_parked(
        self,
        request_id: str,
        task_id: str,
        agent_id: str,
        tool: str,
        description: str,
        tier: int = 2,
    ) -> None:
        """Fire WebSocket broadcast + webhook for a newly parked task.

        Best-effort: exceptions are logged, never propagated.
        """
        payload = {
            "event": "parked",
            "request_id": request_id,
            "task_id": task_id,
            "agent_id": agent_id,
            "tool": tool,
            "description": description,
            "tier": tier,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._broadcast_ws(payload)
        self._fire_webhooks(payload, event_filter="parked")

    def notify_resolved(
        self,
        request_id: str,
        task_id: str,
        decision: str,
    ) -> None:
        """Fire WebSocket broadcast + webhook for a resolved approval.

        Best-effort: exceptions are logged, never propagated.
        """
        payload = {
            "event": "resolved",
            "request_id": request_id,
            "task_id": task_id,
            "decision": decision,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._broadcast_ws(payload)
        self._fire_webhooks(payload, event_filter="resolved")

    def _broadcast_ws(self, payload: dict[str, Any]) -> None:
        """Schedule a WebSocket broadcast via the sync→async bridge."""
        try:
            import asyncio

            from ai_company.dashboard.ws import broadcast_alert

            loop = asyncio.get_running_loop()
            loop.create_task(broadcast_alert({"category": "approval", **payload}))
        except RuntimeError:
            # No running event loop — CLI or test context; skip.
            logger.debug("No event loop; WS broadcast skipped for approval event")
        except Exception:  # noqa: BLE001 - broadcast must never crash
            logger.debug("WebSocket broadcast failed for approval event", exc_info=True)

    def _fire_webhooks(self, payload: dict[str, Any], event_filter: str = "all") -> None:
        """POST to configured webhook URLs (fire-and-forget)."""
        webhooks = self._load_webhooks()
        if not webhooks:
            return

        for wh in webhooks:
            url = wh.get("url", "")
            if not url:
                continue
            secret = wh.get("secret", "")
            events = wh.get("events", ["all"])
            if event_filter not in events and "all" not in events:
                continue

            try:
                self._post_webhook(url, payload, secret)
            except Exception:  # noqa: BLE001 - webhook failure is best-effort
                logger.warning(
                    "Webhook delivery failed: url=%s event=%s",
                    url,
                    payload.get("event"),
                    exc_info=True,
                )

    @staticmethod
    def _post_webhook(url: str, payload: dict[str, Any], secret: str = "") -> None:
        """Synchronous HTTP POST to a webhook URL.

        Signs the payload with HMAC-SHA256 when a secret is configured.
        Sets a 5-second timeout so a slow endpoint never blocks the executor.
        """
        body = json.dumps(payload, default=str).encode("utf-8")
        headers: dict[str, str] = {"Content-Type": "application/json"}

        if secret:
            sig = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
            headers["X-Webhook-Signature"] = f"sha256={sig}"

        req = Request(url, data=body, headers=headers, method="POST")  # noqa: S310
        with urlopen(req, timeout=5) as resp:  # noqa: S310
            logger.info(
                "Webhook delivered: url=%s status=%d",
                url,
                resp.status,
            )
