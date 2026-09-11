import React from 'react';
import { PharosSection } from '../components/PharosSection';

interface InsightsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const InsightsPage: React.FC<InsightsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <section
        aria-labelledby="insights-heading"
        className={`px-4 sm:px-8 pt-16 sm:pt-20 pb-2 max-w-7xl mx-auto w-full ${
          isLight ? 'text-slate-800' : 'text-zinc-100'
        }`}
      >
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
            <span>INSIGHTS // PHAROS</span>
          </div>
          <h1
            id="insights-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            Evidence, Research &amp; the Agentic AI Canon
          </h1>
          <p
            className={`max-w-2xl text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-600' : 'text-zinc-400'
            }`}
          >
            Original research and executive briefings on AI strategy, data residency, and
            governance — written for boards, not engineers, and grounded in production systems.
          </p>
        </div>
      </section>

      <PharosSection theme={theme} onRequestBriefing={onRequestBriefing} />
    </>
  );
};

export default InsightsPage;
