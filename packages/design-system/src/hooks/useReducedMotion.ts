/**
 * useReducedMotion Hook
 *
 * Respects user's prefers-reduced-motion setting
 * Directive §21, §32
 */

import { useState, useEffect } from 'react';

export function useReducedMotion(): boolean {
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setReducedMotion(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return reducedMotion;
}

/**
 * Get motion props for components that respect reduced motion
 */
export function getMotionProps(reducedMotion: boolean) {
  if (reducedMotion) {
    return {
      style: {
        animationDuration: '0.01ms',
        animationIterationCount: 1,
        transitionDuration: '0.01ms',
      },
    };
  }
  return {};
}
