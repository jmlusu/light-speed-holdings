import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { faqs } from '../data/siteContent';

interface FAQPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const FAQPage: React.FC<FAQPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const [openId, setOpenId] = useState<string | null>(null);

  const toggleItem = (id: string) => {
    setOpenId(openId === id ? null : id);
  };

  return (
    <main>
      <PageIntro
        theme={theme}
        eyebrow="FAQ"
        title="Frequently Asked Questions"
        lead="Every question you might have — answered honestly. If something is not covered here, start a conversation and we will be straightforward about what we know and what we are still finding out."
      />

      <SectionHeading
        theme={theme}
        eyebrow="HONEST ANSWERS"
        title="Frequently Asked Questions"
        lead="Every claim on this site carries its honesty status. These answers follow the same standard."
      />

      <div className="px-4 sm:px-8 max-w-3xl mx-auto w-full pb-24 space-y-4">
        {faqs.map((faq, index) => {
          const isOpen = openId === faq.id;
          return (
            <Reveal key={faq.id} delay={index * 0.05}>
              <div
                className={`rounded-3xl border overflow-hidden transition-all duration-300 ${
                  isLight
                    ? 'bg-ls-white border-ls-grey-dark/20'
                    : 'bg-ls-navy/50 border-ls-white/10'
                }`}
              >
                <button
                  type="button"
                  onClick={() => toggleItem(faq.id)}
                  className={`w-full flex items-center justify-between gap-4 px-6 sm:px-8 py-5 text-left cursor-pointer hover:opacity-90 transition-opacity ${
                    isOpen
                      ? 'border-b'
                      : ''
                  } ${
                    isLight ? 'border-ls-grey-dark/10' : 'border-ls-white/5'
                  }`}
                  aria-expanded={isOpen}
                >
                  <h3
                    className={`text-sm sm:text-base font-bold leading-snug ${
                      isLight ? 'text-ls-navy' : 'text-ls-white'
                    }`}
                  >
                    {faq.question}
                  </h3>
                  <ChevronDown
                    className={`w-4 h-4 flex-shrink-0 transition-transform duration-300 ${
                      isOpen ? 'rotate-180' : ''
                    } ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}
                    aria-hidden="true"
                  />
                </button>
                {isOpen && (
                  <div className="px-6 sm:px-8 pb-5">
                    <p
                      className={`text-sm leading-relaxed font-medium ${
                        isLight
                          ? 'text-ls-grey-dark/70'
                          : 'text-ls-grey-light-text/70'
                      }`}
                    >
                      {faq.answer}
                    </p>
                  </div>
                )}
              </div>
            </Reveal>
          );
        })}
      </div>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/trust', label: 'Trust' },
          { to: '/technology#governance', label: 'Technology' },
          { to: '/leadership', label: 'Leadership' },
          { to: '/contact', label: 'Contact' },
        ]}
      />

      <CtaBand theme={theme} onRequestBriefing={onRequestBriefing} />
    </main>
  );
};

export default FAQPage;
