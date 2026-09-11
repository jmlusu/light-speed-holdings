import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { HeroSection } from '../components/HeroSection';
import { StrategyChasmSection } from '../components/StrategyChasmSection';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { StatCounter } from '../components/StatCounter';
import { solutions, industries, technologyPillars, insightTeasers, company } from '../data/siteContent';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/**
 * Verified operating metrics — sourced from company-registry (agent configs),
 * the automated test suite (regression tests), onboarded departments, and the
 * ApprovalGate governance layer (human approval tiers). No other data claims.
 */
interface ProofStat {
  value: number;
  label: string;
  format?: 'plain' | 'comma';
  suffix?: string;
}

const PROOF_STATS: ProofStat[] = [
  { value: 144, label: 'Verified Agent Configurations', format: 'comma' },
  { value: 2373, label: 'Automated Regression Tests', format: 'comma' },
  { value: 20, label: 'Departments Onboarded' },
  { value: 5, label: 'Human Approval Gates', suffix: '-Tier' },
];

const THESIS_COLUMNS = [
  {
    num: '01',
    title: 'Prove It in Malawi',
    body: 'Real clients, real constraints, real infrastructure. The proof is a shipped website, a donor report that used to take weeks, a dashboard that replaced forty-page PDFs — not a press release.',
  },
  {
    num: '02',
    title: 'Ship, Don’t Promise',
    body: 'Every claim on this site is labeled Proven in-house, In pilot, Fieldable, or In development — and the tests that gate our own work are published. We never blur the two.',
  },
  {
    num: '03',
    title: 'Governed by Design',
    body: 'Five-tier human approval, immutable audit trails, and regional compliance are the architecture of the workforce, not bolt-ons. Trust is what scales.',
  },
];

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const [activePillar, setActivePillar] = useState(0);

  const sectionBorder = isLight ? 'border-slate-200/80' : 'border-zinc-800/80';

  return (
    <div>
      <HeroSection
        theme={theme}
        onRequestBriefing={onRequestBriefing}
        activePillar={activePillar}
        onSelectPillar={setActivePillar}
      />

      <StrategyChasmSection theme={theme} />

      {/* The Lightspeed Thesis */}
      <section aria-labelledby="thesis-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="THE LIGHTSPEED THESIS"
          title="Malawi First. Prove It. Then the World."
          lead="Intelligent automation is not a privilege of rich countries. We win trust with real engagements, published case studies, and compliant, secure delivery — in Malawi first, where the constraints are real."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {THESIS_COLUMNS.map((col, idx) => (
            <Reveal key={col.num} delay={idx * 0.08}>
              <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <span className="font-mono text-2xl font-black text-ls-red">{col.num}</span>
                <h3 className="mt-2 font-display font-bold text-base sm:text-lg tracking-tight">{col.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {col.body}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
        <p className={`mt-8 text-center font-mono text-xs font-bold tracking-widest ${
          isLight ? 'text-slate-500' : 'text-zinc-500'
        }`}>
          <span className="text-ls-red">NORTH STAR // </span>
          {company.northStar.toUpperCase()}
        </p>
      </section>

      {/* What We Build — AI Company Builder spotlight */}
      <section aria-labelledby="spotlight-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <Reveal>
          <div className={`relative overflow-hidden rounded-3xl p-8 sm:p-10 flex flex-col lg:flex-row lg:items-center gap-8 ${
            isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-100'
          }`}>
            <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
            <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
            <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
            <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />

            <div className="flex-1 space-y-4">
              <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">WHAT WE BUILD // AI COMPANY BUILDER</span>
              <h3 className="text-2xl sm:text-4xl font-black tracking-tight font-display">Your Governed AI Workforce</h3>
              <p className={`text-sm sm:text-base leading-relaxed max-w-xl ${
                isLight ? 'text-slate-700' : 'text-zinc-300'
              }`}>
                The orchestration engine that runs LightSpeed — 144 agents, 20 departments — licensed to run on your infrastructure. Human direction, audited execution.
              </p>
              <Link
                to="/ai-company-builder"
                className="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:brightness-110"
              >
                Explore AI Company Builder
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
            </div>

            <ul className={`lg:w-80 grid grid-cols-2 lg:grid-cols-1 gap-2.5 text-xs font-bold ${
              isLight ? 'text-slate-800' : 'text-zinc-200'
            }`}>
              {['Human Leadership', 'Agent Workforce', 'Intelligent Workflows', 'Decision Intelligence'].map((rung) => (
                <li key={rung} className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-2xl border border-ls-cyan/25 bg-ls-cyan/5">
                  <span className="w-2 h-2 shrink-0 rounded-full bg-ls-cyan shadow-[0_0_6px_rgba(0,191,255,0.8)]" aria-hidden="true" />
                  {rung}
                </li>
              ))}
            </ul>
          </div>
        </Reveal>
      </section>

      {/* Solutions */}
      <section aria-labelledby="solutions-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="SOLUTIONS"
          title="Six Domains, One Governed Stack"
          lead="From strategy to shipped system — each solution carries its own honesty status."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {solutions.map((sol, idx) => (
            <Reveal key={sol.slug} delay={(idx % 3) * 0.06}>
              <Link to={`/solutions/${sol.slug}`} className={`rounded-3xl p-6 border transition-all h-full flex flex-col justify-between group ${
                isLight ? 'bg-white/95 border-slate-300 shadow-md hover:shadow-xl hover:-translate-y-0.5' : 'bg-zinc-950/80 border-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
              }`}>
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">{sol.eyebrow}</span>
                    <HonestyBadge label={sol.proof} />
                  </div>
                  <h3 className={`font-display font-bold text-base tracking-tight ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {sol.title}
                  </h3>
                  <p className={`text-xs leading-relaxed ${
                    isLight ? 'text-slate-700' : 'text-zinc-300'
                  }`}>
                    {sol.oneLiner}
                  </p>
                </div>
                <div className={`pt-4 mt-4 border-t flex items-center justify-between ${isLight ? 'border-slate-200' : 'border-white/10'}`}>
                  <span className={`text-[10px] font-mono font-bold tracking-widest group-hover:text-ls-red transition-colors ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>EXPLORE</span>
                  <ArrowRight className="w-3.5 h-3.5 text-ls-red" aria-hidden="true" />
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Link to="/solutions" className="font-mono text-xs font-bold tracking-widest text-ls-cyan hover:underline">
            VIEW ALL SOLUTIONS →
          </Link>
        </div>
      </section>

      {/* Technology */}
      <section aria-labelledby="technology-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="TECHNOLOGY"
          title="Engineered to Be Trusted"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {technologyPillars.slice(0, 4).map((pillar, idx) => (
            <Reveal key={pillar.title} delay={(idx % 2) * 0.06}>
              <div className={`rounded-3xl p-6 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <h3 className="font-display font-bold text-sm sm:text-base tracking-tight">{pillar.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {pillar.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Link to="/technology" className="font-mono text-xs font-bold tracking-widest text-ls-cyan hover:underline">
            SEE THE FULL ARCHITECTURE →
          </Link>
        </div>
      </section>

      {/* Industries */}
      <section aria-labelledby="industries-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="INDUSTRIES"
          title="Where We Apply It"
        />
        <div className="flex flex-wrap justify-center gap-2.5">
          {industries.map((ind) => (
            <Link
              key={ind.slug}
              to={`/industries/${ind.slug}`}
              className={`px-4 py-2.5 rounded-full border font-bold text-[11px] tracking-wider transition-colors cursor-pointer ${
                isLight
                  ? 'bg-white/95 border-slate-300 text-slate-700 hover:border-ls-red hover:text-ls-red'
                  : 'bg-zinc-950/80 border-white/15 text-zinc-200 hover:border-ls-red hover:text-ls-red'
              }`}
            >
              {ind.nav}
            </Link>
          ))}
          <Link
            to="/industries"
            className={`px-4 py-2.5 rounded-full border font-bold text-[11px] tracking-wider bg-ls-red/10 border-ls-red/30 text-ls-red transition-colors cursor-pointer hover:brightness-110`}
          >
            All Industries
          </Link>
        </div>
      </section>

      {/* Proof Band: verified operating metrics + work */}
      <Reveal delay={0.05}>
      <section id="proof" aria-label="Verified operating metrics" className="px-4 sm:px-8 pb-4 max-w-7xl mx-auto w-full">
        <div className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 ${
          isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
        }`}>
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />

          <div className="flex flex-col xl:flex-row xl:items-center gap-8 xl:gap-12">
            <div className="flex-1 space-y-6">
              <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
                <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
                <span>PROOF // VERIFIED OPERATING METRICS</span>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
                {PROOF_STATS.map((stat, sIdx) => (
                  <div key={sIdx} className="min-w-0">
                    <span className={`block text-xl sm:text-2xl font-black font-mono tracking-tight ${
                      sIdx % 2 === 0 ? 'text-ls-red' : 'text-ls-cyan'
                    }`}>
                      <StatCounter to={stat.value} format={stat.format} suffix={stat.suffix} />
                    </span>
                    <span className={`block mt-1 text-[10px] font-mono font-bold tracking-widest uppercase ${
                      isLight ? 'text-slate-500' : 'text-zinc-500'
                    }`}>
                      {stat.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className={`shrink-0 w-full xl:w-auto xl:border-l xl:pl-12 flex flex-col items-start gap-3 ${
              isLight ? 'xl:border-slate-300/70' : 'xl:border-white/10'
            }`}>
              <Link
                to="/work"
                className="w-full xl:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:brightness-110"
              >
                See the Work
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
              <span className={`text-[10px] font-mono tracking-widest font-bold ${
                isLight ? 'text-slate-500' : 'text-zinc-500'
              }`}>
                SHIPPED ENGAGEMENTS & POLICY
              </span>
            </div>
          </div>
        </div>
      </section>
      </Reveal>

      {/* Insights */}
      <section aria-labelledby="insights-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="INSIGHTS"
          title="The Agentic AI Voice of the Region"
          lead="Pharos turns LightSpeed's engineering into public intellectual work on Agentic AI Company Building, use cases, and policy — from Malawi's National AI Strategy consultation to the SADC governance framework."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {insightTeasers.map((post, idx) => (
            <Reveal key={post.title} delay={idx * 0.08}>
              <Link to={post.to} className={`rounded-3xl p-6 border transition-all h-full block group ${
                isLight ? 'bg-white/95 border-slate-300 shadow-md hover:shadow-xl' : 'bg-zinc-950/80 border-white/15 shadow-xl hover:shadow-2xl'
              }`}>
                <span className="font-mono text-[10px] font-bold tracking-widest text-ls-cyan">{post.topic}</span>
                <h3 className={`mt-3 font-display font-bold text-base tracking-tight group-hover:text-ls-red transition-colors ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {post.title}
                </h3>
                <span className={`mt-4 inline-flex items-center gap-1.5 text-[11px] font-mono font-bold tracking-widest ${
                  isLight ? 'text-slate-500' : 'text-zinc-400'
                } group-hover:text-ls-red`}>
                  READ →
                </span>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* About band */}
      <section aria-labelledby="about-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <div className={`rounded-3xl p-8 sm:p-10 flex flex-col lg:flex-row lg:items-center gap-6 border ${
          isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
        }`}>
          <div className="flex-1 space-y-3">
            <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">ABOUT</span>
            <h3 className="text-xl sm:text-2xl font-black tracking-tight font-display">One Human CEO. 140+ AI Agents.</h3>
            <p className={`text-sm leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              We are the AI-native company we sell — governed, audited, and holding every claim to its evidence. Read the mission, the values, and what we promise whom.
            </p>
          </div>
          <Link
            to="/about"
            className="inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase border border-ls-red/40 bg-ls-red/10 text-ls-red transition-all cursor-pointer hover:brightness-110"
          >
            About LightSpeed
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>
      </section>

      <CtaBand theme={theme} />
    </div>
  );
};

export default HomePage;
