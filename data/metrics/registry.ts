/**
 * Platform Metrics Registry — Canonical Source of Truth
 *
 * Source: company-registry.yaml + pytest test suite + orchestration systems
 * Directive §22, §37 — Single source for all platform metrics
 *
 * Every metric carries an honesty tier. No invented numbers.
 */

export type HonestyTier = 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';

export interface PlatformMetric {
  id: string;
  label: string;
  value: string | number;
  source: string;
  category: 'agents' | 'departments' | 'tests' | 'governance' | 'cost' | 'uptime' | 'performance';
  honestyTier: HonestyTier;
  description?: string;
  lastUpdated: string; // ISO date
}

export const platformMetrics: PlatformMetric[] = [
  // Agent & Department Metrics (from company-registry.yaml)
  {
    id: 'agent-count',
    label: 'Canonical AI Agents',
    value: 90,
    source: 'company-registry.yaml',
    category: 'agents',
    honestyTier: 'verified',
    description: 'Total roles in operating model: 89 AI agents + 1 Human CEO',
    lastUpdated: '2026-10-05',
  },
  {
    id: 'ai-agent-count',
    label: 'AI Agents',
    value: 89,
    source: 'company-registry.yaml',
    category: 'agents',
    honestyTier: 'verified',
    description: 'Specialized AI agents across 20 departments',
    lastUpdated: '2026-10-05',
  },
  {
    id: 'human-ceo-count',
    label: 'Human CEO',
    value: 1,
    source: 'company-registry.yaml',
    category: 'agents',
    honestyTier: 'verified',
    description: 'Single Human CEO with final decision authority',
    lastUpdated: '2026-10-05',
  },
  {
    id: 'department-count',
    label: 'Departments Modeled',
    value: 20,
    source: 'company-registry.yaml',
    category: 'departments',
    honestyTier: 'verified',
    description: '20 departments across Executive, Technology, AI Research, Operations, Finance, Marketing, Sales, People, Security, IT, Data, Legal, Strategy, Customer Success, Product',
    lastUpdated: '2026-10-05',
  },
  {
    id: 'test-count',
    label: 'Automated Regression Tests',
    value: 2624,
    source: 'pytest test suite',
    category: 'tests',
    honestyTier: 'verified',
    description: 'Automated tests covering registry, orchestrator, LLM, security, workflow, memory, and integration layers',
    lastUpdated: '2026-10-04',
  },
  {
    id: 'approval-tiers',
    label: 'Human Approval Gates',
    value: '5-Tier',
    source: 'ApprovalGate matrix',
    category: 'governance',
    honestyTier: 'proven-in-house',
    description: '5-tier risk-classified approval matrix with expiration sweeps',
    lastUpdated: '2026-10-05',
  },
  {
    id: 'model-tiers',
    label: 'Model Tiers Configured',
    value: 3,
    source: 'llm/platform config',
    category: 'governance',
    honestyTier: 'proven-in-house',
    description: 'Tier 1: Fast (Big Pickle, Gemini Flash, Ollama), Tier 2: Standard (DeepSeek, Kimi), Tier 3: Premium (Gemini Pro, GPT-4o)',
    lastUpdated: '2026-10-05',
  },
  {
    id: 'agent-uptime',
    label: 'Agent Fleet Availability',
    value: '99.8%',
    source: 'orchestrator metrics',
    category: 'uptime',
    honestyTier: 'proven-in-house',
    description: 'Uptime and responsiveness across 90 registered agent cards',
    lastUpdated: '2026-09-09',
  },
  {
    id: 'llm-cost-per-task',
    label: 'Average Cost per Task',
    value: '$0.038',
    source: 'llm cost tracker',
    category: 'cost',
    honestyTier: 'proven-in-house',
    description: 'Inference and token cost per autonomously completed task',
    lastUpdated: '2026-09-09',
  },
  {
    id: 'escalation-rate',
    label: 'Escalation Rate',
    value: '2.1%',
    source: 'orchestrator metrics',
    category: 'performance',
    honestyTier: 'proven-in-house',
    description: 'Percentage of dispatched tasks that escalated to management or CEO',
    lastUpdated: '2026-09-09',
  },
  {
    id: 'csat-satisfaction',
    label: 'Client CSAT Satisfaction',
    value: '96.4%',
    source: 'customer success metrics',
    category: 'performance',
    honestyTier: 'proven-in-house',
    description: 'Enterprise client satisfaction score with AI deliverable accuracy',
    lastUpdated: '2026-09-09',
  },
];

/**
 * Get metric by ID
 */
export function getMetricById(id: string): PlatformMetric | undefined {
  return platformMetrics.find(m => m.id === id);
}

/**
 * Get metrics by category
 */
export function getMetricsByCategory(category: PlatformMetric['category']): PlatformMetric[] {
  return platformMetrics.filter(m => m.category === category);
}

/**
 * Get metrics by honesty tier
 */
export function getMetricsByHonestyTier(tier: HonestyTier): PlatformMetric[] {
  return platformMetrics.filter(m => m.honestyTier === tier);
}

/**
 * Format metric value for display
 */
export function formatMetricValue(metric: PlatformMetric): string {
  if (typeof metric.value === 'number') {
    if (metric.id === 'test-count') {
      return metric.value.toLocaleString('en-US');
    }
    return metric.value.toString();
  }
  return metric.value;
}

export default platformMetrics;
