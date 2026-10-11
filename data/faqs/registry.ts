/**
 * FAQs Registry — Canonical Source of Truth
 *
 * Source: Directive §18 (28 mandatory FAQs)
 * Directive §22 — Single source for all FAQs
 *
 * Every FAQ carries an honesty tier. Answers are evidence-controlled.
 */

export type FAQCategory =
  | 'general'
  | 'ai-company-builder'
  | 'use-cases'
  | 'governance'
  | 'models'
  | 'africa'
  | 'engagement'
  | 'pharos';

export type HonestyTier = 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';

export interface FAQ {
  id: string;
  question: string;
  answer: string;
  category: FAQCategory;
  tags: string[];
  honestyTier: HonestyTier;
  relatedUseCases?: string[];
  relatedSolutions?: string[];
  claimIds?: string[];  // References to claims registry
}

export const faqsRegistry: FAQ[] = [
  {
    id: 'faq-01',
    question: 'What is LightSpeed Holdings?',
    answer: 'LightSpeed Holdings Limited is the AI-native company builder for Southern Africa. We help organisations design, build, and govern AI-native businesses, intelligent workflows, and agentic systems — from Malawi, across SADC, and beyond. Our operating model contains 90 roles: 89 AI agents plus one Human CEO across 20 departments, governed by a 5-tier approval matrix and immutable audit trails.',
    category: 'general',
    tags: ['company', 'overview', 'mission'],
    honestyTier: 'verified',
    claimIds: ['CLM-001'],
  },
  {
    id: 'faq-02',
    question: 'What is the AI Company Builder?',
    answer: 'The AI Company Builder is LightSpeed\'s flagship platform: a governed multi-agent orchestration engine where 90 AI agents and 1 Human CEO operate across 20 departments. It provides multi-agent orchestration, a 5-tier approval matrix, immutable SHA-256 sealed audit trails, 4 governance gates (Contract, DPA, Compliance, Security), and model routing for cost optimization. It can run self-hosted on your infrastructure (Platform Licensing) or as a managed deployment.',
    category: 'ai-company-builder',
    tags: ['platform', 'architecture', 'features'],
    honestyTier: 'fieldable',
    relatedSolutions: ['ai-company-builder', 'platform-licensing', 'enterprise-deployment'],
    claimIds: ['CLM-002'],
  },
  {
    id: 'faq-03',
    question: 'How many agents does LightSpeed have?',
    answer: 'LightSpeed\'s operating model contains 90 roles: 89 AI agents plus one Human CEO. This is the canonical, current number — historical artifacts may reference 127, 143, 144, or 152, but those are superseded. The 89 AI agents are specialized specialists and executives; the 1 Human CEO holds final decision authority and operational intent.',
    category: 'ai-company-builder',
    tags: ['agents', 'count', 'human-ceo'],
    honestyTier: 'verified',
    claimIds: ['CLM-001'],
  },
  {
    id: 'faq-04',
    question: 'What does the Human CEO do?',
    answer: 'The Human CEO (Jack Mlusu) sets company vision, mission, and long-term strategy; makes final decisions on high-stakes matters; represents the company externally; hires and evaluates the executive team; communicates with the Board; approves major budgets; establishes culture; resolves executive conflicts; authorizes production deployments; and drives growth. The Human CEO is NOT an autonomous AI agent — they are the actual human founder/CEO directing the AI agent workforce.',
    category: 'ai-company-builder',
    tags: ['human-ceo', 'governance', 'authority'],
    honestyTier: 'verified',
    claimIds: ['CLM-003'],
  },
  {
    id: 'faq-05',
    question: 'Does LightSpeed replace employees?',
    answer: 'No. LightSpeed\'s model is "AI executes. Humans decide." Agents handle operational execution (classification, extraction, summarization, drafting, monitoring) while humans retain all decision authority, approval rights, and accountability. The Human CEO owns operational intent. In client engagements, we augment teams — we don\'t replace them. The J&S StopOver Bar case demonstrates a 1-human + 5-agent model covering 5 functional roles at fraction of headcount cost, with the human owner retaining full control.',
    category: 'ai-company-builder',
    tags: ['employment', 'augmentation', 'human-in-the-loop'],
    honestyTier: 'proven-in-house',
    relatedUseCases: ['sme-operations'],
    claimIds: ['CLM-004'],
  },
  {
    id: 'faq-06',
    question: 'What is H-A-O-M-T-G-V?',
    answer: 'H-A-O-M-T-G-V is LightSpeed\'s core intellectual and architectural framework:\n\n**H — HUMAN**: Operational intent and final decision authority (Human CEO)\n**A — AGENTS**: 90 specialized operating roles (89 AI agents + 1 Human CEO agent)\n**O — ORCHESTRATION**: Deterministic routing of data, tasks, and decisions across workflows (MessageBus)\n**M — MEMORY**: Persistent contextual data storage across 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate)\n**T — TOOLS**: Isolated execution environments for API integrations and actions (MCP, custom tools)\n**G — GOVERNANCE**: Five-tier approval controls and immutable logging (ApprovalGate, SHA-256 audit trails)\n**V — VALUE**: Measurable reductions in cost and operational latency\n\nThe Human layer remains above the system. Value is the business outcome. Feedback loops exist between Memory, Tools, Orchestration, and Governance.',
    category: 'ai-company-builder',
    tags: ['haomtgv', 'framework', 'architecture'],
    honestyTier: 'verified',
    claimIds: ['CLM-005'],
  },
  {
    id: 'faq-07',
    question: 'How does human approval work?',
    answer: 'Every agent action is risk-classified (5×5 likelihood × impact matrix → 4 risk levels: low, medium, high, critical). Based on risk level, the action routes through a 5-tier approval matrix:\n\n- **Tier 1 (Auto)**: Low risk, fully autonomous (classification, extraction, summarization)\n- **Tier 2 (Lead)**: Medium risk, specialist lead approves (standard workflows)\n- **Tier 3 (Dual)**: High risk, two approvers required (e.g., CISO + CTO for security)\n- **Tier 4 (Executive)**: Critical risk, executive approves (CFO for budgets, CLO for contracts)\n- **Tier 5 (CEO)**: Highest risk, Human CEO approves (strategy, major deployments, regulator filings)\n\nPending approvals expire on a periodic sweep (configured per tier, max 30 minutes for Tier 3+). No silent approvals — every gate is explicit and audited.',
    category: 'governance',
    tags: ['approval', 'hitl', 'risk', 'tiers'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-006'],
  },
  {
    id: 'faq-08',
    question: 'What does five-tier governance mean?',
    answer: 'Five-tier governance means every consequential action passes through a risk-classified approval gate with five escalation levels (Auto → Lead → Dual → Executive → CEO). It also includes 4 mandatory governance gates before any engagement: Contract (G1), Data Processing Agreement (G2), Compliance Review (G3), Security Assessment (G4). Every action generates an append-only SHA-256 sealed audit log. Pending approvals expire instead of queueing forever. This is proven in-house — LightSpeed runs on this governance model daily.',
    category: 'governance',
    tags: ['governance', 'five-tier', 'gates', 'audit'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-007'],
  },
  {
    id: 'faq-09',
    question: 'How are actions audited?',
    answer: 'Every agent action generates an append-only JSONL audit event with: timestamp, actor (agent ID or human), action type, prompt, tool invocations, outputs, approval chain, and SHA-256 seal. Events are written to immutable audit logs (orchestrator/audit_events.jsonl) and correlated via Merkle trees for tamper-evidence. The audit trail is queryable, attributable, and survives regulatory scrutiny. This is proven in-house — LightSpeed\'s internal operations run on this audit system daily with zero tampering incidents.',
    category: 'governance',
    tags: ['audit', 'sha256', 'immutable', 'jsonl'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-008'],
  },
  {
    id: 'faq-10',
    question: 'What is the role of memory?',
    answer: 'LightSpeed\'s memory system provides 6 persistent memory types for long-running context:\n\n1. **Episodic** — Specific task executions and outcomes\n2. **Semantic** — Facts, concepts, domain knowledge\n3. **Procedural** — Workflows, skills, "how-to" patterns\n4. **Relational** — Entity relationships, org charts, dependencies\n5. **Temporal** — Time-series data, trends, schedules\n6. **Aggregate** — Synthesized insights, cross-domain patterns\n\nMemory operates on a "recall-before-execute" principle: agents query relevant memory before acting. Consolidation and forgetting policies bound growth. Memory recall latency stays within executor budgets. This is proven in-house — the memory engine runs in production across all 90 agents.',
    category: 'ai-company-builder',
    tags: ['memory', 'recall', 'context', 'persistence'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-009'],
  },
  {
    id: 'faq-11',
    question: 'What tools can agents use?',
    answer: 'Agents use isolated execution environments with explicitly granted tools. The canonical tool vocabulary (OpenCode v2 permission keys) includes: read, edit, grep, list, bash, webfetch, task. Legacy aliases (write→edit, execute→bash, delegate→task, web_search→webfetch) are accepted but not used in new agent cards. Tools are granted per-agent in the registry (company-registry.yaml). Each tool invocation is logged in the audit trail. Agents cannot access tools not in their granted list — the ToolRunner validates against the canonical 7 tools at runtime.',
    category: 'ai-company-builder',
    tags: ['tools', 'permissions', 'toolrunner', 'mcp'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-010'],
  },
  {
    id: 'faq-12',
    question: 'What models does LightSpeed use?',
    answer: 'LightSpeed uses a model-agnostic, provider-agnostic routing architecture with 3 tiers:\n\n- **Tier 1 (Fast/Local)**: Big Pickle (OpenCode), Gemini 3.5 Flash, Ollama (Llama 3.1, Gemma 2, Qwen 2.5) — ~$0.075/1M tokens or free local\n- **Tier 2 (Standard)**: DeepSeek Chat, Kimi K2, Gemini 3.5 Flash — ~$0.30/1M tokens\n- **Tier 3 (Premium)**: Gemini 3.1 Pro, GPT-4o, DeepSeek Coder — ~$2.50/1M tokens\n\nRouting is automatic based on task complexity, volume, and cost policy. 9 providers configured including free local Ollama models for budget-constrained deployments. LightSpeed does NOT default to premium commercial models for every task.',
    category: 'models',
    tags: ['models', 'providers', 'routing', 'tiers', 'ollama'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-011'],
  },
  {
    id: 'faq-13',
    question: 'Why does LightSpeed prioritize open and open-weight models?',
    answer: 'This is core to LightSpeed\'s Africa-first business model, not a technical preference. Open-weight models enable:\n\n1. **Cost sovereignty** — Near-zero marginal cost for high-volume routine tasks\n2. **Data sovereignty** — Inference on local infrastructure, no data egress\n3. **Provider independence** — No vendor lock-in, no API deprecation risk\n4. **Offline capability** — Runs in low-bandwidth, intermittent connectivity environments\n5. **Regulatory compliance** — Meets Malawi DPA, AU Data Policy, GDPR for sensitive data\n\nCommercial APIs are used only when they provide material quality/latency/capability advantage for specific high-complexity tasks. The principle: "Use the least expensive model that can reliably do the job."',
    category: 'models',
    tags: ['open-weight', 'open-source', 'sovereignty', 'africa-first', 'economics'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-012'],
  },
  {
    id: 'faq-14',
    question: 'Can LightSpeed operate without expensive API calls?',
    answer: 'Yes. LightSpeed\'s architecture is designed for open-weight/local-first economics. With Ollama on local hardware (even CPU), you can run Llama 3.1, Gemma 2, Qwen 2.5 for classification, extraction, summarization, embeddings, and repetitive workflows at near-zero cost. LightSpeed internal operations route 70% of tasks to local/open-weight models, achieving $0.038 average cost per task. The Platform Licensing (E1) offering includes self-hosted deployment with local inference as the default.',
    category: 'models',
    tags: ['local-inference', 'ollama', 'cost', 'api-independence'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-013'],
  },
  {
    id: 'faq-15',
    question: 'Can LightSpeed run locally?',
    answer: 'Yes. The AI Company Builder is designed for offline-first, self-hosted deployment. Platform Licensing (E1) provides one-on-one onboarding to run your own governed AI company on your laptop, VPS, or on-premise servers. The full 90-agent orchestration engine, MessageBus, memory, tools, governance, and audit trails run locally. No cloud dependency required. LightSpeed itself runs this way internally (proven in-house).',
    category: 'models',
    tags: ['local', 'self-hosted', 'offline', 'platform-licensing'],
    honestyTier: 'fieldable',
    relatedSolutions: ['platform-licensing', 'enterprise-deployment'],
    claimIds: ['CLM-014'],
  },
  {
    id: 'faq-16',
    question: 'Can LightSpeed operate in low-bandwidth environments?',
    answer: 'Yes. LightSpeed is engineered for African infrastructure realities:\n\n- Local inference (Ollama) eliminates API latency and bandwidth needs\n- MessageBus uses local JSONL files — no persistent connections required\n- Progressive enhancement: core functionality works without JavaScript\n- WhatsApp-native interfaces work on 2G/3G\n- Mobile-money integration (Airtel Money, TNM Mpamba) works offline via USSD fallbacks\n- Model weights cached locally after initial download\n\nThis is proven in-house — LightSpeed operates from Lilongwe with intermittent connectivity.',
    category: 'africa',
    tags: ['low-bandwidth', 'offline', 'intermittent', 'africa-first'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-015'],
  },
  {
    id: 'faq-17',
    question: 'How does LightSpeed approach data sovereignty?',
    answer: 'Data sovereignty is architectural, not contractual:\n\n1. **Zero-Cloud Boundary option** — All inference, memory, and audit logs stay on your infrastructure\n2. **Malawi DPA 2017/2024 compliance** — Default posture for all engagements\n3. **GDPR-level handling** — For donor/UN data flows\n4. **Local encryption** — Memory encryption at rest, keys managed locally\n5. **No vendor access** — Self-hosted means no third party sees your data\n\nLightSpeed does not store client data in our systems. Client deployments are fully self-contained. This is proven in-house — LightSpeed\'s own operational data never leaves our infrastructure.',
    category: 'africa',
    tags: ['data-sovereignty', 'dpa', 'gdpr', 'encryption', 'zero-cloud'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-016'],
  },
  {
    id: 'faq-18',
    question: 'What sectors does LightSpeed work with?',
    answer: 'LightSpeed targets 10 sectors with varying evidence levels:\n\n**Proven Experience**: Financial Services (compliance automation, 40% reporting reduction)\n**Current Capability**: Agriculture (1,200 coop members pilot), Education (UoM, 3 depts/5K records), Government (National AI Strategy advisory), SMEs (J&S StopOver Bar live)\n**Fieldable**: Technology (Platform Licensing E1), Development (Kobo/DHIS2 pilot)\n**Future Opportunity**: Healthcare, Regulators, Research/Universities\n\nWe clearly distinguish proven experience from pilots and roadmap targets. No fabricated client logos or partnerships.',
    category: 'general',
    tags: ['sectors', 'evidence', 'honesty', 'transparency'],
    honestyTier: 'verified',
    relatedSectors: ['financial-services', 'agriculture', 'education', 'government', 'smes', 'development', 'technology', 'healthcare', 'regulators', 'research'],
    claimIds: ['CLM-017'],
  },
  {
    id: 'faq-19',
    question: 'Does LightSpeed work with universities?',
    answer: 'LightSpeed engages with universities as a strategic sector (Research & Universities). Current status: capacity building programs with Malawian universities (MUBAS, UNIMA) in development. Pharos research program produces evidence-led publications. No formal university partnerships or signed research agreements exist yet — we state this honestly. The goal is building a sovereign agentic-AI talent pipeline across Southern Africa so capability is developed locally rather than imported.',
    category: 'africa',
    tags: ['universities', 'research', 'capacity-building', 'talent'],
    honestyTier: 'future',
    relatedSectors: ['research', 'education'],
    claimIds: ['CLM-018'],
  },
  {
    id: 'faq-20',
    question: 'Does LightSpeed work with regulators?',
    answer: 'LightSpeed engages regulators as a strategic sector (Regulators & Standards Institutions). Current status: SADC Agentic AI Governance Framework in development, authored by CEO Jack Mlusu, submitted to digital ministers, MACRA, CRASA, central banks, and regional development banks. Aligned with AU Continental AI Strategy. Advisory work on Malawi\'s National AI Strategy consultation. No formal regulator partnerships or endorsements claimed — we distinguish policy engagement from formal partnerships.',
    category: 'africa',
    tags: ['regulators', 'policy', 'sadc', 'macra', 'governance'],
    honestyTier: 'future',
    relatedSectors: ['regulators', 'government'],
    claimIds: ['CLM-019'],
  },
  {
    id: 'faq-21',
    question: 'What is Pharos?',
    answer: 'Pharos is LightSpeed\'s in-house thought-leadership team — not a generic blog. Pharos turns LightSpeed\'s engineering, research, experimentation, and field observations into public intellectual work. Formats include: BRIEF (executive summaries), FIELD_NOTE (on-ground observations), RESEARCH_NOTE (evidence-led findings), POLICY_NOTE (regulatory frameworks), SYSTEM_MAP (architecture diagrams), DATA_STORY (visualizations), AI_ECONOMICS (cost/quality analysis), AFRICA_WATCH (regional monitoring). Topics: Agentic AI, AI Company Building, African AI, Open-Weight AI, AI Economics, AI Governance, AI Policy, AI Regulation, AI Safety, Digital Transformation, Data Architecture, Sovereign AI, Resource-Constrained Deployment. Every insight links back to Use Cases, Solutions, Sectors, and engagement CTAs.',
    category: 'pharos',
    tags: ['pharos', 'thought-leadership', 'research', 'formats'],
    honestyTier: 'proven-in-house',
    claimIds: ['CLM-020'],
  },
  {
    id: 'faq-22',
    question: 'What is a Use Case?',
    answer: 'A Use Case answers "What can LightSpeed actually do?" with evidence-controlled transparency. Each Use Case documents: problem, workflow, agents involved, inputs, orchestration, tools, human approval, output, business value, sector, solution, and status. Status levels: LIVE (paying client deployment), PROVEN_IN_HOUSE (running in LightSpeed operations), PILOT (active pilot with real users), DEMONSTRATION (working demo), FIELDABLE (ready for deployment), FUTURE (roadmap target). We never fabricate customer evidence, testimonials, logos, contracts, or metrics.',
    category: 'use-cases',
    tags: ['use-cases', 'evidence', 'status', 'honesty'],
    honestyTier: 'verified',
    claimIds: ['CLM-021'],
  },
  {
    id: 'faq-23',
    question: 'What does "Proven In-House" mean?',
    answer: '"Proven In-House" means the capability runs in LightSpeed\'s own daily operations, validated by our internal systems, tests, and audit trails. It is not a client deployment, but it is running, measured, and auditable. Examples: immutable audit trails (SHA-256 sealed, running daily), 5-tier approval matrix (governs all internal actions), agent fleet availability (99.8% measured), model routing (70% local/open-weight, $0.038/task). This is our highest evidence tier for capabilities not yet deployed to paying clients.',
    category: 'use-cases',
    tags: ['proven-in-house', 'evidence', 'honesty', 'internal'],
    honestyTier: 'verified',
    claimIds: ['CLM-022'],
  },
  {
    id: 'faq-24',
    question: 'Is every Use Case a paying-client deployment?',
    answer: 'No. Most Use Cases are not paying-client deployments. Our status system is explicit:\n- LIVE: Paying client, measurable outcomes (currently: compliance automation for regional financial institution)\n- PROVEN_IN_HOUSE: Running in LightSpeed operations (audit trails, approval matrix, model routing)\n- PILOT: Active pilot with real users, composing evidence (agricultural cooperatives, donor reporting)\n- DEMONSTRATION: Working demo, no live users\n- FIELDABLE: Technically ready, awaiting client\n- FUTURE: Roadmap target, no evidence yet\n\nWe never imply a paying client exists unless verified. The J&S StopOver Bar is a live proof-of-concept, not a paying client engagement.',
    category: 'use-cases',
    tags: ['use-cases', 'evidence', 'paying-client', 'honesty', 'transparency'],
    honestyTier: 'verified',
    claimIds: ['CLM-023'],
  },
  {
    id: 'faq-25',
    question: 'How do we engage LightSpeed?',
    answer: 'Three entry points:\n\n1. **AI Readiness Assessment** — 2-week structured evaluation of data, infrastructure, talent, governance gaps. Delivers prioritized roadmap.\n2. **Boardroom Briefing** — Focused session for leadership: platform demo, governance deep-dive, engagement roadmap.\n3. **Start a Conversation** — General inquiry via contact form; we route to the right team.\n\nAll engagements clear 4 governance gates (Contract, DPA, Compliance, Security) before work begins. Pricing varies by solution: Digital Presence (MWK 150K–1.8M), Business Automation (MWK 900K–2.5M + hosting), Data Intelligence (USD quoted), Platform Licensing (MWK 3.5M + MWK 350K/mo support).',
    category: 'engagement',
    tags: ['engagement', 'assessment', 'briefing', 'pricing', 'process'],
    honestyTier: 'fieldable',
    relatedSolutions: ['boardroom-briefing', 'digital-presence', 'business-automation', 'data-intelligence', 'platform-licensing'],
    claimIds: ['CLM-024'],
  },
  {
    id: 'faq-26',
    question: 'What does an AI Readiness Assessment involve?',
    answer: 'A 2-week structured engagement:\n\n1. **Stakeholder Interviews** — Leadership, IT, operations, compliance\n2. **Data Audit** — Catalog, quality, accessibility, sovereignty\n3. **Infrastructure Review** — Compute, network, cloud/on-prem, security\n4. **Talent Assessment** — Current skills, hiring needs, training plan\n5. **Governance Gap Analysis** — Policies, approvals, audit, regulatory\n6. **Roadmap Delivery** — Prioritized use cases, investment case, timeline\n\nOutput: AI Readiness Report with maturity scores, prioritized use cases, governance requirements, and investment case. Conducted by Pharos + Consulting Lead. Fieldable in 2026.',
    category: 'engagement',
    tags: ['assessment', 'readiness', 'roadmap', 'evaluation'],
    honestyTier: 'fieldable',
    relatedSolutions: ['boardroom-briefing', 'ai-company-builder'],
    claimIds: ['CLM-025'],
  },
  {
    id: 'faq-27',
    question: 'What does LightSpeed cost?',
    answer: 'Pricing varies by solution:\n\n- **Digital Presence**: MWK 150K (Google Business) to MWK 1.8M (E-commerce); 50% upfront/50% delivery\n- **Business Automation**: MWK 900K–2.5M per deliverable + MWK 100K/mo hosting (WhatsApp); pricing validated with prospects\n- **Data Intelligence**: USD quoted (MWK 700K–2M); 50% upfront/50% delivery; international NGOs pay USD\n- **Platform Licensing (E1)**: MWK 3.5M license + MWK 350K/mo support retainer; 1–2 week setup\n- **Boardroom Briefing**: Included in engagement; standalone on inquiry\n- **Enterprise Deployment**: Custom quote (RBAC, governance, local infrastructure)\n\nAll pricing excludes ad spend, hosting, domain, gateway fees. No hidden costs. Custom quotes for agency white-label (E2) and enterprise deployments.',
    category: 'engagement',
    tags: ['pricing', 'cost', 'mwk', 'usd', 'solutions'],
    honestyTier: 'fieldable',
    relatedSolutions: ['digital-presence', 'business-automation', 'data-intelligence', 'platform-licensing', 'enterprise-deployment'],
    claimIds: ['CLM-026'],
  },
  {
    id: 'faq-28',
    question: 'How quickly can an engagement begin?',
    answer: 'Typical timeline:\n\n1. **Initial Conversation** — Within 48 hours of inquiry\n2. **AI Readiness Assessment** — 2 weeks (if chosen as entry point)\n3. **Governance Gates** — Contract, DPA, Compliance, Security (1–2 weeks, parallel)\n4. **Pilot Kickoff** — 1 week after gates clear\n5. **First Deliverable** — 2–4 weeks depending on use case\n\nFastest path: Boardroom Briefing → Governance Gates → Pilot (3–4 weeks total). Platform Licensing (E1): 1–2 weeks setup after license purchase. We don\'t start work until governance gates clear — this is non-negotiable.',
    category: 'engagement',
    tags: ['timeline', 'engagement', 'governance-gates', 'speed'],
    honestyTier: 'fieldable',
    relatedSolutions: ['boardroom-briefing', 'platform-licensing', 'digital-presence', 'business-automation'],
    claimIds: ['CLM-027'],
  },
];

export function getFAQById(id: string): FAQ | undefined {
  return faqsRegistry.find(f => f.id === id);
}

export function getFAQsByCategory(category: FAQCategory): FAQ[] {
  return faqsRegistry.filter(f => f.category === category);
}

export function getFAQsByHonestyTier(tier: HonestyTier): FAQ[] {
  return faqsRegistry.filter(f => f.honestyTier === tier);
}

export function getFAQsForPage(page: 'home' | 'ai-company-builder' | 'use-cases' | 'about' | 'faq'): FAQ[] {
  const pageCategories: Record<string, FAQCategory[]> = {
    home: ['general', 'ai-company-builder', 'engagement'],
    'ai-company-builder': ['ai-company-builder', 'governance', 'models', 'africa'],
    'use-cases': ['use-cases', 'engagement'],
    about: ['general', 'africa', 'pharos'],
    faq: [...Object.values(faqsRegistry).reduce((acc, f) => { if (!acc.includes(f.category)) acc.push(f.category); return acc; }, [] as FAQCategory[])],
  };
  return faqsRegistry.filter(f => pageCategories[page]?.includes(f.category) || page === 'faq');
}

export default faqsRegistry;
