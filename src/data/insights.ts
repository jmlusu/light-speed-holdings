/* LightSpeed Holdings - Insights article data (CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §16).
   Data module instead of MDX: no new toolchain needed (YAGNI - decision recorded
   when the Wayfinder map closes). Every claim is grounded in first-party repo
   sources declared per article (`source`). No invented numbers, no unproven
   superlatives - see research/site-claims-ledger.md. */

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
    title: 'Cutting AI Costs With Open Source: Why Architecture Matters More Than Arithmetic',
    topic: 'COST ARCHITECTURE',
    dek: 'You save the most when you avoid unnecessary model calls. A quota-first router, local inference, and measured cost controls determine your actual savings.',
    category: 'AI governance',
    readMins: 8,
    publishedAt: '2026-10-21',
    seo: {
      title: 'Cutting AI Costs With Open Source | LightSpeed',
      description:
        'You save the most when you avoid unnecessary model calls. A quota-first router, local inference, and measured cost controls determine actual AI savings.',
    },
    source:
      'src/ai_company/llm/model_router.py, src/ai_company/llm/client.py, harness/research/2026-10-21-open-source-ecosystem-analysis.md.',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      { kind: 'h', text: 'The 80% discount claim' },
      {
        kind: 'p',
        text: 'AI strategy presentations often promise an 80% lower model bill after a switch to open source. Production workloads rarely support that simple comparison.',
      },
      {
        kind: 'p',
        text: 'In our own operational logs, 2.1 million routed calls showed a 50 to 65% reduction in total cost of ownership over 90 days. Workload shape explains the range. Classification, extraction, and short drafts landed near 65%. Long-context synthesis, multi-document reasoning, and code generation across large repositories landed near 50%. Routing architecture produced the savings; changing models alone did not.',
      },
      { kind: 'h', text: 'Where the 80% figure comes from' },
      {
        kind: 'p',
        text: "The 80% calculation compares a premium API's per-token rate with a self-hosted open-weight model's marginal inference cost. It leaves out five costs:",
      },
      {
        kind: 'ul',
        items: [
          'Capability fit loss: A local model may solve 70% of tasks at low marginal cost, but you still pay a premium model for the other 30%.',
          'Routing and evaluation overhead: You must build, maintain, and run the logic that selects a sufficient model for each call.',
          'Integration and observability: Self-hosted models still need logging, tracing, rate limits, and failure handling.',
          'Quality regression risk: Include the downstream cost of wrong answers. A cheap error can cost more than an expensive correct result.',
          'Hardware or hosting cost: A Mac Studio running Ollama has capital and electricity costs. A managed open-weight endpoint still charges per token.',
        ],
      },
      { kind: 'h', text: 'The architecture behind the reported 50 to 65% reduction' },
      {
        kind: 'p',
        text: 'First, use a quota-first router. Our `select_model(tier, prefer_free, offline_aware)` logic selects fast, standard, or premium tiers. It checks `ModelTier.FREE/OVERRIDE`, `used/limit/resets_at`, and offline-aware local-first routing. The client supports OpenAI-compatible endpoints, Ollama, and llama.cpp.',
      },
      {
        kind: 'p',
        text: 'Second, make offline operation a normal mode. Keep the registry, audit records, and configuration on-premises. Use local inference when needed, then sync when connectivity returns.',
      },
      {
        kind: 'p',
        text: 'Third, keep cost ledgers per agent and workflow. Record prompt, completion, and total tokens, estimated cost, and attribution by agent, department, workflow, and project.',
      },
      { kind: 'h', text: 'The limitation' },
      {
        kind: 'p',
        text: 'Keep a premium tier for frontier reasoning, very long-context synthesis, and specialized coding tasks that justify it. Use premium models when the task requires them, rather than by default. The reported 50 to 65% range depends on routing discipline. If every call drifts to the most capable model, you lose the savings and still carry the router\'s overhead.',
      },
      { kind: 'h', text: 'What to measure before claiming savings' },
      {
        kind: 'ul',
        items: [
          'Total cost of ownership, including routing, hosting, integration, and error handling.',
          'At least 90 days of operational data.',
          'Workload mix by task type.',
          'Quality regression rate against your existing baseline.',
          'Cost per successful outcome, not cost per call alone.',
        ],
      },
      {
        kind: 'p',
        text: 'We can defend the 50 to 65% range in our own recorded workload. The 80% claim leaves out costs you still have to pay.',
      },
    ],
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'business-automation'],
    relatedSectors: ['agriculture', 'financial-services', 'government'],
  },
  {
    slug: 'dual-economy-ai-pricing',
    title: 'Pricing Agentic AI in a Dual Economy: Kwacha Ladders, Dollar Retainers, and Paying for What You Run',
    topic: 'AI PRICING',
    dek: 'Fixed bundles can hide your actual running costs. In Malawi, pricing must account for Kwacha payments, Dollar retainers, and the model costs underneath both.',
    category: 'Operating models',
    readMins: 7,
    publishedAt: '2026-10-21',
    seo: {
      title: 'Pricing Agentic AI in a Dual Economy | LightSpeed',
      description:
        'Fixed bundles can hide actual running costs. In Malawi, AI pricing must account for Kwacha payments, Dollar retainers, and the model costs underneath both.',
    },
    source:
      'docs-site/src/content/docs/commercial/pricing.mdx, docs/COMMERCIAL_PRICING.md, src/ai_company/llm/cost_tracker.py.',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      { kind: 'h', text: 'The fixed-retainer problem' },
      {
        kind: 'p',
        text: 'A fixed retainer gives you a predictable invoice, but it can hide how much work the system actually performs. Ask what compute, model calls, support, and integrations the price covers.',
      },
      { kind: 'h', text: 'The dual-economy reality' },
      {
        kind: 'p',
        text: 'Local clients pay in MWK through Airtel Money, TNM Mpamba, or bank transfer. International engagements use USD, generally net-15 with 50% upfront. Your unit economics must cover both payment contexts. Our recorded open-model savings range is 50 to 65%, depending on workload; do not treat it as a fixed discount.',
      },
      { kind: 'h', text: 'Four commercial motions, one cost ledger' },
      {
        kind: 'ul',
        items: [
          'Digital Presence: MWK 950,000.',
          'Business Automation: MWK 1,800,000 to 3,500,000.',
          'Enterprise Deployment: MWK 6,500,000+ per month.',
          'AI Company Builder licence: USD 12,000 to 18,000 per year.',
        ],
      },
      {
        kind: 'p',
        text: 'These figures are custom-quoted and non-binding. Confirm scope, currency, billing period, and running-cost allowances in writing before you commit.',
      },
      { kind: 'h', text: 'What a cost ledger gives you' },
      {
        kind: 'p',
        text: 'Token telemetry and attribution by agent, department, workflow, and project show your pricing floor, expose cost spikes, and support a margin discussion based on actual usage.',
      },
      {
        kind: 'p',
        text: 'Price against the work you run. Respect local currency constraints and show the unit economics behind the quote.',
      },
    ],
    relatedSolutions: ['business-automation', 'digital-presence', 'boardroom-briefing'],
    relatedSectors: ['financial-services', 'agriculture', 'government'],
  },
  {
    slug: 'five-tier-approval-matrix',
    title: 'The Five-Tier Approval Matrix: How Approval Friction Scales With Risk in a 90-Agent Company',
    topic: 'AI GOVERNANCE',
    dek: 'Match approval effort to the cost of a wrong action. Routine work should move quickly; consequential work needs explicit authorization.',
    category: 'AI governance',
    readMins: 8,
    publishedAt: '2026-10-21',
    seo: {
      title: 'The Five-Tier Approval Matrix for Agent Governance | LightSpeed',
      description:
        'Match approval effort to the cost of a wrong action. Routine work should move quickly; consequential agent work needs explicit human authorization.',
    },
    source:
      'src/ai_company/orchestrator/approval.py, src/ai_company/governance/.',
    correction: { date: '2026-10-25', text: 'Correction (2026-10-25): the canonical operating model is 90 roles: 89 AI agents plus 1 Human CEO. Earlier wording in this article counted 91 agents by treating the Human CEO as an AI agent. The body is left unchanged for the audit trail.' },
    blocks: [
      { kind: 'h', text: 'Why a generic human review step is insufficient' },
      {
        kind: 'p',
        text: 'A single review rule treats a formatting task and a production-data deletion alike. Define who approves each action, what evidence they need, and when approval expires.',
      },
      { kind: 'h', text: 'Five tiers, one invariant' },
      {
        kind: 'ul',
        items: [
          'T0 AUTO_APPROVE (Negligible; reversible): Format an internal note; run a read-only status check. Automatic execution with an audit log.',
          'T1 SUPERVISED (Low; reversible with effort): Draft an external email from an approved template. Notification and time-boxed review.',
          'T2 HUMAN_REVIEW (Moderate; external or customer-visible): Publish a report to a client workspace. Explicit human review.',
          'T3 HUMAN_APPROVE (High; financial, legal, or security impact): Change a production permission; send a contract. Named approver and recorded rationale.',
          'T4 CEO_ONLY (Critical; irreversible or existential): Delete production data; alter governance policy. Human CEO only.',
        ],
      },
      {
        kind: 'p',
        text: 'The invariant is simple: higher consequence requires stronger authorization.',
      },
      {
        kind: 'p',
        text: 'The implementation also covers tier classification, same-approval checks, expiry sweeps, four pre-execution gates (Contract, DPA, Compliance, Security), SHA-256 sealed append-only audit records, and override controls.',
      },
      { kind: 'h', text: 'Honest boundary' },
      {
        kind: 'p',
        text: 'This architecture runs in-house. It is fieldable, but it has not been validated by years of client incident data.',
      },
    ],
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
    relatedSectors: ['financial-services', 'government'],
  },
  {
    slug: 'inside-a-90-agent-company',
    title: 'Inside a 90-Agent Company: What the Registry, the Queue, and the Approval Gate Actually Do',
    topic: 'AI COMPANY BUILDING',
    dek: 'The 90-role system consists of a registry, a queue, an approval gate, and a human who can stop execution.',
    category: 'AI Company Building',
    readMins: 9,
    publishedAt: '2026-10-21',
    seo: {
      title: 'Inside a 90-Agent Company | LightSpeed',
      description:
        'The 90-role system consists of a registry, a queue, an approval gate, and a human who can stop execution. A look inside the LightSpeed operating model.',
    },
    source:
      'company-registry.yaml, src/ai_company/orchestrator/message_bus.py, src/ai_company/orchestrator/approval.py.',
    correction: { date: '2026-10-22', text: 'Correction (2026-10-22): Jessica, Chen, Grace, David, Marcus, Aisha, and Samuel are role-level examples from a 90-role demo manifest. They are not canonical shipped registry identities. `company-registry.yaml` declares the live agent set: 20 departments and 90 operating roles, including 89 AI agents and the Human CEO, plus one additional human-gated role. The counts and role shapes are accurate; do not read the individual names as deployed staff.' },
    blocks: [
      { kind: 'h', text: 'A registry, not a prompt' },
      {
        kind: 'p',
        text: 'The canonical `company-registry.yaml` defines 20 departments and 90 operating roles. Each role has a scope, allowed tools, and an escalation path.',
      },
      {
        kind: 'p',
        text: 'The article uses Maya, Jessica, Chen, Grace, David, Marcus, Aisha, and Samuel as demo examples across T0 to T4. These names illustrate role behavior; they do not identify deployed staff.',
      },
      { kind: 'h', text: 'The queue' },
      {
        kind: 'p',
        text: 'The MessageBus uses `.opencode/inbox.json`. Its task shape includes `id`, `to`, `from`, `task`, `status`, and `created_at`.',
      },
      { kind: 'h', text: 'The approval gate and human override' },
      {
        kind: 'p',
        text: 'The approval gate checks each action\'s tier before execution. The human CEO retains override authority.',
      },
      { kind: 'h', text: 'Honest boundary' },
      {
        kind: 'p',
        text: 'We orchestrate this system in-house. It is fieldable, but we do not claim uniform deployment at client scale.',
      },
    ],
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
    relatedSectors: ['financial-services', 'government', 'education'],
  },
  {
    slug: 'offline-first-ai-for-africa',
    title: 'Offline-First AI for Africa: Designing for Bandwidth, Sovereignty, and Mobile-Money Reality',
    topic: 'AI IN AFRICA',
    dek: 'Many AI designs assume reliable fibre and card payments. African deployments often need intermittent-connectivity support, mobile money, and jurisdiction-specific data controls.',
    category: 'Operating models',
    readMins: 7,
    publishedAt: '2026-10-21',
    seo: {
      title: 'Offline-First AI for Africa | LightSpeed',
      description:
        'African AI deployments often need intermittent-connectivity support, mobile money, and jurisdiction-specific data controls, not fibre-and-card assumptions.',
    },
    source:
      'src/ai_company/llm/model_router.py, src/ai_company/llm/client.py, docs-site/src/content/docs/commercial/pricing.mdx, MISSION_AND_VISION.md.',
    blocks: [
      { kind: 'h', text: 'Three assumptions that fail' },
      {
        kind: 'p',
        text: 'Do not assume continuous connectivity, card-based payment, or unrestricted cross-border data movement.',
      },
      { kind: 'h', text: 'What offline-first means in the stack' },
      {
        kind: 'p',
        text: 'Use quota-first, offline-aware routing. Keep execution provider-agnostic through OpenAI-compatible endpoints, Ollama, and llama.cpp. Support PWA offline action queues and WhatsApp-native flows.',
      },
      {
        kind: 'quote',
        text: 'Low bandwidth does not mean you cannot use AI. Design the system for the bandwidth you actually have.',
      },
      { kind: 'h', text: 'Data sovereignty as a routing decision' },
      {
        kind: 'p',
        text: 'Enforce residency in the execution path. Use a Zero-Cloud Boundary where required, keep processing in-region, and pin workloads to the approved jurisdiction.',
      },
      { kind: 'h', text: 'Mobile money as a primary payment method' },
      {
        kind: 'p',
        text: 'Support Airtel Money, TNM Mpamba, and PayChangu. Handle MWK and USD. Custom-scoped USD work generally uses 50% upfront and net-15 terms.',
      },
      { kind: 'h', text: 'Evidence boundary' },
      {
        kind: 'p',
        text: 'The router and client run in-house. Offline-first workflows are fieldable in 2026. Some integrations depend on the deployment or pilot.',
      },
    ],
    relatedSolutions: ['enterprise-deployment', 'business-automation', 'digital-presence'],
    relatedSectors: ['agriculture', 'financial-services', 'healthcare', 'government'],
  },
  {
    slug: 'evidence-ladder-honest-claims',
    title: 'The Evidence Ladder: How We Classify Public Claims and What You Should Ask Any Vendor',
    topic: 'EVIDENCE & PROOF',
    dek: 'Ask for the evidence class, artifact, date, and boundary behind each claim. A label without supporting evidence does not help your evaluation.',
    category: 'AI governance',
    readMins: 6,
    publishedAt: '2026-10-21',
    seo: {
      title: 'The Evidence Ladder: Honest Claims for AI Vendors | LightSpeed',
      description:
        'Ask for the evidence class, artifact, date, and boundary behind each AI claim. A label without supporting evidence does not help your evaluation.',
    },
    source:
      'research/site-claims-ledger.md, src/data/siteContent.ts.',
    blocks: [
      { kind: 'h', text: 'Four classes' },
      {
        kind: 'ul',
        items: [
          'Proven in-house: Runs in LightSpeed operations. We can show an artifact, test, or ledger.',
          'In pilot: Runs in a real external deployment with a bounded scope and named constraints. Client naming requires opt-in.',
          'Fieldable in 2026: The architecture exists, is packaged, and can be tested, but lacks extensive production validation at scale.',
          'In development: Designed or partially built and on the roadmap. Do not depend on it today.',
        ],
      },
      { kind: 'h', text: 'What this means when you read our site' },
      {
        kind: 'p',
        text: 'Read the class beside each claim. An internal result does not prove the same result in your environment. A fieldable capability still needs deployment testing.',
      },
      { kind: 'h', text: 'What to ask any AI vendor' },
      {
        kind: 'p',
        text: 'Ask for five things: the claim\'s class, the supporting artifact, the observation date, the operating boundary, and a clear statement of what the vendor does not claim.',
      },
    ],
    relatedSolutions: ['boardroom-briefing', 'digital-presence', 'ai-company-builder'],
    relatedSectors: ['financial-services', 'government', 'healthcare'],
  },
  {
    slug: 'sadc-ai-opportunity',
    title: 'The AI Opportunity in SADC: Why Regional Intelligence Infrastructure Matters',
    topic: 'AI IN AFRICA',
    dek: 'SADC\'s digital economy is growing. Regional AI infrastructure can give organisations more control over data, cost, and deployment than imported SaaS alone.',
    category: 'AI policy',
    readMins: 6,
    publishedAt: '2026-10-15',
    seo: {
      title: 'The AI Opportunity in SADC | LightSpeed',
      description:
        'SADC\'s digital economy is growing. Regional AI infrastructure can give organisations more control over data, cost, and deployment than imported SaaS alone.',
    },
    source:
      'MISSION_AND_VISION.md, docs-site/src/content/docs/commercial/pricing.mdx.',
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
      { kind: 'h', text: 'Key takeaway' },
      {
        kind: 'ul',
        items: [
          'SADC Agentic AI Governance Framework is a policy proposal, not an adopted standard - advisory engagement with member states',
          'Four principles anchor the framework: Agency Control, Agency Sovereignty, Financial Safety, and Traceability',
          'Builders should design for sovereignty by default, offline-first, mobile-money rails, and cost scaling with use from day one',
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
    dek: 'Agent systems can reduce work in reporting, procurement, and citizen services. Test whether the governance controls work as well as the demo.',
    category: 'AI governance',
    readMins: 7,
    publishedAt: '2026-10-10',
    seo: {
      title: 'What Agentic AI Means for African Governments | LightSpeed',
      description:
        'Agent systems can reduce work in reporting, procurement, and citizen services. Test whether the governance controls work as well as the demo.',
    },
    source:
      'src/ai_company/orchestrator/approval.py, MISSION_AND_VISION.md.',
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
      { kind: 'h', text: 'Key takeaway' },
      {
        kind: 'ul',
        items: [
          'Bandwidth and data protection are engineering constraints: offline-first and sovereign-by-default deployment for ministerial networks',
          'Technology debt means integration seams and 90-day pilots, not rip-and-replace - legacy cores keep running while one workflow moves',
          'AI skepticism is answered by evidence: the evidence ladder (Proposed, Verified, Established, Market-leading) strictly governs all claims',
        ],
      },
    ],
    relatedSolutions: ['ai-company-builder', 'boardroom-briefing', 'enterprise-deployment'],
    relatedSectors: ['government', 'financial-services', 'education'],
  },
  {
    slug: 'digital-to-ai-native-transformation',
    title: 'Moving Beyond Digital Transformation to AI-Native Operations',
    topic: 'DIGITAL TRANSFORMATION',
    dek: 'Digital transformation moved workflows onto screens. AI-native operations add governed agents inside those workflows. The change affects architecture and decision rights.',
    category: 'Digital transformation',
    readMins: 6,
    publishedAt: '2026-10-05',
    seo: {
      title: 'Moving Beyond Digital Transformation to AI-Native Operations | LightSpeed',
      description:
        'Digital transformation moved workflows onto screens. AI-native operations add governed agents inside those workflows. The change affects architecture and decision rights.',
    },
    source:
      'MISSION_AND_VISION.md, company-registry.yaml.',
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
        text: 'For a bank, a university or a cooperative, the path is the same one LightSpeed walked: pick one workflow, put it behind a real approval gate, measure it against the old way, then widen. A real, non-tech SME in Malawi (J&S StopOver Bar) runs agentic decision support on inventory, sales velocity and cash reconciliation, built in-house and documented openly: proof that AI-native operations work in the informal economy, not just in a demo. Client engagements have not yet been delivered; the proof is in-house first, and the site says so at every badge.',
      },
      { kind: 'h', text: 'Key takeaway' },
      {
        kind: 'ul',
        items: [
          'Tool users paste prompts with no measurement or compounding: throughput still moves with headcount and mood',
          'AI-native: agents own defined tasks, coordinate through a shared queue, are measured like staff, and act inside human-set permission boundaries',
          'The differentiating test: does the operating structure change when agents change? Remove an agent and owned work leaves the system',
        ],
      },
    ],
    relatedSolutions: ['ai-company-builder', 'business-automation', 'digital-presence'],
    relatedSectors: ['financial-services', 'education', 'agriculture'],
  },
  {
    slug: 'why-we-built-90-agents',
    title: 'Why We Built 90 Agents Instead of One Assistant',
    topic: 'AI COMPANY BUILDING',
    dek: 'One assistant can accumulate broad permissions and many failure modes. Separate roles limit what each agent can do and make its output easier to audit.',
    category: 'AI Company Building',
    readMins: 5,
    publishedAt: '2026-10-01',
    seo: {
      title: 'Why We Built 90 Agents Instead of One Assistant | LightSpeed',
      description:
        'One assistant can accumulate broad permissions and many failure modes. Separate roles limit what each agent can do and make its output easier to audit.',
    },
    source:
      'company-registry.yaml, src/ai_company/orchestrator/approval.py.',
    blocks: [
      { kind: 'h', text: 'The monolith problem' },
      {
        kind: 'p',
        text: 'A single assistant with broad access can exceed its intended scope without a clear boundary check.',
      },
      { kind: 'h', text: 'Specialisation as a safety property' },
      {
        kind: 'p',
        text: 'Give each agent a name, declared tools, an escalation path, and auditable output.',
      },
      { kind: 'h', text: 'The overhead is real' },
      {
        kind: 'p',
        text: 'You must maintain the registry, routing, approvals, and audit records. Separate agents add coordination work; use them where the control benefits justify it.',
      },
      {
        kind: 'p',
        text: 'We arrived at 90 roles by separating responsibilities and approval boundaries. The count itself is not the design goal.',
      },
    ],
    relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
    relatedSectors: ['financial-services', 'government', 'education'],
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
