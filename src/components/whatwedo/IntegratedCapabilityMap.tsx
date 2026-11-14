import React, { useState } from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Network, ArrowRight, Layers, CheckCircle2 } from 'lucide-react';

interface MappingRow {
  id: string;
  capability: string;
  primaryPillars: string[];
  connectionDescription: string;
}

const MAPPING_ROWS: MappingRow[] = [
  { id: 'map-1', capability: 'AI-Native Company Building', primaryPillars: ['H', 'O', 'V'], connectionDescription: 'Human direction initiates company creation; Orchestration coordinates workforce; Value cycle measures ROI.' },
  { id: 'map-2', capability: 'Intelligent Workflow Automation', primaryPillars: ['A', 'T', 'G'], connectionDescription: 'Specialized Agents invoke System Tools guarded by automated 5-tier Governance gates.' },
  { id: 'map-3', capability: 'Agentic Systems & Orchestration', primaryPillars: ['A', 'O', 'M'], connectionDescription: 'Multi-agent networks coordinated by Orchestration engine grounded in Organizational Memory.' },
  { id: 'map-4', capability: 'Enterprise AI Integration', primaryPillars: ['T', 'G'], connectionDescription: 'API sandboxes and tool gateways secured by risk-classified compliance checks.' },
  { id: 'map-5', capability: 'Organizational Memory & Knowledge', primaryPillars: ['M', 'A'], connectionDescription: 'Vector context stores providing domain grounding for every agent decision.' },
  { id: 'map-6', capability: 'AI Governance & Decision Infrastructure', primaryPillars: ['G', 'H'], connectionDescription: 'Continuous oversight layer holding human approval authority at sovereign gates.' },
];

const ALL_PILLARS = [
  { code: 'H', label: 'Human Direction', role: 'Sovereign Authority' },
  { code: 'A', label: 'Specialized Agents', role: 'Task Execution' },
  { code: 'O', label: 'Orchestration Engine', role: 'Routing & State' },
  { code: 'M', label: 'Organizational Memory', role: 'Vector Grounding' },
  { code: 'T', label: 'System Tools', role: 'Sandboxed Integrations' },
  { code: 'G', label: 'Governance Control', role: '5-Tier Approvals' },
  { code: 'V', label: 'Measurable Value', role: 'Continuous Optimization' },
];

interface IntegratedCapabilityMapProps {
  theme?: 'light' | 'dark';
}

export const IntegratedCapabilityMap: React.FC<IntegratedCapabilityMapProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';
  const [selectedCap, setSelectedCap] = useState<string>('map-1');

  const activeRow = MAPPING_ROWS.find((r) => r.id === selectedCap) || MAPPING_ROWS[0];

  return (
    <section id="capability-map" className={`py-24 px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
      isLight ? 'bg-white text-ls-navy' : 'bg-[#070A40] text-white'
    }`}>
      <div className="max-w-7xl mx-auto relative z-10">
        <SectionHeading
          theme={theme}
          eyebrow="ARCHITECTURE MATRIX"
          title="Integrated Capability-to-HAOMTGV Map"
          lead="Interactive relationship architecture connecting LightSpeed's six capability areas directly into the seven HAOMTGV operating pillars."
        />

        {/* Interactive Interactive Topology Visualizer */}
        <div className={`mt-14 p-6 lg:p-8 rounded-2xl border backdrop-blur-xl transition-all ${
          isLight ? 'bg-slate-50/90 border-slate-200 shadow-xl' : 'bg-black/50 border-white/10 shadow-2xl'
        }`}>
          <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-slate-200/20">
            <div className="flex items-center gap-2.5 text-xs font-mono font-bold tracking-wider text-ls-cyan">
              <Network className="w-4 h-4" />
              <span>DYNAMIC MAPPING GRAPH: SELECT A PRACTICE AREA</span>
            </div>
            <div className="flex items-center gap-4 text-[11px] font-mono">
              <span className="flex items-center gap-1.5 text-ls-red font-bold">
                <span className="w-2.5 h-2.5 rounded-full bg-ls-red inline-block" />
                Sovereign / Governance
              </span>
              <span className="flex items-center gap-1.5 text-ls-cyan font-bold">
                <span className="w-2.5 h-2.5 rounded-full bg-ls-cyan inline-block" />
                Coordinated Architecture
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left: Capability Node Selector */}
            <div className="lg:col-span-5 space-y-2.5">
              <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400 block mb-2">
                Enterprise Capabilities (Select to trace)
              </span>
              {MAPPING_ROWS.map((row) => {
                const isSelected = row.id === selectedCap;
                return (
                  <button
                    key={row.id}
                    onClick={() => setSelectedCap(row.id)}
                    style={isSelected ? { borderTop: '1px solid #1e2d3d' } : undefined}
                    className={`w-full p-4 rounded-xl border text-left transition-all cursor-pointer flex items-center justify-between group ${
                      isSelected
                        ? isLight
                          ? 'bg-ls-navy text-white border-ls-navy shadow-lg ring-1 ring-ls-cyan border-t border-t-[#1e2d3d]'
                          : 'bg-ls-cyan/20 text-white border-ls-cyan shadow-xl ring-1 ring-ls-cyan border-t border-t-[#1e2d3d]'
                        : isLight
                          ? 'bg-white text-ls-navy border-slate-200 hover:border-slate-300'
                          : 'bg-white/5 text-slate-300 border-white/5 hover:border-white/20'
                    }`}
                  >
                    <div>
                      <h4 className="text-xs font-bold font-display leading-tight">{row.capability}</h4>
                      <div className="flex items-center gap-1 mt-2">
                        {row.primaryPillars.map((p) => (
                          <span
                            key={p}
                            className={`w-5 h-5 rounded text-[10px] font-mono font-bold flex items-center justify-center ${
                              p === 'H' || p === 'G'
                                ? 'bg-ls-red text-white'
                                : 'bg-ls-cyan/20 text-ls-cyan'
                            }`}
                          >
                            {p}
                          </span>
                        ))}
                      </div>
                    </div>
                    <ArrowRight className={`w-4 h-4 transition-transform ${isSelected ? 'translate-x-1 text-ls-cyan' : 'opacity-40 group-hover:translate-x-1'}`} />
                  </button>
                );
              })}
            </div>

            {/* Right: Traced HAOMTGV Pillar Matrix */}
            <div className={`lg:col-span-7 p-6 rounded-xl border flex flex-col justify-between ${
              isLight ? 'bg-white border-slate-200' : 'bg-black/40 border-white/10'
            }`}>
              <div>
                <div className="flex items-center justify-between pb-4 mb-6 border-b border-slate-200/20">
                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-widest text-ls-cyan block">
                      Active Traced Mapping
                    </span>
                    <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                      {activeRow.capability}
                    </h3>
                  </div>
                  <span className="text-xs font-mono font-bold text-ls-cyan px-2.5 py-1 rounded bg-ls-cyan/10">
                    {activeRow.primaryPillars.length} Linked Pillars
                  </span>
                </div>

                {/* 7 Pillars Visual Connectors */}
                <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400 block mb-3">
                  Pillar Architecture Trace
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5 mb-6">
                  {ALL_PILLARS.map((p) => {
                    const isLinked = activeRow.primaryPillars.includes(p.code);
                    return (
                      <div
                        key={p.code}
                        className={`p-3 rounded-lg border transition-all ${
                          isLinked
                            ? p.code === 'H' || p.code === 'G'
                              ? 'bg-ls-red/15 border-ls-red text-ls-red font-bold shadow-md ring-1 ring-ls-red/50'
                              : 'bg-ls-cyan/15 border-ls-cyan text-ls-cyan font-bold shadow-md ring-1 ring-ls-cyan/50'
                            : 'opacity-30 border-transparent bg-slate-500/5 text-slate-400'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-display font-black text-sm">{p.code}</span>
                          {isLinked && <CheckCircle2 className="w-3.5 h-3.5" />}
                        </div>
                        <div className="text-[11px] leading-tight font-display">{p.label}</div>
                        <span className="text-[9px] font-mono block mt-1 opacity-80">{p.role}</span>
                      </div>
                    );
                  })}
                </div>

                {/* Architectural Relationship Explanation */}
                <div className={`p-4 rounded-xl border text-xs leading-relaxed ${
                  isLight ? 'bg-slate-50 border-slate-200 text-slate-700' : 'bg-white/5 border-white/10 text-slate-300'
                }`}>
                  <strong className="text-ls-cyan font-mono uppercase block mb-1">Architectural Link:</strong>
                  {activeRow.connectionDescription}
                </div>
              </div>

              <div className="mt-8 pt-4 border-t border-slate-200/20 text-[10px] font-mono text-slate-400 flex items-center justify-between">
                <span>Deterministically Bounded</span>
                <span className="text-ls-cyan font-bold">SHA-256 Audit Grounded</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default IntegratedCapabilityMap;
