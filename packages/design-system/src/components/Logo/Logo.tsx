/**
 * Logo Component
 *
 * Canonical LightSpeed logo with variants using real traced artwork from brand/logo/*.svg
 * Directive §6 — New approved LightSpeed logo
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export type LogoVariant = 'full' | 'dark' | 'light' | 'icon' | 'monochrome';
export type LogoSize = 'sm' | 'md' | 'lg' | 'xl';

export interface LogoProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: LogoVariant;
  size?: LogoSize;
}

// Normalized mark paths (viewBox 0 0 64 64)
// Original viewBox: 310.14 231.14 608.85 387.81
// Transform: translate(-310.14, -231.14) scale(64/608.85, 64/387.81) ≈ scale(0.105, 0.165)
const MARK_PATHS = [
  // Blue slab (navy)
  { d: 'M21.4 0.1L35.1 0.3L19.9 29.1L5.6 39.8L2.1 39.6Z', color: '#070A40' },
  // Blue band left (cyan)
  { d: 'M19.9 28.6L38.7 28.9L29.3 39.8L5.5 39.6Z', color: '#00BFFF' },
  // Red top
  { d: 'M35.0 3.9L51.9 4.0L46.1 14.4L43.1 18.9L34.8 18.9L33.1 17.6L38.0 9.1Z', color: '#E63946' },
  // Red lower
  { d: 'M34.7 18.9L42.8 18.8L56.7 36.6L52.3 40.1Z', color: '#E63946' },
  // Red right
  { d: 'M46.0 14.2L61.7 32.8L57.2 36.5L42.9 18.9Z', color: '#E63946' },
  // Blue band right
  { d: 'M38.7 28.5L47.3 39.7L28.8 40.0Z', color: '#00BFFF' },
];

// Monochrome mark path (normalized to 0 0 64 64)
const MONOCHROME_MARK_PATH =
  'M21.4 0.1L35.1 0.3L19.9 29.1L5.6 39.8L2.1 39.6Z ' +
  'M19.9 28.6L38.7 28.9L29.3 39.8L5.5 39.6Z ' +
  'M35.0 3.9L51.9 4.0L46.1 14.4L43.1 18.9L34.8 18.9L33.1 17.6L38.0 9.1Z ' +
  'M34.7 18.9L42.8 18.8L56.7 36.6L52.3 40.1Z ' +
  'M46.0 14.2L61.7 32.8L57.2 36.5L42.9 18.9Z ' +
  'M38.7 28.5L47.3 39.7L28.8 40.0Z';

// Size map for the logo mark
const MARK_SIZE_MAP: Record<LogoSize, number> = {
  sm: 24,
  md: 32,
  lg: 48,
  xl: 72,
};

// Full lockup size map (wider for text)
const FULL_SIZE_MAP: Record<LogoSize, { width: number; height: number }> = {
  sm: { width: 120, height: 32 },
  md: { width: 160, height: 42 },
  lg: { width: 220, height: 58 },
  xl: { width: 320, height: 84 },
};

/**
 * LogoMark - The geometric icon mark (6 paths with brand colors)
 */
const LogoMark = React.forwardRef<SVGSVGElement, { size?: LogoSize; color?: string; testId?: string }>(
  ({ size = 'md', color = 'currentColor', testId }, ref) => {
    const dimension = MARK_SIZE_MAP[size];
    const useBrandColors = color === 'currentColor';

    return (
      <svg
        ref={ref}
        width={dimension}
        height={dimension}
        viewBox="0 0 64 64"
        fill="none"
        aria-hidden="true"
        style={{ display: 'block' }}
        data-testid={testId}
      >
        {MARK_PATHS.map((path, i) => (
          <path
            key={i}
            d={path.d}
            fill={useBrandColors ? path.color : color}
          />
        ))}
      </svg>
    );
  }
);

LogoMark.displayName = 'LogoMark';

/**
 * MonochromeMark - Single path for monochrome usage
 */
const MonochromeMark = React.forwardRef<SVGSVGElement, { size?: LogoSize; color?: string; testId?: string }>(
  ({ size = 'md', color = 'currentColor', testId }, ref) => {
    const dimension = MARK_SIZE_MAP[size];

    return (
      <svg
        ref={ref}
        width={dimension}
        height={dimension}
        viewBox="0 0 64 64"
        fill="none"
        aria-hidden="true"
        style={{ display: 'block' }}
        data-testid={testId}
      >
        <path
          d={MONOCHROME_MARK_PATH}
          fill={color === 'currentColor' ? '#070A40' : color}
          fillRule="nonzero"
        />
      </svg>
    );
  }
);

MonochromeMark.displayName = 'MonochromeMark';

/**
 * Wordmark - SVG text-based wordmark matching brand typography
 * Uses Arial (brand font) with appropriate weights and styling
 */
const Wordmark = ({
  variant,
  size = 'md',
  className = '',
}: { variant: 'full' | 'dark' | 'light'; size?: LogoSize; className?: string }) => {
  const dimensions = FULL_SIZE_MAP[size];
  const isDark = variant === 'dark';
  const isLight = variant === 'light';
  const isFull = variant === 'full';

  // Colors per variant
  const lightColor = isDark ? '#FFFFFF' : '#070A40';
  const speedColor = isDark ? '#FFFFFF' : (isLight ? '#070A40' : 'url(#speedGradient)');
  const holdingsColor = isDark ? '#FFFFFF' : '#070A40';
  const taglineColor = isDark ? 'rgba(255,255,255,0.7)' : 'rgba(7,10,64,0.7)';

  // Font sizes per size
  const fontSizes: Record<LogoSize, { light: number; speed: number; holdings: number; tagline: number }> = {
    sm: { light: 14, speed: 14, holdings: 7, tagline: 5 },
    md: { light: 18, speed: 18, holdings: 9, tagline: 6 },
    lg: { light: 24, speed: 24, holdings: 12, tagline: 8 },
    xl: { light: 36, speed: 36, holdings: 18, tagline: 12 },
  };
  const fs = fontSizes[size];

  return (
    <svg
      width={dimensions.width}
      height={dimensions.height}
      viewBox={`0 0 ${dimensions.width} ${dimensions.height}`}
      className={className}
      style={{ display: 'block' }}
      aria-hidden="true"
    >
      {!isDark && !isLight && (
        <defs>
          <linearGradient id="speedGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#00BFFF" />
            <stop offset="100%" stopColor="#07F1FF" />
          </linearGradient>
        </defs>
      )}
      <text
        x={dimensions.height * 0.1}
        y={dimensions.height * 0.68}
        fontFamily="Arial, Helvetica, sans-serif"
        fontWeight="700"
        fontSize={fs.light}
        fill={lightColor}
        letterSpacing="0.02em"
      >
        LIGHT
        <tspan fill={speedColor}>SPEED</tspan>
      </text>
      {isFull && (
        <>
          <text
            x={dimensions.height * 0.1}
            y={dimensions.height * 0.92}
            fontFamily="Arial, Helvetica, sans-serif"
            fontWeight="400"
            fontSize={fs.holdings}
            fill={holdingsColor}
            letterSpacing="0.1em"
          >
            HOLDINGS LIMITED
          </text>
          <text
            x={dimensions.height * 0.1}
            y={dimensions.height * 1.08}
            fontFamily="Arial, Helvetica, sans-serif"
            fontWeight="400"
            fontSize={fs.tagline}
            fill={taglineColor}
            letterSpacing="0.15em"
          >
            VELOCITY CAPITAL
          </text>
        </>
      )}
    </svg>
  );
};

/**
 * FullLockup - Combined mark + wordmark for full/dark/light variants
 */
const FullLockup = React.forwardRef<HTMLDivElement, { variant: 'full' | 'dark' | 'light'; size?: LogoSize; testId?: string; className?: string; style?: React.CSSProperties }>(
  ({ variant, size = 'md', testId, className = '', style }, ref) => {
    const isDark = variant === 'dark';
    const isLight = variant === 'light';

    // Mark color per variant
    const markColor = isDark ? '#FFFFFF' : (isLight ? '#070A40' : 'currentColor');

    return (
      <div
        ref={ref}
        className={className}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: size === 'sm' ? 6 : size === 'md' ? 8 : size === 'lg' ? 12 : 16,
          ...style,
        }}
        data-testid={testId}
      >
        <>
          <LogoMark size={size} color={markColor} />
          <Wordmark variant={variant} size={size} />
        </>
      </div>
    );
  }
);

FullLockup.displayName = 'FullLockup';

export const Logo = React.forwardRef<HTMLDivElement, LogoProps>(
  (
    {
      variant = 'full',
      size = 'md',
      className = '',
      style,
      ...props
    },
    ref
  ) => {
    const isDark = document.documentElement.classList.contains('dark');

    const variantStyles: Record<string, React.CSSProperties> = {
      full: {},
      dark: {
        color: tokens.colors.white,
      },
      light: {
        color: tokens.colors.navy,
      },
      icon: {},
      monochrome: {
        color: isDark ? tokens.colors.white : tokens.colors.navy,
      },
    };

    const logoColor = variant === 'dark' ? tokens.colors.white
      : variant === 'light' ? tokens.colors.navy
      : variant === 'monochrome' ? (isDark ? tokens.colors.white : tokens.colors.navy)
      : 'inherit';

    const combinedStyle: React.CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      ...variantStyles[variant],
      ...style,
    };

    // Icon-only variants
    if (variant === 'icon') {
      return (
        <div ref={ref} style={{ display: 'inline-flex', alignItems: 'center' }}>
          <LogoMark size={size} color={logoColor} testId="logo-icon" />
        </div>
      );
    }

    if (variant === 'monochrome') {
      return (
        <div ref={ref} style={{ display: 'inline-flex', alignItems: 'center' }}>
          <MonochromeMark size={size} color={logoColor} testId="logo-monochrome" />
        </div>
      );
    }

    // Full lockup variants (full, dark, light)
    return (
      <FullLockup
        ref={ref}
        variant={variant}
        size={size}
        testId={`logo-${variant}`}
        className={className}
        style={combinedStyle}
        {...props}
      />
    );
  }
);

Logo.displayName = 'Logo';

export default Logo;
