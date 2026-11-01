import React from 'react';

interface StatBlockProps {
  /** Rendered as text so the figure stays selectable, searchable and data-driven. */
  value: string | number;
  label: string;
  /** `dark` = on navy surface, `light` = on white surface. */
  mode?: 'dark' | 'light';
  className?: string;
}

/**
 * A single figure + caption. The number is always live text sourced from the
 * metrics registry — never a baked image, so it reflows and stays accessible.
 */
export const StatBlock: React.FC<StatBlockProps> = ({ value, label, mode = 'dark', className }) => {
  const isDark = mode === 'dark';
  return (
    <div className={`flex flex-col ${className ?? ''}`}>
      <span
        className={`font-display text-3xl sm:text-4xl font-bold leading-none tracking-tight ${
          isDark ? 'text-ls-white' : 'text-ls-navy'
        }`}
      >
        {value}
      </span>
      <span
        className={`mt-2 text-[10px] sm:text-[11px] font-semibold uppercase tracking-[0.18em] ${
          isDark ? 'text-ls-white/55' : 'text-ls-grey-dark'
        }`}
      >
        {label}
      </span>
    </div>
  );
};

export default StatBlock;
