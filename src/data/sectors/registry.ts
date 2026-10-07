import raw from '../registries/sector-registry.json';

export interface Sector {
  id: string;
  title: string;
  description: string;
  keyUseCases: string[];
  honestyBadge: string;
  honestyNote: string;
  iconName: string;
  region: string[];
  relevantSolutions: string[];
}

export const sectorsRegistry = raw.sectors as Sector[];
