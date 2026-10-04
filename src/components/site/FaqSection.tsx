import React from 'react';
import { Plus } from 'lucide-react';
import { Reveal } from '../Reveal';
import { SectionHeading } from './SectionHeading';
import { faqs } from '../../data/faqs';

interface FaqSectionProps {
  theme: 'light' | 'dark';
}

/**
 * FAQ section rendered from the §15 FAQ registry (src/data/faqs.ts).
 * Native <details>/<summary> keeps it keyboard-accessible with no JS state.
 */
export const FaqSection: React.FC<FaqSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <section aria-label="Frequently asked questions" className="px-4 sm:px-8 pt-16 sm:pt-20 pb-8 max-w-7xl mx-auto w-full">
      <Reveal>
        <SectionHeading
          theme={theme}
          eyebrow="HONEST ANSWERS"
          title="Frequently Asked Questions"
          lead="Straight answers grounded in how the platform actually works — including what we have not proven yet."
        />
        <div className="max-w-3xl mx-auto space-y-3">
          {faqs.map((faq) => (
            <details
              key={faq.id}
              className={`group rounded-2xl border overflow-hidden ${
                isLight
                  ? 'bg-ls-white border-ls-grey-dark/20'
                  : 'bg-ls-navy border-ls-white/10'
              }`}
            >
              <summary
                className={`flex items-center justify-between gap-4 px-6 py-4 cursor-pointer list-none text-sm font-bold font-display transition-colors ${
                  isLight
                    ? 'text-ls-navy hover:text-ls-red'
                    : 'text-ls-white hover:text-ls-red'
                }`}
              >
                {faq.question}
                <Plus
                  className="w-4 h-4 shrink-0 text-ls-red transition-transform group-open:rotate-45"
                  aria-hidden="true"
                />
              </summary>
              <p
                className={`px-6 pb-5 text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}
              >
                {faq.answer}
              </p>
            </details>
          ))}
        </div>
      </Reveal>
    </section>
  );
};

export default FaqSection;
