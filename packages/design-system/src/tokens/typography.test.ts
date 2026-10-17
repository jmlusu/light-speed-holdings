import { describe, it, expect } from 'vitest';
import { typography } from './typography';

describe('typography tokens', () => {
  it('has font families', () => {
    expect(typography.fontFamily.sans).toContain('Arial');
    expect(typography.fontFamily.mono).toContain('SF Mono');
  });

  it('has font weights', () => {
    expect(typography.fontWeight.normal).toBe(400);
    expect(typography.fontWeight.bold).toBe(700);
    expect(typography.fontWeight.black).toBe(900);
  });

  it('has font sizes', () => {
    expect(typography.fontSize.displayXl).toBe('36pt');
    expect(typography.fontSize.body).toBe('14pt');
    expect(typography.fontSize.caption).toBe('12pt');
  });

  it('has semantic styles', () => {
    expect(typography.styles.displayXl.fontSize).toBe('36pt');
    expect(typography.styles.body.fontSize).toBe('14pt');
    expect(typography.styles.overline.textTransform).toBe('uppercase');
  });
});
