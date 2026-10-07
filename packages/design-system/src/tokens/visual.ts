/**
 * Design Tokens — Shadows, Radius, Breakpoints, Motion
 *
 * Source: brand/tokens/brand-tokens.json + Directive §21, §33
 */

export const shadows = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  glowCyan: '0 0 20px rgba(0, 191, 255, 0.3)',
  glowRed: '0 0 20px rgba(230, 57, 70, 0.3)',
  // Dark mode variants (use rgba(0,0,0,0.3) base)
  dark: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3)',
  },
} as const;

export const radius = {
  small: '4px',
  medium: '8px',
  large: '16px',
  full: '9999px',
} as const;

export const breakpoints = {
  mobile: '640px',
  tablet: '640px',
  laptop: '1024px',
  desktop: '1280px',
  largeDesktop: '1536px',
  // Media query strings
  media: {
    mobile: '(max-width: 639px)',
    tablet: '(min-width: 640px) and (max-width: 1023px)',
    laptop: '(min-width: 1024px) and (max-width: 1279px)',
    desktop: '(min-width: 1280px) and (max-width: 1535px)',
    largeDesktop: '(min-width: 1536px)',
  },
} as const;

export const motion = {
  durations: {
    reveal: '600ms',
    fade: '300ms',
    slideUp: '400ms',
    scale: '200ms',
    lineDraw: '800ms',
    numberCount: '1000ms',
  },
  easings: {
    reveal: 'cubic-bezier(0.16, 1, 0.3, 1)',
    fade: 'ease-out',
    slideUp: 'cubic-bezier(0.16, 1, 0.3, 1)',
    scale: 'ease-out',
    lineDraw: 'ease-in-out',
    numberCount: 'ease-out',
  },
  // Motion types
  types: {
    reveal: { duration: '600ms', easing: 'cubic-bezier(0.16, 1, 0.3, 1)' },
    fade: { duration: '300ms', easing: 'ease-out' },
    slideUp: { duration: '400ms', easing: 'cubic-bezier(0.16, 1, 0.3, 1)' },
    scale: { duration: '200ms', easing: 'ease-out' },
    lineDraw: { duration: '800ms', easing: 'ease-in-out' },
    numberCount: { duration: '1000ms', easing: 'ease-out' },
    parallax: { duration: 'scroll-linked', easing: 'none' },
  },
  // Reduced motion
  reducedMotion: {
    duration: '0.01ms',
    iterationCount: 1,
  },
} as const;

export type Shadows = typeof shadows;
export type Radius = typeof radius;
export type Breakpoints = typeof breakpoints;
export type Motion = typeof motion;
