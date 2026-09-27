import { describe, expect, it } from 'vitest';
import { BRAND, colorWithAlpha, ensureContrast, mix } from './materials';
import { posterStyles } from './poster';

describe('materials', () => {
  it('colorWithAlpha converts brand hexes to rgba', () => {
    expect(colorWithAlpha(BRAND.cyan, 0.5)).toBe('rgba(0, 191, 255, 0.5)');
    expect(colorWithAlpha(BRAND.red, 1)).toBe('rgba(230, 57, 70, 1)');
  });

  it('mix interpolates between two brand hexes', () => {
    expect(mix(BRAND.navy, BRAND.white, 0)).toBe(BRAND.navy.toUpperCase());
    expect(mix(BRAND.navy, BRAND.white, 1)).toBe(BRAND.white.toUpperCase());
    expect(mix(BRAND.navy, BRAND.white, 0.5)).toBe('#8385A0');
  });

  it('ensureContrast lifts near-background hues and leaves distinct hues alone', () => {
    // slate ≈ navy luminance → must be lifted toward white on the dark field
    expect(ensureContrast(BRAND.slate, BRAND.navy)).not.toBe(BRAND.slate);
    // cyan is unmistakable on navy → untouched
    expect(ensureContrast(BRAND.cyan, BRAND.navy)).toBe(BRAND.cyan);
    // white nearly matches the light field → pulled toward navy
    expect(ensureContrast(BRAND.white, BRAND.mist)).not.toBe(BRAND.white);
    // slate reads fine on the light field
    expect(ensureContrast(BRAND.slate, BRAND.mist)).toBe(BRAND.slate);
  });

  it('defines the palette once — the eight brand tokens', () => {
    expect(Object.values(BRAND)).toHaveLength(8);
    expect(BRAND.navy).toBe('#070A40');
    expect(BRAND.red).toBe('#E63946');
    expect(BRAND.cyan).toBe('#00BFFF');
  });
});

describe('posterStyles', () => {
  it('renders a theme-aware gradient + 4px brand grid for both themes', () => {
    for (const theme of ['light', 'dark'] as const) {
      const style = posterStyles(theme);
      expect(style.backgroundImage).toContain('repeating-linear-gradient');
      expect(style.backgroundImage).toContain('1px 4px'); // brand 4px base grid
      expect(style.backgroundImage).toContain('rgba(0, 191, 255'); // cyan glow (both themes)
      expect(style.backgroundColor).toBe(theme === 'dark' ? BRAND.navy : BRAND.mist);
      expect(style.backgroundImage).toContain(theme === 'dark' ? BRAND.slate : BRAND.white);
    }
  });
});
