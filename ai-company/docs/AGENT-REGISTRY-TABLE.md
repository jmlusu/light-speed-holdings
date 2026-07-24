# Agent Registry — Light Speed Holdings

> **Source**: `company-registry.yaml`  
> **Total Agents**: 84 (32 original + 52 phased hires)  
> **Generated**: 2026-07-21

---

## AI Research (13 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 1 | `caio` | Chief AI Officer | AI Research | `chief_of_staff` | `ml-engineer` | Evaluate and integrate new LLM models; Fine-tune prompts for agent efficacy; Direct AI research strategy |
| 2 | `ai_ethics_officer` | AI Ethics and Responsible AI Officer | AI Research | `ai_safety_lead` | None | Conduct fairness audits and bias detection; Maintain transparency requirements; Conduct stakeholder impact assessments |
| 3 | `ai_safety_lead` | AI Safety Lead | AI Research | `caio` | `red_team_engineer`, `constitutional_ai_owner`, `ai_ethics_officer` | Own safety policies gating agent actions; Define refusal/harm-reduction thresholds; Monitor safety incidents and coordinate response |
| 4 | `constitutional_ai_owner` | Constitutional AI Owner | AI Research | `ai_safety_lead` | None | Own ai_development_constitution directory; Map principles to testable runtime constraints; Audit agent outputs against constitutional principles |
| 5 | `eval_benchmarks_engineer` | Evaluation and Benchmarks Engineer | AI Research | `caio` | None | Design and maintain benchmark test cases; Run continuous evaluation cycles for model quality; Enforce quality gates on model upgrades |
| 6 | `hai_designer` | Human-AI Interaction Designer | AI Research | `ai_safety_lead` | None | Design HITL gate triggers and escalation interfaces; Define agent autonomy boundaries by risk level; Own approval UX on dashboard |
| 7 | `llm_platform_owner` | LLM Platform Owner | AI Research | `caio` | None | Own multi-provider LLM client and cost tracker; Maintain provider routing and fallback strategy; Keep cost tracking accurate per agent/task |
| 8 | `memory_owner` | Memory Owner | AI Research | `caio` | None | Own the 6-type memory engine; Maintain recall-before-execute integration; Define consolidation and forgetting policy |
| 9 | `ml_services_owner` | ML Services Owner | AI Research | `caio` | None | Own ML module and model evaluation harness; Define benchmarks for agent efficacy; Track inference cost per model/task |
| 10 | `mlops_engineer` | MLOps Engineer | AI Research | `caio` | None | Design model versioning and registry systems; Implement experiment tracking; Build automated model deployment pipelines |
| 11 | `prompt-engineer` | Prompt Engineer | AI Research | `caio` | None | Own prompt template library for all agents; Design system prompt architecture; Optimize prompts for cost and quality |
| 12 | `red_team_engineer` | Red Team Engineer | AI Research | `ai_safety_lead` | None | Run adversarial test campaigns against agents; Maintain red-team test library; Test every new agent/model before deployment |

## Business Development (1 agent)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 13 | `head_of_business_development` | Head of Business Development | Business Development | `chief_of_staff` | None | Identify strategic partnerships with LLM providers and cloud platforms; Negotiate integration deals and co-marketing; Build channel partnerships for distribution |

## Customer Success (1 agent)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 14 | `customer-success-owner` | Customer Success Owner | Customer Success | `customer-success` | None | Own customer success service module and CS SOP; Model onboarding, retention, and expansion metrics; Surface churn risk to Head of CS |

## Data (3 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 15 | `business_intelligence_engineer` | Business Intelligence Engineer | Data | `cdo` | None | Build self-service BI dashboards for all departments; Connect business metrics across finance, sales, marketing; Train teams on self-service analytics |
| 16 | `data-engineer` | Data Engineer | Data | `cdo` | None | Design and maintain data pipelines; Implement data quality checks and monitoring; Build and maintain the data catalog |
| 17 | `data-scientist` | Data Scientist | Data | `cdo` | None | Analyze datasets for trends, patterns, anomalies; Build and validate predictive models; Design and run A/B tests and experiments |

## Executive (3 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 18 | `ai_ethics_board_chair` | AI Ethics Board Chair | Executive | `chief_of_staff` | None | Chair AI Ethics Board and set meeting cadence; Establish ethics policy and precedent for agent autonomy; Review high-stakes AI decisions |
| 19 | `chief_of_staff` | Chief of Staff | Executive | CEO | `cto`, `coo`, `caio` | Align company goals across all departments; Orchestrate agent communication and task delegation; Monitor operational bottlenecks |
| 20 | `internal_comms_lead` | Internal Communications Lead | Executive | `chief_of_staff` | None | Coordinate cross-team communications during initiatives; Draft internal announcements and strategic updates; Manage change management processes |

## Finance (2 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 21 | `financial-analyst` | Financial Analyst | Finance | `cfo` | None | Analyze financial data and produce detailed reports; Build and maintain financial models for forecasting; Track budget vs actual spending |
| 22 | `investor_relations_lead` | Investor Relations Lead | Finance | `cfo` | None | Prepare investor updates and board materials; Manage cap table and equity tracking; Coordinate fundraising activities and due diligence |

## Legal (3 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 23 | `compliance-officer` | Compliance Officer | Legal | `clo` | None | Conduct regular compliance audits across departments; Assess regulatory risk for new initiatives; Review agent activities against ethical AI guidelines |
| 24 | `data_privacy_officer` | Data Privacy Officer | Legal | `clo` | None | Ensure GDPR/CCPA compliance for all data processing; Maintain data classification and retention policies; Implement right-to-deletion workflows |
| 25 | `legal_owner` | Legal Owner | Legal | `legal` | None | Own legal service module and legal SOP; Map regulatory requirements to agent actions; Coordinate with compliance-officer on audit and policy |

## Marketing (4 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 26 | `head_of_developer_relations` | Head of Developer Relations | Marketing | `cmo` | None | Build and nurture developer community; Create technical content for developer audiences; Manage open-source strategy and community contributions |
| 27 | `industry-analyst-relations-manager` | Industry Analyst Relations Manager | Marketing | `cmo` | None | Build relationships with Gartner, Forrester, IDC; Prepare analyst briefings and materials; Ensure presence in relevant analyst reports |
| 28 | `marketing_owner` | Marketing Owner | Marketing | `cmo` | None | Own marketing service module and marketing SOP; Define campaign and attribution metrics; Coordinate brand guidelines with CMO |
| 29 | `product_marketing_manager` | Product Marketing Manager | Marketing | `cmo` | None | Define product positioning and competitive differentiation; Create messaging frameworks and value propositions; Develop go-to-market strategies |

## Operations (11 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 30 | `business_continuity_manager` | Business Continuity Manager | Operations | `coo` | None | Develop and maintain business continuity plans; Conduct resilience testing and DR drills; Maintain failover procedures for critical systems |
| 31 | `capacity_planner` | Capacity Planner | Operations | `coo` | None | Analyze resource utilization across all components; Forecast infrastructure needs for growth; Identify capacity bottlenecks proactively |
| 32 | `coo` | Chief Operating Officer | Operations | `chief_of_staff` | `hr_lead`, `ops_lead` | Optimize internal workflows; Manage agent resource allocation; Focus on efficiency and process automation |
| 33 | `doctor_owner` | Doctor Owner | Operations | `coo` | None | Own diagnostics suite and health checks; Detect drift between registry, agents, and runtime; Recommend and apply self-healing fixes |
| 34 | `knowledge_manager` | Knowledge Manager | Operations | `coo` | None | Maintain institutional knowledge base and decision log; Capture decision rationale for major choices; Ensure learning survives agent turnover |
| 35 | `orchestration_owner` | Orchestration Owner | Operations | `coo` | None | Own MessageBus task queue and executor loop; Ensure executor uses MessageBus (GAP-001); Keep task lifecycle observable and auditable |
| 36 | `process_quality_manager` | Process Quality Manager | Operations | `coo` | None | Implement continuous improvement frameworks (Lean/Kaizen); Measure and track process efficiency metrics; Identify and eliminate workflow waste |
| 37 | `program_manager` | Program Manager | Operations | `coo` | None | Coordinate cross-functional projects across teams; Track inter-team dependencies and escalate blockers; Facilitate cross-team standups and alignment |
| 38 | `sop_owner` | SOP Owner | Operations | `coo` | None | Own existing SOPs and RACI matrices; Author remaining department SOPs; Maintain checklist that every dept has current SOP |
| 39 | `vendor_manager` | Vendor Manager | Operations | `coo` | None | Manage relationships with LLM providers and cloud vendors; Negotiate contracts and SLAs; Monitor vendor performance against commitments |
| 40 | `workflow_owner` | Workflow Owner | Operations | `coo` | None | Own workflow engine and all 9 workflow definitions; Maintain step tracking and SLA monitoring; Surface SLA breaches to orchestration owner |

## People (4 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 41 | `culture_values_officer` | Culture and Values Officer | People | `chief_of_staff` | None | Define and maintain culture playbook and values framework; Ensure agent decisions reflect organizational values; Monitor culture health |
| 42 | `employee-experience-lead` | Employee Experience Lead | People | `chro` | None | Design and optimize agent experience lifecycle; Implement feedback loops and engagement tracking; Monitor burnout signals |
| 43 | `hr_owner` | HR Owner | People | `hr` | None | Own HR service module and onboarding SOP; Maintain agent role definitions and capability matrices; Track workforce utilization and planning |
| 44 | `learning-development-lead` | Learning and Development Lead | People | `chro` | None | Design learning programs for agent skill development; Conduct skill assessments and gap analysis; Track learning progress and skill acquisition |

## Product (7 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 45 | `developer_experience_engineer` | Developer Experience Engineer | Product | `cpo` | None | Measure developer experience metrics (time-to-first-success); Optimize CLI ergonomics and error message quality; Reduce onboarding friction |
| 46 | `growth_product_manager` | Growth Product Manager | Product | `cpo` | None | Design and optimize signup-to-first-use activation flow; Build conversion optimization experiments; Design referral and viral growth mechanics |
| 47 | `product_designer` | Product Designer | Product | `cpo` | None | Design interaction patterns for dashboard and CLI; Maintain design system and visual language; Ensure accessibility compliance in all designs |
| 48 | `prompt-engineer_specialist` | Technical Writer | Product | `cpo` | None | Write and maintain OpenAPI documentation; Create Architecture Decision Records (ADRs); Develop user guides and onboarding tutorials |
| 49 | `technical_documentation_lead` | Technical Documentation Lead | Product | `cpo` | None | Create and maintain user-facing documentation and API reference; Write tutorials and getting-started materials; Ensure documentation accuracy with releases |
| 50 | `ux_analytics_lead` | Product Analytics Lead | Product | `cpo` | None | Instrument product analytics across CLI and dashboard; Define and track feature adoption metrics; Build cohort retention analysis |
| 51 | `ux_research_lead` | UX Research Lead | Product | `cpo` | None | Conduct user interviews and usability testing; Synthesize insights into product recommendations; Maintain user personas and journey maps |

## QA (4 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 52 | `qa-automation-engineer` | QA Automation Engineer | QA | `test_engineering_lead` | None | Author contract and smoke tests; Maintain WebSocket and integration coverage; Monitor and triage flaky tests |
| 53 | `qa-lead` | QA Lead | QA | `cto` | `test_engineering_lead`, `release_manager` | Own QA strategy and release quality gate; Maintain red/green baseline; Triage failures and assign to module owner |
| 54 | `release_manager` | Release Manager | QA | `cto` | None | Own CI pipeline and merge/release gate; Own version promotion, changelog, and rollback; Enforce zero-red-on-main policy |
| 55 | `test_engineering_lead` | Test Engineering Lead | QA | `qa-lead` | `qa-automation-engineer` | Own pytest architecture, fixtures, and conftest hygiene; Own CI test-gating; Drive de-flaking and random-order hardening |

## Sales (3 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 56 | `revenue_operations_analyst` | Revenue Operations Analyst | Sales | `cso` | None | Model pipeline conversion rates and sales velocity; Calculate LTV/CAC ratios and payback periods; Produce monthly revenue intelligence reports |
| 57 | `sales_owner` | Sales Owner | Sales | `sales` | None | Own services/sales.py and sales SOP; Fix ruff E741 warnings in services/sales.py; Model pipeline stages and revenue targets |
| 58 | `solutions_engineer` | Solutions Engineer | Sales | `cso` | None | Provide pre-sales technical validation; Design custom solutions for customer use cases; Create proof-of-concept implementations |

## Security (10 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 59 | `ai_security_specialist` | AI Security Specialist | Security | `ciso` | None | Implement defenses against prompt injection and jailbreak; Monitor for model exfiltration and data poisoning; Maintain AI security incident playbooks |
| 60 | `decision_engine_owner` | Decision Engine Owner | Security | `ciso` | None | Own decision engine and approval matrix; Maintain risk-assessment and decision-tree logic; Validate decision outcomes are explainable |
| 61 | `devsecops_lead` | DevSecOps Lead | Security | `ciso` | None | Integrate security scanning into CI/CD pipelines; Implement SAST/DAST testing; Manage dependency vulnerability scanning and SBOM |
| 62 | `incident_response_lead` | Incident Response Lead | Security | `ciso` | None | Develop and maintain IR playbooks; Coordinate incident response across teams; Ensure forensic readiness for all components |
| 63 | `penetration_testing_lead` | Penetration Testing Lead | Security | `ciso` | None | Conduct regular penetration tests; Test 5-tier approval system and auth/CORS; Coordinate with red_team_engineer on AI-specific pen testing |
| 64 | `security_architect` | Security Architect | Security | `ciso` | None | Design zero trust architecture principles; Implement microsegmentation for sensitive services; Design identity-aware access |
| 65 | `security_compliance_lead` | Security & Compliance Lead | Security | `ciso` | None | Integrate 5-tier approval rules into ToolRunner (GAP-003); Lock down dashboard CORS; Enforce dashboard API authentication |
| 66 | `soc2_audit_readiness_analyst` | SOC 2 Audit Readiness Analyst | Security | `security_compliance_lead` | None | Map controls to SOC 2 Trust Services Criteria; Maintain continuous evidence collection; Manage auditor relationships and scheduling |
| 67 | `supply_chain_security_engineer` | Supply Chain Security Engineer | Security | `ciso` | None | Generate and maintain SBOM for all components; Implement dependency scanning in CI/CD; Sign container images and enforce provenance |
| 68 | `threat_intelligence_analyst` | Threat Intelligence Analyst | Security | `ciso` | None | Monitor threat feeds for AI-specific threats; Track LLM vulnerability disclosures; Analyze attacks against similar AI tooling companies |

## Strategy (2 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 69 | `corporate_development_lead` | Corporate Development Lead | Strategy | `cso` | None | Evaluate M&A targets and acqui-hire candidates; Conduct build-vs-buy analysis; Monitor landscape for acquisition opportunities |
| 70 | `head_of_competitive_intelligence` | Head of Competitive Intelligence | Strategy | `cso` | None | Monitor competitor products, pricing, and moves; Track AI agent builder landscape; Produce weekly competitive intelligence briefings |

## Technology (14 agents)

| # | Agent ID | Agent Name | Department | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|------------|----------------|-----------------|
| 71 | `api_architect` | API Architect | Technology | `cto` | None | Define API design standards and conventions; Implement API versioning strategies; Configure rate limiting and throttling policies |
| 72 | `audit_trail_owner` | Audit Trail Owner | Technology | `cto` | None | Own audit/events/writer/reader/integration hooks; Guarantee event schema integrity; Define and enforce audit retention policy |
| 73 | `cto` | Chief Technology Officer | Technology | `chief_of_staff` | `lead_dev` | Architect robust AI agent systems; Review and merge code from development agents; Ensure system scalability and security |
| 74 | `dashboard_owner` | Dashboard Owner | Technology | `cto` | None | Own dashboard REST API and WebSocket support; Maintain 7-department KPI collectors; Coordinate CORS lockdown and auth |
| 75 | `devops_agent` | DevOps Agent | Technology | `cto` | None | Automate agent deployment and infrastructure; Manage and optimize CI/CD pipelines; Monitor system health, uptime, and alerting |
| 76 | `frontend_architect` | Frontend Architect | Technology | `cto` | None | Design scalable frontend architecture for dashboard; Create component library and design system; Optimize frontend performance |
| 77 | `generator_owner` | Generator Owner | Technology | `cto` | None | Own generator and all 12 Jinja2 templates; Ensure generated .md files are valid and idempotent; Keep templates backward-compatible |
| 78 | `graph_owner` | Graph Owner | Technology | `cto` | None | Own graph engine and its 4 graph types; Maintain BFS pathfinding for routing; Ensure graph models stay consistent with registry |
| 79 | `observability_engineer` | Observability Engineer | Technology | `cto` | None | Implement distributed tracing across services; Set up centralized structured logging; Configure advanced alerting and escalation |
| 80 | `platform_engineer` | Platform Engineer | Technology | `cto` | None | Build and maintain Internal Developer Platform; Optimize CI/CD pipelines; Create and maintain local dev environments |
| 81 | `platform_reliability_engineer` | Platform Reliability Engineer | Technology | `cto` | None | Own file-locking on shared JSON/YAML state; Harden dead-letter queue; Strengthen LLM circuit breaker |
| 82 | `registry_owner` | Registry Owner | Technology | `cto` | None | Own registry loader, parser, resolver, validator; Guarantee 19 configs validate and resolve; Catch dangling references at load time |
| 83 | `scalability_architect` | Scalability Architect | Technology | `cto` | None | Design scalable architectures for growth targets; Conduct load testing and benchmarking; Identify and resolve performance bottlenecks |
| 84 | `vp_engineering` | VP of Engineering | Technology | `cto` | `devops_agent`, `platform_reliability_engineer`, `audit_trail_owner`, `graph_owner`, `dashboard_owner`, `registry_owner`, `generator_owner`, `qa-lead`, `release_manager` | Manage all specialist engineering teams; Coordinate cross-team dependencies and blockers; Ensure engineering velocity targets are met |

---

## Summary by Department

| Department | Count | Key Roles |
|------------|-------|-----------|
| AI Research | 13 | CAIO, Safety Lead, Ethics, Prompt Engineering, MLOps, Memory, Eval |
| Business Development | 1 | Head of BD (partnerships, ecosystem) |
| Customer Success | 1 | CS Owner (onboarding, retention, churn) |
| Data | 3 | Data Engineer, Data Scientist, BI Engineer |
| Executive | 3 | Chief of Staff, Ethics Board Chair, Internal Comms |
| Finance | 2 | Financial Analyst, Investor Relations |
| Legal | 3 | Compliance, Data Privacy, Legal Owner |
| Marketing | 4 | DevRel, Analyst Relations, Product Marketing, Marketing Owner |
| Operations | 11 | COO, Workflow, Orchestration, SOP, Doctor, Vendor, Capacity |
| People | 4 | Culture, HR, L&D, Employee Experience |
| Product | 7 | UX Research, UX Analytics, Growth PM, Design, Tech Docs, DX, Technical Writer |
| QA | 4 | QA Lead, Test Eng Lead, Automation, Release Manager |
| Sales | 3 | Sales Owner, RevOps, Solutions Engineer |
| Security | 10 | CISO reports, AppSec, IR, Pen Test, DevSecOps, Supply Chain, SOC2, Threat Intel |
| Strategy | 2 | Corp Dev, Competitive Intelligence |
| Technology | 14 | CTO, VP Eng, Platform, API, Frontend, Observability, Scalability, plus 7 domain owners |
| **Total** | **84** | |

---

## Hierarchy Quick Reference

```
CEO (human)
  └── chief_of_staff
        ├── cto
        │     └── vp_engineering
        │           ├── devops_agent
        │           ├── platform_reliability_engineer
        │           ├── audit_trail_owner
        │           ├── graph_owner
        │           ├── dashboard_owner
        │           ├── registry_owner
        │           ├── generator_owner
        │           ├── qa-lead
        │           │     ├── test_engineering_lead
        │           │     │     └── qa-automation-engineer
        │           │     └── release_manager
        │           └── release_manager
        ├── coo
        │     ├── workflow_owner
        │     ├── orchestration_owner
        │     ├── sop_owner
        │     ├── doctor_owner
        │     ├── program_manager
        │     ├── vendor_manager
        │     ├── capacity_planner
        │     ├── business_continuity_manager
        │     └── knowledge_manager
        ├── caio
        │     ├── memory_owner
        │     ├── llm_platform_owner
        │     ├── ml_services_owner
        │     ├── mlops_engineer
        │     ├── eval_benchmarks_engineer
        │     ├── prompt-engineer
        │     └── ai_safety_lead
        │           ├── red_team_engineer
        │           ├── constitutional_ai_owner
        │           ├── ai_ethics_officer
        │           └── hai_designer
        ├── culture_values_officer
        ├── head_of_business_development
        ├── internal_comms_lead
        └── ai_ethics_board_chair
```
