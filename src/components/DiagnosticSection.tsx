import React from 'react';
import { TransformationDiagnostic } from './TransformationDiagnostic';

interface DiagnosticSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const DiagnosticSection: React.FC<DiagnosticSectionProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  return (
    <section id="diagnostic" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <TransformationDiagnostic
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />
    </section>
  );
};
