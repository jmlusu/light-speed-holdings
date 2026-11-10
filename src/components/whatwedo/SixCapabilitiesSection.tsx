import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { Building2, Zap, GitFork, Network, HardDrive, ShieldCheck, CheckCircle2, Lock, ArrowUpRight } from 'lucide-react';
import { Icon3D, Icon3DName } from '../common';

interface CapabilityDetail {
  id: string;
  num: string;
  title: string;
  status: 'Proven in-house' | 'Fieldable in 2026' | 'In pilot' | 'In development';
  statusColor: string;
  icon: any;
  icon3d: Icon3DName;
  whatItIs: string;
  problem: string;
  whatWeBuild: string[];
  architectureConnection: string;
  diagramTitle: string;
  diagramSteps: string[];
  relatedResearch?: { title: string; slug: string }[];
}

const SIX_CAPABILITIES: readonly [CapabilityDetail, ...CapabilityDetail[]] = [
  {
    id: 'cap-1',
    num: '01',
    title: 'AI-Native Company Building',
    status: 'Proven in-house',
    statusColor: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
    icon: Building2,
    icon3d: 'home',
    whatItIs: 'Strategy-to-build capability for designing, launching, and scaling new enterprise entities where AI agents perform core execution.',
    problem: 'Traditional startup launching incurs heavy early management overhead, manual hiring delays, and slow operational ramp-up.',
    whatWeBuild: [
      'Turnkey venture operating models with defined 90-agent role hierarchies.',
      'Sovereign CEO control panels with automated budget and approval limits.',
      'Deployment environments on self-hosted or cloud infrastructure.',
    ],
    architectureConnection: 'Connects Human Authority (H) directly to Orchestration (O) and Value (V) measurement.',
    diagramTitle: 'Venture Creation Pipeline',
    diagramSteps: ['Opportunity Definition', 'Operating Model Synthesis', 'Agent Workforce Deployment', 'Sovereign Launch'],
    relatedResearch: [{ title: 'Inside a 91-Agent Company', slug: 'inside-a-90-agent-company' }]
  },
  {
    id: 'cap-2',
    num: '02',
    title: 'Intelligent Workflow Automation',
    status: 'Fieldable in 2026',
    statusColor: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/20',
    icon: Zap,
    icon3d: 'lightning',
    whatItIs: 'Process compression technology transforming multi-step manual tasks into automated, deterministic execution paths.',
    problem: 'Enterprise workflows get blocked waiting on staff availability, manual copy-pasting across software, and email sign-off chains.',
    whatWeBuild: [
      'Document and report generation pipelines from raw data inputs.',
      'WhatsApp-native automated customer and order assistants.',
      'Mobile-money (Airtel Money, TNM Mpamba, PayChangu) transaction integrations.',
    ],
    architectureConnection: 'Pairs Specialized Agents (A) with System Tools (T) for rapid task completion.',
    diagramTitle: 'Workflow Compression Flow',
    diagramSteps: ['Multi-Source Ingestion', 'Agent Decomposition', 'Tool Invocations', 'Verified Output'],
  },
  {
    id: 'cap-3',
    num: '03',
    title: 'Agentic Systems & Orchestration',
    status: 'Proven in-house',
    statusColor: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
    icon: GitFork,
    icon3d: 'orchestration',
    whatItIs: 'Multi-agent orchestration graphs that break complex business problems into discrete, coordinated sub-tasks.',
    problem: 'Single general-purpose chatbots fail at complex, multi-step operations requiring domain specialization and strict state control.',
    whatWeBuild: [
      'Deterministic state machines routing work packages across specialized agent roles.',
      'Parallel agent execution graphs with automatic retry and regression guards.',
      'Agent-to-agent protocol definitions with strict payload schema validation.',
    ],
    architectureConnection: 'Form the core Orchestration (O) engine coordinating Agents (A) and Memory (M).',
    diagramTitle: 'Agent Network Routing',
    diagramSteps: ['Goal Parsing', 'Task Decomposition', 'Parallel Agent Execution', 'Result Synthesis'],
    relatedResearch: [{ title: 'Inside a 91-Agent Company', slug: 'inside-a-90-agent-company' }]
  },
  {
    id: 'cap-4',
    num: '04',
    title: 'Enterprise AI Integration',
    status: 'In development',
    statusColor: 'bg-amber-500/10 text-amber-600 border-amber-500/20',
    icon: Network,
    icon3d: 'network',
    whatItIs: 'Deep integration architecture connecting AI models safely to core ERP, CRM, database, and internal software stacks.',
    problem: 'Siloed AI prototypes cannot securely interact with existing legacy databases or execute real-world transactional writes.',
    whatWeBuild: [
      'API gateway tool sandboxes with tokenized authentication.',
      'Database connectors supporting structured SQL and unstructured data stores.',
      'Bilingual (Chichewa & English) user interfaces and API endpoints.',
    ],
    architectureConnection: 'Provides System Tools (T) and API boundaries for external execution.',
    diagramTitle: 'Integration Gateway',
    diagramSteps: ['API Authentication', 'Tool Sandbox Boundary', 'Enterprise Database Ingress', 'Safe Execution'],
  },
  {
    id: 'cap-5',
    num: '05',
    title: 'Organizational Memory & Knowledge Systems',
    status: 'Fieldable in 2026',
    statusColor: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/20',
    icon: HardDrive,
    icon3d: 'memory',
    whatItIs: 'Persistent contextual database architecture ensuring historical lessons, policies, and domain knowledge ground every agent action.',
    problem: 'Institutional knowledge is lost when employees depart or rotate, forcing teams to solve the same problems repeatedly.',
    whatWeBuild: [
      'Vector memory stores with automated semantic indexing.',
      'Structured policy and standard operating procedure (SOP) knowledge bases.',
      'Cross-session contextual state retention across long-running projects.',
    ],
    architectureConnection: 'Acts as Organizational Memory (M), grounding Agents (A) before every decision.',
    diagramTitle: 'Context Retrieval Architecture',
    diagramSteps: ['Query Embedding', 'Vector Similarity Search', 'Domain Context Injection', 'Grounded Output'],
  },
  {
    id: 'cap-6',
    num: '06',
    title: 'AI Governance & Decision Infrastructure',
    status: 'Proven in-house',
    statusColor: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
    icon: ShieldCheck,
    icon3d: 'governance',
    whatItIs: 'Risk-classified governance framework enforcing human approval gates, compliance checks, and immutable cryptographic audit logging.',
    problem: 'Uncontrolled AI deployment creates reputational risk, regulatory non-compliance, and catastrophic hallucinated execution.',
    whatWeBuild: [
      'Five-tier human approval matrix (AUTO_APPROVE to CEO_ONLY).',
      'Four automated execution gates (Contract, DPA, Compliance, Security).',
      'Append-only SHA-256 cryptographic audit logs.',
    ],
    architectureConnection: 'Forms the Governance (G) control layer wrapping all operations.',
    diagramTitle: 'Governance Gate Model',
    diagramSteps: ['Action Request', 'Risk Classification', 'Approval Gate Check', 'SHA-256 Ledger Entry'],
    relatedResearch: [{ title: 'The Five-Tier Approval Matrix', slug: 'five-tier-approval-matrix' }]
  },
];

interface SixCapabilitiesSectionProps {
  theme?: 'light' | 'dark';
}

export const SixCapabilitiesSection: React.FC<SixCapabilitiesSectionProps> = ({ theme = 'dark' }) => {
  const [selectedCap, setSelectedCap] = useState<CapabilityDetail>(SIX_CAPABILITIES[0]);
  const isLight = theme === 'light';

  return (
    <section id="six-capabilities" className={`py-24 px-6 lg:px-12 relative transition-colors duration-300 ${
      isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-[#0A0D14] text-white'
    }`}>
      <div className="max-w-7xl mx-auto">
        <SectionHeading
          theme={theme}
          eyebrow="DEEP-DIVE CAPABILITIES"
          title="Six Core Enterprise Practice Areas"
          lead="Detailed breakdown of what LightSpeed builds, the problems addressed, architecture connections, and verified implementation status."
        />

        {/* Capability Navigation Tabs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-12 mb-10">
          <div className="space-y-4">
            <h3 className={`text-xs font-bold uppercase tracking-wider pl-1 ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>Operational Execution</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {SIX_CAPABILITIES.slice(0, 3).map((cap) => {
                const isSelected = cap.id === selectedCap.id;
                return (
                  <button
                    key={cap.id}
                    onClick={() => setSelectedCap(cap)}
                    className={`p-4 rounded-xl border transition-all text-left flex flex-col justify-between cursor-pointer ${
                      isSelected
                        ? isLight
                          ? 'bg-ls-navy text-white border-ls-navy shadow-md'
                          : 'bg-ls-cyan/20 text-white border-ls-cyan shadow-lg'
                        : isLight
                          ? 'bg-white text-ls-navy border-slate-200 hover:border-slate-300'
                          : 'bg-white/5 text-slate-300 border-white/5 hover:border-white/20'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className={`text-[10px] font-mono font-bold ${isSelected ? 'text-ls-cyan' : 'text-slate-400'}`}>
                        {cap.num}
                      </span>
                      <Icon3D name={cap.icon3d} size="xs" />
                    </div>
                    <h4 className="text-xs font-bold font-display line-clamp-2">
                      {cap.title}
                    </h4>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="space-y-4">
            <h3 className={`text-xs font-bold uppercase tracking-wider pl-1 ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>Strategy & Governance</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {SIX_CAPABILITIES.slice(3, 6).map((cap) => {
                const isSelected = cap.id === selectedCap.id;
                return (
                  <button
                    key={cap.id}
                    onClick={() => setSelectedCap(cap)}
                    className={`p-4 rounded-xl border transition-all text-left flex flex-col justify-between cursor-pointer ${
                      isSelected
                        ? isLight
                          ? 'bg-ls-navy text-white border-ls-navy shadow-md'
                          : 'bg-ls-cyan/20 text-white border-ls-cyan shadow-lg'
                        : isLight
                          ? 'bg-white text-ls-navy border-slate-200 hover:border-slate-300'
                          : 'bg-white/5 text-slate-300 border-white/5 hover:border-white/20'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className={`text-[10px] font-mono font-bold ${isSelected ? 'text-ls-cyan' : 'text-slate-400'}`}>
                        {cap.num}
                      </span>
                      <Icon3D name={cap.icon3d} size="xs" />
                    </div>
                    <h4 className="text-xs font-bold font-display line-clamp-2">
                      {cap.title}
                    </h4>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Selected Capability Inspector Detail */}
        <div className={`p-8 rounded-2xl border transition-all ${
          isLight ? 'bg-white border-slate-200 shadow-xl' : 'bg-[#070A40]/90 border-white/10 shadow-2xl'
        }`}>
          <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-200/20">
            <div className="flex items-center gap-3.5">
              <Icon3D name={selectedCap.icon3d} size="md" />
              <div>
                <span className="text-[11px] font-mono font-bold text-ls-cyan px-2 py-0.5 rounded bg-ls-cyan/10 inline-block mb-1">
                  CAPABILITY {selectedCap.num}
                </span>
                <h3 className={`text-2xl font-black font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  {selectedCap.title}
                </h3>
              </div>
            </div>

            <span className={`text-xs font-mono font-bold px-3 py-1 rounded-full border ${selectedCap.statusColor}`}>
              Status: {selectedCap.status}
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-8 text-left">
            {/* Left Column: Descriptions */}
            <div className="lg:col-span-7 space-y-6">
              <div>
                <h4 className={`text-xs font-mono uppercase tracking-wider mb-1 ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
                  Overview & Definition
                </h4>
                <p className={`text-sm leading-relaxed font-medium ${isLight ? 'text-slate-800' : 'text-slate-200'}`}>
                  {selectedCap.whatItIs}
                </p>
              </div>

              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-red/5 border-ls-red/20' : 'bg-ls-red/10 border-ls-red/30'}`}>
                <h4 className="text-xs font-mono uppercase tracking-wider text-ls-red mb-1 font-bold">
                  Problem Addressed
                </h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-slate-200'}`}>
                  {selectedCap.problem}
                </p>
              </div>

              <div>
                <h4 className={`text-xs font-mono uppercase tracking-wider mb-2 ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
                  What LightSpeed Builds & Configures
                </h4>
                <ul className="space-y-2">
                  {selectedCap.whatWeBuild.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs leading-relaxed">
                      <CheckCircle2 className="w-4 h-4 text-ls-cyan shrink-0 mt-0.5" />
                      <span className={isLight ? 'text-slate-700' : 'text-slate-300'}>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className={`p-4 rounded-xl border text-xs ${isLight ? 'bg-slate-50 border-slate-200 text-slate-600' : 'bg-white/5 border-white/10 text-slate-300'}`}>
                <strong className="text-ls-cyan">Architecture Link:</strong> {selectedCap.architectureConnection}
                {selectedCap.relatedResearch && (
                  <div className="mt-2 pt-2 border-t border-slate-200/20">
                    <strong className="text-ls-cyan">Related Research:</strong>
                    {selectedCap.relatedResearch.map(link => (
                      <Link key={link.slug} to={`/insights/${link.slug}`} className="block mt-1 hover:text-white transition-colors underline">
                        {link.title} →
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Right Column: Architectural Visual & Flow Diagram */}
            <div className={`lg:col-span-5 p-6 rounded-2xl border flex flex-col justify-between overflow-hidden relative ${
              isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'
            }`}>
              <div>
                {/* Architectural visual placeholder - the source asset set is not
                    part of this repository, so this panel is rendered in CSS
                    rather than pointing at a path that does not resolve. */}
                <div className="relative w-full aspect-video rounded-xl overflow-hidden mb-6 border border-white/10 shadow-lg group">
                  <div
                    aria-hidden="true"
                    className={`absolute inset-0 ${
                      isLight
                        ? 'bg-gradient-to-br from-ls-navy via-ls-navy/80 to-ls-cyan/30'
                        : 'bg-gradient-to-br from-ls-navy via-black/70 to-ls-cyan/20'
                    }`}
                  />
                  <div aria-hidden="true" className="absolute inset-0 flex items-center justify-center">
                    <Icon3D name={selectedCap.icon3d} size="lg" />
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex items-end p-3">
                    <span className="text-[10px] font-mono font-bold text-white tracking-widest uppercase bg-black/60 px-2.5 py-1 rounded backdrop-blur-sm border border-white/20">
                      Capability {selectedCap.num} Architecture
                    </span>
                  </div>
                </div>

                <span className="text-[10px] font-mono font-bold text-ls-cyan uppercase tracking-widest block mb-1">
                  Execution Flow Diagram
                </span>
                <h4 className={`text-base font-bold font-display mb-4 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  {selectedCap.diagramTitle}
                </h4>

                <div className="space-y-2.5 relative">
                  {selectedCap.diagramSteps.map((step, idx) => (
                    <div key={idx} className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono transition-all hover:translate-x-1 ${
                      isLight ? 'bg-white border-slate-200 text-ls-navy hover:border-ls-cyan' : 'bg-white/5 border-white/10 text-white hover:border-ls-cyan/50'
                    }`}>
                      <div className="flex items-center gap-3">
                        <span className="w-5 h-5 rounded bg-ls-cyan/20 text-ls-cyan text-[10px] font-bold flex items-center justify-center">
                          0{idx + 1}
                        </span>
                        <span>{step}</span>
                      </div>
                      <ArrowUpRight className="w-3.5 h-3.5 opacity-40 text-ls-cyan" />
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-8 pt-4 border-t border-slate-200/20 text-[10px] font-mono text-slate-400 flex items-center justify-between">
                <span>HAOMTGV Grounded</span>
                <span className="text-ls-cyan font-bold">Verified Architecture</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SixCapabilitiesSection;
