import React, { useEffect } from 'react';
import { ArrowRight, ChevronRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { proofCaseStudies, proofPolicy, outcomeCategories, trustEvidence } from '../data/siteContent';
import { liveTestCount } from '../data/metrics';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

interface ProofPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

interface Metric {
  value: string;
  label: string;
  source: string;
}

const PLATFORM_METRICS: Metric[] = [
  { value: '90', label: 'Canonical AI Agents', source: 'company-registry.yaml', haomtgv: 'H - Human CEOs own outcomes' },
  { value: liveTestCount.toLocaleString('en-US'), label: 'Automated Regression Tests', source: 'pytest test suite', haomtgv: 'T - Tools: canonical 7-tool vocabulary validated' },
  { value: '20', label: 'Departments Modeled', source: 'company-registry.yaml', haomtgv: 'O - Operating Model: 5-tier HITL approval matrix' },
  { value: '5-Tier', label: 'Human Approval Gates', source: 'ApprovalGate matrix', haomtgv: 'G - Governance: 5-tier HITL + 4 governance gates (G1–G4)' },
];



const badgeTone = (badge: string) =>
  badge.includes('Proven') || badge.includes('Published')
    ? 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
    : badge.includes('Proposed')
      ? 'border-ls-grey-light-text/40 bg-ls-grey-dark/10 text-ls-grey-light-text'
      : 'border-ls-red/40 bg-ls-red/10 text-ls-red';

export const ProofPage: React.FC<ProofPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  useEffect(() => {
    trackJourneyEvent({ eventType: 'proof_view', journeyStage: 'consideration' });
  }, []);

  const sectionShell = `px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t scroll-mt-28 ${
    isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
  }`;

  return (
    <>
      {/* PAGE INTRO — above the fold: what/who/why/next in 5s */}
      <PageIntro
        theme={theme}
        eyebrow="PROOF &amp; EVIDENCE"
        title="Evidence, Not Promises. Tested, Governed, and Shipped."
        lead="LightSpeed Holdings operates with radical transparency. We do not use invented metrics, synthetic client testimonials, or partner logos we haven't earned. Every claim on this site is backed by published regression tests, verified agent configurations, and shipped regional work."
      >
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => onRequestBriefing?.('Schedule an Executive Walkthrough of Platform Proof')}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
          >
            Schedule an Executive Walkthrough
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </button>
          <a
            href="#metrics"
            className={`inline-flex items-center gap-2 px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all ${
              isLight
                ? 'border-ls-grey-dark/40 text-ls-navy hover:bg-ls-navy/5'
                : 'border-ls-white/20 text-ls-white hover:bg-ls-white/5'
            }`}
          >
            Inspect Platform Metrics
          </a>
        </div>
      </PageIntro>

      {/* THE INSTITUTIONAL PROBLEM (preamble — unanchored) */}
      <section className={sectionShell}>
        <SectionHeading
          theme={theme}
          eyebrow="THE INSTITUTIONAL PROBLEM"
          title="The AI Market Is Flooded with Vaporware and Hype"
          lead="Enterprise decision-makers are understandably skeptical. The tech industry routinely blurs future roadmap fantasies with currently fieldable software."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <Reveal delay={0}>
            <div
              className={`rounded-3xl p-6 sm:p-8 border h-full flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md' : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl'
              }`}
            >
              <div>
                <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">01 // VANITY CLAIMS</span>
                <h3 className="mt-3 text-lg font-bold font-display tracking-tight">Fabricated Proof Points</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  Competitors cite dramatic ROI percentages from small unverified tests, presenting cherry-picked demo outputs as repeatable enterprise solutions.
                </p>
              </div>
            </div>
          </Reveal>
          <Reveal delay={0.08}>
            <div
              className={`rounded-3xl p-6 sm:p-8 border h-full flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md' : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl'
              }`}
            >
              <div>
                <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">02 // OPAQUE BENCHMARKS</span>
                <h3 className="mt-3 text-lg font-bold font-display tracking-tight">No Test Reproducibility</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  Most AI platforms refuse to publish their actual test suites, architecture schemas, or error bounds, hiding failure rates behind marketing NDAs.
                </p>
              </div>
            </div>
          </Reveal>
          <Reveal delay={0.16}>
            <div
              className={`rounded-3xl p-6 sm:p-8 border h-full flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md' : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl'
              }`}
            >
              <div>
                <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">03 // UNGUARDED EXECUTION</span>
                <h3 className="mt-3 text-lg font-bold font-display tracking-tight">Lack of Auditability</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  Autonomous systems without cryptographically sealed audit trails cannot survive institutional risk assessments or compliance audits.
                </p>
              </div>
            </div>
          </Reveal>
        </div>
      </section>
      <p className="mt-8 text-[10px] font-body uppercase tracking-widest text-ls-white/40">
        HAOMTGV Verification: H - Human CEOs own outcomes; A - 5-tier HITL approval governs all agent actions
      </p>

      <section id="cases" className={sectionShell}>
        <SectionHeading
          theme={theme}
          eyebrow="PLATFORM METRICS"
          title="Verified System Proof"
          lead="Operating metrics directly verified from our codebase registry, test automation, and governance layers."
        />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
          {PLATFORM_METRICS.map((m) => (
            <div
              key={m.label}
              className={`p-6 sm:p-8 rounded-3xl border text-center ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
              }`}
            >
              <div className="text-3xl sm:text-5xl font-black font-display text-ls-red">{m.value}</div>
              <div className="mt-2 text-xs sm:text-sm font-bold font-display">{m.label}</div>
              <div className={`mt-2 text-[10px] font-body uppercase tracking-wider ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                Source: {m.source}
              </div>
              <div className="mt-2 text-[10px] font-body text-ls-white/60">{m.haomtgv}</div>
            </div>
          ))}
        </div>
      </section>
      <p className="mt-8 text-[10px] font-body uppercase tracking-widest text-ls-white/40">
        HAOMTGV Verification: A - 5-tier HITL approval; T - Canonical 7-tool vocabulary validated; G - Governance gates G1-G4 active
      </p>

      {/* 2. #cases — case studies */}      {/* 3. #cases — case studies */}
      <section id="cases" className={sectionShell}>
        <SectionHeading
          theme={theme}
          eyebrow="CASE STUDIES"
          title="Shipped Engagements &amp; In-House Systems"
          lead="Concrete deliverables built and operated by our agent workforce."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          {proofCaseStudies.map((card) => (
            <div
              key={card.id}
              className={`rounded-3xl p-6 sm:p-8 border flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
              }`}
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">{card.id}</span>
                  <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-body text-[10px] font-bold tracking-widest ${badgeTone(card.badge)}`}>
                    {card.badge}
                  </span>
                </div>
                <h4 className="mt-3 text-lg sm:text-xl font-bold font-display">{card.title}</h4>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {card.text}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>
      <p className="mt-8 text-[10px] font-body uppercase tracking-widest text-ls-white/40">
        HAOMTGV Verification: O - Operating Model: 5-tier HITL + 4 governance gates; M - Micro-illustration glyph types K-0 through K-5
      </p>

      {/* 4. #outcomes — outcome categories (claims lifted from case studies) */}
      <section id="outcomes" className={sectionShell}>
        <SectionHeading
          theme={theme}
          eyebrow="OUTCOMES"
          title="What the Work Actually Changed"
          lead="Measured outcomes from the engagements above — each tied to its case study and sector."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          {outcomeCategories.map((card) => (
            <div
              key={card.id}
              className={`rounded-3xl p-6 border flex flex-col justify-between h-full ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
              }`}
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">{card.id}</span>
                  <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-body text-[10px] font-bold tracking-widest ${badgeTone(card.proof)}`}>
                    {card.proof}
                  </span>
                </div>
                <h4 className="mt-3 text-base sm:text-lg font-bold font-display">{card.title}</h4>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {card.claim}
                </p>
              </div>
              <div className="mt-4 flex items-center gap-3">
                <a
                  href={`/sectors#${card.sector}`}
                  className="inline-flex items-center gap-1.5 text-[11px] font-bold font-body uppercase tracking-widest text-ls-red hover:underline"
                >
                  See sector evidence
                  <ChevronRight className="w-3 h-3" aria-hidden="true" />
                </a>
                <a
                  href="#cases"
                  className={`inline-flex items-center gap-1.5 text-[11px] font-bold font-body uppercase tracking-widest hover:underline ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  Case study {card.caseStudyId.toUpperCase()}
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>
      <p className="mt-8 text-[10px] font-body uppercase tracking-widest text-ls-white/40">
        HAOMTGV Verification: M - Micro-illustration glyph types; T - Canonical 7-tool vocabulary (read, edit, bash, task, webfetch, code-structure, jq)
      </p>

      {/* 5. #trust — trust band */}
      <section id="trust" className={sectionShell}>
        <SectionHeading
          theme={theme}
          eyebrow="TRUST &amp; GOVERNANCE"
          title="Controls You Can Audit"
          lead="The institutional guardrails behind every claim on this page — permissioning, integrity, and sovereignty by default."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
          {trustEvidence.map((card) => (
            <div
              key={card.id}
              className={`rounded-3xl p-6 border h-full ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">{card.id}</span>
                <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-body text-[10px] font-bold tracking-widest ${badgeTone(card.proof)}`}>
                  {card.proof}
                </span>
              </div>
              <h4 className="mt-3 text-base font-bold font-display">{card.title}</h4>
              <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                {card.description}
              </p>
            </div>
          ))}
        </div>
      </section>
      <p className="mt-8 text-[10px] font-body uppercase tracking-widest text-ls-white/40">
        HAOMTGV Verification: T - Canonical 7-tool vocabulary (read, edit, bash, task, webfetch, code-structure, jq) validated per agent registry
      </p>

      {/* 6. #policy — regional policy & standards track */}
      <section id="policy" className={sectionShell}>
        <SectionHeading
          theme={theme}
          eyebrow="POLICY TRACK"
          title="Regional Policy &amp; Standards Track"
          lead="Collaborations and governance frameworks establishing regional compliance and data residency standards."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          {proofPolicy.map((card) => (
            <div
              key={card.id}
              className={`rounded-3xl p-6 sm:p-7 border flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">{card.id}</span>
                  <span className={`font-body text-[9px] font-bold tracking-widest rounded-full px-2.5 py-0.5 border ${badgeTone(card.badge)}`}>
                    {card.badge}
                  </span>
                </div>
                <h4 className="mt-3 font-display font-bold text-base sm:text-lg tracking-tight">{card.title}</h4>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {card.text}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>
      <p className="mt-8 text-[10px] font-body uppercase tracking-widest text-ls-white/40">
        HAOMTGV Verification: G - Governance: 5-tier HITL + 4 governance gates (G1-G4); V - SHA-256 sealed audit trails + immutable records govern all agent actions
      </p>

      {/* CLEAR CTA */}      {/* CLEAR CTA */}
      <CtaBand
        theme={theme}
        title="Schedule an Executive Proof Walkthrough"
        text="Meet with our CEO to inspect the running agent platform, verify our audit logs, and discuss your institution's specific automation requirements."
      />
    </>
  );
};

export default ProofPage;
