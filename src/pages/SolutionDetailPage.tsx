import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { Check, ArrowLeft, ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { solutions } from '../data/siteContent';

interface SolutionDetailPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /solutions/:slug — shared renderer for the five detailed solution domains,
 * resolved from the slug against the site content model.
 */
export const SolutionDetailPage: React.FC<SolutionDetailPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const { slug } = useParams<{ slug: string }>();
  const record = solutions.find((s) => s.slug === slug);

  if (!record) {
    return (
      <PageIntro
        theme={theme}
        eyebrow="NOT FOUND"
        title="That solution doesn't exist here"
        lead="The solution you followed may have moved."
      >
        <Link
          to="/solutions"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all hover:brightness-110"
        >
          <ArrowLeft className="w-3.5 h-3.5" aria-hidden="true" />
          Back to Solutions
        </Link>
      </PageIntro>
    );
  }

  const base = '/solutions';
  const others = solutions.filter((s) => s.slug !== record.slug);

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow={record.eyebrow}
        title={record.title}
      >
        <div className="mt-4 space-y-3 max-w-2xl">
          <HonestyBadge label={record.proof} />
          <p className={`text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            {record.lead}
          </p>
        </div>
      </PageIntro>

      {/* Capabilities */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="CAPABILITIES"
          title="What This Solution Delivers"
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {record.capabilities.map((cap, idx) => (
            <Reveal key={cap.title} delay={idx * 0.06}>
              <div className={`rounded-3xl p-6 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <h3 className="font-display font-bold text-sm sm:text-base tracking-tight">{cap.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {cap.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Use cases */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="USE CASES"
          title="Where It Lands"
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {record.useCases.map((uc, idx) => (
            <Reveal key={uc.title} delay={idx * 0.06}>
              <div className={`relative rounded-3xl p-6 sm:p-7 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <h3 className="font-display font-bold text-base sm:text-lg tracking-tight">{uc.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {uc.lead}
                </p>
                <div className={`pt-4 mt-4 border-t ${isLight ? 'border-slate-200' : 'border-white/10'}`}>
                  <HonestyBadge label={uc.proof} />
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Keep exploring */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20`}>
        <div className={`rounded-3xl p-6 sm:p-8 border ${
          isLight ? 'bg-white/95 border-slate-300 shadow-md' : 'bg-zinc-950/80 border-white/15 shadow-xl'
        }`}>
          <div className="flex flex-col lg:flex-row lg:items-center gap-6">
            <div className="lg:flex-1">
              <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">KEEP EXPLORING</span>
              <h2 className={`mt-2 text-xl sm:text-2xl font-black tracking-tight font-display ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                Other Solutions
              </h2>
            </div>
            <div className="flex flex-wrap gap-2.5">
              {others.map((sol) => (
                <Link
                  key={sol.slug}
                  to={`${base}/${sol.slug}`}
                  className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-full border font-bold text-[11px] tracking-wider transition-colors cursor-pointer ${
                    isLight
                      ? 'border-slate-300 text-slate-700 hover:border-ls-red hover:text-ls-red'
                      : 'border-white/15 text-zinc-200 hover:border-ls-red hover:text-ls-red'
                  }`}
                >
                  {sol.nav}
                  <ArrowRight className="w-3 h-3" aria-hidden="true" />
                </Link>
              ))}
              <Link
                to={base}
                className={`inline-flex items-center gap-2 px-4 py-2 rounded-full font-bold text-[11px] tracking-wider transition-all cursor-pointer bg-ls-red/10 text-ls-red border border-ls-red/30 ${
                  isLight ? '' : ''
                }`}
              >
                <Check className="w-3 h-3" aria-hidden="true" />
                Solutions Overview
              </Link>
            </div>
          </div>
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Have a Challenge in Mind?"
        text={`Tell us where ${record.title.toLowerCase()} could move your organisation forward. We will be honest about whether we can help — and exactly what it takes to start.`}
        ctaLabel={record.cta.label}
        ctaTo={record.cta.to}
      />
    </>
  );
};

export default SolutionDetailPage;
