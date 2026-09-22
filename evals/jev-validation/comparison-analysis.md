# Jev Validation Comparison Analysis

Generated: 2026-09-19 01:57:09

## Summary Table

| Workflow | Jev Agreement | LLM Agreement | Deterministic Agreement | Jev ECE | LLM ECE | Jev Latency p50 | LLM Latency p50 | Jev Cost | LLM Cost |
|----------|---------------|---------------|------------------------|---------|---------|-----------------|-----------------|----------|----------|
| intent_routing | 20.0% | 20.0% | 0.0% | 0.7000 | 0.6500 | 0ms | 0ms | $0.000400 | $0.000400 |
| tool_verification | 60.0% | 60.0% | 0.0% | 0.3000 | 0.2500 | 0ms | 0ms | $0.000400 | $0.000400 |
| trace_scoring | 40.0% | 40.0% | 0.0% | 0.3000 | 0.3000 | 0ms | 0ms | $0.000400 | $0.000400 |
| customer_triage | 20.0% | 20.0% | 0.0% | 0.7000 | 0.6500 | 0ms | 0ms | $0.000400 | $0.000400 |
| policy_compliance | 20.0% | 20.0% | 0.0% | 0.7000 | 0.6500 | 0ms | 0ms | $0.000400 | $0.000400 |

## Decision Gate

**Criteria**: Jev >=90% LLM agreement on >=4/5 workflows with ECE < 0.1

| Workflow | Jev Agreement | ECE | GO? |
|----------|---------------|-----|-----|
| intent_routing | 20.0% | 0.7000 | [FAIL] |
| tool_verification | 60.0% | 0.3000 | [FAIL] |
| trace_scoring | 40.0% | 0.3000 | [FAIL] |
| customer_triage | 20.0% | 0.7000 | [FAIL] |
| policy_compliance | 20.0% | 0.7000 | [FAIL] |
| **Pass Count** | **0/5** | | |

## Recommendation
[NO-GO] - Execute fallback plan (JEV-FB-01 through JEV-FB-04)