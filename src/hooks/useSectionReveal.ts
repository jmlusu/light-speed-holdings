import { useEffect, useRef, useState } from 'react';

export interface UseSectionRevealOptions {
  /** Percentage of the target's visibility needed to trigger (0.0 to 1.0) */
  threshold?: number;
  /** Margin around root bounding box (e.g. '0px 0px -60px 0px') */
  rootMargin?: string;
  /** Whether the reveal triggers only once (default: true) */
  triggerOnce?: boolean;
  /** Whether to trigger immediately on mount regardless of scroll (e.g. hero section) */
  immediate?: boolean;
}

/**
 * Hook to observe when a section enters the viewport and trigger 'reveal-up'
 * and 'reveal-fade' classes for content elements to create a staged, premium entry.
 */
export function useSectionReveal<T extends HTMLElement = HTMLElement>(
  options: UseSectionRevealOptions = {}
) {
  const {
    threshold = 0.12,
    rootMargin = '0px 0px -40px 0px',
    triggerOnce = true,
    immediate = false,
  } = options;

  const ref = useRef<T | null>(null);

  const [isVisible, setIsVisible] = useState(() => {
    if (typeof window === 'undefined') return true;
    if (immediate) return true;
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  });

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // Respect reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || immediate) {
      setIsVisible(true);
      el.classList.add('is-visible');
      el.querySelectorAll('.reveal-up, .reveal-fade, .reveal-scale').forEach((node) => {
        node.classList.add('is-visible');
      });
      return;
    }

    if (!('IntersectionObserver' in window)) {
      setIsVisible(true);
      el.classList.add('is-visible');
      el.querySelectorAll('.reveal-up, .reveal-fade, .reveal-scale').forEach((node) => {
        node.classList.add('is-visible');
      });
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (entry && entry.isIntersecting) {
          setIsVisible(true);
          // Apply is-visible to container if it carries a reveal class
          if (
            el.classList.contains('reveal-up') ||
            el.classList.contains('reveal-fade') ||
            el.classList.contains('reveal-scale')
          ) {
            el.classList.add('is-visible');
          }
          // Cascade is-visible to all staged children
          el.querySelectorAll('.reveal-up, .reveal-fade, .reveal-scale').forEach((node) => {
            node.classList.add('is-visible');
          });

          if (triggerOnce) {
            observer.disconnect();
          }
        } else if (!triggerOnce) {
          setIsVisible(false);
          el.classList.remove('is-visible');
          el.querySelectorAll('.reveal-up, .reveal-fade, .reveal-scale').forEach((node) => {
            node.classList.remove('is-visible');
          });
        }
      },
      { threshold, rootMargin }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold, rootMargin, triggerOnce, immediate]);

  /**
   * Helper to generate className strings with reveal variant, visibility state, and optional delay
   */
  const getRevealClass = (
    type: 'up' | 'fade' | 'scale' = 'up',
    delayIndex?: 1 | 2 | 3 | 4 | 5 | 6,
    additionalClasses = ''
  ): string => {
    const base = type === 'fade' ? 'reveal-fade' : type === 'scale' ? 'reveal-scale' : 'reveal-up';
    const visible = isVisible ? 'is-visible' : '';
    const delay = delayIndex ? `delay-${delayIndex}` : '';
    return [base, visible, delay, additionalClasses].filter(Boolean).join(' ');
  };

  return { ref, isVisible, getRevealClass };
}

export default useSectionReveal;
