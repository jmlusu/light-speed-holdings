import React, { useState } from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { User, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp, Sparkles, Layers } from 'lucide-react';
import { Icon3D, Icon3DName } from '../common';

interface OperatingModelOverviewProps {
  theme?: 'light' | 'dark';
}

export const OperatingModelOverview: React.FC<OperatingModelOverviewProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';
  const [activePillar, setActivePillar] = useState<string | null>(null);

  const pillars: {
    letter: string;
    name: string;
    role: string;
    desc: string;
    icon: any;
    icon3d: Icon3DName;
    color: string;
    activeRing: string;
    tier: string;
  }[] = [
    {
      letter: 'H',
      name: 'Human Direction',
      role: 'Sovereign Leader',
      desc: 'Sets intent, defines policy boundaries, and retains absolute decision authority.',
      icon: User,
      icon3d: 'users',
      color: 'text-ls-red bg-ls-red/10 border-ls-red/30',
      activeRing: 'ring-2 ring-ls-red shadow-lg shadow-ls-red/20',
      tier: 'Sovereign Governance Tier',
    },
    {
      letter: 'A',
      name: 'Specialized Agents',
      role: 'Executing Units',
      desc: 'Scoped AI roles executing discrete sub-tasks with bounded permission limits.',
      icon: Bot,
      icon3d: 'intelligence',
      color: 'text-ls-cyan bg-ls-cyan/10 border-ls-cyan/30',
      activeRing: 'ring-2 ring-ls-cyan shadow-lg shadow-ls-cyan/20',
      tier: 'Execution Layer',
    },
    {
      letter: 'O',
      name: 'Orchestration Engine',
      role: 'Deterministic Router',
      desc: 'Task graph decomposition and automated dependency management.',
      icon: GitBranch,
      icon3d: 'orchestration',
      color: 'text-ls-cyan bg-ls-cyan/10 border-ls-cyan/30',
      activeRing: 'ring-2 ring-ls-cyan shadow-lg shadow-ls-cyan/20',
      tier: 'Coordination Layer',
    },
    {
      letter: 'M',
      name: 'Organizational Memory',
      role: 'Context Store',
      desc: 'Persistent vector database providing long-term enterprise domain grounding.',
      icon: HardDrive,
      icon3d: 'memory',
      color: 'text-ls-cyan bg-ls-cyan/10 border-ls-cyan/30',
      activeRing: 'ring-2 ring-ls-cyan shadow-lg shadow-ls-cyan/20',
      tier: 'Persistent Context Store',
    },
    {
      letter: 'T',
      name: 'System Tools',
      role: 'Execution Sandboxes',
      desc: 'Isolated API integrations and secure connectors for real-world execution.',
      icon: Wrench,
      icon3d: 'tools',
      color: 'text-ls-cyan bg-ls-cyan/10 border-ls-cyan/30',
      activeRing: 'ring-2 ring-ls-cyan shadow-lg shadow-ls-cyan/20',
      tier: 'Execution Sandboxes',
    },
    {
      letter: 'G',
      name: 'Governance Control',
      role: '5-Tier Approval Gate',
      desc: 'Continuous risk classification and append-only SHA-256 audit logging.',
      icon: ShieldCheck,
      icon3d: 'safe',
      color: 'text-ls-red bg-ls-red/10 border-ls-red/30',
      activeRing: 'ring-2 ring-ls-red shadow-lg shadow-ls-red/20',
      tier: 'Policy & Guardrail Matrix',
    },
    {
      letter: 'V',
      name: 'Measurable Value',
      role: 'Outcome Benchmark',
      desc: 'Operational cost, turnaround SLA, and quality feedback loops.',
      icon: TrendingUp,
      icon3d: 'chart',
      color: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/30',
      activeRing: 'ring-2 ring-emerald-500 shadow-lg shadow-emerald-500/20',
      tier: 'Economic Outcome Tier',
    },
  ];

  return (
    <section id="operating-model" className={`py-24 px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
      isLight ? 'bg-white text-ls-navy' : 'bg-[#070A40] text-white'
    }`}>
      <div className="max-w-7xl mx-auto relative z-10">
        <SectionHeading
          theme={theme}
          eyebrow="THE AI-NATIVE COMPANY BUILDER"
          title="An Operating Model Built Around Seven HAOMTGV Pillars"
          lead="LightSpeed Holdings does not deploy standalone AI tools. We engineer complete operating models where human authority directs coordinated agent execution across a bounded, auditable architecture."
        />

        {/* Interactive Architecture Visual Overview */}
        <div className="mt-12 p-6 rounded-2xl border backdrop-blur-md transition-all ${
          isLight ? 'bg-slate-50/80 border-slate-200' : 'bg-black/30 border-white/10'
        }">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-200/20">
            <div className="flex items-center gap-2 text-xs font-mono font-bold tracking-wider text-ls-cyan">
              <Layers className="w-4 h-4" />
              <span>INTERACTIVE SEVEN-PILLAR STACK</span>
            </div>
            <span className="text-[11px] font-mono text-slate-400">
              Hover or select a pillar to inspect operational boundaries
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3">
            {pillars.map((p) => {
              const Icon = p.icon;
              const isActive = activePillar === p.letter;
              return (
                <button
                  key={p.letter}
                  type="button"
                  onMouseEnter={() => setActivePillar(p.letter)}
                  onClick={() => setActivePillar(isActive ? null : p.letter)}
                  className={`p-4 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                    isActive
                      ? p.activeRing + (isLight ? ' bg-white' : ' bg-white/15')
                      : isLight
                        ? 'bg-white/70 border-slate-200 hover:border-slate-300'
                        : 'bg-white/5 border-white/10 hover:border-white/20'
                  }`}
                  aria-pressed={isActive}
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className={`w-8 h-8 rounded-lg font-display font-black text-sm flex items-center justify-center border ${p.color}`}>
                      {p.letter}
                    </span>
                    <Icon3D name={p.icon3d} size="xs" />
                  </div>
                  <div>
                    <h4 className={`text-xs font-bold font-display leading-snug ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                      {p.name}
                    </h4>
                    <span className={`text-[9px] font-mono block mt-1 ${isLight ? 'text-slate-500' : 'text-ls-cyan'}`}>
                      {p.role}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Active Pillar Inspector Box */}
          {activePillar && (
            <div className={`mt-6 p-4 rounded-xl border animate-fadeIn text-left ${
              isLight ? 'bg-white border-slate-200' : 'bg-black/50 border-white/15'
            }`}>
              {(() => {
                const selected = pillars.find((p) => p.letter === activePillar);
                if (!selected) return null;
                return (
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <Icon3D name={selected.icon3d} size="sm" />
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-ls-cyan px-2 py-0.5 rounded bg-ls-cyan/10">
                            PILLAR {selected.letter}
                          </span>
                          <h4 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                            {selected.name} — {selected.role}
                          </h4>
                        </div>
                        <p className={`text-xs mt-1.5 ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                          {selected.desc}
                        </p>
                      </div>
                    </div>
                    <div className="shrink-0 text-right">
                      <span className="text-[10px] font-mono uppercase px-2.5 py-1 rounded bg-ls-red/10 text-ls-red border border-ls-red/20 font-bold">
                        {selected.tier}
                      </span>
                    </div>
                  </div>
                );
              })()}
            </div>
          )}
        </div>

        {/* Detailed 7 Pillars Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-10">
          {pillars.map((p) => {
            const isHighlighted = activePillar === p.letter;
            return (
              <div
                key={p.letter}
                onMouseEnter={() => setActivePillar(p.letter)}
                className={`p-6 rounded-2xl border transition-all text-left flex flex-col justify-between ${
                  isHighlighted
                    ? isLight
                      ? 'bg-white border-ls-cyan shadow-xl ring-1 ring-ls-cyan'
                      : 'bg-white/10 border-ls-cyan shadow-2xl ring-1 ring-ls-cyan'
                    : isLight
                      ? 'bg-ls-grey-light/40 border-slate-200 hover:shadow-md'
                      : 'bg-white/5 border-white/10 hover:border-ls-cyan/30 hover:shadow-xl'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className={`w-10 h-10 rounded-xl font-display font-black text-lg flex items-center justify-center border ${p.color}`}>
                      {p.letter}
                    </span>
                    <Icon3D name={p.icon3d} size="sm" />
                  </div>

                  <h3 className={`text-base font-bold font-display mb-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                    {p.name}
                  </h3>

                  <span className={`text-[10px] font-mono block mb-3 ${isLight ? 'text-slate-500' : 'text-ls-cyan'}`}>
                    {p.role}
                  </span>

                  <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                    {p.desc}
                  </p>
                </div>

                <div className={`mt-6 pt-3 border-t text-[10px] font-mono flex items-center justify-between ${
                  isLight ? 'border-slate-200 text-slate-400' : 'border-white/10 text-slate-500'
                }`}>
                  <span>{p.tier}</span>
                  <span className="text-ls-cyan font-bold">HAOMTGV</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default OperatingModelOverview;
