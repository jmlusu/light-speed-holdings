/* LightSpeed Holdings — Use Case Summaries
   Single source of truth for the AI Company Builder marketing page.
   Used by UseCaseCarousel component.
   All illustration references point to assets in static/brand/ or public/assets/.
*/

export type UseCaseColor = 'navy' | 'red' | 'cyan';

export interface UseCase {
  id: string;
  title: string;
  problem: string;
  outcome: string;
  illustration: string; // relative path from repo root (e.g. 'static/brand/...' or 'public/assets/...')
  color: UseCaseColor; // accent color for badge/label
}

/** Eight featured use cases demonstrating the AI Company Builder platform */
export const useCases: UseCase[] = [
  {
    id: 'agent-orchestration',
    title: 'Agent Orchestration at Scale',
    problem: 'Organizations struggle to coordinate multiple AI agents without conflict, resulting in duplicated effort and inconsistent outputs.',
    outcome: 'A modular agent topology with explicit role definitions and five-tier approval gates reduced coordination overhead by 68% and eliminated output conflicts.',
    illustration: 'public/assets/catalog/agent-orchestration.svg',
    color: 'cyan',
  },
  {
    id: 'governance-deployment',
    title: 'Governed Deployment Pipeline',
    problem: 'Rapid AI prototyping outpaces governance, creating compliance risk and audit blind spots when moving to production.',
    outcome: 'Append-only SHA-256 audit trails, risk-classified agent tiers, and expiry sweeps on stale approvals enabled compliance‑safe deployment in 45 days vs the industry average of 180.',
    illustration: 'public/assets/catalog/governance-deployment.svg',
    color: 'red',
  },
  {
    id: 'department-distribution',
    title: 'Department‑Wide Agent Distribution',
    problem: 'Scaling AI across 20+ departments requires role-scoped permissions that are simultaneously granular and governable.',
    outcome: '90 specialized agents configured across 20 departments with explicit permission sets reduced deployment time from months to weeks and eliminated unauthorized model access.',
    illustration: 'public/assets/catalog/department-distribution.svg',
    color: 'navy',
  },
  {
    id: 'cost-optimization',
    title: 'Cost‑Optimized Agent Workflows',
    problem: 'Unconstrained AI agent execution drives unpredictable compute costs and resource contention.',
    outcome: 'Latency‑aware routing and modular agent replacement reduced monthly AI spend by 34% while maintaining output quality across 12 use-case scenarios.',
    illustration: 'public/assets/catalog/cost-optimization.svg',
    color: 'cyan',
  },
  {
    id: 'research-acceleration',
    title: 'Research & Policy Acceleration',
    problem: 'Policy researchers spend disproportionate time on literature review and citation management rather than analysis.',
    outcome: 'Keyless database lookups across 78 public scientific databases accelerated evidence gathering by 71% and improved claim‑to‑source traceability.',
    illustration: 'public/assets/catalog/research-acceleration.svg',
    color: 'navy',
  },
  {
    id: 'customer-insights',
    title: 'Customer Insight Generation',
    problem: 'Synthesizing qualitative call transcripts into actionable product insights is manual, slow, and inconsistent across rep teams.',
    outcome: 'Structured evidence‑backed briefs generated from call transcript analysis reduced insight‑to‑action cycle from 3 weeks to 3 days with repeatable format.',
    illustration: 'public/assets/catalog/customer-insights.svg',
    color: 'red',
  },
  {
    id: 'multi‑modal‑deployment',
    title: 'Multi‑Modal Deployment',
    problem: 'Deploying AI capabilities across web, mobile, and edge environments requires separate implementations and inconsistent UX.',
    outcome: 'A single agent topology deployed across web (Vite React SPA), mobile (React Native), and edge (Cloudflare Workers) with shared role definitions and permission inheritance.',
    illustration: 'public/assets/catalog/multi-modal-deployment.svg',
    color: 'cyan',
  },
  {
    id: 'incident‑response',
    title: 'AI Incident Response',
    problem: 'When AI systems produce unexpected outputs, teams lack structured escalation, root‑cause analysis, and remediation playbooks.',
    outcome: 'A formal incident response protocol with SHA-256 audit trails, circuit breakers, and 30‑day support reduced mean‑time‑to‑remediation from 5 days to 8 hours across 23 recorded incidents.',
    illustration: 'public/assets/catalog/incident-response.svg',
    color: 'red',
  },
];
