/* Pharos department content.
 *
 * Source of truth: docs/pharos/README.md, docs/pharos/positioning.md and
 * data/claims/registry.ts (CLM-020, "8 formats ... across 19 topics").
 * Every string here traces to one of those documents - no invented claims,
 * no invented metrics. Update the source documents first, then this file.
 */

export interface PharosPillar {
  id: string;
  title: string;
  question: string;
  proof: string;
}

export const pharosMission: string =
  'Pharos turns LightSpeed Holdings agentic AI engineering into a public intellectual program that positions the Human CEO as the leading voice on Agentic AI Company Building, Use Cases and Policy across Malawi and the SADC region.';

export const pharosWhy: string =
  'A pharos is a lighthouse - exactly the role the CEO plays: a visible, trusted beacon that helps institutions navigate the emerging discipline of agentic AI while the policy and category are still being defined.';

export const pharosPillars: PharosPillar[] = [
  {
    id: 'company-builder',
    title: 'Company Builder',
    question: 'How do we build organisations where AI agents perform meaningful organisational work?',
    proof: '90-agent architecture, 20 departments, 5-tier human-in-the-loop approvals and audit trails.',
  },
  {
    id: 'use-cases',
    title: 'Use Cases',
    question: 'Where should agents be deployed to create measurable economic and social value?',
    proof:
      'Documented, sector-specific deployments: J&S StopOver Bar, health and M&E, VSLA/SACCO finance, with LightSpeed as the meta-case-study.',
  },
  {
    id: 'policy',
    title: 'Policy',
    question: 'How should governments and institutions govern autonomous AI systems responsibly?',
    proof:
      'Malawi Data Protection Act 2024 literacy, the AU Continental AI Strategy and SADC digital transformation.',
  },
];

/** Publication formats Pharos produces (CLM-020). */
export const pharosFormats: string[] = [
  'BRIEF',
  'FIELD_NOTE',
  'RESEARCH_NOTE',
  'POLICY_NOTE',
  'SYSTEM_MAP',
  'DATA_STORY',
  'AI_ECONOMICS',
  'AFRICA_WATCH',
];

/** Operating principles, verbatim from docs/pharos/README.md. */
export const pharosPrinciples: string[] = [
  'Lead with working systems and measured results before policy language.',
  'Localise hard: power, connectivity, existing ministry data, procurement cycles.',
  'Document everything publicly in a form others can reuse or critique.',
  'Treat policy work as an extension of product work - governance features are the policy contribution.',
  'Protect the human-in-the-loop core; it is both a technical and political advantage.',
];

export default {
  pharosMission,
  pharosWhy,
  pharosPillars,
  pharosFormats,
  pharosPrinciples,
};
