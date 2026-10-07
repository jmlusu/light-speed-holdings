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

export const solutionsRegistry = raw.solutions as Solution[];
