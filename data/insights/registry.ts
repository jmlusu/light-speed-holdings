/**
 * Insights Registry — Canonical Source of Truth
 *
 * Source: Directive §13, §40 + siteContent.ts
 * Directive §22 — Single source for all Pharos insights
 *
 * Pharos Formats: BRIEF, FIELD_NOTE, RESEARCH_NOTE, POLICY_NOTE, SYSTEM_MAP, DATA_STORY, AI_ECONOMICS, AFRICA_WATCH
 */

export type PharosFormat =
  | 'BRIEF'
  | 'FIELD_NOTE'
  | 'RESEARCH_NOTE'
  | 'POLICY_NOTE'
  | 'SYSTEM_MAP'
  | 'DATA_STORY'
  | 'AI_ECONOMICS'
  | 'AFRICA_WATCH';

export type InsightTopic =
  | 'Agentic AI'
  | 'AI Company Building'
  | 'African AI'
  | 'Open/Open-Weight AI'
  | 'AI Economics'
  | 'AI Governance'
  | 'AI Policy'
  | 'AI Regulation'
  | 'AI Safety'
  | 'Digital Transformation'
  | 'Data Architecture'
  | 'AI Use Cases'
  | 'Research'
  | 'Universities'
  | 'Academia'
  | 'SADC Technology'
  | 'Malawi Technology'
  | 'Sovereign AI'
  | 'Resource-Constrained AI Deployment';

export interface Insight {
  slug: string;
  title: string;
  topic: InsightTopic;
  excerpt: string;
  content: string;             // Markdown/MDX
  publishedAt: string;         // ISO date
  author: string;              // Pharos team member
  pharosFormat: PharosFormat;
  relatedUseCases: string[];   // Use case slugs
  relatedSolutions: string[];  // Solution slugs
  relatedSectors: string[];    // Sector IDs
  tags: string[];
  featured?: boolean;
  thumbnail?: string;
  readingTimeMinutes?: number;
}

export const insightsRegistry: Insight[] = [
  {
    slug: 'sadc-ai-opportunity',
    title: 'The SADC AI Opportunity',
    topic: 'SADC Technology',
    excerpt: 'How the SADC region can leapfrog to AI-native governance and economic development through sovereign, open-weight model deployment.',
    content: `# The SADC AI Opportunity

## Executive Summary

The Southern African Development Community (SADC) represents 16 member states, 380+ million people, and a combined GDP of $700B. Yet the region risks becoming a passive consumer of AI technologies developed elsewhere.

This brief outlines the strategic case for SADC sovereign AI capability.

## The Case for Sovereign AI

### Data Sovereignty
- Health, financial, and citizen data must remain within SADC jurisdiction
- AU Data Policy Framework and national DPA laws require local processing
- Cloud dependency creates strategic vulnerability

### Economic Opportunity
- AI-native governments can deliver services at 10x lower cost
- Regional AI market projected at $15B by 2030
- Local compute + open-weight models = sustainable economics

### Talent Development
- 50+ universities across SADC
- Youth demographic dividend (60% under 25)
- Curriculum alignment with agentic AI skills

## LightSpeed's Role

LightSpeed Holdings provides:
1. **AI Company Builder** — Governed 90-agent platform for public sector deployment
2. **Pharos Research** — Evidence-led policy analysis and framework development
3. **Capacity Building** — University partnerships for sovereign talent pipeline
4. **Model Routing** — Open-weight/local-first economics for resource-constrained environments

## Recommendations

1. **Adopt SADC Agentic AI Governance Framework** (in development)
2. **Establish Regional Compute Consortium** for shared inference infrastructure
3. **Mandate Open-Weight First** procurement for public sector AI
4. **Create SADC AI Talent Visa** for cross-border researcher mobility

## Next Steps

- Present framework to SADC Digital Ministers (Q4 2026)
- Pilot in 3 member states (Malawi, Zambia, Botswana)
- Scale to full regional deployment by 2028`,
    publishedAt: '2026-09-15',
    author: 'Jack Mlusu',
    pharosFormat: 'POLICY_NOTE',
    relatedUseCases: ['policy-analysis', 'regulatory-monitoring', 'executive-ai-readiness'],
    relatedSolutions: ['ai-governance-policy', 'boardroom-briefing', 'research-applied-ai'],
    relatedSectors: ['government', 'regulators', 'technology'],
    tags: ['SADC', 'sovereign-ai', 'policy', 'governance', 'regional-cooperation'],
    featured: true,
    thumbnail: 'insights/sadc-ai-opportunity.webp',
    readingTimeMinutes: 8,
  },
  {
    slug: 'agentic-ai-african-governments',
    title: 'What Agentic AI Means for African Governments',
    topic: 'Agentic AI',
    excerpt: 'Beyond chatbots: how multi-agent systems with governance can transform public service delivery, compliance, and citizen engagement across Africa.',
    content: `# What Agentic AI Means for African Governments

## Beyond Generative AI

Most African governments' AI exposure is limited to Generative AI (chatbots, content generation). Agentic AI is fundamentally different:

| Generative AI | Agentic AI |
|---------------|------------|
| Single-model, stateless | Multi-agent, stateful |
| Content generation | Task execution |
| No accountability | Full audit trails |
| Human-in-the-loop optional | Human-in-the-loop mandatory |

## The LightSpeed Model

### 90-Role Operating Model
- 89 AI agents + 1 Human CEO
- 20 departments (Finance, Health, Education, Agriculture, etc.)
- 5-tier approval matrix
- Immutable audit trails

### Governance First
Every agent action passes through:
1. **Risk Classification** (5×5 matrix → 4 risk levels)
2. **Approval Gate** (Tier 1–5 based on risk)
3. **Execution** (isolated tool environment)
4. **Audit Logging** (SHA-256 sealed JSONL)
5. **Expiry Sweep** (pending approvals auto-expire)

## African Context Advantages

### Offline-First Architecture
- Runs on local infrastructure (no cloud dependency)
- Ollama + open-weight models for zero-API-cost inference
- Mobile-money integration (Airtel Money, TNM Mpamba, M-Pesa)
- Chichewa/local language support

### Resource-Constrained Optimization
- Model routing: Local → Open-Weight API → Premium API
- Cost per task: $0.038 average
- 99.8% agent fleet availability

## Use Cases for Government

1. **Compliance Automation** — Regulatory reporting across ministries
2. **Citizen Services** — WhatsApp-native query agents
3. **Supply Chain** — Clinic/hospital inventory with anomaly detection
4. **Revenue Collection** — Tax compliance with risk classification
5. **Policy Analysis** — Legislative summarization and impact modeling

## Getting Started

1. **AI Readiness Assessment** — 2-week structured evaluation
2. **Pilot Design** — Single ministry, single use case
3. **Governance Setup** — Approval matrix, audit configuration
4. **Scale** — Department-by-department rollout

## Conclusion

Agentic AI is not a future technology — it's a governance discipline. African governments that adopt it now will set the standard for accountable, sovereign AI deployment globally.`,
    publishedAt: '2026-09-08',
    author: 'Pharos Research Team',
    pharosFormat: 'RESEARCH_NOTE',
    relatedUseCases: ['compliance-automation', 'citizen-engagement', 'policy-analysis', 'regulatory-monitoring'],
    relatedSolutions: ['ai-company-builder', 'ai-governance-policy', 'enterprise-deployment'],
    relatedSectors: ['government', 'regulators', 'healthcare', 'education'],
    tags: ['agentic-ai', 'government', 'governance', 'africa', 'public-sector'],
    featured: true,
    thumbnail: 'insights/agentic-ai-african-governments.webp',
    readingTimeMinutes: 10,
  },
  {
    slug: 'digital-to-ai-native-transformation',
    title: 'From Digital Transformation to AI-Native Transformation',
    topic: 'Digital Transformation',
    excerpt: 'Digital transformation digitized processes. AI-native transformation reimagines the operating model. Here\'s the difference and why it matters for African enterprises.',
    content: `# From Digital Transformation to AI-Native Transformation

## The Evolution

### Digital Transformation (2010–2020)
- Paper → PDF
- On-premise → Cloud
- Manual → Automated workflows
- **Result:** Faster processes, same org structure

### AI-Native Transformation (2024+)
- Human-only → Human + Agent workforce
- Static rules → Adaptive orchestration
- Reactive → Predictive/prescriptive
- **Result:** New operating model, new economics

## The LightSpeed AI Company Builder

### What Changes
| Dimension | Digital | AI-Native |
|-----------|---------|-----------|
| Workforce | 100% Human | 89 AI + 1 Human CEO |
| Decisions | Human-only | Risk-classified, human-gated |
| Memory | Documents | 6-type persistent memory |
| Tools | SaaS apps | Isolated execution environments |
| Governance | Policy docs | Code-enforced approval matrix |
| Economics | Linear scaling | Sub-linear (model routing) |

### The 6-Phase Engagement
1. **Orient** — AI Readiness Assessment
2. **Design** — Agent role definition, approval matrix
3. **Build** — Agent configuration, tool integration
4. **Deploy** — Governance gates, audit activation
5. **Govern** — Ongoing cadence, model routing
6. **Measure** — KPI tracking, value realization

## African Economics

### The Cost Curve
- Traditional: $50K–500K/year per SaaS tool
- AI-Native: $0.038/task average (model routing)
- Open-weight local inference: Near-zero marginal cost

### The Sovereignty Dividend
- Data never leaves your infrastructure
- No vendor lock-in (open-weight models)
- Regulatory compliance by architecture

## Case: J&S StopOver Bar

A Malawian bar/restaurant runs:
- Inventory agent (stock levels, reorder points)
- Sales agent (velocity, forecasting)
- Finance agent (cash reconciliation, P&L)
- Procurement agent (supplier orders)
- CEO dashboard (real-time visibility)

**Result:** 1 human + 5 agents = functional coverage of 5-person team at <10% cost.

## Your Transformation Starts Here

1. **Assess** — Book AI Readiness Assessment
2. **Align** — Boardroom Briefing for leadership
3. **Pilot** — Single department, single use case
4. **Scale** — Governed rollout across organization

The question isn't whether to transform. It's whether you'll govern the transformation or let it govern you.`,
    publishedAt: '2026-08-28',
    author: 'Pharos Research Team',
    pharosFormat: 'BRIEF',
    relatedUseCases: ['executive-ai-readiness', 'sme-operations', 'compliance-automation', 'market-intelligence'],
    relatedSolutions: ['ai-company-builder', 'boardroom-briefing', 'enterprise-deployment', 'platform-licensing'],
    relatedSectors: ['smes', 'technology', 'financial-services', 'government'],
    tags: ['transformation', 'ai-native', 'operating-model', 'africa', 'economics'],
    featured: true,
    thumbnail: 'insights/digital-to-ai-native.webp',
    readingTimeMinutes: 7,
  },
  {
    slug: 'african-ai-economics',
    title: 'African AI Economics: API Dependency vs Local Inference',
    topic: 'AI Economics',
    excerpt: 'Why LightSpeed routes 70% of tasks to local/open-weight models, and how the "least expensive model that reliably does the job" principle saves 80%+ on inference costs.',
    content: `# African AI Economics: API Dependency vs Local Inference

## The Problem

Most AI deployments in Africa default to commercial APIs (OpenAI, Anthropic, Google). This creates:
- **Cost unpredictability** — Per-token pricing at scale
- **Data sovereignty risk** — Data leaves national borders
- **Latency variance** — Cross-continental round trips
- **Vendor lock-in** — Migration costs at scale

## LightSpeed's Model Routing Architecture

### Tier 1: Local / Open-Weight (70% of tasks)
**Models:** Llama 3.1 (Ollama), Gemma 2, Qwen 2.5
**Cost:** Near-zero (electricity only)
**Latency:** 50–200ms local
**Use Cases:** Classification, extraction, summarization, embeddings, repetitive workflows

### Tier 2: Open-Weight APIs (20% of tasks)
**Models:** DeepSeek Chat, Kimi K2, Gemini 3.5 Flash
**Cost:** $0.075–0.30/1M tokens
**Latency:** 200–500ms regional
**Use Cases:** Standard reasoning, planning, synthesis

### Tier 3: Premium APIs (10% of tasks)
**Models:** Gemini 3.1 Pro, GPT-4o, Claude 3.5 Sonnet
**Cost:** $2.50–15.00/1M tokens
**Latency:** 500ms–2s global
**Use Cases:** Exceptional reasoning, complex generation, difficult edge cases

### Tier 4: Human (Final Authority)
**Role:** Decisions, approvals, accountability
**Cost:** Human time
**Use Cases:** Strategic decisions, regulatory filings, client deliverables

## The Routing Logic

\`\`\`python
def route_task(task: Task) -> ModelTier:
    if task.complexity <= 3 and task.volume > 100:
        return Tier1_LOCAL
    elif task.reasoning_depth <= 5:
        return Tier2_OPEN_WEIGHT_API
    elif task.requires_exceptional_reasoning:
        return Tier3_PREMIUM
    else:
        return Tier2_OPEN_WEIGHT_API  # Default
\`\`\`

## Measured Results (LightSpeed Internal)

| Metric | Before Routing | After Routing |
|--------|----------------|---------------|
| Avg cost/task | $0.12 | $0.038 |
| Premium API usage | 45% | 10% |
| Local inference | 15% | 70% |
| Data egress | 2.3 TB/mo | 0.4 TB/mo |

## Implementation for Your Organization

1. **Audit** — Classify your task portfolio by complexity/volume
2. **Provision** — Local GPU (or CPU) for Ollama
3. **Configure** — Routing rules in AI Company Builder
4. **Monitor** — Cost/quality dashboards
5. **Optimize** — Monthly routing review

## The Principle

> "Use the least expensive model that can reliably do the job."

This isn't about being cheap. It's about being sovereign, sustainable, and scalable in African realities.`,
    publishedAt: '2026-08-20',
    author: 'CAIO / Pharos Research Team',
    pharosFormat: 'AI_ECONOMICS',
    relatedUseCases: ['model-routing-optimization', 'local-inference', 'cost-optimization', 'data-sovereignty'],
    relatedSolutions: ['ai-company-builder', 'platform-licensing', 'research-applied-ai', 'enterprise-deployment'],
    relatedSectors: ['technology', 'financial-services', 'government', 'smes'],
    tags: ['ai-economics', 'model-routing', 'local-inference', 'open-weight', 'cost-optimization', 'sovereignty'],
    featured: true,
    thumbnail: 'insights/african-ai-economics.webp',
    readingTimeMinutes: 9,
  },
];

export const pharosFormats: { format: PharosFormat; description: string; template: string }[] = [
  { format: 'BRIEF', description: 'Executive summaries, board-ready', template: 'PharosBriefTemplate' },
  { format: 'FIELD_NOTE', description: 'Field observations, on-ground reality', template: 'PharosFieldNoteTemplate' },
  { format: 'RESEARCH_NOTE', description: 'Evidence-led research findings', template: 'PharosResearchNoteTemplate' },
  { format: 'POLICY_NOTE', description: 'Policy analysis, regulatory frameworks', template: 'PharosPolicyNoteTemplate' },
  { format: 'SYSTEM_MAP', description: 'Architecture diagrams, system explanations', template: 'PharosSystemMapTemplate' },
  { format: 'DATA_STORY', description: 'Data-driven narratives, visualizations', template: 'PharosDataStoryTemplate' },
  { format: 'AI_ECONOMICS', description: 'Cost/quality analysis, model routing', template: 'PharosAIEconomicsTemplate' },
  { format: 'AFRICA_WATCH', description: 'Regional monitoring, SADC/AU tracking', template: 'PharosAfricaWatchTemplate' },
];

export function getInsightBySlug(slug: string): Insight | undefined {
  return insightsRegistry.find(i => i.slug === slug);
}

export function getInsightsByFormat(format: PharosFormat): Insight[] {
  return insightsRegistry.filter(i => i.pharosFormat === format);
}

export function getInsightsByTopic(topic: InsightTopic): Insight[] {
  return insightsRegistry.filter(i => i.topic === topic);
}

export function getInsightsBySector(sectorId: string): Insight[] {
  return insightsRegistry.filter(i => i.relatedSectors.includes(sectorId));
}

export function getFeaturedInsights(): Insight[] {
  return insightsRegistry.filter(i => i.featured);
}

export default insightsRegistry;
