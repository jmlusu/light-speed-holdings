# WLO Salesforce Domain → Light Speed Agent Capability Map

**Document ID:** MAP-WLO-001
**Owner:** solution-architect
**Status:** COMPLETE — capability-gap recommendations are inputs to skill curation
**Date:** 2026-09-06
**Source:** We Lead Out services positioning (10 Salesforce domains), mapped against the
Light Speed Holdings registry (131 agents).

---

## 1. Purpose

We Lead Out delivers across ten Salesforce domains. To position LSH as the
platform that powers that model — and to decide which lines of business LSH can
credibly claim — each domain is mapped to the agents that would execute it.
Domains where LSH currently lacks depth are flagged with a skill recommendation
rather than a new-agent recommendation (skills are cheaper and swappable).

---

## 2. Domain → Agent Mapping

| # | WLO Salesforce domain | LSH lead agent | Supporting agents | LSH readiness |
|---|------------------------|----------------|-------------------|---------------|
| 1 | **Agentforce** (agentic AI in Salesforce) | llm-platform-owner | ai-safety-lead, prompt-engineer, conversation-designer, red-team-engineer | Strong — core competency |
| 2 | **AI & Automation** (Flow, Einstein, LLM integration) | workflow-mapper | workflow-owner, prompt-engineer, integration-engineer | Strong |
| 3 | **Data Cloud** (unify + segment + activate) | data-engineer | data-scientist, business-intelligence-engineer, data-privacy-officer | Strong |
| 4 | **Core Platform** (objects, security, automation) | solution-architect | lead-backend, security-architect, qa-lead | Strong |
| 5 | **Service Cloud** (omnichannel, knowledge, bots) | support-agent | conversation-designer, customer-success-owner | Medium — needs service-cloud skill |
| 6 | **Sales Cloud** (pipeline, lead mgmt) | sales-owner | revenue-operations-analyst, solutions-engineer | Strong for methodology; skill needed for native UI |
| 7 | **Marketing Automation** (journeys, ROI) | marketing-owner | content-writer, growth-hacker, ux-analytics-lead | Medium |
| 8 | **Financial Services Cloud** (FSC) | integration-engineer | data-privacy-officer, compliance-officer, solution-architect | Gap — needs FSC + financial-subject expertise |
| 9 | **Education Cloud** (admissions, alumni) | data-engineer | survey-researcher, technical-documentation-lead | Gap — needs Education Cloud skill |
| 10 | **Managed Support** (admin, enhance, resolve) | customer-success-owner | support-agent, developer-experience-engineer | Strong |

**Legend:** *Strong* = direct agent capability today · *Medium* = works, but needs
a domain skill pack · *Gap* = advisory recommended before client promises.

---

## 3. What the Mapping Means

- **LSH does not need Salesforce configuration expertise out of the box.** The
  platform's value is speed, governance, and knowledge compounding — the same
  AI-native leverage WLO built manually. Domain depth is addable via skills
  (reference libraries, best-practice prompt packs, schema cheat-sheets).
- **Discovery-to-roadmap is fully covered today.** Domains 1–4 and 10 map to
  agents executing the existing `consulting` and `foaster_engagement` pipelines.
- **The practical answer: "sell the process, skill the domain."** The
  consulting-firm template (step 1) plus these skill additions makes the
  consultancies LSH licenses able to staff all ten domains.

---

## 4. Capability-Gap Recommendations (add-skills, not new agents)

| Priority | Gap | Recommendation | Affected domains |
|----------|-----|----------------|------------------|
| P1 | Service Cloud configuration knowledge | Curate a Service Cloud reference skill (objects, queues, omni-channel, knowledge) | 5 |
| P1 | Native Salesforce UI / config depth | Add a "Salesforce expert" skill pack combining Flow + Agentforce + setup patterns | 4, 5, 6, 7 |
| P2 | Financial-services domain terms | Add FSC skill (wealth mgmt flows, compliance surfaces, advisor tooling) | 8 |
| P2 | Education-domain terms | Add Education Cloud skill (admissions, student 360, alumni) | 9 |
| P3 | Marketing ROI accounting | Reuse ux-analytics-lead + revenue-operations-analyst patterns inside marketing compositions | 7 |

---

## 5. Decision Rule for Client Facing Claims

> Only claim a domain as "covered" when the lead agent plus its mapped
> supporting agents can be staffed AND the domain skill pack exists. Until then,
> scope the play to Domains 1–4 and 10 (Strong), and treat 5–7 as
> "with enablement," 8–9 as "advisory only."

---

## 6. Related Assets

- Registry template: `company/registry-templates/consulting-firm/`
- Case study: `docs/case-studies/wlo-ai-native-consultancy.md`
- Pricing model: `docs/ai-caas-pricing-model.md`
- Offer list: `config/company/ai_caas_offers.yaml`
