# Risk Register — Light Speed Holdings

> Last updated: 2026-07-17

## Risk Matrix

| ID | Category | Description | Likelihood (1-5) | Impact (1-5) | Level | Mitigation | Owner |
|----|----------|-------------|-------------------|---------------|-------|------------|-------|
| R01 | Technical | LLM provider outage blocks all agent tasks | 3 | 4 | High | Multi-provider fallback chain in ModelRouter; tier-based redundancy (opencode -> ollama, deepseek -> opencode) | cto |
| R02 | Financial | Uncontrolled API token spend exceeds budget | 3 | 3 | Medium | Tier routing (fast/standard/premium), per-agent overrides, budget ceilings in models.yaml | cfo |
| R03 | Security | Agent executes unauthorized file system changes | 2 | 5 | High | Permission profiles per agent (ReviewOnly, Execute), HITL gate for write/execute, path escape blocking in ToolRunner | security-engineer |
| R04 | Operational | Escalation chain fails to resolve in SLA | 2 | 3 | Medium | EscalationManager with timeout rules, max_retries, and automatic escalation to chief-of-staff | coo |
| R05 | Data | Agent produces incorrect financial analysis | 2 | 4 | High | CFO approval gate for budget/financial actions, dual-approval for actions >$1M | cfo |
| R06 | Compliance | Agent generates non-compliant content | 2 | 3 | Medium | Legal review gate for external-facing content, policy enforcement via Constitution | legal |
| R07 | Technical | Model hallucination causes incorrect task execution | 3 | 3 | Medium | Structured JSON response format, retry on parse failure, result validation in Executor loop | chief-ai-officer |
| R08 | Operational | Key agent (CTO/CAIO) becomes unavailable | 1 | 4 | Medium | Delegation chains documented in org chart, chief-of-staff can reassign | chief-of-staff |
| R09 | Security | Prompt injection via task instruction | 2 | 4 | High | System prompt isolation, input sanitization, HITL gate for sensitive operations | security-engineer |
| R10 | Financial | Model routing selects premium tier for routine tasks | 2 | 2 | Low | Routing rules enforce tier-by-priority, context overrides only for escalation/approval | cfo |

## Risk Levels

- **Critical (20-25)**: Immediate action required. Human CEO must approve.
- **High (12-19)**: Action required within 48 hours. Executive approval needed.
- **Medium (6-11)**: Monitor and mitigate per schedule. Department head owns.
- **Low (1-5)**: Accept and monitor. Review quarterly.

## Review Cadence

- Risk register reviewed monthly by CFO + Risk Board Advisor
- Critical risks escalated to human CEO immediately
- Quarterly risk assessment by full board
