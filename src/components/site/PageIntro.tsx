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
    <header className="relative overflow-hidden px-6 lg:px-12 max-w-7xl mx-auto w-full pt-28 sm:pt-32 pb-6 rounded-3xl mb-4">
      {/* Attached Hexagonal Background Pattern */}
      <div className="absolute inset-0 z-0 pointer-events-none select-none overflow-hidden opacity-35 dark:opacity-20">
        <div
          className={`absolute inset-0 ${
            isLight
              ? 'bg-gradient-to-r from-[#F7F8F9] via-[#F7F8F9]/85 to-transparent'
              : 'bg-gradient-to-r from-[#0A0D14] via-[#0A0D14]/85 to-transparent'
          }`}
        />
      </div>

      <div className="relative z-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest">
          <span>{eyebrow}</span>
        </div>
        <h1
          className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}
        >
          {title}
        </h1>
        {lead && (
          <p
            className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
            }`}
          >
            {lead}
          </p>
        )}
        {children}
      </div>
    </header>
  );
};

export default PageIntro;
