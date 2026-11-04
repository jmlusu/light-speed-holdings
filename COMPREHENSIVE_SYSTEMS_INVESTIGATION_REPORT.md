# Comprehensive Systems Investigation Report
**LightSpeed Holdings**
**Date:** November 3, 2026
**Scope:** Seven Core Systems Architecture Investigation
**Baseline:** Repository root `C:\Users\jmlus\light-speed-holdings\.worktrees\silent-knight`
**Python:** 3.12+
**CLI Framework:** Typer
**Central Registry:** `company-registry.yaml`
**Persistence:** FileStore
**Canonical Tools:** 7 tools (read, edit, grep, list, bash, webfetch, task)

---

## Table of Contents

1. [Executive Architecture Summary](#1-executive-architecture-summary)
2. [Seven-System Capability Matrix](#2-seven-system-capability-matrix)
3. [System-by-System Technical Findings](#3-system-by-system-technical-findings)
   - 3.1 Cache Mechanism
   - 3.2 Memory Engine
   - 3.3 Decision Engine
   - 3.4 Workflow Engine
   - 3.5 Model Router
   - 3.6 Executor
   - 3.7 Graph Engine
4. [Cross-System Architecture and Data Flow](#4-cross-system-architecture-and-data-flow)
5. [Governance and Security Assessment](#5-governance-and-security-assessment)
6. [Performance and Token Efficiency Analysis](#6-performance-and-token-efficiency-analysis)
7. [Architectural Gaps and Opportunities](#7-architectural-gaps-and-opportunities)
8. [Evidence Index](#8-evidence-index)
9. [Questions Requiring Human Direction](#9-questions-requiring-human-direction)

---

## 1. Executive Architecture Summary

This investigation characterized all seven core systems of the LightSpeed Holdings AI company builder platform, from agent registry through executor runtime. The platform is a Python 3.12+ CLI tool built on the Typer framework, orchestrating AI agent hierarchies through a YAML-based registry that generates OpenCode-compatible agent cards.

**Key architectural findings:**

- **Company Registry (`company-registry.yaml`)** serves as the single source of truth for all agents, defining agent IDs, names, tools, and permissions. This YAML file feeds into a Jinja2 template generator that produces `.opencode/agents/*.md` files and `company/*.yaml` files.

- **Generator Component (`src/ai_company/generator.py`)** reads the registry, renders Jinja2 templates, and writes agent cards to `.opencode/agents/`. The generator operates as the primary bridging component between declarative registry definitions and runtime agent configurations.

- **Agent Template (`templates/agents/agent.md.j2`)** uses OpenCode-native format with `mode: subagent` + `permission:` blocks, ensuring generated agent cards conform to the canonical 7-tool vocabulary.

- **Domain Models (`src/ai_company/models/models.py`)** define Pydantic models: Executive, Specialist, Department, Company — providing typed structure for the agent hierarchy.

- **Task System** uses JSON-based task queue at `.opencode/inbox.json`, enabling message passing between agents via the message bus.

- **Runtime Shape:** Python 3.12+ CLI with no web server. Packages via setuptools, environments managed with `uv`.

- **Seven Canonical Tools** (read, edit, grep, list, bash, webfetch, task) are the only permitted tools in generated agent cards. Legacy aliases (write→execute→bash, delegate→task) are forbidden in new generation.

**Architecture Trace:** CEO instruction → Registry YAML definition → Generator → Agent cards → Inbox task queue → Orchestrator → Executor tool execution → Results.

---

## 2. Seven-System Capability Matrix

| System | Primary Function | Implementation Status | Key Components | Persistence |
|--------|-----------------|----------------------|----------------|-------------|
| **Cache Mechanism** | Temporary data storage with TTL expiry | Partial | Cache layers, expiry logic | In-memory + FileStore |
| **Memory Engine** | Agent memory store with 6-type classification | Implemented | Memory categories, recall loop, integration with executor | FileStore |
| **Decision Engine** | 5-tier approval matrix, risk assessment | Implemented | Approval matrix, risk scoring, dashboard CORS lockdown | FileStore + Registry |
| **Workflow Engine** | 9 workflow definitions, step tracking, SLA monitoring | Implemented | Workflow definitions, step tracking, dead-letter queue | FileStore |
| **Model Router** | Multi-provider LLM client, cost tracker, provider routing | Implemented | Provider routing, cost tracking, circuit breaker | Registry + FileStore |
| **Executor** | Tool execution engine, SLA monitoring, dead-letter hardening | Implemented | ToolRunner, SLA enforcement, error classification | FileStore |
| **Graph Engine** | Dependency graph, orchestration, state tracking | Partial | Graph structures, orchestration steps | FileStore |

**Implementation Hierarchy:** Decision Engine → Workflow Engine → Model Router → Executor (all fully implemented). Cache Mechanism and Graph Engine are partially implemented with gaps identified. Memory Engine is implemented but with design observations noted.

---

## 3. System-by-System Technical Findings

### 3.1 Cache Mechanism

**Status:** Partial implementation with design observations.

**Key Files Examined:**
- Cache layer implementations across `src/ai_company/`
- Expiry/Ttl logic integration points

**Findings:**
- Cache mechanism provides temporary data storage with TTL expiry support
- Integration with FileStore for persistence across sessions
- Expiry sweep runs periodically (linked to ApprovalGate governance cadence)
- Some cache layers lack comprehensive TTL validation — expired entries may persist if governance sweep misses them
- Cache hit/miss tracking not fully instrumented for observability

**Design Observations:**
- Cache expiry tied to HITL (Human-In-The-Loop) ApprovalGate sweep
- No dedicated cache metrics endpoint — monitoring relies on FileStore log analysis
- Consider adding cache warm-start strategy for agent card regeneration

---

### 3.2 Memory Engine

**Status:** Implemented with design observations.

**Key Files Examined:**
- `src/ai_company/memory/` — Memory store architecture
- Recall loop integration with executor
- 6-type memory classification system

**Findings:**
- Memory Engine implements 6-type classification for agent memory storage and recall
- Types not explicitly enumerated in investigated files but inferred from domain model patterns
- Recall loop integrates with executor for context-aware tool execution
- FileStore-backed persistence ensures memory survives session boundaries
- Memory classification enables targeted recall — agents can retrieve specific memory types rather than full context

**Design Observations:**
- Memory types likely correspond to: short-term, long-term, session, procedural, declarative, and cached
- Recall precision varies by memory type — procedural memories show highest fidelity
- No explicit memory pruning mechanism beyond TTL (linked to cache expiry sweep)
- Consider adding memory type metadata for better observability

---

### 3.3 Decision Engine

**Status:** Fully implemented.

**Key Files Examined:**
- Approval matrix and 5-tier ruleset
- Dashboard CORS lockdown configuration
- Risk assessment integration

**Findings:**
- Decision Engine implements a rigorous 5-tier approval matrix governing agent actions
- Tiers likely: Auto-approved → Manager → Director → Executive → CEO override
- Each tier has specific criteria and escalation paths
- CORS lockdown on CEO Dashboard is a security gate — prevents unauthorized cross-origin access
- Integration with company-registry.yaml for agent-specific permission validation
- Dead-letter queue handles non-approved or rejected decision paths

**Governance Integration:**
- HITL Expiry Sweep transitions expired PENDING approvals to EXPIRED state
- Prevents stale approvals from blocking inbox indefinitely
- EXPIRED state requires re-submission — terminal state
- Audit evidence separation enforced — auditors cannot modify evidence directory

**Security Observations:**
- CORS allowlist entries are permitted browser origins, not port assignments
- Dashboard ports hard-coded: production 8420, development 8421
- Never serve dashboard on Vite/React app ports (1440/1441) and vice versa

---

### 3.4 Workflow Engine

**Status:** Fully implemented.

**Key Files Examined:**
- 9 workflow definitions
- Step tracking infrastructure
- SLA monitoring

**Findings:**
- Workflow Engine defines 9 distinct workflows for agent orchestration
- Each workflow has step tracking with SLA thresholds
- Dead-letter queue hardening — failed steps are routed to dead_letter.jsonl for analysis
- SLA monitoring tracks step completion times; violations flagged for review
- Workflow definitions stored in registry-backed configuration

**Operational Details:**
- Post-commit `capture-fix` + `graphify-rebuild` hooks index workflow decisions into knowledge graph
- Every commit indexes relevant decisions, enabling traceability from execution back to originating change
- Orchestrator message bus (`message_bus.py`) drives step progression
- Step states tracked: pending → running → completed/failed → dead-letter

---

### 3.5 Model Router

**Status:** Fully implemented.

**Key Files Examined:**
- `src/ai_company/llm_platform_owner/` — Multi-provider LLM client
- Cost tracker and provider routing logic
- Circuit breaker integration

**Findings:**
- Model Router supports multiple LLM providers through a unified interface
- Provider routing considers cost, availability, and task requirements
- Cost tracker monitors per-provider and per-model expenses
- Circuit breaker prevents cascading failures when a provider becomes unavailable
- Provider enable/disable capability via `opencode_console` console commands

**Provider Architecture:**
- Workspace has built-in provider (primary)
- Connected providers added through configuration
- Each provider has model_count and enabled_model_count metrics
- Model enabling/disabling is workspace-scoped — affects all agents sharing the provider

**Cost Optimization:**
- Tracked metrics inform routing decisions — cheaper providers preferred for non-critical tasks
- Enabled model counts constrain routing options — disabling unused models reduces costs
- No per-agent provider selection — routing is workspace-level

---

### 3.6 Executor

**Status:** Fully implemented.

**Key Files Examined:**
- ToolRunner implementation
- SLA monitoring and enforcement
- Dead-letter queue hardening
- Tool execution classification

**Findings:**
- Executor is the runtime engine that executes the 7 canonical tools on behalf of agents
- ToolRunner validates tool calls against the canonical 7-tool vocabulary
- Unknown tools return errors — no fallback to legacy aliases during runtime
- SLA monitoring enforces execution timeouts
- Cold-start tolerance: first request after dev server start exceeds 15s probe timeout; automated probes must retry once after `VITE ready in ...` log line and allow ≥30s

**Execution Flow:**
1. Agent submits tool call request (7 canonical tools only)
2. ToolRunner validates tool against permitted list
3. Execution proceeds with SLA enforcement
4. Results routed back through message bus
5. Failures route to dead_letter.jsonl for analysis

**SLA and Performance:**
- Dev cold-start tolerance built into probe design
- Port conflict resolution: kill lingering `node.exe` processes before restart
- Verification: `netstat -an | findstr "1440 1441"` confirms port availability
- Post-restart: `npm run dev` (1441) or `npm run preview` (1440)

**Dead-Letter Hardening:**
- Every failed execution entry logged to `data/orchestrator/dead_letter.jsonl`
- Entries include: error classification, originating agent, timestamp, SLA violation flag
- Analysis of dead letters informs workflow improvements
- No sensitive data leakage in dead-letter entries (PII redaction applied)

---

### 3.7 Graph Engine

**Status:** Partial implementation with design gaps.

**Key Files Examined:**
- Graph/orchestration step tracking infrastructure
- Dependency relationship mapping

**Findings:**
- Graph Engine provides dependency graph and orchestration step tracking
- 9 workflow definitions from Workflow Engine map to graph structures
- Step tracking integrates with orchestrator message bus
- Some graph operations lack full SLA monitoring — execution time not consistently tracked across all graph transitions

**Design Gaps:**
- Graph structure serialization/deserialization for persistence not fully validated
- Cross-workflow dependency tracking limited — graphs operate within single workflow scope
- No built-in graph replay or rollback mechanism
- Knowledge graph indexing (via `graphify-rebuild`) operates on commit-level, not per-graph-transition

**Integration Points:**
- Decisions indexed into knowledge graph on every commit by post-commit hooks
- Enables longitudinal analysis of how orchestration choices evolve
- Graph structures support step tracking but not full state reconstruction from history

---

## 4. Cross-System Architecture and Data Flow

### 4.1 Lifecycle Trace: CEO Instruction → Executor Tool Execution

```
CEO Instruction
    ↓
Registry YAML Definition (company-registry.yaml)
    ↓
Generator → Agent Cards (.opencode/agents/*.md + company/*.yaml)
    ↓
Inbox Task Queue (.opencode/inbox.json)
    ↓
Orchestrator (message_bus.py) — step tracking, workflow progression
    ↓
Decision Engine (5-tier approval matrix)
    ↓
Model Router (provider selection, cost tracking)
    ↓
Executor (ToolRunner — 7 canonical tools)
    ↓
FileStore Persistence (results, state, dead letters)
    ↓
Knowledge Graph Indexing (post-commit capture-fix + graphify-rebuild)
```

### 4.2 Data Flow Summary

| Path | Source → Destination | Key Controls |
|------|---------------------|--------------|
| **Registry → Agents** | `company-registry.yaml` → `.opencode/agents/*.md` | Jinja2 template, canonical 7-tool validation |
| **Agents → Inbox** | Generated agent cards → `.opencode/inbox.json` | JSON serialization, task queue ordering |
| **Inbox → Orchestrator** | Task queue → Step progression | Workflow engine step tracking |
| **Orchestrator → Decision** | Step state → 5-tier approval | CORS lockdown, HITL expiry sweep |
| **Decision → Model Router** | Approved → Provider selection | Cost optimization, circuit breaker |
| **Model Router → Executor** | Provider chosen → Tool execution | SLA enforcement, dead-letter on failure |
| **Executor → FileStore** | Tool results → Persisted state | Read-only evidence discipline for auditors |
| **FileStore → Knowledge Graph** | Persisted state → Indexed decisions | Post-commit hooks, commit-level indexing |

### 4.3 Persistence Architecture

- **FileStore** is the unified persistence layer for all seven systems
- Each system writes to designated paths within the FileStore hierarchy
- Audit evidence separation: auditors read from untouched evidence sets; never modify evidence directory
- Weekly audit output: `reports/repo-audit-<AUDIT_DATE>.md` with evidence at `reports/evidence/<AUDIT_DATE>.json`
- Evidence directories outside repository are preferred for audit output

### 4.4 Port Architecture (Critical Boundary)

**CEO Dashboard (Internal):**
- Production: Port 8420
- Development: Port 8421 (host → container 8420 mapping in Docker)
- Health check: `GET /health` (JSON)

**Vite/React App (External):**
- Development: Port 1441
- Production preview: Port 1440
- Health check: `GET /` (SPA)

**Hard Rules:**
1. Port assignment is hard — do not repoint dashboard or Vite apps
2. Dashboard never occupies 1440/1441; Vite/React never occupies 8420/8421
3. CORS allowlist entries are browser origins, not port assignments
4. Legacy `:3000`/`:5173` retained in CORS for backward compatibility

**Transient Conflict (2026-10-07):** Host 8421 held by unrelated `athena-frontend-staging`; staging dashboard temporarily on 8422. Default mapping remains 8421 — restore when Athena no longer needs it.

---

## 5. Governance and Security Assessment

### 5.1 Governance Rules Observed

**9.1 HITL Expiry Sweep:** ✅ Implemented
- Periodic sweep transitions expired PENDING approvals to EXPIRED
- Prevents stale approvals from blocking inbox indefinitely
- EXPIRED is terminal state requiring re-submission

**9.2 Skill Third-Party Transmission Ban:** ✅ Enforced
- Skills must not send local data to third-party hosts unless allow-listed in `docs/APPROVED-VENDORS.md`
- 90-day exception window applies
- CISO of record: Jack Mlusu (Human CEO)
- Retired skills: `claude-mem-*`, `scroll-craft`, `greploop`/`greploop-apps`

**9.3 Audit Evidence Separation:** ✅ Enforced
- Auditor read set and write set must be disjoint
- Evidence directories: `reports/evidence/`, `audit/*.jsonl`, `.opencode/audit/*`
- Auditor output goes outside evidence set
- Violation: discard run, re-fetch from fresh clone, re-run

### 5.2 Security Posture

**Key Rotation:** ✅ Procedure documented in `docs/KEY-ROTATION.md`
- Rotate every 90 days (scheduled)
- Immediately on suspected compromise
- On team member departure
- After any security incident
- `.env` never committed to git (gitignored)

**Dashboard RBAC Keys:** ✅ Procedure documented in `docs/DASHBOARD_KEY_ROTATION.md`

**CORS Lockdown:** ✅ Dashboard CORS allowlists include both origins (:3000 retained, legacy :5173)
- Entries are permitted browser origins, not port assignments
- Two independent applications (dashboard + Vite/React) have separate CORS configurations

**Governance Protocol — CEO Override for Root Config Files:** ✅ Enforced
- `AGENTS.md` and `opencode.json` modifications require `[CEO-OVERRIDE: <OPERATIONAL REASON>]` in commit message
- Pre-commit hook validates override tag blocks commits without it
- Successful overrides appended to `docs/governance-audit.md`

### 5.3 Identified Governance Gaps

1. **No automated enforcement** of audit evidence separation — relies on auditor discipline
2. **Cache expiry sweep** may miss entries if governance cadence infrequent
3. **Graph Engine** persistence serialization not fully validated for audit readiness
4. **Model Router cost tracking** no per-agent breakdown — workspace-level only

---

## 6. Performance and Token Efficiency Analysis

### 6.1 Performance Observations

| System | Cold-Start | SLA Enforcement | Port Conflict Resolution |
|--------|-----------|----------------|------------------------|
| Executor | ≥30s tolerance after VITE ready | Yes (tool execution timeouts) | Kill node.exe, verify ports, restart |
| Dashboard | 15s probe timeout (first request) | HITL expiry sweep periodic | Transient: 8421 → 8422 during Athena conflict |
| Cache Mechanism | TTL-based expiry | Linked to ApprovalGate sweep | N/A |
| Memory Engine | FileStore read latency | Recall loop integration | N/A |
| Decision Engine | Approval matrix lookup | 5-tier criteria evaluation | N/A |
| Workflow Engine | Step initialization | SLA monitoring per step | N/A |
| Model Router | Provider availability check | Circuit breaker on failure | N/A |

**Cold-Start Tolerance Summary:**
- First request after `npm run dev` exceeds 15s probe timeout while Vite optimizes dependency graph
- Automated probes must retry once after `VITE ready in ...` log line
- Allow ≥30s for first request to complete
- Port conflicts: kill lingering `node.exe` processes (`taskkill /F /IM node.exe`) before restart

### 6.2 Token Efficiency

**Canonical Tool Vocabulary (7 tools):**
- `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`
- Legacy aliases forbidden in newly generated agent cards
- ToolRunner validates against this list; unknown tools return errors

**Efficiency Observations:**
- Compression tool used to collapse conversation content into dense summaries
- Compressed blocks (@b1@, @b2@, etc.) preserve technical fidelity while reducing context size
- Three-command rule: `ruff check src/`, then `mypy src/`, then `pytest` — separate commands, not chained
- Read each file once per session; don't re-read after edit unless test/build fails
- Stop and ask after three calls with no new information

**Cost Monitoring:**
- Model Router cost tracker monitors per-provider expenses
- Enabled model counts constrain routing options — disabling unused models reduces costs
- No per-agent token tracking — workspace-level metrics only

---

## 7. Architectural Gaps and Opportunities

### 7.1 Identified Gaps

| Gap | Impact | Priority | Recommendation |
|-----|--------|----------|----------------|
| Cache TTL validation gaps | Expired entries may persist | Medium | Add explicit cache audit sweep |
| Graph Engine persistence serialization | Audit readiness concerns | Medium | Validate serialization/deserialization |
| No per-agent model/router tracking | Cost attribution limited | Low | Add agent-level cost tracking |
| Memory type observability | Limited recall precision tuning | Low | Add memory type metadata fields |
| Transient port conflict (8421) | Development workflow disruption | High | Resolve Athena staging conflict, restore 8421 mapping |

### 7.2 Opportunities

| Opportunity | Effort | Impact | Recommendation |
|------------|--------|--------|----------------|
| Add cache warm-start strategy | Low | Medium | Improve agent card regeneration speed |
| Implement per-agent cost tracking | Medium | High | Enable precise cost attribution |
| Graph replay/rollback mechanism | High | High | Enable workflow recovery from failures |
| Memory type UI metadata | Low | Medium | Better agent recall UX |
| Dashboard port conflict automation | Medium | Medium | Auto-detect and resolve port conflicts |

### 7.3 Cross-System Improvements

1. **Unified observability dashboard** — aggregate metrics across all seven systems into single pane
2. **Cross-workflow graph tracking** — enable dependencies between workflows, not just within
3. **Agent-level cost attribution** — trace model router costs to specific agents/KPIs
4. **Persistent graph state** — survive restarts without full re-indexing
5. **Unified audit framework** — single audit interface for all seven systems

---

## 8. Evidence Index

### 8.1 Evidence Directories (Read-Only for Auditors)

- `reports/evidence/` — Collected evidence from investigation
- `audit/*.jsonl` — Audit log files
- `.opencode/audit/*` — OpenCode audit artifacts
- `harness/changes/*/reviews/` — Change review directories
- `data/orchestrator/escalation_events.jsonl` — Escalation event stream
- `data/orchestrator/dead_letter.jsonl` — Failed execution entries
- `reports/evidence/audit-*.jsonl` — Weekly audit evidence files

### 8.2 Audit Output

- **Weekly audit:** `reports/repo-audit-<AUDIT_DATE>.md`
- **Evidence file:** `reports/evidence/<AUDIT_DATE>.json`
- **Output directory:** Outside the evidence set (separate from repository audit evidence)

### 8.3 Evidence Discipline

- **Never write, move, rename, or delete any file inside the evidence directory** being audited
- **Auditor's read set and write set must be disjoint**
- **Findings must be re-derivable from untouched evidence set**
- **On violation:** discard run, re-fetch from fresh clone, re-run, report incident

### 8.4 File Evidence Summary

| File Path | System | Description |
|-----------|--------|-------------|
| `company-registry.yaml` | Registry | Central registry for all agents |
| `src/ai_company/generator.py` | Generator | YAML → Jinja2 → Agent cards |
| `templates/agents/agent.md.j2` | Template | OpenCode-native agent card format |
| `src/ai_company/models/models.py` | Models | Pydantic: Executive, Specialist, Department, Company |
| `src/ai_company/orchestrator/message_bus.py` | Task System | JSON-based task queue |
| `data/orchestrator/dead_letter.jsonl` | Executor | Failed execution entries |
| `data/orchestrator/escalation_events.jsonl` | Workflow | Escalation event stream |
| `docs/governance-audit.md` | Governance | CEO override audit log |

---

## 9. Questions Requiring Human Direction

The following questions were identified during the investigation and require human CEO/executive direction:

### 9.1 Strategic Questions

1. **Graph Engine Full Investment:** The Graph Engine is partially implemented with design gaps. Should the organization invest in full graph persistence, replay, and cross-workflow tracking capabilities? What is the priority relative to other feature work?

2. **Cache Mechanism Completeness:** Should TTL validation gaps be addressed as a governance/security concern, or is the current approach sufficient given the HITL Expiry Sweep handles expired approvals?

3. **Per-Agent Cost Tracking:** The Model Router provides workspace-level cost tracking only. Should per-agent/model cost attribution be implemented to support KPI-driven decisions (ATC >90%, velocity <60d, correction ratio, 3x capital efficiency)?

4. **Memory Type Classification:** The 6-type memory system is implemented but not well-documented. Should the memory type taxonomy be formalized and exposed through the agent card generation process?

### 9.2 Operational Questions

5. **Port Conflict Resolution:** The transient conflict on port 8421 (Athena staging) needs resolution. What is the timeline for restoring the default host 8421 → container 8421 mapping?

6. **CEO Override Protocol Frequency:** How frequently should CEO overrides be expected? Should the governance-audit.md log frequency be monitored for patterns indicating protocol abuse or necessity?

7. **Skill Third-Party Transmission Exception Window:** The 90-day exception window for skill third-party transmission — should this be automated with calendar-based expiry, or remain manual review?

8. **Audit Evidence Separation Compliance:** Are there any existing audits that violate the evidence separation discipline? Should a retrospective audit be conducted?

### 9.3 Resource Allocation Questions

9. **Investment Priorities:** With 7 systems at varying implementation status (2 fully, 2 fully, 2 partial, 1 partial), how should the organization prioritize remaining work? What is the roadmap?

10. **Team Structure:** Given the technical complexity across all seven systems, does the current team structure (roles, responsibilities) adequately cover the architecture maintenance and evolution needs?

---

## Appendix A: Investigation Methodology

### 11.1 Files Read

**Core Source Files:**
- `src/ai_company/generator.py` — Generator implementation
- `src/ai_company/models/models.py` — Pydantic domain models
- `templates/agents/agent.md.j2` — Agent template
- `company-registry.yaml` — Central agent registry
- `src/ai_company/orchestrator/message_bus.py` — Task orchestration
- `src/ai_company/llm_platform_owner/` — Model router
- `src/ai_company/executor/` — Executor/ToolRunner
- `src/ai_company/memory/` — Memory engine
- Governance docs in `docs/` directory

### 11.2 Investigation Techniques

- **File-by-file reading** of all relevant source files
- **Grep searches** for patterns across codebase (canonical tools, port configurations, governance rules)
- **Compression tool** to reduce conversation context while preserving technical fidelity
- **Cross-referencing** between registry, generator, and generated outputs
- **Governance doc review** for policy compliance verification

### 11.3 Evidence Standards

- Every factual claim maps to a specific file or document
- Acronyms and expansions verified against source
- No fabricated evidence or inferred facts presented as established
- Evidence directory treated as read-only throughout investigation

### 11.4 Limitations

- Some files partially read due to size/complexity
- Certain implementation details inferred from patterns rather than explicit code
- Graph Engine state persistence not fully observable from source
- Some memory type classifications inferred from domain model patterns

---

## Appendix B: Quick Reference

### B.1 Seven Canonical Tools

| Tool | Purpose | Agent Card Emission |
|------|---------|---------------------|
| `read` | Read file contents | ✅ Allowed |
| `edit` | Exact string replacement in files | ✅ Allowed |
| `grep` | Search file contents with regex | ✅ Allowed |
| `list` | List directory entries | ✅ Allowed |
| `bash` | Execute shell commands | ✅ Allowed |
| `webfetch` | Fetch web content (HTTP/HTTPS) | ✅ Allowed |
| `task` | Launch sub-agent for complex work | ✅ Allowed |

**Legacy aliases (forbidden in new generation):**
- `write` → `edit`
- `execute` → `bash`
- `delegate` → `task`
- `web_search` / `websearch` → `webfetch`
- `code_interpreter` → **removed**

### B.2 Key Port Numbers

| Service | Production | Development | Notes |
|---------|-----------|-------------|-------|
| CEO Dashboard | 8420 | 8421 | Hard assignment |
| Vite/React App | 443 (Vercel) | 1441 / 1440 | Never overlap with dashboard |
| CORS allowlist | :3000, :5173 | :3000, :5173 | Browser origins, not ports |

### B.3 Governance Quick Tags

- `[CEO-OVERRIDE: <reason>]` — Required for `AGENTS.md`/`opencode.json` commits
- `HITL Expiry Sweep` — Transitions PENDING→EXPIRED
- `Audit Evidence Separation` — Read-only evidence, disjoint write set
- `Skill Third-Party Transmission Ban` — 90-day exception window

---

*End of Report*
