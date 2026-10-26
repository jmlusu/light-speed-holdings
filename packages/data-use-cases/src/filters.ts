/**
 * @lightspeed/data-use-cases — Filter Functions
 *
 * Tree-shaking friendly filter functions for UseCasesPage consumption.
 * Each filter is a pure function for easy testing and composition.
 */

import type { UseCase, UseCaseStatus, ProblemCategory, SolutionCategory } from './types';
import { useCasesRegistry } from './registry';

/**
 * Filter use cases by status
 * @param status - The UseCaseStatus to filter by
 * @returns Array of use cases matching the status
 */
export function getUseCasesByStatus(status: UseCaseStatus): UseCase[] {
  return useCasesRegistry.filter(uc => uc.status === status);
}

/**
 * Filter use cases by sector ID
 * @param sectorId - The sector ID to filter by (matches sectorsRegistry)
 * @returns Array of use cases applicable to the sector
 */
export function getUseCasesBySector(sectorId: string): UseCase[] {
  return useCasesRegistry.filter(uc => uc.sector.includes(sectorId));
}

/**
 * Filter use cases by solution category
 * @param solutionCategory - The SolutionCategory to filter by
 * @returns Array of use cases matching the solution category
 */
export function getUseCasesBySolution(solutionCategory: SolutionCategory): UseCase[] {
  return useCasesRegistry.filter(uc => uc.solutionCategory.includes(solutionCategory));
}

/**
 * Filter use cases by problem category
 * @param problemCategory - The ProblemCategory to filter by
 * @returns Array of use cases matching the problem category
 */
export function getUseCasesByProblemCategory(problemCategory: ProblemCategory): UseCase[] {
  return useCasesRegistry.filter(uc => uc.problemCategory.includes(problemCategory));
}

/**
 * Get featured use cases for hero section
 * @returns Array of featured use cases
 */
export function getFeaturedUseCases(): UseCase[] {
  return useCasesRegistry.filter(uc => uc.featured === true);
}

/**
 * Get all use cases (for "all" filter option)
 * @returns Complete registry
 */
export function getAllUseCases(): UseCase[] {
  return useCasesRegistry;
}

/**
 * Search use cases by query string
 * Searches title, problem, and businessValue fields
 * @param query - Search query string
 * @returns Array of matching use cases
 */
export function searchUseCases(query: string): UseCase[] {
  const lowerQuery = query.toLowerCase().trim();
  if (!lowerQuery) return useCasesRegistry;

  return useCasesRegistry.filter(uc =>
    uc.title.toLowerCase().includes(lowerQuery) ||
    uc.problem.toLowerCase().includes(lowerQuery) ||
    uc.businessValue.toLowerCase().includes(lowerQuery) ||
    (uc.description?.toLowerCase().includes(lowerQuery) ?? false) ||
    (uc.whatItMonitorsOrProves?.toLowerCase().includes(lowerQuery) ?? false)
  );
}

/**
 * Get unique statuses present in registry
 * @returns Sorted array of unique UseCaseStatus values
 */
export function getAvailableStatuses(): UseCaseStatus[] {
  const statuses = new Set(useCasesRegistry.map(uc => uc.status));
  return Array.from(statuses).sort();
}

/**
 * Get unique problem categories present in registry
 * @returns Sorted array of unique ProblemCategory values
 */
export function getAvailableProblemCategories(): ProblemCategory[] {
  const categories = new Set<ProblemCategory>();
  useCasesRegistry.forEach(uc => uc.problemCategory.forEach(cat => categories.add(cat)));
  return Array.from(categories).sort();
}

/**
 * Get unique solution categories present in registry
 * @returns Sorted array of unique SolutionCategory values
 */
export function getAvailableSolutionCategories(): SolutionCategory[] {
  const categories = new Set<SolutionCategory>();
  useCasesRegistry.forEach(uc => uc.solutionCategory.forEach(cat => categories.add(cat)));
  return Array.from(categories).sort();
}

/**
 * Get unique sector IDs present in registry
 * @returns Sorted array of unique sector ID strings
 */
export function getAvailableSectors(): string[] {
  const sectors = new Set<string>();
  useCasesRegistry.forEach(uc => uc.sector.forEach(s => sectors.add(s)));
  return Array.from(sectors).sort();
}

/**
 * Composite filter function for UseCasesPage
 * Applies all active filters in sequence
 * @param filters - Object with optional filter properties
 * @returns Filtered use cases
 */
export interface UseCaseFilters {
  status?: UseCaseStatus | 'all';
  problemCategory?: ProblemCategory | 'all';
  solutionCategory?: SolutionCategory | 'all';
  sector?: string | 'all';
  searchQuery?: string;
}

export function applyFilters(filters: UseCaseFilters): UseCase[] {
  let results = useCasesRegistry;

  if (filters.status && filters.status !== 'all') {
    results = results.filter(uc => uc.status === filters.status);
  }

  if (filters.problemCategory && filters.problemCategory !== 'all') {
    const cat: ProblemCategory = filters.problemCategory;
    results = results.filter(uc => uc.problemCategory.includes(cat));
  }

  if (filters.solutionCategory && filters.solutionCategory !== 'all') {
    const cat: SolutionCategory = filters.solutionCategory;
    results = results.filter(uc => uc.solutionCategory.includes(cat));
  }

  if (filters.sector && filters.sector !== 'all') {
    results = results.filter(uc => uc.sector.includes(filters.sector!));
  }

  if (filters.searchQuery) {
    const query = filters.searchQuery.toLowerCase().trim();
    if (query) {
      results = results.filter(uc =>
        uc.title.toLowerCase().includes(query) ||
        uc.problem.toLowerCase().includes(query) ||
        uc.businessValue.toLowerCase().includes(query)
      );
    }
  }

  return results;
}
