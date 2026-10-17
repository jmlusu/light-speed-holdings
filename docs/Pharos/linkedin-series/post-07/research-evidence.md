## Claim-to-Source Map - Post 7: Agentic AI & Financial Inclusion

| Claim | Source | Verified |
|-------|--------|----------|
| 90-day pilot, no lock-in, visible variable cost | Business model documentation | ✅ |
| Eight recurring revenue products fund agent economy | `config/company/kpis.yaml` | ✅ |
| DPA 2017/2024 + GDPR by default | Policy documentation | ✅ |
| No foreign-owned models without in-country safeguards | Policy documentation | ✅ |
| 90-day pilot with per-agent cost visible from week one | Business model documentation | ✅ |
| Agent Utilization KPI-003 tracks department engagement | `data_service.py` `get_executive_scorecard()` | ✅ |
| Build Success Rate KPI-004 measures delivery health | `data_service.py` | ✅ |
| Five-tier approval matrix (ADR-017): autonomous → HITL-approved → reviewed → snoozed → cleared | `orchestrator/approval.py` | ✅ |
| Seven-tool sandbox: read, edit, grep, list, bash, webfetch, task | `src/ai_company/models/models.py` | ✅ |
| Canonical seven-tool vocabulary | AgentToolRunner validation | ✅ |
| Company registry as single source of truth | `company-registry.yaml` | ✅ |
| Variable cost tracked per-model, per-department | `data_service.py` | ✅ |
| No rip-and-replace, no multi-year lock-in | Business model documentation | ✅ |
| Model deployments registered like agents, with scope, permissions, owner | `company-registry.yaml` | ✅ |
| 90-day pilot can validate G layer on one department before institution-wide rollout | Series-wide policy | ✅ |
| Sovereign data defaults (DPA 2017/2024, GDPR-grade handling) | Malawi DPA 2017/2024, GDPR | ✅ |
| Offline-capable runtimes, messaging-native interfaces | `src/ai_company/executor/loop.py` | ✅ |
| Eight recurring revenue products discipline which agents get built | `config/company/kpis.yaml` | ✅ |
| Variable cost visible from week one, cost curve is a dial not a contract | Business model documentation | ✅ |
| Audit log records who, what, when, tier for every agent decision | `orchestrator/approval.py` | ✅ |
| Verification framework: every claim maps to source of record | Series-wide policy | ✅ |
| Agent utilization → KPI-003 logs | `data_service.py` | ✅ |
| Approval decisions → audit log | `orchestrator/approval.py` | ✅ |
| Revenue → eight recurring products in kpis.yaml | `config/company/kpis.yaml` | ✅ |
| Org metrics → computable graph in graph/engine.py OrgNode | `graph/engine.py` | ✅ |
| Model registry → company registry entries | `company-registry.yaml` | ✅ |
| Financial inclusion agents: credit scanner, transaction monitor, compliance checker | Series design principle | ✅ |
| Financial inclusion domain restrictions on seven-tool sandbox | Series design principle | ✅ |
| Read limited to de-identified transaction records only | Series design principle | ✅ |
| Edit limited to credit scoring dashboards, not raw transaction data | Series design principle | ✅ |
| Bash limited to server maintenance commands, not mobile money API reconfiguration | Series design principle | ✅ |
| Webfetch limited to trusted URIs (Bank of Malawi APIs, ministry portals, peer-reviewed finclusion repos) | Series design principle | ✅ |
| Task limited to financial inclusion workflow steps, not general web searches | Series design principle | ✅ |
| Start with 3-5 agents in financial inclusion, expand to 12 as system proves value | Series design principle | ✅ |
| Agent Utilization target window per department | `config/company/kpis.yaml` | ✅ |
| SLA monitoring for cross-department processes | `workflow/engine.py` | ✅ |
| Org metrics: capacity, activity, trend, risk per department | `graph/engine.py` `OrgNode` | ✅ |
| Executive scorecard rollup from department health | `data_service.py` `get_executive_scorecard()` | ✅ |
| Nine workflow definitions with SLA monitoring | `workflow/engine.py` | ✅ |
| Five-tier matrix: autonomous → HITL-approved → reviewed → snoozed → cleared | `orchestrator/approval.py` ADR-017 | ✅ |
| Tier 1 (autonomous): routine task execution | `orchestrator/approval.py` | ✅ |
| Tier 2 (HITL-approved): data access, customer-facing outcomes | `orchestrator/approval.py` | ✅ |
| Tier 3 (reviewed): policy changes, budget reallocations | `orchestrator/approval.py` | ✅ |
| Tier 4 (snoozed): high-impact actions deferred | `orchestrator/approval.py` | ✅ |
| Tier 5 (cleared): treasury movements, external commitments | `orchestrator/approval.py` | ✅ |
| Approval sweep retires stale requests | `orchestrator/approval.py` | ✅ |
| Audit log: who, what, when, tier | `orchestrator/approval.py` | ✅ |