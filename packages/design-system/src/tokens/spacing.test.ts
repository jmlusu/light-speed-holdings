import { describe, it, expect } from 'vitest';
import { spacing } from './spacing';

describe('spacing tokens', () => {
  it('has base unit', () => {
    expect(spacing.baseUnit).toBe(4);
  });

  it('has scale', () => {
    expect(spacing.scale).toEqual([4, 8, 12, 16, 24, 32, 48, 64, 96]);
  });

  it('has named spacing', () => {
    expect(spacing[1]).toBe('4px');
    expect(spacing[4]).toBe('16px');
    expect(spacing[12]).toBe('48px');
    expect(spacing[24]).toBe('96px');
  });

  it('has semantic spacing', () => {
    expect(spacing.section.vertical).toBe('64px');
    expect(spacing.component.gap).toBe('24px');
    expect(spacing.container.maxWidth).toBe('1200px');
  });
});
