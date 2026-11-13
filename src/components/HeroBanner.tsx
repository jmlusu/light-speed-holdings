import React from 'react';
import { ArrowRight } from 'lucide-react';

interface HeroBannerProps {
  theme: 'light' | 'dark';
  onOpenContactModal: (intent?: string) => void;
}

export const HeroBanner: React.FC<HeroBannerProps> = ({ theme, onOpenContactModal }) => {
  const isLight = theme === 'light';

  return (
    <div className="relative overflow-hidden rounded-3xl p-8 sm:p-12 text-center max-w-4xl mx-auto mb-8">
      {/* Attached Hexagonal Background */}
      <div className="absolute inset-0 z-0 pointer-events-none select-none opacity-30 dark:opacity-15">
        <div
          className={`absolute inset-0 ${
            isLight
              ? 'bg-gradient-to-b from-white/80 via-white/90 to-white'
              : 'bg-gradient-to-b from-ls-navy/80 via-ls-navy/90 to-ls-navy'
          }`}
        />
      </div>

      <div className="relative z-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-body font-bold uppercase tracking-wider mb-4 select-none">
          <span className="w-2 h-2 rounded-full bg-ls-emerald" />
          <span className={isLight ? 'text-[10px] font-body tracking-widest text-ls-navy' : 'text-[10px] font-body tracking-widest text-ls-grey-light-text'}>
            INSTITUTIONAL CHARTER // SOVEREIGN MISSION
          </span>
        </div>
        <h1 className={isLight ? 'text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words text-ls-navy' : 'text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words text-ls-white'}>
          About <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-red/40 to-ls-red/85">LightSpeed</span>
        </h1>
        <p className={isLight ? 'text-base sm:text-lg leading-relaxed font-sans italic text-ls-grey-dark' : 'text-base sm:text-lg leading-relaxed font-sans italic text-ls-grey-light-text'}>
          "Africa does not need to wait for the future of enterprise. It can build it."
        </p>
      </div>
    </div>
  );
};
