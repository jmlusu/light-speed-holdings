import React from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Icon3D, Icon3DName } from '../common';

interface LifecycleStep {
  step: number;
  title: string;
  role: string;
  description: string;
  icon3d: Icon3DName;
  highlight?: boolean;
}

const LIFECYCLE_STEPS: LifecycleStep[] = [
  { step: 1, title: 'Human Intent', role: 'Human Leadership', description: 'Executive sets strategic goal, operational constraints, and risk boundary.', icon3d: 'users', highlight: true },
  { step: 2, title: 'Planning', role: 'Chief Architect Agent', description: 'Evaluates capability registry, memory, and required tool integrations.', icon3d: 'compass' },
  { step: 3, title: 'Decomposition', role: 'Orchestrator Engine', description: 'Breaks complex goals into deterministic, executable sub-task sequences.', icon3d: 'intelligence' },
  { step: 4, title: 'Agent Assignment', role: 'Workforce Dispatcher', description: 'Routes sub-tasks to specialized agent roles based on skill and permission.', icon3d: 'orchestration' },
  { step: 5, title: 'Orchestration', role: 'Execution Pipeline', description: 'Coordinates concurrent agent execution, dependency graph, and state locks.', icon3d: 'network' },
  { step: 6, title: 'Tool Execution', role: 'Tool Sandbox', description: 'Agents invoke isolated APIs, databases, and code environments.', icon3d: 'tools' },
  { step: 7, title: 'Governance & Auth', role: '5-Tier Approval Gate', description: 'Enforces risk threshold checks; escalates to human approver if required.', icon3d: 'safe', highlight: true },
  { step: 8, title: 'Results', role: 'Output Compiler', description: 'Aggregates structured artifacts, reports, and code diffs for delivery.', icon3d: 'verification' },
  { step: 9, title: 'Measurement', role: 'Value Tracker', description: 'Evaluates outcome against latency, cost, and quality benchmarks.', icon3d: 'chart' },
  { step: 10, title: 'Memory & Feedback', role: 'Organizational Memory', description: 'Appends SHA-256 audit receipt and updates vector context for future runs.', icon3d: 'memory' },
];

interface IntentToExecutionLifecycleProps {
  theme?: 'light' | 'dark';
}

export const IntentToExecutionLifecycle: React.FC<IntentToExecutionLifecycleProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';

  return (
    <section id="lifecycle" className={`py-24 px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
      isLight ? 'bg-white text-ls-navy' : 'bg-[#070A40] text-white'
    }`}>
      {/* Background Architectural Pathway Destination Visual */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src="/src/assets/images/cta_pathway_destination_1793817195986.jpg"
          alt="Intent to Execution Pathway Architecture Visual"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-65 dark:opacity-75 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Clear Atmospheric Scrim Overlay for optimal contrast & typography clarity */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-white/70 via-white/45 to-white/75'
              : 'bg-gradient-to-b from-[#070A40]/75 via-[#070A40]/50 to-[#070A40]/80'
          }`}
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <SectionHeading
          theme={theme}
          eyebrow="OPERATIONAL LIFECYCLE"
          title="From Human Intent to Executable Value"
          lead="The 10-stage lifecycle governing every operation at LightSpeed Holdings. Human direction initiates the sequence, governance guards every transition, and persistent memory learns from every outcome."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mt-16">
          {LIFECYCLE_STEPS.map((s) => {
            return (
              <div
                key={s.step}
                className={`p-5 rounded-2xl border transition-all duration-300 flex flex-col justify-between text-left backdrop-blur-xl ${
                  s.highlight
                    ? isLight
                      ? 'bg-ls-navy/95 text-white border-ls-navy shadow-xl'
                      : 'bg-ls-cyan/20 border-ls-cyan text-white shadow-[0_0_24px_rgba(0,191,255,0.25)]'
                    : isLight
                      ? 'bg-white/85 border-slate-200/90 text-ls-navy shadow-md hover:border-slate-300'
                      : 'bg-[#070A40]/75 border-white/10 text-white shadow-lg hover:border-white/20'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className={`text-xs font-mono font-bold ${
                      s.highlight ? 'text-ls-cyan' : (isLight ? 'text-slate-500' : 'text-slate-400')
                    }`}>
                      STAGE 0{s.step}
                    </span>
                    <Icon3D name={s.icon3d} size="sm" />
                  </div>

                  <h3 className={`text-sm font-bold font-display mb-1 ${
                    s.highlight ? 'text-white' : (isLight ? 'text-ls-navy' : 'text-white')
                  }`}>
                    {s.title}
                  </h3>

                  <span className={`text-[10px] font-mono block mb-2 ${
                    s.highlight ? (isLight ? 'text-slate-300' : 'text-ls-cyan') : (isLight ? 'text-slate-500' : 'text-slate-400')
                  }`}>
                    {s.role}
                  </span>

                  <p className={`text-xs leading-relaxed ${
                    s.highlight ? 'text-slate-200' : (isLight ? 'text-slate-600' : 'text-slate-400')
                  }`}>
                    {s.description}
                  </p>
                </div>

                <div className={`mt-4 pt-3 border-t text-[10px] font-mono font-semibold ${
                  s.highlight ? (isLight ? 'border-white/20 text-ls-cyan' : 'border-ls-cyan/20 text-ls-cyan') : (isLight ? 'border-slate-200 text-slate-400' : 'border-white/10 text-slate-500')
                }`}>
                  Stage {s.step} of 10
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default IntentToExecutionLifecycle;
