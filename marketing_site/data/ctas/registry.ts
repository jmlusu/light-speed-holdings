/**
 * CTAs Registry — Canonical Source of Truth
 *
 * Source: Directive §34 + siteContent.ts
 * Directive §22 — Single source for all CTA labels and destinations
 *
 * Canonicalize CTA labels. Do NOT randomly alternate.
 */

export type CTAVariant = 'primary' | 'secondary' | 'contextual';

export interface CTA {
  id: string;
  label: string;
  variant: CTAVariant;
  href: string;
  context: string;             // Where this CTA appears
  trackingLabel: string;       // Analytics/event label
  honestyTier?: 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';
  ariaLabel?: string;          // Accessibility label
}

export const ctasRegistry: CTA[] = [
  // PRIMARY CTA — Global
  {
    id: 'cta-primary',
    label: 'START A CONVERSATION',
    variant: 'primary',
    href: '/contact',
    context: 'Global primary CTA — header, hero, footer, all major sections',
    trackingLabel: 'cta_primary_start_conversation',
    honestyTier: 'verified',
    ariaLabel: 'Start a conversation with LightSpeed Holdings',
  },

  // SECONDARY CTA — Global
  {
    id: 'cta-secondary',
    label: 'REQUEST AN AI READINESS ASSESSMENT',
    variant: 'secondary',
    href: '/ai-assessment',
    context: 'Global secondary CTA — hero, solutions, about, contact pages',
    trackingLabel: 'cta_secondary_ai_assessment',
    honestyTier: 'fieldable',
    ariaLabel: 'Request an AI Readiness Assessment from LightSpeed',
  },

  // CONTEXTUAL CTAs — Page-specific
  {
    id: 'cta-explore-aicb',
    label: 'EXPLORE AI COMPANY BUILDER',
    variant: 'contextual',
    href: '/ai-company-builder',
    context: 'AI Company Builder page, Home page (AI Company Builder section), Solutions page',
    trackingLabel: 'cta_contextual_explore_aicb',
    honestyTier: 'fieldable',
    ariaLabel: 'Explore the AI Company Builder platform',
  },
  {
    id: 'cta-explore-use-cases',
    label: 'EXPLORE USE CASES',
    variant: 'contextual',
    href: '/use-cases',
    context: 'Use Cases page, Home page (Use Cases section), Solutions page, Sectors page',
    trackingLabel: 'cta_contextual_explore_use_cases',
    honestyTier: 'verified',
    ariaLabel: 'Explore LightSpeed use cases',
  },
  {
    id: 'cta-explore-solutions',
    label: 'EXPLORE SOLUTIONS',
    variant: 'contextual',
    href: '/solutions',
    context: 'Solutions page, Home page (Solutions section), What We Do page',
    trackingLabel: 'cta_contextual_explore_solutions',
    honestyTier: 'verified',
    ariaLabel: 'Explore LightSpeed solutions',
  },
  {
    id: 'cta-read-pharos',
    label: 'READ PHAROS INSIGHTS',
    variant: 'contextual',
    href: '/insights',
    context: 'Insights page, Home page (Pharos section), About page',
    trackingLabel: 'cta_contextual_read_pharos',
    honestyTier: 'proven-in-house',
    ariaLabel: 'Read Pharos thought leadership insights',
  },
  {
    id: 'cta-explore-sectors',
    label: 'EXPLORE SECTORS',
    variant: 'contextual',
    href: '/sectors',
    context: 'Sectors page, Home page (Sectors section), Use Cases page',
    trackingLabel: 'cta_contextual_explore_sectors',
    honestyTier: 'verified',
    ariaLabel: 'Explore LightSpeed sectors',
  },
  {
    id: 'cta-view-governance',
    label: 'VIEW GOVERNANCE DETAILS',
    variant: 'contextual',
    href: '/ai-company-builder',
    context: 'Governance solution card, AI Company Builder page, Solutions page',
    trackingLabel: 'cta_contextual_view_governance',
    honestyTier: 'proven-in-house',
    ariaLabel: 'View governance framework details',
  },
  {
    id: 'cta-request-briefing',
    label: 'REQUEST A BOARDROOM BRIEFING',
    variant: 'contextual',
    href: '/contact',
    context: 'Boardroom Briefing solution card, Solutions page, What We Do page',
    trackingLabel: 'cta_contextual_request_briefing',
    honestyTier: 'fieldable',
    ariaLabel: 'Request a boardroom briefing from LightSpeed',
  },
  {
    id: 'cta-explore-digital-presence',
    label: 'EXPLORE DIGITAL PRESENCE',
    variant: 'contextual',
    href: '/solutions',
    context: 'Digital Presence solution card, Solutions page',
    trackingLabel: 'cta_contextual_explore_digital_presence',
    honestyTier: 'fieldable',
    ariaLabel: 'Explore digital presence solutions',
  },
  {
    id: 'cta-explore-business-automation',
    label: 'EXPLORE BUSINESS AUTOMATION',
    variant: 'contextual',
    href: '/solutions',
    context: 'Business Automation solution card, Solutions page',
    trackingLabel: 'cta_contextual_explore_business_automation',
    honestyTier: 'pilot',
    ariaLabel: 'Explore business process automation solutions',
  },
  {
    id: 'cta-explore-data-intelligence',
    label: 'EXPLORE DATA & INTELLIGENCE',
    variant: 'contextual',
    href: '/solutions',
    context: 'Data Intelligence solution card, Solutions page',
    trackingLabel: 'cta_contextual_explore_data_intelligence',
    honestyTier: 'pilot',
    ariaLabel: 'Explore data and intelligence solutions',
  },
  {
    id: 'cta-explore-enterprise-deployment',
    label: 'EXPLORE ENTERPRISE DEPLOYMENT',
    variant: 'contextual',
    href: '/solutions',
    context: 'Enterprise Deployment solution card, Solutions page',
    trackingLabel: 'cta_contextual_explore_enterprise_deployment',
    honestyTier: 'pilot',
    ariaLabel: 'Explore enterprise deployment solutions',
  },
  {
    id: 'cta-explore-platform-licensing',
    label: 'EXPLORE PLATFORM LICENSING',
    variant: 'contextual',
    href: '/solutions',
    context: 'Platform Licensing solution card, Solutions page',
    trackingLabel: 'cta_contextual_explore_platform_licensing',
    honestyTier: 'fieldable',
    ariaLabel: 'Explore platform licensing options',
  },
  {
    id: 'cta-schedule-walkthrough',
    label: 'SCHEDULE AN EXECUTIVE WALKTHROUGH',
    variant: 'contextual',
    href: '/contact',
    context: 'Proof/Use Cases page, Governance section, About page',
    trackingLabel: 'cta_contextual_schedule_walkthrough',
    honestyTier: 'proven-in-house',
    ariaLabel: 'Schedule an executive walkthrough of LightSpeed platform',
  },
  {
    id: 'cta-inspect-metrics',
    label: 'INSPECT PLATFORM METRICS',
    variant: 'contextual',
    href: '/ai-company-builder',
    context: 'Proof/Use Cases page metrics section',
    trackingLabel: 'cta_contextual_inspect_metrics',
    honestyTier: 'verified',
    ariaLabel: 'Inspect LightSpeed platform metrics',
  },
  {
    id: 'cta-see-evidence',
    label: 'SEE THE EVIDENCE',
    variant: 'contextual',
    href: '/use-cases',
    context: 'Home page Proof/Use Cases section, AI Company Builder page',
    trackingLabel: 'cta_contextual_see_evidence',
    honestyTier: 'verified',
    ariaLabel: 'See LightSpeed use case evidence',
  },
];

// Canonical CTA label mapping — use these exact strings only
export const canonicalCTALabels = {
  primary: 'START A CONVERSATION',
  secondary: 'REQUEST AN AI READINESS ASSESSMENT',
  exploreAICB: 'EXPLORE AI COMPANY BUILDER',
  exploreUseCases: 'EXPLORE USE CASES',
  exploreSolutions: 'EXPLORE SOLUTIONS',
  readPharos: 'READ PHAROS INSIGHTS',
  exploreSectors: 'EXPLORE SECTORS',
  viewGovernance: 'VIEW GOVERNANCE DETAILS',
  requestBriefing: 'REQUEST A BOARDROOM BRIEFING',
  exploreDigitalPresence: 'EXPLORE DIGITAL PRESENCE',
  exploreBusinessAutomation: 'EXPLORE BUSINESS AUTOMATION',
  exploreDataIntelligence: 'EXPLORE DATA & INTELLIGENCE',
  exploreEnterpriseDeployment: 'EXPLORE ENTERPRISE DEPLOYMENT',
  explorePlatformLicensing: 'EXPLORE PLATFORM LICENSING',
  scheduleWalkthrough: 'SCHEDULE AN EXECUTIVE WALKTHROUGH',
  inspectMetrics: 'INSPECT PLATFORM METRICS',
  seeEvidence: 'SEE THE EVIDENCE',
} as const;

export function getCTAById(id: string): CTA | undefined {
  return ctasRegistry.find(c => c.id === id);
}

export function getCTAsByVariant(variant: CTAVariant): CTA[] {
  return ctasRegistry.filter(c => c.variant === variant);
}

export function getCTAsByContext(context: string): CTA[] {
  return ctasRegistry.filter(c => c.context.includes(context));
}

export function getPrimaryCTA(): CTA {
  return ctasRegistry.find(c => c.id === 'cta-primary')!;
}

export function getSecondaryCTA(): CTA {
  return ctasRegistry.find(c => c.id === 'cta-secondary')!;
}

export function getContextualCTA(id: string): CTA | undefined {
  const cta = ctasRegistry.find(c => c.id === id);
  return cta?.variant === 'contextual' ? cta : undefined;
}

export default ctasRegistry;
