import React from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { workCaseStudies, workPolicy } from '../data/siteContent';

interface WorkPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /work — proof and policy. Case studies carry their evidence status inline
 * (Proven in-house vs. In pilot). The policy track lists the regional work
 * that makes the governance pattern real outside our own walls.
 */
export const WorkPage: React.FC<WorkPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="PROOF // WORK"
        title="The Work That Makes Us Believable"
        lead="We prove, not promise. These are the reviewed, named engagements and policy artifacts that back every claim on this site — each carrying its own honesty status so you can tell exactly what has shipped from what is in flight."
      />

      {/* Case studies */}
      <section
        id="case-studies"
        aria-labelledby="case-studies-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="CASE STUDIES"
          title="Shipped Work"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {workCaseStudies.map((card, idx) => (
            <Reveal key={card.id} delay={(idx % 2) * 0.06}>
              <div className={`rounded-3xl p-6 sm:p-8 border h-full flex flex-col ${
                card.featured
                  ? (isLight ? 'relative overflow-hidden hardware-chassis-light text-ls-navy' : 'relative overflow-hidden hardware-chassis-dark text-ls-white')
                  : (isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl')
              }`}>
                {card.featured && (
                  <>
                    <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
                    <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
                    <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
                    <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
                  </>
                )}
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-black tracking-widest text-ls-red">{card.id}</span>
                </div>
                <h3 className="mt-3 font-display font-bold text-lg sm:text-xl tracking-tight">{card.title}</h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {card.text}
                </p>
                <div className={`pt-4 border-t mt-auto ${
                  isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
                }`}>
                  <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-body text-[9px] font-bold tracking-widest ${
                    card.badge.includes('Proven')
                      ? 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
                      : card.badge.includes('Pilot')
                        ? 'border-ls-red/40 bg-ls-red/10 text-ls-red'
                        : 'border-ls-red/40 bg-ls-red/10 text-ls-red/30'
                  }`}>
                    <span aria-hidden="true" className="w-1.5 h-1.5 rounded-full bg-current opacity-70" />
                    {card.badge}
                  </span>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Policy track */}
      <section
        id="policy"
        aria-labelledby="policy-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="POLICY TRACK"
          title="Shaping the Rules, Not Just Following Them"
          lead="The governance pattern we operate is proposed as regional standard — so the people writing the rules can see it running first."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {workPolicy.map((card, idx) => (
            <Reveal key={card.id} delay={(idx % 2) * 0.06}>
              <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
              }`}>
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-black tracking-widest text-ls-red">{card.id}</span>
                  <span className={`font-body text-[9px] font-bold tracking-widest rounded-full px-2.5 py-0.5 border ${
                    card.badge.includes('Published') || card.badge.includes('Proven')
                      ? 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
                      : card.badge.includes('Proposed')
                        ? 'border-ls-grey-light-text/40 bg-ls-grey-dark/10 text-ls-grey-light-text'
                        : 'border-ls-red/40 bg-ls-red/10 text-ls-red'
                  }`}>
                    {card.badge}
                  </span>
                </div>
                <h3 className="mt-3 font-display font-bold text-base sm:text-lg tracking-tight">{card.title}</h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {card.text}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="See Proof in a Way That Matters to You"
        text="We will show you live architecture, the tests that gate our work, and the engagement records behind our claims — no slide deck required."
      />
    </>
  );
};

export default WorkPage;
