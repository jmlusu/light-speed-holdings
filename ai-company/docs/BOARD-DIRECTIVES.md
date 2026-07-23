# Board Directives

> Formal instructions issued by the Board of Directors that must be acknowledged, tracked, and completed.

## What Are Board Directives?

A **Board Directive** is a formal, trackable instruction issued by the Board of Directors (or authorized executives) that requires execution by a designated owner. Directives represent the primary mechanism through which the Board translates strategic priorities into concrete actions.

**Key characteristics:**
- Issued by a Board member or authorized authority
- Assigned to a specific owner (agent or role)
- Has a defined deadline and priority level
- Follows a lifecycle: `pending → in_progress → completed` (or `overdue`)
- Source of truth: `config/board/directives.yaml`

## Directive Lifecycle

```
┌─────────┐     ┌──────────────┐     ┌─────────────┐     ┌───────────┐
│  ISSUED  │ ──→ │ ACKNOWLEDGED │ ──→ │ IN_PROGRESS │ ──→ │ COMPLETED │
│ (pending)│     │  (pending)   │     │             │     │           │
└─────────┘     └──────────────┘     └─────────────┘     └───────────┘
                                                                  │
                                                            ┌─────┴─────┐
                                                            │  OVERDUE   │
                                                            │ (if past   │
                                                            │  deadline) │
                                                            └───────────┘
```

**Status definitions:**

| Status | Meaning |
|--------|---------|
| `pending` | Directive issued but not yet acknowledged or started |
| `in_progress` | Owner has acknowledged and is actively working |
| `completed` | Work finished and verified |
| `overdue` | Deadline passed without completion |

## Tracking Table

| ID | Title | Priority | Owner | Status | Deadline |
|----|-------|----------|-------|--------|----------|
| DIR-2026-001 | Establish Agent Deployment Pipeline | critical | cto | completed | 2026-07-22 |
| DIR-2026-002 | Implement Audit Trail for Executor Actions | critical | cto | completed | 2026-07-20 |
| DIR-2026-003 | Complete Sprint 3 — Dashboard, Memory, and Coordination | high | chief-of-staff | completed | 2026-07-23 |
| DIR-2026-004 | Launch Sprint 4 — Quality and Completeness | high | chief-of-staff | pending | 2026-07-30 |
| DIR-2026-005 | Establish Board Directive Tracking System | medium | chief-of-staff | in_progress | 2026-07-23 |

## Priority Levels

| Level | Definition | Response Time |
|-------|-----------|---------------|
| **critical** | Immediate action required; blocks other work | 24 hours |
| **high** | Important; should be addressed within the sprint | 3-5 days |
| **medium** | Desired; addressed when capacity allows | 1-2 weeks |
| **low** | Nice-to-have; backlog item | Next sprint |

## CLI Commands

```bash
# List all directives
ai-company board directives list

# Add a new directive interactively
ai-company board directives add

# Mark a directive as completed
ai-company board directives complete DIR-2026-004

# Show directive status summary
ai-company board directives status
```

## Source of Truth

All directives are stored in **`config/board/directives.yaml`**. This YAML file is the authoritative source. The CLI commands read from and write to this file.

## Integration Points

- **Board Governance** (`docs/BOARD-GOVERNANCE.md`): Directives are the action arm of Board governance
- **Decision Engine**: High-priority directives may require approval via the 5-tier matrix
- **Executor Loop**: Directives can be converted to tasks via the MessageBus
- **Audit Trail**: Directive status changes are logged for compliance
- **Dashboard**: Directive status can be surfaced on the CEO dashboard
