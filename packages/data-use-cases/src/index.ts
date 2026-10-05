/**
 * @lightspeed/data-use-cases — Main Exports
 *
 * Canonical exports for Use Case explorer per Directive §11.
 * Consumed by UseCasesPage.tsx and other pages.
 */

// Types
export type {
  UseCase,
  UseCaseStatus,
  ProblemCategory,
  SolutionCategory,
  UseCaseFilterFn,
} from './types';

// Registry
export { useCasesRegistry, USE_CASE_COUNT, VALID_SECTOR_IDS } from './registry';

// Filters
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
