import React from 'react';
import { Plus } from 'lucide-react';
import { Reveal } from '../Reveal';
import { SectionHeading } from './SectionHeading';
import { faqs } from '../../data/faqs';

interface FaqSectionProps {
  theme: 'light' | 'dark';
  /** Optional DOM id so in-page links (e.g. footer /#faq) can target this section. */
  id?: string;
}

/**
 * FAQ section rendered from the §15 FAQ registry (src/data/faqs.ts).
 * Native <details>/<summary> keeps it keyboard-accessible with no JS state.
 */
export const FaqSection: React.FC<FaqSectionProps> = ({ theme, id }) => {
  const isLight = theme === 'light';
  const bgImage = isLight
    ? '/assets/aistudio/Modern_Villa_Overlooking_a_Mountain_Valley_68700962.png'
    : '/assets/aistudio/Futuristic_Villa_Overlooking_Neon_Valley_84caad32.png';

  return (
    <section
      id={id}
      aria-label="Frequently asked questions"
      className={`relative w-full py-[100px] px-6 lg:px-12 scroll-mt-28 overflow-hidden transition-colors duration-300 ${
        isLight ? 'bg-[#F2F2F2] text-ls-navy' : 'bg-[#121518] text-white'
      }`}
    >
      {/* Background Architectural Valley Imagery */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src={bgImage}
          alt="Villa Overlooking Mountain Valley Background"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-65 dark:opacity-75 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Atmospheric Scrim Overlay for optimal readability & typography clarity */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-[#F2F2F2]/80 via-[#F2F2F2]/55 to-[#F2F2F2]/85'
              : 'bg-gradient-to-b from-[#070A40]/85 via-[#070A40]/65 to-[#070A40]/90'
          }`}
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto w-full">
        <Reveal>
          <SectionHeading
            theme={theme}
            eyebrow="HONEST ANSWERS"
            title="Frequently Asked Questions"
            lead="Straight answers grounded in how the platform actually works, including what we have not proven yet."
          />
          <div className="max-w-3xl mx-auto space-y-3.5 mt-8">
            {faqs.map((faq) => (
              <details
                key={faq.id}
                className={`group rounded-2xl overflow-hidden border backdrop-blur-xl transition-all duration-300 ${
                  isLight
                    ? 'bg-white/85 border-slate-200/90 shadow-md hover:border-slate-300 hover:shadow-lg'
                    : 'bg-[#070A40]/75 border-white/10 shadow-xl hover:border-white/20'
                }`}
              >
                <summary className={`flex items-center justify-between gap-4 px-6 py-4 cursor-pointer list-none text-sm font-bold font-display transition-colors ${
                  isLight ? 'text-ls-navy hover:text-[#DC3641]' : 'text-white hover:text-[#00BFFF]'
                }`}>
                  {faq.question}
                  <Plus
                    className="w-4 h-4 shrink-0 text-[#DC3641] transition-transform group-open:rotate-45"
                    aria-hidden="true"
                  />
                </summary>
                <p className={`px-6 pb-5 text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-slate-300'}`}>
                  {faq.answer}
                </p>
              </details>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
};

export default FaqSection;
