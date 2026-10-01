/* LightSpeed Holdings — Canonical Sector Registry (CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §12)
   Five canonical sectors per MASTER_SPEC and TARGET_ARCHITECTURE.
   Evidence tiers: PROVEN / CURRENT / DEMO / FUTURE (mapped from SECTOR_TIERS).
   One canonical source per sector fact. Only claim sector experience where evidence exists.
   Source: sectors.ts (evidence) + MASTER_SPEC §11 (canonical 5 slugs). */

import type { HonestyLabel, HonestyTone } from './siteContent';
import { sectors as legacySectors, SECTOR_TIERS } from './sectors';

export type SectorStatusTone = HonestyTone;

export interface Sector {
  id: string;           // Canonical slug: financial-services, healthcare, agriculture, education, government
  title: string;
  description: string;
  status: HonestyLabel;
  evidence?: string;
  region?: string[];
  relevantSolutions?: string[]; // Solution slugs that apply to this sector
}

/* MASTER_SPEC §11 four evidence tiers — mapped from SECTOR_TIERS */
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
  { tier: SECTOR_TIERS_CANONICAL.future, desc: 'Roadmap target — no evidence yet, and we say so.' },
];

/* Helper to find legacy sector by partial ID match */
function findLegacySector(ids: string[]): typeof legacySectors[0] | undefined {
  return legacySectors.find(s => ids.some(id => s.id.includes(id) || id.includes(s.id)));
}

/* Five canonical sectors — mapped from legacy sectors where evidence exists */
export const sectors: Sector[] = [
  {
    id: 'financial-services',
    title: 'Financial Services',
    description: 'Risk classification, audit trails, and regulatory reporting for banks and microfinance.',
    status: SECTOR_TIERS_CANONICAL.proven,
    evidence:
      'Governed multi-agent compliance automation for a regional financial institution: regulatory reporting across 14 departments with full audit trails, cutting reporting time by 40%.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['ai-company-builder', 'enterprise-deployment', 'business-automation'],
  },
  {
    id: 'healthcare',
    title: 'Healthcare',
    description: 'Data pipelines, reporting automation, and decision support for clinics and health systems.',
    status: SECTOR_TIERS_CANONICAL.future,
    evidence:
      'Offline-first, sovereignty-first architecture is designed for clinical data — but LightSpeed has no healthcare deployment yet. Listed honestly as a roadmap target.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['enterprise-deployment', 'business-automation'],
  },
  {
    id: 'agriculture',
    title: 'Agriculture',
    description: 'Supply-chain intelligence, mobile-money coordination, and climate-data pipelines for rural economies.',
    status: SECTOR_TIERS_CANONICAL.current,
    evidence:
      'WhatsApp-native coordination platform for agricultural cooperatives across Malawi and Mozambique, with mobile-money payments and supply chain tracking — serving 1,200 members in pilot.',
    region: ['Malawi', 'Mozambique', 'SADC'],
    relevantSolutions: ['digital-presence', 'business-automation', 'enterprise-deployment'],
  },
  {
    id: 'education',
    title: 'Education',
    description: 'Student management, credential verification, and data-driven policy for schools and universities.',
    status: SECTOR_TIERS_CANONICAL.current,
    evidence:
      'Agent-driven student management at the University of Malawi — 3 departments onboarded, 5,000 records processed with immutable audit trails.',
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['ai-company-builder', 'enterprise-deployment', 'business-automation'],
  },
  {
    id: 'government',
    title: 'Government and Public Sector',
    description: 'Digital services, compliance automation, and data-driven policy for ministries and agencies.',
    status: SECTOR_TIERS_CANONICAL.current,
    evidence:
      "Advisory work on Malawi's National AI Strategy consultation. Policy-level engagement so far — no ministerial production deployment claimed.",
    region: ['Malawi', 'SADC'],
    relevantSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
  },
];

/* Helper to get sector by canonical ID */
export function getSectorById(id: string): Sector | undefined {
  return sectors.find((s) => s.id === id);
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