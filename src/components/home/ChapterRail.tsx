import React, { useEffect, useRef, useState } from 'react';
import { homeImmersiveCopy } from '../../data/homeImmersiveCopy';
import { smoothScrollToElement } from '../../hooks/useSmoothScroll';

interface ChapterRailProps {
  theme: 'light' | 'dark';
}

/**
 * Fixed left chapter rail (01–07). Tracks the active chapter with a scroll
 * spy: the active chapter is the last one whose top has crossed 40% of the
 * viewport — robust for short sections and the un-tracked About band (which
 * keeps the previous chapter lit). A brief click-lock (500ms) holds the
 * clicked chapter after programmatic scroll so short sections don't
 * immediately flip to the next. Labels are sr-only until 2xl; between lg
 * and 2xl they surface as an aria-hidden hover/focus pill right of the number.
 */
export const ChapterRail: React.FC<ChapterRailProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const { chapters } = homeImmersiveCopy;
  const [active, setActive] = useState<string>(chapters[0]?.id ?? '');
  const clickLockedUntil = useRef<number>(0);

  useEffect(() => {
    if (typeof window === 'undefined') return undefined;
    let frame = 0;

    const measure = () => {
      frame = 0;
      if (Date.now() < clickLockedUntil.current) return;
      const line = window.innerHeight * 0.4;
      let current = chapters[0]?.id ?? '';
      for (const chapter of chapters) {
        const el = document.getElementById(chapter.id);
        if (el && el.getBoundingClientRect().top <= line) current = chapter.id;
      }
      setActive(current);
    };

    const schedule = () => {
      if (frame) return;
      frame = window.requestAnimationFrame(measure);
    };

    measure();
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    return () => {
      if (frame) window.cancelAnimationFrame(frame);
      window.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', schedule);
    };
  }, [chapters]);

  const jump = (event: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const el = document.getElementById(id);
    if (!el) return;
    event.preventDefault();
    clickLockedUntil.current = Date.now() + 500;
    setActive(id);
    smoothScrollToElement(el);
    el.focus({ preventScroll: true });
  };

  return (
    <nav
      aria-label="Page chapters"
      className={`hidden lg:flex fixed left-3 xl:left-5 top-1/2 -translate-y-1/2 z-40 flex-col gap-1 rounded-full border p-2 backdrop-blur-md shadow-lg ${
        isLight
          ? 'bg-ls-white/85 border-ls-grey-dark/25'
          : 'bg-ls-slate/85 border-ls-white/10'
      }`}
    >
      {chapters.map((chapter) => {
        const isActive = chapter.id === active;
        return (
          <a
            key={chapter.id}
            href={`#${chapter.id}`}
            onClick={(event) => jump(event, chapter.id)}
            aria-current={isActive ? 'true' : undefined}
            className={`group relative flex items-center gap-2 rounded-full px-2.5 py-1.5 font-body text-[11px] font-bold tracking-widest transition-colors ${
              isActive
                ? 'text-ls-red bg-ls-red/10'
                : isLight
                  ? 'text-ls-navy/75 hover:text-ls-red'
                  : 'text-ls-grey-light-text hover:text-ls-red'
            }`}
          >
            <span aria-hidden="true">{chapter.num}</span>
            <span className="sr-only 2xl:not-sr-only">{chapter.label}</span>
            {/* Hover/focus label pill — shown only below 2xl where the inline label is hidden. */}
            <span
              aria-hidden="true"
              className={`2xl:hidden pointer-events-none absolute left-full top-1/2 -translate-y-1/2 ml-2 whitespace-nowrap rounded-full border px-2.5 py-1 font-body text-[10px] font-bold tracking-widest opacity-0 transition-opacity duration-200 group-hover:opacity-100 group-focus-visible:opacity-100 ${
                isLight
                  ? 'bg-ls-white/95 border-ls-grey-dark/25 text-ls-navy'
                  : 'bg-ls-slate/95 border-ls-white/10 text-ls-white'
              }`}
            >
              {chapter.label}
            </span>
          </a>
        );
      })}
    </nav>
  );
};

export default ChapterRail;
