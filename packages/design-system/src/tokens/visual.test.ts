import { describe, it, expect } from 'vitest';
import { shadows, radius, breakpoints, motion } from './visual';

describe('visual tokens', () => {
  it('has shadows', () => {
    expect(shadows.sm).toBeDefined();
    expect(shadows.md).toBeDefined();
    expect(shadows.glowCyan).toBeDefined();
    expect(shadows.dark.md).toBeDefined();
  });

  it('has radius', () => {
    expect(radius.small).toBe('4px');
    expect(radius.medium).toBe('8px');
    expect(radius.large).toBe('16px');
    expect(radius.full).toBe('9999px');
  });

  it('has breakpoints', () => {
    expect(breakpoints.mobile).toBe('640px');
    expect(breakpoints.tablet).toBe('640px');
    expect(breakpoints.laptop).toBe('1024px');
    expect(breakpoints.desktop).toBe('1280px');
    expect(breakpoints.largeDesktop).toBe('1536px');
  });

  it('has motion', () => {
    expect(motion.durations.reveal).toBe('600ms');
    expect(motion.easings.reveal).toBe('cubic-bezier(0.16, 1, 0.3, 1)');
    expect(motion.reducedMotion.duration).toBe('0.01ms');
  });
});
