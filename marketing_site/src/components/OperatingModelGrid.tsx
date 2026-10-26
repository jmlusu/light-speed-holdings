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
    <div className={`p-6 sm:p-8 rounded-3xl border relative overflow-hidden ${isLight ? 'chassis-milled-light' : 'chassis-milled-dark'}`}>

      <div className="flex items-center gap-2 border-b border-ls-grey-dark/80 pb-3 mb-5">
        <span className="w-2 h-2 rounded-full bg-ls-emerald" />
        <h2 className={isLight ? 'text-lg font-bold font-display text-ls-navy' : 'text-lg font-bold font-display text-ls-white'}>
          Operating Model
        </h2>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {steps.map((item) => (
          <div
            key={item.title}
            className={`p-5 rounded-2xl border space-y-2 ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}
          >
            <span className="text-[10px] font-body font-bold tracking-widest text-ls-red">[ {item.step} ]</span>
            <h3 className={isLight ? 'text-sm font-bold font-display text-ls-navy' : 'text-sm font-bold font-display text-ls-white'}>
              {item.title}
            </h3>
            <p className={isLight ? 'text-xs leading-relaxed text-ls-grey-dark' : 'text-xs leading-relaxed text-ls-grey-light-text'}>
              {item.body}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
