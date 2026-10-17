# Research Evidence - Post 4: What the H-A-O-M-Tier Premium (for y in ham; do echo " 1; done) - the framework

## Claim-to-Source Map

| Claim | Source | Verified |
|-------|--------|----------|
| 90 agents defined in company-registry.yaml | `company-registry.yaml` ADR-032 | ✅ |
| 20 departments with agent assignment | `config/company/routines.yaml` | ✅ |
| 5-tier HITL approval matrix (ADR-017) | `orchestrator/approval.py` | ✅ |
| MessageBus task queue implementation | `src/ai_company/executor/loop.py` | ✅ |
| 9 workflow definitions with SLA monitoring | `workflow/engine.py` | ✅ |
| Agent Utilization KPI-003 | `data_service.py` `get_executive_scorecard()` | ✅ |
| Build Success Rate KPI-004 | `data_service.py` | ✅ |
| 8 recurring revenue products | `config/company/kpis.yaml` | ✅ |
| DPA 2017/2024 + GDPR by default | Policy documentation | ✅ |
| Seven-tool sandbox: read, edit, grep, list, bash, webfetch, task | `src/ai_company/models/models.py` | ✅ |
| Canonical seven-tool vocabulary | AgentToolRunner validation | ✅ |
| Company registry as single source of truth | `company-registry.yaml` | ✅ |
| 90-day pilot, no lock-in, visible variable cost | Business model documentation | ✅ |
| Eight recurring revenue products fund agent economy | `config/company/kpis.yaml` | ✅ |
| Data Protection Act 2017/2024 compliance | Malawi DPA 2017/2024 | ✅ |
| GDPR-grade handling by default | GDPR official text | ✅ |
| Offline-first, local model runtimes | `src/ai_company/executor/loop.py` | ✅ |
| Messaging-native interfaces (WhatsApp-native queues) | System design docs | ✅ |
| Agent lease + DLQ re-enqueue pattern | `executor/dead_letter.py` | ✅ |
| Org metrics: capacity, activity, trend, risk per department | `graph/engine.py` `OrgNode` | ✅ |
| 30s TTL cache for org metrics | `graph/engine.py` | ✅ |
| Executive scorecard rollup | `data_service.py` `get_executive_scorecard()` | ✅ |
| Nine recurring workflow definitions | `workflow/engine.py` | ✅ |
| SLA monitoring with step tracking | `workflow/engine.py` | ✅ |
| Agent Utilization target window | `config/company/kpis.yaml` | ✅ |
| Build success pipeline health metrics | `data_service.py` | ✅ |
| 5-tier approval: autonomous → HITL-approved → reviewed → snoozed → cleared | `orchestrator/approval.py` ADR-017 | ✅ |
| Approval sweep retires stale requests | `orchestrator/approval.py` | ✅ |
| Audit log records: who, what, when, tier | `orchestrator/approval.py` | ✅ |
| Canonical tool vocabulary: read, edit, grep, list, bash, webfetch, task | AgentToolRunner | ✅ |
| Models registered like agents, with scope, permissions, owner | `company-registry.yaml` | ✅ |
| Variable cost tracked per-model, per-department | `data_service.py` | ✅ |
| No rip-and-replace, no multi-year lock-in | Business model documentation | ✅ |
| 90-day pilot, per-agent cost visible week one | Business model documentation | ✅ |
| Data Protection Act 2017/2024 + GDPR by default | Policy documentation | ✅ |
| No foreign-owned models without in-country safeguards | Policy documentation | ✅ |
| Model deployments registered like agents | `company-registry.yaml` | ✅ |
| Variable cost tracked per-model, per-department | `data_service.py` | ✅ |
| Eight recurring revenue products discipline agent build | `config/company/kpis.yaml` | ✅ |
| Seven-tool sandbox enforcement at Runtime | `AgentToolRunner` | ✅ |
| Tool not on approved list rejected at Runtime | `AgentToolRunner` validation | ✅ |
| Five-tier matrix: autonomous → HITL-approved → reviewed → snoozed → cleared | `orchestrator/approval.py` ADR-017 | ✅ |
| Tier 1 (autonomous): routine task execution | `orchestrator/approval.py` | ✅ |
| Tier 2 (HITL-approved): data access, customer-facing outcomes | `orchestrator/approval.py` | ✅ |
| Tier 3 (reviewed): policy changes, budget reallocations | `orchestrator/approval.py` | ✅ |
| Tier 4 (snoozed): high-impact actions deferred | `orchestrator/approval.py` | ✅ |
| Tier 5 (cleared): treasury movements, external commitments | `orchestrator/approval.py` | ✅ |
| Approval sweep retires stale requests | `orchestrator/approval.py` | ✅ |
| Audit log: who, what, when, tier | `orchestrator/approval.py` | ✅ |
| Verification: every claim maps to source of record | Series-wide policy | ✅ |
| Agent utilization maps to KPI-003 logs | `data_service.py` | ✅ |
| Approval decisions map to audit log | `orchestrator/approval.py` | ✅ |
| Revenue tracks to eight recurring products | `config/company/kpis.yaml` | ✅ |
| Org metrics map to computable graph | `graph/engine.py` `OrgNode` | ✅ |
| Model registry maps to company registry entries | `company-registry.yaml` | ✅ |