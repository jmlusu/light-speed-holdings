import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Compass, FileText, ScrollText } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { Reveal } from '../components/Reveal';
import { CTAS } from '../data/ctas';
import { insightArticles } from '../data/insights';
import { pharosFormats, pharosMission, pharosPillars, pharosPrinciples, pharosWhy } from '../data/pharos';

interface PharosPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * Pharos department page.
 *
 * Content is sourced from docs/Pharos/README.md, docs/Pharos/positioning.md and
 * data/claims/registry.ts (CLM-020). This page publishes no metrics and no
 * client outcomes - it describes the programme, its three pillars, the formats
 * it publishes and the essays that already exist in src/data/insights.ts.
 */
export const PharosPage: React.FC<PharosPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const cardBase = isLight
    ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md'
    : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl';
  const muted = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';
  const sectionBase = `px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
    isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
  }`;

  return (
    <>
      {/* 1. WHAT PHAROS IS */}
      <PageIntro theme={theme} eyebrow="PHAROS" title="The Public Intellectual Programme" lead={pharosMission}>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <Link
            to="/insights"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all hover:bg-ls-red/90"
          >
            Read the Essays
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
          <Link
            to="/ai-company-builder"
            className={`inline-flex items-center gap-2 px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all ${
              isLight
                ? 'border-ls-grey-dark/40 text-ls-navy hover:bg-ls-navy/5'
                : 'border-ls-white/20 text-ls-white hover:bg-ls-white/5'
            }`}
          >
            See the System It Describes
          </Link>
        </div>
      </PageIntro>

      {/* 2. WHY THE NAME */}
      <section className={sectionBase}>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-start">
          <div>
            <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
              WHY THE NAME
            </span>
            <h2 className={`mt-3 text-2xl sm:text-4xl font-black tracking-tight font-display ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}>
              A Lighthouse, Not a Lectern
            </h2>
            <p className={`mt-4 text-sm sm:text-base leading-relaxed ${muted}`}>{pharosWhy}</p>
          </div>
          <Reveal delay={0.08}>
            <div className={`rounded-3xl p-6 sm:p-8 border ${cardBase}`}>
              <Compass className="w-6 h-6 text-ls-red mb-3" aria-hidden="true" />
              <h3 className="font-display font-bold text-lg">The Positioning Claim</h3>
              <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${muted}`}>
                The programme is a department of LightSpeed Holdings, not a marketing function.
                It converts engineering that already ships into citable public artefacts, and it
                is held to the same evidence rules as the product: claim a class, cite the source,
                correct in public when the source changes.
              </p>
              <Link
                to="/insights/evidence-ladder-honest-claims"
                className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold tracking-wider text-ls-red hover:underline"
              >
                How claims are classified
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 3. THE THREE PILLARS */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="THE PROGRAMME"
          title="Three Pillars, One Argument"
          lead="Company building, use cases and policy are the same question asked at three altitudes. The engineering answers the first, deployments answer the second, and governance answers the third."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {pharosPillars.map((pillar, idx) => (
            <Reveal key={pillar.id} delay={idx * 0.08}>
              <article className={`h-full rounded-3xl p-6 sm:p-8 border flex flex-col ${cardBase}`}>
                <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">
                  PILLAR {String(idx + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-3 text-xl font-bold font-display tracking-tight">{pillar.title}</h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed font-medium ${
                  isLight ? 'text-ls-navy' : 'text-ls-white'
                }`}>
                  {pillar.question}
                </p>
                <div className={`mt-5 pt-4 border-t ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`}>
                  <span className="font-body text-[9px] font-bold tracking-widest text-ls-cyan uppercase">
                    WHAT BACKS IT
                  </span>
                  <p className={`mt-1.5 text-xs leading-relaxed ${muted}`}>{pillar.proof}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 4. PUBLICATION FORMATS */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="FORMATS"
          title="Eight Formats, One Evidence Standard"
          lead="Every Pharos artefact is published in one of eight formats, so a reader knows before opening it whether they are reading a field observation, a research note or a policy position."
        />
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {pharosFormats.map((format) => (
            <div
              key={format}
              className={`rounded-2xl p-4 border text-center ${
                isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy/70 border-ls-white/10'
              }`}
            >
              <FileText className="w-4 h-4 text-ls-red mx-auto mb-2" aria-hidden="true" />
              <span className="font-body text-[10px] font-black tracking-widest">
                {format.replace(/_/g, ' ')}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* 5. PUBLISHED WORK */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="PUBLISHED WORK"
          title="What Has Actually Been Written"
          lead="These essays are live on this site today. Each one declares its first-party sources and carries a dated correction note where the underlying claim changed."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {insightArticles.map((article, idx) => (
            <Reveal key={article.slug} delay={Math.min(idx * 0.04, 0.32)}>
              <article className={`h-full rounded-3xl p-6 border flex flex-col justify-between ${cardBase}`}>
                <div>
                  <div className="flex items-center justify-between gap-3">
                    <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">
                      {article.topic}
                    </span>
                    <span className={`font-body text-[10px] font-bold ${muted}`}>
                      {article.readMins} MIN
                    </span>
                  </div>
                  <h3 className="mt-3 text-base font-bold font-display tracking-tight leading-snug">
                    {article.title}
                  </h3>
                  <p className={`mt-2 text-xs leading-relaxed ${muted}`}>{article.dek}</p>
                </div>
                <div className={`mt-5 pt-4 border-t ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'} flex items-center justify-between gap-3`}>
                  <span className={`font-body text-[10px] font-bold ${muted}`}>
                    {new Date(article.publishedAt).toLocaleDateString('en-GB', {
                      day: '2-digit',
                      month: 'short',
                      year: 'numeric',
                    })}
                  </span>
                  <Link
                    to={`/insights/${article.slug}`}
                    className="inline-flex items-center gap-1 text-xs font-bold tracking-wider text-ls-red hover:underline"
                  >
                    Read
                    <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
                  </Link>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 6. OPERATING PRINCIPLES */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="OPERATING PRINCIPLES"
          title="The Rules the Programme Runs On"
          lead="Five commitments, taken verbatim from the Pharos operating brief. They are constraints on what the programme is allowed to publish."
        />
        <ol className="max-w-3xl mx-auto space-y-4">
          {pharosPrinciples.map((principle, idx) => (
            <li key={principle} className={`flex items-start gap-4 rounded-2xl p-5 border ${cardBase}`}>
              <span
                aria-hidden="true"
                className="flex shrink-0 w-8 h-8 items-center justify-center rounded-full border border-ls-red/40 bg-ls-red/10 font-display font-black text-ls-red text-sm"
              >
                {idx + 1}
              </span>
              <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                {principle}
              </p>
            </li>
          ))}
        </ol>
      </section>

      {/* 7. HONEST STATUS */}
      <section className={sectionBase}>
        <Reveal>
          <div className={`rounded-3xl p-6 sm:p-8 border max-w-4xl mx-auto ${
            isLight ? 'bg-ls-white border-ls-grey-dark/30' : 'bg-ls-navy border-ls-white/15'
          }`}>
            <div className="flex items-center gap-2">
              <ScrollText className="w-5 h-5 text-ls-red" aria-hidden="true" />
              <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">
                HONEST STATUS
              </span>
            </div>
            <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${muted}`}>
              Pharos publishes what the company can evidence and labels the rest. The essays above
              describe systems running in-house at LightSpeed Holdings; they are not case studies of
              paying clients, and the site claims no revenue, win rate or delivered enterprise
              deployment. Where a claim changed, the correction is dated and the original body text
              is left in place so the record stays auditable.
            </p>
          </div>
        </Reveal>
      </section>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/insights', label: 'All Insights' },
          { to: '/ai-company-builder', label: 'AI Company Builder' },
          { to: '/about', label: 'About LightSpeed' },
        ]}
      />

      <CtaBand
        theme={theme}
        title={CTAS.primary.label}
        text="If you work in policy, procurement or institutional leadership and want the underlying evidence behind any Pharos claim, ask for it directly. We answer with sources, not slideware."
        ctaLabel={CTAS.primary.label}
        ctaTo={CTAS.primary.to}
        onRequestBriefing={onRequestBriefing}
      />
    </>
  );
};

export default PharosPage;
