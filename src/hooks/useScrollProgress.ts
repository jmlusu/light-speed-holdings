import { useEffect, useRef } from 'react';

/**
 * Minimal scroll source — structurally satisfied by `window`, and trivially
 * fakeable in tests.
 */
export interface ScrollSource {
  scrollY: number;
  innerHeight: number;
  document: {
    documentElement: { scrollHeight: number };
    body?: { scrollHeight: number } | null;
  };
}

/** Normalized page scroll progress 0..1 (0 = top, 1 = bottom of the homepage). */
export const computeScrollProgress = (source: ScrollSource = window): number => {
  const el = source.document.documentElement;
  const scrollHeight = el.scrollHeight || source.document.body?.scrollHeight || 0;
  const scrollable = scrollHeight - source.innerHeight;
  if (scrollable <= 0) return 0;
  const raw = source.scrollY / scrollable;
  return raw < 0 ? 0 : raw > 1 ? 1 : raw;
};

export interface UseScrollProgressOptions {
  /** Called every rAF with the smoothed progress (0..1). Keep it non-state to avoid re-renders. */
  onProgress: (progress: number) => void;
  /** Disable the loop entirely (e.g. before the scene is live). */
  enabled?: boolean;
  /** Smoothing factor per frame — plan range 0.08–0.15. */
  lerp?: number;
}

const REDUCED_MOTION_QUERY = '(prefers-reduced-motion: reduce)';

/**
 * rAF-lerped scroll progress. Native scrolling is never intercepted (no
 * scroll-jack, no smooth-scroll hijack): the page scrolls normally and this
 * hook only smooths the *value fed to the camera*. Under
 * `prefers-reduced-motion` the loop never starts and progress is pinned to 0
 * (the mount gate shows the static poster in that case anyway).
 */
export const useScrollProgress = ({
  onProgress,
  enabled = true,
  lerp = 0.12,
}: UseScrollProgressOptions): void => {
  const callbackRef = useRef(onProgress);
  callbackRef.current = onProgress;

  useEffect(() => {
    if (!enabled) return undefined;

    const reducedMotion =
      typeof window.matchMedia === 'function' &&
      window.matchMedia(REDUCED_MOTION_QUERY).matches;
    if (reducedMotion) {
      callbackRef.current(0);
      return undefined;
    }

    let target = computeScrollProgress();
    let current = target;
    let rafId = 0;

    const onScrollOrResize = (): void => {
      target = computeScrollProgress();
    };

    const tick = (): void => {
      rafId = requestAnimationFrame(tick);
      if (document.hidden) return; // paused while the tab is hidden
      const delta = target - current;
      current = Math.abs(delta) < 0.0004 ? target : current + delta * lerp;
      callbackRef.current(current);
    };

    window.addEventListener('scroll', onScrollOrResize, { passive: true });
    window.addEventListener('resize', onScrollOrResize);
    rafId = requestAnimationFrame(tick);
    callbackRef.current(current);

    return () => {
      cancelAnimationFrame(rafId);
      window.removeEventListener('scroll', onScrollOrResize);
      window.removeEventListener('resize', onScrollOrResize);
    };
  }, [enabled, lerp]);
};
