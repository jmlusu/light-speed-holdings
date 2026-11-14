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

  // SEO meta tags for the current article page.
  useEffect(() => {
    if (!article) return;

    document.title = `${article.title} | LightSpeed Holdings`;

    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.setAttribute('content', article.seo?.description || '');
    }

    const ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle) {
      ogTitle.setAttribute(
        'content',
        article.seo?.title || `${article.title} | LightSpeed Holdings`,
      );
    }

    const ogDescription = document.querySelector('meta[property="og:description"]');
    if (ogDescription) {
      ogDescription.setAttribute('content', article.seo?.description || '');
    }

    const ogImage = document.querySelector('meta[property="og:image"]');
    if (ogImage) {
      ogImage.setAttribute('content', '/og-default.png');
    }

    const twitterCard = document.querySelector('meta[name="twitter:card"]');
    if (twitterCard) {
      twitterCard.setAttribute('content', 'summary_large_image');
    }

    const twitterTitle = document.querySelector('meta[name="twitter:title"]');
    if (twitterTitle) {
      twitterTitle.setAttribute(
        'content',
        article.seo?.title || `${article.title} | LightSpeed Holdings`,
      );
    }

    const twitterDescription = document.querySelector('meta[name="twitter:description"]');
    if (twitterDescription) {
      twitterDescription.setAttribute('content', article.seo?.description || '');
    }
  }, [article]);

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
  const bodyText = isLight ? 'text-slate-800' : 'text-slate-100';
  const headingText = isLight ? 'text-ls-navy' : 'text-white';
  const cardShell = `rounded-3xl p-6 h-full flex flex-col gap-2 transition-all scroll-mt-28 ${
    isLight
      ? 'bg-ls-white shadow-sm hover:shadow-md'
      : 'bg-ls-navy/80 shadow-xl hover:shadow-2xl'
  }`;
  const related = solutions.filter((s) => article.relatedSolutions.includes(s.slug));
  const relatedSectors = sectors.filter((s) => article.relatedSectors.includes(s.id));

  const renderBlock = (block: InsightBlock, i: number): React.ReactNode => {
    switch (block.kind) {
      case 'h':
        return (
          <h2
            key={i}
            className={`pt-6 pb-1 text-xl sm:text-2xl font-black tracking-tight font-display ${headingText}`}
          >
            {block.text}
          </h2>
        );
      case 'p':
        return (
          <p key={i} className={`text-base sm:text-lg leading-relaxed ${bodyText}`}>
            {block.text}
          </p>
        );
      case 'ul':
        return (
          <ul key={i} className={`list-disc pl-5 space-y-3 text-base sm:text-lg leading-relaxed ${bodyText}`}>
            {block.items.map((item, j) => (
              <li key={j}>{item}</li>
            ))}
          </ul>
        );
      case 'quote':
        return (
          <blockquote
            key={i}
            className={`my-6 px-6 py-5 rounded-2xl italic text-base sm:text-lg leading-relaxed border-l-4 border-ls-red ${
              isLight
                ? 'bg-red-50/70 text-ls-navy'
                : 'bg-red-950/30 text-white'
            }`}
          >
            <p>{block.text}</p>
            {block.cite && (
              <cite className={`mt-3 block not-italic text-xs font-bold tracking-wider uppercase ${
                isLight ? 'text-slate-600' : 'text-slate-300'
              }`}>
                – {block.cite}
              </cite>
            )}
          </blockquote>
        );
      default:
        return null;
    }
  };

  const [readingProgress, setReadingProgress] = React.useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        const currentProgress = (window.scrollY / totalHeight) * 100;
        setReadingProgress(Math.min(100, Math.max(0, currentProgress)));
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Contextual article hero image mapping based on slug
  let articleHeroImage = '/assets/images/pharos_editorial_hero_1793817662034.avif';
  if (article.slug === 'open-source-cost-architecture' || article.slug === 'dual-economy-ai-pricing') {
    articleHeroImage = '/assets/images/pharos_article_thumb_cost_1793817753722.avif';
  } else if (article.slug === 'five-tier-approval-matrix' || article.slug === 'evidence-ladder-honest-claims') {
    articleHeroImage = '/assets/images/pharos_article_thumb_gov_1793817768084.avif';
  } else if (article.slug === 'sadc-ai-opportunity' || article.slug === 'agentic-ai-african-governments') {
    articleHeroImage = '/assets/images/pharos_article_thumb_sadc_1793817783127.avif';
  } else if (article.slug === 'inside-a-90-agent-company') {
    articleHeroImage = '/assets/images/agent_network_topology_1793816821318.avif';
  }

  return (
    <>
      {/* Restrained Reading Progress Indicator */}
      <div className="fixed top-0 left-0 right-0 h-1 z-50 bg-transparent pointer-events-none">
        <div
          className="h-full bg-ls-cyan transition-all duration-150 ease-out"
          style={{ width: `${readingProgress}%` }}
          aria-hidden="true"
        />
      </div>

      <PageIntro theme={theme} eyebrow={`INSIGHTS // ${article.topic}`} title={article.title} lead={article.dek}>
        <div className="flex flex-wrap gap-2 mt-4">
          <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wider ${
            isLight ? 'bg-cyan-500/10 text-cyan-600 border border-cyan-500/20' : 'bg-cyan-950/50 text-cyan-400 border border-cyan-800'
          }`}>
            {article.topic}
          </span>
        </div>
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
          className={`mt-4 max-w-2xl rounded-2xl px-4 py-3 font-body text-[11px] leading-relaxed ${
            isLight
              ? 'bg-ls-white text-ls-grey-dark shadow-sm'
              : 'bg-ls-navy/80 text-ls-grey-light-text shadow-md'
          }`}
        >
          <span className="font-bold tracking-widest text-ls-red">SOURCES </span>
          {article.source}
        </div>
      </PageIntro>

      {/* Featured Editorial Article Hero Visual */}
      <section className="px-6 lg:px-12 max-w-4xl mx-auto w-full pt-6">
        <div className="relative w-full aspect-[21/9] sm:aspect-[16/7] rounded-3xl overflow-hidden border border-white/10 shadow-xl bg-slate-950">
          <img
            src={articleHeroImage}
            alt={`${article.title} architectural illustration`}
            className="w-full h-full object-cover filter saturate-110"
            loading="eager"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent flex items-end p-6">
            <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-300 uppercase px-3 py-1 rounded-full bg-black/70 backdrop-blur-sm border border-cyan-500/30">
              Pharos Canon // Grounded Research
            </span>
          </div>
        </div>
      </section>

      {/* Operating Model Context Callout */}
      <section aria-label="Operating Model Context" className="px-6 lg:px-12 max-w-4xl mx-auto w-full pt-8">
        <div
          role="region"
          className={`longform-contrast-layer rounded-3xl p-6 sm:p-8 font-body text-xs sm:text-sm leading-relaxed transition-all ${
            isLight
              ? 'bg-cyan-50/85 border border-cyan-200/80 text-ls-navy'
              : 'bg-cyan-950/40 border border-cyan-500/25 text-slate-100'
          }`}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
            <span className="font-bold tracking-widest text-xs uppercase font-mono text-cyan-700 dark:text-cyan-300">
              OPERATING MODEL CONTEXT // ARCHITECTURAL DISTINCTION
            </span>
          </div>
          <p className="font-bold text-base sm:text-lg mb-2 font-display text-ls-navy dark:text-white">
            LightSpeed Internal Reference Fleet vs. Client Implementations
          </p>
          <p className={isLight ? 'text-slate-700' : 'text-slate-200'}>
            The <strong>89 AI agents + 1 Human CEO</strong> operating model documented across Pharos research is LightSpeed Holdings&apos; internal reference architecture and stress-tested production benchmark. For enterprise, institutional, and SME client engagements, LightSpeed designs and deploys <strong>configurable AI agent teams scaling from 1 to N+ agents</strong> according to specific business requirements, complexity, and workload. Clients are never required to adopt an 89+1 or fixed-size workforce; sovereign human decision authority and multi-tier approval governance remain strictly enforced regardless of team scale.
          </p>
        </div>
      </section>

      {/* Dated correction note (honesty policy: body text stays unchanged) */}
      {article.correction && (
        <section aria-label="Correction" className="px-6 lg:px-12 max-w-4xl mx-auto w-full pt-6">
          <div
            role="note"
            className={`longform-contrast-layer rounded-2xl px-6 py-4 font-body text-xs sm:text-sm leading-relaxed ${
              isLight
                ? 'bg-red-50/80 text-slate-800 border-red-200'
                : 'bg-red-950/40 text-slate-100 border-red-500/30'
            }`}
          >
            <span className="font-bold tracking-widest text-ls-red">CORRECTION </span>
            {article.correction.text}
          </div>
        </section>
      )}

      {/* Article body with subtle high-contrast background layer */}
      <section className="px-6 lg:px-12 max-w-4xl mx-auto w-full pt-6 pb-6">
        <article className="longform-contrast-layer rounded-3xl p-6 sm:p-10 lg:p-12 space-y-6">
          {article.blocks.map(renderBlock)}
        </article>
      </section>

      {/* §16 related concepts: solutions + sectors */}
      <section aria-label="Related thinking" className="px-6 lg:px-12 max-w-7xl mx-auto w-full pt-12 pb-2">
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
                  <div className={cardShell}>
                    <div className="flex items-start justify-between gap-3">
                      <h3 className={`text-base font-black font-display ${headingText}`}>{sec.title}</h3>
                      <HonestyBadge label={sec.status} className="shrink-0" />
                    </div>
                    <p className={`text-sm leading-relaxed ${bodyText}`}>{sec.description}</p>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* §16 related-thinking CTAs: primary "Explore Related Thinking" + secondary actions */}
      <section aria-label="Related thinking" className="px-6 lg:px-12 max-w-7xl mx-auto w-full pt-12 pb-4">
        <Reveal>
          <div
            className={`rounded-3xl p-8 sm:p-10 text-center space-y-5 ${
              isLight
                ? 'bg-ls-white text-ls-navy shadow-sm'
                : 'bg-ls-navy/80 text-ls-white shadow-xl'
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
                className="btn-milled btn-milled-primary inline-flex items-center gap-2 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all hover:bg-ls-red/90"
              >
                Explore Related Thinking
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
              <Link
                to="/contact"
                className={`btn-milled btn-milled-secondary inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all ${
                  isLight
                    ? 'bg-ls-red/10 text-ls-navy hover:bg-ls-red/20 hover:text-ls-red'
                    : 'bg-ls-red/20 text-ls-white hover:bg-ls-red/30 hover:text-ls-red'
                }`}
              >
                Contact Us
              </Link>
              <Link
                to="/solutions"
                className={`btn-milled btn-milled-secondary inline-flex items-center px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all ${
                  isLight
                    ? 'bg-ls-grey-light text-ls-navy hover:text-ls-red hover:bg-ls-grey-light/80'
                    : 'bg-white/10 text-ls-white hover:text-ls-red hover:bg-white/15'
                }`}
              >
                Explore Solutions
              </Link>
              <Link
                to="/haomtgv"
                className={`btn-milled btn-milled-secondary inline-flex items-center px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all ${
                  isLight
                    ? 'bg-ls-grey-light text-ls-navy hover:text-ls-red hover:bg-ls-grey-light/80'
                    : 'bg-white/10 text-ls-white hover:text-ls-red hover:bg-white/15'
                }`}
              >
                HAOMTGV Architecture
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
          { to: '/solutions', label: 'Solutions' },
          { to: '/contact', label: 'Contact Us' },
        ]}
      />
    </>
  );
};

export default InsightArticlePage;
