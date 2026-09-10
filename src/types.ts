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
