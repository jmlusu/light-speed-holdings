import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Shield, Cpu, Layers, Target, Compass, ShieldCheck, UserCheck, Lock, FileCode, Sparkles, CheckCircle2 } from 'lucide-react';
import { leadership } from '../data/leadership';
import { CTAS } from '../data/ctas';
import { humanAuthorityStatement } from '../data/shipped/company';

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
          <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-cyan-950/40 text-cyan-400 font-body text-xs tracking-widest uppercase border border-cyan-800/40">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span>WHO WE ARE // LIGHTSPEED HOLDINGS LIMITED™</span>
          </div>

          <h1 className={`text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight font-display max-w-4xl mx-auto leading-tight ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            ASPIRE. <span className="font-black text-ls-red">ACT.</span> ACHIEVE.
          </h1>

          <p className={`text-base sm:text-xl max-w-3xl mx-auto leading-relaxed font-sans ${secondaryText}`}>
            LightSpeed Holdings Limited™ builds AI-native companies. We help you design, launch, and scale operations where AI agents execute work under explicit human authority and approval rules.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <Link
              to={CTAS.primary.to}
              className="btn-milled btn-milled-primary inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/25 transition-all hover:bg-ls-red/90 cursor-pointer"
            >
              <span>{CTAS.primary.label}</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 pt-8 max-w-5xl mx-auto text-left">
            {[
              { value: '90', label: 'Operating Roles (89 Agents + 1 Human CEO)' },
              { value: '7', label: 'HAOMTGV Operating Layers' },
              { value: '5', label: 'Human Approval Tiers' },
              { value: '100%', label: 'Audit Trail Coverage' },
            ].map((metric) => (
              <div key={metric.label} className={`p-4 rounded-2xl ${isLight ? 'bg-ls-white border border-slate-200/80' : 'bg-white/5 border border-white/10'}`}>
                <div className={`text-2xl sm:text-3xl font-extrabold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>{metric.value}</div>
                <div className={`text-[11px] sm:text-xs font-body uppercase tracking-wider mt-1 ${mutedText}`}>{metric.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 2. INTRODUCTION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-10" aria-label="Company Introduction">
        <div className={`p-8 sm:p-12 rounded-3xl transition-all ${cardBg}`}>
          <div className="flex items-center gap-2 mb-4">
            <span className="w-2.5 h-2.5 rounded-full bg-ls-red" />
            <span className="font-body text-xs font-bold tracking-widest text-ls-red uppercase">
              COMPANY INTRODUCTION
            </span>
          </div>

          <h2 className={`text-2xl sm:text-3xl font-bold font-display tracking-tight mb-4 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Governed AI-Native Operations
          </h2>

          <p className={`text-sm sm:text-base leading-relaxed max-w-4xl ${secondaryText}`}>
            LightSpeed Holdings Limited™ is an African-headquartered AI venture studio and strategic partner. We combine AI-native company building, workflow automation, and governance controls in one operating model. From Lilongwe, Malawi, we design, launch, and scale enterprises where configurable AI agent teams execute work and human leaders retain final decision authority.
          </p>

          {/* Human authority — canonical statement */}
          <p className={`mt-4 font-body text-sm sm:text-base font-bold tracking-wide border-l-4 pl-4 py-1 ${
            isLight ? 'border-ls-cyan-ink text-ls-navy' : 'border-ls-cyan text-white'
          }`}>
            {humanAuthorityStatement}
          </p>
        </div>
      </section>

      {/* 3. OUR STORY */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-10" aria-label="Our Story">
        <div className={`p-8 sm:p-12 rounded-3xl transition-all ${cardBg}`}>
          <div className="flex items-center gap-2 mb-4">
            <span className="w-2.5 h-2.5 rounded-full bg-ls-cyan" />
            <span className="font-body text-xs font-bold tracking-widest text-ls-cyan uppercase">
              OUR STORY // FROM INTENT TO EXECUTION
            </span>
          </div>

          <h2 className={`text-2xl sm:text-3xl font-bold font-display tracking-tight mb-4 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            An Operating Model Built for Trustworthy AI
          </h2>

          <div className={`space-y-4 text-sm sm:text-base leading-relaxed max-w-4xl ${secondaryText}`}>
            <p>
              LightSpeed started with a clear position: AI needs governance before you let it execute business operations. We built HAOMTGV (Human, Agents, Orchestration, Memory, Tools, Governance, Value) to connect human decision authority with controlled agent execution.
            </p>
            <p>
              Today, LightSpeed operates a 90-role internal workforce: 89 AI agents and one Human CEO. We use it as an internal proof of concept. We apply the same architecture to client work, from single specialized agents to coordinated multi-department systems, with human approval on consequential actions.
            </p>
          </div>
        </div>
      </section>

      {/* 4. MISSION & VISION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-10" aria-label="Mission and Vision">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className={`p-8 sm:p-10 rounded-3xl space-y-4 ${cardBg}`}>
            <div className="p-3.5 rounded-2xl bg-ls-red/10 text-ls-red w-fit">
              <Target className="w-6 h-6" />
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-ls-red" />
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                OUR MISSION
              </h3>
            </div>
            <p className={`text-sm leading-relaxed ${secondaryText}`}>
              Help organisations build, operate, and scale by turning human intent into governed AI execution systems with measurable, trustworthy results.
            </p>
          </div>

          <div className={`p-8 sm:p-10 rounded-3xl space-y-4 ${cardBg}`}>
            <div className="p-3.5 rounded-2xl bg-ls-cyan/10 text-ls-cyan w-fit">
              <Compass className="w-6 h-6" />
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-ls-cyan" />
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                OUR VISION
              </h3>
            </div>
            <p className={`text-sm leading-relaxed ${secondaryText}`}>
              Become a globally recognized leader in AI-native company building and set clear standards for designing, governing, and scaling businesses that use autonomous agents.
            </p>
          </div>
        </div>
      </section>

      {/* 5. CORE VALUES */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Core Values">
        <div className="mb-6">
          <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
            OUR VALUES // THE PRINCIPLES THAT GOVERN US
          </span>
          <h2 className={`text-2xl sm:text-3xl font-bold font-display mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Operating Principles for AI-Native Work
          </h2>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { title: 'AI-Native First', body: 'We design AI into the execution model from the start.', Icon: Cpu, color: 'text-ls-red bg-ls-red/10' },
            { title: 'Human Authority & Accountability', body: 'Agents execute; people decide. Human accountability remains explicit.', Icon: UserCheck, color: 'text-ls-cyan bg-ls-cyan/10' },
            { title: 'Evidence Over Claims', body: 'We prioritize measurable results, empirical validation, and transparent reporting.', Icon: CheckCircle2, color: isLight ? 'text-ls-cyan-ink bg-ls-cyan/10' : 'text-ls-cyan bg-ls-cyan/10' },
            { title: 'Governance by Design', body: 'Compliance checks, audit records, and approval gates form part of the architecture.', Icon: Shield, color: 'text-ls-red bg-ls-red/10' },
            { title: 'Security & Trust', body: 'We use enterprise security controls, data residency options, and tenant isolation by default.', Icon: Lock, color: 'text-ls-cyan bg-ls-cyan/10' },
            { title: 'Continuous Learning', body: 'We design systems and agents to improve from operational feedback.', Icon: Sparkles, color: isLight ? 'text-ls-cyan-ink bg-ls-cyan/10' : 'text-ls-cyan bg-ls-cyan/10' },
          ].map((value) => (
            <div key={value.title} className={`p-6 sm:p-8 rounded-2xl space-y-3 ${cardBg}`}>
              <div className={`p-3 rounded-xl w-fit ${value.color}`}>
                <value.Icon className="w-5 h-5" />
              </div>
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                {value.title}
              </h3>
              <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
                {value.body}
              </p>
            </div>
          ))}
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
            <span className="font-body text-xs font-bold tracking-widest text-cyan-600 dark:text-cyan-400 uppercase">
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

      {/* 6. LEADERSHIP */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Executive Leadership">
        <div className={`p-8 sm:p-10 rounded-3xl transition-all ${cardBg}`}>
          <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-6 border-b border-slate-200 dark:border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-ls-red" />
                <span className="font-body text-xs font-bold tracking-widest text-ls-red uppercase">
                  LEADERSHIP // SOVEREIGN HUMAN DIRECTION
                </span>
              </div>
              <h2 className={`text-2xl font-bold font-display mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Human Authority Behind the Platform
              </h2>
            </div>
          </div>

          <div className="space-y-6">
            {leadership.map((leader) => (
              <div
                key={leader.id}
                className={`p-6 sm:p-8 rounded-2xl flex flex-col sm:flex-row items-start gap-6 transition-all ${
                  isLight ? 'bg-ls-grey-light/50 border border-slate-200' : 'bg-slate-900/90 border border-slate-800'
                }`}
              >
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-ls-red to-ls-red/80 text-white font-extrabold text-2xl font-display flex items-center justify-center shrink-0 shadow-lg shadow-ls-red/20 border border-ls-red/40">
                  {leader.initials}
                </div>

                <div className="flex-1 space-y-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                        {leader.name}
                      </h3>
                    </div>
                    <span className="text-xs font-body font-bold text-ls-red uppercase tracking-wider">
                      {leader.title}
                    </span>
                  </div>

                  <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
                    Designed the HAOMTGV operating model and LightSpeed&apos;s AI-native company-building strategy. Directs the 90-role agent workforce and retains final authority over Tier 5 governance decisions.
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 7. DIFFERENTIATION */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="What Makes LightSpeed Different">
        <div className="mb-6">
          <span className="text-xs font-body font-bold tracking-widest text-cyan-600 dark:text-cyan-400 uppercase">
            DIFFERENTIATION // THE LIGHTSPEED ADVANTAGE
          </span>
          <h2 className={`text-2xl sm:text-3xl font-bold font-display mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            How We Build Governed AI Operations
          </h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {[
            { title: 'AI-Native Company Builder', body: 'We redesign workflows around governed agent execution rather than adding chatbots to existing processes.', Icon: Cpu, color: 'text-ls-red' },
            { title: 'HAOMTGV Architecture', body: 'Our seven-layer framework defines how orchestration, memory, tools, and governance work together under deterministic controls.', Icon: Layers, color: 'text-ls-cyan' },
            { title: 'Governed Autonomous Workforces', body: 'Configurable teams, from one agent upward, execute complex tasks without autonomous privilege escalation.', Icon: UserCheck, color: 'text-ls-cyan' },
            { title: 'Cryptographic Accountability', body: 'The system records agent actions, tool calls, and human approvals in a tamper-evident SHA-256 audit ledger.', Icon: FileCode, color: 'text-ls-red' },
            { title: 'African Context, Global Standards', body: 'We design for mobile money, data residency, and connectivity constraints in African markets while applying enterprise security controls.', Icon: Compass, color: 'text-ls-cyan' },
          ].map((item) => (
            <div key={item.title} className={`p-6 sm:p-8 rounded-2xl space-y-3 ${cardBg}`}>
              <div className="flex items-center gap-2">
                <item.Icon className={`w-5 h-5 ${item.color}`} />
                <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  {item.title}
                </h3>
              </div>
              <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
                {item.body}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* 8. GOVERNANCE, TRUST & SECURITY */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Governance, Trust and Security">
        <div className={`p-8 sm:p-10 rounded-3xl transition-all ${cardBg}`}>
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2.5 h-2.5 rounded-full bg-ls-cyan" />
            <span className="font-body text-xs font-bold tracking-widest text-ls-cyan uppercase">
              GOVERNANCE &amp; TRUST // AUDITABLE BY DESIGN
            </span>
          </div>

          <h2 className={`text-2xl font-bold font-display mb-4 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Governance for Autonomous Systems
          </h2>
          <p className={`text-sm leading-relaxed max-w-4xl mb-6 ${secondaryText}`}>
            LightSpeed enforces a five-tier human approval matrix. Low-risk tasks can execute automatically. Financial, legal, or structural actions stop for explicit human authorization.
          </p>

          <div className="grid md:grid-cols-2 gap-6 pt-2">
            <div className={`p-5 rounded-2xl space-y-2 ${isLight ? 'bg-ls-grey-light/50' : 'bg-slate-900/80'}`}>
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-ls-cyan shrink-0" />
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  Zero-Trust Agent Boundaries
                </h3>
              </div>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Agents run in sandboxed boundaries with least-privilege API access and no raw credential exposure.
              </p>
            </div>

            <div className={`p-5 rounded-2xl space-y-2 ${isLight ? 'bg-ls-grey-light/50' : 'bg-slate-900/80'}`}>
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-ls-red shrink-0" />
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  Tenant-Isolated Memory
                </h3>
              </div>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Tenant boundaries keep organisational memory and prompt data separate. Client data does not train public models.
              </p>
            </div>

            <div className={`p-5 rounded-2xl space-y-2 ${isLight ? 'bg-ls-grey-light/50' : 'bg-slate-900/80'}`}>
              <div className="flex items-center gap-2">
                <UserCheck className="w-4 h-4 text-ls-cyan shrink-0" />
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  5-Tier Human Approval Matrix
                </h3>
              </div>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Configurable approval gates queue high-impact financial, legal, or constitutional decisions for human review.
              </p>
            </div>

            <div className={`p-5 rounded-2xl space-y-2 ${isLight ? 'bg-ls-grey-light/50' : 'bg-slate-900/80'}`}>
              <div className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-ls-cyan shrink-0" />
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  Cryptographic Audit Trails
                </h3>
              </div>
              <p className={`text-xs leading-relaxed ${secondaryText}`}>
                Agent actions, approvals, and state changes generate SHA-256 sealed audit records for compliance review.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 9. FUTURE-FACING APPROACH */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto my-12" aria-label="Future-Facing Approach">
        <div className={`p-8 sm:p-10 rounded-3xl ${
          isLight ? 'bg-ls-navy text-white shadow-lg' : 'bg-[#03061C] text-white border border-slate-800'
        }`}>
          <div className="flex items-center gap-2 mb-3">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
            <span className="font-body text-xs font-bold tracking-widest text-cyan-400 uppercase">
              FUTURE-FACING APPROACH // EVOLVING OPERATING CAPABILITY
            </span>
          </div>
          <h2 className="text-2xl font-bold font-display mb-3 text-white">
            Building Sovereign Agentic Capability
          </h2>
          <p className="text-xs sm:text-sm leading-relaxed text-slate-300 max-w-4xl mb-6">
            LightSpeed Holdings Limited™ continues to develop sovereign AI capability in Africa. We contribute to open agent standards through OpenCode, publish Pharos policy frameworks for SADC regional integration, and build modular agent teams that adapt to changing enterprise requirements without proprietary vendor lock-in.
          </p>

          <div className="relative w-full aspect-[21/9] sm:aspect-[16/7] rounded-2xl overflow-hidden border border-white/10 shadow-xl group">
            <img
              src="/assets/images/modular_agent_architecture_1793818142394.avif"
              alt="Modular and configurable agentic enterprise architecture visual"
              className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end justify-between p-4">
              <span className="text-[10px] font-body font-bold text-cyan-300 uppercase tracking-widest bg-black/60 px-3 py-1 rounded backdrop-blur-sm border border-cyan-800/40">
                Configurable Client Implementations (1 to N+ Agents)
              </span>
              <span className="text-[10px] font-body text-slate-400 hidden sm:inline-block">
                Sovereign Human Direction Enforced
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* 10. ENGAGEMENT CTA */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto pt-8 text-center" aria-label="Engage LightSpeed CTA">
        <div className={`rounded-3xl p-10 sm:p-14 space-y-6 transition-all ${
          isLight ? 'bg-ls-white text-ls-navy shadow-md border border-slate-200' : 'bg-ls-navy/90 text-white shadow-2xl border border-slate-800'
        }`}>
          <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
            PARTNER WITH LIGHTSPEED
          </span>
          <h2 className={`text-3xl sm:text-4xl font-extrabold font-display tracking-tight ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Ready to Build Your AI-Native Operating Capability?
          </h2>
          <p className={`text-sm sm:text-base max-w-2xl mx-auto leading-relaxed ${secondaryText}`}>
            Work with LightSpeed Holdings Limited™ to design, build, and govern agentic operating systems for your institutional goals.
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
