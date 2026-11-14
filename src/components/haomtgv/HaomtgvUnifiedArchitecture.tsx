import React, { useState } from 'react';
import {
  Brain,
  Bot,
  GitBranch,
  HardDrive,
  Wrench,
  ShieldCheck,
  TrendingUp,
  ArrowDown,
  ArrowRight,
  ArrowUp,
  Shield,
  Lock,
  CheckCircle2,
  FileCheck,
  Compass,
  Zap,
  Activity,
  Layers,
  Sparkles,
  type LucideIcon,
} from 'lucide-react';
import { Icon3D, Icon3DName } from '../common';

export interface ArchitectureDimension {
  id: string;
  letter: 'H' | 'A' | 'O' | 'M' | 'T' | 'G' | 'V';
  title: string;
  role: string;
  tagline: string;
  corePrinciple: string;
  executiveSummary: string;
  Icon: LucideIcon;
  icon3d: Icon3DName;
  accent: 'cyan' | 'red';
  inputs: string[];
  outputs: string[];
  operationalScope: string[];
  governanceInterlock: string;
  systemExample: string;
  metrics: { label: string; value: string }[];
  connections: string[];
}

export const ARCHITECTURE_DIMENSIONS: ArchitectureDimension[] = [
  {
    id: 'human',
    letter: 'H',
    title: 'Human Authority',
    role: 'Sovereign Intent & Final Decision Authority',
    tagline: 'Machines execute, humans approve. Accountability cannot be delegated.',
    corePrinciple:
      'Human intent establishes operational boundaries, ethical baselines, and capital allocations. Autonomous agents propose; human directors decide what ships.',
    executiveSummary:
      'Human leadership sits at the sovereign pinnacle of the HAOMTGV architecture. Strategy, risk tolerance, and fiduciary accountability originate solely with human leadership. Rather than replacing human operators, the system augments executive judgment with verifiable intelligence while reserving all high-impact decision rights.',
    Icon: Brain,
    icon3d: 'users',
    accent: 'cyan',
    inputs: [
      'Strategic corporate directives and commercial priorities',
      'Capital allocation, expenditure caps, and risk tolerances',
      'Ethical guardrails and regulatory compliance mandates',
      'Executive sign-off on Tier 2 through Tier 5 decision gates',
    ],
    outputs: [
      'Validated strategic intent passed to Orchestration',
      'Authorized budget and system operating boundaries',
      'Cryptographically signed decision approvals',
      'Operational exception guidance and policy refinements',
    ],
    operationalScope: [
      'Strategic priority setting and problem framing',
      'Human-in-the-loop sign-off for critical workflows',
      'Organizational ethics, accountability, and governance review',
      'Sovereign veto power over all automated recommendations',
    ],
    governanceInterlock:
      'Tied directly to Tier 4 (Strategic Authority) and Tier 5 (Absolute Sovereign Control). Irreversible production releases and financial commitments require multi-factor human authorization.',
    systemExample:
      'Chief Executive Officer and Lead Architect authorize the production deployment manifest and budget allocations before agent automation initiates live transactions.',
    metrics: [
      { label: 'Decision Authority', value: '100% Human' },
      { label: 'Sovereign Veto', value: 'Absolute' },
      { label: 'Governance Tiers', value: 'Tiers 4 & 5' },
    ],
    connections: ['orchestration', 'governance', 'value'],
  },
  {
    id: 'agents',
    letter: 'A',
    title: 'Configurable Agents',
    role: 'Bounded Operational Execution',
    tagline: 'Specialized roles scaling from 1 to N+ agents, bounded by strict contracts.',
    corePrinciple:
      'Agents operate as deterministic, role-specialized units with explicit system prompts, tool permissions, and risk tiers. General-purpose, unbounded chatbots are strictly barred.',
    executiveSummary:
      'LightSpeed deploys configurable AI agent teams engineered to scale dynamically from a single focused agent to an enterprise fleet of N+ agents. Each agent functions within a tightly sandboxed role, such as schema validator, data transformation pipeline, or code compliance reviewer, executing scoped workflows with zero authority to elevate privileges or modify system rules.',
    Icon: Bot,
    icon3d: 'intelligence',
    accent: 'cyan',
    inputs: [
      'Directed task assignments from the Orchestration engine',
      'Contextual state retrieved from persistent Memory',
      'Structured tool interfaces and approved API endpoints',
      'Strict operational constraints defined by Governance',
    ],
    outputs: [
      'Structured draft artifacts, code diffs, and data syntheses',
      'Proposed operational recommendations with confidence intervals',
      'Machine-readable telemetry logs and execution metadata',
      'Escalation requests for human sign-off on high-risk boundaries',
    ],
    operationalScope: [
      'Role-bounded task execution across specialized domains',
      'Automated code generation, test authoring, and documentation',
      'Multi-source research synthesis and structured dataset analysis',
      'Continuous anomaly detection and SLA tracking',
    ],
    governanceInterlock:
      'Constrained by Tier 1 (Auto-execution) and Tier 2 (Supervised Recommendation). Agents cannot alter their own system prompts, bypass sandboxes, or access production credentials directly.',
    systemExample:
      'An Architecture Auditor Agent inspects pull requests against TypeScript strictness rules and security guidelines, generating a detailed compliance report for human review.',
    metrics: [
      { label: 'Team Scalability', value: '1 to N+ Agents' },
      { label: 'Autonomous Scope', value: 'Strictly Bounded' },
      { label: 'Prompt Integrity', value: 'Immutable' },
    ],
    connections: ['orchestration', 'memory', 'tools', 'governance'],
  },
  {
    id: 'orchestration',
    letter: 'O',
    title: 'Orchestration',
    role: 'Deterministic Workflow Routing',
    tagline: 'MessageBus task routing is proven in-house. Deterministic DAG orchestration is an approved enterprise architecture.',
    corePrinciple:
      'Workflows execute through state machines and deterministic event brokers. Spontaneous agent-to-agent chatter is replaced with structured, auditable message routing.',
    executiveSummary:
      'Orchestration governs the routing of tasks, data, and decisions across all participating entities. MessageBus task routing is proven in-house, while deterministic DAG orchestration serves as the approved enterprise architecture ensuring multi-step processes remain completely reproducible, measurable, and auditable from inception to delivery.',
    Icon: GitBranch,
    icon3d: 'orchestration',
    accent: 'cyan',
    inputs: [
      'Strategic intent parameters from Human Authority',
      'Dependency graphs, workflow schemas, and routing policies',
      'Real-time agent availability and resource constraints',
      'Event-driven triggers from webhooks and schedule queues',
    ],
    outputs: [
      'Deterministic task dispatches with idempotency keys',
      'Synchronized state transitions across parallel pipelines',
      'Real-time workflow telemetry and latency monitoring',
      'Automatic fallback triggers and human escalation queues',
    ],
    operationalScope: [
      'In-house MessageBus event and task dispatch validation',
      'Approved enterprise deterministic DAG workflow orchestration',
      'State-machine transition enforcement and conflict resolution',
      'Idempotent task retry and graceful degradation handling',
    ],
    governanceInterlock:
      'Enforces Tier 3 (Tactical Decision Gate) and workflow checkpoints. Halts automated progression instantly if an unexpected state divergence occurs.',
    systemExample:
      'The Orchestration broker coordinates identity and credential verification workflows, queuing human approval before account activation.',
    metrics: [
      { label: 'Routing Model', value: 'In-House Bus / Target DAG' },
      { label: 'Traceability', value: '100% Auditable' },
      { label: 'Failure Recovery', value: 'Idempotent Retries' },
    ],
    connections: ['human', 'agents', 'memory', 'tools', 'governance', 'value'],
  },
  {
    id: 'memory',
    letter: 'M',
    title: 'Persistent Memory',
    role: 'Contextual Operational State',
    tagline: 'Context survives across cycles so agents recall before they act.',
    corePrinciple:
      'Agents never operate from a blank slate. Structured vector embeddings, organizational entity registers, and episodic audit ledgers maintain long-term institutional continuity.',
    executiveSummary:
      'Memory provides persistent contextual recall across multi-step, long-running business processes. LightSpeed combines in-house organizational registries, knowledge embeddings and contextual retrieval with an approved Enterprise Data Isolation Architecture designed to support strict tenant-data separation.',
    Icon: HardDrive,
    icon3d: 'memory',
    accent: 'cyan',
    inputs: [
      'Operational receipts and output artifacts from completed tasks',
      'Organizational knowledge bases, policies, and regulatory docs',
      'Customer interaction histories and verified preferences',
      'System performance benchmarks and error logs',
    ],
    outputs: [
      'Semantic context vectors tailored to active agent prompts',
      'Historical precedence retrieval for decision support',
      'Strict tenant-isolated data partitions',
      'Comprehensive change histories and audit records',
    ],
    operationalScope: [
      'Enterprise Data Isolation Architecture and tenant partitioning',
      'Semantic search and multi-document contextual retrieval',
      'Persistent organizational registry and entity mapping',
      'Episodic audit logging with tamper-evident record keeping',
    ],
    governanceInterlock:
      'Governed by tenant-isolation policies and automated data redaction. Memory pipelines strip sensitive personally identifiable information (PII) before storage.',
    systemExample:
      'A Compliance Review Agent queries the Memory store to cross-reference a draft corporate contract against regional procurement acts and historical precedents.',
    metrics: [
      { label: 'State Model', value: 'Multi-Tier Memory' },
      { label: 'Data Isolation', value: 'Enterprise Data Isolation Architecture' },
      { label: 'Context Fidelity', value: 'Grounded Retrieval' },
    ],
    connections: ['orchestration', 'agents', 'governance'],
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'Sandboxed Tools',
    role: 'Controlled Real-World Interfaces',
    tagline: 'Isolated execution boundaries and scoped API access provide safe execution.',
    corePrinciple:
      'Tools represent the sole mechanism through which agents touch operational systems. Every invocation occurs within isolated execution boundaries with least-privilege credentials.',
    executiveSummary:
      'Tools translate neural intentions into real-world software actions. Rather than granting agents direct network or shell access, LightSpeed routes external calls through isolated execution boundaries and scoped API proxies, validating inputs and enforcing schema compliance before executing transactions.',
    Icon: Wrench,
    icon3d: 'tools',
    accent: 'cyan',
    inputs: [
      'Parameterized tool requests issued by authorized agents',
      'Scoped, short-lived OAuth and API session tokens',
      'Validated input schemas matching strict system types',
      'Rate-limiting and resource-quota allowances',
    ],
    outputs: [
      'Deterministic API call responses and structured datasets',
      'Execution exit codes and telemetry records',
      'Telemetry logs capturing external network latency',
      'Security exception alerts for malformed requests',
    ],
    operationalScope: [
      'Isolated Execution Boundaries & Scoped API Access',
      'REST, GraphQL, and database query proxying',
      'Bounded subprocess execution and target container sandboxes',
      'Automated documentation generation and asset compiling',
    ],
    governanceInterlock:
      'Enforces least-privilege access and credential encapsulation. Tools never expose raw secrets to model prompts and automatically restrict high-risk transactional tools to Tier 4 approval.',
    systemExample:
      'A regulated disbursement workflow supports approved supplier invoice settlements, applying transaction limits and human authorization controls.',
    metrics: [
      { label: 'Execution Boundary', value: 'Isolated Execution Boundaries & Scoped API Access' },
      { label: 'Access Control', value: 'Least Privilege' },
      { label: 'Secrets Exposure', value: 'Zero Raw Keys' },
    ],
    connections: ['orchestration', 'agents', 'governance', 'value'],
  },
  {
    id: 'governance',
    letter: 'G',
    title: 'Transverse Governance',
    role: 'Continuous System-Wide Control Fabric',
    tagline: 'Woven through every dimension: five-tier approvals and cryptographic audit trails.',
    corePrinciple:
      'Governance is not a final inspection gate; it is a continuous, transverse control plane that inspects, constrains, and verifies every input, transition, and output in real time.',
    executiveSummary:
      'Governance constitutes the defining backbone of LightSpeed operating systems. By weaving a Five-Tier Human Approval Matrix into the architecture, alongside automated SHA-256 state receipts and risk classification engines, LightSpeed ensures that autonomous velocity never compromises institutional safety, legal compliance, or human authority.',
    Icon: ShieldCheck,
    icon3d: 'safe',
    accent: 'red',
    inputs: [
      'Real-time prompt vectors and agent execution proposals',
      'Risk classification thresholds and policy rulebooks',
      'Human approval signals across organizational tiers',
      'Cryptographic signatures and access credentials',
    ],
    outputs: [
      'Real-time execution permits or automatic block decisions',
      'Immutable SHA-256 state receipts stored in append-only ledgers',
      'Instant human escalation alerts for boundary crossing',
      'Continuous compliance audit summaries for executive review',
    ],
    operationalScope: [
      'Five-Tier Human Approval Matrix enforcement (in-house proven)',
      'Automated risk classification and prompt sanitization',
      'Cryptographic state receipts and append-only audit ledgers',
      'Compliance verification against regional and global standards',
    ],
    governanceInterlock:
      'The Governance engine itself holds unilateral authority to pause or terminate any workflow that violates security thresholds or attempts unauthorized parameter alterations.',
    systemExample:
      'When an automated workflow prepares a strategic contract modification, the Governance layer freezes execution at Tier 4, alerting the Executive Director for cryptographic sign-off.',
    metrics: [
      { label: 'Architecture Role', value: 'Transverse Fabric' },
      { label: 'Human Gates', value: '5-Tier Matrix (In-House)' },
      { label: 'Audit Verification', value: 'SHA-256 State Receipts' },
    ],
    connections: ['human', 'agents', 'orchestration', 'memory', 'tools', 'value'],
  },
  {
    id: 'value',
    letter: 'V',
    title: 'Measured Value',
    role: 'Empirical Business Outcomes & Strategy Feedback',
    tagline: 'Measured business outcomes fed back into strategy, not vanity metrics.',
    corePrinciple:
      'Value is the only score that counts. Automation is justifiable only when it delivers measurable reductions in cycle time, operational expense, error rates, and capital drag.',
    executiveSummary:
      'The ultimate purpose of the HAOMTGV architecture is the delivery of tangible enterprise value. Rather than measuring arbitrary metrics like token counts or raw model calls, LightSpeed instruments every workflow to evaluate measurable business outcomes, feeding empirical insights back to Human leadership to drive continuous strategy refinement.',
    Icon: TrendingUp,
    icon3d: 'chart',
    accent: 'cyan',
    inputs: [
      'Operational cycle completion times and SLA records',
      'Financial transaction accounting and infrastructure costs',
      'Quality assurance audit results and defect logs',
      'User satisfaction feedback and adoption telemetry',
    ],
    outputs: [
      'Calculated ROI metrics and projected cost compression models',
      'Cycle-time evaluation comparing manual vs governed workflows',
      'Defect monitoring telemetry and accuracy scorecards',
      'Strategic optimization recommendations delivered to Human leaders',
    ],
    operationalScope: [
      'Real-time cost, latency, and quality instrumentation',
      'Target cycle time, opex, defect rate, and capital efficiency optimization',
      'Executive dashboard reporting and board-level metrics',
      'Closed-loop feedback to strategic human planning',
    ],
    governanceInterlock:
      'Value telemetry is audited by the Governance engine to ensure that efficiency targets never compromise regulatory compliance or operational integrity.',
    systemExample:
      'In-house regulatory reporting automation demonstrates governed agent workflows with SHA-256-sealed audit trails for individual reported figures.',
    metrics: [
      { label: 'Evaluation Criteria', value: 'Cycle, Opex, Quality' },
      { label: 'Optimization Target', value: 'Measurable Efficiency' },
      { label: 'Feedback Loop', value: 'Closed-Loop to Human' },
    ],
    connections: ['tools', 'orchestration', 'governance', 'human'],
  },
];

interface HaomtgvUnifiedArchitectureProps {
  theme: 'light' | 'dark';
}

export const HaomtgvUnifiedArchitecture: React.FC<HaomtgvUnifiedArchitectureProps> = ({
  theme,
}) => {
  const isLight = theme === 'light';
  const [selectedId, setSelectedId] = useState<string>('human');
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  const activeId = hoveredId || selectedId;
  const activeDim =
    ARCHITECTURE_DIMENSIONS.find((d) => d.id === activeId) || ARCHITECTURE_DIMENSIONS[0];

  // Helper to check if a node or edge is related to the currently active dimension
  const isConnected = (id: string): boolean => {
    if (activeId === id) return true;
    return activeDim.connections.includes(id);
  };

  return (
    <div className="w-full space-y-10">
      {/* Visual Architectural Diagram Canvas */}
      <div
        className={`relative rounded-3xl overflow-hidden p-6 sm:p-10 transition-all ${
          isLight
            ? 'bg-gradient-to-b from-white via-slate-50 to-slate-100 shadow-xl'
            : 'bg-gradient-to-b from-[#0A1330] via-ls-navy to-[#050B1A] shadow-2xl'
        }`}
      >
        {/* Subtle architectural schematic grid */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 opacity-15"
          style={{
            backgroundImage:
              'radial-gradient(circle at 1px 1px, rgba(0,191,255,0.35) 1px, transparent 0)',
            backgroundSize: '32px 32px',
          }}
        />

        {/* Outer Transverse Governance Boundary Indicator */}
        <div
          className={`relative rounded-2xl p-4 sm:p-6 transition-all duration-300 ${
            activeId === 'governance'
              ? 'shadow-2xl shadow-ls-red/25 bg-ls-red/5'
              : 'bg-ls-red/[0.02]'
          }`}
        >
          {/* Top Banner: Transverse Governance Shield Label */}
          <div className="flex flex-wrap items-center justify-between gap-3 mb-8 pb-3">
            <button
              type="button"
              onClick={() => setSelectedId('governance')}
              onMouseEnter={() => setHoveredId('governance')}
              onMouseLeave={() => setHoveredId(null)}
              className="inline-flex items-center gap-2.5 text-left group cursor-pointer focus:outline-none"
            >
              <span
                className={`w-7 h-7 rounded-lg flex items-center justify-center font-display font-black text-sm transition-transform group-hover:scale-105 ${
                  activeId === 'governance'
                    ? 'bg-ls-red text-white shadow-md shadow-ls-red/40'
                    : 'bg-ls-red/20 text-ls-red'
                }`}
              >
                G
              </span>
              <div>
                <span className="text-xs font-mono font-bold tracking-widest text-ls-red uppercase block">
                  TRANSVERSE GOVERNANCE LAYER (SPANS & CONSTRAINS ALL DIMENSIONS)
                </span>
                <span className="text-[11px] text-slate-400 group-hover:text-ls-white transition-colors">
                  5-Tier Approval Matrix • SHA-256 State Receipts • Real-Time Execution Guardrails
                </span>
              </div>
            </button>

            <span className="text-[10px] font-mono px-3 py-1 rounded bg-ls-red/10 text-ls-red font-bold uppercase tracking-wider">
              CONTINUOUS SECURITY PERIMETER
            </span>
          </div>

          {/* TOP PINNACLE: HUMAN AUTHORITY (H) */}
          <div className="flex justify-center mb-10">
            <div className="w-full max-w-2xl">
              <button
                type="button"
                onClick={() => setSelectedId('human')}
                onMouseEnter={() => setHoveredId('human')}
                onMouseLeave={() => setHoveredId(null)}
                className={`w-full p-6 sm:p-7 rounded-2xl text-left transition-all cursor-pointer relative overflow-hidden group focus:outline-none ${
                  activeId === 'human'
                    ? 'bg-ls-navy shadow-xl shadow-ls-cyan/30 scale-[1.01]'
                    : isConnected('human')
                    ? 'bg-ls-navy/90 text-white'
                    : isLight
                    ? 'bg-white text-ls-navy hover:bg-ls-grey-light/50'
                    : 'bg-[#050B1A]/90 text-white hover:bg-ls-white/5'
                }`}
              >
                {/* Visual Crown Accent */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-ls-cyan via-white to-ls-cyan" />

                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <span
                      className={`w-12 h-12 rounded-xl flex items-center justify-center font-display font-black text-2xl transition-transform group-hover:scale-105 ${
                        activeId === 'human'
                          ? 'bg-ls-cyan text-ls-navy shadow-lg shadow-ls-cyan/40'
                          : 'bg-ls-cyan/20 text-ls-cyan'
                      }`}
                    >
                      H
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold tracking-widest text-ls-cyan uppercase">
                          ARCHITECTURAL PINNACLE
                        </span>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-ls-cyan/15 text-ls-cyan font-bold uppercase">
                          Sovereign Apex
                        </span>
                      </div>
                      <h3 className="text-xl sm:text-2xl font-black font-display tracking-tight text-white mt-0.5">
                        Human Authority & Strategic Intent
                      </h3>
                    </div>
                  </div>

                  <Icon3D name="users" size="sm" />
                </div>

                <p className="text-xs sm:text-sm text-slate-300 mt-3 font-medium leading-relaxed">
                  Machines execute, humans approve. Operational boundaries, capital allocations, and
                  ethical guardrails are established here.
                </p>

                <div className="mt-4 pt-3 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-400">
                  <span>Downlink: Strategic Intent to Orchestration</span>
                  <span className="text-ls-cyan font-bold">Uplink: Empirical Value & Approval Requests</span>
                </div>
              </button>
            </div>
          </div>

          {/* CONDUIT: Human to Operational Core */}
          <div className="flex justify-center -my-6 relative z-10">
            <div className="flex flex-col items-center">
              <div
                className={`w-0.5 h-10 transition-colors duration-300 ${
                  isConnected('human') && isConnected('orchestration')
                    ? 'bg-ls-cyan shadow-[0_0_10px_#00BFFF]'
                    : 'bg-slate-600'
                }`}
              />
              <div
                className={`w-2.5 h-2.5 rotate-45 transition-colors duration-300 ${
                  isConnected('human') && isConnected('orchestration')
                    ? 'bg-ls-cyan'
                    : 'bg-slate-600'
                }`}
              />
            </div>
          </div>

          {/* THE OPERATIONAL ENGINE: [AGENTS] <-> [ORCHESTRATION] <-> [MEMORY] */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4 lg:gap-6 mt-6 items-stretch">
            {/* LEFT FLANK: CONFIGURABLE AGENTS (A) */}
            <div className="md:col-span-4 flex flex-col">
              <button
                type="button"
                onClick={() => setSelectedId('agents')}
                onMouseEnter={() => setHoveredId('agents')}
                onMouseLeave={() => setHoveredId(null)}
                className={`w-full p-5 rounded-2xl text-left transition-all h-full flex flex-col justify-between cursor-pointer group focus:outline-none ${
                  activeId === 'agents'
                    ? 'bg-ls-navy shadow-xl shadow-ls-cyan/20 scale-[1.01]'
                    : isConnected('agents')
                    ? 'bg-ls-navy/80 text-white'
                    : isLight
                    ? 'bg-white text-ls-navy hover:bg-ls-grey-light/70'
                    : 'bg-[#050B1A]/80 text-white hover:bg-ls-white/50'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span
                      className={`w-10 h-10 rounded-xl flex items-center justify-center font-display font-black text-lg ${
                        activeId === 'agents'
                          ? 'bg-ls-cyan text-ls-navy shadow-md shadow-ls-cyan/30'
                          : 'bg-ls-cyan/20 text-ls-cyan'
                      }`}
                    >
                      A
                    </span>
                    <Icon3D name="intelligence" size="xs" />
                  </div>
                  <span className="text-[10px] font-mono font-bold tracking-widest text-ls-cyan uppercase block">
                    COGNITIVE EXECUTION
                  </span>
                  <h4 className="text-base sm:text-lg font-bold font-display tracking-tight text-white mt-1">
                    Configurable Agents
                  </h4>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Scalable agent teams (1 to N+ specialized roles). Strictly bounded contracts;
                    no unconstrained bots.
                  </p>
                </div>

                <div className="mt-4 pt-3 flex items-center justify-between text-[11px] font-mono text-slate-400">
                  <span>Scope: Role Bounded</span>
                  <span className="text-ls-cyan">Zero Self-Elevation</span>
                </div>
              </button>
            </div>

            {/* CENTER SWITCHBOARD: ORCHESTRATION (O) */}
            <div className="md:col-span-4 flex flex-col">
              <button
                type="button"
                onClick={() => setSelectedId('orchestration')}
                onMouseEnter={() => setHoveredId('orchestration')}
                onMouseLeave={() => setHoveredId(null)}
                className={`w-full p-5 sm:p-6 rounded-2xl text-left transition-all h-full flex flex-col justify-between cursor-pointer group focus:outline-none ${
                  activeId === 'orchestration'
                    ? 'bg-ls-navy shadow-xl shadow-ls-cyan/30 scale-[1.01]'
                    : isConnected('orchestration')
                    ? 'bg-ls-navy/90 text-white'
                    : isLight
                    ? 'bg-white text-ls-navy hover:bg-ls-grey-light/50'
                    : 'bg-[#050B1A] text-white hover:bg-ls-white/50'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span
                      className={`w-10 h-10 rounded-xl flex items-center justify-center font-display font-black text-lg ${
                        activeId === 'orchestration'
                          ? 'bg-ls-cyan text-ls-navy shadow-md shadow-ls-cyan/40'
                          : 'bg-ls-cyan/20 text-ls-cyan'
                      }`}
                    >
                      O
                    </span>
                    <Icon3D name="orchestration" size="xs" />
                  </div>
                  <span className="text-[10px] font-mono font-bold tracking-widest text-ls-cyan uppercase block">
                    CENTRAL NERVOUS SYSTEM
                  </span>
                  <h4 className="text-base sm:text-lg font-bold font-display tracking-tight text-white mt-1">
                    Deterministic Orchestration
                  </h4>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Directed Acyclic Graph (DAG) state machines. Coordinates Agents, Memory, and
                    Tools with complete audit trace logs.
                  </p>
                </div>

                <div className="mt-4 pt-3 flex items-center justify-between text-[11px] font-mono text-slate-400">
                  <span>Routing: In-House Bus / Target DAG</span>
                  <span className="text-ls-cyan">100% Traceable</span>
                </div>
              </button>
            </div>

            {/* RIGHT FLANK: PERSISTENT MEMORY (M) */}
            <div className="md:col-span-4 flex flex-col">
              <button
                type="button"
                onClick={() => setSelectedId('memory')}
                onMouseEnter={() => setHoveredId('memory')}
                onMouseLeave={() => setHoveredId(null)}
                className={`w-full p-5 rounded-2xl text-left transition-all h-full flex flex-col justify-between cursor-pointer group focus:outline-none ${
                  activeId === 'memory'
                    ? 'bg-ls-navy shadow-xl shadow-ls-cyan/20 scale-[1.01]'
                    : isConnected('memory')
                    ? 'bg-ls-navy/80 text-white'
                    : isLight
                    ? 'bg-white text-ls-navy hover:bg-ls-grey-light/70'
                    : 'bg-[#050B1A]/80 text-white hover:bg-ls-white/50'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span
                      className={`w-10 h-10 rounded-xl flex items-center justify-center font-display font-black text-lg ${
                        activeId === 'memory'
                          ? 'bg-ls-cyan text-ls-navy shadow-md shadow-ls-cyan/30'
                          : 'bg-ls-cyan/20 text-ls-cyan'
                      }`}
                    >
                      M
                    </span>
                    <Icon3D name="memory" size="xs" />
                  </div>
                  <span className="text-[10px] font-mono font-bold tracking-widest text-ls-cyan uppercase block">
                    CONTEXTUAL CONTINUITY
                  </span>
                  <h4 className="text-base sm:text-lg font-bold font-display tracking-tight text-white mt-1">
                    Persistent Memory
                  </h4>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Tenant-isolated vector knowledge, organizational entity registers, and episodic
                    audit history.
                  </p>
                </div>

                <div className="mt-4 pt-3 flex items-center justify-between text-[11px] font-mono text-slate-400">
                  <span>State: Multi-Tier Memory</span>
                  <span className="text-ls-cyan">Enterprise Isolation</span>
                </div>
              </button>
            </div>
          </div>

          {/* CONDUIT: Orchestration to Tools */}
          <div className="flex justify-center my-3 relative z-10">
            <div className="flex flex-col items-center">
              <div
                className={`w-0.5 h-8 transition-colors duration-300 ${
                  isConnected('orchestration') && isConnected('tools')
                    ? 'bg-ls-cyan shadow-[0_0_10px_#00BFFF]'
                    : 'bg-slate-600'
                }`}
              />
              <div
                className={`w-2.5 h-2.5 rotate-45 transition-colors duration-300 ${
                  isConnected('orchestration') && isConnected('tools')
                    ? 'bg-ls-cyan'
                    : 'bg-slate-600'
                }`}
              />
            </div>
          </div>

          {/* LOWER OPERATIONAL BOUNDARY: SANDBOXED TOOLS (T) */}
          <div className="flex justify-center mb-10">
            <div className="w-full max-w-2xl">
              <button
                type="button"
                onClick={() => setSelectedId('tools')}
                onMouseEnter={() => setHoveredId('tools')}
                onMouseLeave={() => setHoveredId(null)}
                className={`w-full p-5 sm:p-6 rounded-2xl text-left transition-all cursor-pointer group focus:outline-none ${
                  activeId === 'tools'
                    ? 'bg-ls-navy shadow-xl shadow-ls-cyan/20 scale-[1.01]'
                    : isConnected('tools')
                    ? 'bg-ls-navy/90 text-white'
                    : isLight
                    ? 'bg-white text-ls-navy hover:bg-ls-grey-light/80'
                    : 'bg-[#050B1A]/90 text-white hover:bg-ls-white/60'
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <span
                      className={`w-10 h-10 rounded-xl flex items-center justify-center font-display font-black text-lg ${
                        activeId === 'tools'
                          ? 'bg-ls-cyan text-ls-navy shadow-md shadow-ls-cyan/30'
                          : 'bg-ls-cyan/20 text-ls-cyan'
                      }`}
                    >
                      T
                    </span>
                    <div>
                      <span className="text-[10px] font-mono font-bold tracking-widest text-ls-cyan uppercase block">
                        EXTERNAL EXECUTION INTERFACE
                      </span>
                      <h4 className="text-base sm:text-lg font-bold font-display tracking-tight text-white">
                        Sandboxed Tools & Secure APIs
                      </h4>
                    </div>
                  </div>
                  <Icon3D name="tools" size="xs" />
                </div>

                <p className="text-xs text-slate-300 mt-2.5 leading-relaxed">
                  The only safe bridge between neural tokens and the physical world. Sandboxed
                  containers, payment rails, and least-privilege APIs.
                </p>

                <div className="mt-3 pt-3 flex flex-wrap items-center justify-between text-[11px] font-mono text-slate-400">
                  <span>Enclosure: Isolated Boundaries & Scoped APIs</span>
                  <span className="text-ls-cyan font-semibold">Zero Raw Secrets Exposure</span>
                </div>
              </button>
            </div>
          </div>

          {/* CONDUIT: Tools to Measured Value */}
          <div className="flex justify-center -my-6 relative z-10">
            <div className="flex flex-col items-center">
              <div
                className={`w-0.5 h-10 transition-colors duration-300 ${
                  isConnected('tools') && isConnected('value')
                    ? 'bg-ls-cyan shadow-[0_0_10px_#00BFFF]'
                    : 'bg-slate-600'
                }`}
              />
              <div
                className={`w-2.5 h-2.5 rotate-45 transition-colors duration-300 ${
                  isConnected('tools') && isConnected('value')
                    ? 'bg-ls-cyan'
                    : 'bg-slate-600'
                }`}
              />
            </div>
          </div>

          {/* BASE & CLOSED LOOP: MEASURED VALUE (V) */}
          <div className="flex justify-center mt-6">
            <div className="w-full max-w-2xl">
              <button
                type="button"
                onClick={() => setSelectedId('value')}
                onMouseEnter={() => setHoveredId('value')}
                onMouseLeave={() => setHoveredId(null)}
                className={`w-full p-6 sm:p-7 rounded-2xl text-left transition-all cursor-pointer relative overflow-hidden group focus:outline-none ${
                  activeId === 'value'
                    ? 'bg-ls-navy shadow-xl shadow-ls-cyan/30 scale-[1.01]'
                    : isConnected('value')
                    ? 'bg-ls-navy/90 text-white'
                    : isLight
                    ? 'bg-white text-ls-navy hover:bg-ls-grey-light/80'
                    : 'bg-[#050B1A]/90 text-white hover:bg-ls-white/60'
                }`}
              >
                {/* Visual Base Accent */}
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-ls-cyan via-ls-red to-ls-cyan" />

                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <span
                      className={`w-12 h-12 rounded-xl flex items-center justify-center font-display font-black text-2xl transition-transform group-hover:scale-105 ${
                        activeId === 'value'
                          ? 'bg-ls-cyan text-ls-navy shadow-lg shadow-ls-cyan/40'
                          : 'bg-ls-cyan/20 text-ls-cyan'
                      }`}
                    >
                      V
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold tracking-widest text-ls-cyan uppercase">
                          ARCHITECTURAL OUTCOME & AUDIT
                        </span>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-bold uppercase">
                          Empirical Criteria
                        </span>
                      </div>
                      <h3 className="text-xl sm:text-2xl font-black font-display tracking-tight text-white mt-0.5">
                        Measured Value & Strategic Feedback Loop
                      </h3>
                    </div>
                  </div>

                  <Icon3D name="chart" size="sm" />
                </div>

                <p className="text-xs sm:text-sm text-slate-300 mt-3 font-medium leading-relaxed">
                  Value is the only score that counts. Measurable criteria for cost compression, cycle
                  time, and defect avoidance loop directly back to Human Authority.
                </p>

                <div className="mt-4 pt-3 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-400">
                  <span className="text-emerald-400 font-bold">Feedback Loop: Feeds empirical outcome data back to Human Authority</span>
                  <span>Evaluation: Cycle Time • Cost • Quality</span>
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Legend / Quick Instruction */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 text-xs font-mono text-slate-400 px-2">
          <div className="flex items-center gap-3">
            <span className="inline-block w-2.5 h-2.5 rounded-full bg-ls-cyan animate-pulse" />
            <span>Click or hover any dimension to inspect data flows and governance rules</span>
          </div>
          <span className="text-ls-cyan font-bold">Currently Inspecting: Dimension {activeDim.letter}: {activeDim.title}</span>
        </div>
      </div>

      {/* DETAILED SPECIFICATION INSPECTOR FOR THE SELECTED DIMENSION */}
      <div
        className={`rounded-3xl p-6 sm:p-10 transition-all duration-300 ${
          isLight
            ? 'bg-white shadow-xl text-ls-navy'
            : 'bg-ls-navy/90 shadow-2xl text-white'
        }`}
      >
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Dimension Profile */}
          <div className="lg:col-span-5 space-y-6">
            <div className="flex items-center gap-4">
              <Icon3D name={activeDim.icon3d} size="md" />
              <span
                className={`w-14 h-14 rounded-2xl flex items-center justify-center font-display font-black text-3xl shadow-lg ${
                  activeDim.letter === 'G'
                    ? 'bg-ls-red text-white shadow-ls-red/30'
                    : 'bg-ls-cyan text-ls-navy shadow-ls-cyan/30'
                }`}
              >
                {activeDim.letter}
              </span>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold tracking-widest text-ls-cyan uppercase">
                    DIMENSION SPECIFICATION
                  </span>
                  {activeDim.letter === 'G' && (
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-ls-red/20 text-ls-red font-bold uppercase">
                      Transverse Fabric
                    </span>
                  )}
                  {activeDim.letter === 'H' && (
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-ls-cyan/20 text-ls-cyan font-bold uppercase">
                      Pinnacle Anchor
                    </span>
                  )}
                </div>
                <h3 className="text-2xl sm:text-3xl font-black font-display tracking-tight mt-0.5">
                  {activeDim.title}
                </h3>
                <p className="text-xs font-mono text-slate-400">{activeDim.role}</p>
              </div>
            </div>

            <p className="text-sm font-semibold text-ls-cyan leading-relaxed">
              {activeDim.tagline}
            </p>

            <div
              className={`p-4 rounded-xl text-xs leading-relaxed ${
                isLight
                  ? 'bg-slate-50 text-slate-700'
                  : 'bg-[#050B1A]/80 text-slate-300'
              }`}
            >
              <strong className="block font-bold text-ls-red mb-1 font-mono uppercase tracking-wider text-[11px]">
                Architectural Principle
              </strong>
              {activeDim.corePrinciple}
            </div>

            <p
              className={`text-sm leading-relaxed ${
                isLight ? 'text-slate-600' : 'text-slate-300'
              }`}
            >
              {activeDim.executiveSummary}
            </p>

            {/* Key Metrics */}
            <div className="grid grid-cols-3 gap-2.5 pt-2">
              {activeDim.metrics.map((m, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-xl text-center ${
                    isLight
                      ? 'bg-slate-50'
                      : 'bg-[#050B1A]/50'
                  }`}
                >
                  <span className="text-[10px] font-mono text-slate-400 block uppercase truncate">
                    {m.label}
                  </span>
                  <span className="text-xs font-bold text-ls-cyan block mt-1">
                    {m.value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Inputs, Outputs, Scope, Governance Interlock, and Real-World Example */}
          <div className="lg:col-span-7 space-y-6">
            {/* Inputs & Outputs Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Inputs */}
              <div
                className={`p-5 rounded-2xl ${
                  isLight ? 'bg-slate-50' : 'bg-[#050B1A]/70'
                }`}
              >
                <div className="flex items-center gap-2 mb-3">
                  <ArrowDown className="w-3.5 h-3.5 text-ls-cyan" />
                  <span className="text-xs font-mono font-bold text-ls-cyan uppercase tracking-wider">
                    Inbound Signals & Inputs
                  </span>
                </div>
                <ul className="space-y-2 text-xs text-slate-400 font-body">
                  {activeDim.inputs.map((inp, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-ls-cyan font-bold mt-0.5">›</span>
                      <span className={isLight ? 'text-slate-700' : 'text-slate-300'}>
                        {inp}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Outputs */}
              <div
                className={`p-5 rounded-2xl ${
                  isLight ? 'bg-slate-50' : 'bg-[#050B1A]/70'
                }`}
              >
                <div className="flex items-center gap-2 mb-3">
                  <ArrowRight className="w-3.5 h-3.5 text-ls-red" />
                  <span className="text-xs font-mono font-bold text-ls-red uppercase tracking-wider">
                    Outbound Deliverables
                  </span>
                </div>
                <ul className="space-y-2 text-xs text-slate-400 font-body">
                  {activeDim.outputs.map((out, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-ls-red font-bold mt-0.5">›</span>
                      <span className={isLight ? 'text-slate-700' : 'text-slate-300'}>
                        {out}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Operational Scope */}
            <div
              className={`p-5 rounded-2xl ${
                isLight ? 'bg-slate-50' : 'bg-[#050B1A]/70'
              }`}
            >
              <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-ls-cyan mb-3 flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-ls-cyan" />
                Operational Scope & Bounded Responsibilities
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
                {activeDim.operationalScope.map((scope, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <span className="text-ls-cyan font-bold mt-0.5">•</span>
                    <span className={isLight ? 'text-slate-700' : 'text-slate-300'}>
                      {scope}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Governance Interlock */}
            <div
              className={`p-5 rounded-2xl ${
                activeDim.letter === 'G'
                  ? 'bg-ls-red/10 text-white'
                  : isLight
                  ? 'bg-slate-100'
                  : 'bg-[#050B1A]/90'
              }`}
            >
              <div className="flex items-center gap-2 mb-1.5">
                <Shield className="w-4 h-4 text-ls-red" />
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-ls-red">
                  Governance Interlock & Constraint Protocol
                </span>
              </div>
              <p
                className={`text-xs leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-slate-300'
                }`}
              >
                {activeDim.governanceInterlock}
              </p>
            </div>

            {/* System Example */}
            <div
              className={`p-4 rounded-xl flex items-start gap-3 ${
                isLight
                  ? 'bg-ls-cyan/5 text-ls-navy'
                  : 'bg-ls-cyan/10 text-white'
              }`}
            >
              <Compass className="w-5 h-5 text-ls-cyan shrink-0 mt-0.5" />
              <div>
                <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-ls-cyan block">
                  Governed Implementation Verification
                </span>
                <p className="text-xs mt-1 leading-relaxed">
                  {activeDim.systemExample}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HaomtgvUnifiedArchitecture;
