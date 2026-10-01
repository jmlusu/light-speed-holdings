/* LightSpeed Holdings — Insights article data (CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §16).
   Data module instead of MDX: no new toolchain needed (YAGNI — decision recorded
   when the Wayfinder map closes). Every claim is grounded in first-party repo
   sources declared per article (`source`). No invented numbers, no unproven
   superlatives — see research/site-claims-ledger.md. */

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
  blocks: InsightBlock[];
  relatedSolutions: string[]; // solution slugs (siteContent.ts `solutions`)
  relatedSectors: string[]; // canonical 5 sector slugs (sector-registry.ts)
}

export const insightArticles: InsightArticle[] = [
  {
    slug: 'sadc-ai-opportunity',
    title: 'The SADC AI Opportunity',
    topic: 'AI IN AFRICA',
    dek: 'Southern Africa is writing its AI rules in public — and the institutions that build accountability into their architecture first will set the terms for everyone else.',
    category: 'SADC technology',
    readMins: 7,
    publishedAt: '2026-09-30',
    source:
      'docs/Pharos/policy-drafts/sadc-agentic-ai-governance-framework.md · pillars/03-agentic-ai-resource-constrained-africa.md · research/site-claims-ledger.md',
    blocks: [
      {
        kind: 'p',
        text: 'The SADC region is drafting its AI governance in public. Malawi’s UNESCO Regional AI Readiness Assessment Methodology landed in July 2026; a draft national AI Bill is expected by December 2026; the African Union Continental AI Strategy now sits alongside national consultations — including the SADC member-state dialogue held in Harare in August 2026. For banks, ministries and universities in the region, the question has stopped being whether AI will be regulated, and started being which architecture the regulation will assume.',
      },
      { kind: 'h', text: 'A framework built on four principles' },
      {
        kind: 'p',
        text: 'The SADC Agentic AI Governance Framework — a policy proposal authored by LightSpeed’s CEO and targeted at member-state digital ministers, telecom regulators (MACRA, CRASA), central banks and regional development banks — argues for four principles:',
      },
      {
        kind: 'ul',
        items: [
          'Agency Control — humans retain meaningful, revocable control over what agentic systems do.',
          'Agency Sovereignty — data and decision authority stay within the jurisdiction that carries the risk.',
          'Financial Safety — agentic systems touching payment rails (RTGS, SWIFT, Airtel Money, TNM Mpamba) operate inside graduated autonomy tiers, never outside them.',
          'Traceability — every action an agent takes is attributable, logged and reviewable.',
        ],
      },
      { kind: 'h', text: 'Graduated autonomy, not all-or-nothing' },
      {
        kind: 'p',
        text: 'The proposal defines a four-tier graduated-autonomy model for public-sector adoption: from fully supervised operation to cleared, auditable autonomy as evidence accumulates. LightSpeed runs a five-tier human-approval matrix in-house — from automatic action up to CEO sign-off, with expiry sweeps so a stale approval can never block a queue forever. Governance that scales with risk is not a brake on adoption; it is the precondition that lets adoption happen at all.',
      },
      { kind: 'h', text: 'What the opportunity demands of builders' },
      {
        kind: 'ul',
        items: [
          'Sovereignty by default — data stays in-country; a zero-cloud deployment option exists for institutions that cannot risk leakage.',
          'Offline-first design — low-bandwidth and intermittent-connectivity realities are the starting point, not an afterthought.',
          'Mobile-money rails — Airtel Money and TNM Mpamba checkout built in from day one, not bolted on.',
          'Cost that scales with use — dual-economy pricing so institutions pay for what they run, not for idle hyperscaler capacity.',
        ],
      },
      {
        kind: 'quote',
        text: 'Malawi first. Prove it. Then the world.',
        cite: 'LightSpeed Holdings north star',
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'The framework is a policy proposal, not an adopted standard — and LightSpeed’s engagement status in the region is advisory and pilot work, not deployed client systems. Nothing has been delivered to paying clients yet. What exists is the operating evidence: a governed 90-agent company running daily, and the proof pages to check it against.',
      },
    ],
    relatedSolutions: ['boardroom-briefing', 'ai-company-builder', 'enterprise-deployment'],
    relatedSectors: ['government', 'financial-services'],
  },
  {
    slug: 'agentic-ai-african-governments',
    title: 'What Agentic AI Means for African Governments',
    topic: 'AGENTIC AI',
    dek: 'Bandwidth, data protection, technology debt and AI skepticism — the four reservations are real. The engineering answers are already concrete.',
    category: 'Agentic AI',
    readMins: 8,
    publishedAt: '2026-09-27',
    source:
      'docs/Pharos/pillars/03-agentic-ai-resource-constrained-africa.md · pillars/01-built-a-90-agent-company.md · company-registry.yaml (90 agents / 20 departments)',
    blocks: [
      {
        kind: 'p',
        text: 'An agentic system is not a chatbot with an API budget. It is software whose agents perform meaningful, coordinated work under human accountability: they own defined tasks, coordinate through a shared queue, are measured like staff, and act only inside permission boundaries humans set and can revoke. For African governments, that distinction matters — because the difference between a pilot that survives contact with a ministry and one that does not is governance, not model quality.',
      },
      { kind: 'h', text: 'The four reservations governments actually raise' },
      {
        kind: 'ul',
        items: [
          'Bandwidth and resource constraints — inference and orchestration cannot assume fibre and idle GPUs.',
          'Data protection — citizen and financial data cannot leave the jurisdiction, and the Malawi Data Protection Act 2024 already binds it.',
          'Technology debt — ministries run legacy cores; nothing may require a rip-and-replace.',
          'AI skepticism — scepticism earned by years of slide-deck AI that never changed an operating metric.',
        ],
      },
      { kind: 'h', text: 'Engineering answers, not marketing answers' },
      {
        kind: 'p',
        text: 'Each reservation maps to a design decision rather than a disclaimer. Offline-first and sovereign-by-default deployment so the system runs inside the ministry’s own network, with a zero-cloud option where policy demands it. Integration seams and a 90-day co-built pilot instead of a rip-and-replace programme, so legacy cores keep running while one workflow moves. And an evidence ladder — Proposed, Verified, Established, Market-leading — used strictly: claims advance only where evidence exists, which is the only durable answer to skepticism.',
      },
      { kind: 'h', text: 'Governance that scales with risk' },
      {
        kind: 'ul',
        items: [
          'Friction scales with risk — a public-facing reply and an RTGS payment should never clear through the same gate.',
          'Auditability by default — every agent action lands in a SHA-256-sealed, append-only log.',
          'Timeout never final — an approval that expires is re-queued, not silently passed.',
          'Human accountability stays legible — one human CEO remains answerable for what the agents do.',
        ],
      },
      { kind: 'h', text: 'Honest status' },
      {
        kind: 'p',
        text: 'LightSpeed runs this model in-house: 90 agents (89 AI plus one human CEO) across 20 departments, coordinated through a message-bus queue under a five-tier approval matrix. On the public-sector side, the engagement is policy-level — advisory work on Malawi’s National AI Strategy consultation, with a submission prepared for the record. No ministerial production deployment is claimed. The systems are the evidence; the badges say which stage each one is at.',
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
    source:
      'docs/Pharos/linkedin-series/post-01 (draft-v1, feed-v1) · pillars/01-built-a-90-agent-company.md · docs/client-facing/USE-CASE-CATALOG.md',
    blocks: [
      {
        kind: 'quote',
        text: '“We use AI” hides three different realities: tool users, pasting prompts into chat windows where nothing is measured or compounded; process automation, where scripts speed known tasks but throughput stays bounded by headcount; and AI-native — agents as first-class participants in the operating model …',
        cite: 'Pharos — AI-Native Organizations (post 01)',
      },
      { kind: 'h', text: 'Three levels of adoption' },
      {
        kind: 'ul',
        items: [
          'Tool users — individuals paste prompts into chat windows. Nothing is measured, nothing compounds, throughput still moves with headcount and mood.',
          'Process automation — scripts speed up known tasks. Useful, but bounded: the organisation is still the machine.',
          'AI-native — agents own defined tasks, coordinate through a shared queue, are measured like staff, and act inside permission boundaries humans set and can revoke.',
        ],
      },
      { kind: 'h', text: 'The test that separates them' },
      {
        kind: 'p',
        text: 'The test is not “do people use AI.” The test is whether the organisation’s operating structure changes when the agents change. Remove an agent from the registry and owned work leaves the system: the queue, the metrics and the department scorecard all reflect it within a reporting window. Assisted humans are still the whole workflow — an AI-native structure is engineered, not equipped.',
      },
      { kind: 'h', text: 'What LightSpeed runs' },
      {
        kind: 'p',
        text: 'LightSpeed Holdings is an AI-native company builder headquartered in Lilongwe. The company operates the system it sells: 90 agents (89 AI plus one human CEO) across 20 departments, coordinated through a message-bus task queue, governed by a five-tier approval matrix and SHA-256-sealed audit trails. Digital transformation digitised the paperwork; AI-native changes who does the work — and who is answerable for it.',
      },
      { kind: 'h', text: 'Starting where you are' },
      {
        kind: 'p',
        text: 'For a bank, a university or a cooperative, the path is the same one LightSpeed walked: pick one workflow, put it behind a real approval gate, measure it against the old way, then widen. A real, non-tech SME in Malawi — J&S StopOver Bar — runs agentic decision support on inventory, sales velocity and cash reconciliation, built in-house and documented openly: proof that AI-native operations work in the informal economy, not just in a demo. Client engagements have not yet been delivered; the proof is in-house first, and the site says so at every badge.',
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
