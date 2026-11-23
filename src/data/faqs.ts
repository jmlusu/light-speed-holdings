/* FAQ registry - shared by the FAQ page and FAQ card/section surfaces.
 * Keep answers grounded in canonical sources; no invented numbers, clients, prices, or outcomes.
 */

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
      'AI Company Builder is a governed multi-agent platform where 89 AI agents and 1 Human CEO work across 20 departments. Work moves from a brief to an inbox task, assigned agents, human review, and a deliverable. No client-facing deliverable ships without human sign-off.',
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
      'No. Agents handle execution; people remain accountable for outcomes. Every engagement uses 5-tier human-in-the-loop approvals, so your team keeps decision authority while the platform handles the workload.',
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
      'The platform is designed for offline-first operation on local infrastructure. It is built for compliance with the Malawi Data Protection Act 2024 and GDPR from day one. Every action is written to an append-only audit trail that can be queried but never overwritten.',
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
      'Not yet. Nothing has been delivered to paying clients. All offers are fieldable in 2026, in pilot, or in active development. Every proof point on this site carries an explicit honesty badge. We would rather show where we are than invent a track record.',
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
      'Engagements are scoped per brief and priced for the market they serve. Where possible, we quote in local currency instead of foreign-currency consultancy rates. There is no public rate card yet. Start a conversation and we will tell you plainly what your project requires.',
    evidence: [
      {
        source: 'docs/MISSION_AND_VISION.md#Priced in the local currency',
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
      'Start a conversation or request an AI Readiness Assessment. We will tell you honestly whether we can help and what it takes to begin. Qualified enquiries receive a response within two business days.',
    evidence: [
      {
        source: 'src/lib/enquiry.ts#We reply to qualified enquiries within two business days.',
        status: 'verified',
      },
      {
        source: 'src/data/registries/cta-registry.json#REQUEST AN AI READINESS ASSESSMENT',
        status: 'verified',
      },
      {
        source:
          'src/components/site/CtaBand.tsx#Tell us where your organisation stands today. We will tell you whether we can help and what you need to start.',
        status: 'verified',
      },
    ],
  },
];
