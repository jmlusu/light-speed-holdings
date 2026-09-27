import { describe, expect, it } from 'vitest';
import { classifyTier, getMountTier, type TierEnv } from './tiers';

const baseEnv: TierEnv = {
  webgl2: true,
  reducedMotion: false,
  saveData: false,
  coarsePointer: false,
  deviceMemoryGB: 8,
};

describe('classifyTier', () => {
  it('returns none without WebGL2', () => {
    expect(classifyTier({ ...baseEnv, webgl2: false })).toBe('none');
  });

  it('returns none under prefers-reduced-motion', () => {
    expect(classifyTier({ ...baseEnv, reducedMotion: true })).toBe('none');
  });

  it('returns none on Save-Data', () => {
    expect(classifyTier({ ...baseEnv, saveData: true })).toBe('none');
  });

  it('returns lite on coarse pointer', () => {
    expect(classifyTier({ ...baseEnv, coarsePointer: true })).toBe('lite');
  });

  it('returns lite at deviceMemory <= 4 GB', () => {
    expect(classifyTier({ ...baseEnv, deviceMemoryGB: 4 })).toBe('lite');
  });

  it('returns full for capable desktops', () => {
    expect(classifyTier(baseEnv)).toBe('full');
  });

  it('returns full when deviceMemory is unknown', () => {
    expect(classifyTier({ ...baseEnv, deviceMemoryGB: undefined })).toBe('full');
  });

  it('none wins over lite conditions', () => {
    expect(classifyTier({ ...baseEnv, webgl2: false, coarsePointer: true })).toBe('none');
  });
});

describe('getMountTier (jsdom)', () => {
  it('resolves to none where WebGL2 is unavailable', () => {
    // jsdom has no WebGL2 context — the stage must stay on the static poster.
    expect(getMountTier()).toBe('none');
  });
});
