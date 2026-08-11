# Mobile API Reference

REST endpoints optimized for mobile clients accessing the AI Company Builder CEO Dashboard.

**Base URL:** `http://localhost:8420`
**Version:** 0.1.0

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [Mobile Dashboard Summary](#2-mobile-dashboard-summary)
3. [Paginated Task List](#3-paginated-task-list)
4. [Quick Actions](#4-quick-actions)
5. [Push Notification Registration](#5-push-notification-registration)
6. [Mobile Approvals (Swipe Flow)](#6-mobile-approvals-swipe-flow)
7. [Compact KPIs](#7-compact-kpis)
8. [Offline Sync](#8-offline-sync)
9. [Response Optimization](#9-response-optimization)
10. [Rate Limits](#10-rate-limits)

---

## 1. Authentication

Mobile endpoints use the same `X-API-Key` header mechanism as the main dashboard API.

For push notification registration, devices also provide a device token.

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `X-API-Key` | string | Conditional | Required when `DASHBOARD_API_KEY` env var is set |
| `X-Device-ID` | string | Recommended | Unique device identifier for push routing |
| `X-App-Version` | string | Optional | Mobile app version for compatibility |

---

## 2. Mobile Dashboard Summary

Condensed KPI payload designed to minimize data transfer on cellular networks.

### `GET /api/mobile/dashboard`

Returns a compact dashboard summary with only the most critical metrics for mobile viewing.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `compact` | boolean | No | `true` | Return minimal payload (fewer fields) |

**Response:** `MobileDashboardSummary`

```json
{
  "kpis": {
    "pending": 5,
    "completed": 142,
    "escalations": 1,
    "approvals": 3,
    "agents": 27
  },
  "urgent": {
    "approval_count": 3,
    "escalation_count": 1,
    "failed_count": 2
  },
  "recent_tasks": [
    {
      "id": "550e8400",
      "to": "lead-engineer",
      "instruction": "Review PR #42",
      "priority": "high",
      "status": "pending",
      "created": "10:30"
    }
  ],
  "connection": "live",
  "updated_at": "2026-07-20T14:30:00Z"
}
```

**Payload Size:** ~1.2 KB typical (vs ~3.5 KB for full `/api/dashboard` + `/api/tasks`)

**Design Notes:**
- `recent_tasks` limited to 5 items maximum
- Timestamps use short ISO format (no timezone suffix)
- Task IDs are truncated to first 8 characters
- Instructions truncated to 60 characters
- No `result` field in task summaries (use detail endpoint for that)

---

## 3. Paginated Task List

Task list endpoint with cursor-based pagination for efficient scrolling on mobile.

### `GET /api/mobile/tasks`

Returns a page of tasks with pagination metadata.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | — | Filter by status |
| `agent` | string | No | — | Filter by agent ID |
| `priority` | string | No | — | Filter by priority |
| `cursor` | string | No | — | Pagination cursor from previous response |
| `limit` | integer | No | `20` | Items per page (max 50) |

**Response:** `PaginatedTaskList`

```json
{
  "items": [
    {
      "id": "550e8400",
      "from": "human-ceo",
      "to": "lead-engineer",
      "instruction": "Review PR #42 for the authentication module",
      "priority": "high",
      "status": "pending",
      "created": "2026-07-20T10:30:00Z",
      "has_result": false
    }
  ],
  "next_cursor": "eyJpZCI6IjU1MGU4NDAwIn0=",
  "total_count": 158,
  "page_size": 20,
  "has_more": true
}
```

**Pagination Protocol:**
1. First request: no `cursor` parameter → returns first page
2. Response includes `next_cursor` if more items exist
3. Next request: pass `next_cursor` as `cursor` parameter
4. When `has_more` is `false`, no more pages

**Why Cursor-Based (not Offset):**
- Consistent results when new tasks are created between pages
- No skipped or duplicated items
- Efficient for large task lists
- Works well with WebSocket-informed refresh

---

## 4. Quick Actions

Batch action endpoints for mobile users to quickly approve, escalate, or delegate multiple items.

### `POST /api/mobile/actions/batch`

Execute multiple actions in a single request to minimize network round trips.

**Request Body:**

```json
{
  "actions": [
    {
      "type": "approve",
      "target_id": "REQ-001",
      "notes": "Approved from mobile"
    },
    {
      "type": "approve",
      "target_id": "REQ-002"
    },
    {
      "type": "resolve_escalation",
      "target_id": "550e8400"
    }
  ]
}
```

**Action Types:**

| Type | Target ID Format | Description |
|------|-------------------|-------------|
| `approve` | Approval request ID | Approve a pending request |
| `reject` | Approval request ID | Reject a pending request |
| `resolve_escalation` | Task ID | Mark escalation as resolved |
| `delegate` | Task ID | Reassign task (requires `delegate_to` field) |

**Response:**

```json
{
  "results": [
    { "type": "approve", "target_id": "REQ-001", "ok": true },
    { "type": "approve", "target_id": "REQ-002", "ok": true },
    { "type": "resolve_escalation", "target_id": "550e8400", "ok": true }
  ],
  "succeeded": 3,
  "failed": 0
}
```

**Batch Limits:**
- Maximum 10 actions per request
- Actions are processed sequentially (first-failure semantics optional via `continue_on_error`)
- Each action result is independent (partial success is possible)

### `POST /api/mobile/actions/quick-approve`

One-tap approve all pending approvals (dangerous, requires confirmation token).

**Request Body:**

```json
{
  "confirm": true,
  "notes": "Bulk approval from mobile"
}
```

**Response:**

```json
{
  "approved_count": 3,
  "ids": ["REQ-001", "REQ-002", "REQ-003"]
}
```

---

## 5. Push Notification Registration

Register mobile devices for push notifications via FCM (Firebase Cloud Messaging) or APNs (Apple Push Notification service).

### `POST /api/mobile/notifications/register`

Register a device token for push notifications.

**Request Body:**

```json
{
  "device_token": "fcm_token_or_apns_token_here",
  "platform": "android",
  "app_version": "1.0.0",
  "device_name": "Pixel 8 Pro",
  "preferences": {
    "escalations": true,
    "approvals": true,
    "budget_alerts": true,
    "task_complete": false,
    "daily_summary": true,
    "quiet_hours_start": "22:00",
    "quiet_hours_end": "07:00",
    "timezone": "America/New_York"
  }
}
```

**Platform Values:** `ios`, `android`, `web`

**Response:**

```json
{
  "ok": true,
  "device_id": "dev_abc123",
  "registered_at": "2026-07-20T14:30:00Z"
}
```

### `DELETE /api/mobile/notifications/unregister`

Remove a device from push notification delivery.

**Request Body:**

```json
{
  "device_token": "fcm_token_here"
}
```

**Response:**

```json
{
  "ok": true,
  "removed": 1
}
```

### `PATCH /api/mobile/notifications/preferences`

Update notification preferences for a registered device.

**Request Body:**

```json
{
  "device_token": "fcm_token_here",
  "preferences": {
    "escalations": true,
    "approvals": true,
    "quiet_hours_start": "23:00",
    "quiet_hours_end": "08:00"
  }
}
```

**Response:**

```json
{
  "ok": true,
  "updated_fields": ["quiet_hours_start", "quiet_hours_end"]
}
```

### `GET /api/mobile/notifications/status`

Check notification delivery status for recent notifications.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `device_token` | string | Yes | Check status for this device |
| `since` | string | No | ISO timestamp, default last 24h |

**Response:**

```json
{
  "device_token": "fcm_token_here",
  "last_delivery": "2026-07-20T14:00:00Z",
  "notifications_sent_24h": 12,
  "notifications_delivered_24h": 11,
  "delivery_rate": 0.917
}
```

---

## 6. Mobile Approvals (Swipe Flow)

Optimized endpoints for the swipe-to-approve/reject UI pattern on mobile.

### `GET /api/mobile/approvals/stack`

Returns approval requests in swipe-stack format (one at a time, preloaded).

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | `5` | Number of items to preload in stack |

**Response:**

```json
{
  "current": {
    "id": "REQ-001",
    "agent_id": "cto",
    "action": "deploy to production",
    "description": "Deploy v2.1.0 to production servers. Includes security patches and performance improvements.",
    "priority": "high",
    "requested_at": "2026-07-20T09:00:00Z",
    "expires_at": "2026-07-21T09:00:00Z",
    "context": {
      "department": "engineering",
      "estimated_impact": "high",
      "related_tasks": ["550e8400"]
    }
  },
  "stack": [
    {
      "id": "REQ-002",
      "agent_id": "cmo",
      "action": "launch campaign",
      "description": "Launch Q3 marketing campaign",
      "priority": "medium"
    }
  ],
  "remaining_count": 1,
  "total_pending": 3
}
```

### `POST /api/mobile/approvals/swipe`

Process a swipe action (approve or reject with gesture metadata).

**Request Body:**

```json
{
  "request_id": "REQ-001",
  "decision": "approve",
  "gesture": {
    "direction": "right",
    "velocity": "fast",
    "distance_px": 300
  },
  "notes": ""
}
```

**Decision Values:** `approve`, `reject`, `skip`

**Response:**

```json
{
  "ok": true,
  "decision": "approve",
  "next": {
    "id": "REQ-002",
    "agent_id": "cmo",
    "action": "launch campaign",
    "description": "Launch Q3 marketing campaign",
    "priority": "medium"
  },
  "remaining_count": 2
}
```

**Swipe Gesture Mapping:**
| Direction | Action |
|-----------|--------|
| Right (fast) | Approve |
| Left (fast) | Reject |
| Up | Skip (keep in queue) |
| Tap | View details |

---

## 7. Compact KPIs

Lightweight KPI endpoint for widget display and background refresh.

### `GET /api/mobile/kpis/compact`

Returns only numeric KPI values with no metadata. Ideal for widget/notification badges.

**Response:**

```json
{
  "pending": 5,
  "approvals": 3,
  "escalations": 1,
  "completed_today": 12,
  "failed": 0
}
```

**Payload Size:** ~120 bytes

### `GET /api/mobile/kpis/trend`

Returns KPI trend data for sparkline charts on mobile.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metric` | string | No | `pending` | KPI metric name |
| `hours` | integer | No | `24` | Hours of history to return |

**Response:**

```json
{
  "metric": "pending",
  "unit": "count",
  "data_points": [
    { "ts": "2026-07-20T00:00:00Z", "v": 8 },
    { "ts": "2026-07-20T04:00:00Z", "v": 6 },
    { "ts": "2026-07-20T08:00:00Z", "v": 5 },
    { "ts": "2026-07-20T12:00:00Z", "v": 5 }
  ],
  "current": 5,
  "min": 3,
  "max": 12,
  "trend": "decreasing"
}
```

---

## 8. Offline Sync

Endpoints for syncing data when the mobile app reconnects after being offline.

### `POST /api/mobile/sync`

Upload locally queued actions and fetch any updates since the last sync.

**Request Body:**

```json
{
  "last_sync_at": "2026-07-20T10:00:00Z",
  "pending_actions": [
    {
      "client_id": "local_abc123",
      "type": "approve",
      "target_id": "REQ-003",
      "queued_at": "2026-07-20T10:15:00Z"
    }
  ],
  "device_token": "fcm_token_here"
}
```

**Response:**

```json
{
  "synced_at": "2026-07-20T14:30:00Z",
  "processed_actions": [
    {
      "client_id": "local_abc123",
      "server_id": "REQ-003",
      "ok": true
    }
  ],
  "updates": {
    "new_approvals": 1,
    "new_escalations": 0,
    "tasks_changed": 3
  },
  "dashboard_delta": {
    "pending": 5,
    "approvals": 4,
    "escalations": 1,
    "completed_today": 14
  }
}
```

**Offline Sync Protocol:**
1. App detects network loss → queues actions locally in IndexedDB
2. App continues displaying cached data with "offline" indicator
3. On reconnect, app calls `POST /api/mobile/sync` with:
   - Timestamp of last successful sync
   - Any locally queued actions
4. Server processes queued actions and returns:
   - Results of each queued action
   - Dashboard delta since last sync
5. App updates local cache and UI

**Conflict Resolution:**
- If a queued action targets an already-processed item (e.g., already approved), server returns `ok: false` with reason
- Client removes conflict from local queue
- Dashboard data always reflects server state (last-write-wins for KPIs)

---

## 9. Response Optimization

### Payload Compression

All mobile endpoints support gzip and brotli compression via `Accept-Encoding` header.

**Client should send:**
```
Accept-Encoding: gzip, br
```

**Server will respond with compressed body when `Content-Length` > 1 KB.**

### Field Selection

Mobile endpoints accept a `fields` query parameter to request only needed fields.

**Example:**
```
GET /api/mobile/tasks?fields=id,instruction,status
```

**Response (only requested fields included):**
```json
{
  "items": [
    {
      "id": "550e8400",
      "instruction": "Review PR #42",
      "status": "pending"
    }
  ],
  "next_cursor": "...",
  "total_count": 158,
  "page_size": 20,
  "has_more": true
}
```

### ETag Support

All GET endpoints return an `ETag` header. Clients can send `If-None-Match` to avoid re-downloading unchanged data.

**Server response header:**
```
ETag: "a1b2c3d4e5f6"
```

**Client subsequent request:**
```
If-None-Match: "a1b2c3d4e5f6"
```

**Server response (no change):**
```
304 Not Modified
```

### Batch Endpoint

Fetch multiple resources in one request to reduce round trips on high-latency connections.

### `POST /api/mobile/batch`

**Request Body:**

```json
{
  "requests": [
    { "method": "GET", "path": "/api/mobile/dashboard" },
    { "method": "GET", "path": "/api/mobile/approvals/stack?limit=3" },
    { "method": "GET", "path": "/api/mobile/kpis/compact" }
  ]
}
```

**Response:**

```json
{
  "results": [
    { "status": 200, "body": { "kpis": { ... }, "urgent": { ... } } },
    { "status": 200, "body": { "current": { ... }, "stack": [...] } },
    { "status": 200, "body": { "pending": 5, "approvals": 3 } }
  ]
}
```

**Batch Limits:**
- Maximum 5 sub-requests per batch
- All sub-requests must be GET (no mutations in batch)
- Sub-requests processed sequentially

---

## 10. Rate Limits

Mobile endpoints share the same rate limiter as the main dashboard API.

| Limit | Value | Scope |
|-------|-------|-------|
| Requests per minute | 100 | Per IP address |
| Batch requests | 10/min | Per IP (heavier cost) |
| Push registration | 10/hour | Per device token |

**Rate limit headers returned:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1692532200
```

When rate limited (429):
```json
{
  "detail": "Rate limit exceeded",
  "retry_after_seconds": 42
}
```

---

## Offline Strategy Summary

| Layer | Strategy | Storage |
|-------|----------|---------|
| Dashboard KPIs | Cache last response, show stale data with timestamp | localStorage |
| Task list | Cursor-based pages, cache per-cursor response | IndexedDB |
| Approvals | Preloaded swipe stack, local action queue | IndexedDB |
| Actions | Queue locally on offline, sync on reconnect | IndexedDB |
| WebSocket | Auto-reconnect with exponential backoff | In-memory |
| Static assets | Service worker cache-first | Cache API |

**Cache Invalidation:**
- KPIs: 30-second TTL (WebSocket update overrides)
- Tasks: 60-second TTL or explicit refresh
- Approvals: Always fetch fresh on tab focus
- Actions: Processed locally, synced with conflict resolution
