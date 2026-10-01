import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { NewsletterSignup } from '../components/NewsletterSignup';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { CtaBand } from '../components/site/CtaBand';
import { SectionHeading } from '../components/site/SectionHeading';
import { Reveal } from '../components/Reveal';
import { insightCategories } from '../data/siteContent';
import { insightArticles, formatInsightDate } from '../data/insights';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

interface InsightsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const InsightsPage: React.FC<InsightsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  useEffect(() => {
    trackJourneyEvent({
      eventType: 'insight_view',
      contentType: 'index',
      journeyStage: 'consideration',
    });
  }, []);

  return (
    <>
      <section
        aria-labelledby="insights-heading"
        className={`px-4 sm:px-8 pt-16 sm:pt-20 pb-2 max-w-7xl mx-auto w-full ${
          isLight ? 'text-ls-navy' : 'text-ls-white'
        }`}
      >
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest">
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
            <span>INSIGHTS // PHAROS</span>
          </div>
          <h1
            id="insights-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}
          >
            Evidence, Research &amp; the Agentic AI Canon
          </h1>
          <p
            className={`max-w-2xl text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}
          >
            Original research and executive briefings on AI strategy, data residency, and
            governance — written for boards, not engineers, and grounded in production systems.
          </p>
        </div>
      </section>

      {/* §13 content categories */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-2" aria-label="Insight categories">
        <SectionHeading
          theme={theme}
          eyebrow="TOPICS"
          title="What We Write About"
          lead="Short posts and deeper reports across the full agentic AI canon — from operating models to SADC policy."
        />
        <Reveal>
          <ul className="flex flex-wrap gap-2.5">
            {insightCategories.map((cat) => (
              <li
                key={cat}
                className={`px-3.5 py-1.5 rounded-full border font-body text-[11px] font-bold tracking-wider ${
                  isLight
                    ? 'border-ls-grey-dark/40 bg-ls-white text-ls-navy'
                    : 'border-ls-white/15 bg-ls-navy/80 text-ls-white'
                }`}
              >
                {cat}
              </li>
            ))}
          </ul>
        </Reveal>
      </section>

      {/* §16 insight journey: topic → insight */}
      <section aria-label="Featured insights" className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-14 pb-4">
        <SectionHeading
          theme={theme}
          eyebrow="LATEST"
          title="Featured Insights"
          lead="Grounded, first-party analysis — each piece cites its sources and links onward to the solutions and sectors it touches."
        />
        <div className="grid md:grid-cols-3 gap-5">
          {insightArticles.map((article) => (
            <Reveal key={article.slug}>
              <Link
                to={`/insights/${article.slug}`}
                className={`group rounded-3xl border p-6 h-full flex flex-col gap-3 transition-all ${
                  isLight
                    ? 'border-ls-grey-dark/30 bg-ls-white hover:border-ls-red/60'
                    : 'border-ls-white/15 bg-ls-navy/80 hover:border-ls-red/60'
                }`}
              >
                <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">
                  {article.topic}
                </span>
                <h3
                  className={`text-lg font-black font-display leading-snug ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}
                >
                  {article.title}
                </h3>
                <p
                  className={`text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  {article.dek}
                </p>
                <div
                  className={`mt-auto pt-3 flex items-center justify-between font-body text-[10px] font-bold tracking-widest uppercase ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  <span>
                    {formatInsightDate(article.publishedAt)} · {article.readMins} MIN READ
                  </span>
                  <span className="inline-flex items-center gap-1.5 text-ls-red">
                    Read
                    <ArrowRight className="w-3 h-3 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
                  </span>
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/proof', label: 'Proof' },
          { to: '/what-we-do', label: 'What We Do' },
          { to: '/sectors', label: 'Sectors' },
          { to: '/ask', label: 'Ask LightSpeed' },
        ]}
      />

      <NewsletterSignup theme={theme} id="newsletter" />

      <CtaBand theme={theme} onRequestBriefing={onRequestBriefing} />
    </>
  );
};

export default InsightsPage;
