# Approval Flow UX Specification

> Phase 5 — Approval Gate Hardening with Action Tiers, Two-Person Rules, and Timeout Escalation

## 1. Design Principles

| Principle | Rationale |
|-----------|-----------|
| **Friction scales with risk** | Tier 0-1 are invisible; Tier 3-4 force deliberate human action |
| **No silent failures** | Every timeout produces a visible escalation, never a silent drop |
| **Auditability by default** | Every approval/rejection is logged with who, when, and why |
| **Timeout is never final** | A timeout escalates upward — it never auto-approves or auto-deletes |

## 2. Tier Definitions

| Tier | Name | Gate Type | Approvers | Timeout | Example Actions |
|------|------|-----------|-----------|---------|-----------------|
| 0 | Auto | None | — | — | `read`, `list`, `grep`, `recall` |
| 1 | Notify | Log only | — | — | `store_memory`, routine task completion, status updates |
| 2 | Single Approve | One human | Any operator | 60 min → escalate to Tier 3 approver | `edit` code, budget < $100, config changes |
| 3 | Dual Approve | Two humans | Any 2 operators | 30 min → escalate to CEO | `bash` execution, `delete` data, spend > $500, production deploy |
| 4 | CEO Only | CEO explicit | CEO only | 24 hr → board notification | Constitutional change, new agent deployment, org restructure |

## 3. Data Model Extensions

The existing `ApprovalRequest` model gains new fields:

```python
class ApprovalTier(str, Enum):
    TIER_0_AUTO = "tier_0_auto"
    TIER_1_NOTIFY = "tier_1_notify"
    TIER_2_SINGLE = "tier_2_single"
    TIER_3_DUAL = "tier_3_dual"
    TIER_4_CEO = "tier_4_ceo"

class ApprovalRequest(BaseModel):
    # Existing fields (unchanged)
    id: str
    task_id: str
    agent_id: str
    action: str
    description: str
    status: ApprovalStatus  # pending | approved | rejected | expired | escalated
    requested_at: datetime
    responded_at: Optional[datetime]
    response_by: Optional[str]
    notes: Optional[str]
    expires_at: Optional[datetime]

    # New fields for Phase 5
    tier: ApprovalTier = ApprovalTier.TIER_2_SINGLE
    approvals: list[ApprovalSignature] = Field(default_factory=list)
    required_approvals: int = 1
    escalation_path: list[str] = Field(default_factory=list)
    escalated_from: Optional[str] = None
    action_category: str = ""     # e.g. "code_change", "financial", "infrastructure"
    risk_score: int = 0           # 0-100, computed by decision engine

class ApprovalSignature(BaseModel):
    approver_id: str
    decision: str    # "approved" | "rejected"
    decided_at: datetime
    notes: Optional[str] = None
```

### Status Flow

```
                    ┌──────────┐
                    │ PENDING  │
                    └────┬─────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
        Approved     Rejected     Expired
     (1 sig for      │            │
      Tier 2)        │        Escalate
     ┌───────┐       │     (to next tier
     │ NEED_ │       │      approver)
     │ SECOND│       │            │
     └───┬───┘       │       Escalated
         │           │            │
    Approved     (terminal)  (re-enters
   (2 sigs)                 PENDING at
                            higher tier)
```

New status: `escalated` — the request was not resolved within its timeout and has been forwarded to the next escalation target.

## 4. Tier-by-Tier UX Design

### Tier 0 — Auto (No Approval Needed)

**Agent sees:** Nothing. Action executes immediately.

**Operator sees:** Nothing in the approval queue. The action appears only in the task execution log.

**On timeout:** N/A — no timeout applies.

**CLI output when invoked:**
```
(action executes silently, logged to task result)
```

---

### Tier 1 — Notify (Log Only)

**Agent sees:** The action executes. A notification entry is written to the approval log for audit purposes.

**Operator sees:** The action appears in the approval history as a `completed` entry with tier badge `[T1]`. It never blocks.

**On timeout:** N/A — no timeout applies.

**CLI output when invoked:**
```
✓ Memory stored (logged as T1-notify, id: mem-a3f2c1)
```

---

### Tier 2 — Single Approve (One Human)

**What the user (agent requesting approval) sees:**

```
──────────────────────────────────────────────
⏳ APPROVAL REQUIRED — Tier 2 (Single)
──────────────────────────────────────────────
  Request ID:   apr-7b3e9f
  Agent:        lead-backend
  Action:       edit
  Category:     code_change
  Risk Score:   25/100
  Description:  Write 1,247 chars to src/api/routes.py
  Task:         task-4f2a1b
  Expires in:   60 minutes (2026-07-19 15:30 UTC)
──────────────────────────────────────────────
  Waiting for approval...
  Run: ai-company orchestrator approval approve apr-7b3e9f
──────────────────────────────────────────────
```

**What the approver sees (CLI):**

```
$ ai-company orchestrator approval pending

  Pending Approvals (3)
  ════════════════════════════════════════════

  [T2] apr-7b3e9f                      expires in 47m
    Agent:   lead-backend
    Action:  edit
    Desc:    Write 1,247 chars to src/api/routes.py
    Risk:    ██░░░░░░░░ 25/100

  [T3] apr-9c1d2e                      expires in 22m ⚠️
    Agent:   devops-engineer
    Action:  bash
    Desc:    Execute: docker compose up -d
    Risk:    █████░░░░░ 55/100

  [T4] apr-3a8f5c                      expires in 23h 10m
    Agent:   cpo
    Action:  deploy_agent
    Desc:    Deploy new specialist agent: financial-analyst
    Risk:    █████████░ 90/100
```

**Approval flow:**

```bash
# Approve with optional notes
$ ai-company orchestrator approval approve apr-7b3e9f \
    --approved-by human-operator \
    --notes "Looks good, tested locally"

✓ Request apr-7b3e9f APPROVED by human-operator
  Agent lead-backend may now proceed with: edit
```

**Rejection flow:**

```bash
$ ai-company orchestrator approval reject apr-7b3e9f \
    --rejected-by human-operator \
    --notes "Wrong file — should edit src/api/handler.py instead"

✗ Request apr-7b3e9f REJECTED by human-operator
  Reason: Wrong file — should edit src/api/handler.py instead
  Agent lead-backend has been notified.
```

**On timeout (60 min):**

```
⚠ TIMEOUT — Tier 2 request apr-7b3e9f expired
  Escalating to Tier 3 approvers: [human-ceo, cpo]
  Agent lead-backend task-4f2a1b remains blocked.
```

The request status changes to `escalated`, and a new request is created at Tier 3 with `escalated_from` pointing to the original. The original agent's poll loop detects the status change and blocks until the new request resolves.

---

### Tier 3 — Dual Approve (Two Humans)

**What the user (agent) sees:**

```
──────────────────────────────────────────────
⏳ APPROVAL REQUIRED — Tier 3 (Dual)
──────────────────────────────────────────────
  Request ID:    apr-9c1d2e
  Agent:         devops-engineer
  Action:        bash
  Category:      infrastructure
  Risk Score:    55/100
  Description:   Execute: docker compose up -d
  Task:          task-8e4f2a
  Approvals:     0 of 2 required
  Expires in:    30 minutes (2026-07-19 15:00 UTC)
──────────────────────────────────────────────
  Requires TWO approvals before execution.
  Run: ai-company orchestrator approval approve apr-9c1d2e
──────────────────────────────────────────────
```

**What the approver sees:**

```
$ ai-company orchestrator approval pending

  Pending Approvals (1)
  ════════════════════════════════════════════

  [T3] apr-9c1d2e                      expires in 22m ⚠️
    Agent:   devops-engineer
    Action:  bash
    Desc:    Execute: docker compose up -d
    Risk:    █████░░░░░ 55/100
    Sigs:    0/2 approvals
```

**First approval:**

```bash
$ ai-company orchestrator approval approve apr-9c1d2e \
    --approved-by human-operator \
    --notes "Staging env, safe to proceed"

✓ Signature recorded for apr-9c1d2e by human-operator
  Status: 1 of 2 approvals — awaiting second approver
```

**Second approval (different person):**

```bash
$ ai-company orchestrator approval approve apr-9c1d2e \
    --approved-by cpo \
    --notes "Confirmed — I'll monitor post-deploy"

✓ Request apr-9c1d2e APPROVED (2/2 signatures)
  Approvals: human-operator, cpo
  Agent devops-engineer may now proceed with: bash
```

**Self-approval prevention:**

```bash
$ ai-company orchestrator approval approve apr-9c1d2e \
    --approved-by human-operator \
    --notes "Also approving as second"

✗ DENIED: human-operator already signed this request.
  Tier 3 requires two DISTINCT approvers.
```

**On timeout (30 min):**

```
⚠ TIMEOUT — Tier 3 request apr-9c1d2e expired (1/2 signatures)
  Escalating to CEO: human-ceo
  Agent devops-engineer task-8e4f2a remains blocked.
```

---

### Tier 4 — CEO Only (Human CEO Explicit)

**What the user (agent) sees:**

```
──────────────────────────────────────────────
🔒 APPROVAL REQUIRED — Tier 4 (CEO Only)
──────────────────────────────────────────────
  Request ID:    apr-3a8f5c
  Agent:         cpo
  Action:        deploy_agent
  Category:      organizational
  Risk Score:    90/100
  Description:   Deploy new specialist agent: financial-analyst
  Task:          task-2c7e4a
  Approvals:     CEO required
  Expires in:    24 hours (2026-07-20 14:30 UTC)
──────────────────────────────────────────────
  This action requires explicit CEO authorization.
  No other approver may substitute.
──────────────────────────────────────────────
```

**What the CEO sees:**

```
$ ai-company orchestrator approval pending

  Pending Approvals (1)
  ════════════════════════════════════════════

  [T4] apr-3a8f5c                      expires in 23h 10m
    Agent:   cpo
    Action:  deploy_agent
    Desc:    Deploy new specialist agent: financial-analyst
    Risk:    █████████░ 90/100
    ⚠ This requires YOUR approval only.
```

**CEO approval:**

```bash
$ ai-company orchestrator approval approve apr-3a8f5c \
    --approved-by human-ceo \
    --notes "Approved — budget allocated in Q3 plan"

✓ CEO approval recorded for apr-3a8f5c
  Agent cpo may now proceed with: deploy_agent
```

**Non-CEO attempting approval:**

```bash
$ ai-company orchestrator approval approve apr-3a8f5c \
    --approved-by human-operator \
    --notes "I'll approve this"

✗ DENIED: Tier 4 requires CEO-only approval.
  Only human-ceo may approve this request.
```

**On timeout (24 hr):**

```
⚠ TIMEOUT — Tier 4 request apr-3a8f5c expired without CEO approval
  Board notification sent.
  Agent cpo task-2c7e4a BLOCKED until CEO responds.
  Request re-surfaced in CEO's approval queue with ⏰ EXPIRED badge.
```

Tier 4 never auto-resolves. It remains in the queue with an `[EXPIRED]` badge until the CEO explicitly acts on it.

## 5. Escalation Path Design

When a tier times out, the escalation follows this path:

```
Tier 0 ─── (no escalation) ───
Tier 1 ─── (no escalation) ───
Tier 2 ──→ Tier 3 approvers   (timeout: 60 min)
Tier 3 ──→ CEO                (timeout: 30 min)
Tier 4 ──→ Board notification  (timeout: 24 hr, but stays in CEO queue)
```

Escalation creates a **linked request**:
- `id`: new UUID
- `escalated_from`: original request ID
- `tier`: one level higher
- `required_approvals`: updated for the new tier
- Agent's poll loop continues on the new request

## 6. HITL Gate Integration

The existing `HITLGate.request_and_wait()` method updates to:

```python
def request_and_wait(self, task_id, agent_id, tool, args) -> bool:
    tier = classify_tool_tier(tool, args)  # maps tool+args to ApprovalTier
    if tier in (ApprovalTier.TIER_0_AUTO, ApprovalTier.TIER_1_NOTIFY):
        return True  # auto-approve or just log

    request = self.gate.request_approval(
        ...,
        tier=tier,
        required_approvals=2 if tier == ApprovalTier.TIER_3_DUAL else 1,
        escalation_path=ESCALATION_PATH[tier],
    )

    # Poll with tier-appropriate timeout
    timeout = TIER_TIMEOUTS[tier]
    deadline = datetime.now() + timedelta(minutes=timeout)
    while datetime.now() < deadline:
        req = self.gate.get_request(request.id)
        if req and req.status != ApprovalStatus.PENDING:
            return req.status == ApprovalStatus.APPROVED
        # Check for escalation (new request replacing this one)
        if req and req.status == ApprovalStatus.ESCALATED:
            # Re-attach to the new escalated request
            request = self.gate.get_request(req.escalated_to)
            deadline = datetime.now() + timedelta(minutes=TIER_TIMEOUTS[request.tier])
        time.sleep(self.poll_interval)

    return False
```

### Tool-to-Tier Mapping

| Tool | Default Tier | Override Condition |
|------|-------------|-------------------|
| `read` | T0 | — |
| `grep` | T0 | — |
| `list` | T0 | — |
| `write` | T2 | T3 if path in `/etc/` or production dirs |
| `execute` (bash) | T3 | T2 if command is in allowlist |
| `code_interpreter` | T2 | T3 if code touches external APIs |
| `task` | T1 | T2 if budget > $100 |
| `delete` | T3 | T4 if deleting audit logs or configs |

## 7. Notification Design

### When an approval is requested

| Tier | CLI | Dashboard | Optional |
|------|-----|-----------|----------|
| T0 | — | — | — |
| T1 | Log line | Badge count +1 | — |
| T2 | Blocking message | Card in queue | WebSocket push |
| T3 | Blocking message + "2 approvals needed" | Card with sig count | WebSocket push |
| T4 | Blocking message + "CEO only" | Card with lock icon | WebSocket push + email hint |

### When timeout approaches

| Time remaining | Action |
|----------------|--------|
| 50% remaining | — |
| 25% remaining | Warning color in CLI (`⚠`) |
| Expired | Status set to `escalated`, new request created, agent notified |

## 8. Accessibility Notes

- All tier badges use text labels, not color alone: `[T2] Single Approve`
- Timeout warnings use `⚠` symbol alongside color
- Terminal output uses plain ASCII fallback when `NO_COLOR` env var is set
- Dashboard uses `aria-label` on all interactive approval elements
- Keyboard shortcuts: `a` to approve, `r` to reject, `Esc` to dismiss detail view
