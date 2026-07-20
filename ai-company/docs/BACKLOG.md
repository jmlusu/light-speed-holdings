# Product Backlog — AI Company Builder

**Author:** Product Owner  
**Date:** 2026-07-20  
**Prioritization:** MoSCoW (Must / Should / Could / Won't)  
**Story Point Scale:** Fibonacci (1, 2, 3, 5, 8, 13) — 1 point = ~1 hour of focused work

---

## 1. Backlog Summary

| Priority | Items | Total Points | Phase |
|----------|-------|-------------|-------|
| **Must** | 22 | 148 | 1-5 |
| **Should** | 14 | 68 | 1-5 |
| **Could** | 7 | 30 | 1-5 |
| **Won't (this cycle)** | 5 | 21 | N/A |
| **Total** | 48 | 267 | — |

---

## 2. Phase 1-2: Remaining Work (Architecture Gaps)

### 2.1 Must Have — Foundation Fixes

| ID | Item | Points | Gap | Phase |
|----|------|--------|-----|-------|
| M-001 | Route executor I/O through MessageBus | 5 | GAP-001 | 3 |
| M-002 | Create FileStore abstraction (atomic JSON/YAML) | 8 | GAP-002 | 3 |
| M-003 | Integrate tier rules into ToolRunner | 5 | GAP-003 | 3 |
| M-004 | Non-blocking HITL gate (remove busy wait) | 5 | GAP-004 | 3 |
| M-005 | Wire memory engine into executor pipeline | 8 | GAP-005 | 3 |
| M-006 | Wire WebSocket broadcast to executor events | 3 | GAP-006 | 3 |
| M-007 | Integrate scheduler into executor loop | 5 | GAP-007 | 3 |
| M-008 | Persist escalation events to file | 3 | GAP-008 | 3 |
| M-009 | Fix AgentLoop priority forwarding | 2 | GAP-012 | 1 |
| M-010 | Fix BriefingGenerator private method usage | 1 | GAP-014 | 1 |

**Must Have Subtotal:** 45 points

### 2.2 Should Have — Security & Gating

| ID | Item | Points | Gap | Phase |
|----|------|--------|-----|-------|
| S-001 | Dashboard CORS + API key auth | 5 | GAP-010 | 3 |
| S-002 | Fix LLM retry provider cycling | 3 | GAP-015 | 2 |
| S-003 | Remove shell=True from ToolRunner | 5 | GAP-016 | 2 |
| S-004 | CostTracker accumulator persistence | 2 | GAP-009 | 2 |
| S-005 | Dashboard API uses MessageBus | 2 | GAP-011 | 3 |

**Should Have Subtotal:** 17 points

### 2.3 Could Have — Quality & Polish

| ID | Item | Points | Gap | Phase |
|----|------|--------|-----|-------|
| C-001 | Task timeout + dead letter queue | 5 | GAP-017 | 3 |
| C-002 | Wire all KPI department collectors | 3 | GAP-013 | 3 |
| C-003 | Structured logging with correlation IDs | 5 | GAP-018 | 4 |
| C-004 | Agent spec validation | 3 | GAP-019 | 4 |
| C-005 | End-to-end integration tests | 5 | GAP-020 | 4 |

**Could Have Subtotal:** 21 points

---

## 3. Phase 3: Growth Functions

### 3.1 Must Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| G3-01 | Marketing campaign management | 8 | 3.1 | None |
| G3-02 | Lead scoring engine | 5 | 3.1 | G3-01 |
| G3-04 | Sales lead pipeline | 8 | 3.1 | None |
| G3-05 | Deal tracking & forecasting | 5 | 3.1 | G3-04 |
| G3-07 | Ticket management system | 5 | 3.2 | None |
| G3-08 | Customer satisfaction tracking (NPS/CSAT) | 3 | 3.2 | G3-07 |
| G3-10 | Contract lifecycle management | 8 | 3.2 | None |
| G3-11 | Compliance checking engine | 5 | 3.2 | G3-10 |

**Must Have Subtotal:** 47 points

### 3.2 Should Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| G3-03 | Content generation pipeline | 5 | 3.1 | G3-01 |
| G3-06 | Marketing-sales handoff workflow | 3 | 3.1 | G3-01, G3-04 |
| G3-09 | Churn prediction model | 5 | 3.2 | G3-07, G3-08 |
| G3-12 | Risk assessment workflow | 3 | 3.2 | G3-10, G3-11 |
| G3-13 | HR workforce planning | 5 | 3.2 | None |
| G3-14 | Onboarding automation | 3 | 3.2 | G3-13 |

**Should Have Subtotal:** 24 points

### 3.3 Could Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| G3-15 | Performance tracking | 3 | 3.2 | G3-13 |

**Could Have Subtotal:** 3 points

---

## 4. Phase 4: Specialist Agents

### 4.1 Must Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| P4-01 | Financial Analyst agent spec card | 3 | 4.1 | None |
| P4-02 | Financial Analyst tools (cost, budget, ROI) | 8 | 4.1 | P4-01 |
| P4-03 | DevOps agent spec card | 3 | 4.1 | None |
| P4-04 | DevOps tools (CI/CD, infra provisioning) | 8 | 4.1 | P4-03 |
| P4-05 | Data Scientist agent spec card | 3 | 4.1 | None |
| P4-06 | Data Scientist tools (analysis, modeling, reporting) | 5 | 4.1 | P4-05 |
| P4-07 | Compliance Officer agent spec card | 3 | 4.1 | None |
| P4-08 | Compliance Officer tools (audit, policy, risk) | 5 | 4.1 | P4-07 |
| P4-09 | Agent permission matrix | 5 | 4.2 | P4-02, P4-04, P4-06, P4-08 |
| P4-10 | Escalation rules per specialist | 5 | 4.2 | P4-09 |
| P4-13 | Specialist agent tests | 5 | 4.2 | P4-02, P4-04, P4-06, P4-08 |

**Must Have Subtotal:** 53 points

### 4.2 Should Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| P4-11 | Model routing per specialist | 3 | 4.2 | None |
| P4-12 | Agent-to-agent delegation workflows | 5 | 4.2 | P4-09 |

**Should Have Subtotal:** 8 points

### 4.3 Could Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| P4-14 | Agent spec card validation CLI | 3 | 4.2 | P4-01-P4-07 |

**Could Have Subtotal:** 3 points

---

## 5. Phase 5: Autonomous Coordination

### 5.1 Must Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| P5-01 | Scheduled execution cycles (cron daemon) | 8 | 5.1 | GAP-007 |
| P5-02 | Escalation rules engine | 8 | 5.1 | GAP-008 |
| P5-03 | Human approval gates (5-tier) | 8 | 5.1 | GAP-003, GAP-004 |
| P5-04 | Task timeout & dead letter queue | 5 | 5.1 | GAP-017 |
| P5-06 | Multi-agent collaboration protocol | 8 | 5.2 | P5-01, P5-02 |
| P5-07 | Self-healing retry logic | 5 | 5.2 | P5-04 |
| P5-11 | Emergency shutdown mechanism | 3 | 5.2 | None |

**Must Have Subtotal:** 45 points

### 5.2 Should Have

| ID | Item | Points | Sprint | Dependencies |
|----|------|--------|--------|--------------|
| P5-05 | Workflow-triggered scheduling | 3 | 5.1 | P5-01 |
| P5-08 | Agent performance feedback loop | 5 | 5.2 | Phase 3 memory |
| P5-09 | Autonomous daily briefings | 3 | 5.2 | P5-01, GAP-005 |
| P5-10 | CEO dashboard for autonomous oversight | 5 | 5.2 | P5-01-P5-04 |

**Should Have Subtotal:** 16 points

---

## 6. Won't Have (This Cycle)

| ID | Item | Points | Rationale |
|----|------|--------|-----------|
| W-01 | RAG pipeline (vector store, embeddings) | 13 | Phase 6 scope; requires external deps |
| W-02 | Agent self-improvement (prompt optimization) | 8 | Phase 6 scope; requires outcome data first |
| W-03 | Multi-tenant support | 8 | Single-user tool; not needed |
| W-04 | Web UI (React dashboard) | 5 | FastAPI dashboard sufficient for now |
| W-05 | Mobile companion app | 3 | Out of scope for developer tool |

**Won't Have Subtotal:** 21 points

---

## 7. Dependency Graph (Critical Path)

```
PHASE 1-2 GAPS (Foundation)
│
├─ GAP-002 (FileStore) ──▶ GAP-001 (MessageBus routing)
│                              │
│                              ├─▶ G3-01 (Marketing) ──▶ G3-02 (Lead scoring)
│                              │                           │
│                              ├─▶ G3-04 (Sales) ──────▶ G3-05 (Deal tracking)
│                              │
│                              └─▶ G3-07 (Tickets) ────▶ G3-08 (NPS/CSAT)
│
├─ GAP-003 (Tier rules) ──▶ GAP-004 (Non-blocking HITL)
│                              │
│                              ├─▶ P5-03 (5-tier approval gates)
│                              │
│                              └─▶ P4-09 (Permission matrix)
│
├─ GAP-005 (Memory integration) ──▶ P5-08 (Performance feedback)
│                                       │
│                                       └─▶ P5-09 (Daily briefings)
│
├─ GAP-007 (Scheduler) ──▶ P5-01 (Scheduled execution)
│                              │
│                              ├─▶ P5-05 (Workflow-triggered scheduling)
│                              └─▶ P5-06 (Multi-agent collaboration)
│
└─ GAP-017 (Timeout/DLQ) ──▶ P5-04 (Task timeout & DLQ)
                                 │
                                 └─▶ P5-07 (Self-healing retry)
```

**Critical Path:** GAP-002 → GAP-001 → GAP-005 → P5-01 → P5-06 → P5-07

---

## 8. Velocity & Capacity Planning

### Assumptions

- **Sprint duration:** 2 weeks
- **Agent capacity:** 7 agents, ~15 hours/sprint each = ~105 hours/sprint
- **Buffer:** 20% for blockers and unexpected work

### Phase Timeline

| Phase | Points | Sprints | Weeks | Velocity Required |
|-------|--------|---------|-------|-------------------|
| Phase 1-2 gaps | 83 | 2 | 4 | 42 pts/sprint |
| Phase 3 | 74 | 2 | 4 | 37 pts/sprint |
| Phase 4 | 64 | 2 | 4 | 32 pts/sprint |
| Phase 5 | 61 | 2 | 4 | 31 pts/sprint |
| **Total** | **282** | **8** | **16** | **35 pts/sprint avg** |

### Priority Summary

| Priority | Points | % of Backlog |
|----------|--------|-------------|
| Must | 190 | 67% |
| Should | 65 | 23% |
| Could | 27 | 10% |
| Won't | 0 | 0% |

---

## 9. Backlog Maintenance Rules

1. **Grooming:** Every sprint, review and re-prioritize remaining items
2. **New items:** Must have acceptance criteria, story points, and dependencies before entering backlog
3. **De-prioritization:** Items not completed in planned sprint move to next sprint unless blocked
4. **Won't items:** Reviewed quarterly; may move to Could/Must based on customer feedback
5. **Blocked items:** Flagged with blocker ID and escalation owner; resolved within 48h or escalated

---

*This backlog is maintained by the Product Owner and reviewed bi-weekly with the CPO.*
