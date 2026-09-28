/* Content governance registry — MASTER_SPEC §17.
 *
 * Every significant public claim carries a content state, an owner, and a
 * canonical source. Claims involving clients, financial performance,
 * partnerships, outcomes, scale, or impact require evidence before they can
 * be Published. Validate with `validateClaims(CONTENT_CLAIMS)` — it must
 * return an empty array (enforced by src/__tests__/governance.test.ts).
 */

export type ContentState = 'draft' | 'review' | 'approved' | 'published' | 'archived';

export type ClaimCategory =
  | 'client'
  | 'financial'
  | 'partnership'
  | 'outcome'
  | 'scale'
  | 'impact'
  | 'general';

export interface GovernedClaim {
  /** Registry entry id, e.g. "metrics.agent-count". */
  id: string;
  state: ContentState;
  /** Role or agent accountable for the claim's accuracy. */
  owner: string;
  /** Canonical source: data file or source document. */
  source: string;
  /** Sensitivity class — controls whether evidence is mandatory. */
  category: ClaimCategory;
  /** Required for evidence-backed categories once state is 'published'. */
  evidence?: string;
  /** ISO date of last human review. */
  lastReviewed?: string;
}

/** §17: these claim classes require evidence before publishing. */
const EVIDENCE_REQUIRED_CATEGORIES: readonly ClaimCategory[] = [
  'client',
  'financial',
  'partnership',
  'outcome',
  'scale',
  'impact',
];

export function requiresEvidence(category: ClaimCategory): boolean {
  return EVIDENCE_REQUIRED_CATEGORIES.includes(category);
}

/** Only 'published' content is publicly visible on the site. */
export function isPubliclyVisible(state: ContentState): boolean {
  return state === 'published';
}

/**
 * Returns the ids of claims that are published without required evidence,
 * or missing owner/source. An empty array means the registry is compliant.
 */
export function validateClaims(claims: readonly GovernedClaim[]): string[] {
  const violations: string[] = [];
  for (const claim of claims) {
    if (!claim.owner || !claim.source) {
      violations.push(`${claim.id}: missing owner/source`);
      continue;
    }
    if (claim.state === 'published' && requiresEvidence(claim.category) && !claim.evidence) {
      violations.push(`${claim.id}: published ${claim.category} claim without evidence`);
    }
  }
  return violations;
}

/**
 * Canonical registry of significant public claims on light-speed-holdings.com.
 * Grouped by registry (one entry per §15 registry), plus individual
 * evidence-sensitive claims.
 */
export const CONTENT_CLAIMS: readonly GovernedClaim[] = [
  // --- §15 registries ---
  {
    id: 'registry.services',
    state: 'published',
    owner: 'consulting-lead',
    source: 'src/data/useCaseCatalogData.ts (OFFER_FAMILIES)',
    category: 'outcome',
    evidence:
      'CATALOG_POSITIONING.honestyClassification: nothing delivered to paying clients; offers carry honesty-ladder badges.',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.solutions',
    state: 'published',
    owner: 'cmo',
    source: 'src/data/siteContent.ts (solutions, GOVERNANCE_SOLUTION)',
    category: 'general',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.sectors',
    state: 'published',
    owner: 'cmo',
    source: 'src/data/sectors.ts',
    category: 'general',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.case-studies',
    state: 'published',
    owner: 'cmo',
    source: 'src/data/siteContent.ts (workCaseStudies, workPolicy)',
    category: 'outcome',
    evidence:
      'CATALOG_POSITIONING.honestyClassification: case studies are fieldable/pilot work, not delivered client outcomes.',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.insights',
    state: 'published',
    owner: 'thought-leadership-lead',
    source: 'src/data/siteContent.ts (insightTeasers)',
    category: 'general',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.metrics',
    state: 'published',
    owner: 'cto',
    source: 'src/data/metrics.ts',
    category: 'scale',
    evidence: 'liveTestCount verified by uv run pytest; legacyPytestCount is an intentional audit trail.',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.capabilities',
    state: 'published',
    owner: 'coo',
    source: 'src/data/capabilities.ts',
    category: 'general',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.agents',
    state: 'published',
    owner: 'cto',
    source: 'src/data/public-agent-registry.json',
    category: 'scale',
    evidence:
      '90 approved agents, canonical count from company-registry.yaml (retired counts: 127/144/152/89).',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.leadership',
    state: 'published',
    owner: 'chief-of-staff',
    source: 'src/data/leadership.ts (from MISSION_AND_VISION v2.0, Sep 2026)',
    category: 'general',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.faqs',
    state: 'published',
    owner: 'customer-success',
    source: 'src/data/faqs.ts',
    category: 'general',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'registry.ctas',
    state: 'published',
    owner: 'cmo',
    source: 'src/data/ctas.ts',
    category: 'general',
    lastReviewed: '2026-09-28',
  },

  // --- Individual evidence-sensitive claims ---
  {
    id: 'claim.agent-count',
    state: 'published',
    owner: 'cto',
    source: 'src/data/public-agent-registry.json',
    category: 'scale',
    evidence: 'Canonical count of 90 agents; every view must consume this registry, not a hard-coded number.',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'claim.founder',
    state: 'published',
    owner: 'chief-of-staff',
    source: 'MISSION_AND_VISION (v2.0, Sep 2026)',
    category: 'general',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'claim.payment-rails',
    state: 'published',
    owner: 'coo',
    source: 'src/data/useCaseCatalogData.ts (CATALOG_METHOD.sovereignty)',
    category: 'partnership',
    evidence: 'Airtel Money, TNM Mpamba, and PayChangu integration described as platform capability, not a client win.',
    lastReviewed: '2026-09-28',
  },
  {
    id: 'claim.no-paying-clients',
    state: 'published',
    owner: 'ceo',
    source: 'src/data/useCaseCatalogData.ts (CATALOG_POSITIONING.honestyClassification)',
    category: 'client',
    evidence: 'Honesty statement: no work delivered to paying clients; all offers fieldable, piloting, or in development.',
    lastReviewed: '2026-09-28',
  },
];
