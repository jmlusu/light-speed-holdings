import raw from '../registries/use-case-registry.json';

export type UseCaseStatus = 'LIVE' | 'PROVEN_IN_HOUSE' | 'PILOT' | 'DEMONSTRATION' | 'FIELDABLE' | 'FUTURE';

export type ProblemCategory = 'Cost' | 'Operational Latency' | 'Compliance' | 'Reporting' | 'Customer Experience' | 'Decision Intelligence' | 'Growth' | 'Administration' | 'Research' | 'Knowledge Work' | 'Market Intelligence';

export type SolutionCategory = 'Strategy' | 'Agentic Automation' | 'Data & Intelligence' | 'Digital Transformation' | 'AI Governance' | 'Research & Policy';

export interface UseCase {
  id: string;
  title: string;
  problem: string;
  workflow: string;
  agentsInvolved: string[];
  inputs: string[];
  orchestration: string;
  tools: string[];
  humanApproval: string;
  output: string;
  businessValue: string;
  sector: string;
  solution: string;
  status: UseCaseStatus;
  problemCategory?: ProblemCategory[];
  solutionCategory?: SolutionCategory[];
}

export interface UseCasesRegistry {
  version: string;
  description: string;
  lastUpdated: string;
  useCases: UseCase[];
}

const data = raw as unknown as UseCasesRegistry;
export const useCasesRegistry = data;

export function getUseCasesByStatus(status: UseCaseStatus): UseCase[] {
  return data.useCases.filter(uc => uc.status === status);
}

export function getUseCasesBySector(sector: string): UseCase[] {
  return data.useCases.filter(uc => uc.sector === sector);
}

export function getUseCasesBySolution(solution: string): UseCase[] {
  return data.useCases.filter(uc => uc.solution === solution);
}

export function getUseCasesByProblemCategory(category: ProblemCategory): UseCase[] {
  return data.useCases.filter(uc => uc.problemCategory?.includes(category));
}

export function getFeaturedUseCases(): UseCase[] {
  return data.useCases.filter(uc => uc.status === 'LIVE' || uc.status === 'PROVEN_IN_HOUSE');
}
