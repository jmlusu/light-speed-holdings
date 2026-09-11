export interface Agent {
  name: string;
  role: string;
  type: 'Executive' | 'Specialist' | 'Manager' | 'Board';
  department: string;
  reportsTo: string;
  directReports?: string[];
  description: string;
  responsibilities: string[];
  guidelines?: string;
  tools: string[];
  permission: string;
}

export interface Department {
  id: string;
  name: string;
  executive: string;
  mission: string;
  budget_category: string;
  headcount_target: number;
}

export type TaskStatus = 'pending' | 'in_progress' | 'review' | 'completed' | 'escalated';
export type TaskPriority = 'P0' | 'P1' | 'P2' | 'P3';

export interface TaskItem {
  id: string;
  title: string;
  instruction: string;
  status: TaskStatus;
  priority: TaskPriority;
  sender_id: string;
  receiver_id: string;
  department: string;
  created_at: string;
  updated_at: string;
  result?: string;
}

export type ApprovalTier = 'Tier 1 (Auto)' | 'Tier 2 (Single)' | 'Tier 3 (Dual)' | 'Tier 4 (Executive)' | 'Tier 5 (CEO)';

export interface ApprovalRequest {
  id: string;
  task_id: string;
  title: string;
  tier: ApprovalTier;
  requested_by: string;
  approver_role: string;
  status: 'pending' | 'approved' | 'rejected';
  reason: string;
  amount?: string;
  created_at: string;
  notes?: string;
}

export interface EscalationItem {
  id: string;
  task_id: string;
  title: string;
  agent_id: string;
  department: string;
  reason: string;
  level: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'investigating' | 'resolved';
  created_at: string;
  resolved_at?: string;
  resolution_notes?: string;
}

export interface KPIDefinition {
  id: string;
  department: string;
  name: string;
  current: number;
  target: number | null;
  unit: string;
  status: 'good' | 'amber' | 'critical' | 'info';
  description: string;
  trend: 'up' | 'down' | 'stable';
  history: { timestamp: string; value: number }[];
}

export interface ModelTierConfig {
  tier: 'fast' | 'standard' | 'premium';
  name: string;
  costRange: string;
  primaryProviders: string[];
  tokensProcessed: number;
  totalCost: number;
  requestsCount: number;
}

export interface AuditEntry {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  details: string;
  category: 'orchestrator' | 'executor' | 'approval' | 'escalation' | 'security';
}

export type HonestyBadge = 
  | 'Fieldable in 2026'
  | 'In active development'
  | 'In pilot'
  | 'In pilot (composing evidence)'
  | 'In pilot (proposed)'
  | 'Proven in-house'
  | 'Live proof'
  | 'Published';

export interface CatalogOfferDeliverable {
  id: string;
  name: string;
  description: string;
  priceMwk: string;
  priceUsd: string;
  turnaround: string;
  blocked?: boolean;
  blockedReason?: string;
  hostingFee?: string;
}

export interface CatalogOfferFamily {
  id: string;
  letter: 'A' | 'B' | 'C' | 'D' | 'E';
  title: string;
  tagline: string;
  description: string;
  honestyBadge: HonestyBadge;
  targetClients: string[];
  governanceNote: string;
  pricingNote: string;
  deliverables: CatalogOfferDeliverable[];
}

export interface EnterpriseCapability {
  name: string;
  description: string;
  status: string;
}

export interface CatalogIndustryVertical {
  id: string;
  title: string;
  description: string;
  keyUseCases: string[];
  honestyBadge: HonestyBadge;
  honestyNote: string;
  iconName: string;
}

export interface CatalogPlatformScenario {
  id: string; // FOW-01..FOW-08
  code: string;
  title: string;
  subtitle: string;
  description: string;
  honestyBadge: HonestyBadge;
  targetAudience: string;
}

export interface CatalogProofPoint {
  id: string;
  title: string;
  category: 'SME Proof' | 'Meta Case Study' | 'Pilot in Development' | 'Policy Reference';
  honestyBadge: HonestyBadge;
  badgeType: 'live' | 'proven' | 'pilot' | 'policy';
  description: string;
  whatItMonitorsOrProves: string;
  whyItMatters: string;
}

export interface CatalogPolicyItem {
  id: string;
  title: string;
  honestyBadge: HonestyBadge;
  summary: string;
  description: string;
}
