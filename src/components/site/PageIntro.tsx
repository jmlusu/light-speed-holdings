import React from 'react';

interface PageIntroProps {
  theme: 'light' | 'dark';
  eyebrow: string;
  title: string;
  lead?: string;
  children?: React.ReactNode;
}

/**
 * Standard page intro header: eyebrow pill, display title, lead paragraph.
 * Renders any extra children (e.g. the LargeDiagram builder) beneath the lead.
 */
export const PageIntro: React.FC<PageIntroProps> = ({ theme, eyebrow, title, lead, children }) => {
  const isLight = theme === 'light';
  return (
    <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
        <span>{eyebrow}</span>
      </div>
      <h1
        className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}
      >
        {title}
      </h1>
      {lead && (
        <p
          className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}
        >
          {lead}
        </p>
      )}
      {children}
    </header>
  );
};

export default PageIntro;
