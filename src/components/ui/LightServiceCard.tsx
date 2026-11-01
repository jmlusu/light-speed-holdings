import React from 'react';
import { ArrowLink } from './ArrowLink';

interface LightServiceCardProps {
  icon: React.ReactNode;
  title: string;
  body: string;
  to: string;
  linkLabel?: string;
}

/**
 * Light-surface capability card: line icon, title, body, arrow link.
 * Equal-height by design — the link is pinned to the bottom with `mt-auto`.
 */
export const LightServiceCard: React.FC<LightServiceCardProps> = ({
  icon,
  title,
  body,
  to,
  linkLabel = 'Learn more',
}) => (
  <article className="group flex h-full flex-col rounded-xl border border-ls-navy/10 bg-ls-white p-6 transition-[transform,border-color,box-shadow] duration-200 hover:-translate-y-0.5 hover:border-ls-cyan/60 hover:shadow-ls-md focus-within:border-ls-cyan/60 focus-within:shadow-ls-md">
    <span className="text-ls-cyan" aria-hidden="true">
      {icon}
    </span>
    <h3 className="mt-5 font-display text-base sm:text-lg font-bold leading-snug text-ls-navy">{title}</h3>
    <p className="mt-2 text-[13px] leading-relaxed text-ls-grey-dark">{body}</p>
    <div className="mt-auto pt-5">
      <ArrowLink to={to} tone="navy">
        {linkLabel}
      </ArrowLink>
    </div>
  </article>
);

export default LightServiceCard;
