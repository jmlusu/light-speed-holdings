import type { CSSProperties } from 'react';
import { BRAND, colorWithAlpha, themeBackground, type StageTheme } from './materials';

/** Brand spacing base unit (brand-tokens: spacing.baseUnit = 4) — poster grid step in px. */
const GRID_PX = 4;

/**
 * Theme-aware static poster shown when the mount gate resolves to `none`
 * (no WebGL2 / reduced-motion / Save-Data) or when the WebGL boot fails
 * (import error, context loss). Zero canvas bytes, same brand look:
 * brand gradient + 4px brand grid + cyan glow + red CTA-corner hint.
 */
export const posterStyles = (theme: StageTheme): CSSProperties => {
  const dark = theme === 'dark';
  const gridLine = dark ? colorWithAlpha(BRAND.cyan, 0.07) : colorWithAlpha(BRAND.greyDark, 0.1);
  const cyanGlow = dark ? colorWithAlpha(BRAND.cyan, 0.2) : colorWithAlpha(BRAND.cyan, 0.13);
  const redHint = dark ? colorWithAlpha(BRAND.red, 0.14) : colorWithAlpha(BRAND.red, 0.09);
  const base = dark
    ? `linear-gradient(180deg, ${BRAND.navy} 0%, ${BRAND.slate} 100%)`
    : `linear-gradient(180deg, ${BRAND.white} 0%, ${themeBackground('light')} 100%)`;

  return {
    backgroundColor: themeBackground(theme),
    backgroundImage: [
      `repeating-linear-gradient(0deg, ${gridLine} 0 1px, transparent 1px ${GRID_PX}px)`,
      `repeating-linear-gradient(90deg, ${gridLine} 0 1px, transparent 1px ${GRID_PX}px)`,
      `radial-gradient(70% 50% at 50% 38%, ${cyanGlow} 0%, transparent 70%)`,
      `radial-gradient(45% 35% at 82% 88%, ${redHint} 0%, transparent 70%)`,
      base,
    ].join(', '),
  };
};
