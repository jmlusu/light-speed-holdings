import React from 'react';
import {
  RadialBarChart,
  RadialBar,
  Cell,
} from 'recharts';
import { cn } from '@/lib/athena/utils';

interface ATSGaugeProps {
  score: number;
  size?: number;
  strokeWidth?: number;
  showLabel?: boolean;
  label?: string;
  className?: string;
  tier?: 'excellent' | 'good' | 'fair' | 'poor';
}

const TIER_COLORS = {
  excellent: '#10B981', // emerald
  good: '#3B82F6',      // blue
  fair: '#F59E0B',      // amber
  poor: '#EF4444',      // red
} as const;

const TIER_LABELS = {
  excellent: 'Excellent',
  good: 'Good',
  fair: 'Fair',
  poor: 'Poor',
} as const;

export const ATSGauge: React.FC<ATSGaugeProps> = ({
  score,
  size = 80,
  strokeWidth = 8,
  showLabel = true,
  label = 'ATS Score',
  className,
  tier,
}) => {
  const clampedScore = Math.max(0, Math.min(100, Math.round(score)));
  const color = tier ? TIER_COLORS[tier] : TIER_COLORS.excellent;
  const tierLabel = tier ? TIER_LABELS[tier] : '';

  const data = [
    { name: 'Score', value: clampedScore },
    { name: 'Remaining', value: 100 - clampedScore },
  ];

  return (
    <div className={cn('flex flex-col items-center gap-2', className)}>
      <div style={{ width: size, height: size }}>
        <RadialBarChart
          width={size}
          height={size}
          margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
          data={data}
        >
          <RadialBar
            cx="50%"
            cy="50%"
            background
            dataKey="Remaining"
            strokeWidth={strokeWidth}
            stroke="#E5E7EB"
            fill="none"
            cornerRadius={strokeWidth / 2}
          />
          <RadialBar
            cx="50%"
            cy="50%"
            dataKey="Score"
            strokeWidth={strokeWidth}
            stroke={color}
            fill="none"
            cornerRadius={strokeWidth / 2}
          >
            <Cell fill={color} />
          </RadialBar>
        </RadialBarChart>
        <div
          className="absolute flex flex-col items-center justify-center pointer-events-none"
          style={{
            width: size,
            height: size,
            marginTop: -size,
          }}
        >
          <span className="font-display font-bold text-ls-navy" style={{ fontSize: size * 0.22 }}>
            {clampedScore}
          </span>
          {showLabel && tierLabel && (
            <span className="font-body font-medium text-ls-grey-dark" style={{ fontSize: size * 0.1 }}>
              {tierLabel}
            </span>
          )}
        </div>
      </div>

      {showLabel && !tierLabel && (
        <span className="font-body text-xs font-medium text-ls-grey-dark text-center">
          {label}
        </span>
      )}
    </div>
  );
};

// Mini gauge for inline use
export const MiniATSGauge: React.FC<{
  score: number;
  size?: number;
  className?: string;
  tier?: 'excellent' | 'good' | 'fair' | 'poor';
}> = ({ score, size = 40, className, tier }) => {
  const clampedScore = Math.max(0, Math.min(100, Math.round(score)));
  const color = tier ? TIER_COLORS[tier] : TIER_COLORS.excellent;

  const circumference = 2 * Math.PI * (size / 2 - 3);
  const strokeDashoffset = circumference * (1 - clampedScore / 100);

  return (
    <div className={cn('relative inline-flex', className)} style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={size / 2 - 3}
          stroke="#E5E7EB"
          strokeWidth={3}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={size / 2 - 3}
          stroke={color}
          strokeWidth={3}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-all duration-500 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <span className="font-display font-bold text-ls-navy" style={{ fontSize: size * 0.25 }}>
          {clampedScore}
        </span>
      </div>
    </div>
  );
};

// Horizontal progress gauge
export const HorizontalATSGauge: React.FC<{
  score: number;
  width?: number;
  height?: number;
  showScore?: boolean;
  className?: string;
  tier?: 'excellent' | 'good' | 'fair' | 'poor';
}> = ({ score, width = 200, height = 8, showScore = true, className, tier }) => {
  const clampedScore = Math.max(0, Math.min(100, Math.round(score)));
  const color = tier ? TIER_COLORS[tier] : TIER_COLORS.excellent;

  return (
    <div className={cn('flex items-center gap-3', className)}>
      <div className="relative flex-1" style={{ width, height }}>
        <div
          className="rounded-full overflow-hidden"
          style={{
            width: '100%',
            height: '100%',
            backgroundColor: '#E5E7EB',
          }}
        >
          <div
            className="rounded-full transition-all duration-500 ease-out"
            style={{
              width: `${clampedScore}%`,
              height: '100%',
              backgroundColor: color,
            }}
          />
        </div>
      </div>
      {showScore && (
        <span className="font-display font-bold text-ls-navy whitespace-nowrap" style={{ fontSize: '14px' }}>
          {clampedScore}%
        </span>
      )}
    </div>
  );
};
