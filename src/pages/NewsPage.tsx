import React from 'react';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { newsItems } from '../data/siteContent';

interface NewsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /news — company updates: partnerships, capabilities, research,
 * product launches, events, and announcements.
 * Each news item carries a type badge and date.
 */
export const NewsPage: React.FC<NewsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  const typeColorMap: Record<string, string> = {
    'Partnership': 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
    'Capability': 'border-ls-red/40 bg-ls-red/10 text-ls-red',
    'Research': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Product': 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
    'Event': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Company': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Policy': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
  };

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="NEWS & UPDATES"
        title="What We've Done"
        lead="New partnerships, new capabilities, new research, product launches, events, and company announcements."
      />

      <section
        id="news"
        aria-labelledby="news-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-4"
      >
        <SectionHeading
          theme={theme}
          eyebrow="UPDATES"
          title="Recent Announcements"
          lead="From published research to live operations — every update carries its honest status."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {newsItems.map((item, idx) => (
            <Reveal key={item.id} delay={(idx % 2) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border flex flex-col ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-black tracking-widest text-ls-red">
                    {item.id}
                  </span>
                  <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 font-body text-[9px] font-bold tracking-widest ${
                    typeColorMap[item.type] || 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text'
                  }`}>
                    {item.type}
                  </span>
                </div>
                <h3 className="mt-4 font-display font-bold text-lg sm:text-xl tracking-tight">
                  {item.title}
                </h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {item.description}
                </p>
                <div className={`mt-auto pt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
                }`}>
                  <span className={`text-[11px] font-body font-bold tracking-widest ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    {item.date}
                  </span>
                  <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Stay in the Loop"
        text="Follow LightSpeed for updates on agentic AI governance, AI-native transformation, and our work across Malawi and SADC."
        ctaLabel="Get Updates"
      />
    </>
  );
};

export default NewsPage;
