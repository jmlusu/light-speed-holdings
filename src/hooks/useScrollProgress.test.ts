import { describe, expect, it } from 'vitest';
import { computeScrollProgress, type ScrollSource } from './useScrollProgress';

const source = (scrollY: number, scrollHeight: number, innerHeight = 800): ScrollSource => ({
  scrollY,
  innerHeight,
  document: { documentElement: { scrollHeight } },
});

describe('computeScrollProgress', () => {
  it('returns 0 at the top of the page', () => {
    expect(computeScrollProgress(source(0, 4000))).toBe(0);
  });

  it('returns a normalized midpoint', () => {
    // scrollable = 4000 − 800 = 3200 → 1600 / 3200 = 0.5
    expect(computeScrollProgress(source(1600, 4000))).toBeCloseTo(0.5, 5);
  });

  it('clamps past-the-end scrolling to 1', () => {
    expect(computeScrollProgress(source(99_999, 4000))).toBe(1);
  });

  it('returns 0 when the page is not scrollable', () => {
    expect(computeScrollProgress(source(100, 800))).toBe(0);
    expect(computeScrollProgress(source(100, 0))).toBe(0);
  });

  it('falls back to body.scrollHeight when documentElement reports 0', () => {
    const mixed: ScrollSource = {
      scrollY: 500,
      innerHeight: 1000,
      document: {
        documentElement: { scrollHeight: 0 },
        body: { scrollHeight: 3000 },
      },
    };
    expect(computeScrollProgress(mixed)).toBeCloseTo(0.25, 5);
  });
});
