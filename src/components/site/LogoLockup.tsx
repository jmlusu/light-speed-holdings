/**
 * LogoLockup — Inline SVG mark + "LightSpeed / Holdings Limited" wordmark.
 * Session 7 of the LightSpeed redesign.
 * Directive §7
 */

import React from 'react';

interface LogoLockupProps {
  size?: number;
  showText?: boolean;
  theme?: 'light' | 'dark';
  instance?: 'first' | 'repeat';
}

export const LogoLockup: React.FC<LogoLockupProps> = ({
  size = 36,
  showText = true,
  theme = 'dark',
  instance = 'first',
}) => {
  const isDark = theme === 'dark';
  const onNavy = isDark ? '#FFFFFF' : '#070A40';
  const onCyan = '#00BFFF';

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 40"
      fill="none"
      stroke={onCyan}
      strokeWidth={1.5}
      className="flex items-center gap-2"
    >
      <rect x={0} y={0} width={40} height={40} rx={8} fill={onNavy} />
      <text
        x={55}
        y={30}
        fontFamily="Arial, sans-serif"
        fontSize={20}
        fontWeight={700}
        fill={onCyan}
      >
        LightSpeed
      </text>
      <text
        x={115}
        y={30}
        fontFamily="Arial, sans-serif"
        fontSize={14}
        fill={onNavy}
      >
        / Holdings Limited
      </text>
      {showText && (
        <text
          x={180}
          y={30}
          fontFamily="Arial, sans-serif"
          fontSize={11}
          fontWeight={700}
          fill={isDark ? '#9CA3AF' : '#6B7280'}
          transform="translate(-50%)"
        >
          LightSpeed Holdings™
        </text>
      )}
    </svg>
  );
};

export default LogoLockup;
