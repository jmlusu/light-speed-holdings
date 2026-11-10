/**
 * @lightspeed/data-use-cases — Main Exports
 *
 * Canonical exports for Use Case explorer per Directive §11.
 * Consumed by UseCasesPage.tsx and other pages.
 *
 * Ported from AI Studio lsh-prototype data layer.
 * New exports use lightSpeed prefix where names collide with existing exports.
 */

// Types (existing, preserved unchanged)
export type {
  UseCase,
  UseCaseStatus,
  ProblemCategory,
  SolutionCategory,
  UseCaseFilterFn,
} from './types';

// Registry (existing exports preserved)
export { useCasesRegistry, USE_CASE_COUNT, VALID_SECTOR_IDS } from './registry';

// LightSpeed ported data registries (re-export all, no collisions with existing exports)
export * from './capabilities';
export * from './faqs';
export * from './governance';
export * from './insights';
export * from './metrics';
export * from './shipped/company';
export * from './shipped/ctas';
export * from './registry/sectors';
export * from './registry/solutions';

// Filters (existing exports preserved)
export {
  getUseCasesByStatus,
  getUseCasesBySector,
  getUseCasesBySolution,
  getUseCasesByProblemCategory,
  getFeaturedUseCases,
  getAllUseCases,
  searchUseCases,
  getAvailableStatuses,
  getAvailableProblemCategories,
  getAvailableSolutionCategories,
  getAvailableSectors,
  applyFilters,
  type UseCaseFilters,
} from './filters';
