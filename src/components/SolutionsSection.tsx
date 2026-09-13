import React, { useState } from 'react';
import { 
  Bot, 
  Layers, 
  Database, 
  Workflow, 
  Compass, 
  ShieldCheck, 
  ArrowRight, 
  CheckCircle2, 
  ChevronRight,
  Cpu,
  Brain,
  Zap
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille, 
  ChassisPanel 
} from './TactileHardwareElements';
import { ReservationsProbingDemo } from './ReservationsProbingDemo';
import sovereignDatacenterRacks from '../assets/images/sovereign_datacenter_racks_1789251006883.jpg';

interface SolutionsSectionProps {
  initialSubSection?: string;
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const SolutionsSection: React.FC<SolutionsSectionProps> = ({
  initialSubSection = 'agentic-ai',
  onOpenContactModal,
  theme = 'dark'
}) => {
  const [activeSolution, setActiveSolution] = useState<string>(initialSubSection);
  const isLight = theme === 'light';

  const solutionsData = [
    {
      id: 'agentic-ai',
      title: 'Agentic AI Systems',
      icon: Bot,
      tagline: 'Autonomous AI Agents & Multi-Agent Swarms',
      description: 'We build intelligent, goal-directed AI agent systems capable of executing complex multi-step business workflows with sub-second orchestration latency.',
      subItems: [
        'Agentic AI Systems & Multi-Agent Swarms',
        'Custom AI Agent Specification & Tooling',
        'Autonomous Workflow Execution & SLA Monitors',
        'AI Operating Model Integration',
        'AI Company Builder Architecture'
      ],
      outcomes: [
        '10x faster execution compared to manual processing',
        '100% auditable tool invocation logs',
        'Sub-second task dispatch latency across regional nodes'
      ],
      architectureNote: 'Built on modular OpenCode agent specifications with native human-in-the-loop (HITL) permission gates.'
    },
    {
      id: 'digital-transformation',
      title: 'Digital Transformation',
      icon: Layers,
      tagline: 'Enterprise Modernization for the AI Era',
      description: 'Modernize core legacy infrastructure into cloud-native, API-first enterprise platforms ready for agentic automation.',
      subItems: [
        'Digital Strategy & Roadmap',
        'Enterprise Architecture Modernization',
        'Cloud & Platform Engineering',
        'Data & Analytics Infrastructure',
        'Technology Modernisation'
      ],
      outcomes: [
        'Elimination of legacy technical debt bottlenecks',
        'High-availability cloud platform deployment',
        'Seamless integration with modern AI models and data pipelines'
      ],
      architectureNote: 'Designed for resilience, cloud sovereignty, and low-latency connectivity across SADC networks.'
    },
    {
      id: 'data-intelligence',
      title: 'Data & Intelligence',
      icon: Database,
      tagline: 'Semantic Fabric & Decision Support',
      description: 'Transform enterprise data into an active semantic layer that powers both automated agent reasoning and executive decision-making.',
      subItems: [
        'Data Architecture & Engineering',
        'Semantic Fabric & Knowledge Graphs',
        'Business Intelligence & Reporting',
        'Market Intelligence & Macro Feeds',
        'AI-Powered Decision Intelligence'
      ],
      outcomes: [
        'Real-time data synchronization across departments',
        'Context-aware retrieval for domain AI agents',
        'Automated executive briefing generation'
      ],
      architectureNote: 'Employs vector indexing, graph relational models, and local model proxies for maximum privacy.'
    },
    {
      id: 'automation',
      title: 'Intelligent Automation',
      icon: Workflow,
      tagline: 'Workflow Collapse & Process Redesign',
      description: 'Collapse long, inefficient operational approval chains into rapid automated sequences backed by strict SLA enforcement.',
      subItems: [
        'Workflow Automation Engine',
        'Intelligent Process Automation (IPA)',
        'Business Process Redesign',
        'Workflow Collapse Strategy'
      ],
      outcomes: [
        'Up to 80% reduction in operational cycle times',
        'Automated exception routing and escalation',
        'Consistent compliance with internal SOPs'
      ],
      architectureNote: 'Replaces rigid legacy RPA with adaptive, generative sub-agents that handle complex exceptions.'
    },
    {
      id: 'strategy-advisory',
      title: 'Strategy & Advisory',
      icon: Compass,
      tagline: 'Executive AI Strategy & Transformation',
      description: 'Strategic advisory for C-suite executives, government leaders, and boards navigating the transition to AI-native enterprise models.',
      subItems: [
        'AI Strategy & Commercial Roadmaps',
        'Digital Transformation Consulting',
        'Technology Strategy & Architecture',
        'Executive Advisory & Board Briefings',
        'Transformation Roadmaps & PMO'
      ],
      outcomes: [
        'Clear, actionable 12-to-36 month AI adoption roadmap',
        'Risk-adjusted technology investment strategy',
        'Board-level alignment on sovereign AI opportunities'
      ],
      architectureNote: 'Grounded in real African and SADC economic realities and enterprise constraints.'
    },
    {
      id: 'ai-policy-governance',
      title: 'AI Governance & Policy',
      icon: ShieldCheck,
      tagline: 'Responsible AI, Policy & Regulatory Rigs',
      description: 'Establish comprehensive AI governance frameworks, risk controls, and regulatory compliance mechanisms for public and private institutions.',
      subItems: [
        'AI Governance Frameworks',
        'Responsible AI & Ethics Guidelines',
        'National & SADC AI Policy Advisory',
        'AI Risk Tiering & Security Audits',
        'Organizational AI Readiness'
      ],
      outcomes: [
        'Full compliance with regional digital policies & model laws',
        'Granular 5-tier human-in-the-loop permission hierarchy',
        'Mitigated regulatory, legal, and operational risks'
      ],
      architectureNote: 'Incorporates Pharos Policy Track standards developed for Malawi e-Government & SADC initiatives.'
    }
  ];

  const currentData = solutionsData.find(s => s.id === activeSolution) || solutionsData[0];

  return (
    <section id="solutions" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto font-sans">
      
      {/* Title & Classification */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-4 border select-none">
          <StatusLedPip status="amber" isLight={isLight} />
          <span className={`text-[10px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            COMMERCIAL ENGAGEMENT ENGINE // ACTIVE DISPATCH
          </span>
        </div>
        <h2 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Enterprise Solutions</span>
        </h2>
        <p className={`text-base leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          Organized around measurable business outcomes, mathematical rigor, and sovereign institutional compliance rather than generic software prototypes.
        </p>
      </div>

      {/* Grid selector + detail layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Solution Selector Sidebar / Rocker Bank */}
        <div className="lg:col-span-4 space-y-2.5">
          {solutionsData.map((item) => {
            const Icon = item.icon;
            const isSelected = item.id === activeSolution;
            return (
              <button
                key={item.id}
                onClick={() => setActiveSolution(item.id)}
                className={`w-full p-4 rounded-2xl text-left transition-all flex items-center justify-between border relative overflow-hidden group ${
                  isSelected
                    ? isLight
                      ? 'chassis-milled-light border-amber-500 text-slate-900 shadow-md ring-1 ring-amber-500/50'
                      : 'chassis-milled-dark border-amber-500/60 text-zinc-100 shadow-lg shadow-amber-500/10 ring-1 ring-amber-500/30'
                    : isLight
                      ? 'bg-slate-100/90 border-slate-300 text-slate-700 hover:bg-slate-200/80'
                      : 'bg-zinc-900/60 border-zinc-800 text-zinc-300 hover:bg-zinc-800/80'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`p-2.5 rounded-xl transition-colors ${
                    isSelected 
                      ? 'bg-amber-500 text-slate-950 shadow-sm shadow-amber-500/30' 
                      : isLight 
                        ? 'bg-slate-200 text-amber-600' 
                        : 'bg-zinc-800 text-amber-400'
                  }`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <StatusLedPip status={isSelected ? 'emerald' : 'off'} isLight={isLight} />
                      <h3 className={`font-bold font-mono text-xs uppercase tracking-wide ${
                        isSelected 
                          ? (isLight ? 'text-slate-900' : 'text-zinc-100') 
                          : (isLight ? 'text-slate-700' : 'text-zinc-300')
                      }`}>{item.title}</h3>
                    </div>
                    <p className={`text-[11px] mt-0.5 ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>{item.tagline}</p>
                  </div>
                </div>
                <ChevronRight className={`w-4 h-4 transition-transform ${
                  isSelected 
                    ? 'text-amber-500 translate-x-1' 
                    : isLight 
                      ? 'text-slate-400' 
                      : 'text-zinc-600'
                }`} />
              </button>
            );
          })}
        </div>

        {/* Selected Solution Detail Panel Chassis */}
        <div className={`lg:col-span-8 p-6 sm:p-8 rounded-3xl border relative overflow-hidden transition-colors ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>
          <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
          <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
          <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
          <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

          <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b border-zinc-800">
            <div className="flex items-center gap-3.5">
              <div className="p-3 rounded-2xl bg-amber-500/10 text-amber-500 border border-amber-500/30">
                <currentData.icon className="w-7 h-7" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-0.5">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="text-xs font-mono text-amber-500 font-extrabold uppercase tracking-wider">INSTRUMENT SPECIFICATION</span>
                </div>
                <h3 className={`text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{currentData.title}</h3>
              </div>
            </div>
            <AcousticVentGrille cols={4} rows={2} isLight={isLight} />
          </div>

          {/* Strategic Solution Visual Header */}
          <div className="relative rounded-2xl overflow-hidden mb-6 border border-zinc-800 aspect-[21/9] sm:aspect-[3/1]">
            <img 
              src={sovereignDatacenterRacks}
              alt={currentData.title}
              className="w-full h-full object-cover brightness-[0.7] contrast-[1.1]"
              referrerPolicy="no-referrer"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent p-4 sm:p-6 flex flex-col justify-end">
              <span className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-widest">[ SYSTEM ARCHITECTURE INFOGRAPHIC ]</span>
              <h4 className="text-sm sm:text-base font-bold font-mono text-white">{currentData.title} Deployment Flow</h4>
            </div>
          </div>

          <p className={`text-sm sm:text-base mb-8 leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
            {currentData.description}
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            
            {/* Core Capabilities */}
            <div className={`p-5 rounded-2xl border ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}>
              <h4 className="text-xs font-mono text-amber-500 uppercase font-extrabold mb-3.5 flex items-center gap-2">
                <Cpu className="w-4 h-4" /> CORE CAPABILITIES
              </h4>
              <ul className={`space-y-2.5 text-xs ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                {currentData.subItems.map((sub, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                    <span>{sub}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Business Outcomes */}
            <div className={`p-5 rounded-2xl border ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}>
              <h4 className="text-xs font-mono text-emerald-500 uppercase font-extrabold mb-3.5 flex items-center gap-2">
                <Zap className="w-4 h-4" /> VERIFIED OUTCOMES
              </h4>
              <ul className={`space-y-2.5 text-xs ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                {currentData.outcomes.map((out, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                    <span>{out}</span>
                  </li>
                ))}
              </ul>
            </div>

          </div>

          {/* Architecture Guarantee Banner */}
          <div className={`p-4 rounded-xl border text-xs font-mono flex items-center gap-3 mb-8 ${
            isLight 
              ? 'bg-amber-50 border-amber-300 text-slate-800' 
              : 'bg-zinc-950 border-amber-500/30 text-zinc-300'
          }`}>
            <Brain className="w-5 h-5 text-amber-500 shrink-0" />
            <span><strong className="text-amber-500">ARCHITECTURE GUARANTEE:</strong> {currentData.architectureNote}</span>
          </div>

          {/* CTA Button */}
          <div className={`flex justify-end pt-4 border-t ${isLight ? 'border-slate-300' : 'border-zinc-800'}`}>
            <button
              onClick={() => onOpenContactModal(`Discuss ${currentData.title}`)}
              className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 active:scale-95"
            >
              <span>Engage on {currentData.title}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

        </div>

      </div>

      {/* Interactive Client Reservations-Probing Demo Module */}
      <ReservationsProbingDemo
        theme={theme}
        onOpenContactModal={onOpenContactModal}
      />

    </section>
  );
};
