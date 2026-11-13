import React, { useState } from 'react';
import { Info } from 'lucide-react';
import { Icon3D, Icon3DName } from '../common';

interface PillarDetail {
  id: string;
  letter: string;
  name: string;
  role: string;
  authority: string;
  description: string;
  icon3d: Icon3DName;
  isSovereign?: boolean;
}

const PILLARS: PillarDetail[] = [
  {
    id: 'human',
    letter: 'H',
    name: 'Human Authority',
    role: 'Sovereign Direction & Final Decision',
    authority: 'Absolute Sovereign Control (Tier 5)',
    description: 'Human intent sits above the system. Leaders set policy, approve high-risk actions, and maintain total ultimate accountability over autonomous execution.',
    icon3d: 'users',
    isSovereign: true,
  },
  {
    id: 'agents',
    letter: 'A',
    name: 'Specialized Agents',
    role: 'Scoped Task Execution Units',
    authority: 'Autonomous within Bounded Roles (Tier 1-2)',
    description: 'A coordinated workforce of specialized AI agents with deterministic system tools, narrow scopes, and strict prompt guardrails.',
    icon3d: 'intelligence',
  },
  {
    id: 'orchestration',
    letter: 'O',
    name: 'Orchestration Engine',
    role: 'Deterministic Task Routing',
    authority: 'System Routing & State Management',
    description: 'Automated workflow engine that decomposes high-level human goals into agent work packages and manages data dependencies.',
    icon3d: 'orchestration',
  },
  {
    id: 'memory',
    letter: 'M',
    name: 'Organizational Memory',
    role: 'Persistent Context & Knowledge Base',
    authority: 'Read-Only Enterprise Context Store',
    description: 'Long-term vector database and structured domain knowledge store that provides grounding context across multi-step operations.',
    icon3d: 'memory',
  },
  {
    id: 'tools',
    letter: 'T',
    name: 'System Tools',
    role: 'Authorized Capability Interfaces',
    authority: 'API & Execution Gateways',
    description: 'Isolated API integrations, database connectors, and code environments that agents invoke under strict permission scopes.',
    icon3d: 'tools',
  },
  {
    id: 'governance',
    letter: 'G',
    name: 'Governance Layer',
    role: '5-Tier Approval & Audit Trail',
    authority: 'Cryptographic Policy Enforcement Gate',
    description: 'Continuous oversight layer enforcing risk classification, contract checks, data privacy gates, and append-only SHA-256 logs.',
    icon3d: 'governance',
  },
  {
    id: 'value',
    letter: 'V',
    name: 'Measurable Value',
    role: 'Business Outcomes & Feedback Loop',
    authority: 'Strategic ROI & Feedback Measurement',
    description: 'Operational performance metrics, latency reduction, and quality outcomes fed back into continuous system optimization.',
    icon3d: 'value',
  },
];

interface HAOMTGVVisualizationProps {
  theme?: 'light' | 'dark';
}

export const HAOMTGVVisualization: React.FC<HAOMTGVVisualizationProps> = ({ theme = 'dark' }) => {
  const [activePillar, setActivePillar] = useState<PillarDetail>(PILLARS[0]);
  const isLight = theme === 'light';

  return (
    <div className={`w-full max-w-5xl mx-auto rounded-2xl p-6 sm:p-8 border transition-all ${
      isLight ? 'bg-white border-slate-200 shadow-md' : 'bg-[#070A40]/80 border-white/10 shadow-2xl'
    }`}>
      {/* Node Selector Bar */}
      <div className="flex flex-wrap items-center justify-between gap-2 sm:gap-3 pb-8 border-b border-white/10">
        {PILLARS.map((p) => {
          const isSelected = p.id === activePillar.id;
          return (
            <button
              key={p.id}
              onClick={() => setActivePillar(p)}
              className={`flex-1 min-w-[70px] sm:min-w-[90px] p-3 rounded-xl flex flex-col items-center justify-center transition-all cursor-pointer ${
                isSelected
                  ? p.isSovereign
                    ? 'bg-ls-red text-white shadow-lg ring-2 ring-ls-red/50'
                    : 'bg-ls-cyan text-ls-navy font-bold shadow-lg ring-2 ring-ls-cyan/50'
                  : isLight
                    ? 'bg-slate-100 text-ls-navy hover:bg-slate-200'
                    : 'bg-white/5 text-slate-300 hover:bg-white/10'
              }`}
            >
              <span className="font-display font-black text-xl leading-none">{p.letter}</span>
              <span className="text-[10px] font-bold tracking-tight mt-1 truncate max-w-full">
                {p.name.split(' ')[0]}
              </span>
            </button>
          );
        })}
      </div>

      {/* Selected Pillar Detailed Inspector */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
        {/* Left Column: 3D Icon & Letter */}
        <div className="md:col-span-4 flex flex-col items-center justify-center text-center p-6 rounded-2xl bg-ls-navy/10 border border-ls-cyan/20">
          <div className="mb-4 flex items-center justify-center">
            <Icon3D name={activePillar.icon3d} size="hero" isInteractive />
          </div>
          <span className="text-xs font-mono font-bold tracking-widest uppercase text-ls-cyan mb-1">
            HAOMTGV Pillar [{activePillar.letter}]
          </span>
          <h3 className={`text-2xl font-black font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            {activePillar.name}
          </h3>
          <span className={`mt-2 text-xs font-mono px-3 py-1 rounded-full ${
            activePillar.isSovereign
              ? 'bg-ls-red/20 text-ls-red font-bold'
              : 'bg-ls-cyan/20 text-ls-cyan font-semibold'
          }`}>
            {activePillar.authority}
          </span>
        </div>

        {/* Right Column: Description & Role */}
        <div className="md:col-span-8 space-y-4 text-left">
          <div className="flex items-center gap-2">
            <Info className="w-4 h-4 text-ls-cyan" />
            <span className={`text-xs font-mono font-bold uppercase tracking-wider ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
              System Role & Governance Context
            </span>
          </div>

          <h4 className={`text-lg font-bold ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            {activePillar.role}
          </h4>

          <p className={`text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-slate-200'}`}>
            {activePillar.description}
          </p>

          <div className={`p-4 rounded-xl border text-xs leading-relaxed ${
            isLight ? 'bg-slate-50 border-slate-200 text-slate-600' : 'bg-white/5 border-white/10 text-slate-300'
          }`}>
            <strong className="text-ls-cyan">Human Authority Note:</strong> Human intent (H) provides sovereign direction at the apex, while Governance (G) acts as the continuous enforcement loop securing all agent actions (A) and tools (T).
          </div>
        </div>
      </div>
    </div>
  );
};

export default HAOMTGVVisualization;
