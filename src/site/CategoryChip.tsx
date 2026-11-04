import React from 'react';

interface CategoryChipProps {
export type CategoryName = 'STRATEGY' | 'GOVERNANCE' | 'WAVEFORM';

export interface CategoryChipProps {
  /** Article category. Unknown values fall back to the neutral chip. */
  category: string;
  theme: 'light' | 'dark';
}

const CATEGORY_CLASSES = {
  STRATEGY: {
    light: 'bg-ls-blue/10 text-ls-blue border-ls-blue/30',
    dark: 'bg-ls-blue/10 text-ls-blue dark:border-ls-blue/30',
  },
  GOVERNANCE: {
    light: 'bg-ls-red/10 text-ls-red border-ls-red/30',
    dark: 'bg-ls-red/10 text-ls-red dark:border-ls-red/30',
  },
  WAVEFORM: {
    light: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/30',
    dark: 'bg-ls-cyan/10 text-ls-cyan dark:border-ls-cyan/30',
  },
};

export const CategoryChip: React.FC<CategoryChipProps> = ({
  category,
  theme,
}) => {
  const classes = CATEGORY_CLASSES[category][theme];
  return (
    <span className={classes} role="status" aria-live="polite">
      {category}
    </span>
  );
};
/**
 * Category pill for Pharos articles.
 *
 * Colours are restricted to the brand palette in `brand/tokens/brand-tokens.json`
 * (navy / red / cyan / grey). Tailwind only emits classes whose `--color-ls-*`
 * token exists, so an unlisted hue silently renders an unstyled chip.
 */
const CATEGORY_CLASSES: Record<CategoryName, Record<'light' | 'dark', string>> = {
  STRATEGY: {
    light: 'bg-ls-cyan/10 text-ls-navy border-ls-cyan/40',
    dark: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/40',
  },
  GOVERNANCE: {
    light: 'bg-ls-red/10 text-ls-red border-ls-red/40',
    dark: 'bg-ls-red/10 text-ls-red border-ls-red/40',
  },
  WAVEFORM: {
    light: 'bg-ls-navy/10 text-ls-navy border-ls-navy/30',
    dark: 'bg-ls-white/10 text-ls-white border-ls-white/30',
  },
};

const FALLBACK_CLASSES: Record<'light' | 'dark', string> = {
  light: 'bg-ls-grey-dark/10 text-ls-grey-dark border-ls-grey-dark/30',
  dark: 'bg-ls-grey-light-text/10 text-ls-grey-light-text border-ls-grey-light-text/30',
};

const BASE_CLASSES =
  'inline-flex items-center rounded-full border px-2.5 py-1 font-body text-[10px] font-bold tracking-widest uppercase';

const isCategoryName = (value: string): value is CategoryName =>
  Object.prototype.hasOwnProperty.call(CATEGORY_CLASSES, value);

export const CategoryChip: React.FC<CategoryChipProps> = ({ category, theme }) => {
  const classes = isCategoryName(category)
    ? CATEGORY_CLASSES[category][theme]
    : FALLBACK_CLASSES[theme];

  return <span className={`${BASE_CLASSES} ${classes}`}>{category}</span>;
};
