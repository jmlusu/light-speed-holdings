export interface LegacyRedirect {
  /** Route pattern as declared in the router (no leading slash). */
  from: string;
  /** Canonical live route (single hop, V2 architecture ruling). */
  to: string;
  /** Human name shown in the "moved" notice. */
  label: string;
}

/** Every retired path and its one-hop destination. Keep in sync with App.tsx. */
export const LEGACY_REDIRECTS: readonly LegacyRedirect[] = [
  { from: 'ai-company-builder', to: '/what-we-do', label: 'AI Company Builder' },
  { from: 'solutions', to: '/what-we-do', label: 'Solutions' },
  { from: 'sectors', to: '/what-we-do', label: 'Sectors' },
  { from: 'sectors/:slug', to: '/what-we-do', label: 'Sector brief' },
  { from: 'use-cases', to: '/what-we-do', label: 'Use cases' },
  { from: 'use-cases/:slug', to: '/what-we-do', label: 'Use case' },
  { from: 'faqs', to: '/faq', label: 'FAQs' },
  { from: 'who-we-are', to: '/about', label: 'Who we are' },
  { from: 'privacy', to: '/legal/privacy', label: 'Privacy' },
  { from: 'terms', to: '/legal/terms', label: 'Terms' },
  { from: 'architecture', to: '/what-we-do', label: 'Architecture' },
  { from: 'build', to: '/what-we-do', label: 'Build' },
  { from: 'offer-a', to: '/what-we-do', label: 'Offer A' },
  { from: 'offer-b', to: '/what-we-do', label: 'Offer B' },
  { from: 'offer-c', to: '/what-we-do', label: 'Offer C' },
  { from: 'offer-d', to: '/what-we-do', label: 'Offer D' },
  { from: 'offer-e', to: '/what-we-do', label: 'Offer E' },
  { from: 'proof', to: '/what-we-do', label: 'Proof' },
  { from: 'ask', to: '/contact', label: 'Ask LightSpeed' },
];
