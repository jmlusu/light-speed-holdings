import type { InsightArticle } from '../../src/data/insights';

export const article: InsightArticle = {
  slug: 'open-source-cost-architecture',
  title: 'Cutting AI Costs With Open Source: Why the Architecture Matters More Than the Arithmetic',
  topic: 'COST ARCHITECTURE',
  dek: 'In Malawi the binding constraint is not token prices. It is connectivity that costs 8.45% of GNI per capita. The open-source cost argument is architectural, not arithmetic: route to local models, rent open-weight APIs where competition has capped the price, and spend the difference on what actually binds.',
  category: 'African AI',
  readMins: 8,
  publishedAt: '2026-10-12',
  source:
    'docs/Pharos/research-briefs/2026-10-12-open-source-costs.md · docs/Pharos/research-briefs/2026-10-12-africa-open-source-ecosystem.md · pyproject.toml · package-lock.json · src/ai_company/llm/providers/ · src/ai_company/llm/cost_tracker.py · src/ai_company/llm/client.py · docs/adr/004-multi-provider-llm.md · docs/ARCHITECTURE_REMOTE_RUNTIME.md · docs/Pharos/case-study-pipeline.md',
  blocks: [
    {
      kind: 'p',
      text: 'Every argument about the cost of AI in Africa starts in the wrong place: token prices. A hyperscaler publishes a price list, someone divides it by the exchange rate, and the conversation ends in a spreadsheet. It should not end there. In Malawi the binding constraint is not what a million tokens cost. It is what connectivity costs. The ITU\'s data-only mobile broadband basket for Malawi sits at 8.45% of GNI per capita (2025 data, read through a secondary mirror of the dataset), and a 4GB mobile bundle runs about 6,000 kwacha, roughly 12% of the minimum monthly wage, on April 2024 figures with FX conversions approximate. Under that arithmetic, every megabyte an agent does not push over the network is a real cost, not an optimization. This article argues from architecture and external price evidence, and says plainly which savings we have not measured.',
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
      text: 'All 90 agents in our company, 89 AI plus one human CEO, are runnable locally on Ollama/llama.cpp, per our remote-runtime architecture documentation. Open source is our cost architecture, not a licensing shortcut. The machinery of the company (orchestration, approvals, audit, dashboard) does not require a single paid runtime dependency to operate.',
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
  ],
  relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'business-automation'],
  relatedSectors: ['agriculture', 'financial-services', 'government'],
};
