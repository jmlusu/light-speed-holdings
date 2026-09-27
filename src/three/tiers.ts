/**
 * Mount-tier classification for the immersive stage (plan.md / ADR-036).
 *
 *   none  → no WebGL2, prefers-reduced-motion, or Save-Data: static poster, zero canvas bytes
 *   lite  → coarse pointer or deviceMemory ≤ 4 GB: cheaper scene, DPR ≤ 1.5
 *   full  → otherwise: DPR ≤ 2, antialias on
 *
 * The scene module (`./Scene`) must not be imported until a tier other than
 * `none` has been confirmed AND the stage is visible AND the browser is idle.
 */

export type MountTier = 'none' | 'lite' | 'full';

export interface TierEnv {
  webgl2: boolean;
  reducedMotion: boolean;
  saveData: boolean;
  coarsePointer: boolean;
  deviceMemoryGB?: number;
}

let cachedWebgl2: boolean | null = null;

const probeWebGL2 = (): boolean => {
  if (cachedWebgl2 !== null) return cachedWebgl2;
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('webgl2');
    cachedWebgl2 = ctx !== null;
    if (ctx && typeof ctx.getExtension === 'function') {
      ctx.getExtension('WEBGL_lose_context')?.loseContext();
    }
  } catch {
    cachedWebgl2 = false;
  }
  return cachedWebgl2;
};

/** Test hook: reset the memoized WebGL2 probe. */
export const resetWebGL2Probe = (): void => {
  cachedWebgl2 = null;
};

export const detectTierEnv = (): TierEnv => {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return {
      webgl2: false,
      reducedMotion: false,
      saveData: false,
      coarsePointer: false,
    };
  }
  const nav = navigator as Navigator & {
    deviceMemory?: number;
    connection?: { saveData?: boolean };
  };
  const media = (query: string): boolean =>
    typeof window.matchMedia === 'function' ? window.matchMedia(query).matches : false;

  return {
    webgl2: probeWebGL2(),
    reducedMotion: media('(prefers-reduced-motion: reduce)'),
    saveData: Boolean(nav.connection?.saveData),
    coarsePointer: media('(pointer: coarse)'),
    deviceMemoryGB: nav.deviceMemory,
  };
};

export const classifyTier = (env: TierEnv): MountTier => {
  if (!env.webgl2 || env.reducedMotion || env.saveData) return 'none';
  if (env.coarsePointer) return 'lite';
  if (typeof env.deviceMemoryGB === 'number' && env.deviceMemoryGB <= 4) return 'lite';
  return 'full';
};

export const getMountTier = (): MountTier => {
  try {
    return classifyTier(detectTierEnv());
  } catch {
    return 'none';
  }
};
