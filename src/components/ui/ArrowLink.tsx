import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRightIcon } from './icons';

export type ArrowLinkTone = 'cyan' | 'navy' | 'red';

interface ArrowLinkProps {
  to: string;
  children: React.ReactNode;
  /** Colour of label + arrow; sections on dark pick `cyan`. */
  tone?: ArrowLinkTone;
  className?: string;
}

const TONE_CLASS: Record<ArrowLinkTone, string> = {
  cyan: 'text-ls-cyan hover:text-ls-cyan/80 focus-visible:ring-ls-cyan',
  navy: 'text-ls-navy hover:text-ls-navy/80 focus-visible:ring-ls-navy',
  red: 'text-ls-red hover:text-ls-red/80 focus-visible:ring-ls-red',
};

/**
 * Small label + trailing arrow link ("Learn More →").
 * Internal destinations only — every link must resolve to a real route.
 */
export const ArrowLink: React.FC<ArrowLinkProps> = ({
  to,
  children,
  tone = 'cyan',
  className,
}) => (
  <Link
    to={to}
    className={`group inline-flex items-center gap-1.5 text-xs font-bold tracking-wider uppercase transition-colors rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-transparent ${TONE_CLASS[tone]} ${className ?? ''}`}
  >
    {children}
    <ArrowRightIcon className="h-3.5 w-3.5 shrink-0 transition-transform duration-200 group-hover:translate-x-0.5" />
  </Link>
);

export default ArrowLink;
