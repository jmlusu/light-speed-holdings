import React from 'react';
import {
  Building2,
  Globe2,
  Target,
  Compass,
  Users,
  ShieldCheck,
  ArrowRight,
  Sparkles,
  Award,
  Lock
} from 'lucide-react';

interface AboutSectionProps {
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const AboutSection: React.FC<AboutSectionProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';

  return (
    <section id="about" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12 font-sans">

      {/* Header Banner */}
      <div className="text-center max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-body font-bold uppercase tracking-wider mb-4 border select-none">
          <span className="w-2 h-2 rounded-full bg-ls-emerald" />
          <span className={`text-[10px] font-body tracking-widest ${isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'}`}>
            INSTITUTIONAL CHARTER // SOVEREIGN MISSION
          </span>
        </div>
        <h1 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-ls-navy' : 'text-ls-white'
        }`}>
          About <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-red/40 to-ls-red/85">LightSpeed</span>
        </h1>
        <p className={`text-base sm:text-lg leading-relaxed font-sans italic ${
          isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
        }`}>
          "Africa does not need to wait for the future of enterprise. It can build it."
        </p>
      </div>

      {/* Aspire. Act. Achieve. Thesis Banner */}
      <div className={`rounded-3xl border px-6 sm:px-10 py-8 text-center relative overflow-hidden ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>

        <p className="text-[11px] font-body font-bold tracking-[0.35em] text-ls-red uppercase mb-3">
          Our Thesis
        </p>
        <p className="text-2xl sm:text-4xl font-black font-display tracking-tight text-ls-cyan">
          ASPIRE. ACT. ACHIEVE.
        </p>
        <p className={`text-xs sm:text-sm mt-3 max-w-xl mx-auto leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
          Ambition without execution is theatre. We aspire with intent, act with governed speed, and measure what we achieve.
        </p>
      </div>

      {/* Operating Model: Strategy → Build → Govern → Research */}
      <div className={`p-6 sm:p-8 rounded-3xl border relative overflow-hidden ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>

        <div className="flex items-center gap-2 border-b border-ls-grey-dark/80 pb-3 mb-5">
          <span className="w-2 h-2 rounded-full bg-ls-emerald" />
          <h2 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
            Operating Model
          </h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { step: '01', title: 'Strategy', body: 'Clarify ambition, constraints, and the decisions that matter before any build begins.' },
            { step: '02', title: 'Build', body: 'Design and ship agentic systems, data pipelines, and workflows against a governed backlog.' },
            { step: '03', title: 'Govern', body: 'Install controls, policy, and human-in-the-loop authority so systems stay accountable.' },
            { step: '04', title: 'Research', body: 'Feed evidence, benchmarks, and Pharos policy work back into the next strategy cycle.' }
          ].map((item) => (
            <div
              key={item.title}
              className={`p-5 rounded-2xl border space-y-2 ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}
            >
              <span className="text-[10px] font-body font-bold tracking-widest text-ls-red">[ {item.step} ]</span>
              <h3 className={`text-sm font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                {item.title}
              </h3>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                {item.body}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Our Story & Thesis Chassis */}
      <div className={`p-8 sm:p-12 rounded-3xl border relative overflow-hidden transition-all ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>




        <div className="max-w-3xl mx-auto space-y-6 text-sm leading-relaxed">
          <div className="flex items-center justify-between border-b border-ls-grey-dark/80 pb-4">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-ls-emerald" />
              <span className="font-body text-ls-red font-extrabold text-xs uppercase tracking-wider">FOUNDING THESIS & SOVEREIGN MANDATE</span>
            </div>
            <div className="w-16 h-4" />
          </div>

          <h2 className={`text-2xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
            The Lightspeed Leapfrog Thesis
          </h2>
          <p className={isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}>
            LightSpeed Holdings Limited was established on a single core principle: the African enterprise landscape does not need to passively consume legacy Western SaaS or wait through years of incremental chat copilots. By skipping the copilot era, African enterprises have an unprecedented leapfrogging opportunity to construct fully <strong>autonomous, agentic AI operating systems</strong>.
          </p>
          <p className={isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}>
            Operating across Malawi, the SADC economic community, and Pan-African trade corridors, LightSpeed Holdings Limited merges deep AI architecture, sovereign policy governance, and fiduciary advisory into deployable operational machinery.
          </p>
        </div>
      </div>

      {/* Mission, Vision, Values Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className={`p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>


          <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
            <Target className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ls-emerald" />
            <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Institutional Mission</h3>
          </div>
          <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            To empower enterprises, public institutions, and growth companies across Malawi and SADC to design, build, and govern sovereign AI operating models that eliminate workflow latency and multiply human capability.
          </p>
        </div>

        <div className={`p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>


          <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
            <Compass className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ls-emerald" />
            <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Strategic Vision</h3>
          </div>
          <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            To establish LightSpeed Holdings Limited as the premier AI-Native Operator and Partner—recognized across the globe for sovereign agentic systems, regional model laws, operational execution, and category-defining AI enterprise building.
          </p>
        </div>

        <div className={`p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>


          <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ls-emerald" />
            <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Why LightSpeed</h3>
          </div>
          <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            We are not a generic software outsourcer. We provide concrete architectural proof, OpenCode agent standards, SADC regulatory alignment, and fiduciary execution.
          </p>
        </div>

      </div>

      {/* Executive Leadership Chassis */}
      <div className={`p-8 sm:p-10 rounded-3xl border relative overflow-hidden space-y-6 transition-all ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>




        <div className="flex items-center justify-between border-b border-ls-grey-dark pb-3">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ls-emerald" />
            <h2 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
              Executive Command & Fiduciary Authority
            </h2>
          </div>
          <span className="text-[10px] font-body text-ls-grey-light-text uppercase">TIER 5 SIGNATURE</span>
        </div>

        <div className={`p-6 rounded-2xl border flex flex-col sm:flex-row items-start gap-6 ${
          isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
        }`}>
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-ls-red to-ls-red/85 text-ls-navy font-extrabold text-xl font-body flex items-center justify-center shrink-0 shadow-lg shadow-ls-red/20 border border-ls-red/40">
            JM
          </div>
          <div className="space-y-2">
            <div>
              <div className="flex items-center gap-2">
                <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Jack Mlusu</h3>
                <span className="w-2 h-2 rounded-full bg-ls-emerald" />
              </div>
              <span className="text-xs font-body text-ls-red font-extrabold uppercase tracking-wider">Founder & Chief Executive Officer</span>
            </div>
            <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Founder of LightSpeed Holdings Limited and architect of the Pharos Policy Track. Leading human-in-the-loop executive authority overseeing sovereign digital transformation, SADC policy submissions, and agentic AI deployments across Africa.
            </p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="text-center pt-4">
        <button
          onClick={() => onOpenContactModal('Start a Conversation')}
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-ls-red hover:bg-ls-red/40 text-ls-navy font-extrabold font-body text-xs uppercase tracking-wider transition-all shadow-xl shadow-ls-red/20 active:scale-95"
        >
          <span>Partner with LightSpeed Holdings Limited</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

    </section>
  );
};
