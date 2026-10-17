/**
 * useMediaQuery Hook
 *
 * Reactive media query matching for responsive design
 */

import { useState, useEffect } from 'react';

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// Convenience hooks for common breakpoints
export const useIsMobile = () => useMediaQuery('(max-width: 639px)');
export const useIsTablet = () => useMediaQuery('(min-width: 640px) and (max-width: 1023px)');
export const useIsLaptop = () => useMediaQuery('(min-width: 1024px) and (max-width: 1279px)');
export const useIsDesktop = () => useMediaQuery('(min-width: 1280px) and (max-width: 1535px)');
export const useIsLargeDesktop = () => useMediaQuery('(min-width: 1536px)');
export const useIsMobileOrTablet = () => useMediaQuery('(max-width: 1023px)');
export const useIsLaptopOrDesktop = () => useMediaQuery('(min-width: 1024px)');
