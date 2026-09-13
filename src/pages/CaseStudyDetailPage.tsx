import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Check, ShieldCheck, Wrench } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { externalBuildCaseStudy } from '../data/siteContent';

interface CaseStudyDetailPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /work/:slug — full case-study page for external client builds. Renders the
 * honest, evidence-traceable engagement record from the site content model:
 * baseline, delivered modules, measurable outcome, delivery approach, and
 * boundary/honesty notes.
 */
export const CaseStudyDetailPage: React.FC<CaseStudyDetailPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const cardCls = isLight
    ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md'
    : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl';

  return (
    <>
      <PageIntro theme={theme} eyebrow={externalBuildCaseStudy.eyebrow} title={externalBuildCaseStudy.title}>
        <div className="mt-4 space-y-3 max-w-2xl mx-auto">
          <HonestyBadge label={externalBuildCaseStudy.honesty} />
          <p className={`text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            {externalBuildCaseStudy.lead}
          </p>
          <div>
            <Link
              to="/work"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all hover:brightness-110"
            >
              <ArrowLeft className="w-3.5 h-3.5" aria-hidden="true" />
              Back to Work
            </Link>
          </div>
        </div>
      </PageIntro>

      {/* Baseline */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading theme={theme} eyebrow="THE BASELINE" title="Where the Client Started" />
        <div className={`rounded-3xl p-6 sm:p-8 border ${cardCls}`}>
          <ul className="space-y-3 list-none">
            {externalBuildCaseStudy.baseline.map((item) => (
              <li key={item} className="flex gap-3 text-sm leading-relaxed">
                <Check className={`w-4 h-4 mt-0.5 shrink-0 ${isLight ? 'text-ls-red' : 'text-ls-red'}`} aria-hidden="true" />
                <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Delivered */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20`}>
        <SectionHeading
          theme={theme}
          eyebrow="WHAT WE DELIVERED"
          title="The Full Application Layer"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {externalBuildCaseStudy.delivered.map((item, idx) => (
            <Reveal key={item.title} delay={(idx % 3) * 0.06}>
              <div className={`rounded-3xl p-6 border h-full ${cardCls}`}>
                <div className="flex items-start justify-between gap-3">
                  <span className="font-mono text-[10px] font-black tracking-widest text-ls-red">
                    {String(idx + 1).padStart(2, '0')}
                  </span>
                </div>
                <h3 className="mt-3 font-display font-bold text-base sm:text-lg tracking-tight">{item.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                  {item.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Measurable outcome */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20`}>
        <SectionHeading
          theme={theme}
          eyebrow="MEASURABLE OUTCOME"
          title="Verified by the Client\u2019s Own Gates"
        />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
          {externalBuildCaseStudy.outcomes.map((m, idx) => (
            <Reveal key={m.label} delay={idx * 0.06}>
              <div className={`rounded-3xl p-6 text-center border h-full ${cardCls}`}>
                <div className="font-display font-black text-2xl sm:text-3xl tracking-tight text-ls-red">{m.value}</div>
                <p className={`mt-2 text-[11px] sm:text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                  {m.label}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
        <p className={`mt-4 text-xs sm:text-sm leading-relaxed max-w-3xl ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          The full baseline and acceptance record lives in the client repository; this engagement also shipped an opt-in
          chaos suite (11/11 resilience cases) and a security audit of 175 files with zero credential leaks.
        </p>
      </section>

      {/* How we delivered */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="HOW WE DELIVERED"
          title="An Agent Team, a Fixed Contract"
        />
        <div className={`rounded-3xl p-6 sm:p-8 border ${cardCls}`}>
          <ul className="space-y-4 list-none">
            {externalBuildCaseStudy.delivery.map((item) => (
              <li key={item} className="flex gap-3 text-sm leading-relaxed">
                <Wrench className={`w-4 h-4 mt-0.5 shrink-0 text-ls-red`} aria-hidden="true" />
                <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Honesty & boundaries */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20`}>
        <SectionHeading
          theme={theme}
          eyebrow="HONESTY & BOUNDARIES"
          title="What This Case Study Does Not Claim"
        />
        <div className={`rounded-3xl p-6 sm:p-8 border border-ls-red/30 ${cardCls}`}>
          <ul className="space-y-3 list-none">
            {externalBuildCaseStudy.notes.map((item) => (
              <li key={item} className="flex gap-3 text-sm leading-relaxed">
                <ShieldCheck className={`w-4 h-4 mt-0.5 shrink-0 text-ls-red`} aria-hidden="true" />
                <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Could Shape Your Deliverable"
        text="We deliver engineered AI systems on a fixed contract, with honest status at every gate. Tell us where you need to start."
        ctaLabel={externalBuildCaseStudy.cta.label}
        ctaTo={externalBuildCaseStudy.cta.to}
      />
    </>
  );
};

export default CaseStudyDetailPage;
