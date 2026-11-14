/**
 * Company Identity Registry — Canonical Source of Truth
 *
 * Source: brand/tokens/brand-tokens.json + CEO Directives
 * Directive §2, §22 — Single source for all company identity facts
 *
 * DO NOT hardcode these values in components. Import from here.
 */

export interface CompanyIdentity {
  legalName: string;
  shortName: string;
  trademarkDomain: string;
  tagline: string;
  positioning: string;
  geographicProgression: string[];
  northStar: string;
  heroHeadline: string;
  heroSubline: string;
  valueCycle: string[];
  thesis: string;
  foundedYear: number;
  location: string;
  // Canonical role counts (Directive §2)
  totalRoles: number;
  aiAgentCount: number;
  humanCeoCount: number;
  departmentCount: number;
  governanceTiers: number;
}

export const companyIdentity: CompanyIdentity = {
  legalName: 'LightSpeed Holdings Limited',
  shortName: 'LightSpeed Holdings',
  trademarkDomain: 'LightSpeed Holdings Limited™',
  tagline: 'ASPIRE. ACT. ACHIEVE.',
  positioning: 'The AI-native company builder for Southern Africa.',
  geographicProgression: ['Malawi', 'SADC', 'Africa'],
  northStar: 'We build AI-native companies.',
  heroHeadline: 'Build, Govern & Scale Your Autonomous AI Workforce',
  heroSubline: 'LightSpeed Holdings helps organisations design, build and govern AI-native businesses, intelligent workflows and agentic systems — in Malawi, across SADC, and beyond.',
  valueCycle: [
    'Strategy & Roadmap',
    'AI Design Sprint',
    'Forward-Deployed Engineers',
    'Venture Co-Build',
    'Platform Licensing',
    'Industry Accelerators',
    'Client Portal'
  ],
  thesis: 'Aspire. Act. Achieve.',
  foundedYear: 2024,
  location: 'Lilongwe, Malawi',
  // CANONICAL COUNTS — Directive §2
  // NEVER use stale counts (127, 143, 144, 152)
  totalRoles: 90,
  aiAgentCount: 89,
  humanCeoCount: 1,
  departmentCount: 20,
  governanceTiers: 5,
};

/**
 * Human Authority Statement (Directive §24)
 * Use verbatim in all governance communications
 */
export const humanAuthorityStatement =
  'AI executes. Humans decide.';

export const humanAuthorityStatementFull =
  'Agents execute. The Human CEO owns operational intent and final decision authority.';

/**
 * Role breakdown for transparency
 */
export const roleBreakdown = {
  total: 90,
  aiAgents: 89,
  humanCeo: 1,
  departments: 20,
  executives: 15,
  specialists: 73,
  boardMembers: 2,
};

export default companyIdentity;
