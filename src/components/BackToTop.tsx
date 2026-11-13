import React, { useEffect, useState } from 'react';
import { ArrowUp } from 'lucide-react';

interface BackToTopProps {
  theme?: 'light' | 'dark';
  /** Scroll threshold in pixels before showing the button (defaults to 400px - past first section) */
  scrollThreshold?: number;
}

export const BackToTop: React.FC<BackToTopProps> = ({
  theme = 'dark',
  scrollThreshold = 400,
}) => {
  const isLight = theme === 'light';
  const [isVisible, setIsVisible] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      
      const progress = scrollHeight > 0 
        ? Math.min(100, Math.max(0, (currentScrollY / scrollHeight) * 100))
        : 0;

      setScrollProgress(progress);
      setIsVisible(currentScrollY > scrollThreshold);
    };

    // Initial check in case page is already scrolled
    handleScroll();

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleScroll, { passive: true });
    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleScroll);
    };
  }, [scrollThreshold]);

  const scrollToTop = () => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: prefersReducedMotion ? 'auto' : 'smooth',
    });

    const main = document.getElementById('main-content');
    if (main) {
      main.focus({ preventScroll: true });
    }
  };

  // SVG circular progress parameters
  const size = 52;
  const strokeWidth = 3;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (scrollProgress / 100) * circumference;

  return (
    <button
      type="button"
      onClick={scrollToTop}
      aria-label={`Back to top of page (${Math.round(scrollProgress)}% scrolled)`}
      title={`Back to top (${Math.round(scrollProgress)}%)`}
      className={`fixed bottom-6 right-6 z-50 p-1 rounded-full border transition-all duration-300 shadow-2xl backdrop-blur-xl group cursor-pointer flex items-center justify-center ${
        isVisible
          ? 'opacity-100 translate-y-0 pointer-events-auto scale-100'
          : 'opacity-0 translate-y-6 pointer-events-none scale-90'
      } ${
        isLight
          ? 'bg-white/95 border-slate-300 text-ls-navy hover:bg-ls-navy hover:text-white hover:border-ls-navy shadow-[0_8px_25px_rgba(7,10,64,0.15)] ring-1 ring-slate-200'
          : 'bg-[#070A40]/90 border-ls-cyan/40 text-white hover:border-ls-cyan hover:bg-[#0c125e] shadow-[0_8px_30px_rgba(0,191,255,0.25)] ring-1 ring-ls-cyan/20'
      }`}
      style={{ width: size, height: size }}
    >
      {/* SVG Circular Progress Track and Fill */}
      <svg
        className="absolute inset-0 -rotate-90 pointer-events-none"
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
      >
        {/* Background track circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={isLight ? 'rgba(7, 10, 64, 0.1)' : 'rgba(255, 255, 255, 0.12)'}
          strokeWidth={strokeWidth}
        />
        {/* Animated Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={isLight ? '#070A40' : '#00BFFF'}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-[stroke-dashoffset] duration-150 ease-out"
        />
      </svg>

      {/* Center Arrow Icon and Hover Percentage Indicator */}
      <div className="relative z-10 flex flex-col items-center justify-center">
        <ArrowUp className="w-4 h-4 transition-transform duration-300 group-hover:-translate-y-0.5 text-ls-cyan group-hover:text-ls-cyan" />
        <span className="text-[8px] font-mono font-bold leading-none mt-0.5 opacity-75 group-hover:opacity-100 transition-opacity">
          {Math.round(scrollProgress)}%
        </span>
      </div>
    </button>
  );
};

export default BackToTop;
