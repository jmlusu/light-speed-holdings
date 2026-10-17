## Claim-to-Source Map - Post 5: AI Agents for Malawian SMEs

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
| 90-day pilot can validate V layer on one department before institution-wide rollout | Series-wide policy | ✅ |
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
| Start with 8-12 agents, prove output, then scale | Series design principle | ✅ |
| One queue before any agents, even file-backed | Series design principle | ✅ |
| Utilization from day one, KPI-003 is cheapest sensor | Series design principle | ✅ |
| Install gates before autonomy, earn per action class | Series design principle | ✅ |
| Scale on evidence, each step registry-approved | Series design principle | ✅ |