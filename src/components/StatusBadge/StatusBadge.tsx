import React from 'react';

export interface StatusBadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  label: string;
  tone: 'proven' | 'pilot' | 'fieldable' | 'development';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  label,
  tone = 'proven',
  className = '',
  ...props
}) => {
  const toneStyles: Record<'proven' | 'pilot' | 'fieldable' | 'development', string> = {
    proven: 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
    pilot: 'border-ls-red/40 bg-ls-red/10 text-ls-red',
    fieldable: 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    development: 'border-ls-grey-dark/40 bg-ls-grey-dark/10 text-ls-grey-dark',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full border text-xs font-bold',
        toneStyles[tone],
        className
      )}
      {...props}
    >
      {label}
    </span>
  );
};
