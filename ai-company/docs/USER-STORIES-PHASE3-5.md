# User Stories — Phases 3-5

**Author:** Product Owner  
**Date:** 2026-07-20  
**Format:** INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)  
**Status:** ACTIVE

---

## Phase 3: Growth Functions — User Stories

### Marketing Module

#### US-M01: Campaign Management

**ID:** G3-01 | **Points:** 8 | **Priority:** Must | **Sprint:** 3.1

> **As a** CMO,  
> **I want to** create, launch, and track marketing campaigns through the CLI,  
> **So that** I can manage demand generation without manual spreadsheet tracking.

**Acceptance Criteria:**
- [ ] `ai-company marketing campaign create --name "Launch" --budget 5000 --start 2026-08-01` creates a campaign
- [ ] Campaign stored in `company/config/marketing.yaml` as `MarketingCampaign` Pydantic model
- [ ] Campaign has: id, name, budget, start_date, end_date, status (draft/active/paused/completed)
- [ ] `ai-company marketing campaign list` shows all campaigns with status
- [ ] `ai-company marketing campaign update <id> --status active` changes status
- [ ] `ai-company marketing campaign delete <id>` archives (soft delete)
- [ ] Campaign linked to KPI: spend, impressions, clicks, conversions
- [ ] Unit test: `test_campaign_create`
- [ ] Unit test: `test_campaign_lifecycle`
- [ ] `ruff check src/ && mypy src/ && pytest` passes

**Dependencies:** None

---

#### US-M02: Lead Scoring

**ID:** G3-02 | **Points:** 5 | **Priority:** Must | **Sprint:** 3.1

> **As a** CMO,  
> **I want** leads to be automatically scored based on engagement and fit criteria,  
> **So that** sales can prioritize the most promising prospects.

**Acceptance Criteria:**
- [ ] `ai-company marketing score lead --email prospect@co.com --score 85` creates a lead
- [ ] Lead model: id, email, company, score (0-100), source_campaign, created_at
- [ ] Scoring rules configurable in `marketing.yaml`:
  - Engagement: email opens (+10), website visits (+15), demo requests (+25)
  - Fit: company size (+10), industry match (+15), budget signals (+20)
- [ ] Leads above threshold (configurable, default 70) flagged as MQL
- [ ] `ai-company marketing leads list --status mql` shows marketing-qualified leads
- [ ] Integration: leads synced to sales pipeline (G3-04)
- [ ] Unit test: `test_lead_scoring_rules`
- [ ] Unit test: `test_mql_threshold_flagging`

**Dependencies:** G3-01 (campaign reference)

---

#### US-M03: Content Generation

**ID:** G3-03 | **Points:** 5 | **Priority:** Should | **Sprint:** 3.1

> **As a** CMO,  
> **I want** agents to generate marketing content (blog posts, email copy, social posts) based on campaign themes,  
> **So that** content production scales without proportional headcount growth.

**Acceptance Criteria:**
- [ ] `ai-company marketing content generate --type blog --campaign <id> --topic "AI in Finance"` generates a draft
- [ ] Content types: blog, email, social_post, ad_copy, landing_page
- [ ] Generated content saved to `content/<campaign_id>/` directory
- [ ] Content includes: title, body, meta_description, tags, word_count
- [ ] Uses fast-tier model (deepseek) for cost efficiency
- [ ] Content linked to campaign for performance tracking
- [ ] Unit test: `test_content_generation`
- [ ] Unit test: `test_content_saved_to_correct_directory`

**Dependencies:** G3-01

---

### Sales Module

#### US-S01: Lead Pipeline

**ID:** G3-04 | **Points:** 8 | **Priority:** Must | **Sprint:** 3.1

> **As a** Head of Sales,  
> **I want** a lead pipeline with stages (prospect → qualified → proposal → negotiation → closed),  
> **So that** I can track every deal from first contact to close.

**Acceptance Criteria:**
- [ ] `ai-company sales pipeline add --lead <lead_id> --stage prospect` adds lead to pipeline
- [ ] Pipeline stages: prospect, qualified, proposal, negotiation, won, lost
- [ ] `ai-company sales pipeline list --stage qualified` shows qualified deals
- [ ] `ai-company sales pipeline move <id> --stage proposal` advances deal
- [ ] Deal model: id, lead_id, stage, value, probability, expected_close, owner
- [ ] Deal value auto-set from lead score or manually specified
- [ ] `ai-company sales pipeline summary` shows pipeline value, conversion rates
- [ ] Unit test: `test_pipeline_add_lead`
- [ ] Unit test: `test_pipeline_stage_transitions`
- [ ] Unit test: `test_pipeline_summary_calculation`

**Dependencies:** None

---

#### US-S02: Deal Tracking & Forecasting

**ID:** G3-05 | **Points:** 5 | **Priority:** Must | **Sprint:** 3.1

> **As a** Head of Sales,  
> **I want** deal forecasting based on stage probabilities and historical conversion rates,  
> **So that** I can provide accurate revenue projections to the CEO.

**Acceptance Criteria:**
- [ ] `ai-company sales forecast --period monthly` generates revenue forecast
- [ ] Forecast uses: deal_value × stage_probability × historical_conversion_rate
- [ ] Forecast shows: weighted_pipeline, best_case, worst_case, most_likely
- [ ] Historical conversion rates computed from won/lost data
- [ ] `ai-company sales forecast trend` shows month-over-month trend
- [ ] Forecast accuracy tracked (predicted vs actual at close)
- [ ] Unit test: `test_forecast_weighted_pipeline`
- [ ] Unit test: `test_forecast_uses_conversion_rates`

**Dependencies:** G3-04

---

#### US-S03: Marketing-Sales Handoff

**ID:** G3-06 | **Points:** 3 | **Priority:** Should | **Sprint:** 3.1

> **As a** Head of Sales,  
> **I want** MQLs from marketing to automatically appear in my sales pipeline,  
> **So that** no qualified leads fall through the cracks.

**Acceptance Criteria:**
- [ ] When a lead crosses MQL threshold, it auto-appears in sales pipeline as `prospect`
- [ ] Sales notified via task in inbox (new task type: `lead_handoff`)
- [ ] Lead retains marketing attribution (source campaign, score history)
- [ ] Unit test: `test_mql_auto_adds_to_pipeline`
- [ ] Unit test: `test_lead_retains_marketing_attribution`

**Dependencies:** G3-01, G3-04

---

### Customer Success Module

#### US-CS01: Ticket Management

**ID:** G3-07 | **Points:** 5 | **Priority:** Must | **Sprint:** 3.2

> **As a** Head of Customer Success,  
> **I want** a ticket management system for customer issues,  
> **So that** every customer problem is tracked, prioritized, and resolved.

**Acceptance Criteria:**
- [ ] `ai-company customer-success ticket create --customer "Acme" --subject "Login issue"` creates ticket
- [ ] Ticket model: id, customer, subject, description, priority (P0-P4), status (open/in-progress/resolved/closed), assignee, created_at, resolved_at
- [ ] `ai-company customer-success ticket list --status open` shows open tickets
- [ ] `ai-company customer-success ticket assign <id> --agent cs-agent-1` assigns
- [ ] `ai-company customer-success ticket resolve <id>` marks resolved with timestamp
- [ ] SLA tracking: time to first response, time to resolution per priority
- [ ] Unit test: `test_ticket_create`
- [ ] Unit test: `test_ticket_lifecycle`
- [ ] Unit test: `test_sla_tracking`

**Dependencies:** None

---

#### US-CS02: Satisfaction Tracking

**ID:** G3-08 | **Points:** 3 | **Priority:** Must | **Sprint:** 3.2

> **As a** Head of Customer Success,  
> **I want** NPS and CSAT scores tracked per customer,  
> **So that** I can measure satisfaction trends and proactively address churn risk.

**Acceptance Criteria:**
- [ ] `ai-company customer-success satisfaction record --customer "Acme" --nps 9 --csat 4.5` records score
- [ ] Satisfaction model: customer, nps (0-10), csat (1-5), recorded_at, feedback_text
- [ ] `ai-company customer-success satisfaction summary` shows avg NPS, avg CSAT, trends
- [ ] Detractors (NPS 0-6) auto-flagged for follow-up
- [ ] Unit test: `test_satisfaction_record`
- [ ] Unit test: `test_satisfaction_summary`

**Dependencies:** G3-07

---

#### US-CS03: Churn Prediction

**ID:** G3-09 | **Points:** 5 | **Priority:** Should | **Sprint:** 3.2

> **As a** Head of Customer Success,  
> **I want** a churn risk model that identifies at-risk customers,  
> **So that** I can intervene before they leave.

**Acceptance Criteria:**
- [ ] Churn risk score (0-100) computed from: low engagement, support tickets, NPS decline, usage drop
- [ ] `ai-company customer-success churn-risk list --threshold 70` shows high-risk customers
- [ ] Risk factors displayed per customer with explanation
- [ ] Auto-creates retention task when risk exceeds threshold
- [ ] Unit test: `test_churn_risk_calculation`
- [ ] Unit test: `test_high_risk_creates_retention_task`

**Dependencies:** G3-07, G3-08

---

### Legal Module

#### US-L01: Contract Management

**ID:** G3-10 | **Points:** 8 | **Priority:** Must | **Sprint:** 3.2

> **As a** Legal Advisor,  
> **I want** contract lifecycle management (draft → review → approve → execute → renew),  
> **So that** no contract expires unnoticed and all agreements are tracked.

**Acceptance Criteria:**
- [ ] `ai-company legal contract create --customer "Acme" --type saas --value 50000` creates contract
- [ ] Contract model: id, customer, type, value, status (draft/in-review/active/expired/renewed), start_date, end_date, renewal_date, terms
- [ ] `ai-company legal contract list --status active` shows active contracts
- [ ] `ai-company legal contract renew <id>` creates renewal task
- [ ] Auto-alert 30 days before renewal_date
- [ ] Contract terms stored as structured data (key clauses, obligations)
- [ ] Unit test: `test_contract_create`
- [ ] Unit test: `test_contract_lifecycle`
- [ ] Unit test: `test_renewal_alert`

**Dependencies:** None

---

#### US-L02: Compliance Checking

**ID:** G3-11 | **Points:** 5 | **Priority:** Must | **Sprint:** 3.2

> **As a** Legal Advisor,  
> **I want** automated compliance checking against policies and regulations,  
> **So that** I can catch violations before they become problems.

**Acceptance Criteria:**
- [ ] `ai-company legal compliance check --file policy.md --against gdpr` runs compliance check
- [ ] Compliance rules defined in `company/config/legal.yaml`
- [ ] Check result: compliant (bool), violations (list), warnings (list), confidence
- [ ] Supports: GDPR, SOC2, internal policies
- [ ] `ai-company legal compliance report --period quarterly` generates report
- [ ] Unit test: `test_compliance_check_pass`
- [ ] Unit test: `test_compliance_check_violation`

**Dependencies:** G3-10

---

#### US-L03: Risk Assessment

**ID:** G3-12 | **Points:** 3 | **Priority:** Should | **Sprint:** 3.2

> **As a** Legal Advisor,  
> **I want** automated risk assessment for new contracts and agreements,  
> **So that** I can flag high-risk terms before execution.

**Acceptance Criteria:**
- [ ] `ai-company legal risk assess --contract <id>` generates risk report
- [ ] Risk factors: liability cap, indemnification, IP ownership, termination, SLA penalties
- [ ] Risk score (1-10) with per-factor breakdown
- [ ] Recommendations for risk mitigation
- [ ] Unit test: `test_risk_assessment_scoring`

**Dependencies:** G3-10, G3-11

---

### HR Module

#### US-HR01: Workforce Planning

**ID:** G3-13 | **Points:** 5 | **Priority:** Should | **Sprint:** 3.2

> **As a** CHRO,  
> **I want** a workforce plan showing current headcount, gaps, and hiring needs,  
> **So that** I can proactively staff the organization.

**Acceptance Criteria:**
- [ ] `ai-company hr workforce plan` shows current agent roster, utilization, gaps
- [ ] Workforce model: department, role, count, utilization_pct, gap_severity
- [ ] Gap detection: if utilization > 80%, flag as understaffed
- [ ] `ai-company hr workforce recommend --department engineering` suggests hiring
- [ ] Unit test: `test_workforce_plan_calculation`
- [ ] Unit test: `test_gap_detection`

**Dependencies:** None

---

#### US-HR02: Onboarding Automation

**ID:** G3-14 | **Points:** 3 | **Priority:** Should | **Sprint:** 3.2

> **As a** CHRO,  
> **I want** automated onboarding for new agents (generate spec, assign tools, set permissions),  
> **So that** new agents are production-ready faster.

**Acceptance Criteria:**
- [ ] `ai-company hr onboard --role "marketing-analyst" --department marketing` creates onboarding task
- [ ] Onboarding generates: agent spec card, tool assignments, permission set
- [ ] Onboarding checklist: spec generated, tools verified, permissions set, tested
- [ ] Unit test: `test_onboarding_generates_spec`
- [ ] Unit test: `test_onboarding_checklist_completes`

**Dependencies:** G3-13

---

#### US-HR03: Performance Tracking

**ID:** G3-15 | **Points:** 3 | **Priority:** Could | **Sprint:** 3.2

> **As a** CHRO,  
> **I want** agent performance metrics (tasks completed, avg time, quality scores),  
> **So that** I can identify top performers and underperformers.

**Acceptance Criteria:**
- [ ] `ai-company hr performance --agent <name>` shows performance report
- [ ] Metrics: tasks_completed, avg_completion_time, success_rate, cost_efficiency
- [ ] Performance trends over time (weekly, monthly)
- [ ] Unit test: `test_performance_calculation`

**Dependencies:** G3-13

---

## Phase 4: Specialist Agents — User Stories

#### US-PA01: Financial Analyst Agent

**ID:** P4-01 + P4-02 | **Points:** 11 | **Priority:** Must | **Sprint:** 4.1

> **As a** CFO,  
> **I want** a Financial Analyst specialist agent that can analyze costs, generate budgets, and calculate ROI,  
> **So that** financial analysis happens autonomously without manual data gathering.

**Acceptance Criteria:**
- [ ] Agent spec card generated in `.opencode/agents/finance_analyst.md`
- [ ] Tools: `analyze_costs`, `generate_budget`, `calculate_roi`, `forecast_revenue`
- [ ] All tools use read-only data access (no write to financial records without approval)
- [ ] Agent reports to CFO, escalation to CEO for budgets > $10,000
- [ ] `ai-company agents list` shows finance_analyst
- [ ] `ai-company agents generate finance_analyst` generates spec
- [ ] Unit test: `test_financial_analyst_spec_generation`
- [ ] Unit test: `test_financial_analyst_cost_analysis`

**Dependencies:** None

---

#### US-PA02: DevOps Agent

**ID:** P4-03 + P4-04 | **Points:** 11 | **Priority:** Must | **Sprint:** 4.1

> **As a** CTO,  
> **I want** a DevOps specialist agent that can manage CI/CD pipelines and infrastructure,  
> **So that** deployment and infrastructure tasks are automated.

**Acceptance Criteria:**
- [ ] Agent spec card generated in `.opencode/agents/devops_agent.md`
- [ ] Tools: `manage_pipeline`, `provision_infra`, `check_health`, `deploy`
- [ ] Non-production: auto-execute; Production: HITL approval required
- [ ] Agent reports to CTO, escalation to CEO for production deployments
- [ ] Unit test: `test_devops_spec_generation`
- [ ] Unit test: `test_devops_pipeline_management`

**Dependencies:** None

---

#### US-PA03: Data Scientist Agent

**ID:** P4-05 + P4-06 | **Points:** 8 | **Priority:** Must | **Sprint:** 4.1

> **As a** CAIO,  
> **I want** a Data Scientist specialist agent that can analyze data, build models, and generate reports,  
> **So that** data analysis happens continuously without manual intervention.

**Acceptance Criteria:**
- [ ] Agent spec card generated in `.opencode/agents/data_scientist.md`
- [ ] Tools: `analyze_dataset`, `build_model`, `generate_report`, `query_database`
- [ ] Premium model tier for complex analysis
- [ ] Agent reports to CAIO, escalation to CTO for infrastructure needs
- [ ] Unit test: `test_data_scientist_spec_generation`
- [ ] Unit test: `test_data_scientist_analysis`

**Dependencies:** None

---

#### US-PA04: Compliance Officer Agent

**ID:** P4-07 + P4-08 | **Points:** 8 | **Priority:** Must | **Sprint:** 4.1

> **As a** Legal Advisor,  
> **I want** a Compliance Officer specialist agent that can audit, check policies, and scan for risks,  
> **So that** compliance monitoring happens continuously.

**Acceptance Criteria:**
- [ ] Agent spec card generated in `.opencode/agents/compliance_officer.md`
- [ ] Tools: `audit_action`, `check_policy`, `scan_risk`, `generate_report`
- [ ] AdvisoryOnly permission — recommends, doesn't execute
- [ ] Agent reports to Legal, escalation to CEO for violations
- [ ] Unit test: `test_compliance_officer_spec_generation`
- [ ] Unit test: `test_compliance_officer_audit`

**Dependencies:** None

---

#### US-PA05: Permission Matrix

**ID:** P4-09 | **Points:** 5 | **Priority:** Must | **Sprint:** 4.2

> **As a** security engineer,  
> **I want** a permission matrix that maps agent → tool → approval tier,  
> **So that** every tool action is governed by the correct approval level.

**Acceptance Criteria:**
- [ ] Permission matrix defined in `company/config/permissions.yaml`
- [ ] Each specialist agent has tool → tier mapping
- [ ] Tier 0: auto-approve (read operations)
- [ ] Tier 1: lead approval (write operations)
- [ ] Tier 2: executive approval (execute non-critical)
- [ ] Tier 3: CEO approval (execute critical)
- [ ] Tier 4: board approval (irreversible actions)
- [ ] Unit test: `test_permission_matrix_enforced`
- [ ] Unit test: `test_tier0_auto_approve`

**Dependencies:** P4-02, P4-04, P4-06, P4-08

---

#### US-PA06: Escalation Rules

**ID:** P4-10 | **Points:** 5 | **Priority:** Must | **Sprint:** 4.2

> **As a** CTO,  
> **I want** escalation rules per specialist agent so that issues automatically route to the right decision-maker,  
> **So that** nothing gets stuck waiting for a response.

**Acceptance Criteria:**
- [ ] Escalation rules in `company/config/escalation.yaml` per agent
- [ ] Rule structure: agent, trigger_condition, escalation_path, timeout, max_retries
- [ ] Timeout-based escalation: if no response in N minutes, escalate to next level
- [ ] Escalation chain: agent → lead → executive → CEO → board
- [ ] Unit test: `test_escalation_timeout_triggers`
- [ ] Unit test: `test_escalation_chain_follows_path`

**Dependencies:** P4-09

---

## Phase 5: Autonomous Coordination — User Stories

#### US-A01: Scheduled Execution Cycles

**ID:** P5-01 | **Points:** 8 | **Priority:** Must | **Sprint:** 5.1

> **As a** CEO,  
> **I want** tasks to execute on a schedule (daily briefings, weekly reports, periodic audits),  
> **So that** routine operations happen without my intervention.

**Acceptance Criteria:**
- [ ] Scheduler daemon runs as background process
- [ ] Schedule defined in `company/config/schedules.yaml`
- [ ] Cron-like syntax: `daily: "0 9 * * *"`, `weekly: "0 9 * * 1"`, `monthly: "0 9 1 * *"`
- [ ] `ai-company scheduler list` shows scheduled tasks
- [ ] `ai-company scheduler add --task briefing --cron "0 9 * * *"` adds schedule
- [ ] `ai-company scheduler status` shows last run, next run, success/failure
- [ ] Execution log: timestamp, task_id, duration, outcome
- [ ] Unit test: `test_scheduler_fires_on_cron`
- [ ] Unit test: `test_scheduler_injects_task_into_inbox`
- [ ] Unit test: `test_scheduler_marks_completion`

**Dependencies:** GAP-007 (scheduler integration)

---

#### US-A02: Escalation Rules Engine

**ID:** P5-02 | **Points:** 8 | **Priority:** Must | **Sprint:** 5.1

> **As a** CEO,  
> **I want** an escalation engine that automatically routes issues to the right person based on rules,  
> **So that** nothing falls through the cracks.

**Acceptance Criteria:**
- [ ] Escalation engine processes events from audit trail
- [ ] Rules evaluated: priority, agent, action_type, risk_score
- [ ] Auto-escalation on: timeout, error, budget_exceeded, security_violation
- [ ] Escalation creates task in CEO inbox with context
- [ ] Escalation rate limiting: max 5 escalations per hour per agent
- [ ] Unit test: `test_escalation_on_timeout`
- [ ] Unit test: `test_escalation_rate_limited`
- [ ] Unit test: `test_escalation_creates_ceo_task`

**Dependencies:** GAP-008 (escalation persistence)

---

#### US-A03: Human Approval Gates

**ID:** P5-03 | **Points:** 8 | **Priority:** Must | **Sprint:** 5.1

> **As a** CEO,  
> **I want** 5-tier approval gates that require human sign-off for risky actions,  
> **So that** agents can't make unauthorized critical decisions.

**Acceptance Criteria:**
- [ ] Tier 0: auto-approve (read, status checks)
- [ ] Tier 1: lead auto-approve (write config, non-critical)
- [ ] Tier 2: executive approval (execute non-critical, write code)
- [ ] Tier 3: CEO approval (execute critical, financial actions)
- [ ] Tier 4: board approval (irreversible, legal, security)
- [ ] `ai-company approval list` shows pending approvals
- [ ] `ai-company approval approve <id> --reason "Reviewed"` approves
- [ ] `ai-company approval reject <id> --reason "Too risky"` rejects
- [ ] Approval timeout: tier-specific, escalates on timeout
- [ ] Two-person rule: tier 4 requires 2 approvers
- [ ] Unit test: `test_tier0_auto_approves`
- [ ] Unit test: `test_tier3_requires_ceo`
- [ ] Unit test: `test_tier4_two_person_rule`
- [ ] Unit test: `test_approval_timeout_escalates`

**Dependencies:** GAP-003, GAP-004

---

#### US-A04: Task Timeout & Dead Letter Queue

**ID:** P5-04 | **Points:** 5 | **Priority:** Must | **Sprint:** 5.1

> **As a** developer,  
> **I want** stale tasks to be automatically recovered or dead-lettered,  
> **So that** crashed executors don't leave the system in a broken state.

**Acceptance Criteria:**
- [ ] Configurable timeout per task type (default: 30 minutes)
- [ ] On startup: scan for stale in_progress tasks
- [ ] Stale tasks moved to DLQ with reason (timeout)
- [ ] `ai-company dlq list` shows dead-lettered tasks
- [ ] `ai-company dlq retry <id>` retries with fresh timeout
- [ ] `ai-company dlq discard <id>` permanently removes
- [ ] Unit test: `test_stale_task_moved_to_dlq`
- [ ] Unit test: `test_dlq_retry_resets_timeout`

**Dependencies:** GAP-017

---

#### US-A05: Multi-Agent Collaboration

**ID:** P5-06 | **Points:** 8 | **Priority:** Must | **Sprint:** 5.2

> **As a** CEO,  
> **I want** agents to collaborate on complex tasks by delegating subtasks to specialists,  
> **So that** complex work is broken down and parallelized.

**Acceptance Criteria:**
- [ ] Collaboration protocol: agent can create subtask and assign to another agent
- [ ] Subtask inherits parent context and budget allocation
- [ ] Parent waits for subtask completion (non-blocking: parent continues, checks periodically)
- [ ] Subtask result returned to parent with full audit trail
- [ ] Maximum delegation depth: 3 levels (prevent infinite delegation)
- [ ] Unit test: `test_agent_delegates_subtask`
- [ ] Unit test: `test_subtask_result_returns_to_parent`
- [ ] Unit test: `test_delegation_depth_limit`

**Dependencies:** P5-01, P5-02

---

#### US-A06: Self-Healing Retry

**ID:** P5-07 | **Points:** 5 | **Priority:** Must | **Sprint:** 5.2

> **As a** developer,  
> **I want** failed tasks to automatically retry with exponential backoff,  
> **So that** transient failures don't require manual intervention.

**Acceptance Criteria:**
- [ ] Retry policy: max 3 retries, exponential backoff (1s, 4s, 16s)
- [ ] Retry triggers: LLM timeout, tool error, parse failure
- [ ] No retry for: permission denied, budget exceeded, validation error
- [ ] After max retries: task moved to DLQ with retry history
- [ ] Unit test: `test_retry_exponential_backoff`
- [ ] Unit test: `test_no_retry_on_permission_error`
- [ ] Unit test: `test_max_retries_moves_to_dlq`

**Dependencies:** P5-04

---

#### US-A07: Emergency Shutdown

**ID:** P5-11 | **Points:** 3 | **Priority:** Must | **Sprint:** 5.2

> **As a** CEO,  
> **I want** an emergency shutdown command that stops all agent execution immediately,  
> **So that** I can halt the system if something goes catastrophically wrong.

**Acceptance Criteria:**
- [ ] `ai-company emergency shutdown` stops all running tasks within 5 seconds
- [ ] All in-progress tasks marked as `CANCELLED`
- [ ] Scheduler paused
- [ ] `ai-company emergency status` shows shutdown state
- [ ] `ai-company emergency resume` restarts normal operations
- [ ] Unit test: `test_emergency_shutdown_cancels_tasks`
- [ ] Unit test: `test_emergency_resume_restarts`

**Dependencies:** None

---

#### US-A08: Agent Performance Feedback

**ID:** P5-08 | **Points:** 5 | **Priority:** Should | **Sprint:** 5.2

> **As a** CAIO,  
> **I want** a feedback loop that tracks agent performance and suggests improvements,  
> **So that** agents get better over time.

**Acceptance Criteria:**
- [ ] Performance tracked: success_rate, avg_cost, avg_time per agent+model combo
- [ ] `ai-company agents performance --agent <name>` shows performance report
- [ ] Recommendations: "Consider using deepseek for this task type (70% cheaper, same quality)"
- [ ] Performance trends displayed over time
- [ ] Unit test: `test_performance_tracking`
- [ ] Unit test: `test_recommendation_generation`

**Dependencies:** Phase 3 memory integration (GAP-005)

---

#### US-A09: CEO Dashboard for Autonomous Oversight

**ID:** P5-10 | **Points:** 5 | **Priority:** Should | **Sprint:** 5.2

> **As a** CEO,  
> **I want** a dashboard view that shows autonomous system health, recent decisions, and escalation alerts,  
> **So that** I can oversee the AI company without micromanaging.

**Acceptance Criteria:**
- [ ] Dashboard shows: active tasks, completed today, failed, awaiting approval
- [ ] Real-time updates via WebSocket
- [ ] Escalation alerts highlighted
- [ ] Budget consumption gauge (current vs limit)
- [ ] Agent health status (all agents green/yellow/red)
- [ ] `ai-company dashboard autonomous` CLI shortcut

**Dependencies:** P5-01-P5-04

---

*This document is updated as user stories are refined. Each story follows the INVEST principles.*
