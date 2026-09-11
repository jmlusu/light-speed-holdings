import React from 'react';
import { HonestyLabel, TONE_STYLES } from '../../data/siteContent';

interface HonestyBadgeProps {
  label: HonestyLabel;
  className?: string;
}

/**
 * Honesty badge: labels every claim with its evidence status. Colors map to
 * PROVEN IN-HOUSE (cyan) / IN PILOT (red) / Fieldable (amber) / In development
 * (slate). We never blur statuses.
 */
export const HonestyBadge: React.FC<HonestyBadgeProps> = ({ label, className }) => (
  <span
    className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[9px] font-bold tracking-widest ${TONE_STYLES[label.tone]} ${className ?? ''}`}
  >
    <span aria-hidden="true" className="w-1.5 h-1.5 rounded-full bg-current opacity-70" />
    {label.label}
  </span>
);

export default HonestyBadge;
