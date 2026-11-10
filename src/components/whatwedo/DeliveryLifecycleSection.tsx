import React, { useState } from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Compass, Search, Layout, ShieldCheck, Cpu, Code2, CheckCircle, BarChart3, ArrowRight, RotateCw } from 'lucide-react';
import { Icon3D, Icon3DName } from '../common';

interface Stage {
  stage: number;
  title: string;
  focus: string;
  description: string;
  icon: any;
  icon3d: Icon3DName;
  deliverables: string;
}

const DELIVERY_STAGES: readonly [Stage, ...Stage[]] = [
  { stage: 1, title: 'Understand Intent & Objectives', focus: 'Strategic Alignment', description: 'Clarify leadership intent, expected business outcomes, and key performance targets.', icon: Compass, icon3d: 'compass', deliverables: 'Executive Intent Charter & Scope Boundary' },
  { stage: 2, title: 'Assess Workflows & Constraints', focus: 'Baseline Discovery', description: 'Map existing manual processes, data silos, network limits, and regional compliance needs.', icon: Search, icon3d: 'intelligence', deliverables: 'Friction Topology & Latency Baseline' },
  { stage: 3, title: 'Design Target Operating Model', focus: 'HAOMTGV Blueprinting', description: 'Define the target AI-native structure combining human leadership and agentic automation.', icon: Layout, icon3d: 'home', deliverables: 'Target Architecture & Role Taxonomy' },
  { stage: 4, title: 'Define Governance Boundaries', focus: 'Approval Gates', description: 'Establish 5-tier approval thresholds, risk classification, and decision rights.', icon: ShieldCheck, icon3d: 'safe', deliverables: 'Decision Matrix & Cryptographic Policy' },
  { stage: 5, title: 'Architect HAOMTGV Stack', focus: 'Technical Specs', description: 'Configure specialized agent roles, vector memory schemas, and API tool sandboxes.', icon: Cpu, icon3d: 'orchestration', deliverables: 'Agent Task Graphs & Sandboxed Schemas' },
  { stage: 6, title: 'Build & Integrate', focus: 'Iterative Sprints', description: 'Develop agent workflows, integrate mobile-money/ERP APIs, and run regression suites.', icon: Code2, icon3d: 'tools', deliverables: 'Tested Workflows & Verified Connectors' },
  { stage: 7, title: 'Validate & Authorize', focus: 'Gate Sign-Off', description: 'Run G1–G4 security/DPA reviews and obtain human executive sign-off before launch.', icon: CheckCircle, icon3d: 'verification', deliverables: 'Executive Authorization & Audit Ledger Entry' },
  { stage: 8, title: 'Measure, Learn & Improve', focus: 'Continuous Value', description: 'Track latency, cost, and quality KPIs to continuously optimize agent memory and prompts.', icon: BarChart3, icon3d: 'chart', deliverables: 'Continuous SLA Feedback Loop' },
];

interface DeliveryLifecycleSectionProps {
  theme?: 'light' | 'dark';
}

export const DeliveryLifecycleSection: React.FC<DeliveryLifecycleSectionProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';
  const [activeStage, setActiveStage] = useState<number>(1);

  const currentStage = DELIVERY_STAGES.find((s) => s.stage === activeStage) || DELIVERY_STAGES[0];

  return (
    <section id="delivery-lifecycle" className={`py-24 px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
      isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-[#0A0D14] text-white'
    }`}>
      <div className="max-w-7xl mx-auto relative z-10">
        <SectionHeading
          theme={theme}
          eyebrow="DELIVERY APPROACH"
          title="Eight-Stage Delivery Lifecycle"
          lead="Explanatory model detailing how LightSpeed moves projects from strategic intent to governed, operational capability in a continuous improvement loop."
        />

        {/* Continuous Pathway Stepper Visualizer */}
        <div className={`mt-14 p-6 lg:p-8 rounded-2xl border backdrop-blur-xl transition-all ${
          isLight ? 'bg-white/90 border-slate-200 shadow-xl' : 'bg-black/50 border-white/10 shadow-2xl'
        }`}>
          <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-slate-200/20">
            <div className="flex items-center gap-2.5 text-xs font-mono font-bold tracking-wider text-ls-cyan">
              <RotateCw className="w-4 h-4 animate-spin-slow" />
              <span>CONTINUOUS VALUE DELIVERY PATHWAY (STAGE 8 LOOPS TO 1)</span>
            </div>
            <span className="text-[11px] font-mono text-slate-400">
              Select any stage to inspect focus & key deliverables
            </span>
          </div>

          {/* Stepper Node Ribbon */}
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
            {DELIVERY_STAGES.map((s) => {
              const isActive = s.stage === activeStage;
              const isPast = s.stage < activeStage;
              const Icon = s.icon;
              return (
                <button
                  key={s.stage}
                  onClick={() => setActiveStage(s.stage)}
                  className={`p-3 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                    isActive
                      ? isLight
                        ? 'bg-ls-navy text-white border-ls-navy ring-2 ring-ls-cyan shadow-lg'
                        : 'bg-ls-cyan/20 text-white border-ls-cyan ring-2 ring-ls-cyan shadow-xl'
                      : isLight
                        ? 'bg-slate-50 text-slate-700 border-slate-200 hover:border-slate-300'
                        : 'bg-white/5 text-slate-300 border-white/5 hover:border-white/20'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                      isActive ? 'bg-ls-cyan text-ls-navy' : 'bg-slate-500/10 text-slate-400'
                    }`}>
                      0{s.stage}
                    </span>
                    <Icon3D name={s.icon3d} size="xs" />
                  </div>
                  <h4 className="text-[11px] font-bold font-display leading-tight line-clamp-2">
                    {s.title}
                  </h4>
                </button>
              );
            })}
          </div>

          {/* Active Stage Detailed Callout */}
          <div className={`mt-8 p-6 rounded-xl border flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 ${
            isLight ? 'bg-slate-50 border-slate-200 text-ls-navy' : 'bg-white/5 border-white/10 text-white'
          }`}>
            <div className="space-y-1.5 max-w-3xl flex items-start gap-4">
              <Icon3D name={currentStage.icon3d} size="md" />
              <div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono font-bold text-ls-cyan px-2.5 py-1 rounded bg-ls-cyan/10">
                    STAGE 0{currentStage.stage} OF 08
                  </span>
                  <span className="text-xs font-mono uppercase tracking-wider text-ls-red font-bold">
                    Focus: {currentStage.focus}
                  </span>
                </div>
                <h3 className="text-xl font-black font-display mt-2">{currentStage.title}</h3>
                <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                  {currentStage.description}
                </p>
              </div>
            </div>

            <div className={`p-4 rounded-xl border text-left shrink-0 w-full lg:w-auto ${
              isLight ? 'bg-white border-slate-200' : 'bg-black/40 border-white/10'
            }`}>
              <span className="text-[10px] font-mono uppercase tracking-widest text-ls-cyan block mb-1">
                Primary Deliverable
              </span>
              <span className="text-xs font-bold font-display block">
                {currentStage.deliverables}
              </span>
              <div className="mt-3 flex items-center gap-2 text-[10px] font-mono text-slate-400">
                <span>Next:</span>
                <span className="text-ls-cyan font-bold">
                  {currentStage.stage === 8 ? 'Stage 01 (Continuous Loop)' : `Stage 0${currentStage.stage + 1}`}
                </span>
                <ArrowRight className="w-3 h-3 text-ls-cyan" />
              </div>
            </div>
          </div>
        </div>

        {/* 8-Stage Detailed Grid Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
          {DELIVERY_STAGES.map((s) => {
            const Icon = s.icon;
            const isSelected = s.stage === activeStage;
            return (
              <div
                key={s.stage}
                onClick={() => setActiveStage(s.stage)}
                style={isSelected ? { borderTop: '1px solid #1e2d3d' } : undefined}
                className={`p-6 rounded-2xl border transition-all text-left flex flex-col justify-between cursor-pointer ${
                  isSelected
                    ? isLight
                      ? 'bg-white border-ls-cyan shadow-xl ring-1 ring-ls-cyan border-t border-t-[#1e2d3d]'
                      : 'bg-white/10 border-ls-cyan shadow-2xl ring-1 ring-ls-cyan border-t border-t-[#1e2d3d]'
                    : isLight
                      ? 'bg-white border-slate-200 hover:border-ls-navy/30 hover:shadow-lg'
                      : 'bg-white/5 border-white/10 hover:border-ls-cyan/30 hover:shadow-xl'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="w-8 h-8 rounded-lg bg-ls-cyan/20 text-ls-cyan text-xs font-mono font-bold flex items-center justify-center">
                      0{s.stage}
                    </span>
                    <Icon className="w-4 h-4 text-ls-red" />
                  </div>

                  <h3 className={`text-base font-bold font-display mb-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                    {s.title}
                  </h3>

                  <span className={`text-[10px] font-mono block mb-3 ${isLight ? 'text-slate-500' : 'text-ls-cyan'}`}>
                    {s.focus}
                  </span>

                  <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                    {s.description}
                  </p>
                </div>

                <div className={`mt-6 pt-3 border-t text-[10px] font-mono flex items-center justify-between ${
                  isLight ? 'border-slate-200 text-slate-400' : 'border-white/10 text-slate-500'
                }`}>
                  <span>Stage {s.stage} of 8</span>
                  <span className="text-ls-cyan font-bold">{s.stage === 8 ? 'Loop back ↺' : 'Sequential'}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default DeliveryLifecycleSection;
