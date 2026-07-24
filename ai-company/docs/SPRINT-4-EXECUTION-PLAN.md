# Sprint 4 Execution Plan + CEO Decision Operationalization

**Date:** 2026-07-24  
**Author:** Chief of Staff  
**Status:** APPROVED FOR EXECUTION  
**Sprint 4 Start:** Day 0 = Pre-Sprint-4 Gate Closure (all 33 PRE items DONE)  
**Sprint 4 Duration:** 7 working days (Days 0–7)

---

## TABLE OF CONTENTS

1. [Sprint 4 Calendar (Day 0–7)](#a-sprint-4-calendar-day-0-through-day-7)
2. [Board Directive Tracker](#b-board-directive-tracker-decision-2)
3. [AI Ethics Board Charter (Draft)](#c-ai-ethics-board-charter-draft-decision-3)
4. [BizDev Hiring Plan](#d-bizdev-hiring-plan-decision-4)
5. [VP Engineering Authority Memo](#e-vp-engineering-authority-memo-decision-5)
6. [Phase 4 Staggered Activation Schedule](#f-phase-4-staggered-activation-plan-decision-6)
7. [Staging → Production Promotion Checklist](#g-staging--production-promotion-checklist-decision-7)

---

## A. SPRINT 4 CALENDAR (DAY 0 THROUGH DAY 7)

### Critical Path Analysis

| Phase | Item | Effort | Owner | Blockers |
|-------|------|--------|-------|----------|
| **Pre-Sprint Gate** | PRE-01–PRE-20 (33 items) | 61h | Various | **MUST COMPLETE BEFORE DAY 0** |
| **Day 0 (Gate Day)** | PRE-01 Memory Encryption | 0.5h | security_engineer | None |
| **Sprint 4 Core** | PRE-08 Structured Logging (GAP-018) | 6h | lead-backend | PRE-13 (print removal) |
| **Sprint 4 Core** | PRE-14 OAuth2/Key Rotation | 6h | security_engineer | PRE-02 (WS auth) |
| **Sprint 4 Core** | PRE-01 Memory Encryption (PRE-01) | 0.5h | security_engineer | **Done Day 0** |

**Total Sprint 4 Scope (CEO Decision #1, Option A):** 12.5 hours  
**Pre-Sprint-4 Gate:** 61 hours (33 items, see PRE-SPRINT-4-BACKLOG.md)

---

### Day-by-Day Sprint 4 Calendar

| Day | Date | Focus | Activities | Owner | Exit Criteria |
|-----|------|-------|------------|-------|---------------|
| **Day -5 to -1** | 07-25 to 07-31 | **Pre-Sprint-4 Gate** | Execute all 33 PRE items per COORDINATION-PLAN | All agents | All 17 verification gates GREEN (see COORDINATION-PLAN.md §Verification Matrix) |
| **Day 0** | 2026-08-03 | **Gate Closure + Sprint 4 Kickoff** | 1. Final verification of all PRE items<br>2. Sprint 4 kickoff standup (09:00 UTC)<br>3. **Execute PRE-01 (Memory Encryption) — 0.5h**<br>4. Sprint 4 task board created in `.opencode/inbox.json` | Chief of Staff, security_engineer | ✅ All PRE items DONE<br>✅ Memory encryption wired & tested<br>✅ Sprint 4 tasks in inbox |
| **Day 1** | 2026-08-04 | **Structured Logging (PRE-08 / GAP-018)** | 1. Configure `structlog` with JSON formatter<br>2. Add correlation ID middleware (task_id → log context)<br>3. Replace 11 `print()` calls in non-CLI code (PRE-13)<br>4. Update `DEVELOPMENT.md` with log format docs | lead-backend (lead), devops_lead (support) | ✅ `grep -r "print(" src/ai_company/ --include="*.py" | grep -v cli/ \| wc -l` = 0<br>✅ All logs JSON when `LOG_FORMAT=json`<br>✅ Correlation ID propagates task→agent→tool |
| **Day 2** | 2026-08-05 | **Structured Logging (cont.) + Testing** | 1. Integration test: task lifecycle logs correlation<br>2. Add log schema validation test<br>3. Verify dashboard log ingestion works<br>4. Ruff + mypy clean | lead-backend, qa_engineer | ✅ 1205+ tests pass<br>✅ Ruff/mypy clean<br>✅ Log correlation verified in dashboard |
| **Day 3** | 2026-08-06 | **OAuth2 / Key Rotation (PRE-14)** | 1. Implement `KeyRotationManager` in `security/key_rotation.py`<br>2. Add `keys.yaml` with `created_at`/`expires_at`/`rotated_at`<br>3. Add CLI: `ai-company keys rotate`<br>4. Support dual-key format (old + new during migration) | security_engineer, ciso (review) | ✅ Key rotation CLI works<br>✅ Dual-key migration tested<br>✅ Keys persist across restarts |
| **Day 4** | 2026-08-07 | **OAuth2 / Key Rotation (cont.) + Integration** | 1. Wire key rotation into dashboard auth (`app.py`)<br>2. Wire key rotation into WebSocket auth (`ws.py`)<br>3. Add scheduled rotation job (cron: daily 02:00 UTC)<br>4. Integration test: rotated key → existing WS connections handled | security_engineer, lead-frontend | ✅ Dashboard auth works post-rotation<br>✅ WS reconnects with new token<br>✅ Scheduled job runs without error |
| **Day 5** | 2026-08-10 | **Sprint 4 Integration Testing** | 1. Full test suite: `pytest` (target: 1205+ passing)<br>2. Security scan: `bandit -r src/`<br>3. End-to-end: task → log correlation → auth → key rotation<br>4. Ruff + mypy clean | qa-lead, release_manager | ✅ All tests pass<br>✅ Zero bandit HIGH/MEDIUM<br>✅ Ruff/mypy clean<br>✅ E2E scenario works |
| **Day 6** | 2026-08-11 | **Documentation + Sprint Review Prep** | 1. Update `docs/STATUS.md` with Sprint 4 completion<br>2. Update `docs/DEVELOPMENT.md` (logging, key rotation)<br>3. Create Sprint 4 retrospective notes<br>4. Prepare Sprint 5 backlog | chief_of_staff, technical_documentation_lead | ✅ All docs updated<br>✅ Retrospective captured<br>✅ Sprint 5 backlog drafted |
| **Day 7** | 2026-08-12 | **Sprint 4 Review + Gate to Sprint 5** | 1. Sprint Review with Human CEO (30 min)<br>2. Verify Production Promotion Criteria (Section G)<br>3. Tag `v0.4.0` if promotion criteria met<br>4. Sprint 5 planning kickoff | chief_of_staff, human_ceo | ✅ CEO sign-off<br>✅ Promotion criteria assessed<br>✅ Sprint 5 backlog approved |

---

### Sprint 4 Task Definitions (for `.opencode/inbox.json`)

```json
{
  "tasks": [
    {
      "id": "S4-01",
      "title": "Memory Encryption Integration (PRE-01)",
      "description": "Wire EncryptionKeyManager into init_memory() per PRE-01 spec",
      "assignee": "security_engineer",
      "estimated_hours": 0.5,
      "priority": "critical",
      "dependencies": [],
      "verification": "Unit test: mock EncryptionKeyManager, assert enable_encryption() called; Integration: store+recall round-trip with encryption"
    },
    {
      "id": "S4-02",
      "title": "Structured Logging with Correlation IDs (PRE-08 / GAP-018)",
      "description": "Configure structlog JSON formatter, add task_id correlation context, replace all non-CLI print() calls",
      "assignee": "lead-backend",
      "estimated_hours": 6,
      "priority": "high",
      "dependencies": [],
      "verification": "grep print() = 0; LOG_FORMAT=json produces valid JSON; correlation ID flows task→agent→tool"
    },
    {
      "id": "S4-03",
      "title": "OAuth2 / API Key Rotation (PRE-14)",
      "description": "Implement KeyRotationManager, keys.yaml schema, CLI command, scheduled rotation, dual-key migration",
      "assignee": "security_engineer",
      "estimated_hours": 6,
      "priority": "high",
      "dependencies": ["PRE-02 (WS auth)"],
      "verification": "CLI rotate works; dashboard auth survives rotation; WS reconnects with new token; cron job executes"
    }
  ]
}
```

---

## B. BOARD DIRECTIVE TRACKER (DECISION #2)

**Source:** `config/board/directives.yaml` (read 2026-07-24)

### Active Directives (5 Total)

| Directive ID | Title | Status | Priority | Issued By | Issued | Deadline | Owner | SLA | Notes |
|--------------|-------|--------|----------|-----------|--------|----------|-------|-----|-------|
| **DIR-2026-001** | Establish Agent Deployment Pipeline | ✅ Completed | Critical | human-ceo | 2026-07-18 | 2026-07-22 | cto | 4 days | All 127 agents deployed |
| **DIR-2026-002** | Implement Audit Trail for Executor | ✅ Completed | Critical | board-chair | 2026-07-18 | 2026-07-20 | cto | 2 days | Audit module + CLI done |
| **DIR-2026-003** | Complete Sprint 3 | ✅ Completed | High | human-ceo | 2026-07-21 | 2026-07-23 | chief-of-staff | 2 days | 1205 tests, v0.3.0 tagged |
| **DIR-2026-004** | **Launch Sprint 4 - Quality & Completeness** | ⏳ **Pending** | **High** | **human-ceo** | **2026-07-23** | **2026-07-30** | **chief-of-staff** | **7 days** | **THIS PLAN OPERATIONALIZES IT** |
| **DIR-2026-005** | Establish Board Directive Tracking System | ✅ Completed | Medium | human-ceo | 2026-07-23 | 2026-07-23 | chief-of-staff | 0 days | YAML + CLI + docs done |

### Directive DIR-2026-004 — Sprint 4 Launch (Owner: Chief of Staff)

**SLA:** 7 days from Sprint 4 start (Day 0)  
**Tracking Mechanism:**
1. **Dashboard:** `ai-company board directives status DIR-2026-004` — shows real-time status
2. **Status File:** `docs/SPRINT-4-TRACKER.md` — updated daily by Chief of Staff
3. **CLI Command:** `ai-company board directives status DIR-2026-004` — for automation
4. **Daily Standup:** Async update in `#sprint-4` channel by 17:00 UTC

**Completion Criteria (from directive description):**
- [ ] Structured logging with correlation IDs (GAP-018) — **S4-02**
- [ ] Agent spec validation CLI — PRE-08B (Pre-Sprint-4 gate)
- [ ] CLI type hints and docstrings — PRE-Sprint-4 scope
- [ ] OAuth2/key rotation — **S4-03**
- [ ] Memory encryption — **S4-01** (also PRE-01)
- [ ] Token counting integration — PRE-11 (Pre-Sprint-4 gate)

---

## C. AI ETHICS BOARD CHARTER (DRAFT) (DECISION #3)

**Reference:** Board Charter for AI Ethics Board Chair (Phase 4 role: `ai_ethics_board_chair` in `company-registry.yaml:1815-1832`)  
**Backup Agent Spec:** `backup/.opencode-backup/agents/ai_ethics_board_chair.md`

### Charter: AI Ethics Board

| Field | Definition |
|-------|------------|
| **Authority** | Established by Board of Directors under `docs/BOARD-GOVERNANCE.md` §4.3 |
| **Chair** | `ai_ethics_board_chair` (Phase 4 role, reports to Chief of Staff) |
| **Reporting Line** | Chair → Chief of Staff → Human CEO → Board Risk Committee (quarterly) |
| **Meeting Cadence** | **Monthly** (first Tuesday, 10:00 UTC) + **Ad-hoc** for high-stakes decisions |
| **Quorum** | Chair + AI Ethics Officer + AI Safety Lead + Constitutional AI Owner (4 minimum) |
| **Decision Standard** | Consensus preferred; simple majority with Chair tie-break |
| **Scope** | 1. Set AI ethics policy for agent autonomy levels<br>2. Review high-stakes AI decisions (deployment, data use, model selection)<br>3. Establish precedent for recurring ethical dilemmas<br>4. Audit agent outputs for fairness, bias, transparency<br>5. Coordinate with `ai_ethics_officer` on policy implementation |
| **Escalation Path** | Chair → Chief of Staff → Human CEO → Board Risk Committee |
| **Artifacts** | Meeting minutes (YAML), Policy decisions (ADR format), Quarterly ethics report to Board |
| **Independence** | Chair cannot be overruled by product/engineering on ethics matters; escalation only to CEO/Board |

### Charter Adoption Process

| Step | Action | Owner | Target Date |
|------|--------|-------|-------------|
| 1 | Draft charter review with AI Safety Lead, AI Ethics Officer | chief_of_staff | Day 1 (2026-08-04) |
| 2 | Legal review (CLO) for governance compliance | clo | Day 2 (2026-08-05) |
| 3 | Board Risk Committee pre-read | board_risk | Day 3 (2026-08-06) |
| 4 | Human CEO approval | human_ceo | Day 4 (2026-08-07) |
| 5 | Activate `ai_ethics_board_chair` agent (Phase 4 activation) | chief_of_staff | **Phase 4 Wave 1** (see Section F) |
| 6 | First board meeting | ai_ethics_board_chair | 30 days post-activation |

### Candidate Identification

| Candidate | Phase | Current Status | Notes |
|-----------|-------|----------------|-------|
| `ai_ethics_board_chair` | Phase 4 (Weeks 17-24) | **In registry, not yet active** | See Section F for activation schedule |
| `ai_ethics_officer` | Phase 2 (Weeks 1-8) | In registry, reports to `ai_safety_lead` | Will staff the board |
| `constitutional_ai_owner` | Phase 2 (Weeks 1-8) | In registry, reports to `ai_safety_lead` | Will staff the board |
| `ai_safety_lead` | Phase 1 (Immediate) | **Active** (deployed) | Chairs safety, coordinates with ethics board |

---

## D. BIZDEV HIRING PLAN (DECISION #4)

**Role:** Head of Business Development (Phase 2 role)  
**Registry ID:** `head_of_business_development` (`company-registry.yaml:1085-1102`)  
**Reports To:** Chief of Staff  
**Budget:** **APPROVED** by CEO  
**Department:** Business Development (new, under Chief of Staff)

### Job Description (from Registry)

> Owns outbound partnerships, ecosystem alliances, integration deals, and channel strategy for distribution. Identifies and develops strategic partnerships with LLM providers and cloud platforms. Negotiates integration deals and co-marketing arrangements. Builds channel partnerships for distribution. Manages partner relationships and ROI tracking. Reports partnership pipeline to CEO monthly.

### Hiring Plan

| Phase | Activity | Owner | Timeline | Deliverable |
|-------|----------|-------|----------|-------------|
| **1. Requisition** | Create formal req in HR system | hr_owner | Day 1 (2026-08-04) | Req ID, budget code, approval chain |
| **2. Sourcing** | Post to job boards, leverage network, engage recruiters | recruiter | Days 1-10 | 20+ qualified candidates |
| **3. Screen** | Phone screens (30 min) — culture, BD experience, AI knowledge | recruiter + hr | Days 5-15 | 5-8 candidates to panel |
| **4. Panel Interviews** | **Round 1:** Chief of Staff (strategy fit) + CRO (revenue)<br>**Round 2:** CTO (technical partnerships) + CISO (security)<br>**Round 3:** Human CEO (final) | chief_of_staff (lead) | Days 12-20 | Scorecards for each: ≥4/5 on all rounds |
| **5. Case Study** | "Design a partnership strategy for LSP CLI tool targeting enterprise AI teams" | chief_of_staff | Day 18 | Written submission + 30-min presentation |
| **6. Reference Checks** | 3 professional references (former partners, execs) | hr_owner | Days 19-22 | Verified |
| **7. Offer** | Comp package: Base + variable (partner revenue %) + equity | cfo + hr | Day 23 | Offer letter |
| **8. Onboarding** | 30-60-90 plan, agent registry orientation, key partner intros | hr_owner + chief_of_staff | Day 30 start | 90-day plan signed |

### Interview Loop Scorecard

| Competency | Weight | Round 1 | Round 2 | Round 3 | Case Study |
|------------|--------|---------|---------|---------|------------|
| Strategic Partnership Vision | 25% | Chief of Staff | CTO | CEO | ✅ |
| Revenue/BD Track Record | 20% | CRO | — | — | ✅ |
| Technical Fluency (AI/LLM) | 15% | — | CTO | — | ✅ |
| Security/Compliance Awareness | 10% | — | CISO | — | — |
| Cultural Alignment | 15% | Chief of Staff | — | CEO | — |
| Communication/Influence | 15% | All | All | CEO | ✅ |

**Target Start Date:** 2026-09-01 (Week 5 post-Sprint 4)

---

## E. VP ENGINEERING AUTHORITY MEMO (DECISION #5)

**Role:** VP of Engineering (`vp_engineering` in `company-registry.yaml:834-851`)  
**Phase:** 1 (Immediate) — **Already in registry, reports to CTO**  
**Direct Reports (9):** devops_lead, platform_reliability_engineer, audit_trail_owner, graph_owner, dashboard_owner, registry_owner, generator_owner, qa-lead, release_manager

### Authority Confirmation (CEO Ruling: CONFIRMED)

| Authority Area | Scope | Delegation Limit |
|----------------|-------|------------------|
| **Hiring** | All specialist roles reporting to VP Eng (9 direct + their reports) | Up to **$150k/role** annualized without CEO re-approval |
| **Budget** | Engineering tools, cloud infra, CI/CD, contractor spend | **$25k/month** discretionary; >$25k requires CFO + CEO |
| **Technical Decisions** | Architecture, tech stack, standards, debt prioritization | Full authority within engineering; cross-cutting → CTO |
| **Sprint Planning** | Owns Sprint 4+ execution for engineering workstream | Coordinates with CAIO/COO via Program Manager |
| **Performance** | Reviews for all engineering specialists | Calibration with CTO; final say on PIPs |

### Communication Plan

| Audience | Channel | Message | Timing |
|----------|---------|---------|--------|
| **All Engineering Specialists** | `#engineering` channel + email | "VP Engineering (vp_engineering) now has hiring/budget authority per CEO Decision #5. Direct reports: see registry. Escalation: VP Eng → CTO → CEO." | Day 0 (2026-08-04) |
| **CTO** | Direct message | "Authority documented. You retain architectural oversight; VP Eng owns execution layer. Weekly sync recommended." | Day 0 |
| **CFO** | Email | "VP Eng budget authority: $25k/mo discretionary. New hires up to $150k auto-approved. Track in budget system." | Day 0 |
| **HR** | HR system update | Update reporting lines: 9 specialists now report to VP Eng (not CTO). Update approval workflows. | Day 1 |

### SOP Updates Required

| SOP | File | Change |
|-----|------|--------|
| Budget Approval | `docs/sop-budget-approval.md` | Add VP Eng as approver for eng spend ≤$25k |
| Hiring | `docs/raci-hiring.md` | Add VP Eng as "A" (Accountable) for eng specialist hires |
| Deployment | `docs/sop-deployment.md` | VP Eng co-approves production releases with Release Manager |

---

## F. PHASE 4 STAGGERED ACTIVATION PLAN (DECISION #6)

**Source:** `company-registry.yaml` lines 1549–1832 (Phase 4 roles)  
**Total Phase 4 Roles:** 15 specialists  
**Activation Principle:** Stagger over Sprint 4–5 based on **dependencies met + owner assigned + tests passing**

### Phase 4 Roles Inventory

| # | Role ID | Title | Department | Reports To | Dependencies | Priority |
|---|---------|-------|------------|------------|--------------|----------|
| 1 | `prompt-engineer_specialist` | Technical Writer | Product | cpo | technical_documentation_lead active | High |
| 2 | `learning-development-lead` | Learning & Development Lead | People | hr | hr_owner active | High |
| 3 | `employee-experience-lead` | Employee Experience Lead | People | hr | hr_owner active | High |
| 4 | `investor_relations_lead` | Investor Relations Lead | Finance | cfo | cfo active, financial-analyst active | Medium |
| 5 | `revenue_operations_analyst` | Revenue Operations Analyst | Sales | cso | sales_owner active | Medium |
| 6 | `solutions_engineer` | Solutions Engineer | Sales | cso | sales_owner active | Medium |
| 7 | `corporate_development_lead` | Corporate Development Lead | Strategy | cso | head_of_business_development hired | **Medium (blocks: hire)** |
| 8 | `internal_comms_lead` | Internal Communications Lead | Executive | chief_of_staff | chief_of_staff active | High |
| 9 | `knowledge_manager` | Knowledge Manager | Operations | coo | audit_trail_owner, memory_owner active | High |
| 10 | `process_quality_manager` | Process Quality Manager | Operations | coo | workflow_owner active | High |
| 11 | `industry-analyst-relations-manager` | Industry Analyst Relations Manager | Marketing | cmo | head_of_developer_relations active | Medium |
| 12 | `hai_designer` | Human-AI Interaction Designer | AI Research | ai_safety_lead | ai_safety_lead active, dashboard_owner active | **High (safety-critical)** |
| 13 | `business_intelligence_engineer` | Business Intelligence Engineer | Data | cdo | data-engineer active, dashboard_owner active | High |
| 14 | `threat_intelligence_analyst` | Threat Intelligence Analyst | Security | ciso | ciso active, incident_response_lead active | High |
| 15 | `ai_ethics_board_chair` | AI Ethics Board Chair | Executive | chief_of_staff | ai_ethics_officer active, constitutional_ai_owner active | **Critical (Board charter)** |

### Activation Waves

| Wave | Target Sprint | Roles | Activation Criteria | Owner |
|------|---------------|-------|---------------------|-------|
| **Wave 1** | **Sprint 4 (Days 0-3)** | `internal_comms_lead`, `knowledge_manager`, `process_quality_manager`, `hai_designer`, `business_intelligence_engineer`, `threat_intelligence_analyst` | ✅ Dependencies active<br>✅ Tests pass for dependent modules<br>✅ Owner assigned (Chief of Staff) | chief_of_staff |
| **Wave 2** | **Sprint 4 (Days 4-7)** | `prompt-engineer_specialist`, `learning-development-lead`, `employee-experience-lead`, `industry-analyst-relations-manager` | ✅ Wave 1 stable<br>✅ HR/Marketing dept leads confirm capacity | hr, cmo |
| **Wave 3** | **Sprint 5 (Week 1)** | `investor_relations_lead`, `revenue_operations_analyst`, `solutions_engineer`, `corporate_development_lead` | ✅ BizDev hire started (Decision #4)<br>✅ Finance/Sales dept leads confirm | cfo, cso |
| **Wave 4** | **Sprint 5 (Week 2)** | `ai_ethics_board_chair` | ✅ AI Ethics Board Charter approved (Section C)<br>✅ Board Risk Committee briefed<br>✅ ai_ethics_officer + constitutional_ai_owner active | chief_of_staff, human_ceo |

### Activation Checklist (Per Role)

```markdown
- [ ] Dependency agents active and healthy (verify via `ai-company agents status <id>`)
- [ ] Module tests passing for dependent components (`pytest tests/ -k <module>`)
- [ ] Owner assigned and briefed (Chief of Staff or Dept Head)
- [ ] Agent generated: `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"`
- [ ] Agent deployed to `.opencode/agents/` (verify `@<agent-id>` invocable)
- [ ] Added to org chart: `ai-company company org-chart`
- [ ] Onboarding task created in inbox.json for new agent
```

---

## G. STAGING → PRODUCTION PROMOTION CHECKLIST (DECISION #7)

**Current:** Docker Compose Staging on port **9420** (`docker-compose.staging.yml`)  
**Target:** Production on port **8420**  
**Timeline:** **Post-Sprint 4** (target: 2026-08-14, Day 9)

### Promotion Criteria (ALL MUST PASS)

| Category | Criterion | Verification Command | Threshold |
|----------|-----------|----------------------|-----------|
| **Test Suite** | Full test suite passes | `pytest` | ≥1205 tests, 0 failures |
| **Test Suite** | New Sprint 4 tests pass | `pytest tests/ -k "logging or key_rotation or encryption"` | 100% pass |
| **Security** | Bandit scan clean | `bandit -r src/ -ll` | 0 HIGH, 0 MEDIUM |
| **Security** | Dependency scan clean | `pip-audit` | 0 critical vulns |
| **Code Quality** | Ruff clean | `ruff check src/` | 0 errors |
| **Code Quality** | Mypy clean | `mypy src/` | 0 errors |
| **Code Quality** | No print() in non-CLI | `grep -r "print(" src/ai_company/ --include="*.py" \| grep -v cli/ \| wc -l` | 0 |
| **Logging** | Structured JSON logs | `LOG_FORMAT=json ai-company --help \| head -5 \| jq .` | Valid JSON, has `task_id` |
| **Auth** | Dashboard fail-closed | `DASHBOARD_AUTH_MODE=closed curl -X POST /api/v1/tasks` | 401 without key |
| **Auth** | WebSocket auth | Connect to `/ws/dashboard` without token | 4001 close code |
| **Auth** | Key rotation works | `ai-company keys rotate` + verify dashboard/WS | No downtime |
| **Memory** | Encryption round-trip | `pytest tests/unit/test_memory_encryption.py::test_encrypt_decrypt_roundtrip` | Pass |
| **Performance** | API latency p95 | `locust -f load_test.py --headless -u 50 -t 60s` | p95 < 200ms |
| **Performance** | WebSocket throughput | `locust -f ws_load_test.py --headless -u 100 -t 60s` | >100 msg/sec |
| **Reliability** | Circuit breaker | `pytest tests/unit/test_circuit_breaker.py` | All 27 tests pass |
| **Reliability** | Dead letter queue | `pytest tests/ -k "dead_letter"` | All pass |
| **Dashboard** | All KPI endpoints return data | `curl -H "X-API-Key: $KEY" /api/v1/kpis/engineering` | 200 + valid JSON |
| **Dashboard** | WS broadcast works | Connect WS, trigger task, verify broadcast | Message received <100ms |

### Rollback Plan

| Trigger | Action | Owner | RTO |
|---------|--------|-------|-----|
| Any **Critical** criterion fails | **Block promotion**, create incident | release_manager | Immediate |
| Production smoke test fails post-deploy | `docker compose -f docker-compose.prod.yml down` → restart staging | devops_lead | <5 min |
| Data corruption detected | Restore from `.scripts/backup.ps1` latest | cto | <30 min |
| Security incident | Activate IR playbook (`docs/sop-incident-response.md`) | incident_response_lead | Per SOP |

### Promotion Commands

```bash
# 1. Final verification on staging
docker compose -f docker-compose.staging.yml exec app pytest
docker compose -f docker-compose.staging.yml exec app bandit -r src/
docker compose -f docker-compose.staging.yml exec app ruff check src/
docker compose -f docker-compose.staging.yml exec app mypy src/

# 2. Tag release
git tag -a v0.4.0 -m "Sprint 4: Structured logging, key rotation, memory encryption"
git push origin v0.4.0

# 3. Build production image
docker compose -f docker-compose.prod.yml build --no-cache

# 4. Deploy production (blue-green via port swap)
docker compose -f docker-compose.prod.yml up -d --scale app=2
# Verify health on :8420
# Swap nginx/traffic
docker compose -f docker-compose.prod.yml up -d --scale app=1

# 5. Post-deploy smoke tests
curl -f http://localhost:8420/health
curl -H "X-API-Key: $PROD_KEY" http://localhost:8420/api/v1/kpis/engineering
# WS test via dashboard
```

### Sign-Off Required

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Release Manager** | release_manager | | |
| **QA Lead** | qa-lead | | |
| **CTO** | cto | | |
| **CISO** | ciso | | |
| **Chief of Staff** | chief_of_staff | | |
| **Human CEO** | human_ceo | **FINAL** | |

---

## APPENDICES

### Appendix A: Key File References

| File | Purpose | Relevant Lines |
|------|---------|----------------|
| `docs/PRE-SPRINT-4-BACKLOG.md` | 33 pre-sprint items | All |
| `docs/PRE-SPRINT-4-COORDINATION-PLAN.md` | Delegation matrix, daily plan | All |
| `config/board/directives.yaml` | 5 board directives | 78-110 |
| `company-registry.yaml` | 127 agents, 4 phases | Phase 4: 1549-1832 |
| `src/ai_company/generator.py` | Agent generator | 143-174 (`generate_all`) |
| `src/ai_company/memory/integration.py` | PRE-01 target | 20-42 (`init_memory`) |
| `src/ai_company/dashboard/app.py` | PRE-03, PRE-12, PRE-14 | 100-112, 271-324 |
| `src/ai_company/dashboard/ws.py` | PRE-02 | 101-160 |
| `src/ai_company/security/key_rotation.py` | PRE-14 target | (new file) |
| `src/ai_company/security/encryption_key_manager.py` | PRE-01 dependency | (exists) |

### Appendix B: CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `ai-company board directives list` | List all directives |
| `ai-company board directives status DIR-2026-004` | Sprint 4 directive status |
| `ai-company generate` | Regenerate all agents |
| `ai-company agents validate` | PRE-08B: validate agent specs |
| `ai-company keys rotate` | PRE-14: rotate API keys |
| `ai-company status` | Project health dashboard |
| `ai-company company org-chart` | View org hierarchy |

### Appendix C: Escalation Contacts

| Issue Type | Primary | Secondary | CEO |
|------------|---------|-----------|-----|
| Security | ciso | security_engineer | human_ceo |
| Test Failure | qa-lead | test_engineering_lead | cto |
| Build/Deploy | release_manager | devops_lead | cto |
| Resource Conflict | chief_of_staff | coo | human_ceo |
| Ethics/Policy | ai_ethics_board_chair | ai_safety_lead | human_ceo |

---

**END OF DOCUMENT**

*This plan is executable as-is. All tasks reference specific files, line numbers, commands, and verification criteria. Daily standups at 09:00 UTC in #sprint-4 channel. Chief of Staff owns overall coordination.*

**Next Action:** Schedule Day 0 kickoff standup for 2026-08-03 09:00 UTC. Ensure all Pre-Sprint-4 items are GREEN before Sprint 4 starts.