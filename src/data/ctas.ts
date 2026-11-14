/* CTA registry — MASTER_SPEC §10 (CTA).
 * Canonical labels and destinations for every call to action on the site.
 * "ENGAGE LIGHTSPEED" is the single primary CTA (superseded "Start a Conversation"
 * in the prototype rebuild); retired phrasing ("Book a Briefing", "Executive
 * Briefing") must not return. */

export interface Cta {
  label: string;
  to: string;
}

export const CTAS = {
  /** Primary conversion CTA — persistent across all views. */
  primary: { label: 'ENGAGE LIGHTSPEED', to: '/contact' },
  /** What We Do above-the-fold assessment request. */
  assessment: { label: 'Request an AI Readiness Assessment', to: '/contact' },
  /** Anchor jump to the service catalog on What We Do. */
  catalog: { label: 'View Service Catalog', to: '/what-we-do' },
} as const;

export const PRIMARY_CTA_LABEL: string = CTAS.primary.label;
export const PRIMARY_CTA_TO: string = CTAS.primary.to;
