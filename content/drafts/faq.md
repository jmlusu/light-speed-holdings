# FAQ (28 questions) - DRAFT awaiting CEO/Pharos sign-off

> **Status:** DRAFT - awaiting CEO/Pharos sign-off.

**Sources:** src/data/registries/faq-registry.json (canonical answers, 28 entries), Directive "WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md" section 18 (question list 1-28), src/data/faqs.ts (6-entry legacy subset), claims-registry.json (classifications).

**Coverage:** 28 of 28 questions from Directive section 18 / faq-registry.json. Answers are reproduced verbatim from faq-registry.json; no numbers, clients, or outcomes were added.

**Placement note (Directive section 35):** FAQ belongs on Homepage, AI Company Builder, Use Cases, and About - after the value proposition, never above it.

---

## 1. What is LightSpeed Holdings?

LightSpeed Holdings Limited is an AI-native company builder and operating company based in Lilongwe, Malawi. We design, build, and govern AI-native businesses, intelligent workflows, and agentic systems for organisations across Malawi, SADC, and Africa. Our tagline: ASPIRE. ACT. ACHIEVE. Our positioning: The AI-native company builder for Southern Africa.

<!-- src: faq-registry#faq-01, Directive section 18, Q1 -->

## 2. What is the AI Company Builder?

A governed multi-agent orchestration platform where 90 AI agents and 1 human CEO work across 20 departments. Work flows from brief to inbox task to assigned agents to human review to deliverable — no client-facing deliverable ships without human sign-off. The platform enforces 5-tier human-in-the-loop approvals, 4 governance gates (Contract, DPA, Compliance, Security), and immutable SHA-256 sealed audit trails for every action.

<!-- src: faq-registry#faq-02, Directive section 18, Q2 -->

## 3. How many agents does LightSpeed have?

LightSpeed's operating model contains 90 roles: 89 AI agents plus one Human CEO. The Human CEO agent acts at the explicit direction of the actual Human CEO/founder. Never describe LightSpeed as operating without human authority. The canonical technical explanation: "89 AI agents + 1 Human CEO across 20 departments."

<!-- src: faq-registry#faq-03, Directive section 18, Q3 -->

## 4. What does the Human CEO do?

The Human CEO sets company vision, mission, and long-term strategy; makes final decisions on high-stakes matters; represents the company externally to stakeholders and media; hires, manages, and evaluates the executive team; communicates with the Board of Directors; approves major budgets and investments; establishes and maintains company culture and values; resolves executive-level conflicts; authorizes production deployments and critical releases; and drives organizational growth and market expansion. The Human CEO has final authority — AI executes, humans decide.

<!-- src: faq-registry#faq-04, Directive section 18, Q4 -->

## 5. Does LightSpeed replace employees?

No. Agents execute tasks; people own outcomes. Every engagement runs through 5-tier human-in-the-loop approvals, so your team keeps decision authority while the platform carries the workload. The principle is: "Agents execute. The Human CEO owns operational intent and final decision authority." LightSpeed augments teams — it does not replace human judgment or accountability.

<!-- src: faq-registry#faq-05, Directive section 18, Q5 -->

## 6. What is H-A-O-M-T-G-V?

H-A-O-M-T-G-V is LightSpeed's core intellectual and architectural framework: H — HUMAN (operational intent and final decision authority); A — AGENTS (90 specialized operating roles: 89 AI agents + 1 Human CEO); O — ORCHESTRATION (deterministic routing of data, tasks, and decisions across workflows); M — MEMORY (persistent contextual data storage across long-running tasks); T — TOOLS (isolated execution environments for API integrations and actions); G — GOVERNANCE (five-tier approval controls and immutable logging); V — VALUE (measurable reductions in cost and operational latency). The Human layer remains above the system; Value is the business outcome.

<!-- src: faq-registry#faq-06, Directive section 18, Q6 -->

## 7. How does human approval work?

Every agent action is risk-classified and routed through a 5-tier approval matrix: Tier 1 (Auto) — fully autonomous within defined boundaries; Tier 2 (Lead) — department/lead approval; Tier 3 (Executive) — C-level approval; Tier 4 (CEO) — Human CEO sign-off; Tier 5 (Board) — board-level decisions. Pending approvals expire on a periodic sweep instead of queueing forever. Risk-classified actions require tiered approval mapped to a 5×5 likelihood × impact matrix.

<!-- src: faq-registry#faq-07, Directive section 18, Q7 -->

## 8. What does five-tier governance mean?

Five-tier governance means every consequential action passes through a risk-classified approval chain with five levels of human oversight (Auto → Lead → Executive → CEO → Board), four mandatory governance gates (Contract, Data Processing Agreement, Compliance Review, Security Assessment) before work begins, immutable audit trails for every action, and expiry sweeps that prevent stale approvals from blocking work indefinitely. It ensures accountability at every level.

<!-- src: faq-registry#faq-08, Directive section 18, Q8 -->

## 9. How are actions audited?

Every agent action generates an append-only JSONL audit event — correlated, queryable, and never overwritten. Each event is cryptographically sealed with SHA-256, making the trail tamper-evident. The audit log captures prompts, tool invocations, outputs, approval decisions, and escalation events. This is not optional logging — it is the platform's operating substrate.

<!-- src: faq-registry#faq-09, Directive section 18, Q9 -->

## 10. What is the role of memory?

Memory is a 6-type persistent store (episodic, semantic, procedural, relational, temporal, aggregate) that integrates with the executor recall loop. Agents recall before they act — memory is queryable and attributable. Consolidation and forgetting policies bound growth. Memory recall latency stays within executor budgets. It enables long-running tasks, context preservation across sessions, and organizational learning.

<!-- src: faq-registry#faq-10, Directive section 18, Q10 -->

## 11. What tools can agents use?

Agents use a canonical tool vocabulary of 7 tools: read (file contents), edit (exact string replacement), grep (regex search), list (directory entries), bash (shell commands), webfetch (HTTP/HTTPS fetch), and task (launch sub-agent). Legacy aliases (write→edit, execute→bash, delegate→task, web_search→webfetch) are accepted for backward compatibility. The ToolRunner validates against the canonical list; unknown tools return an error. Agents do not have unrestricted shell access — tools are isolated execution environments.

<!-- src: faq-registry#faq-11, Directive section 18, Q11 -->

## 12. What models does LightSpeed use?

LightSpeed uses a model-agnostic, provider-agnostic routing architecture with 9 LLM providers configured. The routing principle: OPEN/LOCAL FIRST → OPEN-WEIGHT MODELS → LOCAL INFERENCE → SELF-HOSTED/LOW-COST INFRASTRUCTURE → COMMERCIAL MODELS WHEN THEY PROVIDE A MATERIAL QUALITY/LATENCY/CAPABILITY ADVANTAGE → GOVERNED MODEL ROUTING. Local Ollama models (free) handle routine classification, extraction, summarization, embeddings, and repetitive workflows. Mid-tier models handle reasoning, planning, synthesis. Premium models handle exceptional reasoning, complex generation, difficult edge cases. Human handles decisions, approvals, accountability. We do not present commercial proprietary models as the default for every task.

<!-- src: faq-registry#faq-12, Directive section 18, Q12 -->

## 13. Why does LightSpeed prioritize open and open-weight models?

Open-source and open-weight AI is a cornerstone of LightSpeed's operating philosophy and business model — designed for African cost realities, constrained infrastructure, intermittent connectivity, data sovereignty, local deployment, low-bandwidth environments, local compute where appropriate, open model portability, provider independence, and avoiding unnecessary API costs. The architecture follows: use the least expensive model that can reliably do the job. We distinguish accurately between open-source software, open-weight models, commercially licensed models, and hosted APIs.

<!-- src: faq-registry#faq-13, Directive section 18, Q13 -->

## 14. Can LightSpeed operate without expensive API calls?

Yes. The platform is engineered for local-first operation with free local models via Ollama for budget-constrained deployments. Routine tasks (classification, extraction, summarization, embeddings, repetitive workflows) run on local open-weight models at near-zero marginal cost. Commercial APIs are only routed when they provide a material quality/latency/capability advantage. This is not theoretical — LightSpeed itself operates this way daily.

<!-- src: faq-registry#faq-14, Directive section 18, Q14 -->

## 15. Can LightSpeed run locally?

Yes. The platform supports offline-first operation on local infrastructure with a Zero-Cloud Boundary option for state, health, and financial data. The AI Company Builder license (E1) runs on your laptop or VPS — self-hosted, provider-agnostic, and extensible. Local Ollama models provide free inference for routine tasks. Data never leaves your infrastructure unless you configure cloud routing.

<!-- src: faq-registry#faq-15, Directive section 18, Q15 -->

## 16. Can LightSpeed operate in low-bandwidth environments?

Yes. The architecture is engineered for African infrastructure realities: intermittent connectivity, low bandwidth, and constrained compute. Local-first inference, offline-first sync, and model routing that prefers local models mean the platform functions without persistent high-speed connectivity. WhatsApp-native workflows operate on 2G/3G networks. This is a design principle, not an afterthought.

<!-- src: faq-registry#faq-16, Directive section 18, Q16 -->

## 17. How does LightSpeed approach data sovereignty?

Data sovereignty is a default posture, not a feature flag. The platform offers a Zero-Cloud Boundary option for state, health, and financial data — meaning data never leaves your infrastructure. Malawi Data Protection Act 2017/2024 compliance and GDPR-level handling apply from day one for donor and UN data flows. Cross-border LLM transfer requires explicit consent workflows. Every engagement clears 4 governance gates (Contract, DPA, Compliance, Security) before work begins.

<!-- src: faq-registry#faq-17, Directive section 18, Q17 -->

## 18. What sectors does LightSpeed work with?

LightSpeed targets 10 sectors across Malawi, SADC, and Africa: Financial Services (proven), Healthcare & Public Health (future), Agriculture & Agritech (pilot), Education & Academia (pilot), Government & Public Sector (current capability), Regulators & Standards Institutions (demonstration), Research & Universities (demonstration), SMEs & Private Enterprise (fieldable), Development & Nonprofit Organizations (pilot), Technology & Digital Businesses (proven in-house). Each sector carries an explicit honesty badge — we do not claim experience we do not have.

<!-- src: faq-registry#faq-18, Directive section 18, Q18 -->

## 19. Does LightSpeed work with universities?

Yes, in active development. LightSpeed is building University & Talent Capacity Building programs in partnership with Malawian universities (MUBAS, UNIMA) to build a sovereign agentic-AI talent pipeline across Southern Africa. The National AI Strategy consultation submission advocates for governing agentic AI alongside generative AI. We do not claim formal signed partnerships — this work is in active development and we say so honestly.

<!-- src: faq-registry#faq-19, Directive section 18, Q19 -->

## 20. Does LightSpeed work with regulators?

Yes, in active development. The SADC Agentic AI Governance Framework was authored by CEO Jack Mlusu and submitted to digital ministers, MACRA, CRASA, central banks, and regional development banks — aligned with the AU Continental AI Strategy. LightSpeed engages regulators through policy submissions and framework development. We do not claim formal regulatory endorsements or approvals — this is policy work in progress.

<!-- src: faq-registry#faq-20, Directive section 18, Q20 -->

## 21. What is Pharos?

Pharos is LightSpeed's in-house thought-leadership team — not a generic blog. Pharos turns LightSpeed's engineering, research, experimentation, and field observations into public intellectual work covering: Agentic AI, AI Company Building, African AI, Open/Open-Weight AI, AI Economics, AI Governance, AI Policy, AI Regulation, AI Safety, Digital Transformation, Data Architecture, AI Use Cases, Research, Universities, Academia, SADC Technology, Malawi Technology, Sovereign AI, and Resource-Constrained AI Deployment. Every major insight links back to Use Cases, Solutions, Sectors, AI Company Builder, and Contact/engagement.

<!-- src: faq-registry#faq-21, Directive section 18, Q21 -->

## 22. What is a Use Case?

A Use Case answers "What can LightSpeed actually do?" Each Use Case communicates: problem, workflow, agents involved, inputs, orchestration, tools, human approval, output, business value, sector, solution, and readiness/evidence status. Status labels: LIVE, PROVEN IN-HOUSE, PILOT, DEMONSTRATION, FIELDABLE, FUTURE. We never fabricate customer evidence, imply paying clients unless verified, or invent testimonials, logos, contracts, deployments, metrics, partnerships, government approvals, university partnerships, or regulator endorsements.

<!-- src: faq-registry#faq-22, Directive section 18, Q22 -->

## 23. What does 'Proven In-House' mean?

'Proven In-House' means the capability, workflow, or outcome has been verified running inside LightSpeed Holdings' own operations — not delivered to an external paying client. Examples: the 5-tier approval matrix, SHA-256 audit trails, 4 governance gates, RBAC with 90-day key rotation, canonical registry numbers (90 agents, 20 departments, test counts), and sovereign offline-first operation are all proven in-house because LightSpeed uses them daily to run itself.

<!-- src: faq-registry#faq-23, Directive section 18, Q23 -->

## 24. Is every Use Case a paying-client deployment?

Honestly: no. Nothing has been delivered to paying clients — all offers are fieldable in 2026, in pilot, or in active development, and every proof point on this site carries an explicit honesty badge. We would rather show you exactly where we are than invent a track record. Use Cases include: LIVE (J&S StopOver Bar), PROVEN IN-HOUSE (LightSpeed meta use case), PILOT (agricultural cooperative, university student management, health M&E, VSLA, Chichewa AI), DEMONSTRATION (enterprise automation, consulting firm scale, non-profit ops, government compliance, e-commerce, healthcare admin, financial services), FIELDABLE (SME digital presence), FUTURE (healthcare deployment).

<!-- src: faq-registry#faq-24, Directive section 18, Q24 -->

## 25. How do we engage LightSpeed?

Start a conversation or request an AI Readiness Assessment. We will tell you honestly whether we can help, and exactly what it takes to start. Qualified enquiries get a response within two business days. The engagement path: Brief → AI Readiness Assessment → Governance Gates (G1-G4) → Scoped Proposal → Deployment. No hidden steps, no surprise costs.

<!-- src: faq-registry#faq-25, Directive section 18, Q25 -->

## 26. What does an AI Readiness Assessment involve?

A structured discovery engagement that evaluates your organization's data maturity, infrastructure readiness, governance capacity, team skills, and use-case viability for AI deployment. Deliverables: assessment report with gap analysis, prioritized use-case roadmap, governance requirements, infrastructure recommendations, and phased engagement plan. Priced for regional markets — accessible pricing in local currency rather than foreign-currency consultancy rates.

<!-- src: faq-registry#faq-26, Directive section 18, Q26 -->

## 27. What does LightSpeed cost?

Engagements are scoped per brief and priced for regional markets — accessible pricing in local currency (MWK) rather than foreign-currency consultancy rates. There is no public rate card; start a conversation and we will tell you plainly what your project takes. Example offer pricing (from catalog): Business Website MWK 800,000 (~$450), E-Commerce MWK 1,800,000 (~$1,000), AI Company Builder License MWK 3,500,000 (~$2,000) + support retainer. International NGO engagements quoted in USD. 50% upfront / 50% on delivery for one-off projects.

<!-- src: faq-registry#faq-27, Directive section 18, Q27 -->

## 28. How quickly can an engagement begin?

Qualified enquiries receive a response within two business days. AI Readiness Assessments can begin within one week of agreement. Platform licensing (E1) setup takes 1-2 weeks. Pilot engagements typically start within 2-3 weeks after governance gates clear. The bottleneck is governance (G1-G4), not capacity — we prioritize doing it right over doing it fast.

<!-- src: faq-registry#faq-28, Directive section 18, Q28 -->
