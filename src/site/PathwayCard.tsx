import React from 'react';
import { Link } from 'react-router-dom';
import { Target } from 'lucide-react';

interface PathwayCardProps {
  id: string;
  /** 1-based position in the pathway list; rendered as the "PATH n" marker. */
  index?: number;
  title: string;
  intent: string;
  body: string;
  primaryLabel: string;
  primaryTo: string;
  secondaryLabels: { label: string; to: string }[];
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const PathwayCard: React.FC<PathwayCardProps> = ({
  id,
  index,
  title,
  intent,
  body,
  primaryLabel,
  primaryTo,
  secondaryLabels,
  theme,
  onRequestBriefing,
}) => {
  const isLight = theme === 'light';

  return (
    <article
      className={`ripple-on h-full rounded-3xl p-6 border flex flex-col gap-4 transition-all hover:-translate-y-0.5 ${isLight
        ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl'
        : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl'}`}
    >
      <div className="flex items-center justify-between gap-3">
        <span className="inline-flex items-center gap-2 rounded-full border px-2.5 py-1 font-body text-[10px] font-bold tracking-widest">
          <Target className="w-3.5 h-3.5" aria-hidden="true" />
          {intent}
        </span>
        <span className={`font-body text-[10px] font-bold tracking-widest ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
          {typeof index === 'number' ? `PATH ${index}` : null}
        </span>
      </div>

      <div>
        <h3 className={`font-display font-bold text-base sm:text-lg tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
          {intent}
        </h3>
        <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
          {body}
        </p>
      </div>

      <div className="mt-auto space-y-3">
        <Link
          to={primaryTo}
          className={`ripple-on group inline-flex w-full items-center justify-between gap-2 rounded-2xl px-4 py-3 font-body text-xs font-bold tracking-widest transition-all ${isLight
            ? 'bg-ls-navy text-ls-white hover:bg-ls-red'
            : 'bg-ls-red text-ls-white hover:bg-ls-red/90'}`}
        >
          <span>{primaryLabel}</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-4 h-4 transition-transform group-hover:translate-x-0.5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M5 12.55a11 11 0 0 1 14.08 0" />
          </svg>
        </Link>
        <div className={`flex flex-wrap gap-x-4 gap-y-1 pt-1 border-t ${isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/15'}`}>
          {secondaryLabels.map((link) => (
            <Link
              key={link.label}
              to={link.to}
              className={`font-body text-[11px] font-bold tracking-wide hover:text-ls-red transition-colors ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
            >
              {link.label} ›
            </Link>
          ))}
        </div>
      </div>
    </article>
  );
};
