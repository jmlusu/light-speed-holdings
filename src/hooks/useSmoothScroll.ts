/**
 * In-page smooth scroll with cubic-bezier(0.25, 1, 0.5, 1) (Part 1 cascade curve).
 * Falls back to native scrollIntoView when reduced-motion is preferred.
 */

const P1 = 0.25;
const P2 = 1;
const P3 = 0.5;
const DURATION_MS = 650;

function bezierY(t: number): number {
  // cubic-bezier(x1,y1,x2,y2) with x1=P1,y1=P2,x2=P3,y2=1 — solve y for x≈t via sampling
  const u = 1 - t;
  // Approximate y for parameter t (same parameterization as CSS for this curve shape)
  return 3 * u * u * t * P2 + 3 * u * t * t * 1 + t * t * t;
}

export function prefersReducedMotion(): boolean {
  return typeof window !== 'undefined'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function smoothScrollToElement(el: HTMLElement): void {
  if (prefersReducedMotion()) {
    el.scrollIntoView({ behavior: 'auto', block: 'start' });
    return;
  }

  const startY = window.scrollY;
  const endY = el.getBoundingClientRect().top + startY;
  const delta = endY - startY;
  if (Math.abs(delta) < 1) return;

  const start = performance.now();

  const step = (now: number) => {
    const t = Math.min(1, (now - start) / DURATION_MS);
    const y = startY + delta * bezierY(t);
    window.scrollTo(0, y);
    if (t < 1) requestAnimationFrame(step);
  };

  requestAnimationFrame(step);
}

export function scrollToHash(hash: string): void {
  const id = hash.startsWith('#') ? hash.slice(1) : hash;
  if (!id) return;
  const el = document.getElementById(id);
  if (el) smoothScrollToElement(el);
}
