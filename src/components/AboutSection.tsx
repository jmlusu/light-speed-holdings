import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Shield, Cpu, Layers, Target, Compass, ShieldCheck, UserCheck, Lock, FileCode, Sparkles, CheckCircle2 } from 'lucide-react';
import { leadership } from '../data/leadership';
import { CTAS } from '../data/ctas';

interface AboutSectionProps {
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const AboutSection: React.FC<AboutSectionProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';

  const containerBg = isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-ls-navy-dark text-white';
  const cardBg = isLight ? 'bg-ls-white text-ls-navy shadow-sm border border-slate-200/80' : 'bg-ls-navy/80 text-white shadow-xl border border-slate-800/80';
  const secondaryText = isLight ? 'text-ls-grey-dark' : 'text-slate-300';
  const mutedText = isLight ? 'text-ls-grey-dark/80' : 'text-slate-400';
  const accentRed = 'text-ls-red';
  const accentCyan = 'text-ls-cyan';

  return (
    <div className={`w-full font-sans pb-16 ${containerBg}`}>
      <section className="relative overflow-hidden pt-28 sm:pt-36 pb-16 px-6 lg:px-12 text-center">
        {/* Background Atmosphere */}
        <div className="absolute inset-0 pointer-events-none select-none z-0">
          <div className={`absolute inset-0 ${
            isLight
              ? 'bg-ls-grey-light'
              : 'bg-[#070A40]'
          }`} />
        </div>

        <div className="max-w-7xl mx-auto space-y-6 relative z-10">
          <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-cyan-950/40 text-cyan-400 font-mono text-xs tracking-widest uppercase border border-cyan-800/40">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span>WHO WE ARE // INSTITUTIONAL CHARTER</span>
          </div>

          <h1 className={`text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight font-display max-w-4xl mx-auto leading-tight ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            AN <span className="text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-red/80 to-ls-cyan">AI-NATIVE COMPANY BUILDER</span>
          </h1>

          <p className={`text-base sm:text-xl max-w-3xl mx-auto leading-relaxed font-sans ${secondaryText}`}>
            LightSpeed Holdings Limited™ transforms human intent into governed, intelligent, and executable business operations across African markets and global enterprise corridors.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <Link
              to={CTAS.primary.to}
              className="btn-milled btn-milled-primary inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/25 transition-all hover:bg-ls-red/90 cursor-pointer"
            >
              <span>{CTAS.primary.label}</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              to="/what-we-do"
              className={`btn-milled btn-milled-secondary inline-flex items-center gap-2 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase transition-all ${
                isLight
                  ? 'bg-ls-white text-ls-navy hover:bg-slate-100 shadow-sm border border-slate-300'
                  : 'bg-white/10 text-white hover:bg-white/15 border border-white/10'
              }`}
            >
              <span>Explore What We Do</span>
            </Link>
          </div>
        </div>
      </section>

      {/* 2. IDENTITY SECTION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-10" aria-label="Company Identity">
        <div className={`p-8 sm:p-12 rounded-3xl transition-all ${cardBg}`}>
          <div className="flex items-center gap-2 mb-4">
            <span className="w-2.5 h-2.5 rounded-full bg-ls-red" />
            <span className="font-mono text-xs font-bold tracking-widest text-ls-red uppercase">
              OUR IDENTITY // WHAT LIGHTSPEED IS
            </span>
          </div>

          <h2 className={`text-2xl sm:text-3xl font-bold font-display tracking-tight mb-4 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Not a Copilot Reseller. Not an Outsourcing Shop. An AI-Native Company Builder.
          </h2>

          <p className={`text-sm sm:text-base leading-relaxed max-w-4xl mb-8 ${secondaryText}`}>
            LightSpeed Holdings Limited™ operates at the intersection of deep AI system architecture, sovereign regulatory policy, and fiduciary advisory. We do not re-sell generic SaaS chat tools or provide temporary IT staffing. We design, deploy, and govern complete, autonomous agentic operating systems—scalable from one agent to the 90-role internal benchmark—that collapse workflow latency, compress operating expenses, and ensure total human sovereign control.
          </p>

          {/* Three Foundations Architectural Triptych Visual */}
          <div className="relative w-full aspect-[21/9] sm:aspect-[16/7] rounded-2xl overflow-hidden mb-8 border border-white/10 shadow-lg group">
            <img
              src="/src/assets/images/identity_triptych_foundations_1793818127924.jpg"
              alt="Three Foundations of LightSpeed Holdings Architectural Triptych"
              className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent flex items-end p-4">
              <span className="text-[10px] font-mono font-bold text-cyan-300 uppercase tracking-widest bg-black/60 px-3 py-1 rounded backdrop-blur-sm border border-cyan-800/40">
                Architectural Builder · Governance-First Operator · African Enterprise Pioneer
              </span>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className={`p-6 rounded-2xl space-y-3 ${isLight ? 'bg-ls-grey-light/60' : 'bg-slate-900/80'}`}>
              <div className="p-3 rounded-xl bg-ls-red/10 text-ls-red w-fit">
                <Cpu className="w-5 h-5" />
              </div>
              <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Architectural Builder
              </h3>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Engineered from the ground up for multi-agent orchestration, deterministic tool routing, and long-running organizational memory.
              </p>
            </div>

            <div className={`p-6 rounded-2xl space-y-3 ${isLight ? 'bg-ls-grey-light/60' : 'bg-slate-900/80'}`}>
              <div className="p-3 rounded-xl bg-ls-cyan/10 text-ls-cyan w-fit">
                <Shield className="w-5 h-5" />
              </div>
              <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Governance-First Operator
              </h3>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Every agent action is bounded by a five-tier approval matrix, cryptographic SHA-256 audit trails, and strict tenant isolation.
              </p>
            </div>

            <div className={`p-6 rounded-2xl space-y-3 ${isLight ? 'bg-ls-grey-light/60' : 'bg-slate-900/80'}`}>
              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-500 w-fit">
                <Sparkles className="w-5 h-5" />
              </div>
              <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                African Enterprise Pioneer
              </h3>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                By skipping the copilot phase, African enterprises leapfrog directly into autonomous, sovereign agentic operating systems.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. PHILOSOPHY SECTION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-10" aria-label="Corporate Philosophy">
        <div className={`rounded-3xl p-8 sm:p-12 text-center relative overflow-hidden transition-all ${
          isLight ? 'bg-ls-navy text-white shadow-xl' : 'bg-[#03061C] text-white shadow-2xl border border-cyan-900/30'
        }`}>
          <span className="text-xs font-mono font-bold tracking-[0.35em] text-ls-red uppercase mb-2 block">
            OFFICIAL CORPORATE PHILOSOPHY &amp; TAGLINE
          </span>
          <h2 className="text-3xl sm:text-5xl font-extrabold font-display tracking-tight text-ls-cyan my-3">
            ASPIRE. ACT. ACHIEVE.
          </h2>
          <p className="text-sm sm:text-base max-w-2xl mx-auto leading-relaxed text-slate-300 font-sans italic mb-8">
            &ldquo;Ambition without execution is theatre. We aspire with intent, act with governed speed, and measure what we achieve.&rdquo;
          </p>

          {/* Philosophy Progression Architectural Visual */}
          <div className="relative w-full aspect-[21/9] sm:aspect-[16/7] rounded-2xl overflow-hidden mb-8 border border-white/10 shadow-lg group">
            <img
              src="/src/assets/images/philosophy_triptych_clean_1793818099752.jpg"
              alt="ASPIRE. ACT. ACHIEVE. Architectural Progression Triptych"
              className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end justify-between p-4 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-300">
              <span className="text-ls-cyan">01 / Strategic Intent</span>
              <span className="text-ls-red">02 / Governed Speed</span>
              <span className="text-emerald-400">03 / Measurable Value</span>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-6 text-left pt-2">
            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 space-y-2">
              <span className="text-xs font-mono font-bold text-ls-cyan uppercase tracking-wider">[ 01 ] ASPIRE</span>
              <h3 className="text-lg font-bold font-display text-white">Strategic Intent</h3>
              <p className="text-xs leading-relaxed text-slate-300">
                Setting clear institutional ambition, evaluating economic feasibility, and designing sovereign agentic architectures before a single line of code is written.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 space-y-2">
              <span className="text-xs font-mono font-bold text-ls-red uppercase tracking-wider">[ 02 ] ACT</span>
              <h3 className="text-lg font-bold font-display text-white">Governed Speed</h3>
              <p className="text-xs leading-relaxed text-slate-300">
                Building and deploying specialized agent teams, collapsing multi-step workflows, and integrating deterministic risk controls for instant operational execution.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 space-y-2">
              <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">[ 03 ] ACHIEVE</span>
              <h3 className="text-lg font-bold font-display text-white">Measurable Value</h3>
              <p className="text-xs leading-relaxed text-slate-300">
                Measuring hard operational outcomes—cycle time compression, operating expense reduction, defect elimination, and sovereign data independence.
              </p>
            </div>
          </div>

          <div className="mt-8 pt-4 border-t border-white/10 text-center">
            <span className="text-[11px] font-mono text-slate-400">
              Note: &ldquo;ASPIRE. ACT. ACHIEVE.&rdquo; is the sole authoritative corporate tagline governed by LightSpeed Brand Guidelines v1.0.1.
            </span>
          </div>
        </div>
      </section>

      {/* 4. VISION AND MISSION SECTION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-10" aria-label="Vision and Mission">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className={`p-8 sm:p-10 rounded-3xl space-y-4 ${cardBg}`}>
            <div className="p-3.5 rounded-2xl bg-ls-red/10 text-ls-red w-fit">
              <Target className="w-6 h-6" />
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-ls-red" />
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Institutional Mission
              </h3>
            </div>
            <p className={`text-sm leading-relaxed ${secondaryText}`}>
              To enable enterprises, public institutions, and growth companies across Malawi and African markets to design, build, and govern sovereign AI operating models that eliminate workflow latency and multiply human capability.
            </p>
          </div>

          <div className={`p-8 sm:p-10 rounded-3xl space-y-4 ${cardBg}`}>
            <div className="p-3.5 rounded-2xl bg-ls-cyan/10 text-ls-cyan w-fit">
              <Compass className="w-6 h-6" />
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-ls-cyan" />
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Strategic Vision
              </h3>
            </div>
            <p className={`text-sm leading-relaxed ${secondaryText}`}>
              To establish LightSpeed Holdings Limited™ as the premier AI-Native Operator and Partner, recognized across the globe for sovereign agentic systems, regional model laws, operational execution, and category-defining AI enterprise building.
            </p>
          </div>
        </div>

        {/* Founding Thesis Banner */}
        <div className={`mt-8 p-8 rounded-3xl ${
          isLight ? 'bg-cyan-50/80 border border-cyan-200/80 text-ls-navy' : 'bg-slate-900/90 border border-cyan-900/40 text-white'
        }`}>
          <div className="flex items-center gap-2 mb-3">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
            <span className="font-mono text-xs font-bold tracking-widest text-cyan-600 dark:text-cyan-400 uppercase">
              FOUNDING LEAPFROG THESIS
            </span>
          </div>
          <h4 className={`text-lg font-bold font-display mb-2 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Skipping the Copilot Era
          </h4>
          <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
            The African enterprise market does not need to passively consume legacy Western SaaS or wait through years of incremental chat copilots. By skipping the copilot era, African enterprises have a once-in-a-generation leapfrogging opportunity to construct fully autonomous, agentic AI operating systems.
          </p>
        </div>
      </section>

      {/* 5. LEADERSHIP SECTION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Executive Leadership">
        <div className={`p-8 sm:p-10 rounded-3xl transition-all ${cardBg}`}>
          <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-6 border-b border-slate-200 dark:border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-ls-red" />
                <span className="font-mono text-xs font-bold tracking-widest text-ls-red uppercase">
                  EXECUTIVE COMMAND &amp; FIDUCIARY AUTHORITY
                </span>
              </div>
              <h2 className={`text-2xl font-bold font-display mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Verified Leadership
              </h2>
            </div>
            <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-ls-red/10 text-ls-red uppercase">
              Tier 5 Signature Authority
            </span>
          </div>

          <div className="space-y-6">
            {leadership.map((leader) => (
              <div
                key={leader.id}
                className={`p-6 sm:p-8 rounded-2xl flex flex-col sm:flex-row items-start gap-6 transition-all ${
                  isLight ? 'bg-ls-grey-light/50 border border-slate-200' : 'bg-slate-900/90 border border-slate-800'
                }`}
              >
                {/* Initials Badge - Authentic, no fake AI faces */}
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-ls-red to-ls-red/80 text-white font-extrabold text-2xl font-display flex items-center justify-center shrink-0 shadow-lg shadow-ls-red/20 border border-ls-red/40">
                  {leader.initials}
                </div>

                <div className="flex-1 space-y-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                        {leader.name}
                      </h3>
                      <span className="w-2 h-2 rounded-full bg-emerald-500" />
                    </div>
                    <span className="text-xs font-mono font-bold text-ls-red uppercase tracking-wider">
                      {leader.title}
                    </span>
                  </div>

                  <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
                    {leader.bio}
                  </p>

                  <div className={`pt-3 border-t text-xs font-mono flex flex-wrap items-center gap-4 ${
                    isLight ? 'border-slate-200 text-ls-grey-dark' : 'border-slate-800 text-slate-400'
                  }`}>
                    <span>• Human Sovereign Authority</span>
                    <span>• SADC Policy Lead</span>
                    <span>• 90-Role Internal Reference Fleet Overseer</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 6. OPERATING PRINCIPLES SECTION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Operating Principles">
        <div className="mb-6">
          <span className="text-xs font-mono font-bold tracking-widest text-cyan-600 dark:text-cyan-400 uppercase">
            AUTHORITATIVE GOVERNANCE
          </span>
          <h2 className={`text-2xl sm:text-3xl font-bold font-display mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Operating Principles
          </h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className={`p-6 sm:p-8 rounded-2xl space-y-3 ${cardBg}`}>
            <div className="flex items-center gap-2">
              <UserCheck className="w-5 h-5 text-ls-red" />
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                1. Human Sovereign Authority
              </h3>
            </div>
            <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
              AI expands execution capacity, but human authority remains sovereign. Critical financial, legal, constitutional, and policy actions require mandatory human sign-off via our five-tier approval matrix.
            </p>
          </div>

          <div className={`p-6 sm:p-8 rounded-2xl space-y-3 ${cardBg}`}>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-ls-cyan" />
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                2. Evidence Before Assertion
              </h3>
            </div>
            <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
              We never fabricate metrics, unproven testimonials, or exaggerated benchmarks. Every claim in Pharos research and client engagements is backed by first-party code proof and transparent audit trails.
            </p>
          </div>

          <div className={`p-6 sm:p-8 rounded-2xl space-y-3 ${cardBg}`}>
            <div className="flex items-center gap-2">
              <Lock className="w-5 h-5 text-emerald-500" />
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                3. Architectural Discipline
              </h3>
            </div>
            <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
              Systems are built with deterministic state transitions, rate limiters, circuit breakers, and bounded blast radiuses. Safety and governance are hardcoded into the runtime, not written in policy memos.
            </p>
          </div>

          <div className={`p-6 sm:p-8 rounded-2xl space-y-3 ${cardBg}`}>
            <div className="flex items-center gap-2">
              <FileCode className="w-5 h-5 text-ls-red" />
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                4. Context-Aware Leapfrogging
              </h3>
            </div>
            <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
              Designed specifically for regional connectivity realities, local data residency regulations, and sovereign infrastructure requirements across African markets and global trade corridors.
            </p>
          </div>
        </div>
      </section>

      {/* 7. RESPONSIBLE AI & GOVERNANCE SECTION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Responsible AI and Risk Controls">
        <div className={`p-8 sm:p-10 rounded-3xl transition-all ${cardBg}`}>
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2.5 h-2.5 rounded-full bg-ls-cyan" />
            <span className="font-mono text-xs font-bold tracking-widest text-ls-cyan uppercase">
              RESPONSIBLE AI // RISK &amp; GOVERNANCE CONTROLS
            </span>
          </div>

          <h2 className={`text-2xl font-bold font-display mb-4 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Sovereign Execution &amp; Fiduciary Controls
          </h2>

          <div className="grid md:grid-cols-3 gap-6 pt-2">
            <div className={`p-5 rounded-2xl space-y-2 ${isLight ? 'bg-ls-grey-light/50' : 'bg-slate-900/80'}`}>
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-ls-cyan shrink-0" />
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  Enterprise Data Segregation
                </h3>
              </div>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Strict tenant isolation boundaries ensure organizational memory and prompt data never cross tenant boundaries or train public models.
              </p>
            </div>

            <div className={`p-5 rounded-2xl space-y-2 ${isLight ? 'bg-ls-grey-light/50' : 'bg-slate-900/80'}`}>
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-ls-red shrink-0" />
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  5-Tier Human Approval Matrix
                </h3>
              </div>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Configurable human-in-the-loop gates queue human review for high-impact financial, legal, or constitutional decisions.
              </p>
            </div>

            <div className={`p-5 rounded-2xl space-y-2 ${isLight ? 'bg-ls-grey-light/50' : 'bg-slate-900/80'}`}>
              <div className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-emerald-500 shrink-0" />
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  Cryptographic Audit Trails
                </h3>
              </div>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Every agent action, approval, and state modification generates a SHA-256 sealed audit record for regulatory compliance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 8. FUTURE-FACING APPROACH */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Future-Facing Approach">
        <div className={`p-8 sm:p-10 rounded-3xl ${
          isLight ? 'bg-ls-navy text-white shadow-lg' : 'bg-[#03061C] text-white border border-slate-800'
        }`}>
          <div className="flex items-center gap-2 mb-3">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
            <span className="font-mono text-xs font-bold tracking-widest text-cyan-400 uppercase">
              FUTURE-FACING APPROACH // EVOLVING OPERATING CAPABILITY
            </span>
          </div>
          <h2 className="text-2xl font-bold font-display mb-3 text-white">
            Building the Sovereign Agentic Ecosystem
          </h2>
          <p className="text-xs sm:text-sm leading-relaxed text-slate-300 max-w-4xl mb-6">
            LightSpeed Holdings Limited™ continues to advance sovereign AI capability across Africa by contributing to open agent standards (OpenCode), authoring Pharos policy frameworks for SADC regional integration, and deploying modular agentic teams that adapt to evolving enterprise demands without locking clients into brittle proprietary vendor ecosystems.
          </p>

          {/* Modular Agent Architecture Visual */}
          <div className="relative w-full aspect-[21/9] sm:aspect-[16/7] rounded-2xl overflow-hidden border border-white/10 shadow-xl group">
            <img
              src="/src/assets/images/modular_agent_architecture_1793818142394.jpg"
              alt="Modular and configurable agentic enterprise architecture visual"
              className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end justify-between p-4">
              <span className="text-[10px] font-mono font-bold text-cyan-300 uppercase tracking-widest bg-black/60 px-3 py-1 rounded backdrop-blur-sm border border-cyan-800/40">
                Configurable Client Implementations (1 to N+ Agents)
              </span>
              <span className="text-[10px] font-mono text-slate-400 hidden sm:inline-block">
                Sovereign Human Direction Enforced
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* 9. ENGAGEMENT CTA */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto pt-8 text-center" aria-label="Engage LightSpeed CTA">
        <div className={`rounded-3xl p-10 sm:p-14 space-y-6 transition-all ${
          isLight ? 'bg-ls-white text-ls-navy shadow-md border border-slate-200' : 'bg-ls-navy/90 text-white shadow-2xl border border-slate-800'
        }`}>
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red uppercase">
            PARTNER WITH LIGHTSPEED
          </span>
          <h2 className={`text-3xl sm:text-4xl font-extrabold font-display tracking-tight ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Ready to Build Your AI-Native Operating Capability?
          </h2>
          <p className={`text-sm sm:text-base max-w-2xl mx-auto leading-relaxed ${secondaryText}`}>
            Engage LightSpeed Holdings Limited™ to design, build, and govern sovereign agentic operating systems tailored to your institutional goals.
          </p>
          <div className="pt-2">
            <button
              onClick={() => onOpenContactModal(CTAS.primary.label)}
              className="btn-milled btn-milled-primary inline-flex items-center gap-2.5 px-8 py-4 rounded-full bg-ls-red text-white font-bold text-xs tracking-widest uppercase transition-all shadow-xl shadow-ls-red/30 cursor-pointer hover:bg-ls-red/90"
            >
              <span>{CTAS.primary.label}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutSection;
