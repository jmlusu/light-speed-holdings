import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { cn } from '@lightspeed/design-system';

export interface ArrowLinkProps {
  /** In-app route, or a click handler for actions that must not navigate. */
  to: string | ((e: React.MouseEvent) => void);
  children: React.ReactNode;
  className?: string;
}

const BASE_CLASSES =
  'inline-flex items-center gap-1 font-body text-ls-red transition-colors hover:underline';

/**
 * ArrowLink - text link with a trailing arrow.
 *
 * String targets route through react-router so the SPA keeps its state. The
 * previous version set `window.location.href`, which forced a full document
 * reload on every click.
 */
export const ArrowLink: React.FC<ArrowLinkProps> = ({ to, children, className }) => {
  const classes = cn(BASE_CLASSES, className);

  if (typeof to === 'function') {
    return (
      <button type="button" onClick={to} className={classes}>
        {children}
        <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
      </button>
    );
  }

  return (
    <Link to={to} className={classes}>
      {children}
      <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
    </Link>
  );
};
