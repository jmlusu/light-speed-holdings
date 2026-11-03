import React from 'react';

interface CategoryChipProps {
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
