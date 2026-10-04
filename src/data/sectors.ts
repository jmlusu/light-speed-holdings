/* LightSpeed Holdings — Sectors Registry (MASTER_SPEC §11)
   Canonical sector definitions: nine sectors, four evidence tiers.
   One canonical source per sector fact (§15). Only claim sector experience
   where evidence exists — every sector carries an evidence tier.
   Source: MASTER_SPEC §11 + verified engagements (siteContent case studies). */

import type { HonestyLabel, HonestyTone } from './siteContent';
import { liveTestCount } from './metrics';

export type SectorStatusTone = HonestyTone;

export interface Sector {
  id: string;
  title: string;
  description: string;
  status: HonestyLabel;
  evidence?: string;
  region?: string[];
}

/* MASTER_SPEC §11 four evidence tiers */
export const SECTOR_TIERS: Record<
  'proven' | 'current' | 'demonstration' | 'future',
  HonestyLabel
> = {
  proven: { label: 'PROVEN EXPERIENCE', tone: 'proven' },
  current: { label: 'CURRENT CAPABILITY', tone: 'pilot' },
  demonstration: { label: 'DEMONSTRATION', tone: 'fieldable' },
  future: { label: 'FUTURE OPPORTUNITY', tone: 'development' },
};

export const sectorTierLegend: { tier: HonestyLabel; desc: string }[] = [
  { tier: SECTOR_TIERS.proven, desc: 'Delivered engagements with named, measurable outcomes.' },
  { tier: SECTOR_TIERS.current, desc: 'Running pilots or capability we can deploy now.' },
  { tier: SECTOR_TIERS.demonstration, desc: 'Working demonstration without a live client engagement.' },
  { tier: SECTOR_TIERS.future, desc: 'Roadmap target — no evidence yet, and we say so.' },
];

export const sectors: Sector[] = [
  {
    id: 'government-public-sector',
    title: 'Government and Public Sector',
    description:
      'Digital services, compliance automation, and data-driven policy for ministries and agencies.',
    status: SECTOR_TIERS.current,
    evidence:
      'Agent-driven student management at the University of Malawi — 3 departments onboarded, 5,000 records processed with immutable audit trails. Advisory work on Malawi\u2019s National AI Strategy consultation.',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'development-donors',
    title: 'Development and Donor Organizations',
    description:
      'Donor reporting, M&E pipelines, and compliance workflows for UN and development partners.',
    status: SECTOR_TIERS.current,
    evidence:
      'Donor reporting automation with GDPR-level data handling as the default posture for UN and development data flows. Engagements priced in USD for international partners.',
    region: ['Malawi', 'SADC', 'Global'],
  },
  {
    id: 'health',
    title: 'Health',
    description:
      'Data pipelines, reporting automation, and decision support for clinics and health systems.',
    status: SECTOR_TIERS.future,
    evidence:
      'Offline-first, sovereignty-first architecture is designed for clinical data — but LightSpeed has no health-sector deployment yet. Listed honestly as a roadmap target.',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'financial-services',
    title: 'Financial Services',
    description:
      'Risk classification, audit trails, and regulatory reporting for banks and microfinance.',
    status: SECTOR_TIERS.proven,
    evidence:
      'Governed multi-agent compliance automation for a regional financial institution: regulatory reporting across 14 departments with full audit trails, cutting reporting time by 40%.',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'agriculture',
    title: 'Agriculture',
    description:
      'Supply-chain intelligence, mobile-money coordination, and climate-data pipelines for rural economies.',
    status: SECTOR_TIERS.current,
    evidence:
      'WhatsApp-native coordination platform for agricultural cooperatives across Malawi and Mozambique, with mobile-money payments and supply chain tracking — serving 1,200 members in pilot.',
    region: ['Malawi', 'Mozambique', 'SADC'],
  },
  {
    id: 'energy',
    title: 'Energy',
    description:
      'Data pipelines, reporting automation, and operational dashboards for energy providers.',
    status: SECTOR_TIERS.future,
    evidence:
      'No energy-sector engagement to date. The governance model and offline-first stack apply directly when the first partner appears.',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'telecommunications',
    title: 'Telecommunications',
    description:
      'Mobile-money rails and payment integrations embedded in delivered platforms.',
    status: SECTOR_TIERS.demonstration,
    evidence:
      'Mobile-money rails (Airtel Money, TNM Mpamba) integrated into delivered platforms. No direct telco operator engagement yet.',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'smes-entrepreneurs',
    title: 'SMEs and Entrepreneurs',
    description:
      'Mobile-first digital presence, automation, and AI tooling priced for the local market.',
    status: SECTOR_TIERS.current,
    evidence:
      'Mobile-first websites and e-commerce stores with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one, delivered at local cost from Malawi.',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'technology-companies',
    title: 'Technology Companies',
    description:
      'AI-native operating models, agentic workflows, and governance frameworks for tech firms.',
    status: SECTOR_TIERS.proven,
    evidence: `The AI Company Builder platform itself: a 90-agent registry, 5-tier approval matrix, and immutable audit trails verified by ${liveTestCount.toLocaleString('en-US')} automated regression tests.`,
    region: ['Malawi', 'SADC', 'Global'],
  },
];

// Helper to get sector by ID
export function getSectorById(id: string): Sector | undefined {
  return sectors.find((s) => s.id === id);
}

// Helper to get sectors by status tone
export function getSectorsByStatus(tone: SectorStatusTone): Sector[] {
  return sectors.filter((s) => s.status.tone === tone);
}

// Helper to get sectors by region
export function getSectorsByRegion(region: string): Sector[] {
  return sectors.filter((s) => s.region?.includes(region));
}
