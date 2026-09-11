import React from 'react';
import { Radar } from 'lucide-react';
import { DiagnosticSection } from '../components/DiagnosticSection';

interface DiagnosticPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/**
 * AI Diagnostic page: interactive, sector-aware transformation assessment.
 */
export const DiagnosticPage: React.FC<DiagnosticPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <Radar className="w-3.5 h-3.5" />
          <span>TRANSFORMATION DIAGNOSTIC</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
          Score Your Operating Model. Honestly.
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
          An interactive, sector-aware assessment that scores your organization across the four pillars — strategy, data, autonomy, and governance — and returns tiered recommendations before any engagement begins.
        </p>
      </header>

      <DiagnosticSection theme={theme} onRequestBriefing={onRequestBriefing} />
    </>
  );
};

export default DiagnosticPage;
