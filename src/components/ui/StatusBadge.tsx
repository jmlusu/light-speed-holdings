import React from 'react';
import { CheckCircle2, Clock, Sparkles, Shield, AlertCircle } from 'lucide-react';

export type HonestyTier = 
  | 'proven-in-house' 
  | 'pilot' 
  | 'fieldable-2026' 
  | 'in-development';

interface StatusBadgeProps {
  tier: HonestyTier;
  label?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  tier,
  label,
  size = 'md',
  className = ''
}) => {
  const configs: Record<HonestyTier, {
    defaultLabel: string;
    icon: React.ElementType;
    badgeStyle: string;
    dotStyle: string;
    desc: string;
  }> = {
    'proven-in-house': {
      defaultLabel: 'PROVEN IN-HOUSE',
      icon: Shield,
      badgeStyle: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/30',
      dotStyle: 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.7)]',
      desc: 'Tested and active on our internal 144-agent enterprise operations'
    },
    'pilot': {
      defaultLabel: 'PILOT IN PROGRESS',
      icon: Sparkles,
      badgeStyle: 'bg-orange-500/10 text-orange-500 border-orange-500/30',
      dotStyle: 'bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.7)] animate-pulse',
      desc: 'Active stakeholder pilot or ecosystem testing phase'
    },
    'fieldable-2026': {
      defaultLabel: 'FIELDABLE IN 2026',
      icon: Clock,
      badgeStyle: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
      dotStyle: 'bg-blue-400 shadow-[0_0_8px_rgba(96,165,250,0.7)]',
      desc: 'Productized architecture scheduled for regional field rollouts'
    },
    'in-development': {
      defaultLabel: 'IN ACTIVE DEVELOPMENT',
      icon: AlertCircle,
      badgeStyle: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
      dotStyle: 'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.7)]',
      desc: 'Core codebase and agent DAGs currently in active development'
    }
  };

  const config = configs[tier];
  const Icon = config.icon;

  const sizeClasses = {
    sm: 'text-[9px] px-2 py-0.5 gap-1.5 font-mono font-bold',
    md: 'text-[10px] px-2.5 py-1 gap-1.5 font-mono font-bold',
    lg: 'text-xs px-3.5 py-1.5 gap-2 font-mono font-bold'
  }[size];

  return (
    <span 
      className={`inline-flex items-center rounded-full border tracking-wider uppercase transition-all shadow-xs ${config.badgeStyle} ${sizeClasses} ${className}`}
      title={config.desc}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${config.dotStyle}`} />
      <Icon className="w-3 h-3" />
      <span>{label || config.defaultLabel}</span>
    </span>
  );
};
