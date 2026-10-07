# AI Company Builder - DRAFT awaiting CEO/Pharos sign-off

> **Status:** DRAFT - awaiting CEO/Pharos sign-off.
> **Section:** Directive "WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md" §14 (AI Company Builder), §13/§23 (claims), §24 (honesty), §34 (CTA), §35 (FAQ placement).
> **Sources:** `src/data/registries/faq-registry.json` (faq-02, faq-03, faq-06 - faq-17, faq-24), `src/data/registries/claims-registry.json`, `src/data/registries/metrics-registry.json`, `src/data/siteContent.ts` (solutions[0], GOVERNANCE_SOLUTION, trustEvidence), `src/data/companyData.ts` (registry field shape), `src/data/registries/use-case-registry.json`.

**Tone:** public product architecture / product tour - not a generic landing page (Directive §14). Every claim carries a source comment and, where relevant, a status label (LIVE / PROVEN IN-HOUSE / PILOT / DEMONSTRATION / FIELDABLE / FUTURE).

---

## HERO

<!-- src: Directive §14 "HERO"; §17 CTA system -->

**Eyebrow:** LIGHTSPEED HOLDINGS // FLAGSHIP PLATFORM

**Headline:** Build. Govern. Scale.
<!-- src: Directive §14 HERO (verbatim) -->

**Subheadline:** The governed multi-agent orchestration platform that runs LightSpeed Holdings - 90 roles, 20 departments, five-tier human approval, SHA-256 sealed audit trails. AI executes. Humans decide.
<!-- src: faq-registry faq-02, faq-05; claims-registry claim.agent-count, claim.five-tier-approval, claim.immutable-audit-trails (PROVEN_IN_HOUSE) -->

**Primary CTA:** START A CONVERSATION -> `/contact`
**Contextual CTA:** EXPLORE USE CASES -> `/use-cases`
<!-- src: cta-registry; Directive §34 -->

**Status line:** FIELDABLE - governance core (approvals, gates, audit trails) PROVEN IN-HOUSE; LightSpeed Holdings is the platform's own first customer.
<!-- src: siteContent.ts solutions[0].proof "Fieldable in 2026"; sector-registry Technology & Digital Businesses badge -->

---

## OPERATING MODEL

<!-- src: Directive §14 "OPERATING MODEL" (chain verbatim); faq-registry faq-02 -->

The chain, top to bottom:

```
Human CEO
   ↓
89 AI agents
   ↓
Orchestration
   ↓
20 departments
   ↓
Workflows
   ↓
Deliverables
```

**Caption:** The human sits above the system. Every deliverable passes through human review before it ships - no client-facing deliverable ships without human sign-off.
<!-- src: Directive §14; faq-registry faq-02; §24 (never imply AI runs the company without humans) -->

<!-- src: claims-registry claim.agent-count, claim.department-count (PROVEN_IN_HOUSE) -->

---

## H-A-O-M-T-G-V

<!-- src: Directive §14 "H-A-O-M-T-G-V"; faq-registry faq-06 -->

The platform's seven architectural layers. **Status: PROVEN IN-HOUSE.**

- **H - HUMAN:** Operational intent and final decision authority. The Human CEO sets vision, owns high-stakes decisions, approves budgets and releases, and is accountable to the Board.
<!-- src: faq-registry faq-04, faq-06 -->
- **A - AGENTS:** 90 specialized operating roles - 89 AI agents plus 1 Human CEO, each with a defined mission, responsibilities, reporting line and tool set.
<!-- src: claims-registry claim.agent-count; faq-registry faq-03 -->
- **O - ORCHESTRATION:** Deterministic routing of data, tasks and decisions across workflows - brief -> inbox task -> assigned agents -> human review -> deliverable.
<!-- src: faq-registry faq-06, faq-02 -->
- **M - MEMORY:** Persistent contextual storage across long-running tasks - 6 memory types, recall before action, bounded by consolidation and forgetting policies.
<!-- src: faq-registry faq-10 -->
- **T - TOOLS:** Isolated execution environments - a canonical 7-tool vocabulary, validated on every call.
<!-- src: faq-registry faq-11 -->
- **G - GOVERNANCE:** Five-tier approval controls, four mandatory gates, immutable logging.
<!-- src: claims-registry claim.five-tier-approval, claim.four-governance-gates, claim.immutable-audit-trails (PROVEN_IN_HOUSE) -->
- **V - VALUE:** Measurable reductions in cost and operational latency.
<!-- src: faq-registry faq-06 -->

---

## 90-ROLE WORKFORCE

<!-- src: Directive §14 "90-role workforce"; claims-registry claim.agent-count, claim.canonical-registry-numbers -->

**Headline:** 89 AI agents + 1 Human CEO across 20 departments.

Every role is a generated agent card with mission, responsibilities, department, reporting line and permitted tools. Every platform figure - 90 agents, 20 departments, the regression-test count - is read from `company-registry.yaml` and the test suite, never from marketing copy. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.canonical-registry-numbers (PROVEN_IN_HOUSE); companyData.ts toAgent()/departmentsList() field shape -->

| Figure | Value | Classification |
|---|---|---|
| Total roles | 90 | PROVEN IN-HOUSE |
| AI agents | 89 | PROVEN IN-HOUSE |
| Human CEO | 1 | PROVEN IN-HOUSE |
| Departments | 20 | PROVEN IN-HOUSE |

<!-- §23 note: historical counts 89/90/127/143/144/152 in old artifacts are not equivalent - canonical model is 90 = 89 + 1 (claim.historical-agent-counts, HISTORICAL). -->

---

## DEPARTMENT ARCHITECTURE

<!-- src: Directive §14 "Department architecture"; companyData.ts departmentsList() -->

Twenty departments, each carrying an executive owner, mission statement, budget category and headcount target. Work enters a department as an inbox task, is routed by orchestration, and exits as a reviewed deliverable. Cross-department actions escalate rather than bypass approval. [PROVEN IN-HOUSE]
<!-- src: faq-registry faq-02 (work flow); companyData.ts Department fields (id, name, executive, mission, budget_category, headcount_target) -->
<!-- TODO: needs fact - full list of the 20 department names for the org visualization; read from company-registry.yaml at build time, never hand-typed -->

---

## AGENT REGISTRY

<!-- src: Directive §14 "Agent registry"; companyData.ts toAgent() -->

Each of the 90 roles resolves from a public agent registry entry: id, title, type (Executive / Specialist / Board), department, reporting line, mission, responsibilities and tool set. The registry is the single source of truth - agent cards are generated from it, so the org chart you see on this page is the org chart the platform runs. [PROVEN IN-HOUSE]
<!-- src: companyData.ts toAgent() mapping of PublicAgent fields; AGENTS.md company-registry.yaml workflow -->

---

## WORKFLOW EXECUTION

<!-- src: Directive §14 "Workflow execution"; faq-registry faq-02 -->

**The path of one unit of work:**

1. Brief arrives (conversation, assessment, or inbound request).
2. It becomes a task in the inbox queue.
3. Orchestration routes it to assigned agents in the right department.
4. Agents execute inside their tool boundaries.
5. Risk classification determines the approval tier.
6. A human reviews, approves, escalates, or rejects.
7. The deliverable ships - or does not.

No client-facing deliverable ships without human sign-off. Pending approvals expire on a periodic sweep instead of queueing forever. [PROVEN IN-HOUSE]
<!-- src: faq-registry faq-02, faq-07; claims-registry claim.five-tier-approval (PROVEN_IN_HOUSE) -->

---

## MEMORY

<!-- src: Directive §14 "Memory"; faq-registry faq-10 -->

**Status: PROVEN IN-HOUSE.**

A 6-type persistent store - episodic, semantic, procedural, relational, temporal, aggregate - integrated with the executor recall loop. Agents recall before they act: memory is queryable and attributable. Consolidation and forgetting policies bound growth; recall latency stays within executor budgets. This is what makes long-running tasks, cross-session context and organisational learning possible.
<!-- src: faq-registry faq-10 (verbatim structure) -->

---

## TOOLS

<!-- src: Directive §14 "Tools"; faq-registry faq-11 -->

**Status: PROVEN IN-HOUSE.**

A canonical tool vocabulary of 7 tools:

| Tool | Purpose |
|---|---|
| read | File contents |
| edit | Exact string replacement |
| grep | Regex search |
| list | Directory entries |
| bash | Shell commands |
| webfetch | HTTP/HTTPS fetch |
| task | Launch sub-agent |

Legacy aliases (write -> edit, execute -> bash, delegate -> task, web_search -> webfetch) are accepted for backward compatibility. The ToolRunner validates against the canonical list; unknown tools return an error. Agents do not have unrestricted shell access - tools are isolated execution environments.
<!-- src: faq-registry faq-11; AGENTS.md §8 Tool Vocabulary -->

---

## GOVERNANCE

<!-- src: Directive §14 "Governance"; siteContent.ts GOVERNANCE_SOLUTION; claims-registry -->

**Status: PROVEN IN-HOUSE.** The governance layer that makes deployment safe.

**5-tier human-in-the-loop approval matrix:**

| Tier | Approver | Scope |
|---|---|---|
| 1 | Auto | Fully autonomous within defined boundaries |
| 2 | Lead | Department/lead approval |
| 3 | Executive | C-level approval (Tier 3+ also requires AI Ethics Board review) |
| 4 | CEO | Human CEO sign-off |
| 5 | Board | Board-level decisions |

<!-- src: faq-registry faq-07; claims-registry claim.ai-ethics-board-review (PROVEN_IN_HOUSE) -->

**4 mandatory governance gates before any work begins:** Contract -> Data Processing Agreement -> Compliance Review -> Security Assessment.
<!-- src: claims-registry claim.four-governance-gates (PROVEN_IN_HOUSE) -->

**Five principles:** agents execute while the Human CEO owns outcome; no client-facing deliverable ships without human sign-off; every action generates an append-only audit receipt; pending approvals expire on a periodic sweep; risk-classified actions require tiered approval.
<!-- src: siteContent.ts GOVERNANCE_SOLUTION.keyPrinciples -->

---

## AUDITABILITY

<!-- src: Directive §14 "Auditability"; faq-registry faq-09 -->

**Status: PROVEN IN-HOUSE.**

Every agent action generates an append-only JSONL audit event - correlated, queryable and never overwritten. Each event is cryptographically sealed with SHA-256, making the trail tamper-evident. The log captures prompts, tool invocations, outputs, approval decisions and escalation events. This is not optional logging - it is the platform's operating substrate.
<!-- src: faq-registry faq-09; claims-registry claim.immutable-audit-trails (PROVEN_IN_HOUSE) -->

---

## MODEL ROUTING

<!-- src: Directive §14 "Model routing"; faq-registry faq-12 -->

**Status: PROVEN IN-HOUSE.** Model-agnostic, provider-agnostic routing across 9 configured LLM providers.

Routing order:

1. Open / local first
2. Open-weight models
3. Local inference
4. Self-hosted / low-cost infrastructure
5. Commercial models - only when they provide a material quality, latency or capability advantage
6. Governed model routing
7. Human decisions, approvals and accountability

Local models handle routine classification, extraction, summarisation and embeddings. Mid-tier models handle reasoning, planning and synthesis. Premium models are reserved for exceptional reasoning and hard edge cases. Commercial proprietary models are not presented as the default for every task.
<!-- src: faq-registry faq-12; claims-registry claim.9-llm-providers (PROVEN_IN_HOUSE) -->
<!-- §23 note: per-tier cost figures visible in the internal dashboard (modelTiers in companyData.ts) are demo/operational data - not published here pending validation. -->
<!-- TODO: needs fact - publish routing benchmarks only if Phase 0 validation confirms them -->

---

## OPEN-WEIGHT / LOCAL-FIRST ECONOMICS

<!-- src: Directive §14 "Open-weight/local-first economics"; faq-registry faq-13, faq-14, faq-15 -->

**Status: PROVEN IN-HOUSE - LightSpeed operates this way daily.**

Open and open-weight AI is a cornerstone of the operating philosophy: designed for African cost realities, constrained infrastructure, intermittent connectivity, data sovereignty and local deployment. Routine tasks run on free local Ollama models at near-zero marginal cost; commercial APIs are routed only for material advantage. The platform supports offline-first operation on local infrastructure, with a Zero-Cloud Boundary option for state, health and financial data - data never leaves your infrastructure unless you configure cloud routing.
<!-- src: faq-registry faq-13, faq-14, faq-15; claims-registry claim.sovereign-offline-first (PROVEN_IN_HOUSE) -->

---

## VALUE MEASUREMENT

<!-- src: Directive §14 "Value measurement"; faq-registry faq-06 (V layer) -->

**Status: framework PROVEN IN-HOUSE; published outcome metrics pending Phase 0 validation.**

Value is the seventh layer: measurable reductions in cost and operational latency. Value is tracked per engagement against the baseline captured during the AI Readiness Assessment, and reported to the client - not asserted in marketing copy.

Verified outcomes that are claims-ledger approved for public use:

- 40% reduction in compliance reporting time across 14 departments. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.compliance-automation-40-percent (PROVEN_IN_HOUSE) -->
- Canonical platform figures read from `company-registry.yaml`, never from marketing copy. [PROVEN IN-HOUSE]
<!-- src: claims-registry claim.canonical-registry-numbers -->

<!-- §23 note: internal dashboard KPIs (task success rate, agent availability, cost per task, CSAT) are demo-dashboard data and are deliberately NOT published here. -->
<!-- TODO: needs fact - public value-metric set requires Phase 0 validation before any number is shown -->

---

## HUMAN APPROVAL

<!-- src: Directive §14 "Human approval"; faq-registry faq-04, faq-05, faq-07 -->

**Status: PROVEN IN-HOUSE.**

- Every agent action is risk-classified and routed through the 5-tier matrix (Auto -> Lead -> Executive -> CEO -> Board), mapped to a 5x5 likelihood x impact matrix.
<!-- src: faq-registry faq-07 -->
- The Human CEO has final authority - AI executes, humans decide.
<!-- src: faq-registry faq-04 -->
- Agents execute tasks; people own outcomes. LightSpeed augments teams - it does not replace human judgment or accountability.
<!-- src: faq-registry faq-05 -->
- Pending approvals expire on a periodic sweep instead of queueing forever.
<!-- src: faq-registry faq-08 -->
<!-- §24 note: never word this section so it implies "AI runs the company without humans". -->

---

## USE CASE EXAMPLES

<!-- src: Directive §14 "Use Case examples"; §10 status labels; use-case-registry.json -->

Each example carries a status label. None implies a paying client unless verified.

| Use case | Status | What it shows |
|---|---|---|
| LightSpeed Holdings - the platform runs itself | PROVEN IN-HOUSE | 90-role registry, 5-tier approvals and SHA-256 audit trails in daily internal use |
| Solo Founder + Governed AI Workforce (FOW-01) | PROVEN IN-HOUSE | One founder with a governed agent workforce across departments |
| AI Company Builder Platform Deployment | FIELDABLE | The same orchestration engine, licensed onto your infrastructure |
| Enterprise Agent Workforce Automation | DEMONSTRATION | Augmenting existing teams with governed agents |
| Compliance Automation for Financial Services | FIELDABLE | Risk-classified approvals on regulatory reporting flows |

<!-- src: use-case-registry.json (uc-meta, fow-01 statuses; fow-02 DEMONSTRATION); siteContent.ts solutions[0].useCases labels -->
<!-- §10 note: full explorer (filters by problem/solution/sector/status, detail pages) lives at /use-cases; this page links out rather than duplicating it. -->

**CTA:** EXPLORE USE CASES -> `/use-cases`
<!-- src: cta-registry contextual; Directive §34 -->

---

## FAQ

<!-- src: Directive §35 (FAQ on AI Company Builder page), §14 (page must handle objections) -->

**Section label:** FREQUENTLY ASKED QUESTIONS

Use the canonical set in `content/drafts/faq.md`. Page-specific subset (objections this page must remove):

- What is the AI Company Builder? (Q2)
- How many agents does LightSpeed have? (Q3)
- What is H-A-O-M-T-G-V? (Q6)
- How does human approval work? (Q7)
- What does five-tier governance mean? (Q8)
- How are actions audited? (Q9)
- Can LightSpeed run locally? (Q15)
- Is every Use Case a paying-client deployment? (Q24)

<!-- src: faq-registry faq-02, faq-03, faq-06 - faq-09, faq-15, faq-24; Directive §18 -->

---

## CTA (PAGE CLOSE)

**Headline:** See it run on your infrastructure - or see it run first.

**Primary CTA:** START A CONVERSATION -> `/contact`
**Secondary CTA:** REQUEST AN AI READINESS ASSESSMENT -> `/contact`
**Contextual CTA:** EXPLORE USE CASES -> `/use-cases`

<!-- src: cta-registry; Directive §34 - labels canonicalized, no "Book Briefing" / "Contact Us" variants -->

---

## DRAFT NOTES FOR CEO / PHAROS REVIEW

1. **Hero "Autonomous" wording avoided:** headline follows §14 verbatim ("Build. Govern. Scale."); subheadline uses preferred phrasing "AI executes. Humans decide." to satisfy §24.
2. **Department names omitted** from the architecture section - must be read from `company-registry.yaml` at build time (TODO marked).
3. **Value metrics:** only claims-ledger-approved figures appear (40% compliance reporting). Dashboard KPIs and model-tier cost data are demo/operational data and were excluded (§23).
4. **Pricing not on this page:** FAQ Q27 owns cost language; product page links to FAQ rather than repeating MWK figures.
5. **Status labels used:** PROVEN IN-HOUSE (governance core), FIELDABLE (licensing/deployment), DEMONSTRATION (enterprise augmentation) - all traceable to siteContent.ts / use-case-registry.json.
