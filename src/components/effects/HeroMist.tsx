import React, { useEffect, useRef } from 'react';

interface HeroMistProps {
  theme: 'light' | 'dark';
}

function prefersReducedMotion(): boolean {
  return typeof window !== 'undefined'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function isCoarseOrNarrow(): boolean {
  if (typeof window === 'undefined') return false;
  return window.innerWidth < 768 || window.matchMedia('(pointer: coarse)').matches;
}

/**
 * Ambient hero mist — CSS blurred radial gradients only (Part 1, option A).
 * Gated on prefers-reduced-motion and mobile/coarse pointer.
 */
export const HeroMist: React.FC<HeroMistProps> = ({ theme }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const hide = () => { el.style.display = 'none'; };
    if (prefersReducedMotion() || isCoarseOrNarrow()) {
      hide();
      return;
    }
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const onChange = () => {
      if (mq.matches) hide();
      else el.style.display = '';
    };
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);

  return (
    <div
      ref={ref}
      aria-hidden="true"
      className={`hero-mist ${theme === 'light' ? 'hero-mist-light' : 'hero-mist-dark'}`}
    >
      <span className="hero-mist-blob hero-mist-blob-1" />
      <span className="hero-mist-blob hero-mist-blob-2" />
      <span className="hero-mist-blob hero-mist-blob-3" />
      <span className="hero-mist-blob hero-mist-blob-4" />
      <span className="hero-mist-blob hero-mist-blob-5" />
      <span className="hero-mist-blob hero-mist-blob-6" />
    </div>
  );
};

export default HeroMist;
