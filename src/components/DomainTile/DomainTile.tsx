import React from 'react';
import { Link } from 'react-router-dom';

export interface DomainTileProps {
  title: string;
  description?: string;
  /**
   * In-app route. When present the whole tile becomes a `Link`; when absent the
   * tile renders as a static block (e.g. inside a card that is already a link).
   */
  to?: string;
  theme: 'light' | 'dark';
  /** Marks the tile the reader is currently on: adds a brand accent. */
  active?: boolean;
  badge?: string;
}

/**
 * DomainTile - compact summary tile used for cross-linking between domains.
 *
 * The `to` prop used to be accepted and silently dropped, which made every tile
 * a dead end. It now decides the element: an anchor that routes in-app, or a
 * plain block when there is nowhere to go.
 */
export const DomainTile: React.FC<DomainTileProps> = ({
  title,
  description,
  to,
  theme,
  active = false,
  badge,
}) => {
  const isLight = theme === 'light';
  const titleColor = isLight ? 'text-ls-navy' : 'text-ls-white';
  const descriptionColor = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';
  const frameColor = active
    ? 'border-ls-red/60'
    : isLight
      ? 'border-ls-grey-dark/30'
      : 'border-ls-white/15';
  const surface = isLight ? 'bg-ls-white/95' : 'bg-ls-navy/80';

  const content = (
    <>
      <div className="flex items-start justify-between gap-3">
        <h3 className={`font-display text-base sm:text-lg font-bold tracking-tight ${titleColor}`}>
          {title}
        </h3>
        {badge && (
          <span className="inline-flex shrink-0 items-center gap-1 rounded-full border border-ls-cyan/40 bg-ls-cyan/10 px-2 py-0.5 font-body text-[9px] font-bold tracking-widest uppercase text-ls-cyan">
            {badge}
          </span>
        )}
      </div>
      {description && (
        <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${descriptionColor}`}>{description}</p>
      )}
    </>
  );

  const className = `flex h-full flex-col rounded-2xl border p-5 transition-shadow ${surface} ${frameColor} ${
    to ? 'hover:shadow-lg' : ''
  }`;

  if (!to) {
    return <div className={className}>{content}</div>;
  }

  return (
    <Link to={to} className={className}>
      {content}
    </Link>
  );
};
