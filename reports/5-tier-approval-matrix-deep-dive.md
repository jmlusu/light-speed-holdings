# Deep Dive Report: The 5-Tier Approval Matrix

**Prepared by:** Internal Communications Lead  
**Date:** July 23, 2026  
**Classification:** Internal — Leadership & Cross-Team Distribution  
**Audience:** Executive Team, Department Leads, All Agents

---

## Executive Summary

The **5-tier approval matrix** is the governance backbone of Light Speed Holdings' AI Company Builder. It is a risk-based classification system that determines whether an AI agent action can proceed autonomously or requires human approval — and at what level.

Every privileged action in our system — from reading a file to deploying to production to signing a contract — passes through this matrix. It ensures that autonomy is **graduated, not binary**: low-risk operations proceed instantly, while high-risk operations require one, two, or even CEO-level approvals before execution.

**Why it exists:** In an organization where 127 AI agents operate autonomously, unchecked autonomy is a liability. The 5-tier matrix provides the architectural guardrails that make autonomous operation safe, auditable, and compliant — without creating unnecessary friction for routine work.

**Current status:** The system is fully implemented and integrated. The ToolRunner consults `classify_tool_action()` on every privileged tool call. The HITL gate is non-blocking. 1,205 tests pass. The approval CLI supports filtering, history, statistics, and a live watch monitor.

---

## The 5 Tiers

The matrix classifies every tool action into one of five tiers, defined in `src/ai_company/orchestrator/tier_rules.py`:

### Tier 0 — Auto-Approve (No Gate)

| Attribute | Value |
|-----------|-------|
| **Label** | Auto-Approve |
| **Required Approvers** | 0 |
| **Timeout** | None |
| **Notification** | None |
| **Examples** | `read`, `list`, `grep`, `glob`, `search`, `ping`, `view` |

**When it applies:** Read-only operations that carry no risk. An agent can read any file, search any codebase, or list any directory without human intervention. These operations cannot modify state, delete data, or execute commands.

**Design rationale:** Read operations are the foundation of agent capability. Requiring approval for reads would cripple agent productivity. The audit trail logs these actions for compliance, but no gate blocks them.

---

### Tier 1 — Notify (Log & Alert)

| Attribute | Value |
|-----------|-------|
| **Label** | Notify |
| **Required Approvers** | 0 |
| **Timeout** | None |
| **Notification** | Slack, Email |
| **Examples** | `delegate`, config writes, documentation updates, CHANGELOG edits |

**When it applies:** Low-risk write operations that modify non-critical files. Writing to `config/`, `.github/`, `docs/`, or updating markdown files triggers notification but not blocking approval. The action proceeds immediately, and humans are notified via Slack and email.

**Design rationale:** Some writes are inherently safe — updating a README, editing a changelog, or modifying a configuration file that gets validated on load. These don't need a human in the loop, but visibility matters. Notify-tier ensures humans stay informed without creating bottlenecks.

---

### Tier 2 — Single Approver (One Human Required)

| Attribute | Value |
|-----------|-------|
| **Label** | Single Approver |
| **Required Approvers** | 1 |
| **Timeout** | 4 hours |
| **Notification** | Slack, Email |
| **Examples** | Code changes (`src/`, `tests/`, `app/`), test execution, dependency updates |

**When it applies:** Code modifications, test execution, and changes to application logic. Any write to source code paths (`src/`, `tests/`, `app/`, `lib/`, `handler/`, `service/`, `routes/`, `api/`) requires one human to approve before execution.

**The seniority exception:** Executive agents (CEO, CTO, CFO, etc.) and lead-level agents can auto-approve Tier 2 actions based on their authority level. The matrix checks `SENIORITY_AUTO_APPROVE_TIER` to determine whether an agent's seniority allows bypass.

**Escalation path:** If no approver responds within 4 hours, the request escalates to Tier 3 (Two-Person Rule).

---

### Tier 3 — Two-Person Rule (Dual Approval)

| Attribute | Value |
|-----------|-------|
| **Label** | Two-Person Rule |
| **Required Approvers** | 2 (distinct individuals) |
| **Timeout** | 2 hours |
| **Notification** | Slack, Email, Pager |
| **Examples** | Production deployments, database changes, `terraform apply`, `docker push`, `kubectl apply` |

**When it applies:** High-risk operations that affect production systems, infrastructure, or data integrity. The "two-person rule" requires two **distinct** human approvers — self-approval is explicitly rejected by the system.

**What triggers Tier 3:**
- **Path-based:** Writes to `/production/`, `/prod/`, `deploy/`, `terraform/`, `k8s/`, `helm/`, `Dockerfile`, `Makefile`
- **Command-based:** `docker push`, `kubectl apply`, `terraform apply/destroy`, `helm upgrade`, `npm publish`, `pip install --upgrade`
- **Context-based:** Tasks with `risk_level: high` escalate from Tier 2 to Tier 3

**Escalation path:** If the two required approvals are not obtained within 2 hours, the request escalates to Tier 4 (CEO Only).

---

### Tier 4 — CEO Only (Final Authority)

| Attribute | Value |
|-----------|-------|
| **Label** | CEO Only |
| **Required Approvers** | 1 (CEO only — no substitutes) |
| **Timeout** | 1 hour (→ board notification) |
| **Notification** | Slack, Email, Pager, SMS |
| **Examples** | Constitutional changes, new agent deployments, financial transactions, security incidents, access to secrets |

**When it applies:** The most sensitive actions in the organization — those that affect legal standing, financial integrity, security posture, or organizational structure. Only the `human_ceo` agent can approve or reject these requests.

**What triggers Tier 4:**
- **Path-based:** Writes to `/secrets/`, `/.env`, `config/secrets.yaml`, `security/`, `audit/`, `legal/`, `compliance/`, or files containing `private_key`
- **Command-based:** `rm -rf`, `drop table`, `drop database`, `truncate table`, `sudo rm`, `shutdown`, `reboot`, `chmod 777`, `dd if=`, fork bombs, pipe-to-shell patterns
- **Context-based:** Tasks with `risk_level: critical` escalate to Tier 4 regardless of tool type

**Escalation path:** If the CEO does not respond within 1 hour, the system triggers a board notification — the highest-level alert in the organization.

---

## Organizational Context

### How the Matrix Fits Into Governance

The 5-tier approval matrix is not an isolated mechanism. It is one layer in a multi-layered governance architecture:

```
Board of Directors
    │
    ├── Board Directives (formal instructions → task conversion)
    │
    ├── Board Governance (charter, voting rules, decision authority)
    │
Human CEO
    │
    ├── Tier 4 Authority (CEO-only approvals)
    │
    ├── Executive Team (CTO, CFO, CMO, CHRO, CISO, CLO, CSO, CPO)
    │       │
    │       ├── Tier 3 Authority (dual approvals)
    │       ├── Tier 2 Authority (single approvals)
    │       │
    │       └── Specialist Agents (84+ across 17 departments)
    │               │
    │               ├── Tier 0-1 (autonomous operations)
    │               └── Tier 2+ (escalation required)
    │
    └── 5-Tier Approval Matrix (enforced at ToolRunner level)
            │
            ├── Decision Engine (approval evaluation, risk assessment)
            ├── HITL Gate (non-blocking approval flow)
            ├── Audit Trail (append-only event logging)
            └── Escalation System (timeout → upward routing)
```

### The Governance Stack

| Layer | Mechanism | Owner | Scope |
|-------|-----------|-------|-------|
| **Strategic** | Board Directives | Board Chair | Company-wide priorities |
| **Executive** | CEO Authority | Human CEO | High-stakes decisions |
| **Operational** | 5-Tier Matrix | Decision Engine Owner | Every tool action |
| **Technical** | HITL Gate | Security Compliance Lead | Executor pipeline |
| **Audit** | Audit Trail | Audit Trail Owner | Compliance & forensics |

---

## Key Stakeholders & Roles

### Primary Owners

| Role | Agent ID | Department | Responsibility |
|------|----------|------------|----------------|
| **Decision Engine Owner** | `decision_engine_owner` | Security | Owns the decision engine, approval matrix, risk assessment, and decision-tree navigation |
| **Security & Compliance Lead** | `security_compliance_lead` | Security | Integrates 5-tier approval rules into ToolRunner (GAP-003); enforces tier-gated compliance |
| **Human CEO** | `human_ceo` | Executive | Tier 4 approver — the only authority for high-stakes decisions |
| **CISO** | `ciso` | Security | Reports security posture to CEO and Board; oversees the security hierarchy |

### Secondary Stakeholders

| Role | Agent ID | Involvement |
|------|----------|-------------|
| **Chief of Staff** | `chief_of_staff` | Cross-team coordination; escalation recipient for Tier 3 timeouts |
| **CTO** | `cto` | Technical architecture decisions; Tier 3 approver for infrastructure |
| **CFO** | `cfo` | Budget approvals; financial action oversight |
| **CLO** | `clo` | Legal and compliance review; contract approvals |
| **Penetration Testing Lead** | `penetration_testing_lead` | Tests the 5-tier approval system, auth/CORS, and audit trail for vulnerabilities |
| **Audit Trail Owner** | `audit_trail_owner` | Ensures every privileged action emits a correlated audit event |

---

## Decision Flow

### How a Decision Moves Through the Tiers

```
Agent plans tool action
        │
        ▼
┌─────────────────────────────────────────┐
│  ToolRunner calls classify_tool_action()│
│  (tier_rules.py)                        │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Classification considers:              │
│  • Tool type default tier               │
│  • Path sensitivity (secrets → Tier 4)  │
│  • Command sensitivity (rm -rf → Tier 4)│
│  • Agent seniority (executive bypass)   │
│  • Task risk context (high → escalate)  │
└─────────────────────────────────────────┘
        │
        ▼
   ┌────┴────┐
   │ Tier 0-1│──→ Auto-approve + optional notification
   └────┬────┘
        │
   ┌────┴────┐
   │ Tier 2  │──→ HITL Gate → 1 approver → proceed/escalate
   └────┬────┘
        │
   ┌────┴────┐
   │ Tier 3  │──→ HITL Gate → 2 distinct approvers → proceed/escalate
   └────┬────┘
        │
   ┌────┴────┐
   │ Tier 4  │──→ HITL Gate → CEO only → proceed/board notification
   └─────────┘
```

### Escalation Path

| From | To | Trigger | Timeout |
|------|-----|---------|---------|
| Tier 2 | Tier 3 | No single approver response | 4 hours |
| Tier 3 | Tier 4 | No dual approval completed | 2 hours |
| Tier 4 | Board | CEO does not respond | 1 hour |

### Exception Handling

- **Self-approval rejection:** Tier 3 requires two **distinct** approvers. If the same person attempts to sign twice, the system denies with: *"Tier 3 requires two DISTINCT approvers."*
- **Non-CEO on Tier 4:** Only `human_ceo` can approve Tier 4 requests. Any other identity is rejected with: *"Tier 4 requires CEO-only approval."*
- **Expired requests:** If a request expires before approval, it is automatically escalated to the next tier. The original request is marked as expired, and a new request is created at the higher tier.

---

## Real-World Examples

### Example 1: Routine Code Read (Tier 0)

**Scenario:** The `lead_backend` agent needs to read `src/api/routes.py` to understand the current API structure.

**Classification:** `tool=read`, `path=src/api/routes.py` → **Tier 0 (Auto-Approve)**

**Result:** Action executes immediately. Audit event logged. No human involved.

---

### Example 2: Documentation Update (Tier 1)

**Scenario:** The `technical_documentation_lead` agent updates `docs/API-REFERENCE.md` with new endpoint documentation.

**Classification:** `tool=write`, `path=docs/API-REFERENCE.md` → **Tier 1 (Notify)**

**Result:** Action executes immediately. Slack and email notifications sent to the CPO and Technical Documentation Lead's manager. No blocking approval required.

---

### Example 3: Code Change (Tier 2)

**Scenario:** The `lead_backend` agent writes a fix to `src/api/handler.py` to resolve a bug.

**Classification:** `tool=write`, `path=src/api/handler.py` → **Tier 2 (Single Approver)**

**Result:** HITL gate creates an approval request. A human operator (or executive agent with sufficient seniority) reviews and approves. The action proceeds. If no approval within 4 hours, the request escalates to Tier 3.

---

### Example 4: Production Deployment (Tier 3)

**Scenario:** The `devops_lead` agent runs `docker push` to deploy a new container image to production.

**Classification:** `tool=execute`, `command=docker push` → **Tier 3 (Two-Person Rule)**

**Result:** HITL gate creates an approval request requiring 2 distinct approvers. The human operator signs first. The CTO signs second. The action proceeds. If only one approval is obtained within 2 hours, the request escalates to Tier 4 (CEO).

---

### Example 5: Accessing Secrets (Tier 4)

**Scenario:** The `cfo` agent writes to `config/secrets.yaml` to update API credentials.

**Classification:** `tool=write`, `path=config/secrets.yaml` → **Tier 4 (CEO Only)**

**Result:** HITL gate creates an approval request routed exclusively to `human_ceo`. The CEO reviews and approves. If no response within 1 hour, a board notification is triggered.

---

### Example 6: Dangerous Command (Tier 4)

**Scenario:** An agent attempts to execute `rm -rf /tmp/cache` (contains a dangerous pattern).

**Classification:** `tool=execute`, `command=rm -rf /tmp/cache` → **Tier 4 (CEO Only)**

**Result:** Even though the target is a cache directory, the `rm -rf` pattern is in the `DANGEROUS_COMMANDS` list. CEO approval required. This is by design — dangerous command patterns always escalate regardless of target.

---

### Example 7: Seniority De-escalation

**Scenario:** The `cto` agent (seniority: executive) writes to `src/main.py`.

**Classification:** `tool=write`, `path=src/main.py` → raw tier is Tier 2 (code path). But the CTO's seniority level allows auto-approval of Tier ≤ 2.

**Result:** The tier is de-escalated based on seniority. The CTO can auto-approve the write without external approval.

---

## Integration Points

### How the Matrix Connects to Other Systems

| System | Integration | Evidence |
|--------|-------------|----------|
| **ToolRunner** | Calls `classify_tool_action()` on every privileged tool call | `tool_runner.py:361` |
| **HITL Gate** | Receives tier info for tier-specific timeout and approver count | `hitl_gate.py:72` — returns `Future` (non-blocking) |
| **Audit Trail** | Logs every classification decision and approval outcome | `audit/integration.py` — `log_hitl_decision()` |
| **Decision Engine** | Evaluates actions against the approval matrix | `decision/engine.py` — `evaluate_action()` |
| **Escalation System** | Timeout triggers upward routing | `orchestrator/escalation.py` — tier-aware timeouts |
| **Dashboard** | Surfaces pending approvals, tier badges, signature status | `dashboard/api.py` — `/api/approvals` endpoint |
| **CLI** | `ai-company orchestrator approval` commands | `APPROVAL-CLI-COMMANDS.md` — list, approve, reject, history, tiers, stats, watch |
| **WebSocket** | Real-time approval notifications to connected clients | `dashboard/ws.py` — `broadcast_alert()` |
| **Board Governance** | High-priority directives may require approval via the matrix | `BOARD-DIRECTIVES.md` — integration point |
| **Cost Tracker** | Tier context influences model routing decisions | `model_router.py` — priority forwarding |

### Data Flow: Tool Action to Audit Event

```
Agent plans tool call
        │
        ▼
ToolRunner.run_plan()
        │
        ▼
classify_tool_action(tool, args, agent_id, task_context)
        │
        ▼
ApprovalTier returned
        │
        ├── Tier 0-1 → Execute immediately
        │                └── AuditWriter.log_tool_call(tier=0/1, result)
        │
        └── Tier 2+ → HITLGate.request()
                       │
                       ├── Creates ApprovalRequest (tier, required_approvers, timeout)
                       │
                       ├── ApprovalGate stores in approvals.yaml (atomic write)
                       │
                       ├── AuditWriter.log_hitl_decision(tier, status="pending")
                       │
                       ├── Executor marks task as AWAITING_APPROVAL, yields
                       │
                       └── When approved:
                           ├── AuditWriter.log_hitl_decision(tier, status="approved")
                           ├── ToolRunner executes the action
                           └── AuditWriter.log_tool_call(tier, result)
```

---

## Current Status & Recommendations

### Implementation Status

| Component | Status | Evidence |
|-----------|--------|----------|
| **Tier classification logic** | ✅ RESOLVED | `tier_rules.py` — 418 lines, full 5-tier implementation |
| **ToolRunner integration** | ✅ RESOLVED | `tool_runner.py:361` — calls `classify_tool_action()` |
| **Non-blocking HITL gate** | ✅ RESOLVED | `hitl_gate.py:72` — returns `Future`, no busy-wait |
| **Approval persistence** | ✅ RESOLVED | `approval.py` — YAML persistence with atomic writes |
| **Audit trail integration** | ✅ RESOLVED | `audit/integration.py` — `log_hitl_decision()` |
| **Dashboard surfacing** | ✅ RESOLVED | `dashboard/api.py` — approval endpoints |
| **CLI commands** | ✅ RESOLVED | 8 approval subcommands (list, approve, reject, show, history, tiers, stats, watch) |
| **Escalation routing** | ✅ RESOLVED | `orchestrator/escalation.py` — tier-aware timeouts |
| **Test coverage** | ✅ RESOLVED | 1,205 tests passing, including approval prompt tests |

### Known Gaps and Recommendations

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| **Memory consolidation not wired** (GAP-005) | Medium | Wire periodic `memory.consolidate()` into executor loop to bound memory growth |
| **Mobile API bypasses MessageBus** (GAP-011) | Medium | Route `mobile_api.py` reads through MessageBus for consistency |
| **Structured logging incomplete** (GAP-018) | Low | Add correlation IDs linking task → agent → tool call → approval |
| **Agent spec validation missing** (GAP-019) | Low | Add `ai-company agents validate` CLI command |

### Strategic Recommendations

1. **Publish tier thresholds publicly.** All agents should have clear visibility into what actions require what level of approval. The `approval tiers` CLI command exists — ensure every agent's system prompt includes tier-awareness guidance.

2. **Track approval velocity as a KPI.** The `approval stats` command shows average approval times. Track these over time. If Tier 2 approvals consistently exceed 4 hours, we have a bottleneck. If Tier 4 approvals exceed 24 hours, we have a governance problem.

3. **Conduct quarterly tier reviews.** The tier classifications in `tier_rules.py` are based on initial risk assessments. As the organization matures, some actions may warrant reclassification. A quarterly review by the CISO and Decision Engine Owner ensures the matrix stays aligned with actual risk.

4. **Expand the audit correlation model.** Every approval request should emit an audit event with: request ID, tier, agent, action, approvers, decision, timestamp, and escalation chain. This creates a complete forensic record.

5. **Integrate with Board Directives.** High-priority Board Directives (e.g., `DIR-2026-001: Establish Agent Deployment Pipeline`) should automatically generate Tier 3+ approval requests when converted to tasks. This ensures Board intent is enforced at the execution layer.

---

## Quick Reference Card

### Tier Summary

| Tier | Name | Approvers | Timeout | Escalates To | Color |
|------|------|-----------|---------|--------------|-------|
| **T0** | Auto-Approve | 0 | — | — | Dim |
| **T1** | Notify | 0 | — | — | Blue |
| **T2** | Single Approver | 1 | 4 hours | T3 | Yellow |
| **T3** | Two-Person Rule | 2 | 2 hours | T4 | Red |
| **T4** | CEO Only | 1 (CEO) | 1 hour | Board | Magenta |

### CLI Quick Commands

```bash
# View pending approvals
ai-company orchestrator approval list

# Approve a request
ai-company orchestrator approval approve <id> --notes "Safe to proceed"

# Reject a request (reason required)
ai-company orchestrator approval reject <id> --reason "Exceeds scope"

# View tier definitions
ai-company orchestrator approval tiers

# View approval statistics
ai-company orchestrator approval stats --since 30d

# Live monitor
ai-company orchestrator approval watch
```

---

## Appendix: Classification Rules Reference

### Path Escalation Rules

| Path Pattern | Tier | Examples |
|--------------|------|----------|
| `/secrets/`, `/.env`, `config/secrets.yaml` | 4 | Any write to secrets |
| `/production/`, `deploy/`, `terraform/`, `k8s/` | 3 | Infrastructure changes |
| `src/`, `tests/`, `app/`, `lib/` | 2 | Code modifications |
| `config/`, `docs/`, `.github/`, `.md` | 1 | Config/doc updates |

### Command Escalation Rules

| Command Pattern | Tier | Examples |
|-----------------|------|----------|
| `rm -rf`, `drop table`, `sudo rm`, `shutdown` | 4 | Destructive operations |
| `docker push`, `kubectl apply`, `terraform apply` | 3 | Production deployments |
| Other commands | 0 | Standard execution |

### Seniority Auto-Approval

| Seniority | Max Auto-Approve Tier |
|-----------|----------------------|
| Junior | 0 |
| Mid | 1 |
| Senior | 1 |
| Lead | 2 |
| Executive | 2 |

---

*This report was produced by the Internal Communications Lead. For questions about the 5-tier approval matrix, contact the Decision Engine Owner (`decision_engine_owner`) or the Security & Compliance Lead (`security_compliance_lead`).*
