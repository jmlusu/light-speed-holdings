import React from 'react';

interface ImpactImageSectionProps {
  imageSrc: string;
  eyebrow: string;
  title: string;
  quote: string;
  author?: string;
  badge?: string;
  reverse?: boolean;
}

export const ImpactImageSection: React.FC<ImpactImageSectionProps> = ({
  imageSrc,
  eyebrow,
  title,
  quote,
  author,
  badge,
  reverse = false,
}) => {
  return (
    <section className="relative py-[100px] px-6 lg:px-12 min-h-[600px] flex items-center overflow-hidden bg-[#070A40]">
      {/* Immersive Background Image */}
      <div className="absolute inset-0 z-0">
        <img
          src={imageSrc}
          alt=""
          className="w-full h-full object-cover object-center scale-105"
          referrerPolicy="no-referrer"
        />
        {/* Cinematic Scrim Overlay */}
        <div className={`absolute inset-0 z-10 ${reverse
          ? 'bg-gradient-to-l from-[#070A40]/98 via-[#070A40]/80 to-transparent'
          : 'bg-gradient-to-r from-[#070A40]/98 via-[#070A40]/80 to-transparent'}`}
        />
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center relative z-20 w-full">

        {/* Text / Philosophy Column */}
        <div className={`lg:col-span-6 space-y-7 sm:space-y-8 ${reverse ? 'lg:col-start-7' : ''}`}>
          <div className="inline-flex items-center gap-2.5 px-3 py-1 bg-transparent border-none backdrop-blur-md rounded-full text-[10px] font-bold uppercase tracking-widest text-[#00BFFF]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#00BFFF] animate-pulse" />
            {eyebrow}
          </div>

          <h2 className="text-4xl lg:text-5xl font-black tracking-tight text-white leading-[1.1] font-display">
            {title}
          </h2>

          <div className="w-20 h-[2px] bg-[#DC3641]" />

          <p className="text-[#9CA3AF] text-lg leading-relaxed max-w-xl font-body">
            LightSpeed Holdings moves beyond conventional consulting into disciplined AI company building. By uniting rigorous human oversight, deterministic orchestration, and autonomous agent execution, we create enduring operational value.
          </p>

          <div className="bg-transparent border-none shadow-none p-6 rounded-2xl max-w-xl">
            <p className="text-base sm:text-lg font-medium text-white italic font-body leading-snug">
              &ldquo;{quote}&rdquo;
            </p>
            {author && (
              <p className="text-xs text-[#00BFFF] mt-3 font-bold uppercase tracking-widest">
                — {author}
              </p>
            )}
          </div>

          <div className="pt-4 flex flex-wrap items-center gap-8">
            <div className="flex flex-col">
              <span className="text-2xl font-black text-white font-display">ASPIRE.</span>
              <span className="text-[10px] text-[#9CA3AF] font-bold tracking-widest uppercase">Strategic Vision</span>
            </div>

            <div className="flex flex-col">
              <span className="text-2xl font-black text-[#DC3641] font-display">ACT.</span>
              <span className="text-[10px] text-[#9CA3AF] font-bold tracking-widest uppercase">Agentic Execution</span>
            </div>

            <div className="flex flex-col">
              <span className="text-2xl font-black text-[#00BFFF] font-display">ACHIEVE.</span>
              <span className="text-[10px] text-[#9CA3AF] font-bold tracking-widest uppercase">Governed Value</span>
            </div>
          </div>
        </div>

        {/* Floating Badge / Visual Cue Column */}
        {!reverse && badge && (
          <div className="hidden lg:flex lg:col-span-6 justify-end items-start pt-12">
            <div className="px-5 py-2 bg-transparent border-none backdrop-blur-md rounded-full text-[11px] font-bold text-[#00BFFF]">
              {badge}
            </div>
          </div>
        )}
        {reverse && badge && (
          <div className="hidden lg:flex lg:col-span-6 lg:col-start-1 lg:row-start-1 justify-start items-start pt-12">
            <div className="px-5 py-2 bg-transparent border-none backdrop-blur-md rounded-full text-[11px] font-bold text-[#00BFFF]">
              {badge}
            </div>
          </div>
        )}

      </div>
    </section>
  );
};
