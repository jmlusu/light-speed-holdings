/* FAQ registry — MASTER_SPEC §15.
 * Every answer is grounded in a canonical source file; no invented numbers,
 * clients, prices, or outcomes (MASTER_SPEC §17 evidence rules). */

export interface Faq {
  id: string;
  question: string;
  answer: string;
}

export const faqs: readonly Faq[] = [
  {
    id: 'what-is-acb',
    question: 'What is the AI Company Builder?',
    answer:
      'A governed multi-agent orchestration platform where 90 AI agents and 1 human CEO work across 20 departments. Work flows from brief to inbox task to assigned agents to human review to deliverable — no client-facing deliverable ships without human sign-off.',
  },
  {
    id: 'human-in-the-loop',
    question: 'Does this replace our staff?',
    answer:
      'No. Agents execute tasks; people own outcomes. Every engagement runs through 5-tier human-in-the-loop approvals, so your team keeps decision authority while the platform carries the workload.',
  },
  {
    id: 'data-protection',
    question: 'How is our data protected?',
    answer:
      'The platform is designed for offline-first operation on local infrastructure and compliance with the Malawi Data Protection Act 2017/2024 and GDPR from day one. Every action writes to an append-only audit trail that is queryable and never overwritten.',
  },
  {
    id: 'proven-clients',
    question: 'Is this proven with paying clients?',
    answer:
      'Honestly: not yet. Nothing has been delivered to paying clients — all offers are fieldable in 2026, in pilot, or in active development, and every proof point on this site carries an explicit honesty badge. We would rather show you exactly where we are than invent a track record.',
  },
  {
    id: 'pricing',
    question: 'What does it cost?',
    answer:
      'Engagements are scoped per brief and priced for regional markets — accessible pricing in local currency rather than foreign-currency consultancy rates. There is no public rate card yet; start a conversation and we will tell you plainly what your project takes.',
  },
  {
    id: 'how-to-start',
    question: 'How do we start?',
    answer:
      'Start a conversation or request an AI Readiness Assessment. We will tell you honestly whether we can help, and exactly what it takes to start. Qualified enquiries get a response within two business days.',
  },
];
