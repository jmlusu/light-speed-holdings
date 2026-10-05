import raw from '../registries/solution-registry.json';

export interface Solution {
  slug: string;
  title: string;
  description: string;
  eyebrow: string;
  capabilities: string[];
  useCases: string[];
  cta: string;
}

export interface SolutionsRegistry {
  version: string;
  description: string;
  lastUpdated: string;
  solutions: Solution[];
}

export const solutionsRegistry = raw as SolutionsRegistry;
