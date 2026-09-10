import rawAgents from '../../company/agent-registry.json';
import { Agent, Department, TaskItem, ApprovalRequest, EscalationItem, KPIDefinition, ModelTierConfig, AuditEntry } from '../types';

export const agentsList: Agent[] = (rawAgents as any[]).map(a => ({
  name: a.name || a.id,
  role: a.role || a.title || a.name,
  type: (a.type as any) || 'Specialist',
  department: a.department || 'Operations',
  reportsTo: a.reportsTo || a.reports_to || 'chief-of-staff',
  directReports: a.directReports || a.direct_reports || [],
  description: a.description || '',
  responsibilities: a.responsibilities || [],
  guidelines: a.guidelines || '',
  tools: a.tools || ['read', 'edit', 'bash'],
  permission: a.permission || 'Execute'
}));

export const departmentsList: Department[] = [
  { id: 'board', name: 'Board', executive: 'board-chair', mission: 'Provide governance oversight, strategic counsel, and fiduciary stewardship to the CEO and executive team.', budget_category: 'operations', headcount_target: 7 },
  { id: 'ai_research', name: 'AI Research', executive: 'caio', mission: 'Advance AI research, model selection, and prompt engineering strategies.', budget_category: 'product_development', headcount_target: 10 },
  { id: 'business_development', name: 'Business Development', executive: 'cso', mission: 'Identify partnerships, ecosystem alliances, and channel strategy.', budget_category: 'growth', headcount_target: 3 },
  { id: 'customer_success', name: 'Customer Success', executive: 'customer-success', mission: 'Own customer onboarding, retention, expansion, and satisfaction metrics.', budget_category: 'growth', headcount_target: 5 },
  { id: 'data', name: 'Data', executive: 'cdo', mission: 'Manage data strategy, analytics, pipelines, and data governance.', budget_category: 'product_development', headcount_target: 5 },
  { id: 'executive', name: 'Executive', executive: 'human-ceo', mission: 'Set company vision, strategy, and culture. Orchestrate the organization.', budget_category: 'operations', headcount_target: 3 },
  { id: 'finance', name: 'Finance', executive: 'cfo', mission: 'Manage financial planning, budgeting, and fiscal health.', budget_category: 'operations', headcount_target: 3 },
  { id: 'it', name: 'IT', executive: 'cio', mission: 'Manage IT infrastructure and internal tools.', budget_category: 'infrastructure', headcount_target: 4 },
  { id: 'legal', name: 'Legal', executive: 'clo', mission: 'Manage legal affairs, contracts, compliance, and regulatory matters.', budget_category: 'operations', headcount_target: 3 },
  { id: 'marketing', name: 'Marketing', executive: 'cmo', mission: 'Drive brand awareness, demand generation, and market positioning.', budget_category: 'growth', headcount_target: 8 },
  { id: 'operations', name: 'Operations', executive: 'coo', mission: 'Optimize internal processes, workflows, and operational efficiency.', budget_category: 'operations', headcount_target: 8 },
  { id: 'people', name: 'People', executive: 'hr', mission: 'Attract, develop, and retain top talent. Maintain culture and values.', budget_category: 'people', headcount_target: 5 },
  { id: 'product', name: 'Product', executive: 'cpo', mission: 'Drive product vision, strategy, discovery, and design.', budget_category: 'product_development', headcount_target: 5 },
  { id: 'qa', name: 'QA', executive: 'qa-lead', mission: 'Ensure software quality through testing strategies, automation, and quality gates.', budget_category: 'product_development', headcount_target: 4 },
  { id: 'sales', name: 'Sales', executive: 'sales', mission: 'Generate revenue through new business acquisition and pipeline management.', budget_category: 'growth', headcount_target: 10 },
  { id: 'security', name: 'Security', executive: 'ciso', mission: 'Protect company assets, data, and systems from security threats.', budget_category: 'infrastructure', headcount_target: 5 },
  { id: 'strategy', name: 'Strategy', executive: 'cso', mission: 'Drive corporate strategy, M&A, competitive intelligence, and market expansion.', budget_category: 'operations', headcount_target: 3 },
  { id: 'consulting', name: 'Consulting', executive: 'consulting-lead', mission: 'Deliver AI-native consulting engagements, mapping workflows and identifying transformation opportunities.', budget_category: 'growth', headcount_target: 4 },
  { id: 'technology', name: 'Technology', executive: 'cto', mission: 'Build and maintain software, infrastructure, and technical architecture.', budget_category: 'product_development', headcount_target: 25 },
  { id: 'pharos', name: 'Pharos', executive: 'thought-leadership-lead', mission: 'Position the Human CEO as the leading voice on Agentic AI Company Building and Policy across SADC region.', budget_category: 'growth', headcount_target: 7 }
];

export const initialTasks: TaskItem[] = [
  {
    id: 'TSK-1092',
    title: 'Model Routing Cost Optimization for Batch Evaluation',
    instruction: 'Route non-critical background jobs from Tier 3 (Premium) to Tier 1 (Fast Big Pickle / Gemini Flash). Measure latency and token savings.',
    status: 'in_progress',
    priority: 'P1',
    sender_id: 'cto',
    receiver_id: 'lead-backend',
    department: 'Technology',
    created_at: '2026-09-09T08:15:00Z',
    updated_at: '2026-09-09T09:40:00Z'
  },
  {
    id: 'TSK-1093',
    title: 'SADC Agentic Governance Policy Framework Draft',
    instruction: 'Complete section 4 regarding cross-border data transfer safeguards and AI safety certifications for public sector deployments.',
    status: 'review',
    priority: 'P0',
    sender_id: 'human-ceo',
    receiver_id: 'agentic-policy-analyst',
    department: 'Pharos',
    created_at: '2026-09-08T14:30:00Z',
    updated_at: '2026-09-09T10:05:00Z'
  },
  {
    id: 'TSK-1094',
    title: 'Q3 Enterprise Client Onboarding Security Audit',
    instruction: 'Perform automated SOC2 compliance checklist verification on the newly provisioned tenant data vaults.',
    status: 'pending',
    priority: 'P2',
    sender_id: 'ciso',
    receiver_id: 'security-architect',
    department: 'Security',
    created_at: '2026-09-09T07:20:00Z',
    updated_at: '2026-09-09T07:20:00Z'
  },
  {
    id: 'TSK-1095',
    title: 'Quarterly Cloud & LLM Budget Variance Report',
    instruction: 'Aggregate token consumption across all 20 departments against the $15.0M annual allocation.',
    status: 'completed',
    priority: 'P1',
    sender_id: 'cfo',
    receiver_id: 'financial-analyst',
    department: 'Finance',
    created_at: '2026-09-07T11:00:00Z',
    updated_at: '2026-09-08T16:45:00Z',
    result: 'Report generated: LLM spend is at 18.4% of annualized cap. Efficiency gains from prompt caching reduced monthly inference cost by 22%.'
  },
  {
    id: 'TSK-1096',
    title: 'Sub-agent Concurrency Deadlock in Async Task Queue',
    instruction: 'Deadlock observed in MessageBus when 12+ subagents synchronously invoke external REST endpoints without token bucket rate limiting.',
    status: 'escalated',
    priority: 'P0',
    sender_id: 'orchestration-owner',
    receiver_id: 'vp-engineering',
    department: 'Technology',
    created_at: '2026-09-09T09:12:00Z',
    updated_at: '2026-09-09T10:20:00Z'
  },
  {
    id: 'TSK-1097',
    title: 'Customer Satisfaction Score (CSAT) Trend Ingestion',
    instruction: 'Sync Zendesk and Slack Connect enterprise sentiment scores into the customer success KPI pipeline.',
    status: 'completed',
    priority: 'P2',
    sender_id: 'customer-success',
    receiver_id: 'business-intelligence-engineer',
    department: 'Customer Success',
    created_at: '2026-09-06T10:00:00Z',
    updated_at: '2026-09-07T15:30:00Z',
    result: 'Aggregated CSAT for active enterprise clients stands at 96.4% across 48 accounts.'
  }
];

export const initialApprovals: ApprovalRequest[] = [
  {
    id: 'APR-204',
    task_id: 'TSK-1088',
    title: 'Model Routing Tier Upgrade for Malawian Language Model Fine-tuning',
    tier: 'Tier 5 (CEO)',
    requested_by: 'caio',
    approver_role: 'Human CEO',
    status: 'pending',
    reason: 'Requires allocation of $14,200 for specialized multi-GPU cluster compute hours and proprietary dataset licensing.',
    amount: '$14,200',
    created_at: '2026-09-09T08:30:00Z'
  },
  {
    id: 'APR-205',
    task_id: 'TSK-1089',
    title: 'External API Integration Whitelist: World Bank Open Data Gateway',
    tier: 'Tier 4 (Executive)',
    requested_by: 'consulting-lead',
    approver_role: 'Chief Technology Officer (CTO)',
    status: 'pending',
    reason: 'Enables real-time retrieval of sub-Saharan agricultural macroeconomic indicators for the Pharos consultancy engagement.',
    created_at: '2026-09-09T09:10:00Z'
  },
  {
    id: 'APR-206',
    task_id: 'TSK-1085',
    title: 'Sub-agent Permission Elevation for Database Migration',
    tier: 'Tier 3 (Dual)',
    requested_by: 'lead-backend',
    approver_role: 'CISO & CTO',
    status: 'approved',
    reason: 'Granted automated execution permissions to backend agent for running idempotent migration scripts.',
    created_at: '2026-09-08T16:00:00Z',
    notes: 'Approved with requirement of continuous JSONL audit log stream.'
  }
];

export const initialEscalations: EscalationItem[] = [
  {
    id: 'ESC-401',
    task_id: 'TSK-1096',
    title: 'Sub-agent Concurrency Deadlock in Async Task Queue',
    agent_id: 'orchestration-owner',
    department: 'Technology',
    reason: 'High contention on .opencode/inbox.json under concurrent sub-agent batch dispatch. SLA exceeded 15 minutes.',
    level: 'critical',
    status: 'open',
    created_at: '2026-09-09T09:12:00Z'
  },
  {
    id: 'ESC-402',
    task_id: 'TSK-1077',
    title: 'Contract Liability Clause Conflict in Client SOW',
    agent_id: 'legal-owner',
    department: 'Legal',
    reason: 'Client requested uncapped indemnification for autonomous agent execution. Requires CLO and CEO sign-off.',
    level: 'high',
    status: 'investigating',
    created_at: '2026-09-08T11:45:00Z'
  }
];

export const initialKPIs: KPIDefinition[] = [
  {
    id: 'org_health_composite',
    department: 'Executive',
    name: 'Org Health Composite Score',
    current: 94.2,
    target: 90.0,
    unit: 'score',
    status: 'good',
    description: 'Weighted aggregate of task success rate, agent uptime, cost efficiency, and escalation frequency.',
    trend: 'up',
    history: [
      { timestamp: 'Sep 03', value: 88.5 },
      { timestamp: 'Sep 04', value: 90.1 },
      { timestamp: 'Sep 05', value: 91.4 },
      { timestamp: 'Sep 06', value: 92.0 },
      { timestamp: 'Sep 07', value: 93.5 },
      { timestamp: 'Sep 08', value: 93.8 },
      { timestamp: 'Sep 09', value: 94.2 }
    ]
  },
  {
    id: 'task_success_rate',
    department: 'Technology',
    name: 'Task Completion Rate',
    current: 97.4,
    target: 95.0,
    unit: '%',
    status: 'good',
    description: 'Percentage of tasks successfully fulfilled by specialists without human intervention.',
    trend: 'up',
    history: [
      { timestamp: 'Sep 03', value: 94.0 },
      { timestamp: 'Sep 04', value: 95.2 },
      { timestamp: 'Sep 05', value: 96.1 },
      { timestamp: 'Sep 06', value: 96.8 },
      { timestamp: 'Sep 07', value: 97.0 },
      { timestamp: 'Sep 08', value: 97.1 },
      { timestamp: 'Sep 09', value: 97.4 }
    ]
  },
  {
    id: 'agent_uptime',
    department: 'Technology',
    name: 'Agent Fleet Availability',
    current: 99.8,
    target: 99.0,
    unit: '%',
    status: 'good',
    description: 'Uptime and responsiveness across 144 registered agent cards.',
    trend: 'stable',
    history: [
      { timestamp: 'Sep 03', value: 99.7 },
      { timestamp: 'Sep 04', value: 99.8 },
      { timestamp: 'Sep 05', value: 99.6 },
      { timestamp: 'Sep 06', value: 99.9 },
      { timestamp: 'Sep 07', value: 99.8 },
      { timestamp: 'Sep 08', value: 99.8 },
      { timestamp: 'Sep 09', value: 99.8 }
    ]
  },
  {
    id: 'llm_cost_per_task',
    department: 'Finance',
    name: 'Average Cost per Task',
    current: 0.038,
    target: 0.050,
    unit: '$',
    status: 'good',
    description: 'Inference and token cost per autonomously completed task.',
    trend: 'down',
    history: [
      { timestamp: 'Sep 03', value: 0.062 },
      { timestamp: 'Sep 04', value: 0.055 },
      { timestamp: 'Sep 05', value: 0.048 },
      { timestamp: 'Sep 06', value: 0.043 },
      { timestamp: 'Sep 07', value: 0.041 },
      { timestamp: 'Sep 08', value: 0.039 },
      { timestamp: 'Sep 09', value: 0.038 }
    ]
  },
  {
    id: 'escalation_rate',
    department: 'Operations',
    name: 'Escalation Rate',
    current: 2.1,
    target: 5.0,
    unit: '%',
    status: 'good',
    description: 'Percentage of dispatched tasks that escalated to management or CEO.',
    trend: 'down',
    history: [
      { timestamp: 'Sep 03', value: 4.8 },
      { timestamp: 'Sep 04', value: 4.2 },
      { timestamp: 'Sep 05', value: 3.6 },
      { timestamp: 'Sep 06', value: 3.1 },
      { timestamp: 'Sep 07', value: 2.7 },
      { timestamp: 'Sep 08', value: 2.4 },
      { timestamp: 'Sep 09', value: 2.1 }
    ]
  },
  {
    id: 'csat_satisfaction',
    department: 'Customer Success',
    name: 'Client CSAT Satisfaction',
    current: 96.4,
    target: 92.0,
    unit: '%',
    status: 'good',
    description: 'Enterprise client satisfaction score with AI deliverable accuracy.',
    trend: 'up',
    history: [
      { timestamp: 'Sep 03', value: 93.0 },
      { timestamp: 'Sep 04', value: 94.2 },
      { timestamp: 'Sep 05', value: 94.8 },
      { timestamp: 'Sep 06', value: 95.5 },
      { timestamp: 'Sep 07', value: 95.9 },
      { timestamp: 'Sep 08', value: 96.1 },
      { timestamp: 'Sep 09', value: 96.4 }
    ]
  }
];

export const modelTiers: ModelTierConfig[] = [
  {
    tier: 'fast',
    name: 'Tier 1: Fast Execution',
    costRange: '$0.075 / 1M tokens',
    primaryProviders: ['OpenCode Big Pickle', 'Gemini 3.5 Flash', 'Ollama Llama 3.1'],
    tokensProcessed: 142850000,
    totalCost: 10.71,
    requestsCount: 28410
  },
  {
    tier: 'standard',
    name: 'Tier 2: Standard Synthesis',
    costRange: '$0.30 / 1M tokens',
    primaryProviders: ['DeepSeek Chat', 'Gemini 3.5 Flash', 'Kimi K2'],
    tokensProcessed: 96420000,
    totalCost: 28.93,
    requestsCount: 12190
  },
  {
    tier: 'premium',
    name: 'Tier 3: Complex Reasoning',
    costRange: '$2.50 / 1M tokens',
    primaryProviders: ['Gemini 3.1 Pro', 'DeepSeek Coder', 'OpenAI GPT-4o'],
    tokensProcessed: 31200000,
    totalCost: 78.00,
    requestsCount: 3450
  }
];

export const initialAuditLog: AuditEntry[] = [
  {
    id: 'AUD-901',
    timestamp: '2026-09-09T10:45:12Z',
    actor: 'orchestrator',
    action: 'DISPATCH_BATCH',
    details: 'Scheduled 14 recurring workflow ticks across Technology and Data departments.',
    category: 'orchestrator'
  },
  {
    id: 'AUD-902',
    timestamp: '2026-09-09T10:20:00Z',
    actor: 'human-ceo',
    action: 'APPROVE_GATE',
    details: 'Approved Tier 3 permissions elevation for lead-backend database migration.',
    category: 'approval'
  },
  {
    id: 'AUD-903',
    timestamp: '2026-09-09T09:12:35Z',
    actor: 'orchestration-owner',
    action: 'RAISE_ESCALATION',
    details: 'Triggered ESC-401 due to lock contention in asynchronous task distributor.',
    category: 'escalation'
  },
  {
    id: 'AUD-904',
    timestamp: '2026-09-09T08:30:19Z',
    actor: 'ciso',
    action: 'SECURITY_AUDIT',
    details: 'Completed secret scanner audit: zero exposed API credentials found.',
    category: 'security'
  }
];
