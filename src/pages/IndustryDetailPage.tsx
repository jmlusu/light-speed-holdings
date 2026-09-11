import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { industries } from '../data/siteContent';

interface IndustryDetailPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /industries/:slug — shared renderer for the five industry verticals,
 * resolved from the slug against the site content model.
 */
export const IndustryDetailPage: React.FC<IndustryDetailPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const { slug } = useParams<{ slug: string }>();
  const record = industries.find((i) => i.slug === slug);

  if (!record) {
    return (
      <PageIntro
        theme={theme}
        eyebrow="NOT FOUND"
        title="That industry page doesn't exist here"
        lead="The page you followed may have moved."
      >
        <Link
          to="/industries"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all hover:brightness-110"
        >
          <ArrowLeft className="w-3.5 h-3.5" aria-hidden="true" />
          Back to Industries
        </Link>
      </PageIntro>
    );
  }

  const others = industries.filter((i) => i.slug !== record.slug);

  const blocks: { eyebrow: string; title: string; body: string }[] = [
    { eyebrow: 'THE PROBLEM', title: 'What Holds the Industry Back', body: record.problem },
    { eyebrow: 'THE OPPORTUNITY', title: 'Where Agentic AI Moves the Needle', body: record.opportunity },
    { eyebrow: 'OUR APPROACH', title: 'How We Deliver', body: record.solution },
  ];

  return (
    <>
      <PageIntro theme={theme} eyebrow="INDUSTRY" title={record.title}>
        <div className="mt-4">
          <HonestyBadge label={record.proof} />
        </div>
      </PageIntro>

      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {blocks.map((block, idx) => (
            <Reveal key={block.eyebrow} delay={idx * 0.08}>
              <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">
                  {block.eyebrow}
                </span>
                <h2 className="mt-3 font-display font-bold text-lg tracking-tight">{block.title}</h2>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {block.body}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="USE CASES"
          title="Where It Lands in this Industry"
        />
        <div className="max-w-3xl mx-auto">
          <div className={`rounded-3xl p-6 sm:p-8 border ${
            isLight ? 'bg-white/95 border-slate-300 shadow-md' : 'bg-zinc-950/80 border-white/15 shadow-xl'
          }`}>
            <ul className={`space-y-3 text-sm leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              {record.useCases.map((uc, idx) => (
                <li key={uc} className="flex items-start gap-3">
                  <span className="mt-0.5 shrink-0 w-5 h-5 rounded-full bg-ls-red/10 text-ls-red flex items-center justify-center font-mono text-[10px] font-black" aria-hidden="true">
                    {String(idx + 1).padStart(2, '0')}
                  </span>
                  <span>{uc}</span>
                </li>
              ))}
            </ul>
            {record.note && (
              <p className={`mt-6 pt-5 border-t text-xs leading-relaxed ${
                isLight ? 'border-slate-200 text-slate-500' : 'border-white/10 text-zinc-500'
              }`}>
                <span className="font-mono font-bold tracking-widest text-ls-red">HONESTY NOTE: </span>
                {record.note}
              </p>
            )}
          </div>
        </div>
      </section>

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
                Other Industries
              </h2>
            </div>
            <div className="flex flex-wrap gap-2.5">
              {others.map((ind) => (
                <Link
                  key={ind.slug}
                  to={`/industries/${ind.slug}`}
                  className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-full border font-bold text-[11px] tracking-wider transition-colors cursor-pointer ${
                    isLight
                      ? 'border-slate-300 text-slate-700 hover:border-ls-red hover:text-ls-red'
                      : 'border-white/15 text-zinc-200 hover:border-ls-red hover:text-ls-red'
                  }`}
                >
                  {ind.nav}
                  <ArrowRight className="w-3 h-3" aria-hidden="true" />
                </Link>
              ))}
              <Link
                to="/industries"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full font-bold text-[11px] tracking-wider transition-all cursor-pointer bg-ls-red/10 text-ls-red border border-ls-red/30"
              >
                Industries Overview
              </Link>
            </div>
          </div>
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Working in this Industry?"
        text="Tell us the problem you are facing today. We lead with your constraint, not our tooling — and we will be honest about whether agentic AI is the right answer."
      />
    </>
  );
};

export default IndustryDetailPage;
