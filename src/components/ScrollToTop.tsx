import React, { useState, useEffect } from 'react';
import { ChevronUp } from 'lucide-react';

interface ScrollToTopProps {
  theme?: 'light' | 'dark';
}

export const ScrollToTop: React.FC<ScrollToTopProps> = ({ theme = 'dark' }) => {
  const [isVisible, setIsVisible] = useState(false);
  const isLight = theme === 'light';

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.scrollY > 500) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', toggleVisibility, { passive: true });
    toggleVisibility(); // Check initial scroll position

    return () => {
      window.removeEventListener('scroll', toggleVisibility);
    };
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-6 right-6 sm:bottom-8 sm:right-8 z-40 animate-in fade-in slide-in-from-bottom-4 duration-300">
      <button
        type="button"
        onClick={scrollToTop}
        aria-label="Scroll to top of page"
        title="Scroll to top"
        className={`group relative flex flex-col items-center justify-center w-11 h-11 sm:w-12 sm:h-12 rounded-2xl cursor-pointer transition-all duration-200 focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:outline-none hover:scale-105 active:scale-95 active:translate-y-0.5 ${
          isLight
            ? 'bg-gradient-to-b from-slate-100 via-slate-200 to-slate-300 border border-slate-300/90 shadow-[0_4px_12px_rgba(0,0,0,0.12),inset_0_1px_1px_rgba(255,255,255,0.9),inset_0_-1px_2px_rgba(0,0,0,0.15)] text-slate-800 hover:from-slate-50 hover:to-slate-200'
            : 'bg-gradient-to-b from-zinc-800 via-zinc-900 to-black border border-white/20 shadow-[0_6px_16px_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.25),inset_0_-1px_2px_rgba(0,0,0,0.8)] text-zinc-200 hover:from-zinc-700 hover:to-zinc-900'
        }`}
      >
        {/* Skeuomorphic Bezel Ring */}
        <div className={`absolute inset-0.5 rounded-[14px] pointer-events-none transition-opacity border ${
          isLight 
            ? 'border-slate-300/60 bg-gradient-to-b from-white/40 to-black/5' 
            : 'border-white/10 bg-gradient-to-b from-white/10 to-transparent'
        }`} />

        {/* Orange LED Accent Indicator */}
        <div className="flex items-center gap-1 mb-0.5 z-10">
          <span className="w-1.5 h-1.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.9)] animate-pulse" />
        </div>

        {/* Tactile Arrow Icon */}
        <ChevronUp className={`w-4 h-4 sm:w-5 sm:h-5 z-10 transition-transform group-hover:-translate-y-0.5 ${
          isLight ? 'text-slate-900 drop-shadow-xs' : 'text-white drop-shadow-md'
        }`} />

        {/* Screw / Mechanical Corner Accents */}
        <div className="absolute top-1 left-1 w-1 h-1 rounded-full bg-black/20 dark:bg-white/10" />
        <div className="absolute top-1 right-1 w-1 h-1 rounded-full bg-black/20 dark:bg-white/10" />
        <div className="absolute bottom-1 left-1 w-1 h-1 rounded-full bg-black/20 dark:bg-white/10" />
        <div className="absolute bottom-1 right-1 w-1 h-1 rounded-full bg-black/20 dark:bg-white/10" />
      </button>
    </div>
  );
};
