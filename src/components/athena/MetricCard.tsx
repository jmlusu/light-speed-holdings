import React from 'react';
import { TrendingUp, TrendingDown, Minus, Target, Users, DollarSign, Clock, Award } from 'lucide-react';
import { cn } from '@/lib/athena/utils';
import type { MetricCardProps } from '@/lib/athena/types';

const ICON_MAP: Record<string, React.ReactNode> = {
  target: <Target className="w-5 h-5" />,
  users: <Users className="w-5 h-5" />,
  dollar: <DollarSign className="w-5 h-5" />,
  clock: <Clock className="w-5 h-5" />,
  award: <Award className="w-5 h-5" />,
  default: <Target className="w-5 h-5" />,
};

const ACCENT_COLORS = {
  orange: { bg: 'bg-orange-100', text: 'text-orange-600', border: 'border-orange-200', icon: 'text-orange-600' },
  red: { bg: 'bg-red-100', text: 'text-red-600', border: 'border-red-200', icon: 'text-red-600' },
  cyan: { bg: 'bg-cyan-100', text: 'text-cyan-600', border: 'border-cyan-200', icon: 'text-cyan-600' },
  navy: { bg: 'bg-ls-navy/10', text: 'text-ls-navy', border: 'border-ls-navy/20', icon: 'text-ls-navy' },
  emerald: { bg: 'bg-emerald-100', text: 'text-emerald-600', border: 'border-emerald-200', icon: 'text-emerald-600' },
  blue: { bg: 'bg-blue-100', text: 'text-blue-600', border: 'border-blue-200', icon: 'text-blue-600' },
  purple: { bg: 'bg-purple-100', text: 'text-purple-600', border: 'border-purple-200', icon: 'text-purple-600' },
  amber: { bg: 'bg-amber-100', text: 'text-amber-600', border: 'border-amber-200', icon: 'text-amber-600' },
} as const;

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  trend = 'stable',
  icon: customIcon,
  accentColor = 'navy',
  className,
}) => {
  const colors = ACCENT_COLORS[accentColor] || ACCENT_COLORS.navy;
  const icon = customIcon || ICON_MAP.default;

  const trendIcon = trend === 'up' ? (
    <TrendingUp className="w-4 h-4 text-emerald-600" aria-hidden="true" />
  ) : trend === 'down' ? (
    <TrendingDown className="w-4 h-4 text-red-600" aria-hidden="true" />
  ) : (
    <Minus className="w-4 h-4 text-gray-400" aria-hidden="true" />
  );

  const trendLabel = trend === 'up' ? 'Increase' : trend === 'down' ? 'Decrease' : 'Stable';

  return (
    <article
      className={cn(
        'relative p-5 sm:p-6 rounded-xl border transition-all duration-200',
        'bg-ls-white',
        colors.border,
        'hover:shadow-md hover:border-ls-red/30',
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span
              className={cn(
                'p-2 rounded-lg flex-shrink-0',
                colors.bg,
                colors.icon
              )}
              aria-hidden="true"
            >
              {icon}
            </span>
            <h3 className="font-body text-xs font-bold tracking-widest uppercase text-ls-grey-dark truncate">
              {title}
            </h3>
          </div>
          <div className="flex items-baseline gap-2 flex-wrap">
            <span className="font-display font-black text-2xl sm:text-3xl text-ls-navy">
              {value}
            </span>
            {subtitle && (
              <span className="font-body text-sm text-ls-grey-dark self-end">
                {subtitle}
              </span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-1.5 flex-shrink-0">
          {trendIcon}
          <span className="font-body text-xs font-medium text-ls-grey-dark" aria-label={`${trendLabel} trend`}>
            {trendLabel}
          </span>
        </div>
      </div>

      {/* Subtle accent bar */}
      <div
        className="absolute bottom-0 left-0 right-0 h-1 rounded-b-xl"
        style={{ backgroundColor: `var(--ls-${accentColor === 'navy' ? 'red' : accentColor})` }}
        aria-hidden="true"
      />
    </article>
  );
};

// Large metric card for dashboard header
export const MetricCardLarge: React.FC<{
  title: string;
  value: string | number;
  subtitle?: string;
  description?: string;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: string;
  icon?: React.ReactNode;
  accentColor?: keyof typeof ACCENT_COLORS;
  className?: string;
}> = ({
  title,
  value,
  subtitle,
  description,
  trend = 'stable',
  trendValue,
  icon,
  accentColor = 'navy',
  className,
}) => {
  const colors = ACCENT_COLORS[accentColor] || ACCENT_COLORS.navy;

  const trendIcon = trend === 'up' ? (
    <TrendingUp className="w-4 h-4 text-emerald-600" aria-hidden="true" />
  ) : trend === 'down' ? (
    <TrendingDown className="w-4 h-4 text-red-600" aria-hidden="true" />
  ) : (
    <Minus className="w-4 h-4 text-gray-400" aria-hidden="true" />
  );

  return (
    <article
      className={cn(
        'relative p-6 sm:p-8 rounded-2xl border transition-all duration-200',
        'bg-ls-white',
        colors.border,
        'hover:shadow-lg hover:border-ls-red/30',
        className
      )}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span
            className={cn('p-3 rounded-xl flex-shrink-0', colors.bg, colors.icon)}
            aria-hidden="true"
          >
            {icon || <Target className="w-6 h-6" />}
          </span>
          <div>
            <h3 className="font-body text-xs font-bold tracking-widest uppercase text-ls-grey-dark">
              {title}
            </h3>
            {description && (
              <p className="font-body text-sm text-ls-grey-dark mt-1 max-w-xs">
                {description}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          {trendIcon}
          {trendValue && (
            <span className="font-body text-sm font-medium" style={{ color: trend === 'up' ? '#10B981' : trend === 'down' ? '#EF4444' : '#6B7280' }}>
              {trendValue}
            </span>
          )}
        </div>
      </div>

      <div className="flex items-baseline gap-3 flex-wrap">
        <span className="font-display font-black text-4xl sm:text-5xl text-ls-navy">
          {value}
        </span>
        {subtitle && (
          <span className="font-body text-lg text-ls-grey-dark self-end">
            {subtitle}
          </span>
        )}
      </div>

      <div
        className="absolute bottom-0 left-0 right-0 h-1.5 rounded-b-2xl"
        style={{ backgroundColor: `var(--ls-${accentColor === 'navy' ? 'red' : accentColor})` }}
        aria-hidden="true"
      />
    </article>
  );
};

// Stat counter for proof stats
export const StatCounter: React.FC<{
  value: number;
  label: string;
  format?: 'plain' | 'comma';
  suffix?: string;
  accentColor?: keyof typeof ACCENT_COLORS;
  className?: string;
}> = ({ value, label, format = 'comma', suffix, accentColor = 'navy', className }) => {
  const colors = ACCENT_COLORS[accentColor] || ACCENT_COLORS.navy;

  const formattedValue = format === 'comma'
    ? value.toLocaleString()
    : String(value);

  return (
    <div className={cn('text-center p-4', className)}>
      <div className="relative inline-block mb-2">
        <span className={cn('font-display font-black text-3xl sm:text-4xl', colors.text)}>
          {formattedValue}
          {suffix && <span className="font-display font-bold text-xl text-ls-grey-dark ml-1">{suffix}</span>}
        </span>
      </div>
      <p className="font-body text-xs font-bold tracking-widest uppercase text-ls-grey-dark">
        {label}
      </p>
    </div>
  );
};
