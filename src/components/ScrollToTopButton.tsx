import React, { useState, useEffect } from 'react';
import { ArrowUp } from 'lucide-react';
import { MachineScrewHead } from './TactileHardwareElements';

interface ScrollToTopButtonProps {
  theme?: 'light' | 'dark';
}

export const ScrollToTopButton: React.FC<ScrollToTopButtonProps> = ({
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [isVisible, setIsVisible] = useState<boolean>(false);
  const [scrollProgress, setScrollProgress] = useState<number>(0);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
      
      setScrollProgress(Math.min(100, Math.max(0, progress)));
      if (scrollTop > 350) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2 group animate-in fade-in slide-in-from-bottom-4 duration-300 pointer-events-auto">
      {/* Tactile Hardware Scroll-To-Top Button */}
      <button
        onClick={scrollToTop}
        className={`p-3 rounded-2xl border transition-all duration-300 flex items-center gap-2.5 shadow-2xl relative overflow-hidden group/btn cursor-pointer active:scale-95 ${
          isLight
            ? 'bg-slate-100 border-slate-300 text-slate-900 hover:border-amber-500 shadow-slate-900/10'
            : 'bg-slate-900/90 border-slate-800 text-amber-300 hover:border-amber-500 shadow-black/80'
        }`}
        title="Return to Top"
      >
        <MachineScrewHead isLight={isLight} className="absolute top-1 left-1" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-1 right-1" />

        {/* Circular Progress Ring */}
        <div className="relative w-7 h-7 flex items-center justify-center shrink-0">
          <svg className="w-7 h-7 -rotate-90" viewBox="0 0 36 36">
            <path
              className={isLight ? "text-slate-300" : "text-zinc-800"}
              strokeWidth="3"
              stroke="currentColor"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              className="text-amber-500 transition-all duration-150 ease-out"
              strokeDasharray={`${scrollProgress}, 100`}
              strokeWidth="3.5"
              strokeLinecap="round"
              stroke="currentColor"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
          </svg>
          <ArrowUp className="w-3.5 h-3.5 text-amber-500 absolute group-hover/btn:-translate-y-0.5 transition-transform font-black" />
        </div>

        <div className="hidden sm:flex flex-col text-left pl-0.5 pr-1">
          <span className="text-[9px] font-mono font-bold uppercase tracking-wider text-amber-500 leading-none">
            TOP
          </span>
          <span className="text-[8px] font-mono text-zinc-400 leading-tight mt-0.5">
            {Math.round(scrollProgress)}%
          </span>
        </div>
      </button>
    </div>
  );
};
