/* LightSpeed Holdings — Public Agent Registry
   Canonical source: company/agent-registry.json (90 agents)
   This file exposes ONLY approved public fields per MASTER_SPEC §28.
   DO NOT expose: prompts, credentials, internal endpoints, private tool config,
   private memory, security controls, internal orchestration instructions. */

import type { HonestyTone } from './siteContent';

export type AgentType = 'Executive' | 'Specialist';
export type AgentPermission = 'Execute' | 'Read' | 'Advise';

export interface PublicAgent {
  name: string;
  role: string;
  type: AgentType;
  department: string;
  description: string;
  publicResponsibilities: string[];
  capabilities: string[];
  modelTier?: 'standard' | 'premium';
  technicalDomain?: string;
  status: 'Active' | 'In Development' | 'Deprecated';
  honestyStatus: HonestyTone;
  reportsTo: string;
}

/** Transform full agent registry into public-safe records */
export function toPublicAgent(agent: any): PublicAgent {
  return {
    name: agent.name,
    role: agent.role,
    type: agent.type,
    department: agent.department,
    description: agent.description,
    publicResponsibilities: (agent.responsibilities || []).slice(0, 3).map((r: string) => 
      r.replace(/\(GAP-\d+\)|\(ticket #\d+\)|\(issue #\d+\)/gi, '').trim()
    ),
    capabilities: agent.tools || [],
    modelTier: agent.model_tier,
    technicalDomain: agent.technical_domain,
    status: 'Active',
    honestyStatus: 'proven',
    reportsTo: agent.reportsTo,
  };
}

/** Department display order for public registry */
export const DEPARTMENT_ORDER = [
  'Executive',
  'Technology',
  'AI Research',
  'Operations',
  'Security',
  'Product',
  'Marketing',
  'Sales',
  'Finance',
  'Data',
  'Legal',
  'People',
  'Business Development',
  'QA',
  'Customer Success',
];

/** Department colors for visual grouping */
export const DEPARTMENT_COLORS: Record<string, { light: string; dark: string }> = {
  'Executive': { light: 'bg-ls-red/10 text-ls-red border-ls-red/30', dark: 'bg-ls-red/10 text-ls-red border-ls-red/30' },
  'Technology': { light: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/30', dark: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/30' },
  'AI Research': { light: 'bg-ls-red/10 text-ls-red border-ls-red/30', dark: 'bg-ls-red/10 text-ls-red border-ls-red/30' },
  'Operations': { light: 'bg-ls-green/10 text-ls-green border-ls-green/30', dark: 'bg-ls-green/10 text-ls-green border-ls-green/30' },
  'Security': { light: 'bg-ls-orange/10 text-ls-orange border-ls-orange/30', dark: 'bg-ls-orange/10 text-ls-orange border-ls-orange/30' },
  'Product': { light: 'bg-ls-purple/10 text-ls-purple border-ls-purple/30', dark: 'bg-ls-purple/10 text-ls-purple border-ls-purple/30' },
  'Marketing': { light: 'bg-ls-pink/10 text-ls-pink border-ls-pink/30', dark: 'bg-ls-pink/10 text-ls-pink border-ls-pink/30' },
  'Sales': { light: 'bg-ls-blue/10 text-ls-blue border-ls-blue/30', dark: 'bg-ls-blue/10 text-ls-blue border-ls-blue/30' },
  'Finance': { light: 'bg-ls-emerald/10 text-ls-emerald border-ls-emerald/30', dark: 'bg-ls-emerald/10 text-ls-emerald border-ls-emerald/30' },
  'Data': { light: 'bg-ls-indigo/10 text-ls-indigo border-ls-indigo/30', dark: 'bg-ls-indigo/10 text-ls-indigo border-ls-indigo/30' },
  'Legal': { light: 'bg-ls-slate/10 text-ls-slate border-ls-slate/30', dark: 'bg-ls-slate/10 text-ls-slate border-ls-slate/30' },
  'People': { light: 'bg-ls-rose/10 text-ls-rose border-ls-rose/30', dark: 'bg-ls-rose/10 text-ls-rose border-ls-rose/30' },
  'Business Development': { light: 'bg-ls-amber/10 text-ls-amber border-ls-amber/30', dark: 'bg-ls-amber/10 text-ls-amber border-ls-amber/30' },
  'QA': { light: 'bg-ls-violet/10 text-ls-violet border-ls-violet/30', dark: 'bg-ls-violet/10 text-ls-violet border-ls-violet/30' },
  'Customer Success': { light: 'bg-ls-teal/10 text-ls-teal border-ls-teal/30', dark: 'bg-ls-teal/10 text-ls-teal border-ls-teal/30' },
};

/** Agent type badges */
export const TYPE_BADGES = {
  'Executive': { light: 'bg-ls-red/10 text-ls-red border-ls-red/30', dark: 'bg-ls-red/10 text-ls-red border-ls-red/30', label: 'EXEC' },
  'Specialist': { light: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/30', dark: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/30', label: 'SPEC' },
};

/** Honesty status labels */
export const HONESTY_LABELS: Record<HonestyTone, { label: string; light: string; dark: string }> = {
  'proven': { label: 'Proven in-house', light: 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan', dark: 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan' },
  'pilot': { label: 'In pilot', light: 'border-ls-red/40 bg-ls-red/10 text-ls-red', dark: 'border-ls-red/40 bg-ls-red/10 text-ls-red' },
  'fieldable': { label: 'Fieldable in 2026', light: 'border-ls-amber/40 bg-ls-amber/10 text-ls-amber', dark: 'border-ls-amber/40 bg-ls-amber/10 text-ls-amber' },
  'development': { label: 'In development', light: 'border-ls-slate/40 bg-ls-slate/10 text-ls-slate', dark: 'border-ls-slate/40 bg-ls-slate/10 text-ls-slate' },
};