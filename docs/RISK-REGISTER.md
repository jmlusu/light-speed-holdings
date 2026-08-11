# Risk Register — Light Speed Holdings

> Last updated: 2026-07-20

## Risk Matrix

| ID | Category | Description | Likelihood (1-5) | Impact (1-5) | Level | Mitigation | Owner | Status |
|----|----------|-------------|-------------------|---------------|-------|------------|-------|--------|
| R01 | Technical | LLM provider outage blocks all agent tasks | 3 | 4 | High | Multi-provider fallback chain in ModelRouter; tier-based redundancy (opencode -> ollama, deepseek -> opencode); CircuitBreaker fails fast after 3 errors | cto | 🟢 Mitigated |
| R02 | Financial | Uncontrolled API token spend exceeds budget | 3 | 3 | Medium | Tier routing (fast/standard/premium), per-agent overrides, budget ceilings in models.yaml, CostTracker with daily/task budgets | cfo | 🟢 Mitigated |
| R03 | Security | Agent executes unauthorized file system changes | 2 | 5 | High | Permission profiles per agent (ReviewOnly, Execute), HITL gate for write/execute, path escape blocking in ToolRunner, tier-based classification (GAP-003) | security-engineer | 🟡 Partial |
| R04 | Operational | Escalation chain fails to resolve in SLA | 2 | 3 | Medium | EscalationManager with timeout rules, max_retries, and automatic escalation to chief-of-staff; postmortem tracking | coo | 🟢 Mitigated |
| R05 | Data | Agent produces incorrect financial analysis | 2 | 4 | High | CFO approval gate for budget/financial actions, dual-approval for actions >$1M, 5-tier approval system (GAP-003) | cfo | 🟡 Partial |
| R06 | Compliance | Agent generates non-compliant content | 2 | 3 | Medium | Legal review gate for external-facing content, policy enforcement via Constitution, audit trail for all actions | legal | 🟢 Mitigated |
| R07 | Technical | Model hallucination causes incorrect task execution | 3 | 3 | Medium | Structured JSON response format, retry on parse failure (3-strategy), result validation in AgentLoop, max 10 iterations | chief-ai-officer | 🟢 Mitigated |
| R08 | Operational | Key agent (CTO/CAIO) becomes unavailable | 1 | 4 | Medium | Delegation chains documented in org chart, chief-of-staff can reassign, memory system preserves institutional knowledge | chief-of-staff | 🟢 Mitigated |
| R09 | Security | Prompt injection via task instruction | 2 | 4 | High | System prompt isolation, input sanitization, HITL gate for sensitive operations, tier-based classification | security-engineer | 🟡 Partial |
| R10 | Financial | Model routing selects premium tier for routine tasks | 2 | 2 | Low | Routing rules enforce tier-by-priority, context overrides only for escalation/approval, priority forwarded to router (GAP-012 resolved) | cfo | 🟢 Mitigated |
| R11 | Technical | Agent loop infinite cycling (AgentLoop) | 2 | 4 | Medium | Hard limit on `max_iterations` (default 10), circuit breaker on repeated tool failures, budget enforcement | cio | 🟢 Mitigated |
| R12 | Financial | LLM cost runaway in autonomous mode | 3 | 4 | High | Per-task and per-agent cost ceilings in CostTracker, automatic task suspension on limit breach, circuit breaker | cfo | 🟢 Mitigated |
| R13 | Technical | Audit log storage growth exceeds disk capacity | 4 | 2 | Medium | Log rotation (daily), configurable retention policy (default 30d), archival to cold storage (retention module exists) | cio | 🟡 Partial |
| R14 | Technical | WebSocket connection leaks degrade dashboard performance | 2 | 3 | Medium | Heartbeat/ping-pong (30s), connection timeout (5m), max concurrent connections limit per IP | lead-frontend | 🟡 Partial |
| R15 | Security | Concurrent file writes corrupt shared JSON state | 3 | 4 | High | FileStore abstraction with atomic writes (Sprint 2 S2-02), single source of truth via MessageBus (Sprint 2 S2-01) | lead-backend | 🔴 Open |
| R16 | Security | Dashboard API allows unauthenticated access | 3 | 4 | High | API key middleware, CORS restrictions, rate limiting (Sprint 2 S2-08) | lead-frontend | 🔴 Open |
| R17 | Technical | HITL gate blocks executor for 30 minutes | 3 | 3 | Medium | Non-blocking approval flow, AWAITING_APPROVAL status, concurrent task processing (Sprint 2 S2-05) | lead-backend | 🔴 Open |
| R18 | Security | Shell injection via ToolRunner | 2 | 5 | High | shlex.split() instead of shell=True, command allowlist validation (Sprint 2 S2-10) | lead-backend | 🔴 Open |

## Risk Levels

- **Critical (20-25)**: Immediate action required. Human CEO must approve.
- **High (12-19)**: Action required within 48 hours. Executive approval needed.
- **Medium (6-11)**: Monitor and mitigate per schedule. Department head owns.
- **Low (1-5)**: Accept and monitor. Review quarterly.

## Risk Summary

| Level | Count | Actions |
|-------|-------|---------|
| Critical | 0 | — |
| High | 6 | R03, R05, R09, R15, R16, R18 |
| Medium | 7 | R02, R04, R06, R07, R11, R13, R14, R17 |
| Low | 2 | R01, R08, R10, R12 |

## Top Risks Requiring Sprint 2 Action

| Risk | Gap | Sprint 2 Item | Effort |
|------|-----|---------------|--------|
| R15 (concurrent writes) | GAP-002 | S2-02 (FileStore) | 6h |
| R16 (dashboard auth) | GAP-010 | S2-08 (Dashboard Auth) | 3h |
| R17 (HITL blocking) | GAP-004 | S2-05 (Non-blocking HITL) | 4h |
| R18 (shell injection) | GAP-016 | S2-10 (Remove shell=True) | 2h |
| R03 (unauthorized changes) | GAP-003 | S2-04 (Tier Rules) | 4h |
| R05 (incorrect financial) | GAP-003 | S2-04 (Tier Rules) | 4h |

## Review Cadence

- Risk register reviewed monthly by CFO + Risk Board Advisor
- Critical risks escalated to human CEO immediately
- Quarterly risk assessment by full board
- Sprint 2 will close 6 high-risk items (R15, R16, R17, R18, R03, R05)
