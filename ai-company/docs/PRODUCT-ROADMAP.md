# Product Roadmap — AI Company Builder

**Author:** Product Owner  
**Date:** 2026-07-20  
**Status:** ACTIVE  
**Review Cadence:** Bi-weekly  
**Owner:** CPO

---

## 1. Vision

Transform AI Company Builder from a developer tool that generates agent hierarchies into an autonomous, self-governing AI company that executes business functions end-to-end — from marketing campaigns to financial forecasting — with minimal human intervention and maximum accountability.

---

## 2. Current State (Phase 1-2 Complete)

| Capability | Status | Quality |
|------------|--------|---------|
| Agent registry & generation | Production | High — 19 YAML configs, 24 CLI commands |
| Multi-provider LLM routing | Production | High — 5 providers, 3-tier routing |
| Task orchestration (MessageBus) | Functional | Medium — GAP-001/002 integration gaps |
| Dashboard API | Functional | Medium — No auth, no live KPIs |
| Memory engine | Functional | High — 6 types, not wired to executor |
| Decision engine | Functional | High — approval matrix, risk assessment |
| Workflow engine | Functional | High — 9 workflows, SLA tracking |
| HITL gate | Functional | Medium — blocking, binary approve/deny |
| Cost tracking | Functional | Medium — in-memory accumulators lost on restart |
| Audit trail | Missing | N/A — module does not exist |

**Test Coverage:** 183 tests passing, ruff clean, mypy clean  
**Known Architecture Gaps:** 20 (CRITICAL: 2, HIGH: 5, MEDIUM: 9, LOW: 4)

---

## 3. Phase Overview

| Phase | Name | Theme | Timeline | Status |
|-------|------|-------|----------|--------|
| 1 | Foundation | Project structure, CLI, registry, generator | Complete | Done |
| 2 | Core Operations | MessageBus, models, orchestrator, tests | Complete | Done |
| **3** | **Growth Functions** | **Marketing, Sales, CS, Legal, HR modules** | **Weeks 1-8** | **Planning** |
| **4** | **Specialist Agents** | **Financial Analyst, DevOps, Data Scientist, Compliance** | **Weeks 9-16** | **Planning** |
| **5** | **Autonomous Coordination** | **Scheduled cycles, escalation, approval gates, self-healing** | **Weeks 17-24** | **Planning** |

---

## 4. Phase 3: Growth Functions

### 4.1 Goal

Implement business function modules (Marketing, Sales, Customer Success, Legal, HR) as first-class CLI commands with data models, workflows, KPIs, and SOPs — enabling the AI company to operate real business processes.

### 4.2 Sprint Breakdown

#### Sprint 3.1 — Marketing & Sales (Weeks 1-4)

| ID | Feature | Story Points | Priority | Dependencies |
|----|---------|-------------|----------|--------------|
| G3-01 | Marketing campaign management | 8 | Must | None |
| G3-02 | Lead scoring engine | 5 | Must | G3-01 |
| G3-03 | Content generation pipeline | 5 | Should | G3-01 |
| G3-04 | Sales lead pipeline | 8 | Must | None |
| G3-05 | Deal tracking & forecasting | 5 | Must | G3-04 |
| G3-06 | Marketing-sales handoff workflow | 3 | Should | G3-01, G3-04 |

**Sprint 3.1 Total:** 34 points

#### Sprint 3.2 — Customer Success & Legal (Weeks 5-8)

| ID | Feature | Story Points | Priority | Dependencies |
|----|---------|-------------|----------|--------------|
| G3-07 | Ticket management system | 5 | Must | None |
| G3-08 | Customer satisfaction tracking (NPS/CSAT) | 3 | Must | G3-07 |
| G3-09 | Churn prediction model | 5 | Should | G3-07, G3-08 |
| G3-10 | Contract lifecycle management | 8 | Must | None |
| G3-11 | Compliance checking engine | 5 | Must | G3-10 |
| G3-12 | Risk assessment workflow | 3 | Should | G3-10, G3-11 |
| G3-13 | HR workforce planning | 5 | Should | None |
| G3-14 | Onboarding automation | 3 | Should | G3-13 |
| G3-15 | Performance tracking | 3 | Could | G3-13 |

**Sprint 3.2 Total:** 40 points

### 4.3 Architecture Impact

```
Phase 3 adds to existing architecture:
├── src/ai_company/marketing/     (NEW — campaign, scoring, content)
├── src/ai_company/sales/         (NEW — pipeline, deals, forecasting)
├── src/ai_company/customer_success/  (NEW — tickets, satisfaction, churn)
├── src/ai_company/legal/         (NEW — contracts, compliance, risk)
├── src/ai_company/hr/            (NEW — workforce, onboarding, performance)
├── company/config/marketing.yaml (NEW — marketing KPIs, thresholds)
├── company/config/sales.yaml     (NEW — sales KPIs, thresholds)
├── company/config/cs.yaml        (NEW — CS KPIs, thresholds)
├── company/config/legal.yaml     (NEW — legal KPIs, thresholds)
├── company/config/hr.yaml        (NEW — HR KPIs, thresholds)
└── cli/{marketing,sales,customer-success,legal,hr}.py  (wired)
```

### 4.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Scope creep across 5 departments | High | High | Strict sprint boundaries; deferrable items marked Could |
| Data model conflicts between departments | Medium | Medium | Unified base model (EntityBase) with department-specific extensions |
| LLM costs spike from content generation | Medium | Low | Use fast-tier models (deepseek) for content; premium for legal review |
| Integration with existing MessageBus | Low | Medium | Use established patterns from Phase 1-2 |

---

## 5. Phase 4: Specialist Agents

### 5.1 Goal

Deploy four specialist agents — Financial Analyst, DevOps, Data Scientist, Compliance Officer — with domain-specific tools, permissions, and escalation rules. These agents operate as subagents under their respective executives.

### 5.2 Sprint Breakdown

#### Sprint 4.1 — Agent Definitions & Tools (Weeks 9-12)

| ID | Feature | Story Points | Priority | Dependencies |
|----|---------|-------------|----------|--------------|
| P4-01 | Financial Analyst agent spec card | 3 | Must | None |
| P4-02 | Financial Analyst tools (cost analysis, budgeting, ROI) | 8 | Must | P4-01 |
| P4-03 | DevOps agent spec card | 3 | Must | None |
| P4-04 | DevOps tools (CI/CD management, infra provisioning) | 8 | Must | P4-03 |
| P4-05 | Data Scientist agent spec card | 3 | Must | None |
| P4-06 | Data Scientist tools (analysis, modeling, reporting) | 5 | Must | P4-05 |
| P4-07 | Compliance Officer agent spec card | 3 | Must | None |
| P4-08 | Compliance Officer tools (audit, policy check, risk scan) | 5 | Must | P4-07 |

**Sprint 4.1 Total:** 38 points

#### Sprint 4.2 — Integration & Permissions (Weeks 13-16)

| ID | Feature | Story Points | Priority | Dependencies |
|----|---------|-------------|----------|--------------|
| P4-09 | Agent permission matrix (tool → permission → approval tier) | 5 | Must | P4-02, P4-04, P4-06, P4-08 |
| P4-10 | Escalation rules per specialist agent | 5 | Must | P4-09 |
| P4-11 | Model routing per specialist (cost/quality) | 3 | Should | None |
| P4-12 | Agent-to-agent delegation workflows | 5 | Should | P4-09 |
| P4-13 | Specialist agent tests (unit + integration) | 5 | Must | P4-02, P4-04, P4-06, P4-08 |
| P4-14 | Agent spec card validation CLI | 3 | Could | P4-01-P4-07 |

**Sprint 4.2 Total:** 26 points

### 5.3 Agent Specification Summary

| Agent | Executive Parent | Tools | Permission | Model Tier | Escalation |
|-------|-----------------|-------|------------|------------|------------|
| Financial Analyst | CFO | read, write, execute, code_interpreter | Execute (budget < $10K) | Standard | CFO → CEO for > $10K |
| DevOps | CTO | read, write, execute, code_interpreter | Execute (non-prod) | Standard | CTO → CEO for prod |
| Data Scientist | CAIO | read, write, execute, code_interpreter, web_search | Execute | Premium | CAIO → CTO for infra |
| Compliance Officer | Legal | read, write | AdvisoryOnly | Premium | Legal → CEO for violations |

### 5.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Agent over-permissioning | Medium | High | Principle of least privilege; approval tiers enforced |
| Tool execution in production | Low | Critical | HITL gate mandatory for prod actions; tier_rules integration |
| Model cost escalation | Medium | Medium | Per-agent cost budgets; fast-tier for routine tasks |
| Inter-agent coordination failures | Medium | Medium | Clear delegation chains; timeout + retry |

---

## 6. Phase 5: Autonomous Coordination

### 6.1 Goal

Enable the AI company to operate in autonomous mode with scheduled execution cycles, intelligent escalation, human approval gates for critical actions, multi-agent collaboration, and self-healing retry logic — achieving the vision of a self-governing AI organization.

### 6.2 Sprint Breakdown

#### Sprint 5.1 — Scheduling & Escalation (Weeks 17-20)

| ID | Feature | Story Points | Priority | Dependencies |
|----|---------|-------------|----------|--------------|
| P5-01 | Scheduled execution cycles (cron daemon) | 8 | Must | GAP-007 |
| P5-02 | Escalation rules engine | 8 | Must | GAP-008 |
| P5-03 | Human approval gates (5-tier) | 8 | Must | GAP-003, GAP-004 |
| P5-04 | Task timeout & dead letter queue | 5 | Must | GAP-017 |
| P5-05 | Workflow-triggered scheduling | 3 | Should | P5-01 |

**Sprint 5.1 Total:** 32 points

#### Sprint 5.2 — Collaboration & Self-Healing (Weeks 21-24)

| ID | Feature | Story Points | Priority | Dependencies |
|----|---------|-------------|----------|--------------|
| P5-06 | Multi-agent collaboration protocol | 8 | Must | P5-01, P5-02 |
| P5-07 | Self-healing retry logic | 5 | Must | P5-04 |
| P5-08 | Agent performance feedback loop | 5 | Should | Phase 3 memory integration |
| P5-09 | Autonomous daily briefings | 3 | Should | P5-01, GAP-005 |
| P5-10 | CEO dashboard for autonomous oversight | 5 | Should | P5-01-P5-04 |
| P5-11 | Emergency shutdown mechanism | 3 | Must | None |

**Sprint 5.2 Total:** 29 points

### 6.3 Architecture Impact

```
Phase 5 completes the autonomous loop:
┌─────────────────────────────────────────────────────────┐
│                    Autonomous Cycle                      │
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │ Scheduler │───▶│ Executor │───▶│ Agent    │          │
│  │ (cron)    │    │ (tick)   │    │ Loop     │          │
│  └──────────┘    └────┬─────┘    └──────────┘          │
│                       │                                  │
│                 ┌─────▼─────┐                           │
│                 │ Escalation │───▶ CEO Dashboard         │
│                 │ Engine     │                           │
│                 └─────┬─────┘                           │
│                       │                                  │
│                 ┌─────▼─────┐                           │
│                 │ HITL Gate  │───▶ Human CEO             │
│                 │ (5-tier)   │                           │
│                 └───────────┘                           │
│                                                          │
│  Self-Healing: timeout → retry → escalate → DLQ         │
└─────────────────────────────────────────────────────────┘
```

### 6.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Autonomous execution exceeds budget | High | Critical | Per-task + per-agent + per-day cost ceilings; auto-suspend |
| Escalation storms (cascading escalations) | Medium | High | Rate limiting on escalations; max depth per task |
| Scheduler drift (cron timing) | Low | Low | Monitor execution timestamps; alert on drift > 5min |
| Self-healing creates infinite retry loops | Medium | High | Max retry count per task type; exponential backoff with cap |
| Human CEO overwhelmed by approval requests | Medium | High | Tier-based approval; auto-approve Tier 0-1; batch low-tier |

---

## 7. Cross-Phase Dependencies

```
Phase 3 (Growth Functions)     Phase 4 (Specialist Agents)
┌────────────────────────┐     ┌────────────────────────────┐
│ Marketing module        │     │ Financial Analyst           │
│ Sales module            │────▶│   uses: cost data from     │
│ CS module               │     │   CFO + marketing/sales    │
│ Legal module            │     │   module cost tracking      │
│ HR module               │     │                             │
└───────────┬────────────┘     │ DevOps                       │
            │                   │   uses: deployment workflows │
            │                   │   from Phase 3               │
            ▼                   │                             │
Phase 5 (Autonomous)           │ Data Scientist               │
┌────────────────────────┐     │   uses: all department data  │
│ Scheduled cycles        │     │   from Phase 3 modules      │
│ Escalation engine       │◀───│                             │
│ HITL gates              │     │ Compliance Officer           │
│ Multi-agent collab      │     │   uses: legal + CS module    │
│ Self-healing            │     │   compliance data            │
└────────────────────────┘     └────────────────────────────┘
```

---

## 8. Success Metrics by Phase

### Phase 3: Growth Functions

| Metric | Target | Measurement |
|--------|--------|-------------|
| Departments with working CLI commands | 5/5 | `ai-company marketing --help` etc. |
| Department KPIs wired to dashboard | 5/5 | Live data in dashboard panels |
| Workflows per department | >= 2 each | `ai-company workflows list` |
| SOPs per department | >= 1 each | docs/sop-*.md |
| Test coverage for new modules | >= 80% | pytest --cov |

### Phase 4: Specialist Agents

| Metric | Target | Measurement |
|--------|--------|-------------|
| Specialist agents generated | 4/4 | `.opencode/agents/` has 4 new files |
| Agent tool permissions enforced | 100% | HITL blocks unauthorized tools |
| Escalation rules per agent | >= 2 each | escalation.yaml config |
| Model routing per agent | Working | CRITICAL → premium, LOW → fast |
| Agent delegation success rate | >= 90% | Task completion audit |

### Phase 5: Autonomous Coordination

| Metric | Target | Measurement |
|--------|--------|-------------|
| Scheduled tasks execute on time | 100% | Scheduler execution log |
| HITL approval turnaround | < 5 min avg | Approval timestamp diff |
| Self-healing retry success | >= 70% | Retry → success rate |
| Escalation resolution within SLA | >= 95% | Escalation log timestamps |
| Budget adherence (autonomous mode) | Within 10% | Cost tracker daily summary |
| Zero unapproved production changes | 0 | Audit trail |

---

## 9. Budget Estimate

| Phase | Estimated Hours | LLM Cost (Testing) | Total |
|-------|----------------|--------------------|----|
| Phase 3 | ~120 hours | ~$50 | ~$50 |
| Phase 4 | ~80 hours | ~$30 | ~$30 |
| Phase 5 | ~100 hours | ~$40 | ~$40 |
| **Total** | **~300 hours** | **~$120** | **~$120** |

*Note: LLM costs assume local Ollama for dev/testing, premium models only for integration tests.*

---

## 10. Milestones

| Milestone | Date | Deliverable |
|-----------|------|-------------|
| M3.1 | Week 2 | Marketing + Sales modules working |
| M3.2 | Week 4 | Sprint 3.1 complete, all tests pass |
| M3.3 | Week 6 | CS + Legal modules working |
| M3.4 | Week 8 | **Phase 3 complete** — all 5 departments operational |
| M4.1 | Week 10 | 4 specialist agent spec cards generated |
| M4.2 | Week 12 | Specialist tools implemented and tested |
| M4.3 | Week 14 | Permissions + escalation wired |
| M4.4 | Week 16 | **Phase 4 complete** — specialist agents operational |
| M5.1 | Week 18 | Scheduler + escalation engine working |
| M5.2 | Week 20 | HITL 5-tier gates operational |
| M5.3 | Week 22 | Multi-agent collaboration + self-healing |
| M5.4 | Week 24 | **Phase 5 complete** — autonomous mode operational |

---

*This roadmap is reviewed bi-weekly by the CPO and updated based on sprint outcomes.*
