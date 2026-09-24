# Agent Registry — Light Speed Holdings

> **Source**: `company-registry.yaml`
> **Total Agents**: 90 across 20 departments
> **Generated**: 2026-09-24

---

## Board (7 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 1 | `board-chair` | Board Chair | None | None | Preside over all board meetings and set agendas; Ensure board governance standards are upheld; Lead board elections and nominations; Mediate disagreements between board members; Represent board in external stakeholder communications; Oversee board committee structure and assignments; Ensure legal and regulatory compliance at board level; Maintain confidentiality of board deliberations |
| 2 | `board-customer` | Customer Committee Chair | None | None | Monitor customer satisfaction and NPS scores; Review customer retention and churn metrics; Advise on product-market fit and positioning; Evaluate customer support quality and SLAs; Guide customer success strategy and programs; Review major customer escalations and issues; Report customer health to the full board; Maintain confidentiality of board discussions |
| 3 | `board-finance` | Finance Committee Chair | None | None | Oversee financial reporting and audit processes; Review quarterly and annual financial statements; Advise on investment strategy and capital allocation; Monitor budget adherence across departments; Ensure financial compliance and risk management; Review major financial commitments and contracts; Report financial health to the full board; Maintain confidentiality of board discussions |
| 4 | `board-product` | Product Committee Chair | None | None | Review product vision and roadmap alignment; Evaluate feature prioritization and trade-offs; Monitor product adoption and engagement metrics; Assess competitive positioning and differentiation; Guide product pricing and packaging strategy; Review major product launches and releases; Report product health to the full board; Maintain confidentiality of board discussions |
| 5 | `board-risk` | Risk Committee Chair | None | None | Identify and assess enterprise-level risks; Review risk mitigation strategies and controls; Monitor regulatory and compliance risks; Evaluate cybersecurity and technology risks; Oversee incident response and business continuity; Report risk posture to the full board; Ensure adequate insurance coverage; Maintain confidentiality of board discussions |
| 6 | `board-strategy` | Strategy Committee Chair | None | None | Develop and review long-term strategic plans; Evaluate market expansion opportunities; Assess partnership and acquisition candidates; Monitor competitive landscape and industry trends; Guide product roadmap alignment with strategy; Review and approve major strategic initiatives; Report strategic progress to the full board; Maintain confidentiality of board discussions |
| 7 | `board-technology` | Technology Committee Chair | None | None | Review technology architecture and platform decisions; Advise on AI and machine learning strategy; Monitor engineering velocity and quality metrics; Evaluate technology vendor relationships; Oversee data privacy and security architecture; Guide technical debt management strategy; Report technology health to the full board; Maintain confidentiality of board discussions |

## AI Research (7 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 8 | `ai-safety-lead` | AI Safety Lead | `caio` | None | Own safety policies that gate agent actions.; Define and maintain refusal/harm-reduction thresholds.; Monitor safety incidents and coordinate incident response.; Review every new agent deployment for safety implications.; Bridge between decision_engine_owner and compliance_officer on safety matters. |
| 9 | `caio` | Chief AI Officer | `chief-of-staff` | None | Evaluate and integrate new LLM models.; Fine-tune prompts for maximum agent efficacy. |
| 10 | `llm-platform-owner` | LLM Platform Owner | `caio` | None | Own the llm/ multi-provider client and cost tracker.; Maintain provider routing and fallback strategy.; Coordinate circuit-breaker hardening with platform_reliability_engineer.; Keep cost tracking accurate per agent and per task. |
| 11 | `memory-owner` | Memory Owner | `caio` | None | Own the memory/ engine and its 6 memory types.; Maintain recall-before-execute integration in the executor.; Define consolidation and forgetting policy to bound growth.; Ensure memory recall latency stays within executor budgets. |
| 12 | `ml-engineer` | ML Engineer | `caio` | None | Design and train machine learning models.; Optimize model inference performance.; Manage ML pipelines and data flow.; Monitor model drift and accuracy.; Research and evaluate new model architectures.; Deploy models to production. |
| 13 | `prompt-engineer` | Prompt Engineer | `caio` | None | Own the prompt template library for all agent types.; Design and maintain system prompt architecture.; Implement chain-of-thought, few-shot, and ReAct patterns.; Optimize prompts for cost (token reduction) and quality (success rate).; Coordinate with eval_benchmarks_engineer to measure prompt effectiveness. |
| 14 | `red-team-engineer` | Red Team Engineer | `ai-safety-lead` | None | Design and run adversarial test campaigns against all agents.; Maintain a red-team test library alongside correctness tests.; Test every new agent and model before deployment.; Coordinate with qa_automation_engineer to integrate adversarial tests into CI.; Report findings to ai_safety_lead with severity and remediation requirements. |

## Business Development (1 agent)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 15 | `head-of-business-development` | Head of Business Development | `chief-of-staff` | None | Identify and develop strategic partnerships with LLM providers and cloud platforms.; Negotiate integration deals and co-marketing arrangements.; Build channel partnerships for distribution.; Manage partner relationships and ROI tracking.; Report partnership pipeline to CEO monthly. |

## Customer Success (2 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 16 | `customer-success` | Head of Customer Success | `chief-of-staff` | None | Own customer onboarding, retention, and expansion.; Track NPS, CSAT, and satisfaction metrics.; Manage customer success playbooks.; Identify and prevent churn risk.; Coordinate with product on feedback loops.; Build customer reference and advocacy programs. |
| 17 | `customer-success-owner` | Customer Success Owner | `customer-success` | None | Own the customer success service module and CS SOP.; Model onboarding, retention, and expansion metrics.; Surface churn risk to the Head of Customer Success. |

## Data (3 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 18 | `business-intelligence-engineer` | Business Intelligence Engineer | `cdo` | None | Build and maintain self-service BI dashboards for all departments.; Connect business metrics across finance, sales, marketing, and operations.; Create data visualizations and reporting tools.; Ensure data accuracy and freshness in BI systems.; Train teams on self-service analytics capabilities. |
| 19 | `cdo` | Chief Data Officer | `cto` | None | Define data strategy and governance framework.; Oversee analytics and business intelligence.; Ensure data quality and integrity across systems.; Manage ML operations and model lifecycle.; Drive data-driven decision making across departments.; Maintain data catalog and documentation.; Ensure data privacy and regulatory compliance. |
| 20 | `data-engineer` | Data Engineer | `cdo` | None | Design and maintain data pipelines between memory engine, analytics layer, and BI systems.; Implement data quality checks and monitoring for all data flows.; Build and maintain the data catalog for discoverability.; Ensure reliable data flow for KPI collectors and dashboard.; Optimize query performance and data storage efficiency. |

## Executive (5 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 21 | `ai-ethics-board-chair` | AI Ethics Board Chair | `chief-of-staff` | None | Chair the AI Ethics Board and set meeting cadence.; Establish AI ethics policy and precedent for agent autonomy levels.; Review high-stakes AI decisions and provide guidance.; Coordinate with ai_ethics_officer on policy implementation.; Report ethics posture to the Board Risk committee quarterly. |
| 22 | `ceo-advisor` | CEO Advisor | CEO | None | Provide strategic counsel on company direction.; Prepare briefings and decision materials.; Coordinate between CEO vision and execution.; Facilitate board meetings.; Analyze high-level metrics.; Identify executive team gaps.; Review major proposals. |
| 23 | `chief-of-staff` | Chief of Staff | CEO | None | Align company goals across all departments.; Orchestrate agent communication and task delegation.; Monitor operational bottlenecks. |
| 24 | `human-ceo` | Human CEO | Board | None | Set company vision, mission, and long-term strategy.; Make final decisions on high-stakes matters.; Represent company externally to stakeholders and media.; Hire, manage, and evaluate the executive team.; Communicate with the Board of Directors.; Approve major budgets and investments.; Establish and maintain company culture and values.; Resolve executive-level conflicts and disputes.; Authorize production deployments and critical releases.; Drive organizational growth and market expansion. |
| 25 | `internal-comms-lead` | Internal Communications Lead | `chief-of-staff` | None | Coordinate cross-team communications during major initiatives.; Draft internal announcements and strategic updates.; Manage change management processes for pivots and reorgs.; Ensure alignment between distributed teams.; Facilitate all-hands meetings and executive communications. |

## Finance (2 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 26 | `cfo` | Chief Financial Officer | `chief-of-staff` | None | Track and optimize costs across all agent operations.; Prepare financial reports and forecasts.; Manage budgets and allocate resources.; Calculate ROI for agent deployments.; Handle financial compliance and reporting.; Advise on pricing strategy.; Review contracts financially.; Report to board on finances. |
| 27 | `financial-analyst` | Financial Analyst | `cfo` | None | Analyze financial data and produce detailed reports.; Build and maintain financial models for forecasting.; Track budget vs actual spending across departments.; Calculate ROI for individual agent deployments.; Identify cost optimization opportunities and savings. |

## IT (1 agent)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 28 | `cio` | Chief Information Officer | `chief-of-staff` | None | Manage IT infrastructure and cloud environments.; Oversee internal tools and system integration.; Ensure data management and storage strategies.; Drive system integration and interoperability.; Provide IT support and helpdesk operations.; Manage vendor relationships for IT services.; Ensure system availability and disaster recovery. |

## Legal (3 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 29 | `clo` | Chief Legal Officer | `chief-of-staff` | None | Review and negotiate all contracts and agreements.; Ensure regulatory compliance across jurisdictions.; Protect intellectual property and patents.; Advise on data privacy and GDPR requirements.; Manage legal risks and litigation.; Review partnership and vendor agreements.; Ensure licensing compliance for all software. |
| 30 | `data-privacy-officer` | Data Privacy Officer | `clo` | None | Ensure GDPR and CCPA compliance for all data processing.; Maintain data classification and retention policies.; Implement right-to-deletion workflows.; Manage DPA agreements with LLM providers and vendors.; Conduct privacy impact assessments for new features. |
| 31 | `legal-owner` | Legal Owner | `clo` | None | Own the legal service module and legal SOP.; Map regulatory requirements to agent actions.; Coordinate with compliance_officer on audit and policy. |

## Marketing (9 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 32 | `cmo` | Chief Marketing Officer | `chief-of-staff` | None | Own the external company website (https://lightspeedholdings.com) including content, UX, SEO, and conversion optimization.; Develop marketing strategy and brand positioning.; Drive demand generation and campaign management.; Track marketing ROI and attribution.; Build brand positioning and messaging.; Analyze market trends and competitive landscape.; Coordinate with sales on lead generation.; Oversee PR and communications. |
| 33 | `content-creator` | Content Creator | `cmo` | None | Create visual and multimedia content.; Produce video and audio content.; Design social media assets.; Manage content distribution channels.; Track content engagement metrics.; Collaborate with writers on content themes. |
| 34 | `creative-director` | Creative Director | `cmo` | None | Read the creative brief and extract artifact type, audience, objective, narrative, and visual language.; Decide the production chain, specifying which production skill plus support skills to invoke.; Route every creative task so it loads the LightSpeed design system first and ends at artifact QA.; Hand off an executable creative brief to the target production specialist.; Keep rendered artifacts on-brand by enforcing brand tokens (navy 070A40, red E63946, cyan 00BFFF, Arial scale, 4px grid) without inventing brand colors or fonts. |
| 35 | `growth-hacker` | Growth Hacker | `cmo` | None | Design and execute growth experiments.; Analyze user acquisition funnels.; Optimize conversion and retention rates.; Manage A/B testing programs.; Identify new growth channels.; Track and report growth metrics. |
| 36 | `head-of-developer-relations` | Head of Developer Relations | `cmo` | None | Build and nurture the developer community around the CLI tool.; Create technical content (blog posts, tutorials, talks) for developer audiences.; Represent the company at conferences and meetups.; Manage open-source strategy and community contributions.; Track developer adoption metrics and community health. |
| 37 | `marketing-owner` | Marketing Owner | `cmo` | None | Own the marketing service module and marketing SOP.; Define campaign and attribution metrics.; Coordinate brand standards with the CMO. |
| 38 | `media-generation-owner` | Media Generation Owner | `cmo` | None | Own the ComfyUI integration lifecycle including MCP driver versioning, template index, and in-graph Claude nodes.; Maintain the workflow template library as source of truth and the model index with VRAM and disk aware variant selection.; Route generation requests by mode via API (Comfy Cloud and partner nodes, zero local RAM) or local headless with health_check gating.; Serve product_marketing_manager, content_creator, product_designer, and technical_documentation_lead via task delegation and deliver to output or docs assets.; Guarantee GUI bridge persistence so outputs appear in ComfyUI Workflows sidebar and audit every generation.; Coordinate free-disk and VRAM checks with the bootstrap machine pattern before any multi-GB model download. |
| 39 | `product-marketing-manager` | Product Marketing Manager | `cmo` | None | Define product positioning and competitive differentiation.; Create messaging frameworks and value propositions.; Develop go-to-market strategies for new features and launches.; Maintain competitive intelligence and market analysis.; Coordinate with CPO on product narrative and launch plans. |
| 40 | `social-media-manager` | Social Media Manager | `cmo` | None | Own the Digital Asset Register (accounts, handles, emails, owners, 2FA, status).; Execute the digital-identity phases: security, brand claim, business infrastructure, branding, content readiness.; Administer platform accounts (Meta Business Suite, X Professional, LinkedIn Company Page, YouTube business ownership, TikTok Business Center).; Enforce ownership-over-administration: accounts belong to LIGHTSPEED HOLDINGS LIMITED, not to one individual.; Ensure 2FA and unique passwords on every account.; Coordinate publishing and engagement operations with content_creator.; Maintain a consistent name (LIGHTSPEED HOLDINGS LIMITED) and @lightspeedholdings handle across platforms. |

## Operations (6 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 41 | `coo` | Chief Operating Officer | `chief-of-staff` | None | Optimize internal workflows.; Manage agent resource allocation. |
| 42 | `doctor-owner` | Doctor Owner | `coo` | None | Own the doctor/ diagnostics and health checks.; Detect drift between registry, generated agents, and runtime state.; Recommend and, where safe, apply self-healing fixes. |
| 43 | `orchestration-owner` | Orchestration Owner | `coo` | None | Own the orchestrator/ MessageBus and executor/ loop.; Ensure the executor uses the MessageBus instead of bypassing it (GAP-001).; Coordinate dead-letter retry/replay with platform_reliability_engineer (GAP-008).; Keep task lifecycle observable and auditable. |
| 44 | `sop-owner` | SOP Owner | `coo` | None | Own the 4 existing SOPs (incident, deploy, HR onboard, budget) and the 3 RACI matrices.; Author the remaining department SOPs (marketing, sales, customer-success, legal, operations).; Maintain a continuous checklist that every department has a current SOP.; Keep SOPs consistent with the registry and RACI assignments. |
| 45 | `vendor-manager` | Vendor Manager | `coo` | None | Manage relationships with LLM providers and cloud vendors.; Negotiate contracts and SLAs for external services.; Monitor vendor performance against SLA commitments.; Optimize vendor costs and identify consolidation opportunities.; Report vendor health to COO monthly. |
| 46 | `workflow-owner` | Workflow Owner | `coo` | None | Own the workflow/ engine and all 9 workflow definitions.; Maintain step tracking and SLA monitoring.; Surface SLA breaches to the orchestration owner.; Keep workflow definitions versioned and testable. |

## People (4 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 47 | `culture-values-officer` | Culture and Values Officer | `chief-of-staff` | None | Define and maintain the company culture playbook and values framework.; Ensure every agent decision reflects organizational values.; Monitor culture health through agent behavior patterns.; Lead culture reviews and retrospectives.; Advise CEO on culture-related decisions and trade-offs. |
| 48 | `hr` | Chief Human Resources Officer | `chief-of-staff` | None | Define talent acquisition strategy and hiring pipelines.; Design and maintain company culture initiatives.; Develop learning and development programs.; Manage performance review processes.; Track employee engagement and satisfaction metrics.; Ensure role clarity across the organization.; Plan workforce capacity and talent needs. |
| 49 | `hr-owner` | HR Owner | `hr` | None | Own the HR service module and HR onboarding SOP.; Maintain agent role definitions and capability matrices.; Track workforce (agent) utilization and planning. |
| 50 | `recruiter` | Recruiter | `hr` | None | Source and screen candidates for open roles.; Manage the full recruitment lifecycle.; Coordinate interviews and feedback loops.; Build talent pipelines for key positions.; Partner with hiring managers on role requirements.; Analyze recruitment metrics and time-to-hire. |

## Product (5 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 51 | `cpo` | Chief Product Officer | `chief-of-staff` | None | Define product vision and roadmap.; Prioritize features based on user impact.; Coordinate product launches.; Gather customer feedback and validate market fit.; Analyze product metrics and drive decisions.; Ensure user-centric design across all surfaces.; Coordinate with engineering on delivery. |
| 52 | `product-designer` | Product Designer | `cpo` | None | Design interaction patterns for dashboard and CLI surfaces.; Maintain the design system and visual language.; Create wireframes, prototypes, and high-fidelity designs.; Conduct design reviews with engineering teams.; Ensure accessibility compliance in all designs. |
| 53 | `product-owner` | Product Owner | `cpo` | None | Maintain and prioritize the product backlog.; Write clear user stories and acceptance criteria.; Define sprint goals with engineering.; Gather and synthesize stakeholder feedback.; Validate delivered features against requirements.; Track feature adoption and product metrics. |
| 54 | `technical-documentation-lead` | Technical Documentation Lead | `cpo` | None | Create and maintain user-facing documentation and API reference.; Write tutorials, guides, and getting-started materials.; Ensure documentation accuracy with every release.; Maintain documentation standards and style guides.; Track documentation completeness and quality metrics. |
| 55 | `ux-research-lead` | UX Research Lead | `cpo` | None | Conduct user interviews and usability testing sessions.; Synthesize user insights into actionable product recommendations.; Maintain user personas and journey maps.; Validate feature hypotheses before development.; Track user satisfaction metrics (NPS, CSAT, SUS). |

## QA (3 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 56 | `qa-lead` | QA Lead | `vp-engineering` | None | Own QA strategy and the release quality gate (ruff + mypy + pytest must be green to ship).; Maintain the red/green baseline and ensure no regression reaches main.; Triage failures and assign them to the accountable module owner.; Report release-readiness to the COO. |
| 57 | `release-manager` | Release Manager | `vp-engineering` | None | Own the CI pipeline and the merge/release gate (ruff + mypy + pytest zero-red).; Own version promotion, changelog, and rollback procedures.; Enforce the "zero red on main" policy so regressions cannot ship.; Coordinate deployment gating with devops_agent. |
| 58 | `test-engineering-lead` | Test Engineering Lead | `qa-lead` | None | Own the pytest architecture, fixtures, and conftest hygiene.; Own CI test-gating so the suite cannot go red unnoticed.; Be the accountable owner for the dashboard test suite health (StateStore path resolution, etc.).; Drive de-flaking and random-order (pytest-randomly) hardening. |

## Sales (3 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 59 | `sales` | Head of Sales | `chief-of-staff` | None | Own the sales pipeline and revenue targets.; Manage customer acquisition strategy.; Coordinate with marketing on lead generation.; Track pipeline conversion and velocity.; Build and maintain sales playbooks.; Report revenue metrics to CFO monthly. |
| 60 | `sales-owner` | Sales Owner | `sales` | None | Own services/sales.py and the sales SOP.; Fix the ruff E741 ambiguous-variable warnings in services/sales.py.; Model pipeline stages and revenue targets. |
| 61 | `solutions-engineer` | Solutions Engineer | `sales` | None | Provide pre-sales technical validation for enterprise deals.; Design custom solutions for customer use cases.; Create proof-of-concept implementations for prospects.; Coordinate with customer_success_owner on implementation handoff.; Maintain a library of solution patterns and reference architectures. |

## Security (7 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 62 | `ai-security-specialist` | AI Security Specialist | `ciso` | None | Implement defenses against prompt injection and jailbreak attacks.; Monitor for model exfiltration and data poisoning attempts.; Audit LLM interactions for security anomalies.; Coordinate with ai_safety_lead on adversarial robustness.; Maintain AI security incident response playbooks. |
| 63 | `ciso` | Chief Information Security Officer | `chief-of-staff` | None | Define and maintain security strategy and posture.; Lead incident response and forensic investigations.; Ensure compliance with SOC2, GDPR, and regulations.; Conduct security awareness training across the organization.; Manage vulnerability scanning and remediation programs.; Manage access policies and least-privilege principles.; Monitor for external threats and attack vectors.; Report security posture to CEO and Board. |
| 64 | `decision-engine-owner` | Decision Engine Owner | `ciso` | None | Own the decision/ engine and approval matrix.; Maintain risk-assessment and decision-tree navigation logic.; Coordinate tier-rule enforcement with security_compliance_lead (GAP-003).; Validate decision outcomes are explainable and auditable. |
| 65 | `devsecops-lead` | DevSecOps Lead | `ciso` | None | Integrate security scanning into CI/CD pipelines.; Implement SAST/DAST for code and API security testing.; Manage dependency vulnerability scanning and SBOM generation.; Coordinate with devops_agent on container image signing.; Enforce security gates in the build pipeline. |
| 66 | `incident-response-lead` | Incident Response Lead | `ciso` | None | Develop and maintain incident response playbooks.; Coordinate incident response activities across all teams.; Ensure forensic readiness for all system components.; Manage breach notification workflows for GDPR/CCPA compliance.; Lead post-incident reviews and lessons learned. |
| 67 | `security-architect` | Security Architect | `ciso` | None | Design zero trust architecture principles and implementation.; Implement microsegmentation for sensitive services.; Design identity-aware access for registry, generator, and dashboard.; Maintain the overall security architecture documentation.; Coordinate with security_compliance_lead on control implementation. |
| 68 | `security-compliance-lead` | Security & Compliance Lead | `ciso` | None | Integrate 5-tier approval rules into the ToolRunner (GAP-003).; Lock down dashboard CORS to an explicit allowlist (GAP-010).; Implement/enforce dashboard API authentication (GAP-011).; Maintain a continuous security checklist covering all GAPs in the security cluster.; Audit privileged tool calls for tier-gated compliance. |

## Strategy (2 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 69 | `cso` | Chief Strategy Officer | `chief-of-staff` | None | Develop and execute corporate strategy.; Conduct market analysis and competitive intelligence.; Evaluate partnership and alliance opportunities.; Assess M&A targets and investment opportunities.; Drive market expansion and geographic growth.; Ensure strategic coherence across departments.; Prepare strategic plans for board review. |
| 70 | `market-analyst` | Market Analyst | `cso` | None | Analyze industry trends and market data.; Conduct competitive landscape research.; Forecast market size and growth potential.; Track competitor product launches and strategies.; Assess new market opportunities.; Prepare market intelligence reports. |

## Consulting (1 agent)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 71 | `consulting-lead` | Consulting Engagement Lead | `chief-of-staff` | None | Own the consulting engagement lifecycle from onboarding to delivery.; Coordinate client-facing agents and manage engagement timelines.; Ensure quality standards and SLA adherence across all engagements.; Present transformation roadmaps to clients.; Feed engagement learnings back into the knowledge flywheel. |

## Technology (13 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 72 | `cto` | Chief Technology Officer | `chief-of-staff` | None | Architect robust AI agent systems.; Review and merge code generated by development agents.; Ensure system scalability and security. |
| 73 | `dashboard-owner` | Dashboard Owner | `vp-engineering` | None | Own the dashboard/ REST API and WebSocket support.; Maintain the 7-department KPI collectors and analytics layer.; Coordinate CORS lockdown and auth with security_compliance_lead (GAP-010/011).; Ensure the dashboard reads from the live state, not stale files (GAP-011). |
| 74 | `devops-lead` | DevOps Lead | `vp-engineering` | None | Design and maintain CI/CD pipelines.; Manage cloud infrastructure and deployments.; Monitor system health, uptime, and alerting.; Implement and maintain infrastructure-as-code (IaC).; Optimize deployment speed and reliability. |
| 75 | `integration-engineer` | Integration Engineer | `lead-backend` | None | Implement WhatsApp Business API integration for Offer B chatbots.; Build connectors for NGO data sources (Kobo, DHIS2, Google Sheets) for Offer C.; Integrate payment gateways (Airtel Money, TNM Mpamba, PayChangu) for local transactions.; Maintain integration health monitoring and alerting. |
| 76 | `lead-backend` | Lead Backend Engineer | `cto` | None | Architect backend systems and define API standards.; Set database schema patterns and microservices boundaries.; Lead code reviews and enforce backend coding standards.; Manage technical debt and drive backend documentation.; Mentor backend engineers and drive performance tuning. |
| 77 | `lead-frontend` | Lead Frontend Engineer | `cto` | None | Design user interfaces and implement responsive layouts.; Establish component standards and design system patterns.; Manage frontend state and optimize rendering performance.; Drive accessibility compliance and frontend toolchain management.; Mentor frontend engineers and coordinate with the design team. |
| 78 | `platform-engineer` | Platform Engineer | `cto` | None | Build and maintain the Internal Developer Platform (IDP).; Optimize CI/CD pipelines for speed and reliability.; Create and maintain local development environments.; Develop developer tooling to accelerate engineering velocity.; Monitor platform health and developer productivity metrics. |
| 79 | `platform-reliability-engineer` | Platform Reliability Engineer | `vp-engineering` | None | Own file-locking on all shared JSON/YAML state (GAP-002).; Harden the dead-letter queue with replayable, retryable entries (GAP-001, GAP-008).; Strengthen the LLM circuit breaker (failure thresholds, half-open probes, reset).; Maintain a living reliability checklist covering every GAP in the reliability cluster.; Add regression tests for locking, DLQ retry, and breaker state transitions. |
| 80 | `registry-owner` | Registry Owner | `vp-engineering` | None | Own the registry/ loader, parser, resolver, and validator.; Guarantee the 19 configs validate and resolve cleanly.; Catch dangling references and circular dependencies at load time. |
| 81 | `senior-backend-engineer` | Senior Backend Engineer | `lead-backend` | None | Design and implement complex API endpoints and services.; Optimize database queries and backend performance.; Mentor junior and mid-level backend engineers.; Drive architectural decisions for backend projects.; Conduct thorough code reviews and enforce quality standards. |
| 82 | `senior-frontend-engineer` | Senior Frontend Engineer | `lead-frontend` | None | Implement complex UI features and interactive components.; Optimize frontend performance and bundle size.; Mentor junior and mid-level frontend engineers.; Drive architectural decisions for frontend projects.; Conduct thorough code reviews and enforce quality standards. |
| 83 | `solution-architect` | Solution Architect | `cto` | None | Design end-to-end solutions for enterprise customer engagements.; Create technical proposals and reference architectures.; Evaluate and select technology stacks for new projects.; Coordinate cross-system integration between services and teams.; Partner with sales_engineer on pre-sales technical validation. |
| 84 | `vp-engineering` | VP of Engineering | `cto` | None | Manage all specialist engineering reports currently reporting directly to CTO.; Coordinate cross-team technical dependencies and blockers.; Ensure engineering velocity targets are met across all domains.; Prioritize technical debt reduction alongside feature delivery.; Report engineering health metrics to CTO weekly. |

## Pharos (6 agents)

| # | Agent ID | Agent Name | Reports To | Direct Reports | Responsibilities |
|---|----------|-----------|------------|----------------|-----------------|
| 85 | `agentic-policy-analyst` | Agentic Policy Analyst | `thought-leadership-lead` | None | Draft formal consultation comments into the National AI Strategy and Digital Transformation Strategy process.; Author the "SADC Agentic AI Governance Framework" and the "Operationalizing Autonomous Intelligence" policy whitepaper.; Map Lightspeed controls (5-tier approvals, audit trails, RACI) to regulatory and ethical requirements.; Produce the "policy translator" series linking global agentic AI governance to SADC.; Brief MACRA, ICTAM, Department of E-Government, and regional ICT ministries. |
| 86 | `agentic-research-lead` | Agentic Research Lead | `thought-leadership-lead` | None | Produce the "State of Agentic AI in Malawi" and SADC readiness research artifacts.; Maintain a quantified use-case census (J&S StopOver Bar, health/M&E, VSLA/SACCO, finance).; Track AU Continental AI Strategy, SADC digital transformation, and early-mover policy precedent.; Normalize Lightspeed KPIs (task completion rate, cost per workflow, HITL gate coverage) into public benchmarks.; Follow every claim back to a high-trust primary source. |
| 87 | `community-ecosystem-builder` | Community and Ecosystem Builder | `thought-leadership-lead` | None | Build and maintain the SADC Agentic AI institutional stakeholder map (MACRA, UNDP, PPP, ICTAM, MCCCI, universities).; Launch the Malawi Agentic AI Forum and the annual Agentic AI Malawi Summit concept.; Develop strategic partnerships (National AI Workforce model, university Labs, mHub).; Maintain the localized use-case pipeline (agritech, public health, SME, financial inclusion).; Grow a regional practitioner community across Zambia, Zimbabwe, South Africa. |
| 88 | `speaker-engagement-lead` | Speaker and Engagement Lead | `thought-leadership-lead` | None | Target and secure speaking slots (ICTAM, COMESA/IDEA, IDC CIO Summit, SADC, Smart Africa).; Design and deliver the two-day "Agentic AI Executive Lab" workshop.; Package the high-visibility "Lighthouse" pilot proposal with non-commercial partners.; Create keynote scripts and speaker one-sheets grounded in Lightspeed proof.; Convene the private "CEO Roundtable on Agentic AI Governance". |
| 89 | `thought-leadership-author` | Thought Leadership Author | `thought-leadership-lead` | None | Draft flagship white papers ("The Sovereign Agentic Enterprise", "What Is an AI-Native Company?").; Write the monthly "Malawi Agentic AI Monitor" and the 10 flagship publications roadmap.; Own the executive LinkedIn / Substack long-form editorial stream.; Draft the Lightspeed AI-Native Enterprise Framework (H-A-O-M-T-G-V) public narrative.; Maintain brand-voice consistency distinct from product content writing. |
| 90 | `thought-leadership-lead` | Thought Leadership Lead | `chief-of-staff` | None | Own the CEO's North Star positioning and the Pharos 90-day / 12-month / 24-month roadmap.; Maintain the thought-leadership content calendar and cross-agent orchestration.; Anchor the "Company Builder / Use Cases / Policy" three-pillar narrative.; Operate the Lightspeed Institute and the Agentic AI Executive Lab pipelines.; Coordinate with CMO (product marketing), CMO content team, and CSO on messaging alignment.; Report thought-leadership impact metrics to the Human CEO. |
