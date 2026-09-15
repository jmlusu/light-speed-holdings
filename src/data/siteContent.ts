/* LightSpeed Holdings client-site content model.
   Source of truth: MISSION_AND_VISION (v2.0, Sep 2026) + use-case messaging
   brief (Sep 2026) + verified platform facts from company-registry/tests.
   Every claim here carries its honesty status. No invented numbers. */

export type HonestyTone = 'proven' | 'pilot' | 'fieldable' | 'development';

export interface HonestyLabel {
  label: string;
  tone: HonestyTone;
}

export const TONE_STYLES: Record<HonestyTone, string> = {
  proven: 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
  pilot: 'border-ls-red/40 bg-ls-red/10 text-ls-red',
  fieldable: 'border-amber-400/40 bg-amber-400/10 text-amber-300',
  development: 'border-slate-400/40 bg-slate-400/10 text-slate-400',
};

/* ── Company identity ─────────────────────────────────────── */
export const company = {
  legalName: 'LightSpeed Holdings Limited',
  firstMention: 'LightSpeed Holdings Limited™',
  shortName: 'LightSpeed Holdings',
  location: 'Lilongwe, Malawi',
  tagline: 'ASPIRE. ACT. ACHIEVE.',
  northStar: 'Malawi first. Prove it. Then the world.',
  heroHeadline: 'Build the intelligent enterprise.',
  heroSubline:
    'LightSpeed Holdings helps organisations design, build and govern AI-native businesses, intelligent workflows and agentic systems — in Malawi, across SADC, and beyond.',
  valueCycle: ['Strategy', 'Build', 'Govern', 'Scale'] as const,
};

/* ── Mission & Vision (MISSION_AND_VISION v2.0) ───────────── */
export const mission: { statement: string; why: string } = {
  statement:
    'Prove agentic AI works in Malawi by shipping real services — websites, automation, reporting, and marketing — for the organizations that need them most.',
  why: 'Malawi\u2019s SMEs, NGOs, schools, clinics, and cooperatives are underserved by an industry that prices enterprise-grade work out of reach. One human CEO directs a workforce of 140+ AI agents to deliver world-class output at local cost. Our proof is not a press release; it is a shipped website, a donor report that used to take weeks, a dashboard that replaced forty-page PDFs.',
};

export const vision: { statement: string; why: string } = {
  statement:
    'Every organization — from Malawian clinics to global enterprises — operating with intelligent AI agents.',
  why: 'Intelligent automation is not a privilege of rich countries. We win trust with real engagements, published case studies, and compliant, secure delivery. We prove it in Malawi first — where the constraints are real — then serve organizations everywhere that need AI at fair cost.',
};

/* ── Core values ──────────────────────────────────────────── */
export interface Value {
  num: number;
  title: string;
  sentence: string;
  showsUp: string;
}

export const values: Value[] = [
  {
    num: 1,
    title: 'Innovation Through Iteration',
    sentence: 'We ship fast, learn faster. Perfection is the enemy of progress; rigorous iteration is the path to breakthrough outcomes.',
    showsUp: 'We deploy weekly, measure outcomes, and treat informative failures — in the market as much as in code — as data.',
  },
  {
    num: 2,
    title: 'Transparency in All Operations',
    sentence: 'We operate with radical openness — internally with our teams and externally with our customers. Trust is built through honesty, not spin.',
    showsUp: 'Published case studies with named metrics. Open unit economics. We say what a deliverable costs to produce, not just what we charge.',
  },
  {
    num: 3,
    title: 'Security by Design',
    sentence: 'Security is not a feature — it is a foundation. Every system, agent, and API is designed assuming adversaries.',
    showsUp: 'Malawi Data Protection Act 2017, GDPR-level rigour for donor data, threat-modelling before building, Bandit + pre-commit hooks, least-privilege agent permissions.',
  },
  {
    num: 4,
    title: 'Customer-First Mindset',
    sentence: 'Our success is measured entirely by the success of our customers.',
    showsUp: 'MWK quotes for local businesses, USD for international partners, delivery to clients, and support staffed with people who solve problems.',
  },
  {
    num: 5,
    title: 'Automate Repetitive Work',
    sentence: 'If a machine can do a task reliably and repeatedly, we automate it — and redeploy the human to judgment, creativity, and empathy.',
    showsUp: 'Our own delivery pipeline runs on our orchestration engine. We measure hours reclaimed and reinvest them in client work.',
  },
  {
    num: 6,
    title: 'Excellence Without Ego',
    sentence: 'We hold ourselves to the highest standards and welcome scrutiny. The best idea wins regardless of seniority.',
    showsUp: 'Rigorous, respectful reviews; post-mortems focused on systems, not blame; respect as the recruiting pitch as we hire our first Malawian team members.',
  },
  {
    num: 7,
    title: 'Security, Reliability, Trust',
    sentence: 'Our customers depend on us for mission-critical operations. Downtime and data loss are not options.',
    showsUp: 'We target 99.99% platform uptime, run DR drills, and test failure modes. NGO contracts are not the place for \u201cit usually works.\u201d',
  },
  {
    num: 8,
    title: 'Local by Default',
    sentence: 'Priced in the local currency, paid through the rails Malawians already use — Airtel Money, TNM Mpamba, PayChangu.',
    showsUp: 'MWK pricing floors for local SMEs. Community embeddedness over imported polish. We are not a foreign outfit parachuting in.',
  },
];

/* ── Strategic pillars ────────────────────────────────────── */
export interface StrategicPillar {
  num: number;
  title: string;
  body: string;
  metric: string;
}

export const pillars: StrategicPillar[] = [
  {
    num: 1,
    title: 'Product & Platform Excellence',
    body: 'Make the agent platform the product, not just the delivery mechanism. Low-bandwidth, mobile-first engineering, idempotent and tested generations, and Offer E platform licensing as the bridge from services to product.',
    metric: 'Offer E licenses closed + client report card of quality failures',
  },
  {
    num: 2,
    title: 'Market Proof (Malawi First)',
    body: 'Prove the model with delivered, referenceable work — not claims. Five offers as one proof engine, lighthouse clients as living proof, and delivery discipline: ≤10-day turnaround, ≥4.5/5 satisfaction, 30 days support included.',
    metric: '20–25 paid clients and 8 lighthouse clients in the first 12 months',
  },
  {
    num: 3,
    title: 'Trust, Security & Local Compliance',
    body: 'Enterprise-grade rigour at MWK pricing — trust is the only moat we can buy. Data Protection Act 2017 compliance as default posture, GDPR-level handling for donor and UN data flows, hardened mobile-money rails.',
    metric: 'Zero critical security breaches; compliance checklist 100% complete',
  },
  {
    num: 4,
    title: 'Talent & Ecosystem',
    body: 'Growth means building local talent and global capability: the Lightspeed Academy, first local hires on a named timeline, and university partnerships that make Malawians want to build here.',
    metric: 'Local talent hired or trained; Academy cohorts graduated',
  },
  {
    num: 5,
    title: 'Thought Leadership & Policy',
    body: 'Make Malawi a source of agentic-AI answers, not just a market. Pharos positions the Human CEO as the leading voice on Agentic AI Company Building, Use Cases, and Policy across Malawi and SADC.',
    metric: 'Published research monographs + speaking engagements per quarter',
  },
];

/* ── Financial guardrails (select client-relevant facts) ──── */
export const financialGuardrails: { title: string; detail: string }[] = [
  {
    title: 'MWK pricing floor',
    detail: 'MWK 150,000 (~$85) on every local deliverable; anything cheaper needs CFO sign-off.',
  },
  {
    title: 'Dual-currency rails',
    detail: 'Local SMEs pay in MWK via Airtel Money, TNM Mpamba, or bank transfer. NGO and international clients pay in USD, net-15 with 50% upfront.',
  },
  {
    title: 'No donor subsidy',
    detail: 'NGO work is quoted at full commercial rates. Grants may fund Academy or community programs — never delivery subsidies that mask unit economics.',
  },
  {
    title: 'LLM + infra discipline',
    detail: 'LLM and infrastructure spend is tracked monthly, held to ≤10% of revenue.',
  },
];

/* ── Commitments ──────────────────────────────────────────── */
export interface CommitmentGroup {
  audience: string;
  items: string[];
}

export const commitments: CommitmentGroup[] = [
  {
    audience: 'Malawi & Our Clients',
    items: [
      'We will prove, not promise. Every claim in our marketing traces to a delivered, named engagement — starting in Malawi.',
      'We meet our clients where they are — content, interfaces, and support adapt to the context of every engagement.',
      'We will pay our way and build local talent — local hires, Academy graduates, a Majority-Malawian delivery team as we grow.',
      'We will respect Malawi\u2019s data and dignity — Data Protection Act 2017 compliance is not negotiable.',
    ],
  },
  {
    audience: 'SMEs, NGOs, Government & Cooperatives',
    items: [
      'We build what you need, not what we think you should want. Your feedback drives the roadmap.',
      'We will protect your data as if it were our own.',
      'We will deliver quickly — weeks, not quarters — and stand behind it with 30 days of support.',
      'We will never lock you in. Your site, your data, your dashboards are yours.',
      'We will be transparent when things go wrong — the moment they go wrong.',
    ],
  },
  {
    audience: 'Our Team',
    items: [
      'Clarity: you will always know what the company is trying to achieve and what \u201cgood\u201d looks like.',
      'Growth: a real development plan, Academy seats, and work that makes a visible difference at home.',
      'Psychological safety: challenge any idea, question any decision, raise any concern without retribution.',
      'Fair compensation benchmarked to Malawian and regional market reality.',
    ],
  },
  {
    audience: 'Partners & Investors',
    items: [
      'We communicate honestly — good news and bad news travel at the same speed.',
      'We deploy capital efficiently — every dollar is measured against the Malawi proof thesis.',
      'We build for the long term — the SADC AI-services category, not an exit.',
      'We return value through durable growth, not through vendor lock-in or subsidy accounting.',
    ],
  },
];

/* ── Solutions (6 domains, 5 with detail pages) ───────────── */
export interface SolutionCta {
  label: string;
  to: string;
}

export interface SolutionUseCase {
  title: string;
  lead: string;
  proof: HonestyLabel;
}

export interface SolutionRecord {
  slug: string;
  nav: string;
  eyebrow: string;
  title: string;
  oneLiner: string;
  lead: string;
  proof: HonestyLabel;
  capabilities: { title: string; desc: string }[];
  useCases: SolutionUseCase[];
  cta: SolutionCta;
}

export const solutions: SolutionRecord[] = [
  {
    slug: 'agentic-ai',
    nav: 'Agentic AI',
    eyebrow: 'SOLUTION // AGENTIC AI',
    title: 'Agentic AI',
    oneLiner:
      'We design intelligent systems capable of executing work — AI agents, multi-agent systems, and agentic workflows — governed by human approval at every step.',
    lead:
      'Not chatbots. Intelligent systems that take a brief, work across tools, and return auditable output. LightSpeed designs and operates AI agents, multi-agent architectures, and agentic workflows for organisations that need work done — with a 5-tier human-in-the-loop approval matrix and immutable audit trails on every action.',
    proof: { label: 'Proven in-house — our own 144-agent operation runs on this platform daily', tone: 'proven' },
    capabilities: [
      { title: 'AI Agents', desc: 'Specialist agents for compliance scanning, data pipelines, contract review, reporting, and customer success — configured per role.' },
      { title: 'Multi-Agent Systems', desc: 'Coordinated agent teams across departments, with escalation paths, RACI matrices, and role-scoped permissions.' },
      { title: 'Agentic Workflows', desc: 'End-to-end work loops that accept briefs, execute against tools, and hand off to humans at approval gates.' },
      { title: 'AI Operating Models', desc: 'The operating model behind your agents: who approves, what is audited, how risk is classified before work starts.' },
      { title: 'Enterprise AI', desc: 'Agent deployments inside existing organisational structures — adapted to your registry, not the other way around.' },
      { title: 'AI Company Builder', desc: 'License the same orchestration engine we run: your own governed AI workforce, self-hosted and provider-agnostic.' },
    ],
    useCases: [
      {
        title: 'Startup Acceleration',
        lead: 'A solo founder operates with the functional coverage of a multi-person team — agents handle finance, legal, marketing, sales; the founder sets vision.',
        proof: { label: 'Proven in-house', tone: 'proven' },
      },
      {
        title: 'Enterprise Automation',
        lead: 'Existing teams gain specialist agents for compliance, contracts, and data pipelines — without the 6-month hiring cycle.',
        proof: { label: 'In active development', tone: 'development' },
      },
      {
        title: 'Consulting Firm Scale',
        lead: 'Agents carry research, analysis, and report generation as a delivery backbone; humans focus on client relationships.',
        proof: { label: 'In active development', tone: 'development' },
      },
      {
        title: 'E-Commerce Operations',
        lead: '24/7 customer success, sales, and marketing with customer context maintained across interactions and high-value escalations.',
        proof: { label: 'In active development', tone: 'development' },
      },
    ],
    cta: { label: 'Explore AI Company Builder', to: '/ai-company-builder' },
  },
  {
    slug: 'digital-transformation',
    nav: 'Digital Transformation',
    eyebrow: 'SOLUTION // DIGITAL TRANSFORMATION',
    title: 'Digital Transformation',
    oneLiner:
      'Strategy, architecture, and delivery that move organisations from manual processes to working digital and AI-native operations.',
    lead:
      'Every business in Malawi deserves a digital front door. LightSpeed builds mobile-first websites, e-commerce stores, brand identities, and modernised operating stacks — with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one. From MWK 150,000 (~$85) for a Google Business listing to a full online store, we design for the way Malawi actually transacts.',
    proof: { label: 'Fieldable in 2026 — pricing validated against real prospects before publishing', tone: 'fieldable' },
    capabilities: [
      { title: 'Digital Strategy', desc: 'A clear map from today\u2019s operation to a digital one, prioritised by business outcome, not technology novelty.' },
      { title: 'Enterprise Architecture', desc: 'The target architecture your transformation builds toward — systems, data, integration, and governance designed together.' },
      { title: 'Data & Analytics', desc: 'Turn operational data into decisions with dashboards and reporting your field team can use on a phone.' },
      { title: 'Cloud & Platforms', desc: 'Sovereign, in-region hosting decisions with a Zero-Cloud Boundary option for state, health, and financial data.' },
      { title: 'Technology Modernisation', desc: 'No rip-and-replace — API connectors, quiet migration, and deliverables that stay yours.' },
    ],
    useCases: [
      {
        title: 'Business Website',
        lead: 'Mobile-first site with local payment rails — from an MWK 150,000 Google Business-grade presence upward.',
        proof: { label: 'Fieldable in 2026', tone: 'fieldable' },
      },
      {
        title: 'E-Commerce / Online Store',
        lead: 'A full online store with checkout on Airtel Money, TNM Mpamba, and PayChangu — no app download required.',
        proof: { label: 'Fieldable in 2026', tone: 'fieldable' },
      },
      {
        title: 'Brand Identity',
        lead: 'Logo, visuals, and tone built from your market reality — community embeddedness over imported polish.',
        proof: { label: 'Fieldable in 2026', tone: 'fieldable' },
      },
      {
        title: 'Digital Marketing',
        lead: 'Content calendars, community management, and ad campaigns on Facebook, WhatsApp, and Google — ad spend excluded and transparent.',
        proof: { label: 'Fieldable in 2026', tone: 'fieldable' },
      },
    ],
    cta: { label: 'Start a Conversation', to: '/contact' },
  },
  {
    slug: 'data-intelligence',
    nav: 'Data & Intelligence',
    eyebrow: 'SOLUTION // DATA & INTELLIGENCE',
    title: 'Data & Intelligence',
    oneLiner:
      'Turn scattered data into decisions: architecture, engineering, business intelligence, and AI-powered decision intelligence.',
    lead:
      'NGOs and development programmes spend weeks turning Kobo and DHIS2 data into donor-ready reports. LightSpeed automates that pipeline: clean the data, generate narrative reports against donor templates, and build interactive dashboards your field team can access on a phone. All hosted in-region, all compliant with Malawi\u2019s Data Protection Act.',
    proof: { label: 'In pilot with UNDP Malawi stakeholders', tone: 'pilot' },
    capabilities: [
      { title: 'Data Architecture', desc: 'Data models and pipelines designed for low-bandwidth environments and sovereign in-region processing.' },
      { title: 'Data Engineering', desc: 'ETL, cleaning, and quality checks that turn messy field data into trustworthy datasets.' },
      { title: 'Business Intelligence', desc: 'Dashboards and reporting that replace forty-page PDFs with living, shareable surfaces.' },
      { title: 'Market Intelligence', desc: 'Competitive, pricing, and market analysis grounded in real, sourced data.' },
      { title: 'AI-Powered Decision Intelligence', desc: 'Anomaly detection and decision support on top of your data — with human sign-off on consequential calls.' },
    ],
    useCases: [
      {
        title: 'Donor / Project Reports',
        lead: 'Narrative reports generated against USAID, EU, and UN templates from Kobo/DHIS2 data — accuracy inspectors can rely on.',
        proof: { label: 'In pilot (composing evidence)', tone: 'pilot' },
      },
      {
        title: 'Interactive Dashboards',
        lead: 'Program dashboards field teams can open on a phone, with Z-score anomaly triggers and audit-ready histories.',
        proof: { label: 'In pilot', tone: 'pilot' },
      },
      {
        title: 'Data Cleaning & Analysis',
        lead: 'Reconciliation and quality pipelines that make grant data board-ready rather than spreadsheet-fragile.',
        proof: { label: 'In active development', tone: 'development' },
      },
      {
        title: 'Survey Design + Analysis',
        lead: 'Questionnaire design and analysis that pair with the reporting pipeline end-to-end.',
        proof: { label: 'In active development', tone: 'development' },
      },
    ],
    cta: { label: 'Start a Conversation', to: '/contact' },
  },
  {
    slug: 'automation',
    nav: 'Intelligent Automation',
    eyebrow: 'SOLUTION // INTELLIGENT AUTOMATION',
    title: 'Intelligent Automation',
    oneLiner:
      'Workflow automation and AI agents that absorb repetitive work so your people can do the parts that need judgment.',
    lead:
      'Your customers are already on WhatsApp. LightSpeed builds WhatsApp-native assistants that handle FAQs, take orders, process bookings, and hand off to a human when the conversation gets complex — integrated with Airtel Money and TNM Mpamba for instant mobile-money checkout. Where a process is repeatable and documented, we automate it; where it needs judgment, a human stays in the loop.',
    proof: { label: 'In pilot preparation — gated on the G1–G4 security review and liability ratification', tone: 'pilot' },
    capabilities: [
      { title: 'Workflow Automation', desc: 'Documented processes run by agents: intake, triage, follow-up, and escalation without inbox debt.' },
      { title: 'Intelligent Process Automation', desc: 'Automation that reads context and decides — with human approval tiers on consequential steps.' },
      { title: 'Business Process Design', desc: 'We map your current workflow first (interviews, not assumptions), then automate what is safe to automate.' },
      { title: 'Workflow Collapse', desc: 'Identifying processes where agents collapse a 5-step manual chain into one task with one audit record.' },
    ],
    useCases: [
      {
        title: 'WhatsApp Customer Chatbot',
        lead: 'FAQs, orders, bookings, and mobile-money checkout via WhatsApp — no app download for your customers.',
        proof: { label: 'In pilot preparation', tone: 'pilot' },
      },
      {
        title: 'AI Document / Report Generator',
        lead: 'Draft donor, compliance, and operational reports from structured data — reviewed by humans before they ship.',
        proof: { label: 'In pilot preparation', tone: 'pilot' },
      },
      {
        title: 'Form + Survey Automation',
        lead: 'Field data collection, validation, and routing that removes manual transcription.',
        proof: { label: 'In pilot preparation', tone: 'pilot' },
      },
      {
        title: 'Clinic Supply-Chain Anomaly Alerts',
        lead: 'Auto-generated procurement requests on anomaly detection (Z-score triggers), so shortages are flagged fast.',
        proof: { label: 'Use case in active development', tone: 'development' },
      },
    ],
    cta: { label: 'Start a Conversation', to: '/contact' },
  },
  {
    slug: 'strategy-advisory',
    nav: 'Strategy & Advisory',
    eyebrow: 'SOLUTION // STRATEGY & ADVISORY',
    title: 'Strategy & Advisory',
    oneLiner:
      'Executive advisory and transformation roadmaps that decide what to build — and what to retire — before any system exists.',
    lead:
      'Traditional consulting charges per-head, per-hour. LightSpeed delivers enterprise-grade output at a fraction of the cost — with full audit trails and governed delivery. We don\u2019t sell hours; we sell outcomes, backed by a 5-tier human-in-the-loop system. For boards and leadership teams, we run discovery, AI readiness assessment, and a transformation roadmap in a 90-day pilot window — no rip-and-replace.',
    proof: { label: 'Architectured and piloted in Malawi; architected for SADC', tone: 'pilot' },
    capabilities: [
      { title: 'AI Strategy', desc: 'Where AI creates leverage in your organisation — and where it should not be used at all.' },
      { title: 'Digital Strategy', desc: 'Priorities, sequencing, and funding maps for your transformation.' },
      { title: 'Technology Strategy', desc: 'The architectural decisions, integration points, and retirement list your team needs.' },
      { title: 'Executive Advisory', desc: 'Board-level counsel on AI governance, risk, and responsible deployment — evidence-led, never boastful.' },
      { title: 'Transformation Roadmaps', desc: 'A pragmatic 90-day pilot to measurable scale, with honest-status gates at every phase.' },
    ],
    useCases: [
      {
        title: 'AI Readiness Assessment',
        lead: 'A sector-aware, interactive diagnostic scoring your operating model across strategy, data, technology, people, and governance.',
        proof: { label: 'Proven in-house', tone: 'proven' },
      },
      {
        title: 'Board Discovery',
        lead: 'A governed, 5-tier-approved discovery conversation instead of a product demo.',
        proof: { label: 'Architectured and piloted in Malawi', tone: 'pilot' },
      },
      {
        title: 'Transformation Roadmap',
        lead: 'From current state to an AI-native enterprise, sequenced and costed — with no lock-in.',
        proof: { label: 'In active development', tone: 'development' },
      },
    ],
    cta: { label: 'Request an Assessment', to: '/contact' },
  },
];

export interface GovernanceSolutionRecord {
  slug: string;
  nav: string;
  to: string;
  eyebrow: string;
  title: string;
  oneLiner: string;
  lead: string;
  proof: HonestyLabel;
}

export const GOVERNANCE_SOLUTION: GovernanceSolutionRecord = {
  slug: 'ai-policy-governance',
  nav: 'AI Governance & Policy',
  to: '/technology#governance',
  eyebrow: 'SOLUTION // AI GOVERNANCE & POLICY',
  title: 'AI Governance & Policy',
  oneLiner:
    'The governance layer that makes agentic AI safe to deploy: responsible AI, risk classification, and the regional policy work shaping the rules.',
  lead:
    'LightSpeed doesn\u2019t just build agentic AI — we shape the policy that governs it. Our SADC Agentic AI Governance Framework proposes graduated autonomy, cryptographic agent identity, immutable audit trails, and in-country data sovereignty standards for Southern Africa\u2019s low-bandwidth, dual-economy reality. National AI Strategy consultation submission published; SADC framework targeted at regional ICT ministers and regulators.',
  proof: { label: 'SADC framework in active development (policy track) / National AI Strategy published', tone: 'development' },
};

/* ── Industries (5 MVP detail pages) ──────────────────────── */
export interface IndustryRecord {
  slug: string;
  nav: string;
  title: string;
  problem: string;
  opportunity: string;
  solution: string;
  proof: HonestyLabel;
  useCases: string[];
  note?: string;
}

export const industries: IndustryRecord[] = [
  {
    slug: 'government',
    nav: 'Government & Public Sector',
    title: 'Government & Public Sector',
    problem:
      'Government agencies face enormous compliance burdens with limited budgets, and no governed deployment standard exists in-region for AI.',
    opportunity:
      'Citizen-query agents, legislative summarisation, project monitoring, and compliance reporting — built for governance-first standards and auditable at every step.',
    solution:
      'Our 5-tier approval matrix aligns to government authorisation levels; every action is recorded on an immutable audit trail. Governance is mapped to Malawi\u2019s Data Protection Act and SADC\u2019s digital-transformation agenda.',
    proof: { label: 'In active development — National AI Strategy consultation submission published', tone: 'development' },
    useCases: [
      'Citizen-query agents for public service information',
      'Legislative summarisation and policy analysis',
      'Compliance monitoring and regulatory reporting',
      'Contract review and document analysis at scale',
    ],
    note: 'Governance framework mapped to Malawi DPA and SADC standards.',
  },
  {
    slug: 'development',
    nav: 'Development & Donor',
    title: 'Development & Donor Organisations',
    problem:
      'Manual M&E is slow and error-prone; donor reporting templates consume weeks; tools like Kobo and DHIS2 do not auto-generate narrative reports.',
    opportunity:
      'A reporting pipeline that moves field data to boardroom in hours, with accuracy inspectors can rely on and full in-region hosting.',
    solution:
      'Offer C — Data, Analytics & Donor Reporting: clean the data, generate narrative reports against donor templates, and deliver mobile-first dashboards. Donor and UN data flows get GDPR-level handling with documented cross-border consent waivers.',
    proof: { label: 'In pilot with UNDP Malawi stakeholders', tone: 'pilot' },
    useCases: [
      'Donor-ready quarterly and annual reports from Kobo/DHIS2 data',
      'Interactive program dashboards for field teams',
      'Anomaly-triggered procurement and supply-chain alerts',
      'Survey design and analysis for evaluations',
    ],
    note: 'Donor data cross-border consent waiver workflow in active development.',
  },
  {
    slug: 'financial-services',
    nav: 'Financial Services',
    title: 'Financial Services',
    problem:
      'Southern Africa runs a dual economy: regulated institutions and informal savings groups (VSLA/SACCO) transacting over mobile money — with reconciliation and audibility as the constant burden.',
    opportunity:
      'Agentic workflows over Airtel Money and TNM Mpamba rails: micro-loan risk assessment, automated savings tracking, reconciliation, and continuous compliance.',
    solution:
      'The 5-tier approval matrix maps directly to financial-services authorisation levels, and immutable audit trails meet regulatory documentation requirements while the production value lands over the rails Malawians already use.',
    proof: { label: 'Use case in active development — actively sought by COMESA/IDEA', tone: 'development' },
    useCases: [
      'Automated savings tracking for VSLA/SACCO groups',
      'Micro-loan risk assessment for smallholder farmers',
      'Mobile-money reconciliation and reporting',
      'Continuous compliance monitoring and audit preparation',
    ],
    note: 'No signed engagement exists; no paid client deployments to date.',
  },
  {
    slug: 'healthcare',
    nav: 'Healthcare',
    title: 'Healthcare & Public Health M&E',
    problem:
      'Clinic supply chains run on manual monitoring; procurement reacts late; donor M&E reports take weeks to produce.',
    opportunity:
      'Monitor clinic supply chains, auto-generate procurement requests on anomaly detection, and produce donor-ready M&E reports from Kobo and DHIS2 data.',
    solution:
      'A data pipeline designed to move from field collection to boardroom in hours. Healthcare administration agents handle billing compliance, scheduling, credentialing, and PII-sensitive workflows with memory encryption and Malawi DPA / GDPR compliance built in.',
    proof: { label: 'In pilot (composing evidence)', tone: 'pilot' },
    useCases: [
      'Clinic supply-chain monitoring with Z-score anomaly detection',
      'Auto-generated procurement requests on anomalies',
      'Donor-ready M&E reporting',
      'Citizen-query agents for public health information',
    ],
    note: 'No confirmed partnership with any named health organisation has been signed.',
  },
  {
    slug: 'agriculture',
    nav: 'Agriculture',
    title: 'Agriculture & Agritech',
    problem:
      'Smallholder farmers and agri-businesses operate in offline-first environments with intermittent connectivity and thin margins.',
    opportunity:
      'Weather data, soil analysis, and mobile-money micro-loan risk assessments — agentic workflows that help farmers decide better and agri-businesses manage supply chains.',
    solution:
      'Advisory modelled on existing Ulangizi-style chatbot patterns, delivered over WhatsApp offline-first, paired with supply-chain monitoring and procurement automation for agri-businesses.',
    proof: { label: 'Use case in active development — fieldable 2026', tone: 'fieldable' },
    useCases: [
      'Agentic weather + soil advisory for smallholder farmers',
      'Mobile-money micro-loan risk assessment for cooperatives',
      'Supply-chain monitoring and procurement automation',
    ],
  },
];

/* ── Technology (10 pillars) ──────────────────────────────── */
export interface TechnologyPillar {
  title: string;
  desc: string;
}

export const technologyPillars: TechnologyPillar[] = [
  { title: 'AI-Native Architecture', desc: 'Systems built as agentic operating layers from day one — not AI bolted onto legacy software.' },
  { title: 'Agent Architecture', desc: 'Role-scoped agents bound to the canonical 7-tool runtime, configured in a registry, not scattered scripts.' },
  { title: 'Semantic Fabric', desc: 'A structured, queryable layer (knowledge graph + memory) that gives agents context without transcript dumping.' },
  { title: 'Data Architecture', desc: 'Sovereign in-region processing by default, with documented cross-border flows and consent waivers.' },
  { title: 'Enterprise AI', desc: 'Agents that fit your existing org structure and governance, via YAML configuration and RACI mapping.' },
  { title: 'Integration', desc: 'API connectors into Kobo, DHIS2, mobile-money rails, CRMs, and existing stacks — no rip-and-replace.' },
  { title: 'Cloud & Infrastructure', desc: 'Sovereign hosting choices with a Zero-Cloud Boundary option for state, health, and financial data.' },
  { title: 'Security', desc: 'Least-privilege permissions, Bandit + pre-commit gates, SHA-256 audit trails, encryption and PII detection.' },
  { title: 'Governance', desc: '5-tier human approval, risk-classified agent tiers, circuit breakers, and expiry sweeps on stale approvals.' },
  { title: 'Technical Proof', desc: 'Architecture documented in the open, regenerated benchmarks, and a test suite that gates our own work.' },
];

export const technologyMetrics: { value: string; label: string; source: string }[] = [
  { value: '144', label: 'Verified Agent Configurations', source: 'company-registry.yaml' },
  { value: '2,373', label: 'Automated Regression Tests', source: 'pytest suite' },
  { value: '20', label: 'Departments Modeled', source: 'company-registry.yaml' },
  { value: '5-TIER', label: 'Human Approval Gates', source: 'ApprovalGate matrix' },
];

export const technologyMethods: { step: string; title: string; detail: string }[] = [
  { step: '01', title: 'AST-only knowledge graph', detail: 'Rebuilt post-commit by graphify. Structure only — no transcript dumping, no API cost.' },
  { step: '02', title: 'Four-gate CI on every patch', detail: 'ruff + mypy + bandit + 2,373 pytest gates must pass before a change lands.' },
  { step: '03', title: 'Per-request cost tracking', detail: 'An OpenAI-compatible usage ledger records token and spend per request.' },
  { step: '04', title: 'Human approval + expiry sweep', detail: 'HITL approval gates and ApprovalGate expiry sweeps are reported on the control plane.' },
];

/* ── AI Company Builder ───────────────────────────────────── */
export const aiCompanyBuilder = {
  concept:
    'An AI Company Builder is a governed AI workforce for your organisation: role-scoped agent teams with a human decision layer, an operating model, an architecture, and an audit trail — licensable and self-hosted.',
  ladder: {
    traditional: [
      'Human Workforce',
      'Processes',
      'Software',
      'Data',
    ],
    native: [
      'Human Leadership',
      'AI Operating Model',
      'Agent Workforce',
      'Intelligent Workflows',
      'Data + Semantic Layer',
      'Decision Intelligence',
      'Continuous Improvement',
    ],
  },
  dimensions: [
    { title: 'The Concept', desc: 'One human + a governed agent workforce = full organisational capability, measured and auditable.' },
    { title: 'AI-Native Enterprise', desc: 'An enterprise designed with automation as the default and humans on judgment.' },
    { title: 'AI Operating Model', desc: 'The decision rights, approval tiers, and escalation paths your agents operate under.' },
    { title: 'Agent Workforce', desc: 'Role-scoped agents configured in a registry, each bound to a canonical toolset and permissions.' },
    { title: 'AI Architecture', desc: 'The orchestration, memory, audit, and provider layers that make the workforce run.' },
    { title: 'AI Product Factory', desc: 'A repeatable pipeline that turns your data and processes into shipped products and reports.' },
    { title: 'Workflow Automation', desc: 'Documented processes collapsed into agent-run workflows with human sign-off.' },
    { title: 'Human + AI Operating Model', desc: 'The hybrid: agents execute, humans approve, and escalation is explicit.' },
    { title: 'Governance', desc: '5-tier approvals, immutable trails, risk-classified tiers, and circuit breakers.' },
    { title: 'Transformation Journey', desc: '90-day pilot to scale: discovery, assessment, architecture, build, govern, iterate.' },
  ],
  licensing: {
    offer: 'Offer E — AI Company Builder License',
    price: 'MWK 3,500,000 (~$2,000) one-off + $200/month support',
    details: [
      'The same orchestration engine that runs LightSpeed Holdings, licensed to run on your infrastructure.',
      'Self-hosted, provider-agnostic, and extensible.',
      'White-label agent teams for agencies and their clients.',
      'One-on-one onboarding included.',
    ],
  },
};

/* ── The 8 platform deployment scenarios ──────────────────── */
export interface Scenario {
  id: string;
  title: string;
  desc: string;
  status: string;
}

export const scenarios: Scenario[] = [
  {
    id: 'FOW-01',
    title: 'Startup Acceleration (Solo Founder + AI)',
    desc: 'A solo founder operates with the functional coverage of a multi-person team: agents handle CTO, CFO, CMO, and CLO roles, with a CEO dashboard for real-time visibility.',
    status: 'Proven in-house — LightSpeed itself operates as a 1-human, 144-agent organisation.',
  },
  {
    id: 'FOW-02',
    title: 'Enterprise Automation (Augment Existing Teams)',
    desc: 'Existing teams gain specialist AI agents for compliance scanning, data pipelines, and contract review — without the 6-month hiring cycle.',
    status: 'In active development — designed for SADC regulatory environments.',
  },
  {
    id: 'FOW-03',
    title: 'Consulting Firm Scale (Delivery Backbone)',
    desc: 'Agents handle research, analysis, and report generation; humans focus on client relationships.',
    status: 'In active development — validated in LightSpeed\u2019s own consulting operations.',
  },
  {
    id: 'FOW-04',
    title: 'Non-Profit Operations (Full Capability, Minimal Staff)',
    desc: 'Coverage across finance, HR, compliance, M&E, and donor communications — with the audit trail grantmakers require.',
    status: 'In active development — supports free local models (Ollama).',
  },
  {
    id: 'FOW-05',
    title: 'Government Compliance (Authorisation-Aligned)',
    desc: 'Compliance monitoring, contract review, and regulatory reporting with the 5-tier approval matrix aligned to government authorisation levels.',
    status: 'In active development — mapped to Malawi DPA and SADC standards.',
  },
  {
    id: 'FOW-06',
    title: 'E-Commerce (24/7 Customer Success)',
    desc: 'Customer success, sales pipeline, and marketing analytics without shift-based teams, WhatsApp-native and mobile-first.',
    status: 'In active development.',
  },
  {
    id: 'FOW-07',
    title: 'Healthcare Administration',
    desc: 'Billing compliance, scheduling, credentialing, and regulatory reporting with memory encryption and PII detection.',
    status: 'In active development — designed for Malawi DPA and GDPR compliance.',
  },
  {
    id: 'FOW-08',
    title: 'Financial Services (Risk & Compliance)',
    desc: 'Continuous compliance monitoring, risk analysis, and audit preparation with the audit trail meeting regulatory documentation requirements.',
    status: 'In active development.',
  },
];

/* ── Work / Proof ─────────────────────────────────────────── */
export interface WorkCard {
  id: string;
  title: string;
  badge: string;
  text: string;
  featured?: boolean;
}

export const workCaseStudies: WorkCard[] = [
  {
    id: 'PC-01',
    title: 'J&S StopOver Bar — SME AI Transformation',
    badge: 'Proven in-house — live proof, not a paid client.',
    featured: true,
    text: 'A real, non-tech SME in Malawi running agentic decision support: inventory, sales, shortage detection, cash reconciliation, procurement triggers, and profitability tracking. The world\u2019s smallest AI-native bar — a genuinely African SME AI transformation case, built in-house and documented openly.',
  },
  {
    id: 'PC-04',
    title: 'LightSpeed Holdings — The Meta Case Study',
    badge: 'Proven in-house.',
    text: 'The company is its own first customer. 144 agents across 20 departments, five-tier HITL approvals, immutable audit trails, RACI matrices, and governance controls mapped to regulatory requirements — operating daily.',
  },
  {
    id: 'PC-02',
    title: 'Health / M&E — Clinic Supply Chain Monitoring',
    badge: 'In pilot (composing evidence).',
    text: 'Agentic workflows for monitoring clinic supply chains and auto-generating procurement requests on anomaly detection (dashboard Z-score triggers).',
  },
  {
    id: 'PC-03',
    title: 'VSLA / SACCO / Mobile Money — Financial Inclusion',
    badge: 'In pilot (use case in active development).',
    text: 'Agentic workflows over mobile-money rails (Airtel Money, TNM Mpamba) for informal savings groups and micro-finance institutions.',
  },
  {
    id: 'PC-05',
    title: 'Chichewa AI / Ministry of Agriculture — Farmer Advisory',
    badge: 'In pilot.',
    text: 'Building the foundation for farmer advisory, citizen-query, and public-service agents in partnership with the Ministry of Agriculture.',
  },
];

export const workPolicy: WorkCard[] = [
  {
    id: 'POL-01',
    title: 'Citizen-Inquiry Lighthouse (Proposed)',
    badge: 'Proposed — not yet launched.',
    text: 'A high-visibility lighthouse use case — a citizen-inquiry or legislative-summary agent — with a non-commercial partner, as part of the National AI Strategy consultation.',
  },
  {
    id: 'POL-02',
    title: 'Governance Controls as National Template',
    badge: 'Proven in-house.',
    text: 'The governance pattern we propose as a national template already operates in-house: 5-tier approvals, immutable trails, RACI matrices, risk-classified tiers, and 4-gate client onboarding (G1–G4).',
  },
  {
    id: 'POL-03',
    title: 'Capacity Building',
    badge: 'In active development.',
    text: 'Training and certification programmes with Malawian universities (MUBAS, UNIMA) to build a sovereign agentic-AI talent pipeline.',
  },
  {
    id: 'SADC',
    title: 'National AI Strategy + SADC Framework',
    badge: 'Published (NAS) / In active development (SADC).',
    text: 'The SADC Agentic AI Governance Framework — the region\u2019s first operational governance standard for autonomous agentic AI — authored by the CEO and submitted to member-state ministers and regulators; National AI Strategy consultation published.',
  },
];

export const honestyPolicy: string[] = [
  'We publish the tests that gate our own work.',
  'Claims are labeled Proven in-house vs. In pilot — we do not blur them.',
  'Benchmarks are dated and regenerated on every release.',
];

/* ── Insights previews ────────────────────────────────────── */
export const insightTeasers: { title: string; topic: string; to: string }[] = [
  { title: 'The SADC AI Opportunity', topic: 'AI IN AFRICA', to: '/insights' },
  { title: 'What Agentic AI Means for African Governments', topic: 'AGENTIC AI', to: '/insights' },
  { title: 'From Digital Transformation to AI-Native Transformation', topic: 'DIGITAL TRANSFORMATION', to: '/insights' },
];

export default {
  company,
  mission,
  vision,
  values,
  pillars,
  financialGuardrails,
  commitments,
  solutions,
  GOVERNANCE_SOLUTION,
  industries,
  technologyPillars,
  technologyMetrics,
  technologyMethods,
  aiCompanyBuilder,
  scenarios,
  workCaseStudies,
  workPolicy,
  honestyPolicy,
  insightTeasers,
};
