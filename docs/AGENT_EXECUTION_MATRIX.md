# Agent Execution Classification Matrix — LightSpeed 90-Agent Architecture

**Source**: `company-registry.yaml` (3993 lines, 90 agents)  
**Generated**: October 3, 2026  
**Purpose**: Classify each agent for remote execution platform assignment

---

## Classification Legend

| Column | Values |
|--------|--------|
| **Type** | `executive`, `specialist`, `board` |
| **Runtime** | `python_cli` (all agents) |
| **Local-only?** | `yes` = requires local files/models; `no` = can run remote |
| **Network** | `yes` = needs internet/API access; `no` = fully offline capable |
| **State** | `high` = persistent state required; `med` = session state; `low` = stateless |
| **Can be Ephemeral?** | `yes` = can run as short-lived worker; `no` = needs persistent process |
| **Human Approval** | `exec`, `lead`, `board`, `ceo`, `none` |
| **Candidate Platform** | Primary platform assignment for remote execution |

---

## Complete Matrix (90 Agents)

| # | Agent ID | Name | Type | Dept | Dependencies | Runtime | Local-only? | Network | State | Ephemeral? | Human Approval | Candidate Platform |
|---|----------|------|------|------|--------------|---------|-------------|---------|-------|------------|----------------|-------------------|
| 1 | chief_of_staff | Chief of Staff | executive | Executive | All depts | python_cli | no | yes | high | no | exec | Cloudflare Worker (control) |
| 2 | cto | Chief Technology Officer | executive | Technology | Tech depts | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 3 | coo | Chief Operating Officer | executive | Operations | Ops depts | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 4 | caio | Chief AI Officer | executive | AI Research | AI depts | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 5 | human_ceo | Human CEO | executive | Executive | All | human | N/A | N/A | N/A | N/A | ceo | N/A (human) |
| 6 | cfo | Chief Financial Officer | executive | Finance | Finance | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 7 | cpo | Chief Product Officer | executive | Product | Product | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 8 | cmo | Chief Marketing Officer | executive | Marketing | Marketing | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 9 | hr | Chief Human Resources Officer | executive | People | People | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 10 | ciso | Chief Information Security Officer | executive | Security | Security | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 11 | cio | Chief Information Officer | executive | IT | IT | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 12 | cdo | Chief Data Officer | executive | Data | Data | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 13 | clo | Chief Legal Officer | executive | Legal | Legal | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 14 | cso | Chief Strategy Officer | executive | Strategy | Strategy | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 15 | ceo_advisor | CEO Advisor | executive | Executive | CEO | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 16 | customer_success | Head of Customer Success | executive | Customer Success | CS | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 17 | sales | Head of Sales | executive | Sales | Sales | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 18 | consulting_lead | Consulting Engagement Lead | executive | Consulting | Consulting | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 19 | thought_leadership_lead | Thought Leadership Lead | executive | Pharos | Pharos | python_cli | no | yes | high | no | exec | Cloudflare Worker |
| 20 | board_chair | Board Chair | board | Board | All | python_cli | no | yes | low | yes | board | Cloudflare Worker |
| 21 | board_finance | Finance Committee Chair | board | Board | Finance | python_cli | no | yes | low | yes | board | Cloudflare Worker |
| 22 | board_risk | Risk Committee Chair | board | Board | Risk | python_cli | no | yes | low | yes | board | Cloudflare Worker |
| 23 | board_strategy | Strategy Committee Chair | board | Board | Strategy | python_cli | no | yes | low | yes | board | Cloudflare Worker |
| 24 | board_technology | Technology Committee Chair | board | Board | Tech | python_cli | no | yes | low | yes | board | Cloudflare Worker |
| 25 | board_customer | Customer Committee Chair | board | Board | Customer | python_cli | no | yes | low | yes | board | Cloudflare Worker |
| 26 | board_product | Product Committee Chair | board | Board | Product | python_cli | no | yes | low | yes | board | Cloudflare Worker |
| 27 | financial_analyst | Financial Analyst | specialist | Finance | CFO | python_cli | no | no | med | yes | lead | GitHub Actions |
| 28 | devops_lead | DevOps Lead | specialist | Technology | VP Eng | python_cli | no | yes | med | yes | lead | GitHub Actions (native) |
| 29 | platform_reliability_engineer | Platform Reliability Engineer | specialist | Technology | VP Eng | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 30 | security_compliance_lead | Security & Compliance Lead | specialist | Security | CISO | python_cli | no | yes | med | yes | lead | Cloudflare Worker |
| 31 | memory_owner | Memory Owner | specialist | AI Research | CAIO | python_cli | no | no | high | no | lead | Cloudflare Durable Object |
| 32 | decision_engine_owner | Decision Engine Owner | specialist | Security | CISO | python_cli | no | no | med | no | lead | Cloudflare Durable Object |
| 33 | workflow_owner | Workflow Owner | specialist | Operations | COO | python_cli | no | yes | med | yes | lead | GitHub Actions / Cloudflare |
| 34 | dashboard_owner | Dashboard Owner | specialist | Technology | VP Eng | python_cli | no | yes | high | no | lead | Render (always-on) |
| 35 | llm_platform_owner | LLM Platform Owner | specialist | AI Research | CAIO | python_cli | no | yes | high | yes | lead | Cloudflare Worker |
| 36 | orchestration_owner | Orchestration Owner | specialist | Operations | COO | python_cli | no | yes | med | yes | lead | Cloudflare Worker (queue consumer) |
| 37 | registry_owner | Registry Owner | specialist | Technology | VP Eng | python_cli | no | no | low | yes | lead | GitHub Actions |
| 38 | doctor_owner | Doctor Owner | specialist | Operations | COO | python_cli | no | yes | low | yes | lead | GitHub Actions (scheduled) |
| 39 | sales_owner | Sales Owner | specialist | Sales | Sales | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 40 | marketing_owner | Marketing Owner | specialist | Marketing | CMO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 41 | social_media_manager | Social Media Manager | specialist | Marketing | CMO | python_cli | no | yes | high | no | lead | Cloudflare Worker (API) |
| 42 | customer_success_owner | Customer Success Owner | specialist | Customer Success | CS | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 43 | legal_owner | Legal Owner | specialist | Legal | CLO | python_cli | no | no | med | yes | lead | GitHub Actions |
| 44 | hr_owner | HR Owner | specialist | People | HR | python_cli | no | no | low | yes | lead | GitHub Actions |
| 45 | sop_owner | SOP Owner | specialist | Operations | COO | python_cli | no | no | low | yes | lead | GitHub Actions |
| 46 | qa_lead | QA Lead | specialist | QA | VP Eng | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 47 | test_engineering_lead | Test Engineering Lead | specialist | QA | QA Lead | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 48 | release_manager | Release Manager | specialist | QA | VP Eng | python_cli | no | yes | med | yes | lead | GitHub Actions (native) |
| 49 | vp_engineering | VP of Engineering | specialist | Technology | CTO | python_cli | no | yes | med | yes | lead | Cloudflare Worker |
| 50 | data_engineer | Data Engineer | specialist | Data | CDO | python_cli | no | yes | high | no | lead | Render / Cloudflare D1 |
| 51 | ai_safety_lead | AI Safety Lead | specialist | AI Research | CAIO | python_cli | no | no | med | no | lead | Cloudflare Worker |
| 52 | ux_research_lead | UX Research Lead | specialist | Product | CPO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 53 | technical_documentation_lead | Technical Documentation Lead | specialist | Product | CPO | python_cli | no | no | low | yes | lead | GitHub Actions |
| 54 | head_of_developer_relations | Head of Developer Relations | specialist | Marketing | CMO | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 55 | culture_values_officer | Culture and Values Officer | specialist | People | Chief of Staff | python_cli | no | no | low | yes | lead | GitHub Actions |
| 56 | red_team_engineer | Red Team Engineer | specialist | AI Research | AI Safety Lead | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 57 | platform_engineer | Platform Engineer | specialist | Technology | CTO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 58 | product_marketing_manager | Product Marketing Manager | specialist | Marketing | CMO | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 59 | head_of_business_development | Head of Business Development | specialist | Business Development | Chief of Staff | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 60 | ai_security_specialist | AI Security Specialist | specialist | Security | CISO | python_cli | no | no | med | no | lead | Cloudflare Worker |
| 61 | incident_response_lead | Incident Response Lead | specialist | Security | CISO | python_cli | no | yes | med | no | lead | Cloudflare Worker |
| 62 | devsecops_lead | DevSecOps Lead | specialist | Security | CISO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 63 | prompt_engineer | Prompt Engineer | specialist | AI Research | CAIO | python_cli | no | no | low | yes | lead | GitHub Actions |
| 64 | data_privacy_officer | Data Privacy Officer | specialist | Legal | CLO | python_cli | no | no | med | yes | lead | GitHub Actions |
| 65 | security_architect | Security Architect | specialist | Security | CISO | python_cli | no | yes | med | no | lead | Cloudflare Worker |
| 66 | product_designer | Product Designer | specialist | Product | CPO | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 67 | vendor_manager | Vendor Manager | specialist | Operations | COO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 68 | solutions_engineer | Solutions Engineer | specialist | Sales | Sales | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 69 | internal_comms_lead | Internal Communications Lead | specialist | Executive | Chief of Staff | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 70 | business_intelligence_engineer | Business Intelligence Engineer | specialist | Data | CDO | python_cli | no | yes | med | yes | lead | Render |
| 71 | ai_ethics_board_chair | AI Ethics Board Chair | specialist | Executive | Chief of Staff | python_cli | no | yes | high | yes | lead | GitHub Actions |
| 72 | lead_backend | Lead Backend Engineer | specialist | Technology | CTO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 73 | lead_frontend | Lead Frontend Engineer | specialist | Technology | CTO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 74 | solution_architect | Solution Architect | specialist | Technology | CTO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 75 | senior_frontend_engineer | Senior Frontend Engineer | specialist | Technology | Lead Frontend | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 76 | senior_backend_engineer | Senior Backend Engineer | specialist | Technology | Lead Backend | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 77 | product_owner | Product Owner | specialist | Product | CPO | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 78 | growth_hacker | Growth Hacker | specialist | Marketing | CMO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 79 | market_analyst | Market Analyst | specialist | Strategy | CSO | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 80 | recruiter | Recruiter | specialist | People | HR | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 81 | content_creator | Content Creator | specialist | Marketing | CMO | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 82 | ml_engineer | ML Engineer | specialist | AI Research | CAIO | python_cli | no | yes | high | no | lead | Render (GPU) / GitHub Actions |
| 83 | integration_engineer | Integration Engineer | specialist | Technology | Lead Backend | python_cli | no | yes | high | no | lead | Render (persistent) |
| 84 | agentic_research_lead | Agentic Research Lead | specialist | Pharos | Thought Leadership | python_cli | no | yes | high | yes | lead | GitHub Actions |
| 85 | thought_leadership_author | Thought Leadership Author | specialist | Pharos | Thought Leadership | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 86 | agentic_policy_analyst | Agentic Policy Analyst | specialist | Pharos | Thought Leadership | python_cli | no | yes | med | yes | lead | GitHub Actions |
| 87 | speaker_engagement_lead | Speaker and Engagement Lead | specialist | Pharos | Thought Leadership | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 88 | community_ecosystem_builder | Community and Ecosystem Builder | specialist | Pharos | Thought Leadership | python_cli | no | yes | low | yes | lead | GitHub Actions |
| 89 | media_generation_owner | Media Generation Owner | specialist | Marketing | CMO | python_cli | no | yes | high | no | lead | Render (GPU) |
| 90 | creative_director | Creative Director | specialist | Marketing | CMO | python_cli | no | yes | med | yes | lead | GitHub Actions |

---

## Platform Assignment Summary

| Platform | Agent Count | Agent Types |
|----------|-------------|-------------|
| **Cloudflare Worker (Control Plane)** | 19 | All executives + board + stateful specialists |
| **Cloudflare Worker (Queue Consumer)** | 2 | orchestration_owner, social_media_manager |
| **Cloudflare Durable Object** | 2 | memory_owner, decision_engine_owner |
| **GitHub Actions (Ephemeral)** | 52 | Most specialists (stateless, batch) |
| **GitHub Actions (Native CI/CD)** | 3 | devops_lead, release_manager, registry_owner |
| **Render (Persistent)** | 5 | dashboard_owner, integration_engineer, ml_engineer, data_engineer, media_generation_owner |
| **GitHub Actions (Scheduled)** | 1 | doctor_owner |
| **Human** | 1 | human_ceo |
| **Cloudflare Worker (AI Security)** | 5 | ai_security_specialist, incident_response_lead, security_architect, prompt_engineer, ai_safety_lead |

---

## Agents Requiring Persistent/Always-On Runtime (22)

| Agent | Reason |
|-------|--------|
| chief_of_staff | Orchestrates all depts; continuous coordination |
| cto | Tech oversight; continuous monitoring |
| coo | Operations coordination; continuous |
| caio | AI research direction; continuous |
| cfo | Financial monitoring; continuous |
| cpo | Product direction; continuous |
| cmo | Marketing ops; continuous |
| hr | People ops; continuous |
| ciso | Security posture; continuous |
| cio | IT infrastructure; continuous |
| cdo | Data strategy; continuous |
| clo | Legal/compliance; continuous |
| cso | Strategy execution; continuous |
| ceo_advisor | CEO support; continuous |
| customer_success | Customer health; continuous |
| sales | Pipeline management; continuous |
| consulting_lead | Engagement lifecycle; continuous |
| thought_leadership_lead | Content calendar; continuous |
| dashboard_owner | FastAPI + WebSocket server; always-on |
| integration_engineer | WhatsApp/CRM webhooks; persistent connections |
| media_generation_owner | ComfyUI GPU; long-running generations |
| memory_owner | 6-type memory store; persistent state |

---

## Agents Suitable for Ephemeral Execution (68)

All remaining specialists can execute as short-lived workers triggered by queue messages, with state checkpointed to Durable Objects.