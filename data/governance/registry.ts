/**
 * Governance Registry — Canonical Source of Truth
 *
 * Source: Directive §24 + siteContent.ts + company-registry.yaml
 * Directive §22 — Single source for all governance framework details
 */

export interface HITLTier {
  tier: number;
  name: string;
  description: string;
  approverRole: string;
  maxAutoApproveMinutes: number;
  actions: string[];
  riskLevels: ('low' | 'medium' | 'high' | 'critical')[];
}

export interface GovernanceGate {
  id: string;
  name: string;
  description: string;
  requiredFor: 'all-engagements' | 'client-facing' | 'internal';
  approverRoles: string[];
  documentation: string[];
}

export interface AuditTrailSpec {
  format: 'JSONL';
  sealing: 'SHA-256';
  structure: string[];
  retention: string;
  queryable: boolean;
  merkleTrees: boolean;
}

export interface ApprovalExpiryPolicy {
  tier: number;
  maxPendingMinutes: number;
  sweepFrequency: string;
  onExpiry: 'reject' | 'escalate' | 'requeue';
}

export interface RiskLevel {
  level: 'low' | 'medium' | 'high' | 'critical';
  likelihood: number;  // 1-5
  impact: number;      // 1-5
  approvalTier: number;
  examples: string[];
}

export interface HumanAuthorityStatement {
  short: string;
  full: string;
  principle: string;
}

export interface GovernanceFramework {
  hitlMatrix: HITLTier[];
  governanceGates: GovernanceGate[];
  auditTrail: AuditTrailSpec;
  approvalExpiry: ApprovalExpiryPolicy[];
  riskMatrix: RiskLevel[];
  humanAuthority: HumanAuthorityStatement;
}

export const governanceFramework: GovernanceFramework = {
  hitlMatrix: [
    {
      tier: 1,
      name: 'Auto (Autonomous)',
      description: 'Low-risk, repetitive tasks fully autonomous. No human intervention required.',
      approverRole: 'System (auto-approved)',
      maxAutoApproveMinutes: 0,
      actions: [
        'Classification (document, risk, intent)',
        'Extraction (data, entities, key-values)',
        'Summarization (reports, transcripts, articles)',
        'Embedding generation',
        'Routine monitoring & alerting',
        'Cache invalidation',
        'Log rotation',
      ],
      riskLevels: ['low'],
    },
    {
      tier: 2,
      name: 'Lead (Specialist Approval)',
      description: 'Medium-risk standard workflows. Specialist lead reviews and approves.',
      approverRole: 'Department Lead / Specialist',
      maxAutoApproveMinutes: 60,
      actions: [
        'Standard document generation',
        'Data pipeline execution',
        'WhatsApp message responses (FAQ)',
        'Dashboard updates',
        'Report compilation',
        'Code review (non-security)',
        'Content publishing (approved templates)',
      ],
      riskLevels: ['medium'],
    },
    {
      tier: 3,
      name: 'Dual (Two Approvers Required)',
      description: 'High-risk actions requiring two independent approvals from different domains.',
      approverRole: 'Two Leads from different departments (e.g., CISO + CTO, Legal + Finance)',
      maxAutoApproveMinutes: 30,
      actions: [
        'Security configuration changes',
        'Database schema migrations',
        'External API integrations',
        'Client data processing workflows',
        'Financial transactions > threshold',
        'Compliance report submissions',
        'Model tier upgrades',
      ],
      riskLevels: ['high'],
    },
    {
      tier: 4,
      name: 'Executive (C-Level Approval)',
      description: 'Critical-risk actions requiring named executive approval.',
      approverRole: 'Relevant C-Level Executive (CFO, CLO, CTO, CMO, etc.)',
      maxAutoApproveMinutes: 15,
      actions: [
        'Budget approvals > $10K',
        'Contract signing',
        'Regulatory filings',
        'Major deployment authorizations',
        'Data processing agreement execution',
        'Strategic partnership agreements',
        'Infrastructure scaling decisions',
      ],
      riskLevels: ['critical'],
    },
    {
      tier: 5,
      name: 'CEO (Human CEO Approval)',
      description: 'Highest-risk actions requiring Human CEO (Jack Mlusu) personal approval.',
      approverRole: 'Human CEO (Jack Mlusu)',
      maxAutoApproveMinutes: 5,
      actions: [
        'Company strategy changes',
        'Major investment decisions',
        'Board-level commitments',
        'Crisis response authorization',
        'Ethics board escalations',
        'Public statement approvals',
        'Organizational restructuring',
      ],
      riskLevels: ['critical'],
    },
  ],
  governanceGates: [
    {
      id: 'G1',
      name: 'Contract Review',
      description: 'Legal review of engagement terms, scope, liability, and IP provisions.',
      requiredFor: 'all-engagements',
      approverRoles: ['CLO', 'Legal Owner'],
      documentation: ['Engagement letter', 'MSA', 'SOW', 'Liability caps'],
    },
    {
      id: 'G2',
      name: 'Data Processing Agreement',
      description: 'DPA execution covering data sovereignty, encryption, retention, and cross-border transfer.',
      requiredFor: 'all-engagements',
      approverRoles: ['CLO', 'Data Privacy Officer', 'CISO'],
      documentation: ['DPA', 'Data flow map', 'Encryption spec', 'Retention schedule'],
    },
    {
      id: 'G3',
      name: 'Compliance Review',
      description: 'Regulatory compliance assessment for sector, jurisdiction, and data type.',
      requiredFor: 'all-engagements',
      approverRoles: ['Security Compliance Lead', 'CISO', 'CLO'],
      documentation: ['Compliance matrix', 'Regulatory mapping', 'Gap analysis', 'Remediation plan'],
    },
    {
      id: 'G4',
      name: 'Security Assessment',
      description: 'Infrastructure, application, and operational security review.',
      requiredFor: 'all-engagements',
      approverRoles: ['CISO', 'Security Architect', 'Platform Reliability Engineer'],
      documentation: ['Threat model', 'Penetration test', 'Vulnerability scan', 'Incident response plan'],
    },
  ],
  auditTrail: {
    format: 'JSONL',
    sealing: 'SHA-256',
    structure: [
      'timestamp (ISO 8601)',
      'actor (agent ID or human)',
      'action_type',
      'prompt_hash',
      'tool_invocations[]',
      'outputs_hash',
      'approval_chain[]',
      'risk_level',
      'sha256_seal',
      'merkle_root',
    ],
    retention: '7 years minimum (configurable per engagement)',
    queryable: true,
    merkleTrees: true,
  },
  approvalExpiry: [
    { tier: 1, maxPendingMinutes: 0, sweepFrequency: 'continuous', onExpiry: 'reject' },
    { tier: 2, maxPendingMinutes: 60, sweepFrequency: 'every 5 minutes', onExpiry: 'escalate' },
    { tier: 3, maxPendingMinutes: 30, sweepFrequency: 'every 2 minutes', onExpiry: 'escalate' },
    { tier: 4, maxPendingMinutes: 15, sweepFrequency: 'every minute', onExpiry: 'escalate' },
    { tier: 5, maxPendingMinutes: 5, sweepFrequency: 'every 30 seconds', onExpiry: 'escalate' },
  ],
  riskMatrix: [
    {
      level: 'low',
      likelihood: 1,
      impact: 1,
      approvalTier: 1,
      examples: ['Document classification', 'Log aggregation', 'Cache refresh'],
    },
    {
      level: 'low',
      likelihood: 2,
      impact: 1,
      approvalTier: 1,
      examples: ['Routine summarization', 'Standard extraction'],
    },
    {
      level: 'medium',
      likelihood: 2,
      impact: 2,
      approvalTier: 2,
      examples: ['Report generation', 'Dashboard update', 'FAQ response'],
    },
    {
      level: 'medium',
      likelihood: 3,
      impact: 2,
      approvalTier: 2,
      examples: ['Data pipeline run', 'Content publish', 'Code review'],
    },
    {
      level: 'high',
      likelihood: 3,
      impact: 3,
      approvalTier: 3,
      examples: ['External API call', 'Client data processing', 'Compliance report'],
    },
    {
      level: 'high',
      likelihood: 4,
      impact: 3,
      approvalTier: 3,
      examples: ['Database migration', 'Security config change', 'Financial transaction'],
    },
    {
      level: 'critical',
      likelihood: 4,
      impact: 4,
      approvalTier: 4,
      examples: ['Regulatory filing', 'Contract execution', 'Major deployment'],
    },
    {
      level: 'critical',
      likelihood: 5,
      impact: 5,
      approvalTier: 5,
      examples: ['Strategy change', 'Crisis response', 'Board commitment'],
    },
  ],
  humanAuthority: {
    short: 'AI executes. Humans decide.',
    full: 'Agents execute. The Human CEO owns operational intent and final decision authority.',
    principle: 'No agent action with external consequences proceeds without human approval at the appropriate tier. The Human CEO is the ultimate accountable party for all agent operations.',
  },
};

export default governanceFramework;
