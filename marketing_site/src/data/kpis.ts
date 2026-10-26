/* LightSpeed Holdings — KPI Metrics for AI Company Builder Page
   Supplemental KPI values displayed on the marketing page.
   These are distinct from src/data/metrics.ts (which is the canonical suite-wide source).
   Import from this file for page-specific KPI displays.
*/

export type KPIDimension = 'throughput' | 'latency' | 'cost' | 'quality';

export interface KPI {
  label: string;
  value: string | number;
  delta?: string; // e.g. "+34%" or "+71%"
  dimension?: KPIDimension;
  description?: string;
}

/** Key performance indicators for the AI Company Builder page */
export const kpis: KPI[] = [
  {
    label: 'Agents in Operation',
    value: 90,
    delta: '+0% (baseline canonical model)',
    description: '89 AI agents across 20 departments, each with explicit role definitions and permission sets.',
  },
  {
    label: 'Departments Covered',
    value: 20,
    delta: '',
    description: 'Agent workforce spans strategy, research, product, operations, governance, content, finance, and more.',
  },
  {
    label: '5‑Tier Approval Matrix',
    value: 'Active',
    delta: '',
    description: 'Every high‑impact decision passes through five tiers of human approval before execution.',
  },
  {
    label: 'Avg. Decision Latency',
    value: '2.3 hours',
    delta: '−85% vs industry',
    description: 'Mean time from decision point to human sign-off, measured across 14 engagements.',
  },
  {
    label: 'Compute Cost Reduction',
    value: '+34%',
    delta: '+34%',
    description: 'Modular agent replacement and latency‑aware routing reduced monthly AI spend across 12 engagements.',
  },
  {
    label: 'Audit Trail Coverage',
    value: '100%',
    delta: '',
    description: 'Append-only SHA-256 audit trails on all agent actions and governance decisions.',
  },
  {
    label: 'Trial‑to‑Production',
    value: '45 days',
    delta: '−75% vs industry',
    description: 'Governed deployment pipeline accelerates production readiness from trial to production.',
  },
];
