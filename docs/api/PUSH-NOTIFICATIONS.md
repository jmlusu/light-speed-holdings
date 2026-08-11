# Push Notification System

Push notification architecture for the AI Company Builder mobile dashboard.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Notification Types](#2-notification-types)
3. [Payload Formats](#3-payload-formats)
4. [FCM Integration](#4-fcm-integration)
5. [Device Registration](#5-device-registration)
6. [Delivery Rules](#6-delivery-rules)
7. [Quiet Hours](#7-quiet-hours)
8. [Server Implementation](#8-server-implementation)
9. [Client Implementation](#9-client-implementation)
10. [Testing](#10-testing)

---

## 1. Overview

The push notification system delivers real-time alerts to mobile devices when critical events occur in the AI Company Builder. Notifications are dispatched via Firebase Cloud Messaging (FCM) for Android and web, and can be extended to APNs for iOS.

**Architecture:**

```
Event Source → Notification Service → FCM/APNs → Mobile Device
     ↑
  Dashboard API
  (approvals, escalations, KPIs)
```

**Notification Delivery Flow:**
1. Event occurs (approval requested, escalation triggered, etc.)
2. Dashboard API detects event (via background tasks or WebSocket broadcast)
3. Notification service queries registered devices with matching preferences
4. Service constructs payload and sends to FCM
5. FCM delivers to device
6. Device shows notification, routes to appropriate screen on tap

---

## 2. Notification Types

| Type | Priority | Default | Description | Trigger |
|------|----------|---------|-------------|---------|
| `escalation` | `high` | ON | Task escalated to CEO | Escalation engine triggers |
| `approval_needed` | `high` | ON | Approval request pending | Agent requests approval |
| `budget_alert` | `high` | ON | Budget threshold exceeded | KPI collector detects |
| `task_complete` | `normal` | OFF | Assigned task completed | Task status → completed |
| `task_failed` | `high` | ON | Task execution failed | Task status → failed |
| `daily_summary` | `low` | ON | End-of-day summary | Scheduled (daily) |
| `system_alert` | `critical` | ON | System health issue | Health check failure |
| `delegation` | `normal` | OFF | Task delegated to you | Task reassigned |

**Priority Mapping to FCM:**

| App Priority | FCM Priority | Behavior |
|-------------|--------------|----------|
| `critical` | `high` | Heads-up display, sound, vibration |
| `high` | `high` | Heads-up display, sound |
| `normal` | `normal` | Status bar, no sound |
| `low` | `low` | Silent delivery, badge only |

---

## 3. Payload Formats

### Standard Notification Payload

All notification types follow this base structure:

```json
{
  "notification": {
    "title": "Escalation: Task exceeded SLA",
    "body": "Backend engineer task exceeded 30-min timeout. Requires immediate review.",
    "image": null
  },
  "data": {
    "type": "escalation",
    "category": "urgent",
    "target_id": "550e8400-e29b-41d4-a716-446655440000",
    "action_url": "/approvals?escalation=550e8400",
    "timestamp": "2026-07-20T14:30:00Z"
  },
  "android": {
    "priority": "high",
    "notification": {
      "channel_id": "urgent",
      "click_action": "OPEN_APPROVALS"
    }
  },
  "apns": {
    "headers": {
      "apns-priority": "10"
    },
    "payload": {
      "aps": {
        "alert": {
          "title": "Escalation: Task exceeded SLA",
          "body": "Backend engineer task exceeded 30-min timeout."
        },
        "sound": "default",
        "badge": 3
      }
    }
  }
}
```

### Type-Specific Payloads

#### Escalation Notification

```json
{
  "notification": {
    "title": "Escalation: Task SLA Timeout",
    "body": "backend-engineer → lead-engineer: Task exceeded 30-min SLA timeout"
  },
  "data": {
    "type": "escalation",
    "task_id": "550e8400",
    "from_agent": "backend-engineer",
    "to_agent": "lead-engineer",
    "reason": "Task exceeded SLA timeout of 30 minutes",
    "action_url": "/approvals?tab=escalations"
  }
}
```

#### Approval Needed Notification

```json
{
  "notification": {
    "title": "Approval Required",
    "body": "CTO requests approval: deploy to production (v2.1.0)"
  },
  "data": {
    "type": "approval_needed",
    "request_id": "REQ-001",
    "agent_id": "cto",
    "action": "deploy to production",
    "description": "Deploy v2.1.0 to production servers",
    "priority": "high",
    "expires_at": "2026-07-21T09:00:00Z",
    "action_url": "/approvals?request=REQ-001"
  }
}
```

#### Budget Alert Notification

```json
{
  "notification": {
    "title": "Budget Alert: Engineering",
    "body": "Engineering department at 85% of monthly budget ($42,500 / $50,000)"
  },
  "data": {
    "type": "budget_alert",
    "department": "engineering",
    "utilization_pct": 85,
    "spent": 42500,
    "budget": 50000,
    "threshold": 80,
    "action_url": "/dashboard?highlight=budget"
  }
}
```

#### Task Complete Notification

```json
{
  "notification": {
    "title": "Task Completed",
    "body": "lead-engineer completed: Review PR #42 for authentication module"
  },
  "data": {
    "type": "task_complete",
    "task_id": "550e8400",
    "receiver_id": "lead-engineer",
    "instruction": "Review PR #42 for authentication module",
    "action_url": "/tasks?task=550e8400"
  }
}
```

#### Task Failed Notification

```json
{
  "notification": {
    "title": "Task Failed",
    "body": "backend-engineer: Build pipeline failed for main branch"
  },
  "data": {
    "type": "task_failed",
    "task_id": "660f9500",
    "receiver_id": "backend-engineer",
    "instruction": "Build pipeline for main branch",
    "error": "CI/CD pipeline exited with code 1",
    "action_url": "/tasks?task=660f9500&filter=failed"
  }
}
```

#### Daily Summary Notification

```json
{
  "notification": {
    "title": "Daily Summary — July 20, 2026",
    "body": "12 completed, 2 failed, 3 pending approvals, 1 escalation. 27 agents active."
  },
  "data": {
    "type": "daily_summary",
    "date": "2026-07-20",
    "completed": 12,
    "failed": 2,
    "pending_approvals": 3,
    "open_escalations": 1,
    "active_agents": 27,
    "action_url": "/dashboard"
  }
}
```

#### System Alert Notification

```json
{
  "notification": {
    "title": "System Alert",
    "body": "Dashboard service health check failed. Service may be unreachable."
  },
  "data": {
    "type": "system_alert",
    "severity": "critical",
    "service": "ceo-dashboard",
    "check": "health",
    "error": "Connection refused",
    "action_url": "/system"
  }
}
```

---

## 4. FCM Integration

### Server-Side FCM Setup

```python
# Required dependency: firebase-admin
# pip install firebase-admin

import firebase_admin
from firebase_admin import credentials, messaging

# Initialize with service account key
cred = credentials.Certificate("config/firebase-service-account.json")
firebase_admin.initialize_app(cred)


def send_push_notification(
    token: str,
    title: str,
    body: str,
    data: dict[str, str],
    priority: str = "normal",
    channel_id: str = "general",
) -> messaging.SendResponse:
    """Send a push notification via FCM."""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        token=token,
        android=messaging.AndroidConfig(
            priority=priority,
            notification=messaging.AndroidNotification(
                channel_id=channel_id,
                click_action="OPEN_DASHBOARD",
            ),
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title=title,
                        body=body,
                    ),
                    sound="default",
                    badge=_get_badge_count(token),
                ),
            ),
        ),
    )
    return messaging.send(message)
```

### FCM Channel Configuration (Android)

| Channel ID | Name | Priority | Sound | Vibration |
|-----------|------|----------|-------|-----------|
| `urgent` | Urgent Alerts | HIGH | Yes | Yes |
| `approvals` | Approvals | HIGH | Yes | Yes |
| `general` | General | DEFAULT | No | No |
| `summary` | Daily Summary | LOW | No | No |

---

## 5. Device Registration

### Registration Flow

```
Mobile App → POST /api/mobile/notifications/register
    → Server stores device token + preferences
    → Server returns device_id
    → App stores device_id locally
```

### Device Storage Schema

```python
from pydantic import BaseModel
from typing import Optional


class NotificationPreferences(BaseModel):
    escalations: bool = True
    approvals: bool = True
    budget_alerts: bool = True
    task_complete: bool = False
    task_failed: bool = True
    daily_summary: bool = True
    system_alert: bool = True
    delegation: bool = False
    quiet_hours_start: Optional[str] = None  # "22:00"
    quiet_hours_end: Optional[str] = None    # "07:00"
    timezone: str = "UTC"


class DeviceRegistration(BaseModel):
    device_id: str
    device_token: str
    platform: str  # "ios" | "android" | "web"
    app_version: str = ""
    device_name: str = ""
    preferences: NotificationPreferences = NotificationPreferences()
    registered_at: str
    last_active_at: str
    is_active: bool = True
```

### Device Token Rotation

- Tokens should be refreshed on app update
- Server detects duplicate registrations (same device_id, different token) and updates
- Tokens older than 90 days without activity are marked inactive
- Inactive devices are excluded from push delivery

---

## 6. Delivery Rules

### Notification Dispatch Logic

```python
async def dispatch_notification(
    notification_type: str,
    payload: dict,
    target_agents: list[str] | None = None,
) -> int:
    """Dispatch notification to all eligible devices.

    Returns the number of devices notified.
    """
    # 1. Find devices with this notification type enabled
    devices = await get_active_devices(notification_type)

    # 2. Filter by quiet hours
    now = datetime.now(timezone.utc)
    eligible = [d for d in devices if not in_quiet_hours(d, now)]

    # 3. Deduplicate (one notification per device_id)
    seen = set()
    unique = []
    for d in eligible:
        if d.device_id not in seen:
            seen.add(d.device_id)
            unique.append(d)

    # 4. Send via FCM
    sent = 0
    for device in unique:
        try:
            send_push_notification(
                token=device.device_token,
                title=payload["title"],
                body=payload["body"],
                data=payload["data"],
                priority=_priority_for_type(notification_type),
                channel_id=_channel_for_type(notification_type),
            )
            sent += 1
            await log_delivery(device.device_id, notification_type)
        except Exception as e:
            logger.warning(f"Push failed for {device.device_id}: {e}")
            await handle_token_error(device, e)

    return sent
```

### Deduplication Rules

| Scenario | Rule |
|----------|------|
| Same escalation, multiple agents | One notification per device |
| Rapid-fire approvals | Coalesce within 5-second window |
| KPI threshold repeatedly hit | Max 1 per hour per device |
| Daily summary | Once per day per device (at configured time) |

### Retry Policy

| Attempt | Delay | Condition |
|---------|-------|-----------|
| 1 | Immediate | First attempt |
| 2 | 30 seconds | FCM returned transient error |
| 3 | 2 minutes | Still failing |
| 4 | 15 minutes | Final attempt |

After 4 failures, mark token as potentially invalid. After 3 consecutive failures on the same token, mark as inactive.

---

## 7. Quiet Hours

Quiet hours suppress notification display but still log the notification for in-app review.

### Behavior During Quiet Hours

| Aspect | Behavior |
|--------|----------|
| Push notification | Suppressed (not sent) |
| In-app badge count | Updated normally |
| Notification log | Recorded with `suppressed: true` |
| WebSocket alert | Sent normally (if connected) |
| Missed notifications | Summary shown on app open |

### Implementation

```python
def in_quiet_hours(device: DeviceRegistration, now: datetime) -> bool:
    """Check if current time falls within device's quiet hours."""
    if not device.preferences.quiet_hours_start or not device.preferences.quiet_hours_end:
        return False

    tz = ZoneInfo(device.preferences.timezone)
    local_now = now.astimezone(tz)
    current_time = local_now.strftime("%H:%M")

    start = device.preferences.quiet_hours_start
    end = device.preferences.quiet_hours_end

    if start <= end:
        # Same day: 22:00 to 07:00 wraps around
        return start <= current_time <= end
    else:
        # Wraps midnight: 22:00 to 07:00
        return current_time >= start or current_time <= end
```

---

## 8. Server Implementation

### Notification Service Module

```python
# src/ai_company/dashboard/notifications.py

"""Push notification service for mobile devices."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

logger = logging.getLogger(__name__)

DEVICE_STORE_PATH = Path("orchestrator/devices.yaml")


class NotificationEvent(BaseModel):
    type: str
    title: str
    body: str
    data: dict[str, str] = {}
    priority: str = "normal"
    target_agents: list[str] | None = None


class NotificationService:
    """Manages device registrations and notification dispatch."""

    def __init__(self) -> None:
        self._devices: list[dict] = []
        self._load_devices()

    def _load_devices(self) -> None:
        if DEVICE_STORE_PATH.exists():
            with open(DEVICE_STORE_PATH, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            self._devices = data.get("devices", [])

    def _save_devices(self) -> None:
        DEVICE_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DEVICE_STORE_PATH, "w", encoding="utf-8") as f:
            yaml.dump(
                {"devices": self._devices},
                f,
                default_flow_style=False,
                sort_keys=False,
            )

    def register_device(self, registration: dict[str, Any]) -> dict[str, Any]:
        """Register or update a device for push notifications."""
        device_id = registration.get("device_id", "")
        existing = next((d for d in self._devices if d.get("device_id") == device_id), None)

        if existing:
            existing.update(registration)
        else:
            import uuid
            registration.setdefault("device_id", f"dev_{uuid.uuid4().hex[:12]}")
            registration.setdefault("registered_at", datetime.now(timezone.utc).isoformat())
            self._devices.append(registration)

        registration["last_active_at"] = datetime.now(timezone.utc).isoformat()
        self._save_devices()
        return registration

    def unregister_device(self, device_token: str) -> int:
        """Remove a device by token. Returns count removed."""
        before = len(self._devices)
        self._devices = [d for d in self._devices if d.get("device_token") != device_token]
        self._save_devices()
        return before - len(self._devices)

    def get_devices_for_notification(self, notification_type: str) -> list[dict]:
        """Get active devices that have this notification type enabled."""
        return [
            d for d in self._devices
            if d.get("is_active", True)
            and d.get("preferences", {}).get(notification_type, False)
        ]

    def dispatch(self, event: NotificationEvent) -> int:
        """Dispatch notification event to eligible devices."""
        devices = self.get_devices_for_notification(event.type)
        # ... FCM send logic (see Section 4)
        return len(devices)
```

### Integration with Dashboard API

Notifications are triggered as background tasks from the existing dashboard API endpoints:

```python
# In api.py — existing approval endpoint already broadcasts via WebSocket
# Add notification dispatch as additional background task

@router.post("/approvals/{request_id}/approve")
def approve_request(request_id: str, body: ApprovalDecision | None = None, background_tasks: BackgroundTasks = None) -> dict:
    # ... existing approval logic ...

    # Dispatch push notification (new)
    if background_tasks:
        background_tasks.add_task(
            _dispatch_notification,
            NotificationEvent(
                type="task_complete",
                title=f"Approval {request_id} processed",
                body=f"Request approved by {body.approved_by if body else 'human-ceo'}",
                data={"request_id": request_id, "action": "approved"},
            ),
        )

    return {"ok": True, "id": request_id}
```

---

## 9. Client Implementation

### Service Worker (Web/PWA)

```javascript
// static/js/push-worker.js

self.addEventListener("push", (event) => {
  const data = event.data?.json() || {};

  const options = {
    body: data.notification?.body || "",
    icon: "/icons/icon-192.png",
    badge: "/icons/badge-72.png",
    data: data.data || {},
    actions: _getActionsForType(data.data?.type),
    tag: data.data?.type || "general",
    renotify: true,
    requireInteraction: data.data?.category === "urgent",
  };

  event.waitUntil(
    self.registration.showNotification(
      data.notification?.title || "AI Company Builder",
      options
    )
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  const url = event.notification.data?.action_url || "/";
  const action = event.action;

  if (action === "approve") {
    // Quick approve via API
    event.waitUntil(
      fetch(`/api/approvals/${event.notification.data.request_id}/approve`, {
        method: "POST",
      }).then(() => clients.openWindow(url))
    );
  } else if (action === "reject") {
    event.waitUntil(
      fetch(`/api/approvals/${event.notification.data.request_id}/reject`, {
        method: "POST",
      }).then(() => clients.openWindow(url))
    );
  } else {
    event.waitUntil(clients.openWindow(url));
  }
});

function _getActionsForType(type) {
  switch (type) {
    case "approval_needed":
      return [
        { action: "approve", title: "Approve" },
        { action: "reject", title: "Reject" },
      ];
    case "escalation":
      return [
        { action: "view", title: "View Details" },
      ];
    default:
      return [];
  }
}
```

### FCM Token Management (Client)

```javascript
// In mobile.js or app initialization

async function initializePushNotifications() {
  // Request permission
  const permission = await Notification.requestPermission();
  if (permission !== "granted") return;

  // Get FCM token
  const registration = await navigator.serviceWorker.ready;
  const token = await messaging.getToken({
    vapidKey: "YOUR_VAPID_KEY",
    serviceWorkerRegistration: registration,
  });

  // Register with server
  await fetch("/api/mobile/notifications/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      device_token: token,
      platform: "web",
      app_version: "1.0.0",
      preferences: _loadNotificationPreferences(),
    }),
  });

  // Listen for token refresh
  messaging.onTokenRefresh(async () => {
    const newToken = await messaging.getToken();
    await _updateServerToken(newToken);
  });
}
```

---

## 10. Testing

### Unit Tests

```python
# tests/unit/test_notifications.py

import pytest
from ai_company.dashboard.notifications import NotificationService, NotificationEvent


@pytest.fixture
def service(tmp_path, monkeypatch):
    """Create a NotificationService with a temporary device store."""
    monkeypatch.setattr(
        "ai_company.dashboard.notifications.DEVICE_STORE_PATH",
        tmp_path / "devices.yaml",
    )
    return NotificationService()


def test_register_device(service):
    result = service.register_device({
        "device_token": "test_token_123",
        "platform": "android",
        "preferences": {"escalations": True, "approvals": True},
    })
    assert result["device_id"].startswith("dev_")
    assert result["platform"] == "android"


def test_unregister_device(service):
    service.register_device({"device_token": "tok_1"})
    removed = service.unregister_device("tok_1")
    assert removed == 1
    assert len(service.get_devices_for_notification("escalations")) == 0


def test_get_devices_filters_by_type(service):
    service.register_device({
        "device_token": "tok_1",
        "preferences": {"escalations": True, "approvals": False},
    })
    service.register_device({
        "device_token": "tok_2",
        "preferences": {"escalations": False, "approvals": True},
    })

    escalation_devices = service.get_devices_for_notification("escalations")
    assert len(escalation_devices) == 1
    assert escalation_devices[0]["device_token"] == "tok_1"

    approval_devices = service.get_devices_for_notification("approvals")
    assert len(approval_devices) == 1
    assert approval_devices[0]["device_token"] == "tok_2"


def test_dispatch_returns_count(service):
    service.register_device({
        "device_token": "tok_1",
        "preferences": {"escalations": True},
    })
    event = NotificationEvent(
        type="escalations",
        title="Test",
        body="Test body",
    )
    # dispatch would normally call FCM; mock it
    count = service.dispatch(event)
    assert count == 1
```

### Integration Tests

```python
# tests/integration/test_mobile_notifications.py

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_check_status(async_client: AsyncClient):
    # Register device
    reg = await async_client.post("/api/mobile/notifications/register", json={
        "device_token": "test_fcm_token",
        "platform": "android",
        "preferences": {"escalations": True},
    })
    assert reg.status_code == 200
    device_id = reg.json()["device_id"]

    # Check status
    status = await async_client.get(
        f"/api/mobile/notifications/status?device_token=test_fcm_token"
    )
    assert status.status_code == 200
    assert status.json()["device_token"] == "test_fcm_token"


@pytest.mark.asyncio
async def test_unregister_device(async_client: AsyncClient):
    await async_client.post("/api/mobile/notifications/register", json={
        "device_token": "tok_to_remove",
        "platform": "ios",
    })

    result = await async_client.delete("/api/mobile/notifications/unregister", json={
        "device_token": "tok_to_remove",
    })
    assert result.status_code == 200
    assert result.json()["removed"] == 1
```
