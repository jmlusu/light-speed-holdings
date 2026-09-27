/**
 * Brand-sourced color constants for the immersive stage.
 *
 * Canonical source: `brand/tokens/brand-tokens.json` (ADR-020 — brand tokens only).
 * Mirrored for Tailwind v4 in `src/brand/brand-tokens.css` (`@theme`).
 *
 * RULE: no hex literal may appear anywhere else in `src/three/**` or in the
 * stage components — every color must be derived from BRAND below.
 */

export const BRAND = {
  navy: '#070A40',
  red: '#E63946',
  cyan: '#00BFFF',
  mist: '#F7F8F9',
  slate: '#121518',
  white: '#FFFFFF',
  greyDark: '#6B7280',
  greyLightText: '#9CA3AF',
} as const;

export type BrandColor = (typeof BRAND)[keyof typeof BRAND];

export type StageTheme = 'light' | 'dark';

/** Scene/fog/paper background per theme (plan: light = pale field, dark = deep navy field). */
export const themeBackground = (theme: StageTheme): BrandColor =>
  theme === 'dark' ? BRAND.navy : BRAND.mist;

/** Grid line tint per theme (4px brand grid plane). */
export const themeGridColor = (theme: StageTheme): BrandColor =>
  theme === 'dark' ? BRAND.cyan : BRAND.greyDark;

export const themeGridOpacity = (theme: StageTheme): number =>
  theme === 'dark' ? 0.5 : 0.35;

/**
 * One hue per agent category for the 90-node constellation, order matching
 * `AGENT_CATEGORIES` on the homepage (Strategy → Finance & Legal).
 *
 * DEVIATION NOTE (reported): the homepage uses `text-ls-gold/-green/-purple/
 * -pink/-teal` classes, but those five have NO token values in
 * `src/brand/brand-tokens.css` or `brand/tokens/brand-tokens.json`. ADR-020
 * forbids inventing hexes, so the seven non-navy palette tokens stand in
 * until the missing category tokens are defined (navy excluded — it equals
 * the dark-theme background).
 */
export const AGENT_CATEGORY_COLORS: readonly BrandColor[] = [
  BRAND.red, // Strategy (ls-red)
  BRAND.cyan, // Research (ls-cyan)
  BRAND.mist, // Product & Eng (stand-in for ls-gold)
  BRAND.white, // Operations (stand-in for ls-pink)
  BRAND.greyLightText, // Governance (stand-in for ls-purple)
  BRAND.greyDark, // Content & Comms (stand-in for ls-green)
  BRAND.slate, // Finance & Legal (stand-in for ls-teal)
];

const HEX_RE = /^#?([0-9a-f]{6})$/i;

const parseHex = (hex: string): [number, number, number] => {
  const match = HEX_RE.exec(hex.trim());
  if (!match) throw new Error(`materials: invalid hex color "${hex}"`);
  const value = parseInt(match[1], 16);
  return [(value >> 16) & 255, (value >> 8) & 255, value & 255];
};

const toHex = (r: number, g: number, b: number): string =>
  '#' +
  [r, g, b]
    .map((c) => Math.max(0, Math.min(255, Math.round(c))).toString(16).padStart(2, '0'))
    .join('')
    .toUpperCase();

/** `#RRGGBB` + alpha → `rgba(r, g, b, a)` (used by the static poster gradients). */
export const colorWithAlpha = (hex: string, alpha: number): string => {
  const [r, g, b] = parseHex(hex);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

/** Linear interpolation between two brand hexes, `t` in 0..1. */
export const mix = (a: string, b: string, t: number): string => {
  const [ar, ag, ab] = parseHex(a);
  const [br, bg, bb] = parseHex(b);
  const k = Math.max(0, Math.min(1, t));
  return toHex(ar + (br - ar) * k, ag + (bg - ag) * k, ab + (bb - ab) * k);
};

/** Relative luminance (WCAG), 0..1. */
export const luminance = (hex: string): number => {
  const [r, g, b] = parseHex(hex).map((c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

/**
 * Keep constellation nodes legible against the current background: if a
 * palette hue is too close to the background luminance, pull it toward the
 * opposite end of the brand range (navy on light fields, white on dark).
 * Brand hues already distinct are returned untouched.
 */
export const ensureContrast = (nodeHex: string, backgroundHex: string): string => {
  const node = luminance(nodeHex);
  const bg = luminance(backgroundHex);
  if (Math.abs(node - bg) >= 0.2) return nodeHex;
  return bg > 0.5 ? mix(nodeHex, BRAND.navy, 0.55) : mix(nodeHex, BRAND.white, 0.55);
};
