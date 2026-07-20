# Notification System Design

> When to notify, channels, formatting, and priority levels.

---

## 1. Design Principles

| Principle | Description |
|-----------|-------------|
| **Actionable** | Every notification implies a next step |
| **Prioritized** | Urgent items surface first |
| **Contextual** | Notifications include enough info to act |
| **Non-intrusive** | Don't interrupt workflow for low-priority items |
| **Auditable** | All notifications are logged for compliance |

---

## 2. Notification Events

### 2.1 Event Catalog

| Event | Trigger | Priority | Default Channels |
|-------|---------|----------|------------------|
| `task.created` | New task assigned to agent | Low | Dashboard badge |
| `task.completed` | Agent finishes task | Low | Dashboard badge |
| `task.failed` | Agent task execution fails | High | Dashboard + CLI |
| `task.escalated` | Task exceeds timeout | High | Dashboard + CLI |
| `approval.requested` | Agent needs human approval | Medium | Dashboard card |
| `approval.approved` | Human approves request | Low | Dashboard badge |
| `approval.rejected` | Human rejects request | Medium | Dashboard + CLI |
| `approval.timeout` | Approval request expires | High | Dashboard + CLI + WebSocket |
| `escalation.triggered` | Escalation rule fires | Critical | Dashboard + CLI + WebSocket |
| `escalation.resolved` | Human resolves escalation | Medium | Dashboard badge |
| `budget.threshold` | Department exceeds budget % | High | Dashboard + CLI |
| `agent.offline` | Agent becomes unresponsive | Critical | Dashboard + CLI + WebSocket |
| `circuit_breaker.open` | LLM provider fails | High | Dashboard + CLI |
| `circuit_breaker.closed` | LLM provider recovers | Low | Dashboard badge |

### 2.2 Event Payload Structure

```json
{
  "event": "escalation.triggered",
  "timestamp": "2026-07-20T14:30:00Z",
  "priority": "critical",
  "source": {
    "type": "agent",
    "id": "lead-engineer",
    "department": "engineering"
  },
  "data": {
    "task_id": "task-abc123",
    "rule_id": "timeout-rule",
    "reason": "Task stalled for 30 minutes",
    "escalated_to": "cto"
  },
  "actions": [
    {"label": "View Task", "command": "ai-company executor status"},
    {"label": "View Escalation", "command": "ai-company orchestrator escalation pending"}
  ]
}
```

---

## 3. Notification Channels

### 3.1 Dashboard (Primary)

**Real-time via WebSocket:**
- KPI card badges update immediately
- Approval queue cards appear/disappear
- Escalation cards with red highlight
- Toast notifications for transient events

**Persistent notifications:**
- Notification bell icon with unread count
- Notification center panel (expandable)
- History of past 50 notifications

**Dashboard notification display:**
```
+------------------------------------------------------------------+
|  [LS] Light Speed Holdings    CEO Dashboard    [Bell: 3]  Uptime|
+------------------------------------------------------------------+
|                                                                    |
|  +--Notification Center (click bell)--------------------------+  |
|  |                                                             |  |
|  |  [Critical] Escalation: lead-engineer → cto               |  |
|  |  Task stalled for 30 minutes                               |  |
|  |  2 minutes ago                              [Resolve] [X]  |  |
|  |                                                             |  |
|  |  [High] Approval timeout: apr-7b3e9f                      |  |
|  |  Tier 2 request expired, escalating to Tier 3              |  |
|  |  5 minutes ago                              [View] [X]     |  |
|  |                                                             |  |
|  |  [Medium] Task completed: budget-report                    |  |
|  |  cfo completed Q3 budget analysis                          |  |
|  |  12 minutes ago                             [Dismiss] [X]  |  |
|  +-------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### 3.2 CLI Output

**Immediate feedback (inline):**
```
$ ai-company orchestrator tick

  Processing task a3f2c1 → lead-engineer
  ⚠ Task a3f2c1 requires approval (Tier 2)
  ✓ Task b7d4e2 completed by cfo
  ✗ Task c1a8f3 failed: LLM provider timeout
  ⚠ Task d4e5f6 escalated → cto (stalled 30 min)
```

**Persistent notifications (command):**
```bash
$ ai-company orchestrator notifications

  Recent Notifications (last 24h)
  ============================================================

  [CRITICAL] 14:30  Escalation: lead-engineer → cto
             Task stalled for 30 minutes
             Status: Unresolved

  [HIGH]     14:25  Approval timeout: apr-7b3e9f
             Tier 2 request expired
             Status: Escalated to Tier 3

  [MEDIUM]   14:18  Task completed: budget-report
             cfo completed Q3 budget analysis
             Status: Acknowledged

  Total: 3 notifications (1 critical, 1 high, 1 medium)
```

### 3.3 WebSocket Broadcast

```json
{
  "type": "alert",
  "timestamp": "2026-07-20T14:30:00Z",
  "payload": {
    "category": "escalation",
    "priority": "critical",
    "task_id": "task-abc123",
    "reason": "Task stalled for 30 minutes",
    "agent_id": "lead-engineer",
    "escalated_to": "cto"
  }
}
```

**Client handling:**
```javascript
ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.type === 'alert') {
    showNotification(msg.payload);
    updateBadge(msg.payload.priority);
  }
};
```

### 3.4 CLI WebSocket Push (Future)

When the executor is running, the CLI can subscribe to WebSocket updates:

```bash
$ ai-company executor start --watch

  Listening for events...
  
  [14:30:01] Task created: a3f2c1 → lead-engineer
  [14:30:03] Approval requested: apr-7b3e9f (Tier 2)
  [14:30:05] ✓ Task a3f2c1 completed
  [14:30:07] ⚠ Escalation: lead-engineer → cto
```

---

## 4. Notification Formatting

### 4.1 Dashboard Toast

```
+------------------------------------------+
| ⚠ Escalation Triggered                   |
| Task stalled for 30 minutes              |
| lead-engineer → cto                      |
|                                    [X]   |
+------------------------------------------+
```

**Position:** Top-right corner
**Auto-dismiss:** 10 seconds for Low/Medium, persistent for High/Critical
**Stack:** Multiple toasts stack vertically

### 4.2 Dashboard Card

```
+------------------------------------------+
| [CRITICAL]                               |
| Escalation: lead-engineer → cto          |
|                                          |
| Task stalled for 30 minutes              |
| Rule: timeout-rule                       |
|                                          |
| [View Task]  [Resolve]  [Dismiss]       |
+------------------------------------------+
```

### 4.3 CLI Inline

```
[CRITICAL] 14:30  Escalation: lead-engineer → cto
           Task stalled for 30 minutes
```

**Format:** `[PRIORITY] TIME  TITLE`
            `           BODY`

### 4.4 CLI Summary

```
Notifications: 3 (1 critical, 1 high, 1 medium)
Last: Escalation triggered 2 minutes ago
```

---

## 5. Priority Levels

| Level | Badge | Color | Auto-Dismiss | Sound |
|-------|-------|-------|--------------|-------|
| `critical` | 🔴 | Red | Never | Yes |
| `high` | 🟠 | Amber | Never | Yes |
| `medium` | 🟡 | Yellow | 30 seconds | No |
| `low` | 🟢 | Green | 10 seconds | No |

### Priority Escalation Rules

- If a `medium` notification is unacknowledged for 5 minutes → escalate to `high`
- If a `high` notification is unacknowledged for 15 minutes → escalate to `critical`
- `critical` never auto-escalates (already highest)

---

## 6. Notification Lifecycle

```
Created → Displayed → Acknowledged → Archived
              ↓
          Expired (if Low/Medium and no action)
```

### States

| State | Description |
|-------|-------------|
| `created` | Event occurred, notification generated |
| `displayed` | Shown to user in channel |
| `acknowledged` | User clicked/dismissed/resolved |
| `expired` | Auto-dismissed (Low/Medium only) |
| `archived` | Moved to history |

---

## 7. Notification Groups

Notifications are grouped by category for batch actions:

| Group | Events | Batch Action |
|-------|--------|--------------|
| Approvals | `approval.requested`, `approval.timeout` | "Approve All Tier 2" |
| Escalations | `escalation.triggered` | "Resolve All" |
| Tasks | `task.completed`, `task.failed` | "Dismiss All" |
| System | `circuit_breaker.open`, `agent.offline` | "Acknowledge All" |

---

## 8. Filtering & Preferences

### 8.1 Filter Options

```bash
$ ai-company orchestrator notifications --priority critical

  Critical Notifications (1)
  ============================================================
  
  [CRITICAL] 14:30  Escalation: lead-engineer → cto
             Task stalled for 30 minutes
```

### 8.2 User Preferences (Future)

```yaml
# company/config/notifications.yaml
preferences:
  dashboard:
    toast_duration: 10
    sound_enabled: true
    show_low_priority: false
  cli:
    color_enabled: true
    verbose_mode: false
  channels:
    websocket: true
    email: false
    slack: false
```

---

## 9. Notification History

Stored in `orchestrator/notifications.json`:

```json
[
  {
    "id": "notif-001",
    "event": "escalation.triggered",
    "priority": "critical",
    "timestamp": "2026-07-20T14:30:00Z",
    "source": {"type": "agent", "id": "lead-engineer"},
    "data": {"task_id": "task-abc123", "reason": "Stalled 30min"},
    "status": "acknowledged",
    "acknowledged_at": "2026-07-20T14:32:00Z",
    "acknowledged_by": "human-ceo"
  }
]
```

### Retention

- Last 50 notifications kept in memory
- Last 500 notifications kept in file
- Archived notifications older than 30 days are purged

---

## 10. Accessibility

- All notifications include `aria-label` with full text
- Critical notifications trigger screen reader announcement
- Sound notifications can be disabled via `NO_SOUND` env var
- Color is never sole indicator (text labels always present)
- Keyboard shortcut: `n` to open notification center, `Esc` to close
