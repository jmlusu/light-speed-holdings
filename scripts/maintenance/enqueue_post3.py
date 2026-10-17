from ai_company.publishing.queue import PublishQueue

queue = PublishQueue()

# Post 3 body
body_post3 = """LightSpeed AI-native org structure: 90 agents orchestrated via a MessageBus task queue, 20 departments with health rollup, and 5-tier HITL governance cascading from executive to specialist level. This is the orchestration layer (O in HAOMT-G-V) that makes the system work.

## Executive Summary

The orchestration layer is the operational backbone of an AI-native organization. LightSpeed Holdings has built this layer using three foundational components:

1. **MessageBus task queue** -- crash-safe, idempotent task execution (`src/ai_company/executor/loop.py`)
2. **Department health rollup** -- executive scorecard with metrics per department (`data_service.py` `get_executive_scorecard()`)
3. **5-tier HITL governance** -- from autonomous decisions through to cleared rulings (`orchestrator/approval.py`)

For Malawi and SADC institutions, this orchestration layer must operate with sovereign data defaults, low-bandwidth operation (offline-first, local models), and visible variable cost (90-day pilot, no lock-in).

## Why Orchestration Matters (Builder Proof)

- **We built the queue.** `src/ai_company/executor/loop.py` polls inbox.json, runs AgentLoop (multi-turn ReAct), dead-letter queue, memory recall, audit logging.
- **We measured the metrics.** `graph/engine.py` `OrgNode` + `compute_org_metrics()` returns per-node capacity, activity, trend, and risk with a 30s TTL cache.
- **We govern it.** 5-tier HITL approval matrix (ADR-017, `orchestrator/approval.py`) ensures every agentic action is traceable from autonomous → HITL-approved → reviewed → snoozed → cleared.

## Framework Layer: Orchestration (O)

The orchestration layer (O in HAOMT-G-V) enables:
- Cross-department workflow automation via the Workflow Engine (`workflow/engine.py`)
- 9 workflow definitions with step tracking and SLA monitoring
- Org chart with metrics that feeds the CEO dashboard (`GET /api/v1/ceo-dashboard`)
- Agent lease + DLQ re-enqueue ensuring task reliability (`executor/dead_letter.py` + `executor/loop.py`)

## Malawi/SADC Context

For Malawi and SADC institutions, the orchestration layer must operate with:
- Sovereign data defaults (DPA 2017/2024 + GDPR by default)
- Low-bandwidth operation (offline-first, local models, WhatsApp-native queues)
- Visible variable cost (90-day pilot, no lock-in, cost per active agent)
- 30s TTL cache for org metrics (reduced bandwidth for dashboard refresh)

## Claims Traceability

| Claim | Traceable To |
|-------|-------------|
| 90 agents orchestrated via MessageBus | `src/ai_company/executor/loop.py` + `message_bus.py` |
| 20 departments with health rollup | `data_service.py` `get_executive_scorecard()` |
| 5-tier HITL governance cascades | ADR-017, `orchestrator/approval.py` |
| Orchestration enables cross-department workflow | `workflow/engine.py` step tracking + SLA monitoring |
| Live org chart with metrics feeds CEO dashboard | `graph/engine.py` `OrgNode` + `compute_org_metrics()` |
| Agent lease + DLQ re-enqueue ensures reliability | `executor/dead_letter.py` + `executor/loop.py` lease fields |

## CTA (Call to Action)

Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

## Voice Checklist (Per CEO Review)

- [ ] No emojis in text
- [ ] `™` on first mention of "LightSpeed Holdings Limited"
- [ ] Every claim traceable to registry/results/Pharos artifact
- [ ] Framework layer (H-A-O-M-T-G-V) explicitly named (here: O)
- [ ] Malawi/SADC context present (not generic)
- [ ] CTA aligned: Build / Evidence / Shape
- [ ] Voice matches "builder-writer-advocate" (professional, authoritative, first-person plural for company work)"""

# Enqueue Post 3
record = queue.enqueue(
    platform="linkedin",
    title="LightSpeed AI-native org structure",
    body=body_post3,
    notes="Post 3 of AI-Native Organizations series, approved by CEO",
)

print(f"Enqueued Post 3: {record.id}")
print(f"Platform: {record.platform}")
print(f"Title: {record.title}")
print(f"Status: {record.status}")
print(f"Char count: {len(record.body)}")
print(f"Created at: {record.created_at}")
