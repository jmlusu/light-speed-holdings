/* CTA registry — MASTER_SPEC §15.
 * Canonical labels and destinations for every call to action on the site.
 * "Start a Conversation" is the single primary CTA (rebuild decision 2);
 * retired phrasing ("Book a Briefing", "Executive Briefing") must not return. */

export interface Cta {
  label: string;
  to: string;
}

export const CTAS = {
  /** Primary conversion CTA — every high-intent button funnels here. */
  primary: { label: 'Start a Conversation', to: '/contact' },
  /** What We Do above-the-fold assessment request. */
  assessment: { label: 'Request an AI Readiness Assessment', to: '/contact' },
  /** Anchor jump to the service catalog on What We Do. */
  catalog: { label: 'View Service Catalog', to: '/what-we-do' },
} as const;

export const PRIMARY_CTA_LABEL: string = CTAS.primary.label;
export const PRIMARY_CTA_TO: string = CTAS.primary.to;
