import React, { useEffect } from 'react';
import { Link, Navigate, useParams } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { Reveal } from '../components/Reveal';
import { PageIntro } from '../components/site/PageIntro';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { NewsletterSignup } from '../components/NewsletterSignup';
import { getInsightArticle, formatInsightDate, type InsightBlock } from '../data/insights';
import { solutions } from '../data/siteContent';
import { sectors } from '../data/sector-registry';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

interface InsightArticlePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const InsightArticlePage: React.FC<InsightArticlePageProps> = ({ theme }) => {
  const { slug } = useParams<{ slug: string }>();
  const article = slug ? getInsightArticle(slug) : undefined;

  useEffect(() => {
    if (!slug) return;
    trackJourneyEvent({
      eventType: 'insight_view',
      contentType: 'article',
      journeyStage: 'consideration',
      metadata: { slug },
    });
  }, [slug]);

  if (!article) return <Navigate to="/insights" replace />;

  const isLight = theme === 'light';
  const bodyText = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';
  const headingText = isLight ? 'text-ls-navy' : 'text-ls-white';
  const cardShell = `rounded-3xl border p-6 h-full flex flex-col gap-2 transition-all scroll-mt-28 ${
    isLight
      ? 'border-ls-grey-dark/30 bg-ls-white hover:border-ls-red/50'
      : 'border-ls-white/15 bg-ls-navy/80 hover:border-ls-red/50'
  }`;
  const related = solutions.filter((s) => article.relatedSolutions.includes(s.slug));
  const relatedSectors = sectors.filter((s) => article.relatedSectors.includes(s.id));

  const renderBlock = (block: InsightBlock, i: number): React.ReactNode => {
    switch (block.kind) {
      case 'h':
        return (
          <h2
            key={i}
            className={`pt-8 text-xl sm:text-2xl font-black tracking-tight font-display ${headingText}`}
          >
            {block.text}
          </h2>
        );
      case 'p':
        return (
          <p key={i} className={`text-sm sm:text-base leading-relaxed ${bodyText}`}>
            {block.text}
          </p>
        );
      case 'ul':
        return (
          <ul key={i} className={`list-disc pl-5 space-y-2.5 text-sm sm:text-base leading-relaxed ${bodyText}`}>
            {block.items.map((item, j) => (
              <li key={j}>{item}</li>
            ))}
          </ul>
        );
      case 'quote':
        return (
          <blockquote
            key={i}
            className={`border-l-4 border-ls-red pl-5 py-1 italic text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}
          >
            <p>{block.text}</p>
            {block.cite && (
              <cite className={`mt-2 block not-italic text-xs font-body font-bold tracking-wider ${bodyText}`}>
                — {block.cite}
              </cite>
            )}
          </blockquote>
        );
      default:
        return null;
    }
  };

  return (
    <>
      <PageIntro theme={theme} eyebrow={`INSIGHTS // ${article.topic}`} title={article.title} lead={article.dek}>
        <div
          className={`mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 font-body text-[11px] font-bold tracking-widest uppercase ${
            isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
          }`}
        >
          <span>{formatInsightDate(article.publishedAt)}</span>
          <span aria-hidden="true">·</span>
          <span>{article.readMins} min read</span>
          <span aria-hidden="true">·</span>
          <span className="text-ls-red">{article.category}</span>
        </div>
        <div
          className={`mt-4 max-w-2xl rounded-2xl border px-4 py-3 font-body text-[11px] leading-relaxed ${
            isLight
              ? 'border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark'
              : 'border-ls-white/15 bg-ls-navy/80 text-ls-grey-light-text'
          }`}
        >
          <span className="font-bold tracking-widest text-ls-red">SOURCES </span>
          {article.source}
        </div>
      </PageIntro>

      {/* Article body */}
      <article className="px-4 sm:px-8 max-w-3xl mx-auto w-full pt-6 pb-4 space-y-5">
        {article.blocks.map(renderBlock)}
      </article>

      {/* §16 related concepts: solutions + sectors */}
      <section aria-label="Related thinking" className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-2">
        <div className="space-y-10">
          <div>
            <span className="text-xs font-body font-bold tracking-widest text-ls-red">
              RELEVANT SOLUTIONS
            </span>
            <div className="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {related.map((sol) => (
                <Reveal key={sol.slug}>
                  <Link to={`/solutions#${sol.slug}`} className={`${cardShell} group`}>
                    <h3 className={`text-base font-black font-display ${headingText}`}>{sol.title}</h3>
                    <p className={`text-sm leading-relaxed ${bodyText}`}>{sol.oneLiner}</p>
                    <span className="mt-auto pt-3 inline-flex items-center gap-1.5 text-[11px] font-bold tracking-widest uppercase text-ls-red">
                      Explore <ArrowRight className="w-3 h-3" aria-hidden="true" />
                    </span>
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>
          <div>
            <span className="text-xs font-body font-bold tracking-widest text-ls-red">
              RELEVANT SECTORS
            </span>
            <div className="mt-4 grid sm:grid-cols-2 gap-4">
              {relatedSectors.map((sec) => (
                <Reveal key={sec.id}>
                  <Link to={`/sectors#${sec.id}`} className={cardShell}>
                    <div className="flex items-start justify-between gap-3">
                      <h3 className={`text-base font-black font-display ${headingText}`}>{sec.title}</h3>
                      <HonestyBadge label={sec.status} className="shrink-0" />
                    </div>
                    <p className={`text-sm leading-relaxed ${bodyText}`}>{sec.description}</p>
                    <span className="mt-auto pt-3 inline-flex items-center gap-1.5 text-[11px] font-bold tracking-widest uppercase text-ls-red">
                      Explore <ArrowRight className="w-3 h-3" aria-hidden="true" />
                    </span>
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* §16 journey CTAs: primary "Explore Related Thinking" + secondary actions */}
      <section aria-label="Continue the journey" className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-4">
        <Reveal>
          <div
            className={`rounded-3xl border p-8 sm:p-10 text-center space-y-5 ${
              isLight
                ? 'border-ls-grey-dark/30 bg-ls-white text-ls-navy'
                : 'border-ls-white/15 bg-ls-navy/80 text-ls-white'
            }`}
          >
            <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
              KEEP EXPLORING
            </span>
            <h2 className="text-2xl sm:text-3xl font-black tracking-tight font-display">
              Explore Related Thinking
            </h2>
            <div className="flex flex-wrap items-center justify-center gap-3 pt-1">
              <Link
                to="/insights"
                className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98]"
              >
                Explore Related Thinking
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
              <Link
                to="/ask"
                className={`inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all hover:bg-ls-red/10 ${
                  isLight
                    ? 'border-ls-red text-ls-navy hover:text-ls-red'
                    : 'border-ls-red/60 text-ls-white hover:text-ls-red'
                }`}
              >
                Ask LightSpeed
              </Link>
              <Link
                to="/solutions"
                className={`inline-flex items-center px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all hover:bg-ls-red/10 ${
                  isLight
                    ? 'border-ls-grey-dark/40 text-ls-navy hover:text-ls-red'
                    : 'border-ls-white/25 text-ls-white hover:text-ls-red'
                }`}
              >
                Explore Solutions
              </Link>
              <Link
                to="/sectors"
                className={`inline-flex items-center px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all hover:bg-ls-red/10 ${
                  isLight
                    ? 'border-ls-grey-dark/40 text-ls-navy hover:text-ls-red'
                    : 'border-ls-white/25 text-ls-white hover:text-ls-red'
                }`}
              >
                Explore Sectors
              </Link>
              <Link
                to="/contact"
                className={`inline-flex items-center px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all hover:bg-ls-red/10 ${
                  isLight
                    ? 'border-ls-grey-dark/40 text-ls-navy hover:text-ls-red'
                    : 'border-ls-white/25 text-ls-white hover:text-ls-red'
                }`}
              >
                Contact
              </Link>
            </div>
          </div>
        </Reveal>
      </section>

      <NewsletterSignup theme={theme} id="newsletter" />

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/insights', label: 'All Insights' },
          { to: '/proof', label: 'Proof' },
          { to: '/solutions', label: 'Solutions' },
          { to: '/sectors', label: 'Sectors' },
          { to: '/ask', label: 'Ask LightSpeed' },
        ]}
      />
    </>
  );
};

export default InsightArticlePage;
