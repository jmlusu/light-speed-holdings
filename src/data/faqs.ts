/* FAQ registry - MASTER_SPEC §15.
 * Every answer is grounded in a canonical source file; no invented numbers,
 * clients, prices, or outcomes (MASTER_SPEC §17 evidence rules).
 *
 * Evidence contract (2026-10-25): every rendered FAQ carries at least one
 * `evidence` entry. A `verified` entry must point at a claim id in
 * src/data/registries/claims-registry.json or at a repo path plus literal
 * anchor text that actually contains the supporting wording. When no source
 * supports an answer, mark the entry `unknown` and say why in `note` - an
 * honest unknown beats a false verified. Guarded by
 * src/__tests__/faq-evidence.test.ts. */

export interface FaqEvidence {
  /** Claim id from claims-registry.json, or "repo/relative/path.md#literal anchor text". */
  source: string;
  status: 'verified' | 'unknown';
  note?: string;
}

export interface Faq {
  id: string;
  question: string;
  answer: string;
  /** Closest canonical entry in src/data/registries/faq-registry.json (traceability, not wording parity). */
  registryId: string;
  evidence: readonly FaqEvidence[];
}

export const faqs: readonly Faq[] = [
  {
    id: 'what-is-acb',
    registryId: 'faq-02',
    question: 'What is the AI Company Builder?',
    answer:
      'A governed multi-agent orchestration platform where 89 AI agents and 1 Human CEO work across 20 departments. Work flows from brief to inbox task to assigned agents to human review to deliverable; no client-facing deliverable ships without human sign-off.',
    evidence: [
      { source: 'claim.agent-count', status: 'verified' },
      { source: 'claim.department-count', status: 'verified' },
      {
        source: 'src/data/siteContent.ts#no client-facing deliverable ships without human',
        status: 'verified',
      },
    ],
  },
  {
    id: 'human-in-the-loop',
    registryId: 'faq-05',
    question: 'Does this replace our staff?',
    answer:
      'No. Agents execute tasks; people own outcomes. Every engagement runs through 5-tier human-in-the-loop approvals, so your team keeps decision authority while the platform carries the workload.',
    evidence: [
      { source: 'claim.five-tier-approval', status: 'verified' },
      {
        source: 'docs/client-facing/USE-CASE-CATALOG.md#Agents execute; the human CEO owns the outcome.',
        status: 'verified',
      },
    ],
  },
  {
    id: 'data-protection',
    registryId: 'faq-17',
    question: 'How is our data protected?',
    answer:
      'The platform is designed for offline-first operation on local infrastructure and compliance with the Malawi Data Protection Act 2017/2024 and GDPR from day one. Every action writes to an append-only audit trail that is queryable and never overwritten.',
    evidence: [
      { source: 'claim.sovereign-offline-first', status: 'verified' },
      { source: 'claim.data-protection-act-compliance', status: 'verified' },
      { source: 'claim.append-only-audit-trails', status: 'verified' },
      {
        source: 'docs/client-facing/USE-CASE-CATALOG.md#correlated, queryable, and never overwritten',
        status: 'verified',
      },
    ],
  },
  {
    id: 'proven-clients',
    registryId: 'faq-24',
    question: 'Is this proven with paying clients?',
    answer:
      'Honestly: not yet. Nothing has been delivered to paying clients. All offers are fieldable in 2026, in pilot, or in active development, and every proof point on this site carries an explicit honesty badge. We would rather show you exactly where we are than invent a track record.',
    evidence: [
      { source: 'claim.no-paying-clients', status: 'verified' },
      {
        source:
          'docs/client-facing/USE-CASE-CATALOG.md#Nothing in this document has been delivered to paying clients.',
        status: 'verified',
      },
    ],
  },
  {
    id: 'pricing',
    registryId: 'faq-27',
    question: 'What does it cost?',
    answer:
      'Engagements are scoped per brief and priced for regional markets: accessible pricing in local currency rather than foreign-currency consultancy rates. There is no public rate card yet; start a conversation and we will tell you plainly what your project takes.',
    evidence: [
      {
        source: 'src/data/insights.ts#no public rate card exists',
        status: 'verified',
      },
      {
        source: 'docs/MISSION_AND_VISION.md#Priced in the local currency',
        status: 'verified',
      },
      {
        source: 'src/data/offerFamilies.ts#50% upfront / 50% on delivery for all one-off projects.',
        status: 'verified',
        note: 'Supports the regional-currency pricing posture and payment terms; individual prices are offer language pending prospect validation.',
      },
    ],
  },
  {
    id: 'how-to-start',
    registryId: 'faq-25',
    question: 'How do we start?',
    answer:
      'Start a conversation or request an AI Readiness Assessment. We will tell you honestly whether we can help, and exactly what it takes to start. Qualified enquiries get a response within two business days.',
    evidence: [
      {
        source: 'src/lib/enquiry.ts#We respond to qualified enquiries within two business days.',
        status: 'verified',
      },
      {
        source: 'src/data/registries/cta-registry.json#REQUEST AN AI READINESS ASSESSMENT',
        status: 'verified',
      },
      {
        source:
          'src/components/ContactSection.tsx#We will be honest about whether we can help, and exactly what it takes to start.',
        status: 'verified',
      },
    ],
  },
];
