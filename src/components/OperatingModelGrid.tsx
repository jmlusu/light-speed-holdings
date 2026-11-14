import React from 'react';
import { ArrowRight } from 'lucide-react';

interface OperatingModelGridProps {
  theme: 'light' | 'dark';
}

export const OperatingModelGrid: React.FC<OperatingModelGridProps> = ({ theme }) => {
  const isLight = theme === 'light';

  const steps = [
    { step: '01', title: 'Strategy', body: 'Clarify ambition, constraints, and the decisions that matter before any build begins.' },
    { step: '02', title: 'Build', body: 'Design and ship agentic systems, data pipelines, and workflows against a governed backlog.' },
    { step: '03', title: 'Govern', body: 'Install controls, policy, and human-in-the-loop authority so systems stay accountable.' },
    { step: '04', title: 'Research', body: 'Feed evidence, benchmarks, and Pharos policy work back into the next strategy cycle.' }
  ];

  return (
    <div className={`p-6 sm:p-8 border relative overflow-hidden ${
      isLight ? 'bg-white border-slate-300 shadow-[4px_4px_0px_#070A40]' : 'bg-[#070A40] border-white/20 shadow-[4px_4px_0px_#00BFFF]'
    }`}>
      <div className="flex items-center gap-2 pb-3 mb-5 border-b border-white/10">
        <span className="w-2 h-2 bg-ls-cyan shadow-[0_0_6px_#00BFFF]" />
        <h2 className={`text-lg font-bold font-sans uppercase tracking-wider ${isLight ? 'text-ls-navy' : 'text-white'}`}>
          Operating Model
        </h2>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {steps.map((item) => (
          <div
            key={item.title}
            className={`p-5 border space-y-2 ${
              isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'
            }`}
          >
            <span className="text-[10px] font-mono font-bold tracking-widest text-ls-red tabular-nums">[ {item.step} ]</span>
            <h3 className={`text-base font-bold font-sans ${isLight ? 'text-ls-navy' : 'text-white'}`}>
              {item.title}
            </h3>
            <p className={`text-xs leading-relaxed font-sans ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
              {item.body}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default OperatingModelGrid;
