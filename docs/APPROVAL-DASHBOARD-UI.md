# Dashboard Approval Queue UI Specification

> Phase 5 — FastAPI Dashboard with Real-Time Approval Management

## 1. Page Layout

The approval queue replaces the current minimal `/approvals` section with a full-page view accessible from the dashboard sidebar.

```
┌─────────────────────────────────────────────────────────────────┐
│  Light Speed Holdings — CEO Dashboard                    [⚙]   │
├──────────┬──────────────────────────────────────────────────────┤
│          │                                                      │
│ Overview │  Approvals                                    [Refresh]│
│ Agents   │  ─────────────────────────────────────────────────── │
│ Tasks    │                                                      │
│ > Approvals  ┌─────────┬──────────┬──────────┬──────────┐      │
│ Escalations  │ Pending │ Approved │ Rejected │ History  │      │
│ Departments  │  (3)    │   (12)   │   (2)    │  (47)    │      │
│ Models       └─────────┴──────────┴──────────┴──────────┘      │
│ Scheduler                                                    │
│ KPIs                                                         │
│                   ┌──────────────────────────────────────┐     │
│                   │ FILTERS: [All Tiers ▾] [All Agents ▾]│     │
│                   │         [Sort: Expiry ▾]              │     │
│                   └──────────────────────────────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ ⚠ T3 │ apr-9c1d2e          │ devops-engineer  │ 22m    │ │
│  │       │ bash: docker compose │ 1/2 approvals    │ ⚠     │ │
│  │       │ Risk: █████░░░░░ 55  │                  │       │ │
│  │       ├──────────────────────────────────────────────────┤ │
│  │       │ Human Operator ✓  14:32  "Staging env, safe"    │ │
│  │       │                                                  │ │
│  │       │ [✓ Approve]  [✗ Reject]  [View Details]         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ T2 │ apr-7b3e9f          │ lead-backend       │ 47m    │ │
│  │    │ edit: src/api/routes │ 0/1 approvals      │        │ │
│  │    │ Risk: ██░░░░░░░░ 25  │                    │        │ │
│  │    │                      │ [✓ Approve] [✗ Reject]      │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 🔒 T4 │ apr-3a8f5c          │ cpo              │ 23h   │ │
│  │       │ deploy_agent:       │ CEO required      │       │ │
│  │       │ financial-analyst   │                    │       │ │
│  │       │ Risk: █████████░ 90 │ [✓ CEO Approve]  │       │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 2. Tab Views

### Pending Tab (Default)

Shows all unresolved approval requests sorted by expiry (soonest first).

Each card contains:
- **Tier badge**: `[T0]` through `[T4]` with color coding
- **Request ID**: monospace, copyable
- **Agent**: who requested
- **Action + description**: human-readable summary
- **Risk score**: visual bar + numeric
- **Expiry countdown**: live-updating, warning at 25% remaining
- **Approval signatures**: for T3, shows `1/2` with checkmarks per signer
- **Action buttons**: Approve / Reject / View Details

### Approved Tab

Shows resolved requests with status `approved`. Sorted by `responded_at` descending.

Each row shows:
- Tier badge, request ID, agent, action, who approved, when, notes

### Rejected Tab

Shows resolved requests with status `rejected`. Sorted by `responded_at` descending.

Each row shows:
- Tier badge, request ID, agent, action, who rejected, when, **rejection reason** (prominent)

### History Tab

Full audit log of all requests (all statuses). Filterable by:
- Tier
- Agent
- Date range
- Status
- Action category

Exportable as CSV.

## 3. Approval Action Flow

### Approve Button

Clicking "Approve" opens an inline form:

```
┌──────────────────────────────────────────────┐
│  Approve apr-7b3e9f                          │
│                                              │
│  Identity: [human-ceo ▾]                     │
│  Notes (optional):                            │
│  ┌────────────────────────────────────────┐  │
│  │                                        │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  [Cancel]              [Confirm Approval]    │
└──────────────────────────────────────────────┘
```

**Validation rules:**
- T4: Identity dropdown only shows CEO identity. Non-CEO identities are grayed out with tooltip "Tier 4 requires CEO approval"
- T3: If the selected identity already signed, show error: "This identity has already signed. Tier 3 requires two distinct approvers."
- Notes are optional for approval but recommended

### Reject Button

Clicking "Reject" opens an inline form. **Rejection reason is required:**

```
┌──────────────────────────────────────────────┐
│  Reject apr-7b3e9f                           │
│                                              │
│  Identity: [human-ceo ▾]                     │
│  Reason (required):                           │
│  ┌────────────────────────────────────────┐  │
│  │                                        │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  [Cancel]              [Confirm Rejection]   │
└──────────────────────────────────────────────┘
```

**Validation rules:**
- Reason field is required; "Confirm Rejection" button is disabled until reason is non-empty
- Identity follows same tier rules as approval

### View Details

Expands the card to show full request context:

```
┌──────────────────────────────────────────────────────────────┐
│  apr-7b3e9f — Tier 2 Single Approve                [×]     │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  Request Details                                             │
│  ─────────────────                                           │
│  Agent:        lead-backend                                  │
│  Task:         task-4f2a1b                                   │
│  Action:       edit                                          │
│  Category:     code_change                                   │
│  Risk Score:   25/100                                        │
│  Description:  Write 1,247 chars to src/api/routes.py       │
│  Requested:    2026-07-19 14:30:00 UTC                       │
│  Expires:      2026-07-19 15:30:00 UTC                       │
│  Escalated:    (not escalated)                               │
│                                                              │
│  Signatures                                                  │
│  ──────────                                                  │
│  (none yet)                                                  │
│                                                              │
│  Task Context                                                │
│  ────────────                                                │
│  Status:    in_progress                                      │
│  Priority:  high                                             │
│  Created:   2026-07-19 13:45:00 UTC                          │
│                                                              │
│  [✓ Approve]  [✗ Reject]                                    │
└──────────────────────────────────────────────────────────────┘
```

## 4. Tier Badge Design

| Tier | Badge | Color | Icon |
|------|-------|-------|------|
| T0 | `T0 Auto` | Gray `#6b7280` | — |
| T1 | `T1 Notify` | Blue `#3b82f6` | `ℹ` |
| T2 | `T2 Single` | Yellow `#eab308` | `⏳` |
| T3 | `T3 Dual` | Orange `#f97316` | `⚠` |
| T4 | `T4 CEO` | Red `#ef4444` | `🔒` |

Expiry warning overlay: when < 25% time remaining, badge pulses with `animate-pulse` and shows countdown.

## 5. Real-Time Updates via WebSocket

### Connection

```
WS /ws/approvals
```

### Message Types

**Server → Client:**

```json
{
  "type": "approval.created",
  "payload": {
    "id": "apr-7b3e9f",
    "tier": "tier_2_single",
    "agent_id": "lead-backend",
    "action": "edit",
    "description": "Write 1,247 chars to src/api/routes.py",
    "risk_score": 25,
    "expires_at": "2026-07-19T15:30:00Z"
  }
}
```

```json
{
  "type": "approval.signed",
  "payload": {
    "id": "apr-9c1d2e",
    "approver": "human-operator",
    "decision": "approved",
    "current_sigs": 1,
    "required_sigs": 2
  }
}
```

```json
{
  "type": "approval.resolved",
  "payload": {
    "id": "apr-7b3e9f",
    "status": "approved",
    "responded_at": "2026-07-19T14:55:00Z"
  }
}
```

```json
{
  "type": "approval.escalated",
  "payload": {
    "original_id": "apr-7b3e9f",
    "new_id": "apr-b2c4d6",
    "from_tier": "tier_2_single",
    "to_tier": "tier_3_dual",
    "reason": "timeout"
  }
}
```

```json
{
  "type": "approval.ticking",
  "payload": {
    "id": "apr-9c1d2e",
    "remaining_seconds": 1320,
    "pct_remaining": 73
  }
}
```

**Client → Server:**

```json
{
  "type": "approval.approve",
  "payload": {
    "id": "apr-7b3e9f",
    "approved_by": "human-ceo",
    "notes": "Looks good"
  }
}
```

```json
{
  "type": "approval.reject",
  "payload": {
    "id": "apr-7b3e9f",
    "rejected_by": "human-ceo",
    "notes": "Wrong file path"
  }
}
```

### Client Behavior

1. On connect: subscribe to `/ws/approvals`
2. On `approval.created`: prepend card to Pending tab, increment badge count, play subtle chime for T3/T4
3. On `approval.signed`: update signature count on the card, show signer name inline
4. On `approval.resolved`: animate card moving to Approved or Rejected tab
5. On `approval.escalated`: remove old card, insert new card with escalated tier badge
6. On `approval.ticking`: update countdown display, trigger warning style at < 25%
7. On disconnect: show "Connection lost — retrying..." banner, auto-reconnect with exponential backoff

## 6. REST API Extensions

New endpoints added to `dashboard/api.py`:

```
GET  /api/approvals                    — list all (with query params)
GET  /api/approvals/history            — full audit log (paginated)
GET  /api/approvals/{id}               — single request detail
POST /api/approvals/{id}/approve       — approve (body: ApprovalDecision)
POST /api/approvals/{id}/reject        — reject (body: ApprovalDecision with required reason)
GET  /api/approvals/tiers              — tier definitions
GET  /ws/approvals                     — WebSocket stream
```

### Query Parameters for `GET /api/approvals`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | string | `pending` | Filter by status |
| `tier` | string | all | Filter by tier (`tier_2_single`, etc.) |
| `agent` | string | all | Filter by requesting agent |
| `category` | string | all | Filter by action category |
| `sort` | string | `expires_at` | Sort field |
| `order` | string | `asc` | Sort direction |
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Items per page |

### Response Model Extensions

```python
class ApprovalItem(BaseModel):
    # Existing fields
    id: str
    task_id: str
    agent_id: str
    action: str
    description: str
    status: str
    requested_at: Optional[str]
    expires_at: Optional[str]

    # New fields
    tier: str = "tier_2_single"
    tier_label: str = "Single Approve"
    risk_score: int = 0
    action_category: str = ""
    approvals: list[ApprovalSignatureItem] = Field(default_factory=list)
    required_approvals: int = 1
    escalated_from: Optional[str] = None
    responded_at: Optional[str] = None

class ApprovalSignatureItem(BaseModel):
    approver_id: str
    decision: str
    decided_at: str
    notes: Optional[str] = None

class ApprovalDecision(BaseModel):
    approved_by: str = "human-ceo"
    notes: Optional[str] = None
    # Rejection requires reason — validated at endpoint level
```

## 7. Dashboard KPI Changes

The existing `KPIs` model adds tier breakdown:

```python
class KPIs(BaseModel):
    # ... existing fields ...
    pending_approvals: int = 0
    pending_approvals_t2: int = 0
    pending_approvals_t3: int = 0
    pending_approvals_t4: int = 0
    approvals_today: int = 0
    avg_approval_time_minutes: float = 0
    escalated_today: int = 0
```

## 8. Keyboard Shortcuts

| Key | Action | Context |
|-----|--------|---------|
| `a` | Approve selected | Pending tab focused |
| `r` | Reject selected | Pending tab focused |
| `Enter` | Open detail view | Card focused |
| `Escape` | Close detail / cancel action | Any |
| `j` / `k` | Navigate up/down cards | Pending tab |
| `1`-`4` | Switch tabs | Any |
| `f` | Focus filter bar | Any |
| `/` | Search | Any |

## 9. Empty States

### No Pending Approvals

```
┌──────────────────────────────────────────────┐
│                                              │
│              ✓                               │
│                                              │
│        All clear!                            │
│   No pending approvals at the moment.        │
│                                              │
│   Approvals will appear here when agents     │
│   request permission for Tier 2+ actions.    │
│                                              │
└──────────────────────────────────────────────┘
```

### No History

```
┌──────────────────────────────────────────────┐
│                                              │
│              📋                              │
│                                              │
│      No approval history yet.                │
│                                              │
│   Completed approvals will appear here       │
│   with full audit details.                   │
│                                              │
└──────────────────────────────────────────────┘
```
