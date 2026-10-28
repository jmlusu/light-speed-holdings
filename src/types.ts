import type { HonestyTone } from './data/siteContent';

export type PublicTool = 'read' | 'edit' | 'grep' | 'list' | 'bash' | 'webfetch' | 'task';
export type PublicAgentType = 'executive' | 'specialist' | 'board';

export interface PublicAgent {
  id: string;
  name: string;
  title: string;
  type: PublicAgentType;
  department: string;
  department_id: string;
  reports_to: string | null;
  mission: string;
  is_human?: boolean;
  tools?: PublicTool[];
  kpi_labels?: string[];
  decision_rights?: string[];
  responsibilities?: string[];
  technical_domain?: string;
}

export interface PublicDepartment {
  id: string;
  name: string;
  executive: string;
  mission: string;
  budget_category: string;
  headcount_target: number;
}

export interface PublicAgentRegistry {
  schema_version: string;
  generated_at: string;
  source: string;
  meta: { agents: number; departments: number };
  agents: PublicAgent[];
  departments: PublicDepartment[];
}

export interface Agent {
  name: string;
  role: string;
  type: 'Executive' | 'Specialist' | 'Manager' | 'Board';
  department: string;
  reportsTo: string;
  directReports?: string[];
  description: string;
  responsibilities: string[];
  tools: PublicTool[];
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
  media?: CatalogMedia;
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
  media?: CatalogMedia;
}

export interface ScreenshotMedia {
  kind: 'screenshot';
  src: string;
  alt: string;
  width: number;
  height: number;
  tone: HonestyTone;
}

export interface BrandMedia {
  kind: 'brand-mark';
  src: string;
  alt: '';
  width: number;
  height: number;
}

export interface DiagramMedia {
  kind: 'diagram';
  alt: string;
  tone: HonestyTone;
  component?: string;
}

export interface MetricMedia {
  kind: 'metrics';
  alt: string;
  tone: HonestyTone;
  component?: string;
}

export interface IllustrationProvenance {
  origin: 'authored' | 'generated';
  vendor?: string;
  model?: string;
  prompt?: string;
  recordedAt?: string;
}

export interface IllustrationMedia {
  kind: 'illustration';
  src: string;
  alt: string;
  width: number;
  height: number;
  tone: HonestyTone;
  generated: boolean;
  provenance?: IllustrationProvenance;
}

export type ContentMedia =
  | ScreenshotMedia
  | BrandMedia
  | DiagramMedia
  | MetricMedia
  | IllustrationMedia;

export interface ContentMediaSet {
  hero?: ContentMedia;
  gallery?: ContentMedia[];
  thumbnail?: ContentMedia;
}
