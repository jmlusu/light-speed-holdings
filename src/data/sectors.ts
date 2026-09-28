/* LightSpeed Holdings — Sectors Registry
   Canonical sector definitions with honest status labels.
   Source: MISSION_AND_VISION (v2.0, Sep 2026) + verified engagements. */

import type { HonestyTone } from './siteContent';

export type SectorStatusTone = HonestyTone;

export interface Sector {
  id: string;
  title: string;
  description: string;
  status: {
    label: string;
    tone: SectorStatusTone;
  };
  evidence?: string;
  region?: string[];
}

export const sectors: Sector[] = [
  {
    id: 'government-public-sector',
    title: 'Government & Public Sector',
    description: 'Digital services, compliance automation, and data-driven policy for ministries and agencies.',
    status: { label: 'Proven in-house', tone: 'proven' },
    evidence: 'Malawi Central Bank Compliance Automation — 40% reduction in compliance reporting time across 14 departments',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'development-donors',
    title: 'Development & Donors',
    description: 'Donor reporting, M&E pipelines, and compliance workflows for UNDP and development partners.',
    status: { label: 'In pilot', tone: 'pilot' },
    evidence: 'SADC governance framework contributions; UNDP engagement in progress',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'financial-services',
    title: 'Financial Services',
    description: 'Risk classification, audit trails, and regulatory reporting for banks and microfinance.',
    status: { label: 'Fieldable in 2026', tone: 'fieldable' },
    evidence: 'Risk classification and audit trail generation proven in-house; regulatory reporting fieldable 2026',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'health',
    title: 'Health',
    description: 'Data pipelines, reporting automation, and decision support for clinics and health systems.',
    status: { label: 'Concept', tone: 'development' },
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'agriculture-energy',
    title: 'Agriculture & Energy',
    description: 'Supply-chain intelligence, climate-data pipelines, and operational dashboards for rural economies.',
    status: { label: 'Concept', tone: 'development' },
    evidence: 'SADC Agricultural Cooperative Digital Platform pilot — 1,200 cooperative members across Malawi and Mozambique',
    region: ['Malawi', 'Mozambique', 'SADC'],
  },
  {
    id: 'smes-entrepreneurs',
    title: 'SMEs & Entrepreneurs',
    description: 'Mobile-first digital presence, automation, and AI tooling priced for the local market.',
    status: { label: 'Fieldable in 2026', tone: 'fieldable' },
    evidence: 'Digital Presence solution with Airtel Money, TNM Mpamba, PayChangu integration',
    region: ['Malawi', 'SADC'],
  },
  {
    id: 'technology-companies',
    title: 'Technology Companies',
    description: 'AI-native operating models, agentic workflows, and governance frameworks for tech firms.',
    status: { label: 'In development', tone: 'development' },
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