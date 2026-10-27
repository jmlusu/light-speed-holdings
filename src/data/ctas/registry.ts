import raw from '../registries/cta-registry.json';

export interface CTAEntry {
  id: string;
  label: string;
  to: string;
  href: string;
  description: string;
  variant: string;
  usage: string;
}

export interface CTAsRegistry extends Array<CTAEntry> {
  primary: CTAEntry;
  secondary: CTAEntry;
  contextual: CTAEntry[];
  retired: string[];
  rules: string[];
}

const ctas = raw.ctas;
const allCTAs: CTAEntry[] = [
  { ...ctas.primary, href: ctas.primary.to },
  { ...ctas.secondary, href: ctas.secondary.to },
  ...ctas.contextual.map((c: any) => ({ ...c, href: c.to })),
];
export const ctasRegistry = allCTAs as CTAsRegistry & CTAEntry[];
ctasRegistry.primary = allCTAs[0];
ctasRegistry.secondary = allCTAs[1];
ctasRegistry.contextual = allCTAs.slice(2);
ctasRegistry.retired = ctas.retired;
ctasRegistry.rules = ctas.rules;

export const canonicalCTALabels: Record<string, string> = {
  primary: ctas.primary.label,
  secondary: ctas.secondary.label,
};

export function getPrimaryCTA(): CTAEntry {
  return ctasRegistry.primary;
}

export function getSecondaryCTA(): CTAEntry {
  return ctasRegistry.secondary;
}

export function getContextualCTAs(): CTAEntry[] {
  return ctasRegistry.contextual;
}
