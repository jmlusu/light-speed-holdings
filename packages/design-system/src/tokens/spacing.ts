/**
 * Design Tokens — Spacing
 *
 * Source: brand/tokens/brand-tokens.json
 * Base unit: 4px
 * Scale: [4, 8, 12, 16, 24, 32, 48, 64, 96]
 * Directive §5, §7
 */

export const spacing = {
  baseUnit: 4,
  scale: [4, 8, 12, 16, 24, 32, 48, 64, 96],

  // Named spacing tokens
  1: '4px',
  2: '8px',
  3: '12px',
  4: '16px',
  5: '20px',
  6: '24px',
  8: '32px',
  10: '40px',
  12: '48px',
  16: '64px',
  20: '80px',
  24: '96px',
  32: '128px',

  // Semantic spacing
  section: {
    vertical: '64px',    // spacing-16
    horizontal: '48px',  // spacing-12
    mobileVertical: '48px',   // spacing-12
    mobileHorizontal: '24px', // spacing-6
  },
  component: {
    gap: '24px',      // spacing-6
    gapLoose: '32px', // spacing-8
    gapTight: '12px', // spacing-3
    inline: '8px',    // spacing-2
  },
  container: {
    maxWidth: '1200px',
    padding: '48px',  // spacing-12
  },
} as const;

export type Spacing = typeof spacing;
