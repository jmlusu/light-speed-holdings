import React from 'react';
import { ArrowRight, CheckCircle2, ShieldCheck, GitBranch, Database, FileCheck } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { workCaseStudies, workPolicy } from '../data/siteContent';

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
  { value: '90', label: 'Verified Agent Configurations', source: 'company-registry.yaml' },
  { value: '2,373', label: 'Automated Regression Tests', source: 'pytest test suite' },
  { value: '20', label: 'Departments Modeled', source: 'company-registry.yaml' },
  { value: '5-Tier', label: 'Human Approval Gates', source: 'ApprovalGate matrix' },
];

export const ProofPage: React.FC<ProofPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* 1. EXECUTIVE OUTCOME (Above the fold: what/who/why/next in 5s) */}
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

      {/* 2. THE INSTITUTIONAL PROBLEM */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
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

      {/* 3. LIGHTSPEED'S APPROACH */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="LIGHTSPEED'S APPROACH"
          title="The 4-Tier Honesty Ladder"
          lead="We classify every single capability on this website into one of four verified honesty tiers. We never pretend an R&amp;D concept is a battle-tested product."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'}`}>
            <span className="inline-block px-2.5 py-1 rounded-full text-[10px] font-bold tracking-widest bg-ls-cyan/10 text-ls-cyan border border-ls-cyan/30 uppercase">
              Proven
            </span>
            <h4 className="mt-3 text-base font-bold font-display">Proven In-House</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Running in our daily operations, validated against 2,373 automated tests, and generating verified audit receipts.
            </p>
          </div>
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'}`}>
            <span className="inline-block px-2.5 py-1 rounded-full text-[10px] font-bold tracking-widest bg-ls-red/10 text-ls-red border border-ls-red/30 uppercase">
              Pilot
            </span>
            <h4 className="mt-3 text-base font-bold font-display">Active Pilot</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Under active deployment trial with early partner organizations under governed human CEO oversight.
            </p>
          </div>
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'}`}>
            <span className="inline-block px-2.5 py-1 rounded-full text-[10px] font-bold tracking-widest bg-ls-grey-light/20 text-ls-grey-light-text border border-ls-grey-light/30 uppercase">
              Fieldable
            </span>
            <h4 className="mt-3 text-base font-bold font-display">Fieldable in 2026</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Architecturally complete, tested in simulation, and ready for immediate deployment on client infrastructure.
            </p>
          </div>
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'}`}>
            <span className="inline-block px-2.5 py-1 rounded-full text-[10px] font-bold tracking-widest bg-ls-navy/40 text-ls-grey-dark border border-ls-grey-dark/40 uppercase">
              Development
            </span>
            <h4 className="mt-3 text-base font-bold font-display">In Development</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Active engineering track. We describe the architectural intent without making commercial availability claims.
            </p>
          </div>
        </div>
      </section>

      {/* 4. PROOF AND EVIDENCE (METRICS + CASE STUDIES + POLICY TRACK) */}
      <section
        id="metrics"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
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
            </div>
          ))}
        </div>

        {/* Shipped Case Studies */}
        <div className="mt-16 pt-12 border-t border-inherit">
          <h3 className="text-xl sm:text-2xl font-bold font-display">Shipped Engagements &amp; In-House Systems</h3>
          <p className={`mt-1 text-xs sm:text-sm max-w-xl ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            Concrete deliverables built and operated by our agent workforce.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            {workCaseStudies.map((card) => (
              <div
                key={card.id}
                className={`rounded-3xl p-6 sm:p-8 border flex flex-col justify-between ${
                  isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">{card.id}</span>
                    <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-body text-[10px] font-bold tracking-widest ${
                      card.badge.includes('Proven')
                        ? 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
                        : 'border-ls-red/40 bg-ls-red/10 text-ls-red'
                    }`}>
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
        </div>

        {/* Regional Policy Track */}
        <div className="mt-16 pt-12 border-t border-inherit">
          <h3 className="text-xl sm:text-2xl font-bold font-display">Regional Policy &amp; Standards Track</h3>
          <p className={`mt-1 text-xs sm:text-sm max-w-xl ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            Collaborations and governance frameworks establishing regional compliance and data residency standards.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            {workPolicy.map((card) => (
              <div
                key={card.id}
                className={`rounded-3xl p-6 sm:p-7 border flex flex-col justify-between ${
                  isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
                }`}
              >
                <div>
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">{card.id}</span>
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
        </div>
      </section>

      {/* 5. ENGAGEMENT PATH */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-16 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="HOW TO VERIFY"
          title="Verify Our Systems Before You Commit"
          lead="We offer transparent inspection paths for executive teams, technical auditors, and compliance officers."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'}`}>
            <GitBranch className="w-6 h-6 text-ls-red mb-3" />
            <h4 className="font-bold text-base font-display">1. Code &amp; Test Suite Review</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Technical teams can inspect our CI pipelines, ruff/mypy/bandit linting reports, and the 2,373 automated regression tests.
            </p>
          </div>
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'}`}>
            <ShieldCheck className="w-6 h-6 text-ls-cyan mb-3" />
            <h4 className="font-bold text-base font-display">2. Governance Walkthrough</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Review the 5-tier Human-in-the-Loop approval gate, immutable SHA-256 audit trails, and data processing agreements.
            </p>
          </div>
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'}`}>
            <FileCheck className="w-6 h-6 text-ls-red mb-3" />
            <h4 className="font-bold text-base font-display">3. 90-Day Governed Pilot</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Deploy a low-risk, bounded pilot with explicit milestone deliverables, fixed Kwacha/USD pricing, and human CEO sign-off.
            </p>
          </div>
        </div>
      </section>

      {/* 6. CLEAR CTA */}
      <CtaBand
        theme={theme}
        title="Schedule an Executive Proof Walkthrough"
        text="Meet with our CEO to inspect the running agent platform, verify our audit logs, and discuss your institution's specific automation requirements."
        ctaLabel="Book an Executive Briefing"
        ctaTo="/contact"
      />
    </>
  );
};

export default ProofPage;
