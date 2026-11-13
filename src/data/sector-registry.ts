/* LightSpeed Holdings - Canonical Sector Registry (CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §12)
   Canonical source of truth: 10 target sectors loaded from sector-registry.json.
   Evidence tiers: PROVEN / CURRENT / DEMO / FUTURE (mapped from SECTOR_TIERS).
   One canonical source per sector fact. Only claim sector experience where evidence exists. */

import type { HonestyLabel, HonestyTone } from './siteContent';
import rawSectors from './registries/sector-registry.json';

export type SectorStatusTone = HonestyTone;

export interface Sector {
  id: string;           // Canonical slug
  title: string;
  description: string;
  status: HonestyLabel;
  evidence?: string;
  region?: string[];
  relevantSolutions?: string[]; // Solution slugs that apply to this sector
}

/* MASTER_SPEC §11 four evidence tiers - mapped from SECTOR_TIERS */
export const SECTOR_TIERS_CANONICAL: Record<
  'proven' | 'current' | 'demonstration' | 'future',
  HonestyLabel
> = {
  proven: { label: 'PROVEN EXPERIENCE', tone: 'proven' },
  current: { label: 'CURRENT CAPABILITY', tone: 'pilot' },
  demonstration: { label: 'DEMONSTRATION', tone: 'fieldable' },
  future: { label: 'FUTURE OPPORTUNITY', tone: 'development' },
};

export const sectorTierLegend: { tier: HonestyLabel; desc: string }[] = [
  { tier: SECTOR_TIERS_CANONICAL.proven, desc: 'Delivered engagements with named, measurable outcomes.' },
  { tier: SECTOR_TIERS_CANONICAL.current, desc: 'Running pilots or capability we can deploy now.' },
  { tier: SECTOR_TIERS_CANONICAL.demonstration, desc: 'Working demonstration without a live client engagement.' },
  { tier: SECTOR_TIERS_CANONICAL.future, desc: 'Roadmap target: no evidence yet, and we say so.' },
];

/** Parse badge string into HonestyLabel with appropriate visual tone */
export function parseHonestyBadge(badge: string): HonestyLabel {
  const b = badge.toUpperCase();
  if (b.includes('PROVEN')) return { label: 'PROVEN EXPERIENCE', tone: 'proven' };
  if (b.includes('CURRENT')) return { label: 'CURRENT CAPABILITY', tone: 'pilot' };
  if (b.includes('PILOT')) return { label: 'IN PILOT', tone: 'pilot' };
  if (b.includes('FIELDABLE')) return { label: 'FIELDABLE', tone: 'fieldable' };
  if (b.includes('DEMO')) return { label: 'DEMONSTRATION', tone: 'fieldable' };
  if (b.includes('FUTURE')) return { label: 'FUTURE OPPORTUNITY', tone: 'development' };
  return { label: badge, tone: 'development' };
}

/* 10 canonical sectors mapped directly from sector-registry.json */
export const sectors: Sector[] = rawSectors.sectors.map((item) => ({
  id: item.id,
  title: item.title,
  description: item.description,
  status: parseHonestyBadge(item.honestyBadge),
  evidence: item.honestyNote,
  region: item.region,
  relevantSolutions: item.relevantSolutions,
}));

/* Alias map for backwards compatibility with legacy short slugs */
const SLUG_ALIASES: Record<string, string> = {
  'healthcare': 'healthcare-public-health',
  'agriculture': 'agriculture-agritech',
  'education': 'education-academia',
  'government': 'government-public-sector',
  'academia-research': 'research-universities',
  'smes': 'smes-private-enterprise',
  'nonprofit': 'development-nonprofit-organizations',
  'tech': 'technology-digital-businesses',
};

/* Helper to get sector by canonical or legacy ID */
export function getSectorById(id: string): Sector | undefined {
  const canonicalId = SLUG_ALIASES[id] || id;
  return sectors.find(
    (s) => s.id === canonicalId || s.id === id || s.id.startsWith(id) || id.startsWith(s.id)
  );
}

/* Helper to get sectors by status tone */
export function getSectorsByStatus(tone: SectorStatusTone): Sector[] {
  return sectors.filter((s) => s.status.tone === tone);
}

/* Helper to get sectors by region */
export function getSectorsByRegion(region: string): Sector[] {
  return sectors.filter((s) => s.region?.includes(region));
}

/* Helper to get sectors relevant to a solution */
export function getSectorsBySolution(solutionSlug: string): Sector[] {
  return sectors.filter((s) => s.relevantSolutions?.includes(solutionSlug));
}

/* Helper to get solutions relevant to a sector */
export function getSolutionsBySector(sectorId: string): string[] {
  const sector = getSectorById(sectorId);
  return sector?.relevantSolutions ?? [];
}
