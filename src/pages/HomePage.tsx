import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { HeroSection } from '../components/HeroSection';
import { StrategyChasmSection } from '../components/StrategyChasmSection';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { UseCaseCatalogSection } from '../components/UseCaseCatalogSection';
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
  { value: 152, label: 'Verified Agent Configurations', format: 'comma' },
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
    title: 'Ship, Don\u2019t Promise',
    body: 'Every claim on this site is labeled Proven in-house, In pilot, Fieldable, or In development — and the tests that gate our own work are published. We never blur the two.',
  },
  {
    num: '03',
    title: 'Governed by Design',
    body: 'Five-tier human approval, immutable audit trails, and regional compliance are the architecture of the workforce, not bolt-ons. Trust is what scales.',
  },
  {
    num: '04',
    title: 'Research Informed',
    body: 'Pharos turns engineering into public intellectual work. The SADC Agentic AI Governance Framework and Malawi\u2019s National AI Strategy consultation position LightSpeed as a source of policy, not just product. Every finding is dated, benchmarks are regenerated on each release, and no claim is fabricated.',
  },
];

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const [activePillar, setActivePillar] = useState(0);

  const sectionBorder = isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80';

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
                isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
              }`}>
                <span className="font-body text-2xl font-black text-ls-red">{col.num}</span>
                <h3 className="mt-2 font-display font-bold text-base sm:text-lg tracking-tight">{col.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {col.body}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
        <p className={`mt-8 text-center font-body text-xs font-bold tracking-widest ${
          isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
        }`}>
          <span className="text-ls-red">NORTH STAR // </span>
          {company.northStar.toUpperCase()}
        </p>
      </section>

      {/* What We Build — AI Company Builder spotlight */}
      <section aria-labelledby="spotlight-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <Reveal>
          <div className={`relative overflow-hidden rounded-3xl p-8 sm:p-10 flex flex-col lg:flex-row lg:items-center gap-8 border shadow-xl ${
            isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy' : 'bg-ls-navy border-ls-white/15 text-ls-white'
          }`}>
            <div className="flex-1 space-y-4">
              <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">WHAT WE BUILD // AI COMPANY BUILDER</span>
              <h3 className="text-2xl sm:text-4xl font-black tracking-tight font-display">Your Governed AI Workforce</h3>
              <p className={`text-sm sm:text-base leading-relaxed max-w-xl ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                The orchestration engine that runs LightSpeed — 90 agents, 20 departments — licensed to run on your infrastructure. Human direction, audited execution.
              </p>
              <Link
                to="/ai-company-builder"
                className="ripple-on inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
              >
                Explore AI Company Builder
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
            </div>

            <ul className={`lg:w-80 grid grid-cols-2 lg:grid-cols-1 gap-2.5 text-xs font-bold ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
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
              <Link to={`/solutions/${sol.slug}`} className={`ripple-on rounded-3xl p-6 border transition-all h-full flex flex-col justify-between group ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
              }`}>
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">{sol.eyebrow}</span>
                    <HonestyBadge label={sol.proof} />
                  </div>
                  <h3 className={`font-display font-bold text-base tracking-tight ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    {sol.title}
                  </h3>
                  <p className={`text-xs leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    {sol.oneLiner}
                  </p>
                </div>
                <div className={`pt-4 mt-4 border-t flex items-center justify-between ${isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'}`}>
                  <span className={`text-[10px] font-body font-bold tracking-widest group-hover:text-ls-red transition-colors ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>EXPLORE</span>
                  <ArrowRight className="w-3.5 h-3.5 text-ls-red" aria-hidden="true" />
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Link to="/what-we-do" className="font-body text-xs font-bold tracking-widest text-ls-cyan hover:underline">
            VIEW ALL CAPABILITIES &amp; CATALOG →
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
                isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
              }`}>
                <h3 className="font-display font-bold text-sm sm:text-base tracking-tight">{pillar.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {pillar.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Link to="/technology" className="font-body text-xs font-bold tracking-widest text-ls-cyan hover:underline">
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
              className={`ripple-on px-4 py-2.5 rounded-full border font-bold text-[11px] tracking-wider transition-colors cursor-pointer ${
                isLight
                  ? 'bg-ls-white/95 border-ls-grey-dark text-ls-grey-dark hover:border-ls-red hover:text-ls-red'
                  : 'bg-ls-navy/80 border-ls-white/15 text-ls-white hover:border-ls-red hover:text-ls-red'
              }`}
            >
              {ind.nav}
            </Link>
          ))}
          <Link
            to="/what-we-do"
            className={`ripple-on px-4 py-2.5 rounded-full border font-bold text-[11px] tracking-wider bg-ls-red/10 border-ls-red/30 text-ls-red transition-colors cursor-pointer hover:brightness-110`}
          >
            All Industries &amp; Verticals
          </Link>
        </div>
      </section>

      {/* Use Case Catalog — 50 offerable scenarios, honestly tagged */}
      <UseCaseCatalogSection theme={theme} onRequestBriefing={onRequestBriefing} />

      {/* Proof Band: verified operating metrics + work */}
      <Reveal delay={0.05}>
      <section id="proof" aria-label="Verified operating metrics" className="px-4 sm:px-8 pb-4 max-w-7xl mx-auto w-full">
        <div className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 border shadow-xl ${
          isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy' : 'bg-ls-navy border-ls-white/15 text-ls-white'
        }`}>
          <div className="flex flex-col xl:flex-row xl:items-center gap-8 xl:gap-12">
            <div className="flex-1 space-y-6">
              <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest">
                <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
                <span>PROOF // VERIFIED OPERATING METRICS</span>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
                {PROOF_STATS.map((stat, sIdx) => (
                  <div key={sIdx} className="min-w-0">
                    <span className={`block text-xl sm:text-2xl font-black font-body tracking-tight ${
                      sIdx % 2 === 0 ? 'text-ls-red' : 'text-ls-cyan'
                    }`}>
                      <StatCounter to={stat.value} format={stat.format} suffix={stat.suffix} />
                    </span>
                    <span className={`block mt-1 text-[10px] font-body font-bold tracking-widest uppercase ${
                      isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                    }`}>
                      {stat.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className={`shrink-0 w-full xl:w-auto xl:border-l xl:pl-12 flex flex-col items-start gap-3 ${
              isLight ? 'xl:border-ls-grey-dark/30' : 'xl:border-ls-white/10'
            }`}>
              <Link
                to="/proof"
                className="ripple-on w-full xl:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
              >
                See the Evidence
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
              <span className={`text-[10px] font-body tracking-widest font-bold ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                SHIPPED ENGAGEMENTS &amp; POLICY
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
              <Link to={post.to} className={`ripple-on rounded-3xl p-6 border transition-all h-full block group ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl'
              }`}>
                <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan">{post.topic}</span>
                <h3 className={`mt-3 font-display font-bold text-base tracking-tight group-hover:text-ls-red transition-colors ${
                  isLight ? 'text-ls-navy' : 'text-ls-white'
                }`}>
                  {post.title}
                </h3>
                <span className={`mt-4 inline-flex items-center gap-1.5 text-[11px] font-body font-bold tracking-widest ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
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
          isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
        }`}>
          <div className="flex-1 space-y-3">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">ABOUT</span>
            <h3 className="text-xl sm:text-2xl font-black tracking-tight font-display">One Human CEO. 140+ AI Agents.</h3>
            <p className={`text-sm leading-relaxed ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}>
              We are the AI-native company we sell — governed, audited, and holding every claim to its evidence. Read the mission, the values, and what we promise whom.
            </p>
          </div>
          <Link
            to="/about"
            className="ripple-on inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase border border-ls-red/40 bg-ls-red/10 text-ls-red transition-all cursor-pointer hover:brightness-110"
          >
            About LightSpeed
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>
      </section>

      {/* Who we work with */}
      <section aria-labelledby="who-work-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="WHO WE WORK WITH"
          title="Organisations We Partner With"
          lead="SMEs, NGOs, government agencies, donor organisations, financial services providers, healthcare organisations, and growth companies across Malawi and SADC. We also license the AI Company Builder platform to organisations that want their own governed AI workforce."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="p-4 border rounded-xl h-full">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan">SMEs</span>
            <p className="mt-2 text-sm leading-relaxed">Small and medium enterprises building digital presence and automating operations</p>
          </div>
          <div className="p-4 border rounded-xl h-full">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan">NGOs</span>
            <p className="mt-2 text-sm leading-relaxed">Non-governmental organisations driving development impact</p>
          </div>
          <div className="p-4 border rounded-xl h-full">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan">Government</span>
            <p className="mt-2 text-sm leading-relaxed">Malawi government agencies and SADC institutions</p>
          </div>
          <div className="p-4 border rounded-xl h-full">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan">Donor Organisations</span>
            <p className="mt-2 text-sm leading-relaxed">Donor bodies requiring compliant AI workflows</p>
          </div>
          <div className="p-4 border rounded-xl h-full">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan">Healthcare</span>
            <p className="mt-2 text-sm leading-relaxed">Hospitals and clinics across Malawi and SADC</p>
          </div>
          <div className="p-4 border rounded-xl h-full">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan">Financial Services</span>
            <p className="mt-2 text-sm leading-relaxed">Banks, microfinance, and insurance institutions</p>
          </div>
        </div>
      </section>

      <CtaBand theme={theme} />
    </div>
  );
};

export default HomePage;
