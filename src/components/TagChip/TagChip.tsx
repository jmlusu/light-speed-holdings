import React from 'react';
import { cn } from '@lightspeed/design-system';

export interface TagChipProps {
  label: string;
  tone?: 'proven' | 'pilot' | 'fieldable' | 'development';
  size?: 'sm' | 'md';
}

export const TagChip: React.FC<TagChipProps> = ({ label, tone = 'proven', size = 'md' }) => {
  const toneStyles: Record<'proven' | 'pilot' | 'fieldable' | 'development', string> = {
    proven: 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
    pilot: 'border-ls-red/40 bg-ls-red/10 text-ls-red',
    fieldable: 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    development: 'border-ls-grey-dark/40 bg-ls-grey-dark/10 text-ls-grey-dark',
  };

  const sizeStyles: Record<'sm' | 'md', string> = {
    sm: 'px-2 py-1 text-[10px]',
    md: 'px-3 py-1.5 text-[11px]',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full border',
        toneStyles[tone],
        sizeStyles[size]
      )}
    >
      {label}
    </span>
  );
};
