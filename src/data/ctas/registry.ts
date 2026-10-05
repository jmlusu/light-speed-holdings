import raw from '../registries/cta-registry.json';

export interface CTAEntry {
  label: string;
  to: string;
  description: string;
  variant: string;
  usage: string;
}

export interface CTAsRegistry {
  version: string;
  description: string;
  lastUpdated: string;
  ctas: {
    primary: CTAEntry;
    secondary: CTAEntry;
    contextual: CTAEntry[];
    retired: string[];
    rules: string[];
  };
}

export const ctasRegistry = raw as CTAsRegistry;

export const canonicalCTALabels: Record<string, string> = {
  primary: raw.ctas.primary.label,
  secondary: raw.ctas.secondary.label,
};

export function getPrimaryCTA(): CTAEntry {
  return raw.ctas.primary;
}

export function getSecondaryCTA(): CTAEntry {
  return raw.ctas.secondary;
}

export function getContextualCTAs(): CTAEntry[] {
  return raw.ctas.contextual;
}
