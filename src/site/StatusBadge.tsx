import React from 'react';

export type SolutionStatus =
  | 'IN DEVELOPMENT'
  | 'PILOT'
  | 'PROTOTYPE'
  | 'IN-HOUSE'
  | 'EXPLORATION';

export interface StatusBadgeProps {
  status: SolutionStatus;
  theme: 'light' | 'dark';
}

/**
 * Status pill for solution maturity.
 *
 * Colours are restricted to the brand palette in `brand/tokens/brand-tokens.json`
 * (navy / red / cyan / grey). Tailwind only emits classes whose `--color-ls-*`
 * token exists, so using an unlisted hue silently renders an unstyled chip.
 */
const STATUS_CLASSES: Record<SolutionStatus, Record<'light' | 'dark', string>> = {
  'IN DEVELOPMENT': {
    light: 'bg-ls-grey-dark/10 text-ls-grey-dark border-ls-grey-dark/30',
    dark: 'bg-ls-grey-light-text/10 text-ls-grey-light-text border-ls-grey-light-text/30',
  },
  PILOT: {
    light: 'bg-ls-cyan/10 text-ls-navy border-ls-cyan/40',
    dark: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/40',
  },
  PROTOTYPE: {
    light: 'bg-ls-red/10 text-ls-red border-ls-red/40',
    dark: 'bg-ls-red/10 text-ls-red border-ls-red/40',
  },
  'IN-HOUSE': {
    light: 'bg-ls-navy/10 text-ls-navy border-ls-navy/30',
    dark: 'bg-ls-white/10 text-ls-white border-ls-white/30',
  },
  EXPLORATION: {
    light: 'bg-ls-grey-light-text/15 text-ls-grey-dark border-ls-grey-dark/25',
    dark: 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/20',
  },
};

const BASE_CLASSES =
  'inline-flex items-center rounded-full border px-2.5 py-1 font-body text-[10px] font-bold tracking-widest uppercase';

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, theme }) => {
  const classes = STATUS_CLASSES[status][theme];
  return <span className={`${BASE_CLASSES} ${classes}`}>{status}</span>;
};
