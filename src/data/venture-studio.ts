/* AI Venture Studio content.
 *
 * Source of truth: docs/venture-studio/03-operating-model.md and
 * docs/venture-studio/05-kpi-scorecard.md. The scorecard numbers are
 * blueprint TARGETS from the strategy deliverable, not measured results -
 * they are labelled as targets on the page for that reason.
 */

export interface StudioModel {
  id: string;
  title: string;
  definition: string;
  failureMode: string;
}

export interface StudioPillar {
  id: string;
  title: string;
  owns: string;
  sharedAssets: string;
}

export interface PortfolioArchetype {
  id: 'A' | 'B' | 'C';
  title: string;
  valueProp: string;
  stackPull: string;
}

export interface StudioMetric {
  id: string;
  metric: string;
  definition: string;
  target: string;
}

export interface StageGate {
  phase: string;
  window: string;
  goal: string;
  exitGate: string;
}

export const studioModels: StudioModel[] = [
  {
    id: 'ai-native-org',
    title: 'AI-Native Organisation',
    definition:
      'Agents and autonomous systems sit at the operational core. Workflows prioritise agentic workflows over static pipelines; agents execute under human oversight.',
    failureMode:
      'Removing AI collapses the operational system - headcount cannot absorb the load at the same cost or speed.',
  },
  {
    id: 'venture-studio',
    title: 'AI-Company Builder (Venture Studio)',
    definition:
      'A repeatable engine that co-founds, validates, builds and launches AI-native entities using shared technical infrastructure, agent stacks, data pipelines and go-to-market.',
    failureMode:
      'Each venture rebuilds the stack: capital burn, inconsistent governance and no compounding learning.',
  },
];

export const studioPillars: StudioPillar[] = [
  {
    id: 'strategic-validation',
    title: 'Strategic Validation',
    owns: 'Thesis pressure-test, buyer discovery, kill/continue gates.',
    sharedAssets: 'Opportunity scorecards and the sector matrix.',
  },
  {
    id: 'agent-orchestration',
    title: 'Agent Orchestration & Modular Core',
    owns: 'MessageBus, model router, human-in-the-loop approval engine, memory, tool sandbox and registry loader.',
    sharedAssets: 'Canonical agent cards, workflow definitions and the audit chain.',
  },
  {
    id: 'shared-services',
    title: 'Shared Services & GTM',
    owns: 'Pricing templates, onboarding SOPs, proof and evidence pack, Pharos thought leadership and dashboard KPIs.',
    sharedAssets: 'The honesty policy, claim rules and brand tokens.',
  },
];

export const portfolioArchetypes: PortfolioArchetype[] = [
  {
    id: 'A',
    title: 'Enterprise Agent',
    valueProp: 'Department-scale agent workforce inside a client organisation.',
    stackPull: 'Registry, human-in-the-loop gates, audit and dashboards.',
  },
  {
    id: 'B',
    title: 'B2B AI Workflow',
    valueProp: 'A repeatable multi-step process: procurement, reporting, reconciliation.',
    stackPull: 'Workflow engine, durable state and connectors.',
  },
  {
    id: 'C',
    title: 'Sovereign Data',
    valueProp: 'In-country or on-premises constrained deployment.',
    stackPull: 'Local models, offline PWA and data residency controls.',
  },
];

/** Blueprint targets from the studio scorecard (Part 5). Not measured results. */
export const studioMetrics: StudioMetric[] = [
  {
    id: 'atc',
    metric: 'Agentic Task Completion (ATC) Rate',
    definition: 'Share of end-to-end agentic tasks completed without manual intervention.',
    target: '> 90%',
  },
  {
    id: 'velocity',
    metric: 'Velocity to MVP',
    definition: 'Days from Phase 1 thesis approval to Phase 3 customer deployment.',
    target: '< 60 days',
  },
  {
    id: 'correction',
    metric: 'Manual Correction Ratio',
    definition: 'Human override or correction events per 1,000 executed agent actions.',
    target: 'Baseline first, then reduce',
  },
  {
    id: 'capital-efficiency',
    metric: 'Capital Efficiency per Spin-Out',
    definition: 'Output per capital unit against a traditional seed benchmark.',
    target: '3-5x capital efficiency',
  },
];

export const stageGates: StageGate[] = [
  {
    phase: '1. Discovery',
    window: 'Weeks 1-2',
    goal: 'Problem discovery and thesis across high-value operational bottlenecks.',
    exitGate: 'Written thesis, sector fit and a named owner.',
  },
  {
    phase: '2. Validation',
    window: 'Weeks 3-6',
    goal: 'Proof of concept plus structured buyer discovery.',
    exitGate: 'Design-partner LOIs or paid pilot intent; PoC demo on the real data shape.',
  },
  {
    phase: '3. Build',
    window: 'Weeks 7-14',
    goal: 'Minimum viable agent on shared studio infrastructure, deployed to design partners.',
    exitGate: 'ATC baseline recorded, human-in-the-loop gates live, correction ratio instrumented.',
  },
  {
    phase: '4. Scale',
    window: 'Month 4+',
    goal: 'Spin-out with dedicated leadership and institutional capitalisation.',
    exitGate: 'Spin-out scorecard green on capital efficiency, velocity and ATC.',
  },
];

export default {
  studioModels,
  studioPillars,
  portfolioArchetypes,
  studioMetrics,
  stageGates,
};
