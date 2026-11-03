import React from 'react';

interface StatusBadgeProps {
  status: 'IN DEVELOPMENT' | 'PILOT' | 'PROTOTYPE' | 'IN-HOUSE' | 'EXPLORATION';
  theme: 'light' | 'dark';
}

const STATUS_CLASSES = {
  'IN DEVELOPMENT': {
    light: 'bg-ls-green/10 text-ls-green border-ls-green/30',
    dark: 'bg-ls-green/10 text-ls-green dark:border-ls-green/30',
  },
  PILOT: {
    light: 'bg-ls-teal/10 text-ls-teal border-ls-teal/30',
    dark: 'bg-ls-teal/10 text-ls-teal dark:border-ls-teal/30',
  },
  PROTOTYPE: {
    light: 'bg-ls-crimson/10 text-ls-crimson border-ls-crimson/30',
    dark: 'bg-ls-crimson/10 text-ls-crimson dark:border-ls-crimson/30',
  },
  'IN-HOUSE': {
    light: 'bg-ls-navy/10 text-ls-navy border-ls-navy/30',
    dark: 'bg-ls-navy/10 text-ls-navy dark:border-ls-navy/30',
  },
  EXPLORATION: {
    light: 'bg-ls-yellow/10 text-ls-yellow border-ls-yellow/30',
    dark: 'bg-ls-yellow/10 text-ls-yellow dark:border-ls-yellow/30',
  },
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  theme,
}) => {
  const classes = STATUS_CLASSES[status][theme];
  return (
    <span className={classes} role="status" aria-live="polite">
      {status}
    </span>
  );
};