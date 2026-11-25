import React from 'react';
import { BADGE_BASE_CLASSES, HonestyLabel, TONE_STYLES } from '../../data/siteContent';

interface HonestyBadgeProps {
  label: HonestyLabel;
  className?: string;
}

/**
 * Honesty badge: labels every claim with its evidence status. Proven (cyan) /
 * pilot (red) / fieldable (grey) / development (graphite). We never blur statuses.
 */
export const HonestyBadge: React.FC<HonestyBadgeProps> = ({ label, className }) => (
  <span className={`${BADGE_BASE_CLASSES} ${TONE_STYLES[label.tone]} ${className ?? ''}`}>
    <span aria-hidden="true" className="w-1.5 h-1.5 rounded-full bg-current opacity-70" />
    {label.label}
  </span>
);

export default HonestyBadge;
