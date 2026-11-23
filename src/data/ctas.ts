/* CTA registry — canonical labels and destinations for calls to action on the site.
 * "Contact Us" is the primary CTA. Keep retired phrasing ("Book a Briefing",
 * "Executive Briefing", "ENGAGE LIGHTSPEED") out of new copy. */

export interface Cta {
  label: string;
  to: string;
}

export const CTAS = {
  /** Primary conversion CTA — persistent across all views. */
  primary: { label: 'Contact Us', to: '/contact' },
  /** What We Do above-the-fold assessment request. */
  assessment: { label: 'Request an AI Readiness Assessment', to: '/contact' },
  /** Anchor jump to the service catalog on What We Do. */
  catalog: { label: 'Explore What We Do', to: '/what-we-do' },
} as const;

export const PRIMARY_CTA_LABEL: string = CTAS.primary.label;
export const PRIMARY_CTA_TO: string = CTAS.primary.to;
