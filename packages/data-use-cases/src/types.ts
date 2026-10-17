/**
 * @lightspeed/data-use-cases — Type Definitions
 *
 * Canonical types for Use Case explorer per Directive §11.
 * Matches the types expected by UseCasesPage.tsx.
 */

export type UseCaseStatus =
  | 'LIVE'
  | 'PROVEN_IN_HOUSE'
  | 'PILOT'
  | 'DEMONSTRATION'
  | 'FIELDABLE'
  | 'FUTURE';

export type ProblemCategory =
  | 'Cost'
  | 'Operational Latency'
  | 'Compliance'
  | 'Reporting'
  | 'Customer Experience'
  | 'Decision Intelligence'
  | 'Growth'
  | 'Administration'
  | 'Research'
  | 'Knowledge Work'
  | 'Market Intelligence';

export type SolutionCategory =
  | 'Strategy'
  | 'Agentic Automation'
  | 'Data & Intelligence'
  | 'Digital Transformation'
  | 'AI Governance'
  | 'Research & Policy';

/**
 * Core Use Case interface matching UseCasesPage consumption.
 * The page expects these exact properties for filtering and display.
 */
export interface UseCase {
  /** Unique slug for routing (e.g., '/use-cases/j-s-stopover-bar') */
  slug: string;

  /** Display title */
  title: string;

  /** Problem statement — what challenge does this solve? */
  problem: string;

  /** Quantified business value / outcome */
  businessValue: string;

  /** Evidence status — from Directive §11 honesty ladder */
  status: UseCaseStatus;

  /** Problem categories this use case addresses */
  problemCategory: ProblemCategory[];

  /** Solution categories this use case demonstrates */
  solutionCategory: SolutionCategory[];

  /** Sector IDs this use case applies to (matches sectorsRegistry) */
  sector: string[];

  /** Optional: mark as featured for hero section */
  featured?: boolean;

  /** Optional: detailed description for detail page */
  description?: string;

  /** Optional: what it monitors or proves */
  whatItMonitorsOrProves?: string;

  /** Optional: why it matters */
  whyItMatters?: string;

  /** Optional: badge type for visual styling */
  badgeType?: 'live' | 'proven' | 'pilot' | 'fieldable' | 'demonstration' | 'future';
}

/** Filter function types for tree-shaking friendly imports */
export type UseCaseFilterFn = (useCases: UseCase[]) => UseCase[];
