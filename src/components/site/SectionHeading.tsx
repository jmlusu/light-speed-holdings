import React from 'react';

interface SectionHeadingProps {
  theme: 'light' | 'dark';
  eyebrow: string;
  title: string;
  lead?: string;
  /** Heading level; use 'h1' for the single page title, default 'h2' for sections. */
  level?: 'h1' | 'h2';
}

/**
 * Centered section heading: mono eyebrow, display title, optional lead —
 * the shared rhythm used by every interior section across the site.
 */
export const SectionHeading: React.FC<SectionHeadingProps> = ({ theme, eyebrow, title, lead, level = 'h2' }) => {
  const isLight = theme === 'light';
  const Heading = level;
  return (
    <div className={`text-center max-w-3xl mx-auto mb-12 sm:mb-16 space-y-3 ${
      isLight ? 'text-ls-navy' : 'text-ls-white'
    }`}>
      <span className="text-xs font-body font-bold tracking-widest text-ls-red">{eyebrow}</span>
      <Heading className="text-3xl sm:text-5xl font-black tracking-tight font-display">{title}</Heading>
      {lead && (
        <p className={`text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
        }`}>
          {lead}
        </p>
      )}
    </div>
  );
};

export default SectionHeading;
