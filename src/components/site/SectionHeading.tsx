import React from 'react';

interface SectionHeadingProps {
  theme: 'light' | 'dark';
  eyebrow: string;
  title: string;
  lead?: string;
}

/**
 * Centered section heading: mono eyebrow, display title, optional lead —
 * the shared rhythm used by every interior section across the site.
 */
export const SectionHeading: React.FC<SectionHeadingProps> = ({ theme, eyebrow, title, lead }) => {
  const isLight = theme === 'light';
  return (
    <div className={`text-center max-w-3xl mx-auto mb-12 sm:mb-16 space-y-3 ${
      isLight ? 'text-slate-900' : 'text-white'
    }`}>
      <span className="text-xs font-mono font-bold tracking-widest text-ls-red">{eyebrow}</span>
      <h2 className="text-3xl sm:text-5xl font-black tracking-tight font-display">{title}</h2>
      {lead && (
        <p className={`text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          {lead}
        </p>
      )}
    </div>
  );
};

export default SectionHeading;
