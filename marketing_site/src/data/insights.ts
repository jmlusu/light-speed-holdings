/* LightSpeed Holdings - Insights article data (CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §16).
   Data module instead of MDX: no new toolchain needed (YAGNI - decision recorded
   when the Wayfinder map closes). Every claim is grounded in first-party repo
   sources declared per article (`source`). No invented numbers, no unproven
   superlatives - see research/site-claims-ledger.md.
   --brand-navy
   --brand-red
   --brand-cyan */

export type InsightBlock =
  | { kind: 'h'; text: string }
  | { kind: 'p'; text: string }
  | { kind: 'ul'; items: string[] }
  | { kind: 'quote'; text: string; cite?: string };

export interface InsightArticle {
  slug: string;
  title: string;
  topic: string;
  dek: string;
  category: string; // must be one of insightCategories (siteContent.ts)
  readMins: number;
  publishedAt: string; // ISO date
  source: string; // first-party provenance (honesty grounding)
  /** Dated correction note rendered above the body; body text stays unchanged for the audit trail. */
  correction?: { date: string; text: string };
  seo?: { title: string; description: string }; // head metadata; title <=~65ch, description <=~155ch
  blocks: InsightBlock[];
  relatedSolutions: string[]; // solution slugs (siteContent.ts `solutions`)
  relatedSectors: string[]; // canonical sector slugs (sector-registry.ts)
}

export const insightArticles: InsightArticle[] = [
  {
    slug: 'open-source-cost-architecture',
    title: 'Cutting AI Costs With Open Source: Why the Architecture Matters More Than the Arithmetic',
    topic: 'COST ARCHITECTURE',
    dek: 'In Malawi the binding constraint is not token prices. It is connectivity that costs 8.45% of GNI per capita. The open-source cost argument is architectural, not arithmetic: route to local models, rent open-weight APIs where competition has capped the price, and spend the difference on what actually binds.',
    category: 'African AI',
    readMins: 8,
    publishedAt: '2026-10-12',
    seo: {
      title: 'Cutting AI Costs With Open Source | LightSpeed',
      description:
        'Token prices are not the binding constraint in Malawi, connectivity is. Why open-source AI cost is an architecture argument, with honest limits.',
    },
    source:
      'docs/Pharos/research-briefs/2026-10-12-open-source-costs.md · docs/Pharos/research-briefs/2026-10-12-africa-open-source-ecosystem.md · pyproject.toml · package-lock.json · src/ai_company/llm/providers/ · src/ai_company/llm/cost_tracker.py · src/ai_company/llm/client.py · docs/adr/004-multi-provider-llm.md · docs/ARCHITECTURE_REMOTE_RUNTIME.md · docs/Pharos/case-study-pipeline.md',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      {
        kind: 'p',
        text: 'In Malawi the binding constraint is not token prices. It is connectivity that costs 8.45% of GNI per capita. The open-source cost argument is architectural, not arithmetic: route to local models, rent open-weight APIs where competition has capped the price, and spend the difference on what actually binds.',
      },
      { kind: 'h', text: 'The constraint, not the price list' },
      {
        kind: 'p',
        text: 'Malawi\'s internet penetration sits at 27.7% against a SADC average of 59.8% (our PESTEL 2026 baseline, an internal scan, labelled as such), and household computer ownership is thin enough that the deployment target is a phone on an intermittent link, not a workstation on fibre. Freedom on the Net\'s 2024 Malawi chapter, citing ITU, NSO and World Bank data, puts rural internet usage at 13.5% against 40.7% urban. It is an advocacy-organisation report, but one whose direction nobody disputes. Any credible AI cost strategy for this environment has to start from the network bill and the device class, not from a cloud console\'s pricing page.',
      },
      { kind: 'h', text: 'What the stack is actually built on' },
      {
        kind: 'p',
        text: 'Our stack runs on permissive-licensed open source end to end: MIT-licensed React, Vite and Tailwind on the frontend, Apache-2.0 TypeScript, and Ollama plus llama.cpp providers behind a single model router. Our own codebase remains proprietary today, with Apache 2.0 targeted at v1.0. That distinction matters. The open-source argument here is about the foundation we build on, not a claim that our own code is already open. Two honesty notes follow the inventory. Our npm lockfile records 292 license fields (react, tailwindcss, vite and vitest are MIT; typescript is Apache-2.0). Our Python lockfile records none. uv.lock carries zero license fields, so Python dependency licenses are unrecorded in-repo. We treat that as a documentation gap, not a licence conclusion.',
      },
      {
        kind: 'ul',
        items: [
          'Python core: Python 3.12+, Typer, FastAPI, Uvicorn, Pydantic 2.8+, Jinja2, httpx and cryptography: per-package licences not recorded in the lockfile.',
          'LLM runtime: Ollama and llama.cpp providers (MIT upstream) alongside an OpenAI-compatible provider, all resolved through one model router.',
          'Frontend: Vite, React, Tailwind, TypeScript, Vitest and Playwright under MIT or Apache-2.0.',
          'Quality gates: four CI gates, ruff lint, mypy typecheck, pytest on Ubuntu and Windows, plus a bandit security gate in pre-commit.',
          'Delivery: one Python CLI, one FastAPI dashboard, one Vite/React single-page app, packaged in a multi-stage python:3.12-slim container with a non-root user; no paid SaaS sits in the runtime path.',
        ],
      },
      { kind: 'h', text: 'Free by ledger convention, a design choice, not a saving' },
      {
        kind: 'p',
        text: 'Local inference is priced at zero in our cost ledger by convention, a deliberate architecture choice and not a measured saving, because models served through Ollama or llama.cpp carry no per-token charge. The ledger comment next to the entry says it plainly: local models are effectively free. What the convention buys is routing freedom. Our model router resolves across OpenAI-compatible, Ollama and llama.cpp providers, so adding or swapping a provider is a configuration decision rather than a code rewrite, and a deployment that loses its link can fall back to models running on hardware it controls. Our architecture decision record for multi-provider LLM access selects Ollama for the fast tier on exactly this basis, zero-cost inference for development and testing, with live integration tests run against a local instance.',
      },
      {
        kind: 'p',
        text: 'All 91 agents in our company, 90 AI plus one human CEO, are runnable locally on Ollama/llama.cpp, per our remote-runtime architecture documentation. Open source is our cost architecture, not a licensing shortcut. The machinery of the company (orchestration, approvals, audit, dashboard) does not require a single paid runtime dependency to operate.',
      },
      {
        kind: 'quote',
        text: 'Route to local models where the marginal token is free by design, rent open-weight APIs where competition has already capped the price, and spend the difference on the constraints that actually bind.',
        cite: 'Cost-architecture thesis · docs/adr/004-multi-provider-llm.md',
      },
      { kind: 'h', text: 'Cost controls that are code, not policy' },
      {
        kind: 'p',
        text: 'A cost architecture is only as good as the controls that enforce it. In our stack the controls live where the spend happens, inside the LLM client, as code with tests, not as a policy memo:',
      },
      {
        kind: 'ul',
        items: [
          'A MODEL_COSTS table in dollars per million tokens, sourced to public pricing pages as of 2025 and dated by design, so pricing drift is visible rather than assumed.',
          'Daily and per-task budget caps, plus token-bucket rate limiting, so a runaway loop hits a wall instead of an invoice.',
          'A response cache that deduplicates repeated calls, and a prompt compressor that shrinks inputs before they are billed.',
          'Retries capped at five attempts behind a thread-safe circuit breaker, so retry storms cannot amplify spend.',
          'A five-tier human approval matrix bounding blast radius, from automatic action up to CEO-only, with first-party access control, PII detection and content filtering in our own security module.',
        ],
      },
      { kind: 'h', text: 'The external evidence: open weights set the floor' },
      {
        kind: 'p',
        text: 'Since OpenAI put gpt-oss-20b under Apache 2.0 in August 2025, hosted versions have traded at $0.075 per million input tokens on Groq, a price set by open weights and host competition, not by a vendor\'s list price. That figure comes from a third-party commercial price tracker (llmcostlab.com; prices re-read 2 October 2026), and per-token prices move weekly. Treat it as a floor being pushed down, not a quote. Two facts around it matter more than the number. OpenAI does not serve gpt-oss through its API. The weights run on vLLM, Ollama or llama.cpp on infrastructure you control (vendor documentation; terms change without notice). And the hardware figures, 16GB for the natively quantized 20b and 80GB for the 120b, are vendor-stated. A comparable MIT-licensed option, DeepSeek V4 Flash, was tracked at $0.30 per million input tokens in the same pass.',
      },
      {
        kind: 'p',
        text: 'For market-scale framing only, a Linux Foundation blog post from September 2025, advocacy commentary and not an audited study, projected Africa\'s AI market at roughly $6.4 billion by the end of 2025 and framed open source as the continent\'s democratising pathway. We cite it as framing, not evidence. A projection is not proof of anything we have done.',
      },
      { kind: 'h', text: 'Three moves, in order' },
      {
        kind: 'ul',
        items: [
          'Route to local models where the marginal token is free by ledger convention: Ollama or llama.cpp on hardware you own.',
          'Rent open-weight APIs where host competition has already capped the price, the gpt-oss-20b floor above.',
          'Spend the difference on what actually binds: connectivity, devices, power, and the human approvals that keep agents governable.',
        ],
      },
      {
        kind: 'p',
        text: 'The third move is the one most cost essays skip. Cheaper tokens do not fix a network that costs 8.45% of GNI per capita, a fleet of phones as the primary device class, or a governance gap that turns savings into incident reports. Local open-weight models also mean budget-constrained deployments avoid per-seat SaaS agent licensing entirely. Our own finance SOP documents free Ollama models as a budget tier, and the use-case catalog positions them for budget-constrained deployments.',
      },
      { kind: 'h', text: 'Offline has already been demonstrated' },
      {
        kind: 'p',
        text: 'Researchers have already shown offline-first LLM inference holding 1 to 3 second response times on legacy CPU-only hardware with no cloud dependency, serving 120 students and 9 instructors under limited connectivity. This is the Arapai architecture, reported in a 2026 education-domain preprint (arXiv:2603.03339) that was not peer-reviewed at the time we fetched it. One preprint is not a market. It is, however, proof that the pattern our provider-agnostic routing is built to exploit runs on hardware of the class our market actually has.',
      },
      { kind: 'h', text: 'Sovereignty, skills, and the budget that outlives the grant' },
      {
        kind: 'p',
        text: 'In formal commentary on Malawi\'s National AI Strategy, we recommended open-weight, locally hosted models and air-gapped inference. Sovereignty and budget are the same design constraint. Data that never leaves the jurisdiction is data that never incurs an egress bill, and our privacy posture follows the same logic: local processing with no external transmission when local models serve the request. Malawi\'s Data Protection Act (2024) is in force but has no autonomous-systems interpretation yet, which is another reason the processing boundary should be architectural rather than promised.',
      },
      {
        kind: 'p',
        text: 'On skills, the external picture is encouraging and specifically bounded. OpenUK\'s Open Source Africa Report (27 March 2026, fetched 12 October 2026) reads GitHub and Octoverse data to report roughly 3.4 million new Africa-and-Middle-East developers across 2024 and 2025, with country detail for Kenya, Nigeria and Rwanda. The coverage excludes Malawi, and we will not project those growth rates onto it. What the report supports is narrower and still useful. Open-source participation on the continent is measurable and growing, and it is the pool local engineers can be hired into and trained on, exactly this kind of stack.',
      },
      {
        kind: 'p',
        text: 'Sustainability is the quieter half of the argument. Our roadmap frames category leadership while national and regional strategies are still being defined. Malawi validated its UNESCO AI Readiness Assessment in July 2026 and is drafting its first National AI Strategy with support from UNDP and the PPP Commission\'s Digital Malawi Acceleration Project, so the consultation window is open. The AU\'s Continental AI Strategy (2024) is a non-binding reference framework and SADC\'s regional framework is still at an early stage, which leaves room for a practical implementation story rather than a policy adopter\'s press release. We claim no donor funding, secured or lost.',
      },
      { kind: 'h', text: 'The counter: J&S StopOver Bar' },
      {
        kind: 'p',
        text: 'Architecture arguments are cheap until they touch a counter. J&S StopOver Bar, a real non-tech SME, is the one LIVE commercial proof point in our case pipeline: inventory, procurement and pricing agents running on a small business\'s actual numbers, built in-house and documented openly. It matters to this thesis for a blunt reason. If the only proof sits inside a company with an engineering department, the region\'s risk officers are right to be skeptical. A small business running the same stack is the test that it is not reserved for hyperscaler customers.',
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'We have mechanisms and inventories, not published savings measurements. There is no measured before/after in our repository, so this article claims no dollar savings, no percentage cost reduction, no bandwidth-savings figure and no cost-per-workflow number. Those would require evidence we do not have. The zero price on local inference is a ledger convention. Offline-first, zero-cloud and SHA-256-chained append-only audit trails are design and implementation claims, not externally audited guarantees; our decision logs are auditable on request. External prices above are third-party tracker figures that move weekly and must be re-verified before anyone relies on them. J&S StopOver Bar is a real SME in our case pipeline, not a paid client delivery. Nothing has been delivered to paying clients yet, and the proof you can inspect is the stack, the gates, and the ledger.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'Connectivity, not token prices, is the primary binding constraint in Malawi, where mobile broadband costs 8.45% of GNI per capita and a 4GB bundle runs about 6,000 kwacha, roughly 12% of the minimum monthly wage, making every megabyte an agent does not push over the network a real cost rather than an optimization.',
          'Open-source AI cost is an architectural argument, not arithmetic: route to local models, rent open-weight APIs where competition has capped the price, and spend the difference on what actually binds, since the argument is about foundation, not licensing shortcuts.',
          'Savings should be directed toward actual binding constraints like network, devices, power, and the human approvals that keep agents governable, rather than assuming cheaper tokens alone will resolve deployment challenges.',
        ],
      },
    ],
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'business-automation'],
    relatedSectors: ['agriculture', 'financial-services', 'government'],
  },
  {
    slug: 'dual-economy-ai-pricing',
    title: 'Pricing Agentic AI in a Dual Economy: Kwacha Ladders, Dollar Retainers, and Paying for What You Run',
    topic: 'AI PRICING',
    dek: 'Take a US list price, divide by the exchange rate, hope. That method died on the night the kwacha devalued 44%. Malawi\'s market pays in kwacha; its NGO and regional work is quoted in dollars. So we run two rails: a published MWK ladder, USD-denominated retainers, and mobile-money collection built in from day one. Here is the ladder, the reasoning, and an honest account of what has actually been sold.',
    category: 'Market intelligence',
    readMins: 7,
    publishedAt: '2026-10-12',
    seo: {
      title: 'Pricing Agentic AI in a Dual Economy | MWK and USD',
      description:
        'A dollar list price divided by the exchange rate died with the 44% kwacha devaluation. Kwacha ladders, dollar retainers, mobile-money rails.',
    },
    source:
      'docs/Pharos/research-briefs/2026-10-12-ai-economics-sadc.md · docs/client-facing/USE-CASE-CATALOG.md · docs/marketing/competitive-landscape.md · content/drafts/faq.md · results/pestel-lightspeed-2026.md · src/data/insights.ts · docs/venture-studio/12-T3-call-scripts.md · docs/Pharos/articles/h-a-o-m-t-g-v-seven-layers.md · docs/Pharos/roadmap.md · docs/Pharos/case-study-pipeline.md',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      {
        kind: 'p',
        text: 'The standard way to price software in an emerging market is arithmetic: take the vendor\'s dollar list price, divide by the exchange rate, and hope the rate holds until the invoice clears. In Malawi that hope has already failed once. The kwacha devalued 44% in a single night in November 2023 and has been managed at roughly 1,716 to 1,751 per US dollar since (our PESTEL 2026 baseline, an internal scan, labelled as such). A dollar price that looked competitive in 2023 can now be wrong for a Blantyre SME by more than a month\'s margin. So we do not price on one rail. Our catalog states it directly: pricing is "anchored in dual currency (MWK for local clients, ~USD for international)", kwacha for Malawian institutions and dollars for the international organisations that budget in them. This article lays out the ladder, the reasoning under it, and what has actually been sold so far.',
      },
      { kind: 'h', text: 'Two rails, one catalog' },
      {
        kind: 'p',
        text: 'One clarification before the numbers: this is offer language, not transacted revenue. The MWK figures are stated in kwacha with ~USD estimates that are explicitly labelled estimates in the source and pending prospect validation before public reliance. The USD-quoted side (international NGO and regional work) is documented in our FAQ and catalog, but no public rate card exists, and none will be invented here. With that boundary set, the published ladder:',
      },
      {
        kind: 'ul',
        items: [
          'Licensing: MWK 3,500,000 (~$2,000 estimate), paired with a USD-denominated support retainer at $200/month.',
          'Minimum viable deployment: MWK 150,000 (~$85), the entry rung for a first automation.',
          'Business website (A1): MWK 800,000 (~$450).',
          'E-commerce store (A2): MWK 1,800,000 (~$1,000).',
          'WhatsApp chatbot (B1): MWK 1,500,000 (~$850) plus MWK 100,000/month hosting.',
          'One-off payment terms: 50% upfront, 50% on delivery.',
        ],
      },
      { kind: 'h', text: 'Why two currencies, not one' },
      {
        kind: 'p',
        text: 'The two rails exist because the two buyers carry different risks. A Malawian institution earns kwacha, borrows in kwacha, and was taught by the 2023 devaluation that a dollar-denominated invoice is a currency bet it did not ask to make. An international NGO or regional programme budgets in dollars twelve months ahead and cannot plan against a kwacha figure that moves. Quoting each in the currency it carries is not a discount tactic. It is risk sitting with the party that can actually hold it. Every ~USD figure above stays the catalog\'s own estimate; we do not convert kwacha prices at rates of our own invention.',
      },
      {
        kind: 'p',
        text: 'The collection side matters as much as the quote. Seventy-five percent of Malawian adults already transact on mobile money (MWK 8.6 trillion in volume in 2025) on Airtel Money and TNM Mpamba, rails our catalog says are "built in from day one, not bolted on". A price in kwacha is only as real as the phone it can be paid from, and in this market the phone already is the bank.',
      },
      {
        kind: 'quote',
        text: 'Dual-economy pricing so institutions pay for what they run, not for idle hyperscaler capacity.',
        cite: 'src/data/insights.ts:69 · docs/client-facing/USE-CASE-CATALOG.md:76',
      },
      { kind: 'h', text: 'The market underneath the price' },
      {
        kind: 'p',
        text: 'A ladder is only defensible against the market it climbs. Our PESTEL 2026 baseline (an internal scan, cited as such) describes it plainly:',
      },
      {
        kind: 'ul',
        items: [
          'Demographics: ~22.2m people, ~62% under 25, median age 19.2, ~18 to 20% urban.',
          'Informal-first demand: ~1.6m MSMEs, 90%+ informal, the addressable market is informal-first.',
          'Slow growth, projected: GDP 1.9% (2025) rising to 2.3% (2026 projected).',
          'Easing but high inflation: 28.4% average in 2025, ~22% average projected for 2026.',
          'Connectivity is the constraint, not demand: 27.7% internet penetration against a SADC average of 59.8%.',
        ],
      },
      {
        kind: 'p',
        text: 'Every figure in that list carries the same caveat: it is our own scan, not an official statistic we commissioned. What it explains is the shape of the ladder. An economy that is young, overwhelmingly informal and phone-first cannot start at seat licences and annual commits. It starts at MWK 150,000 for a first deployment and MWK 800,000 for a website, with the dollar retainer reserved for the buyers who already budget in dollars.',
      },
      { kind: 'h', text: 'The competitor is the spreadsheet' },
      {
        kind: 'p',
        text: 'The buyer\'s real alternative is not another AI vendor. It is the stack they already have: Kobo and Google Forms feeding spreadsheets, plus global consultancies priced out of reach for most of the market. Our sales doctrine meets that directly: no rip-and-replace; we sit beside the current M&E sheets for one cycle, and the 90-day pilot is a documented offer, classified internally as an offer rather than a result. When a risk officer says no, they are usually raising one of four legitimate objections (bandwidth and devices, data location, forever-maintenance, prior AI failures). The honest answer to all four is a bounded pilot, not a bigger claim.',
      },
      {
        kind: 'p',
        text: 'On the local competitive set, an internal read (labelled as such): nearly every Malawi player above sells custom software, and none sells a governed agentic organisation. The category is empty locally. Those named players do not disclose pricing, and the global consultancies sell governance-shaped messaging at enterprise rates with no SADC-specific price points we can cite. So we cite none. The competitor that matters is the spreadsheet, and the price has to beat the cost of staying where they are.',
      },
      { kind: 'h', text: 'What has actually been sold' },
      {
        kind: 'p',
        text: 'Here is the constraint that governs everything above: nothing has been delivered to paying clients yet. What exists is operating evidence. J&S StopOver Bar, a real non-tech SME, is the single LIVE commercial proof point: inventory, procurement and pricing agents running on a small business\'s actual numbers. The 91-agent company itself (90 AI agents and one human CEO) is proven in-house, verified by a direct count of the company registry on 23 September 2026. The agricultural coop, health monitoring and VSLA/SACCO work are pilots, honest about being pilots, with no signed partnership or engagement to name. The WhatsApp automation offer is blocked pending security review. No revenue figures, win rates or pipeline values appear here because none exist to appear.',
      },
      { kind: 'h', text: 'A category being defined, not settled' },
      {
        kind: 'p',
        text: 'Pricing lands in a policy environment that is still moving. Malawi validated its UNESCO AI Readiness Assessment in July 2026 and is drafting its first National AI Strategy; the Data Protection Act (2024) is in force but is not AI-specific; an AI Bill was announced in August 2026 with its status moving; the AU\'s Continental AI Strategy (2024) is a non-binding reference. One naming point of honesty: the SADC "Agentic AI Governance Framework" is our own policy proposal, not an adopted standard, and our engagement on it is advisory and pilot work, not deployed client systems. A category being defined is precisely why governance architecture has to ship before throughput. It is also why a published price, stated plainly in the currencies the market actually uses, is worth more than a discount introduced at signature.',
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'What this article does not contain is as deliberate as what it does: no TAM, SAM or SOM figure for Malawi or SADC agentic AI; no adoption percentage for African enterprises; no competitor prices, because they are undisclosed; no FX conversions beyond the catalog\'s own ~USD estimates; no signed-revenue, win-rate or pipeline numbers, because no paying client delivery exists yet. The ladder is offer language pending prospect validation, not a revenue record. The policy citations are current as of October 2026 and should be re-verified if this is read more than 30 days out. The pricing is defensible because it is published, collectable on rails that already exist, and denominated in the currency the buyer carries. That is the whole claim, and it is enough to start a conversation on.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'Kwacha devaluation makes single-currency pricing unreliable in Malawi, where the 44% devaluation in a single night in November 2023 means a dollar price that looked competitive in 2023 can now be wrong for a Blantyre SME by more than a month\'s margin, so hoping the rate holds until the invoice clears is a failed strategy.',
          'Dual-rail pricing (MWK ladders, USD retainers) aligns with buyer currency risk by quoting each in the currency it carries, placing risk with the party that can actually hold it, and every ~USD figure stays the catalog\'s own estimate without independent conversion.',
          'Mobile money rails built in from day one are essential for local collectability, since 75% of Malawian adults already transact on mobile money (MWK 8.6 trillion in volume in 2025) on Airtel Money and TNM Mpamba, making the phone the de facto bank.',
        ],
      },
    ],
    relatedSolutions: ['business-automation', 'digital-presence', 'boardroom-briefing'],
    relatedSectors: ['financial-services', 'agriculture', 'government'],
  },
  {
    slug: 'five-tier-approval-matrix',
    title: 'The Five-Tier Approval Matrix: How Friction Scales With Risk in a 90-Agent Company',
    topic: 'AI GOVERNANCE',
    dek: 'A permission system that gates every action drowns its humans. One that gates nothing is not a company. The middle is a tier table in code and a timeout that never means yes.',
    category: 'AI governance',
    readMins: 7,
    publishedAt: '2026-10-12',
    seo: {
      title: 'The Five-Tier Approval Matrix for Agent Governance',
      description:
        'A permission system that gates everything drowns humans. One that gates nothing is not a company. The tier table lives in code; a timeout never means yes.',
    },
    source:
      'src/ai_company/orchestrator/tier_rules.py · src/ai_company/executor/hitl_gate.py · src/ai_company/orchestrator/approval.py · docs/Pharos/pillars/02-5-tier-human-in-the-loop.md · docs/APPROVAL-UX-SPEC.md',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      {
        kind: 'p',
        text: 'Ask a team how they govern their AI agents and you will hear a policy. Ask them what happens when nobody answers an approval request and you will learn whether the policy is real. That second question is the one this article is about, because LightSpeed Holdings runs 91 agents (90 AI personas plus one human CEO) across 20 departments, and the only thing standing between that fleet and ungoverned action is a five-tier approval matrix enforced in code, not prose.',
      },
      { kind: 'h', text: 'The failure mode nobody designs for' },
      {
        kind: 'p',
        text: 'There are two ways to get permission wrong. Gate nothing, and an agent with shell access is an incident report waiting for a timestamp. Gate everything, and the humans drown: every read, every search, every status update lands in an approval queue until the queue is ignored, and an ignored queue is governance theater. The design principle that resolves this is short enough to remember under pressure: friction scales with risk. Low-risk work moves without asking. High-risk work cannot move without deliberate human action. The tier table is where that principle stops being a slogan.',
      },
      { kind: 'h', text: 'The five tiers, as the code defines them' },
      {
        kind: 'p',
        text: 'The implementation lives in tier_rules.py: an ApprovalTier enum with five values, each with a label, a default timeout, and a class of work it is responsible for. This is the table risk officers should ask to see from any vendor claiming governed agents. It is also the table we can produce, because it is ours:',
      },
      {
        kind: 'ul',
        items: [
          'Tier 0: Auto-Approve. Read-only work: listing, searching, recalling. No gate; the action executes and lands in the execution log. Most agent work lives here, which is correct.',
          'Tier 1: Notify. Low-risk writes humans should see in history but never in a queue: memory storage, routine status updates. Logged for audit, never blocking.',
          'Tier 2: Single Approver. Code edits, test execution, sub-threshold changes. One human must approve before the action proceeds.',
          'Tier 3: Two-Person Rule. Production paths, shell execution that reaches production, destructive or high-spend actions. Two distinct humans; the gate rejects a second signature from the first approver.',
          'Tier 4: CEO Only. Secrets, legal and compliance paths, financial and security exposure, constitutional moves like deploying a new agent. No substitute approver exists.',
        ],
      },
      {
        kind: 'p',
        text: 'Classification is not vibes. tier_rules.py maps tool defaults to tiers (read-only tools at Tier 0, edits at Tier 2) and then applies path and command rules on top. A fragment list for sensitive paths (secrets, .env files, audit directories, legal and compliance trees) escalates the action to CEO-only unconditionally. Production and deploy fragments escalate to the two-person rule. Dangerous commands, the ones that delete broadly or reach production systems, escalate the same way. The default tier is a floor; overrides only ever raise risk, never lower it.',
      },
      {
        kind: 'quote',
        text: 'Friction scales with risk. No silent failures. Auditability by default. Timeout is never final.',
        cite: 'LightSpeed approval doctrine · docs/APPROVAL-UX-SPEC.md',
      },
      { kind: 'h', text: 'What the gate does while a human is deciding' },
      {
        kind: 'p',
        text: 'A tier table is only half of governance. The other half is behavior at the boundary: what the system does while an approval is pending, and what it does when nobody answers. Three mechanics matter, and all three are implemented rather than proposed.',
      },
      {
        kind: 'p',
        text: 'First, requests persist. The executor-side HITL gate writes pending requests to disk, so a restart does not lose the ask and does not reset the clock into silence. An agent blocks on the gate; it does not route around it.',
      },
      {
        kind: 'p',
        text: 'Second, timeouts never approve. Per-tier deadlines sit in configuration (four hours at Tier 2, two at Tier 3, one at Tier 4) with a shorter default on the executor-side wait. When a deadline passes, the governance sweep moves the request from pending to expired: a visible, terminal state that must be re-submitted, written to the audit ledger on the way. No path in the system converts an unanswered request into a yes. That is the whole ballgame. A fallback deadline under agent pressure becomes default permission; ours becomes a louder ask.',
      },
      {
        kind: 'p',
        text: 'Third, unsafe requests are flagged at creation, not discovered at review. A tool call carrying shell metacharacters or a blocked pattern is marked at request time, so a pending item that will always be rejected is not silently retried into a loop. The audit trail records why it was flagged, not merely that it died.',
      },
      { kind: 'h', text: 'What a risk officer should demand from any agent deployment' },
      {
        kind: 'p',
        text: 'None of this is exotic. It is the same discipline banks and hospitals learned decades ago, translated to a world where the actor is software. If you are evaluating agent governance (as a CRO, a regulator, a procurement lead), the transferable test is four questions:',
      },
      {
        kind: 'ul',
        items: [
          'Ask for the tier table. What classifies to which tier, and who approves what? If the answer is a policy slide rather than a mapping in code, keep asking.',
          'Test the timeout rule. Ask what happens at one minute past the deadline. If the answer is "it dropped" or "it approved," that is governance-shaped risk.',
          'Audit the audit trail. Who, when, why, in what order, and can the agent under review modify the evidence? If yes, the governance fails exactly where it must hold.',
          'Require two distinct approvers for irreversible actions. One signature on deletion, spend, or production deployment is one person away from an incident.',
        ],
      },
      { kind: 'h', text: 'The honest trade-off' },
      {
        kind: 'p',
        text: 'The tiers are not free. Tier 2 and Tier 3 requests block agents until humans respond, and human attention is the scarcest resource in the company. There are days when the queue is the controller of the workflow. The alternative is worse, and we have lived it: post-hoc review, where the governance layer arrives after the incident, playing catch-up while the agent that caused the problem is still running. The cost of the queue is the price of the permission. It is the discipline that makes a 90-agent company deployable outside a laboratory.',
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'LightSpeed runs this model in-house. The five-tier matrix is implemented in our platform code: the ApprovalTier enum, path and command escalation, per-tier timeouts, request persistence, the expired-state sweep, and metacharacter flagging are all in the repository, exercised by our own regression suite, not drafted for a deck. The pillar essay that narrates this system is a draft awaiting CEO review; the code it describes is not. What this governance has not yet earned is a client claim: no paid enterprise deployment has been delivered this stack. The operating evidence is our own company (91 agents, one human CEO, every gated action attributable), and the tier table above is what we would show a regulator today.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'Friction scales with risk: low-risk work moves without asking, high-risk work needs deliberate human action, and the tier table is where that principle stops being a slogan and becomes code, with classification mapped in tier_rules.py from read-only tools at Tier 0 to CEO-only at Tier 4, and SADC region context informing the graduated-autonomy model from fully supervised operation to cleared auditable autonomy as evidence accumulates.',
          'The tier table is where that principle stops being a slogan and becomes code, with secrets and legal paths unconditionally escalating to CEO-only, production and deploy paths hitting the two-person rule, and dangerous commands flagged at creation rather than discovered at review, with governance that scales with risk being the precondition that lets adoption happen at all.',
          'Timeout never approves: unanswered requests escalate through escalated_from linked back to the original request via the governance sweep, and nothing auto-approves on the way up, with per-tier deadlines (four hours at Tier 2, two at Tier 3, one at Tier 4) and a shorter default on the executor-side wait, and SADC\'s regional framework being still at an early stage leaving room for practical implementation.',
        ],
      },
    ],
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
    relatedSectors: ['financial-services', 'government'],
  },
  {
    slug: 'inside-a-90-agent-company',
    title: 'Inside a 91-Agent Company: What the Registry, the Queue, and the Approval Gate Actually Do',
    topic: 'AI COMPANY BUILDING',
    dek: 'Building ninety-one personas takes an afternoon. Making them safe to run takes a control plane: a registry, a message bus, and an approval gate that scales friction with risk.',
    category: 'AI Company Building',
    readMins: 8,
    publishedAt: '2026-10-12',
    seo: {
      title: 'Inside a 91-Agent Company | Registry, Queue, Gate',
      description:
        '91 agents (90 AI + 1 human CEO) across 20 departments. What the registry, message bus, and five-tier approval gate actually do.',
    },
    source:
      'company-registry.yaml · src/ai_company/orchestrator/tier_rules.py · src/ai_company/orchestrator/approval.py · src/ai_company/orchestrator/message_bus.py · docs/Pharos/pillars/01-built-a-90-agent-company.md · docs/APPROVAL-UX-SPEC.md',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      {
        kind: 'p',
        text: 'Most conversations about "AI companies" start with the model. Ours starts with the paperwork. LightSpeed Holdings runs 91 agents (90 AI personas plus one human CEO) across 20 departments. That count is not a marketing abstraction; it is a direct tally of company-registry.yaml, the single source of truth that defines every agent\'s identity, tools, approval level, and escalation path. The agents themselves are the easy part. A schema, a generator, and an afternoon will mint ninety-one personas. What took the discipline was everything that sits above them: how work is assigned, how actions are gated, and what happens when a human does not answer.',
      },
      { kind: 'h', text: 'The org is a registry, not a slide' },
      {
        kind: 'p',
        text: 'An AI-native company is not a chat window with a budget. It is an operating structure in which software owns defined work under human accountability. LightSpeed\'s structure is described by a seven-layer frame: Human, Agents, Orchestration, Memory, Tools, Governance, Value (H-A-O-M-T-G-V). Each layer is a design question, not a slogan. Humans keep strategy, ethics, leadership, and final answerability. Agents take research, monitoring, reporting, and other discrete knowledge work. Orchestration wires them together. Governance decides who must approve what.',
      },
      {
        kind: 'p',
        text: 'In practice, that structure is concrete files. company-registry.yaml lists every agent: id, department, reports_to, direct_reports, tools, approval_level, escalation_path, KPIs, and decision rights. The Chief of Staff reports to human_ceo and coordinates executives from CPO to CISO; a backend lead reports to the CTO; permissions are not folklore. They are fields. When someone asks "who can spend money?" the answer is a grep, not a meeting.',
      },
      { kind: 'h', text: 'The queue is the operating system' },
      {
        kind: 'p',
        text: 'Agents do not collaborate by osmosis. They collaborate through a task queue. The orchestrator\'s message bus persists work to a JSON inbox under a file lock, so concurrent agents, the dashboard, and the human operators cannot corrupt each other\'s updates. Every task carries identity and context; the briefing path turns a backlog of inbox items into something an agent can actually execute. This is unglamorous infrastructure, and it is the difference between ninety demos and a company. If you cannot point to where work lives between handoffs, you do not have an operating model; you have a pile of sessions.',
      },
      { kind: 'h', text: 'The control plane: five tiers, friction that scales with risk' },
      {
        kind: 'p',
        text: 'The layer that earned its keep is governance. Early on we did what most teams do: let agents act, then review afterwards. That approach died with one incident: a state-changing action no human had consciously authorized. Post-hoc review is archaeology. By the time you are reading the log, the action has already happened. The rebuild around a five-tier approval matrix, enforced in code rather than policy prose, is now the constitution of the company.',
      },
      {
        kind: 'ul',
        items: [
          'Tier 0: Auto-Approve. Read-only work: listing, searching, recalling. No gate; the action executes and lands in the log.',
          'Tier 1: Notify. Low-risk writes that humans should see in history but never in a queue: memory storage, routine status updates.',
          'Tier 2: Single Approver. Code edits, tests, sub-threshold changes. One human must approve; a timeout escalates rather than expires into silence.',
          'Tier 3: Two-Person Rule. Shell execution, production paths, destructive or high-spend actions. Two distinct humans (the second can never be the first), and a timeout climbs to the CEO.',
          'Tier 4: CEO Only. Constitutional moves: deploying a new agent, financial/legal/security exposure, changes to the rules of the company itself.',
        ],
      },
      {
        kind: 'p',
        text: 'Classification is not vibes. tier_rules.py maps tools and path fragments to tiers: secrets, legal, and compliance paths escalate to CEO-only; production and deploy paths hit the two-person rule; source and test paths require a single approver. Sensitive paths are tuples in code. When the executor evaluates a tool call, seniority caps and tool defaults combine into a tier, and the approval gate either lets it through or parks it for a human. The gate itself is a working store with versioned records, retention, and an append-only audit ledger of record: every request and every decision, including expiry sweeps that move stale pending items to EXPIRED instead of blocking a queue forever.',
      },
      {
        kind: 'quote',
        text: 'Friction scales with risk. Auditability is the default. Timeout is never final. It escalates; it does not silently pass.',
        cite: 'LightSpeed approval doctrine · docs/APPROVAL-UX-SPEC.md',
      },
      { kind: 'h', text: 'What broke, and what that taught us' },
      {
        kind: 'p',
        text: 'Three failures shaped the control plane more than any architecture slide. First, the post-hoc review failure above: governance that only inspects after the fact is not governance. Second, the silent-timeout trap. Early queues treated an unanswered approval as a soft failure; agents would stall or, worse, find a path that skipped the gate. The fix is boring and non-negotiable: every timeout produces a visible escalation, linked back to the original request via escalated_from, and nothing auto-approves on the way up. Third, metacharacter and shell-risk handling, flagged at request time so a pending tool call that will always be rejected is not silently retried into a loop.',
      },
      {
        kind: 'p',
        text: 'The pattern across all three is the same: make the dangerous path the explicit path. If an agent needs a human, the queue says so. If the human is late, the system says so again, upward. If the action is inherently unsafe as proposed, the request carries that fact forward instead of hiding it.',
      },
      { kind: 'h', text: 'Proof before promise' },
      {
        kind: 'p',
        text: 'Two proofs sit under this architecture. The first is the company itself: a running registry, a locked message bus, a five-tier gate, and append-only SHA-256 sealed audit trails exercised daily, not a lab toy and not a client deployment claimed where none exists. The second is deliberately small. J&S StopOver Bar is a real, non-tech SME in Malawi already using agentic decision support for pricing through an LLM-council methodology, with a documented arc from finance and inventory agents through procurement and operations to a human owner\'s dashboard. If the stack only works inside an engineering department, it is not a company model; it is a specialist tool. The SME is the test that it is neither.',
      },
      { kind: 'h', text: 'Starting from the registry' },
      {
        kind: 'p',
        text: 'For a bank, a ministry, or a cooperative asking how to begin: start with the registry, not the model. Define what work agents will own, which tools they may touch, who approves what, and where escalation lands, before wiring a single LLM call. Pick one workflow, put it behind a real gate, measure it against the old way, then widen. Retrofitting governance onto an ungoverned fleet is an order of magnitude harder than designing the tiers in from day one. That is the whole lesson of ninety-one agents in one sentence.',
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'LightSpeed runs this model in-house. The agent count is 91 (90 AI plus one human CEO) across 20 departments per company-registry.yaml, verified by direct count. The five-tier matrix, message-bus queue, and audit-ledger patterns ship in our own platform code: Tier 0 through Tier 4 classification, approval-gate persistence, and expiry sweeps are implemented, not proposed. J&S StopOver Bar is a real SME running agentic decision support; it is not a LightSpeed client engagement. No paid enterprise client has been delivered this stack yet. Client-facing badges on the site say the same thing: proven in-house first, fieldable and piloted where true, never claimed delivered when it is not.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'The registry is the single source of truth for 91 agents (90 AI plus one human CEO) across 20 departments per company-registry.yaml, verified by direct count, with each agent listing identity, department, reports_to, direct_reports, tools, approval_level, escalation_path, KPIs, and decision rights, and SADC region insights showing that agentic AI deployment requires local context awareness.',
          'The message bus persists work to a JSON inbox under a file lock, so concurrent agents, the dashboard, and human operators cannot corrupt each other\'s updates, and every task carries identity and context through the briefing path that turns a backlog of inbox items into something an agent can actually execute, with mobile-money rails built in from day one as in markets where Airtel Money and TNM Mpamba are default.',
          'The five-tier approval matrix governs actions with friction that scales with risk, from Tier 0 auto-approve for read-only work up to Tier 4 CEO only for secrets, legal, compliance, financial exposure, and constitutional moves like deploying a new agent, with graduated autonomy tiers as proposed in the SADC Agentic AI Governance Framework.',
        ],
      },
    ],
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
    relatedSectors: ['financial-services', 'government', 'education'],
  },
  {
    slug: 'offline-first-ai-for-africa',
    title: 'Offline-First AI for Africa: Designing for Bandwidth, Sovereignty, and Mobile-Money Reality',
    topic: 'AI IN AFRICA',
    dek: 'Low-bandwidth is not a deployment footnote. It is the design brief. Here is how offline-first routing, a zero-cloud boundary, and local models answer the four reservations risk officers actually raise.',
    category: 'African AI',
    readMins: 8,
    publishedAt: '2026-10-12',
    seo: {
      title: 'Offline-First AI for Africa | Bandwidth and Sovereignty',
      description:
        'Low-bandwidth is the design brief, not a footnote. How offline-first routing, a zero-cloud boundary, and local models answer the four reservations.',
    },
    source:
      'docs/RESERVATIONS-STRATEGY.md · docs/Pharos/pillars/03-agentic-ai-resource-constrained-africa.md · docs/Pharos/case-study-pipeline.md · src/ai_company/llm/providers/ · src/ai_company/model_router.py · research/site-claims-ledger.md',
    blocks: [
      {
        kind: 'p',
        text: 'The default deployment story for agentic AI assumes fibre, idle GPUs, and a data centre in another hemisphere. That story does not survive contact with a district clinic, a Lilongwe SME counter, or a ministry network that still runs legacy cores. In Malawi and across SADC, the binding constraints are bandwidth, power, device class, data-sovereignty law, and a legitimate fatigue with vendor hype. Offline-first is not a nice-to-have mode we bolt on for rural demos. It is the design principle: core functions run against local state and local models where the constraint demands it, and the system reconciles when the network returns. The workflow, not the cloud, is the unit of operation.',
      },
      { kind: 'h', text: 'The four reservations, named' },
      {
        kind: 'p',
        text: 'Decision-makers in the region do not object to AI out of technophobia. They raise four reservations, and they are right to. Our answer doctrine (honesty-badged, never claimed as delivered unless it was) starts by naming them without softening:',
      },
      {
        kind: 'ul',
        items: [
          'Bandwidth and resource constraints: inference and orchestration cannot assume always-on connectivity or new devices.',
          'Data protection: citizen and financial data cannot casually leave the jurisdiction; Malawi\'s Data Protection Act (2024) already binds it, with no published interpretation yet for autonomous systems.',
          'Technology debt: institutions run systems that already cost years of budget; nothing may require a rip-and-replace programme.',
          'AI skepticism: earned by demos that never changed an operating metric, and answered only by evidence.',
        ],
      },
      {
        kind: 'p',
        text: 'Each reservation maps to architecture, not a disclaimer. The sections below are how we engineer the answers in our own stack, with badges that say what is proven in-house, what is fieldable, and what is still in development.',
      },
      { kind: 'h', text: 'Offline-first routing, not offline brochureware' },
      {
        kind: 'p',
        text: 'Offline-first means the system is allowed to work when the network is bad or absent. In practice that shows up in three places we can point at in code and architecture docs. First, model routing with quota-first and offline-aware behaviour: when connectivity or budget is the constraint, traffic prefers free or local paths rather than failing into a spinner. The router\'s tier order (fast, standard, premium, with special free and override lanes) exists so cost and connectivity are routing inputs, not afterthoughts. Second, provider-agnostic execution: the LLM client is not welded to one cloud vendor. It resolves providers through the model router and can call OpenAI-compatible endpoints, Ollama, or llama.cpp. Local inference is a first-class provider class, not an undocumented fallback. Third, client surfaces that queue work and sync on reconnect: PWA offline action queues and WhatsApp-native flows so the interface meets users where they already are, without forcing an app download as a prerequisite for participation.',
      },
      {
        kind: 'quote',
        text: 'Low-bandwidth does not mean no-AI. It means AI designed for the constraint, which is usually the better engineering problem.',
        cite: 'Pharos pillar 03: resource-constrained Africa',
      },
      { kind: 'h', text: 'Zero-cloud boundary and sovereign-by-default' },
      {
        kind: 'p',
        text: 'The second reservation (where does our data go?) cannot be answered with a privacy policy alone. It is answered with a deployment boundary. Sovereign in-country processing is the default posture: processing happens where the data lives, audit trails stay local, and any cross-border flow to an external LLM is an explicit, documented governance decision rather than a silent side effect. For institutions that cannot risk external inference at all, a zero-cloud option exists in the architecture: orchestration and state on infrastructure they control. When a regulator asks who processed what, under what authority, and where it still resides, the answer should be a map and an audit log, not a promise slide. Malawi\'s DPA 2024 and GDPR-shaped expectations are treated as engineering constraints from day one; we never use client data to train models. Honesty badge: proven in-house for architecture and governance posture; specific consent-workflow productisation is still in active development where noted in our catalog.',
      },
      { kind: 'h', text: 'Local models and provider-agnostic routing' },
      {
        kind: 'p',
        text: '"Local model" is not one capability. It is a routing choice. Our providers module ships OpenAI-compatible, Ollama, and llama.cpp implementations behind a common provider interface, with circuit breakers, token accounting, response caching, and prompt compression as cross-cutting concerns. The model router escalates across fast → standard → premium tiers on failure and supports free and override lanes for budget-constrained or human-directed runs. That structure is what makes "run free models when connectivity or budget demands it" an operable policy rather than a whiteboard intention: the same client code path can target a cloud endpoint when the link is healthy and a local server when it is not, without rewriting the agents. Specific model weights and sizes vary by deployment hardware; we do not claim a single universal offline stack for every device class in the region.',
      },
      { kind: 'h', text: 'Mobile-money rails from day one' },
      {
        kind: 'p',
        text: 'Agentic AI that cannot touch how value actually moves in Malawi is a science project. Airtel Money and TNM Mpamba are not exotic edge cases in our market. They are default rails for SMEs and households, with PayChangu in the checkout mix where e-commerce is in scope. Our digital-presence and automation surfaces treat local mobile-money checkout as day-one integration, not a phase-two roadmap item, because the customer\'s money already moves that way. On the deeper financial-inclusion side, the case pipeline sketches agentic workflows over mobile-money rails and informal savings groups for VSLA/SACCO risk assessment (use cases regional bodies have asked for). Badge discipline still applies: mobile-money checkout for our digital products is fieldable; broader agentic finance workflows over those rails remain piloted or conceptual until a documented deployment exists.',
      },
      { kind: 'h', text: 'No rip-and-replace: seams, pilots, and debt honesty' },
      {
        kind: 'p',
        text: 'Technology debt is the reservation that kills good AI programmes in institutions that cannot afford a greenfield. The engineering answer is integration seams and a 90-day pilot pattern: thin, reversible connectors to existing systems, one workflow in scope, measured cost and benefit, and a decision gate to continue, adjust, or stop. We hold ourselves to the same rule: our own engineering debt is tracked in a ledger and reviewed, because transparency about what you are choosing not to fix is part of trust. The point is not to sell a forever platform. The point is to let an institution learn on a boundary it can defend to a board.',
      },
      { kind: 'h', text: 'The SME anchor: J&S StopOver Bar' },
      {
        kind: 'p',
        text: 'Architecture arguments are cheap until they touch a counter. J&S StopOver Bar is a real, non-tech SME already running agentic decision support for pricing through an LLM-council methodology, with a documented story arc from human business through finance, inventory, procurement, and operations agents to a CEO dashboard. It matters to the offline-first thesis for a blunt reason: if the only proof lives inside a company with an engineering department, the region\'s risk officers are right to be skeptical. A small business in Lilongwe is the proof that the stack is not reserved for hyperscaler customers.',
      },
      { kind: 'h', text: 'A 90-day pilot, in one page' },
      {
        kind: 'ul',
        items: [
          'Scope one workflow that already hurts: inventory, reconciliation, citizen query, or field reporting.',
          'Deploy with sovereignty constraints explicit: where models run, where data rests, what may cross a border.',
          'Route for the real link: local or free models when bandwidth is thin; cloud tiers when it is not.',
          'Gate every consequential action; measure approvals, timeouts, and escalations as first-class metrics.',
          'At day 90: continue, adjust, or stop, with the audit trail as the board pack, not a marketing appendix.',
        ],
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'Offline-first routing, provider-agnostic LLM clients (including Ollama and llama.cpp), and sovereign deployment patterns are proven in-house on LightSpeed\'s own platform. WhatsApp-native and mobile-money-aware product surfaces are fieldable or in pilot as tagged on the site. J&S StopOver Bar is a real SME running agentic pricing support; it is not a paid LightSpeed client delivery. No ministerial or bank production deployment of this full stack is claimed. Class-level architecture claims above describe capabilities and design decisions we run and publish; they do not assert a finished client product where none has been delivered. Nothing in this article should be read as a paid engagement reference.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'Offline-first means the system is allowed to work when the network is bad or absent, with model routing preferring free or local paths rather than failing into a spinner, and the router\'s tier order (fast, standard, premium, with special free and override lanes) exists so cost and connectivity are routing inputs, not afterthoughts.',
          'Sovereign-by-default: processing happens where the data lives, audit trails stay local, and any cross-border flow to an external LLM is an explicit, documented governance decision rather than a silent side effect, with a zero-cloud option for institutions that cannot risk external inference at all.',
          'Mobile-money rails (Airtel Money and TNM Mpamba) are built in from day one for local collectability, since agentic AI that cannot touch how value actually moves in Malawi is a science project, and the phone already is the bank.',
        ],
      },
    ],
    relatedSolutions: ['enterprise-deployment', 'business-automation', 'digital-presence'],
    relatedSectors: ['agriculture', 'financial-services', 'healthcare', 'government'],
  },
  {
    slug: 'evidence-ladder-honest-claims',
    title: 'The Evidence Ladder: How Every Public Claim Gets a Class, and What Buyers Should Demand',
    topic: 'EVIDENCE & PROOF',
    dek: 'Architecture never earns a risk officer\'s "yes" on its own. Claims do the rest of the work, which is why every claim we publish is classified, sourced, and occasionally cut.',
    category: 'Operating models',
    readMins: 7,
    publishedAt: '2026-10-12',
    seo: {
      title: 'The Evidence Ladder | How Every Claim Gets a Class',
      description:
        'Every public claim gets a class and a source, and occasionally gets cut. What the ledger killed, and what buyers should demand of any AI vendor.',
    },
    source:
      'research/site-claims-ledger.md · research/site-claims-audit.md · research/site-claims-index.yaml · src/data/registries/claims-registry.json · src/data/governance.ts · src/data/sectors.ts · src/data/insights.ts · docs/Pharos/pillars/03-agentic-ai-resource-constrained-africa.md · docs/Pharos/manifesto-draft.md',
    blocks: [
      {
        kind: 'p',
        text: 'Every AI vendor deck contains the same slide: a wall of logos, a throughput number with no unit, a customer quote nobody can call. The slide exists because claims are cheap and verification is expensive. In markets where buyers have been burned (and AI skepticism across African enterprises and ministries was, in our own research, earned by years of slide-deck AI that never changed an operating metric), that slide is not persuasion. It is a liability. This article is about the operating model we built to stop ourselves from writing it: an evidence ladder, a claims registry, and a public ledger that classifies every claim on our own website before it ships.',
      },
      { kind: 'h', text: 'The principle, stated once' },
      {
        kind: 'p',
        text: 'The thesis we publish and practice is uncomfortable for a growth-stage company: architecture never earns a Chief Risk Officer\'s or a minister\'s "yes" on its own. The architecture gets you into the room. The claims (what you say the architecture has done, is doing, and will do) decide whether anyone believes you. So the claims get the same engineering discipline as the code. We use an evidence ladder, applied strictly: Proposed, Verified, Established, Market-leading. A claim advances a rung only where evidence exists. Most of what any honest operator has lives in the first two rungs. The top rung is where almost nothing should sit without independent market data. Nothing we publish sits at a rung its evidence does not support.',
      },
      {
        kind: 'quote',
        text: 'An evidence ladder (Proposed, Verified, Established, Market-leading) used strictly: claims advance only where evidence exists, which is the only durable answer to skepticism.',
        cite: 'LightSpeed public doctrine · src/data/insights.ts',
      },
      { kind: 'h', text: 'Three machines under the ladder' },
      {
        kind: 'p',
        text: 'A ladder without machinery is a slogan. Ours runs on three artifacts that exist in the repository, not in a brand guide.',
      },
      {
        kind: 'p',
        text: 'First, a claims registry. Every public claim is classified before it can appear anywhere on the site: Verified, Proven in-house, Pilot, Demonstration, Fieldable, Future, Historical, or Unverified. That last one is labeled "do not publish," and the registry says so in its own description. "Proven in-house" means the claim is verified running inside LightSpeed\'s own operations: our 90-agent company is the reference deployment, and we say that rather than implying a client win we do not have. "Future" means a roadmap target with no evidence yet, stated honestly.',
      },
      {
        kind: 'p',
        text: 'Second, a claims ledger. Before any public surface ships, claims are read against the repository (the actual source files, the actual artifacts) and assigned a class: (a) fully evidenced, (b) qualified (labeled, hedged, or internally consistent), or (c) unqualified (no provenance, or contradicted). Class (c) does not ship. The ledger we last reconciled books 67 classified claims: 18 fully evidenced, 26 qualified, 23 previously flagged and resolved by fixing the copy, and zero remaining contradictions. Every one of the 18 legacy unqualified claims was remediated (hedged, labeled, or deleted) rather than quietly defended.',
      },
      {
        kind: 'p',
        text: 'Third, sector evidence tiers on the public site itself. Every sector we claim experience in carries one of four badges: Proven Experience, Current Capability, Demonstration, or Future Opportunity. The legend for the last one is a sentence we would want every vendor forced to print: roadmap target, no evidence yet, and we say so. A governance rule in code backs this: claims in evidence-sensitive categories cannot reach a published state without an evidence field attached, and the check surfaces violations rather than trusting the author\'s memory.',
      },
      { kind: 'h', text: 'What the ladder actually cut' },
      {
        kind: 'p',
        text: 'The test of an evidence system is not what it lets through. It is what it kills. A sample of our own cuts, all traceable in the public ledger:',
      },
      {
        kind: 'ul',
        items: [
          'An unverifiable superlative: "the world\'s smallest AI-native bar," removed from three surfaces after the audit found zero sizing artifacts behind it. The SME story survived; the boast did not.',
          'Fabricated-looking performance numbers on marketing surfaces deleted rather than defended, because no measured run backed them.',
          'A submission claim that said a governance standard had been "submitted to member-state ministers" downgraded to "authored as a policy proposal" because the repo held the proposal and not the submission.',
          'A "published" badge on a national AI strategy consultation response re-badged to "prepared for drafting for submission" when the artifact on disk still said DRAFT.',
          'An absolute quality claim: "every decision auditable," softened to "decision logs auditable on request," because the audit-trail design exists but the absolute did not.',
          'A throughput claim stated as measured reality rewritten as design intent: "designed for 10x to 100x," and a simulated product console explicitly labeled "SIMULATED OUTPUT: NOT A LIVE RUN" so the demo could not be mistaken for telemetry.',
        ],
      },
      {
        kind: 'p',
        text: 'None of these cuts required a crisis. They required a ledger, a class system, and the standing rule that copy loses arguments with evidence. That is the whole operating model. The alternative (shipping the claim and hoping no one asks) is the slide-deck economy this industry is trying to grow out of.',
      },
      { kind: 'h', text: 'What buyers should demand from any AI vendor' },
      {
        kind: 'p',
        text: 'If you are a bank, a ministry, or a cooperative evaluating AI claims this year, you do not need to adopt our registry to use its logic. Four demands separate evidence-led vendors from story-led ones:',
      },
      {
        kind: 'ul',
        items: [
          'Ask every claim for its class and its source. Verified against what? Proven where? If the answer is a case study you cannot inspect, the claim is unqualified by definition.',
          'Treat superlatives as a red flag, not a highlight. "First," "only," "fastest," "world\'s": each one is a data obligation. Vendors who cannot discharge it will soften when pressed. Vendors who refuse to soften are telling you how they will handle the next unverifiable claim.',
          'Demand rung-discipline on timelines. A pilot is not a deployment. A demonstration is not proven experience. A roadmap item is not a capability. Vendors who blur those boundaries in the pitch will blur them in the delivery report.',
          'Check whether the honesty badge survives contact with sales. The badge that says "no paid clients yet" should still be legible on the website after the first serious conversation. If it disappears under commercial pressure, you have learned something about the vendor that no reference call would have told you.',
        ],
      },
      { kind: 'h', text: 'Why this is the durable answer to skepticism' },
      {
        kind: 'p',
        text: 'The four reservations we hear from African risk officers and ministers (bandwidth, data protection, technology debt, and AI skepticism) are not answered by louder claims. They are answered by inspectable ones. A regulator cannot test a value statement; they can test a tier table, an audit log, and a claims ledger that says, in public, which numbers are measured and which are targets. Running this discipline on ourselves is not modesty. It is the only sales architecture that survives a technical due diligence, and it is why the operating evidence of a 90-agent company, classified rung by rung, is worth more to a CRO than any logo wall we could have built instead.',
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'LightSpeed runs this model on ourselves. The claims registry, the ledger, and the sector evidence tiers are in the repository; the last full reconciliation booked 67 claims with zero unqualified rows remaining, and the remediation trail is public in our own research files rather than performed behind a rebrand. What the ladder has not yet earned us is a client claim: no paid enterprise deployment has been delivered this stack, and every public surface says so. What it has earned is the right to be inspected, which for a buyer who has sat through one too many logo walls is the only claim that should matter. SADC region claims follow the same evidence ladder framework, with sector badges ensuring claims in sensitive categories are classified before publication.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'An evidence ladder (Proposed, Verified, Established, Market-leading) classes every claim where evidence exists, with most honest operators having claims only in the first two rungs and the top rung requiring independent market data.',
          'Most honest operators have claims only in the first two rungs; the top rung is where almost nothing should sit without independent market data, and a projection is not proof of anything the operator has done.',
          'Claims advance only where evidence supports them, which is the only durable answer to skepticism, and the alternative of shipping the claim and hoping no one asks is the slide-deck economy this industry is trying to grow out of.',
        ],
      },
    ],
    relatedSolutions: ['boardroom-briefing', 'digital-presence', 'ai-company-builder'],
    relatedSectors: ['financial-services', 'government', 'healthcare'],
  },
  {
    slug: 'sadc-ai-opportunity',
    title: 'The SADC AI Opportunity',
    topic: 'AI IN AFRICA',
    dek: 'Southern Africa is writing its AI rules in public, and the institutions that build accountability into their architecture first will set the terms for everyone else.',
    category: 'SADC technology',
    readMins: 7,
    publishedAt: '2026-09-30',
    seo: {
      title: 'The SADC AI Opportunity | LightSpeed',
      description:
        'Southern Africa is writing its AI rules in public. Why accountability-first architecture will set the terms for everyone else.',
    },
    source:
      'docs/Pharos/policy-drafts/sadc-agentic-ai-governance-framework.md · pillars/03-agentic-ai-resource-constrained-africa.md · research/site-claims-ledger.md',
    blocks: [
      {
        kind: 'p',
        text: 'The SADC region is drafting its AI governance in public. Malawi’s UNESCO Regional AI Readiness Assessment Methodology landed in July 2026; a draft national AI Bill is expected by December 2026; the African Union Continental AI Strategy now sits alongside national consultations, including the SADC member-state dialogue held in Harare in August 2026. For banks, ministries and universities in the region, the question has stopped being whether AI will be regulated, and started being which architecture the regulation will assume.',
      },
      { kind: 'h', text: 'A framework built on four principles' },
      {
        kind: 'p',
        text: 'The SADC Agentic AI Governance Framework, a policy proposal authored by LightSpeed’s CEO and targeted at member-state digital ministers, telecom regulators (MACRA, CRASA), central banks and regional development banks, argues for four principles:',
      },
      {
        kind: 'ul',
        items: [
          'Agency Control: humans retain meaningful, revocable control over what agentic systems do.',
          'Agency Sovereignty: data and decision authority stay within the jurisdiction that carries the risk.',
          'Financial Safety: agentic systems touching payment rails (RTGS, SWIFT, Airtel Money, TNM Mpamba) operate inside graduated autonomy tiers, never outside them.',
          'Traceability: every action an agent takes is attributable, logged and reviewable.',
        ],
      },
      { kind: 'h', text: 'Graduated autonomy, not all-or-nothing' },
      {
        kind: 'p',
        text: 'The proposal defines a four-tier graduated-autonomy model for public-sector adoption: from fully supervised operation to cleared, auditable autonomy as evidence accumulates. LightSpeed runs a five-tier human-approval matrix in-house: from automatic action up to CEO sign-off, with expiry sweeps so a stale approval can never block a queue forever. Governance that scales with risk is not a brake on adoption; it is the precondition that lets adoption happen at all.',
      },
      { kind: 'h', text: 'What the opportunity demands of builders' },
      {
        kind: 'ul',
        items: [
          'Sovereignty by default: data stays in-country; a zero-cloud deployment option exists for institutions that cannot risk leakage.',
          'Offline-first design: low-bandwidth and intermittent-connectivity realities are the starting point, not an afterthought.',
          'Mobile-money rails: Airtel Money and TNM Mpamba checkout built in from day one, not bolted on.',
          'Cost that scales with use: dual-economy pricing so institutions pay for what they run, not for idle hyperscaler capacity.',
        ],
      },
      {
        kind: 'quote',
        text: 'We build AI-native companies.',
        cite: 'LightSpeed Holdings north star',
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'The framework is a policy proposal, not an adopted standard, and LightSpeed’s engagement status in the region is advisory and pilot work, not deployed client systems. Nothing has been delivered to paying clients yet. What exists is the operating evidence: a governed 90-agent company running daily, and the proof pages to check it against.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'SADC regional AI governance is a policy proposal, not yet an adopted standard, with Malawi’s UNESCO Regional AI Readiness Assessment Methodology landing in July 2026 and a draft national AI Bill expected by December 2026, while the African Union Continental AI Strategy sits alongside national consultations including the SADC member-state dialogue held in Harare in August 2026.',
          'Malawi’s National AI Strategy is under drafting with UNDP and Digital Malawi Acceleration Project support, so the consultation window is open and practical implementation stories have room to be defined rather than policy adopter press releases.',
          'Sovereignty by default and offline-first design are core architecture principles for the region, with data staying in-country, a zero-cloud deployment option for institutions that cannot risk leakage, and low-bandwidth realities the starting point rather than an afterthought.',
        ],
      },
    ],
    relatedSolutions: ['boardroom-briefing', 'ai-company-builder', 'enterprise-deployment'],
    relatedSectors: ['government', 'financial-services'],
  },
  {
    slug: 'agentic-ai-african-governments',
    title: 'What Agentic AI Means for African Governments',
    topic: 'AGENTIC AI',
    dek: 'Bandwidth, data protection, technology debt and AI skepticism: the four reservations are real. The engineering answers are already concrete.',
    category: 'Agentic AI',
    readMins: 8,
    publishedAt: '2026-09-27',
    seo: {
      title: 'What Agentic AI Means for African Governments | LightSpeed',
      description:
        'Bandwidth, data protection, technology debt and AI skepticism are real. The engineering answers are already concrete.',
    },
    source:
      'docs/Pharos/pillars/03-agentic-ai-resource-constrained-africa.md · pillars/01-built-a-90-agent-company.md · company-registry.yaml (91 agents / 20 departments)',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      {
        kind: 'p',
        text: 'An agentic system is not a chatbot with an API budget. It is software whose agents perform meaningful, coordinated work under human accountability: they own defined tasks, coordinate through a shared queue, are measured like staff, and act only inside permission boundaries humans set and can revoke. For African governments, that distinction matters, because the difference between a pilot that survives contact with a ministry and one that does not is governance, not model quality.',
      },
      { kind: 'h', text: 'The four reservations governments actually raise' },
      {
        kind: 'ul',
        items: [
          'Bandwidth and resource constraints: inference and orchestration cannot assume fibre and idle GPUs.',
          'Data protection: citizen and financial data cannot leave the jurisdiction, and the Malawi Data Protection Act 2024 already binds it.',
          'Technology debt: ministries run legacy cores; nothing may require a rip-and-replace.',
          'AI skepticism: scepticism earned by years of slide-deck AI that never changed an operating metric.',
        ],
      },
      { kind: 'h', text: 'Engineering answers, not marketing answers' },
      {
        kind: 'p',
        text: 'Each reservation maps to a design decision rather than a disclaimer. Offline-first and sovereign-by-default deployment so the system runs inside the ministry’s own network, with a zero-cloud option where policy demands it. Integration seams and a 90-day co-built pilot instead of a rip-and-replace programme, so legacy cores keep running while one workflow moves. And an evidence ladder (Proposed, Verified, Established, Market-leading) used strictly: claims advance only where evidence exists, which is the only durable answer to skepticism.',
      },
      { kind: 'h', text: 'Governance that scales with risk' },
      {
        kind: 'ul',
        items: [
          'Friction scales with risk: a public-facing reply and an RTGS payment should never clear through the same gate.',
          'Auditability by default: every agent action lands in a SHA-256-sealed, append-only log.',
          'Timeout never final: an approval that expires is re-queued, not silently passed.',
          'Human accountability stays legible: one human CEO remains answerable for what the agents do.',
        ],
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'LightSpeed runs this model in-house: 91 agents (90 AI plus one human CEO) across 20 departments, coordinated through a message-bus queue under a five-tier approval matrix. On the public-sector side, the engagement is policy-level: advisory work on Malawi’s National AI Strategy consultation, with a submission prepared for the record. No ministerial production deployment is claimed. The systems are the evidence; the badges say which stage each one is at.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          '91 agents (90 AI plus one human CEO) across 20 departments coordinated through a message-bus queue under a five-tier approval matrix, with Tier 0 auto-approve for read-only work, Tier 1 notify for low-risk writes, Tier 2 single approver for code edits, Tier 3 two-person rule for production paths, and Tier 4 CEO only for secrets and financial exposure, with governance that scales with risk as discussed in the SADC region framework.',
          'Public-sector engagement is policy-level advisory work on Malawi’s National AI Strategy consultation, with a submission prepared for the record, and no ministerial production deployment is claimed, making the systems the evidence and the badges the indicator of which stage each one is at, with SADC member-state dialogue in Harare (August 2026) informing the policy landscape.',
          'Systems are the evidence; the badges say which stage each one is at, with proven in-house for architecture and governance posture, fieldable for mobile-money-aware surfaces, and piloted or conceptual for broader agentic finance workflows over mobile-money rails, with the SADC Agentic AI Governance Framework as a policy proposal not yet an adopted standard.',
        ],
      },
    ],
    relatedSolutions: ['ai-company-builder', 'boardroom-briefing', 'enterprise-deployment'],
    relatedSectors: ['government', 'financial-services', 'education'],
  },
  {
    slug: 'digital-to-ai-native-transformation',
    title: 'From Digital Transformation to AI-Native Transformation',
    topic: 'DIGITAL TRANSFORMATION',
    dek: 'Most organisations adopt AI the way they adopted email: they buy tools, hand them to people, and hope for a transformation. Here is the test that separates tool use from an operating model.',
    category: 'Digital transformation',
    readMins: 7,
    publishedAt: '2026-09-24',
    seo: {
      title: 'From Digital Transformation to AI-Native | LightSpeed',
      description:
        'Most organisations adopt AI the way they adopted email. The test that separates tool use from an operating model.',
    },
    source:
      'docs/Pharos/linkedin-series/post-01 (draft-v1, feed-v1) · pillars/01-built-a-90-agent-company.md · docs/client-facing/USE-CASE-CATALOG.md',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      {
        kind: 'quote',
        text: '“We use AI” hides three different realities: tool users, pasting prompts into chat windows where nothing is measured or compounded; process automation, where scripts speed known tasks but throughput stays bounded by headcount; and AI-native: agents as first-class participants in the operating model …',
        cite: 'Pharos: AI-Native Organizations (post 01)',
      },
      { kind: 'h', text: 'Three levels of adoption' },
      {
        kind: 'ul',
        items: [
          'Tool users: individuals paste prompts into chat windows. Nothing is measured, nothing compounds, throughput still moves with headcount and mood.',
          'Process automation: scripts speed up known tasks. Useful, but bounded: the organisation is still the machine.',
          'AI-native: agents own defined tasks, coordinate through a shared queue, are measured like staff, and act inside permission boundaries humans set and can revoke.',
        ],
      },
      { kind: 'h', text: 'The test that separates them' },
      {
        kind: 'p',
        text: 'The test is not “do people use AI.” The test is whether the organisation’s operating structure changes when the agents change. Remove an agent from the registry and owned work leaves the system: the queue, the metrics and the department scorecard all reflect it within a reporting window. Assisted humans are still the whole workflow. An AI-native structure is engineered, not equipped.',
      },
      { kind: 'h', text: 'What LightSpeed runs' },
      {
        kind: 'p',
        text: 'LightSpeed Holdings is an AI-native company builder headquartered in Lilongwe. The company operates the system it sells: 91 agents (90 AI plus one human CEO) across 20 departments, coordinated through a message-bus task queue, governed by a five-tier approval matrix and SHA-256-sealed audit trails. Digital transformation digitised the paperwork; AI-native changes who does the work, and who is answerable for it.',
      },
      { kind: 'h', text: 'Starting where you are' },
      {
        kind: 'p',
        text: 'For a bank, a university or a cooperative, the path is the same one LightSpeed walked: pick one workflow, put it behind a real approval gate, measure it against the old way, then widen. A real, non-tech SME in Malawi (J&S StopOver Bar) runs agentic decision support on inventory, sales velocity and cash reconciliation, built in-house and documented openly: proof that AI-native operations work in the informal economy, not just in a demo. Client engagements have not yet been delivered; the proof is in-house first, and the site says so at every badge. Malawi context shows this is particularly relevant where connectivity costs 8.45% of GNI per capita.',
      },
      { kind: 'h', text: 'Key Takeaway' },
      {
        kind: 'ul',
        items: [
          'AI-native changes who does the work and who is answerable for it in the operating model, where removing an agent from the registry and owned work leaves the system: the queue, the metrics and the department scorecard all reflect it within a reporting window, and assisted humans are still the whole workflow, with SADC region insight that AI-native operations in informal economies require context-aware governance.',
          'J&S StopOver Bar proof that AI-native operations work in the informal economy, not just in a demo, with inventory, sales velocity and cash reconciliation agents running on a small business\'s actual numbers, built in-house and documented openly, and operating in markets where mobile-money rails are the default collectability mechanism.',
          'Client engagements not yet delivered; proof is in-house first, and the site states so at every badge, with client-facing badges saying the same thing: proven in-house first, fieldable and piloted where true, never claimed delivered when it is not, and Malawi context reinforces the importance of in-house proof for regions with constrained connectivity.',
        ],
      },
    ],
    relatedSolutions: ['ai-company-builder', 'business-automation', 'digital-presence'],
    relatedSectors: ['financial-services', 'education', 'agriculture'],
  },
];

export function getInsightArticle(slug: string): InsightArticle | undefined {
  return insightArticles.find((a) => a.slug === slug);
}

export const insightSlugs: string[] = insightArticles.map((a) => a.slug);

export function formatInsightDate(iso: string): string {
  return new Date(`${iso}T00:00:00`).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}
