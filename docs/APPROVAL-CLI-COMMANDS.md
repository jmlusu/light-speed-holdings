# CLI Approval Commands Specification

> Phase 5 — Enhanced `ai-company orchestrator approval` subcommands

## 1. Command Tree

```
ai-company orchestrator approval
├── list                  Show pending approvals with tier badges
├── approve <id>          Approve a request (optional notes)
├── reject <id>           Reject a request (required reason)
├── show <id>             Show full details of a request
├── history               Show past approvals (paginated)
├── tiers                 Show tier definitions
├── stats                 Show approval statistics
└── watch                 Live-updating pending approval monitor
```

## 2. Command Specifications

### `approval list`

Show all pending approval requests, sorted by expiry (soonest first).

**Usage:**
```bash
ai-company orchestrator approval list [OPTIONS]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--tier` | all | Filter by tier: `0`, `1`, `2`, `3`, `4` |
| `--agent` | all | Filter by requesting agent ID |
| `--category` | all | Filter by action category |
| `--sort` | `expiry` | Sort by: `expiry`, `risk`, `tier`, `requested` |
| `--limit` | 20 | Max rows to display |
| `--json` | false | Output as JSON (for scripting) |

**Output (default):**
```
  Pending Approvals (3)                     Sorted by: expiry
  ═══════════════════════════════════════════════════════════════

  [T3] apr-9c1d2e                           ⏱ 22m remaining ⚠
    Agent:      devops-engineer
    Action:     bash — docker compose up -d
    Category:   infrastructure
    Risk:       █████░░░░░ 55/100
    Signatures: 1/2 (human-operator ✓)

  [T2] apr-7b3e9f                           ⏱ 47m remaining
    Agent:      lead-backend
    Action:     edit — src/api/routes.py
    Category:   code_change
    Risk:       ██░░░░░░░░ 25/100
    Signatures: 0/1

  [T4] apr-3a8f5c                           ⏱ 23h 10m remaining
    Agent:      cpo
    Action:     deploy_agent — financial-analyst
    Category:   organizational
    Risk:       █████████░ 90/100
    Signatures: CEO required

  ─────────────────────────────────────────────────────────────
  Run: ai-company orchestrator approval approve <id>
       ai-company orchestrator approval reject <id>
       ai-company orchestrator approval show <id>
```

**Output (`--json`):**
```json
[
  {
    "id": "apr-9c1d2e",
    "tier": "tier_3_dual",
    "tier_label": "Dual Approve",
    "agent_id": "devops-engineer",
    "action": "bash",
    "action_description": "docker compose up -d",
    "category": "infrastructure",
    "risk_score": 55,
    "status": "pending",
    "approvals": [
      {"approver": "human-operator", "decision": "approved", "at": "2026-07-19T14:32:00Z"}
    ],
    "required_approvals": 2,
    "expires_at": "2026-07-19T14:52:00Z",
    "remaining_seconds": 1320
  }
]
```

**Filtered example (`--tier 3`):**
```
  Pending Approvals — Tier 3 (1)
  ═══════════════════════════════════════════════════════════════

  [T3] apr-9c1d2e                           ⏱ 22m remaining ⚠
    Agent:      devops-engineer
    Action:     bash — docker compose up -d
    Risk:       █████░░░░░ 55/100
    Signatures: 1/2 (human-operator ✓)
```

---

### `approval approve <id>`

Approve a pending request. For Tier 3, records one of two required signatures.

**Usage:**
```bash
ai-company orchestrator approval approve <id> [OPTIONS]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--approved-by` | `human-operator` | Identity of approver |
| `--notes` | none | Optional approval notes |

**Output — Tier 2 (single approval, success):**
```
✓ Request apr-7b3e9f APPROVED
  Approved by: human-operator
  Notes:       Looks good, tested locally
  Agent lead-backend may now proceed with: edit
```

**Output — Tier 3 (first signature):**
```
✓ Signature recorded for apr-9c1d2e
  Signed by:  human-operator
  Notes:      Staging env, safe to proceed
  Status:     1 of 2 approvals — awaiting second approver
```

**Output — Tier 3 (second signature, completes):**
```
✓ Request apr-9c1d2e APPROVED (2/2 signatures)
  Signatures: human-operator, cpo
  Agent devops-engineer may now proceed with: bash
```

**Output — Tier 4 (CEO approval):**
```
✓ CEO approval recorded for apr-3a8f5c
  Approved by: human-ceo
  Notes:       Approved — budget allocated in Q3 plan
  Agent cpo may now proceed with: deploy_agent
```

**Error — self-approval on Tier 3:**
```
✗ DENIED: human-operator already signed this request.
  Tier 3 requires two DISTINCT approvers.
  Existing signatures: human-operator (approved)
```

**Error — non-CEO on Tier 4:**
```
✗ DENIED: Tier 4 requires CEO-only approval.
  Only human-ceo may approve this request.
  Your identity: human-operator
```

**Error — already resolved:**
```
✗ Request apr-7b3e9f not found or already processed.
  Current status: approved
  Resolved by: human-operator at 2026-07-19 14:55 UTC
```

**Error — expired:**
```
✗ Request apr-7b3e9f has expired and was escalated.
  Escalated to: apr-b2c4d6 (Tier 3)
  Approve that request instead.
```

---

### `approval reject <id>`

Reject a pending request. **Reason is required.**

**Usage:**
```bash
ai-company orchestrator approval reject <id> [OPTIONS]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--rejected-by` | `human-operator` | Identity of rejector |
| `--reason` | *required* | Rejection reason (mandatory) |

**Output — success:**
```
✗ Request apr-7b3e9f REJECTED
  Rejected by: human-operator
  Reason:      Wrong file — should edit src/api/handler.py instead
  Agent lead-backend has been notified.
```

**Error — no reason provided:**
```
✗ Rejection requires a reason.
  Usage: ai-company orchestrator approval reject <id> --reason "your reason"
```

**Error — Tier 4 non-CEO:**
```
✗ DENIED: Tier 4 requires CEO-only rejection.
  Only human-ceo may reject this request.
```

---

### `approval show <id>`

Display full details for a single approval request.

**Usage:**
```bash
ai-company orchestrator approval show <id>
```

**Output:**
```
  Approval Request: apr-9c1d2e
  ═══════════════════════════════════════════════════════════════

  Tier:           T3 — Dual Approve
  Status:         PENDING (1/2 signatures)
  Category:       infrastructure
  Risk Score:     55/100

  Agent:          devops-engineer
  Task:           task-8e4f2a
  Action:         bash
  Description:    Execute: docker compose up -d

  Requested:      2026-07-19 14:30:00 UTC
  Expires:        2026-07-19 14:52:00 UTC
  Time remaining: 22 minutes

  Escalated from: (none)

  ─────────────────────────────────────────────────────────────
  Signatures
  ─────────────────────────────────────────────────────────────

  1. human-operator              ✓ approved   14:32 UTC
     "Staging env, safe to proceed"

  2. (awaiting second approver)

  ─────────────────────────────────────────────────────────────
  Task Context
  ─────────────────────────────────────────────────────────────

  Status:    in_progress
  Priority:  high
  Created:   2026-07-19 13:45:00 UTC
  Sender:    cpo
```

---

### `approval history`

Show resolved approvals (approved, rejected, expired, escalated).

**Usage:**
```bash
ai-company orchestrator approval history [OPTIONS]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--status` | all | Filter: `approved`, `rejected`, `expired`, `escalated` |
| `--tier` | all | Filter by tier |
| `--agent` | all | Filter by requesting agent |
| `--limit` | 20 | Max rows |
| `--json` | false | JSON output |
| `--since` | 7d | Time window: `1h`, `24h`, `7d`, `30d`, `all` |

**Output:**
```
  Approval History (12 in last 7 days)          Showing: 1-10
  ═══════════════════════════════════════════════════════════════

  ✓  [T2] apr-a1b2c3  lead-backend       edit              2h ago
     Approved by: human-operator
     Notes: "Tested locally, LGTM"

  ✓  [T3] apr-d4e5f6  devops-engineer    bash              5h ago
     Approved by: human-operator, cpo
     Notes: "Post-deploy monitoring active"

  ✗  [T2] apr-g7h8i9  marketing-lead     budget_spend      1d ago
     Rejected by: cpo
     Reason: "Exceeds quarterly budget cap — resubmit with CFO approval"

  ⏰ [T3] apr-j0k1l2  lead-frontend      delete            2d ago
     Escalated to: apr-m3n4o5 (T4)
     Reason: timeout (0/2 signatures)

  🔒 [T4] apr-p6q7r8  cpo                deploy_agent     3d ago
     Approved by: human-ceo
     Notes: "Approved per Q3 roadmap"

  ─────────────────────────────────────────────────────────────
  Page 1 of 2    [← Prev] [Next →]
```

---

### `approval tiers`

Display the tier definitions with their rules.

**Usage:**
```bash
ai-company orchestrator approval tiers
```

**Output:**
```
  Approval Tiers
  ═══════════════════════════════════════════════════════════════

  T0  Auto
      Gate:      None (instant execution)
      Approvers: —
      Timeout:   —
      Examples:  read, list, grep, recall, status updates

  T1  Notify
      Gate:      Log only (no blocking)
      Approvers: —
      Timeout:   —
      Examples:  store_memory, routine task completion

  T2  Single Approve
      Gate:      One human approval
      Approvers: Any operator
      Timeout:   60 minutes → escalates to T3
      Examples:  edit code, budget < $100, config changes

  T3  Dual Approve
      Gate:      Two distinct human approvals
      Approvers: Any 2 operators
      Timeout:   30 minutes → escalates to CEO
      Examples:  bash execution, delete data, spend > $500

  T4  CEO Only
      Gate:      CEO explicit approval
      Approvers: CEO only (no substitutes)
      Timeout:   24 hours → board notification
      Examples:  constitutional change, new agent deployment

  Escalation Path: T2 → T3 → T4 → Board
```

---

### `approval stats`

Show approval statistics for a time window.

**Usage:**
```bash
ai-company orchestrator approval stats [OPTIONS]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--since` | `30d` | Time window |
| `--json` | false | JSON output |

**Output:**
```
  Approval Statistics (last 30 days)
  ═══════════════════════════════════════════════════════════════

  Total Requests:     47
  ├── Approved:       38 (81%)
  ├── Rejected:        5 (11%)
  ├── Expired:         2 (4%)
  └── Escalated:       2 (4%)

  By Tier:
  T0  Auto:           — (no approvals tracked)
  T1  Notify:         — (no approvals tracked)
  T2  Single:        24 approved, 3 rejected, 1 escalated
  T3  Dual:          12 approved, 2 rejected, 1 escalated
  T4  CEO Only:       2 approved, 0 rejected, 0 escalated

  Average Approval Time:
  T2:  12.3 minutes
  T3:  8.7 minutes (per signature)
  T4:  4.2 hours

  Top Approvers:
  1. human-operator:  32 approvals
  2. cpo:             18 approvals
  3. human-ceo:        2 approvals

  Escalation Rate:   4.3% (2 of 47)
  Timeout Rate:      4.3% (2 of 47)
```

---

### `approval watch`

Live-updating terminal monitor for pending approvals. Uses ANSI escape codes for real-time refresh.

**Usage:**
```bash
ai-company orchestrator approval watch [OPTIONS]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--interval` | 5 | Refresh interval in seconds |
| `--tier` | all | Filter by tier |

**Output (refreshes in place):**
```
  ╔══════════════════════════════════════════════════════════════╗
  ║  APPROVAL MONITOR                          Last: 14:52:03  ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                              ║
  ║  ⚠ [T3] apr-9c1d2e  devops-engineer  bash      ⏱ 22m 1/2  ║
  ║    └─ docker compose up -d                                   ║
  ║                                                              ║
  ║    [T2] apr-7b3e9f  lead-backend     edit       ⏱ 47m 0/1  ║
  ║      └─ Write 1,247 chars to src/api/routes.py              ║
  ║                                                              ║
  ║    🔒 [T4] apr-3a8f5c  cpo           deploy     ⏱ 23h CEO  ║
  ║        └─ Deploy new specialist agent: financial-analyst     ║
  ║                                                              ║
  ╠══════════════════════════════════════════════════════════════╣
  ║  Press q to exit · a <id> to approve · r <id> to reject     ║
  ╚══════════════════════════════════════════════════════════════╝
```

In watch mode, the user can press:
- `a` then paste an ID to quick-approve
- `r` then paste an ID to quick-reject
- `d` then paste an ID to show detail
- `q` to exit

## 3. JSON Output Contract

All commands support `--json` for machine-readable output. The JSON schema:

```json
{
  "command": "approval list",
  "timestamp": "2026-07-19T14:52:03Z",
  "count": 3,
  "items": [
    {
      "id": "apr-9c1d2e",
      "tier": "tier_3_dual",
      "tier_label": "Dual Approve",
      "status": "pending",
      "agent_id": "devops-engineer",
      "task_id": "task-8e4f2a",
      "action": "bash",
      "description": "Execute: docker compose up -d",
      "category": "infrastructure",
      "risk_score": 55,
      "requested_at": "2026-07-19T14:30:00Z",
      "expires_at": "2026-07-19T14:52:00Z",
      "remaining_seconds": 1320,
      "approvals": [
        {
          "approver_id": "human-operator",
          "decision": "approved",
          "decided_at": "2026-07-19T14:32:00Z",
          "notes": "Staging env, safe to proceed"
        }
      ],
      "required_approvals": 2,
      "escalated_from": null
    }
  ]
}
```

## 4. Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Request not found or already processed |
| 2 | Permission denied (wrong tier, non-CEO on T4) |
| 3 | Validation error (missing required args like `--reason`) |
| 4 | No pending requests (for `list` when empty) |

## 5. Implementation Notes

### Current State to Change

| File | Current | Target |
|------|---------|--------|
| `orchestrator/approval.py` | Flat `ApprovalRequest` | Add `tier`, `approvals[]`, `required_approvals`, `escalation_path` fields |
| `cli/orchestrator.py` | `pending`, `approve`, `reject` | Add `list`, `show`, `history`, `tiers`, `stats`, `watch` |
| `dashboard/models.py` | `ApprovalItem` (flat) | Add tier, signatures, escalation fields |
| `dashboard/api.py` | Basic CRUD | Add `/history`, `/tiers`, `/stats`, WebSocket |
| `executor/hitl_gate.py` | Single-tier poll | Tier-aware classification + escalation re-attach |

### Naming Convention

The current `pending` command is renamed to `list` for consistency with `scheduler list` and `escalation list`. The old `pending` name is kept as an alias for backward compatibility.

```python
@approval_app.command("list")
@approval_app.command("pending", hidden=True)  # alias
def approval_list(...):
    ...
```

### Color Coding (Terminal)

Tier badges use ANSI colors. When `NO_COLOR` env var is set or output is piped, fall back to plain text.

| Tier | ANSI Code | Fallback |
|------|-----------|----------|
| T0 | `\033[90m` (dim) | `[T0]` |
| T1 | `\033[34m` (blue) | `[T1]` |
| T2 | `\033[33m` (yellow) | `[T2]` |
| T3 | `\033[31m` (red) | `[T3]` |
| T4 | `\033[35m` (magenta) + bold | `[T4]` |
| Warning | `\033[33m` (yellow) | `⚠` |
| Success | `\033[32m` (green) | `✓` |
| Failure | `\033[31m` (red) | `✗` |

### Backward Compatibility

- `ai-company orchestrator approval pending` → alias for `list`
- `ai-company orchestrator approval approve <id>` → unchanged interface
- `ai-company orchestrator approval reject <id>` → unchanged interface (note: `--reason` becomes required; old invocations without `--reason` will error with exit code 3 and a helpful message)
