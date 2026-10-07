/**
 * Generate Public Agent Registry
 *
 * Reads company-registry.yaml and outputs data/agents/registry.generated.ts
 * with only public-safe agent data.
 *
 * Run: npx tsx scripts/generate-public-agent-registry.ts
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';

interface InternalAgent {
  id: string;
  name: string;
  title: string;
  description: string;
  type: string;
  department: string;
  reports_to: string;
  direct_reports: string[];
  responsibilities: string[];
  guidelines: string;
  tools: string[];
  model_tier?: string;
  approval_level: string;
  escalation_path: string[];
  kpis: string[];
  decision_rights: string[];
  workflows: string[];
  inputs: string[];
  outputs: string[];
}

interface InternalDepartment {
  id: string;
  name: string;
  executive: string;
  mission: string;
  budget_category: string;
  headcount_target: number;
}

interface CompanyRegistry {
  company: {
    name: string;
    agents: InternalAgent[];
  };
}

interface InternalDepartment {
  id: string;
  name: string;
  executive: string;
  mission: string;
  budget_category: string;
  headcount_target: number;
}

interface PublicAgent {
  id: string;
  name: string;
  title: string;
  description: string;
  type: 'executive' | 'specialist' | 'board';
  department: string;
  reportsTo: string;
  mission: string;
  responsibilities: string[];
  tools: string[];
  approvalLevel: string;
  modelTier?: 'fast' | 'standard' | 'premium';
  kpis: string[];
  decisionRights: string[];
}

interface PublicDepartment {
  id: string;
  name: string;
  executive: string;
  mission: string;
  budgetCategory: string;
  headcountTarget: number;
  agentCount: number;
}

interface PublicAgentRegistry {
  agents: PublicAgent[];
  departments: PublicDepartment[];
  totals: {
    totalRoles: number;
    aiAgents: number;
    humanCeo: number;
    departments: number;
    executives: number;
    specialists: number;
    boardMembers: number;
  };
  generatedAt: string;
  source: string;
}

function toPublicAgent(agent: InternalAgent): PublicAgent {
  const typeMap: Record<string, 'executive' | 'specialist' | 'board'> = {
    executive: 'executive',
    specialist: 'specialist',
    board: 'board',
  };

  return {
    id: agent.id,
    name: agent.name,
    title: agent.title,
    description: agent.description,
    type: typeMap[agent.type] ?? 'specialist',
    department: agent.department,
    reportsTo: agent.reports_to,
    mission: agent.mission || '',
    responsibilities: agent.responsibilities || [],
    tools: agent.tools || ['read', 'edit', 'bash'],
    approvalLevel: agent.approval_level,
    modelTier: agent.model_tier as 'fast' | 'standard' | 'premium' | undefined,
    kpis: agent.kpis || [],
    decisionRights: agent.decision_rights || [],
  };
}

function toPublicDepartment(dept: InternalDepartment, agentCount: number): PublicDepartment {
  return {
    id: dept.id,
    name: dept.name,
    executive: dept.executive,
    mission: dept.mission,
    budgetCategory: dept.budget_category,
    headcountTarget: dept.headcount_target,
    agentCount,
  };
}

async function main() {
  const registryPath = path.resolve('company-registry.yaml');
  const outputPath = path.resolve('data/agents/registry.generated.ts');

  console.log('Reading company-registry.yaml...');
  const fileContent = fs.readFileSync(registryPath, 'utf-8');
  const registry = yaml.parse(fileContent) as CompanyRegistry;

  console.log(`Found ${registry.company.agents.length} agents`);

  // Transform agents
  const publicAgents = registry.company.agents.map(toPublicAgent);

  // Count agents per department
  const agentCounts: Record<string, number> = {};
  for (const agent of publicAgents) {
    agentCounts[agent.department] = (agentCounts[agent.department] || 0) + 1;
  }

  // Build departments from unique department names in agents
  const departmentNames = [...new Set(publicAgents.map(a => a.department))];

  // Department metadata (from directive and registry knowledge)
  const departmentMetadata: Record<string, { executive: string; mission: string; budget_category: string; headcount_target: number }> = {
    'Executive': { executive: 'human_ceo', mission: 'Set company vision, strategy, and culture. Make final decisions on high-stakes matters.', budget_category: 'Executive', headcount_target: 2 },
    'Technology': { executive: 'cto', mission: 'Architect robust AI agent systems. Review and merge code. Ensure system scalability and security.', budget_category: 'Technology', headcount_target: 10 },
    'Operations': { executive: 'coo', mission: 'Optimize internal workflows. Manage agent resource allocation.', budget_category: 'Operations', headcount_target: 8 },
    'AI Research': { executive: 'caio', mission: 'Evaluate and integrate new LLM models. Fine-tune prompts for maximum agent efficacy.', budget_category: 'AI Research', headcount_target: 8 },
    'Finance': { executive: 'cfo', mission: 'Track and optimize costs. Prepare financial reports. Manage budgets.', budget_category: 'Finance', headcount_target: 4 },
    'Product': { executive: 'cpo', mission: 'Define product vision and roadmap. Prioritize features based on user impact.', budget_category: 'Product', headcount_target: 6 },
    'Marketing': { executive: 'cmo', mission: 'Own external website. Develop marketing strategy. Drive demand generation.', budget_category: 'Marketing', headcount_target: 6 },
    'People': { executive: 'hr', mission: 'Define talent acquisition strategy. Design culture initiatives. Manage performance reviews.', budget_category: 'People', headcount_target: 4 },
    'Security': { executive: 'ciso', mission: 'Define security strategy. Lead incident response. Ensure compliance.', budget_category: 'Security', headcount_target: 8 },
    'IT': { executive: 'cio', mission: 'Manage IT infrastructure. Oversee internal tools. Ensure data management.', budget_category: 'IT', headcount_target: 4 },
    'Data': { executive: 'cdo', mission: 'Define data strategy. Oversee analytics. Ensure data quality.', budget_category: 'Data', headcount_target: 4 },
    'Legal': { executive: 'clo', mission: 'Review contracts. Ensure regulatory compliance. Protect IP.', budget_category: 'Legal', headcount_target: 4 },
    'Strategy': { executive: 'cso', mission: 'Develop corporate strategy. Conduct market analysis. Evaluate partnerships.', budget_category: 'Strategy', headcount_target: 3 },
    'Customer Success': { executive: 'customer_success', mission: 'Own customer onboarding, retention, expansion. Track NPS/CSAT.', budget_category: 'Customer Success', headcount_target: 4 },
    'Sales': { executive: 'sales', mission: 'Own sales pipeline and revenue targets. Manage customer acquisition.', budget_category: 'Sales', headcount_target: 4 },
    'Business Development': { executive: 'head_of_business_development', mission: 'Own outbound partnerships. Ecosystem alliances. Integration deals.', budget_category: 'Business Development', headcount_target: 3 },
    'Consulting': { executive: 'consulting_lead', mission: 'Own Foaster-style AI consulting engagement lifecycle.', budget_category: 'Consulting', headcount_target: 6 },
    'QA': { executive: 'qa_lead', mission: 'Own QA strategy, release quality gates, red/green baseline.', budget_category: 'QA', headcount_target: 4 },
    'Board': { executive: 'board_chair', mission: 'Preside over board meetings. Set agendas. Ensure governance standards.', budget_category: 'Board', headcount_target: 7 },
  };

  // Transform departments
  const publicDepartments = departmentNames.map(deptName => {
    const meta = departmentMetadata[deptName] || { executive: '', mission: '', budget_category: '', headcount_target: 0 };
    return toPublicDepartment({
      id: deptName.toLowerCase().replace(/\s+/g, '-'),
      name: deptName,
      executive: meta.executive,
      mission: meta.mission,
      budget_category: meta.budget_category,
      headcount_target: meta.headcount_target,
    }, agentCounts[deptName] || 0);
  });

  // Calculate totals
  const aiAgents = publicAgents.filter(a => a.id !== 'human_ceo').length;
  const humanCeo = publicAgents.filter(a => a.id === 'human_ceo').length;
  const executives = publicAgents.filter(a => a.type === 'executive').length;
  const specialists = publicAgents.filter(a => a.type === 'specialist').length;
  const boardMembers = publicAgents.filter(a => a.type === 'board').length;

  const registryOutput: PublicAgentRegistry = {
    agents: publicAgents,
    departments: publicDepartments,
    totals: {
      totalRoles: publicAgents.length,
      aiAgents,
      humanCeo,
      departments: publicDepartments.length,
      executives,
      specialists,
      boardMembers,
    },
    generatedAt: new Date().toISOString(),
    source: 'company-registry.yaml',
  };

  // Generate TypeScript file
  const tsContent = `/**
 * Public Agent Registry — Generated from company-registry.yaml
 *
 * DO NOT EDIT MANUALLY — Run \`npx tsx scripts/generate-public-agent-registry.ts\`
 *
 * Only exposes public-safe data. Never exposes:
 * - Secrets / internal credentials
 * - Internal memory / audit data
 * - Private client data
 * - Internal prompts
 * - Private operational logs
 * - Full internal agent configurations
 */

import type { PublicAgent, PublicDepartment, PublicAgentRegistry } from './registry';

export const publicAgentRegistry: PublicAgentRegistry = ${JSON.stringify(registryOutput, null, 2)};

export default publicAgentRegistry;
`;

  fs.writeFileSync(outputPath, tsContent);
  console.log(`Generated ${outputPath}`);
  console.log(`Total roles: ${registryOutput.totals.totalRoles}`);
  console.log(`AI Agents: ${registryOutput.totals.aiAgents}`);
  console.log(`Human CEO: ${registryOutput.totals.humanCeo}`);
  console.log(`Departments: ${registryOutput.totals.departments}`);
}

main().catch(console.error);
