import React from 'react';
import { MapPin, Briefcase, DollarSign, Clock, ExternalLink, ChevronRight } from 'lucide-react';
import { MiniATSGauge } from './ATSGauge';
import { cn, formatSalary, formatDate, getJobTypeLabel, getJobSourceLabel, getMatchTierColor, getMatchTierLabel } from '@/lib/athena/utils';
import type { Job, JobCardProps } from '@/lib/athena/types';

interface JobCardPropsExtended extends JobCardProps {
  compact?: boolean;
  showActions?: boolean;
}

export const JobCard: React.FC<JobCardPropsExtended> = ({
  job,
  onClick,
  matchScore,
  matchTier,
  compact = false,
  showActions = false,
}) => {
  const effectiveMatchScore = matchScore ?? job.match_score;
  const effectiveMatchTier = matchTier ?? job.match_tier;

  return (
    <article
      onClick={onClick}
      className={cn(
        'relative group cursor-pointer transition-all duration-200',
        'bg-ls-white border border-ls-grey-dark/30 rounded-xl p-4 sm:p-5',
        'hover:border-ls-red/40 hover:shadow-lg hover:shadow-ls-red/10 hover:-translate-y-0.5',
        'focus:outline-none focus-visible:ring-2 focus-visible:ring-ls-red focus-visible:ring-offset-2',
        compact && 'p-3'
      )}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
      role="button"
      aria-label={`View job details: ${job.title} at ${job.company}`}
    >
      {/* Top row: Company + Source badge */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1.5 flex-wrap">
            <span className="font-display font-bold text-sm text-ls-navy truncate">
              {job.company}
            </span>
            <span
              className={cn(
                'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider',
                `border ${getMatchTierColor(effectiveMatchTier)}`
              )}
            >
              {getMatchTierLabel(effectiveMatchTier)}
            </span>
          </div>
          <h3 className="font-display font-bold text-base sm:text-lg text-ls-navy truncate group-hover:text-ls-red transition-colors">
            {job.title}
          </h3>
        </div>

        {/* ATS Gauge */}
        <div className="flex-shrink-0 ml-3">
          <MiniATSGauge
            score={job.ats_score ?? 0}
            size={48}
            tier={effectiveMatchTier}
          />
        </div>
      </div>

      {/* Meta info row */}
      <div className="flex flex-wrap items-center gap-3 text-xs font-body text-ls-grey-dark mb-3">
        <span className="flex items-center gap-1.5">
          <MapPin className="w-3.5 h-3.5 text-ls-grey-light-text" aria-hidden="true" />
          {job.location}
        </span>
        <span className="flex items-center gap-1.5">
          <Briefcase className="w-3.5 h-3.5 text-ls-grey-light-text" aria-hidden="true" />
          {getJobTypeLabel(job.job_type)}
        </span>
        <span className="flex items-center gap-1.5">
          <DollarSign className="w-3.5 h-3.5 text-ls-grey-light-text" aria-hidden="true" />
          {formatSalary(job.salary_range)}
        </span>
        <span className="flex items-center gap-1.5">
          <Clock className="w-3.5 h-3.5 text-ls-grey-light-text" aria-hidden="true" />
          {formatDate(job.posted_date)}
        </span>
      </div>

      {/* Source badge */}
      <div className="flex items-center justify-between">
        <span
          className={cn(
            'inline-flex items-center px-2 py-1 rounded-md text-[10px] font-bold tracking-wider',
            'bg-ls-grey-light text-ls-grey-dark border border-ls-grey-dark/30'
          )}
        >
          <span className="w-2 h-2 rounded-full bg-ls-cyan mr-1.5" aria-hidden="true" />
          {getJobSourceLabel(job.source)}
        </span>

        {showActions && (
          <a
            href={job.application_url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="p-2 rounded-lg bg-ls-red/10 text-ls-red hover:bg-ls-red/20 transition-colors"
            aria-label={`Apply on ${getJobSourceLabel(job.source)}`}
          >
            <ExternalLink className="w-4 h-4" aria-hidden="true" />
          </a>
        )}
      </div>

      {/* Click hint */}
      {!compact && (
        <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <ChevronRight className="w-5 h-5 text-ls-grey-light-text" aria-hidden="true" />
        </div>
      )}
    </article>
  );
};

// Compact job card for list views
export const JobCardCompact: React.FC<JobCardProps & { onApplyClick?: (e: React.MouseEvent) => void }> = ({
  job,
  onClick,
  matchScore,
  matchTier,
  onApplyClick,
}) => {
  const effectiveMatchScore = matchScore ?? job.match_score;
  const effectiveMatchTier = matchTier ?? job.match_tier;

  return (
    <div
      onClick={onClick}
      className="group cursor-pointer flex items-center gap-4 p-3 bg-ls-white border border-ls-grey-dark/30 rounded-lg hover:border-ls-red/40 hover:bg-ls-red/5 transition-all"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
      role="button"
      aria-label={`View job: ${job.title} at ${job.company}`}
    >
      <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-ls-grey-light flex items-center justify-center">
        <span className="font-display font-bold text-xl text-ls-navy">
          {job.company.charAt(0).toUpperCase()}
        </span>
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <h4 className="font-display font-bold text-sm text-ls-navy truncate group-hover:text-ls-red transition-colors">
            {job.title}
          </h4>
          <span className={cn('px-1.5 py-0.5 rounded text-[9px] font-bold', getMatchTierColor(effectiveMatchTier))}>
            {getMatchTierLabel(effectiveMatchTier)}
          </span>
        </div>
        <p className="font-body text-xs text-ls-grey-dark truncate">{job.company}</p>
        <div className="flex items-center gap-3 mt-1 text-[10px] text-ls-grey-light-text">
          <span className="flex items-center gap-1">
            <MapPin className="w-3 h-3" aria-hidden="true" />
            {job.location}
          </span>
          <span className="flex items-center gap-1">
            <Briefcase className="w-3 h-3" aria-hidden="true" />
            {getJobTypeLabel(job.job_type)}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <MiniATSGauge score={job.ats_score ?? 0} size={40} tier={effectiveMatchTier} />
        {onApplyClick && (
          <button
            onClick={onApplyClick}
            className="p-2 rounded-lg bg-ls-red/10 text-ls-red hover:bg-ls-red/20 transition-colors"
            aria-label="Apply"
          >
            <ExternalLink className="w-4 h-4" aria-hidden="true" />
          </button>
        )}
      </div>
    </div>
  );
};
