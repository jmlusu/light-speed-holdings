import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { HeroSection } from '../components/HeroSection';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { solutions, insightTeasers, company } from '../data/siteContent';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

const PROOF_STATS = [
  { value: 90, label: 'Agent Configurations', format: 'comma' },
  { value: 2557, label: 'Automated Regression Tests', format: 'comma' },
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
    body: 'Pharos turns engineering into public intellectual work. The SADC Agentic AI Governance Framework and Malawi\u2019s National AI Strategy consultation position LightSpeed as a source of policy, not just product.',
  },
];

const SECTORS = [
  { title: 'Government & Public Sector', desc: 'Digital services, compliance automation, and data-driven policy for ministries and agencies.', status: { label: 'Proven in-house', tone: 'proven' as const } },
  { title: 'Development & Donors', desc: 'Donor reporting, M&E pipelines, and compliance workflows for UNDP and development partners.', status: { label: 'In pilot', tone: 'pilot' as const } },
  { title: 'Financial Services', desc: 'Risk classification, audit trails, and regulatory reporting for banks and microfinance.', status: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
  { title: 'Health', desc: 'Data pipelines, reporting automation, and decision support for clinics and health systems.', status: { label: 'Concept', tone: 'development' as const } },
  { title: 'Agriculture & Energy', desc: 'Supply-chain intelligence, climate-data pipelines, and operational dashboards for rural economies.', status: { label: 'Concept', tone: 'development' as const } },
  { title: 'SMEs & Entrepreneurs', desc: 'Mobile-first digital presence, automation, and AI tooling priced for the local market.', status: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
  { title: 'Technology Companies', desc: 'AI-native operating models, agentic workflows, and governance frameworks for tech firms.', status: { label: 'In development', tone: 'development' as const } },
];

const AGENT_CATEGORIES = [
  { label: 'Strategy', count: '12', color: 'text-ls-red' },
  { label: 'Research', count: '14', color: 'text-ls-cyan' },
  { label: 'Product & Eng', count: '18', color: 'text-ls-gold' },
  { label: 'Operations', count: '11', color: 'text-ls-green' },
  { label: 'Governance', count: '16', color: 'text-ls-purple' },
  { label: 'Content & Comms', count: '9', color: 'text-ls-pink' },
  { label: 'Finance & Legal', count: '10', color: 'text-ls-teal' },
];

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const sectionBorder = isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80';

  return (
    <div>
      <HeroSection theme={theme} onRequestBriefing={onRequestBriefing} />

      {/* The Lightspeed Thesis — Strategy → Build → Govern → Research & Policy */}
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

      {/* AI Company Builder spotlight */}
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
              <Link to="/contact" className={`ripple-on rounded-3xl p-6 border transition-all h-full flex flex-col justify-between group ${
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

      {/* 90-Agent Workforce */}
      <section aria-labelledby="workforce-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="OPERATING MODEL"
          title="A Coordinated Workforce of 90 Agents"
          lead="LightSpeed operates through a governed digital workforce — 90 agents across 20 departments, each with explicit role definitions and approval thresholds. Human direction, audited execution."
        />
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3">
          {AGENT_CATEGORIES.map((cat, idx) => (
            <Reveal key={cat.label} delay={idx * 0.04}>
              <div className={`rounded-2xl p-4 border text-center ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
              }`}>
                <span className={`font-body text-2xl sm:text-3xl font-black ${cat.color}`}>{cat.count}</span>
                <p className="mt-2 text-[10px] font-body font-bold tracking-widest uppercase opacity-70">{cat.label}</p>
              </div>
            </Reveal>
          ))}
        </div>
        <div className="mt-6 text-center">
          <Link to="/ai-company-builder" className="font-body text-xs font-bold tracking-widest text-ls-cyan hover:underline">
            EXPLORE THE AGENT ARCHITECTURE →
          </Link>
        </div>
      </section>

      {/* Sectors */}
      <section aria-labelledby="sectors-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${sectionBorder}`}>
        <SectionHeading
          theme={theme}
          eyebrow="SECTORS"
          title="Where We Apply It"
          lead="Only claim sector experience where evidence exists. Each area is labeled with its honest status — proven, pilot, fieldable, or emerging."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {SECTORS.map((sector, idx) => (
            <Reveal key={sector.title} delay={(idx % 3) * 0.06}>
              <Link to="/sectors" className={`ripple-on rounded-3xl p-5 border transition-all group ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
              }`}>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h3 className={`font-display font-bold text-sm sm:text-base tracking-tight group-hover:text-ls-red transition-colors ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    {sector.title}
                  </h3>
                  <HonestyBadge label={sector.status} />
                </div>
                <p className={`text-xs leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {sector.desc}
                </p>
              </Link>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Link to="/sectors" className="font-body text-xs font-bold tracking-widest text-ls-cyan hover:underline">
            EXPLORE ALL SECTORS →
          </Link>
        </div>
      </section>

      {/* Proof Band */}
      <Reveal delay={0.05}>
      <section id="proof" aria-label="Verified operating metrics" className="px-4 sm:px-8 pb-4 max-w-7xl mx-auto w-full">
        <div className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 border shadow-xl ${
          isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy' : 'bg-ls-navy border-ls-white/15 text-ls-white'
        }`}>
          <div className="flex flex-col xl:flex-row xl:items-center gap-8 xl:gap-12">
            <div className="flex-1 space-y-6">
              <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest">
                <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80" />
                <span>PROOF // VERIFIED OPERATING METRICS</span>
              </div>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
                {PROOF_STATS.map((stat, sIdx) => (
                  <div key={sIdx} className="min-w-0">
                      <span className="block text-xl sm:text-2xl font-black font-body tracking-tight">
                        {stat.value}
                        {stat.suffix}
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
            <h3 className="text-xl sm:text-2xl font-black tracking-tight font-display">One Human CEO. 90 AI Agents.</h3>
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

      <CtaBand theme={theme} />
    </div>
  );
};

export default HomePage;
