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
import {
  StatusLedPip,
  MachineScrewHead,
  AcousticVentGrille,
  ChassisPanel
} from './TactileHardwareElements';

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
          <StatusLedPip status="emerald" isLight={isLight} />
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

      {/* Our Story & Thesis Chassis */}
      <div className={`p-8 sm:p-12 rounded-3xl border relative overflow-hidden transition-all ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

        <div className="max-w-3xl mx-auto space-y-6 text-sm leading-relaxed">
          <div className="flex items-center justify-between border-b border-ls-grey-dark/80 pb-4">
            <div className="flex items-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="font-body text-ls-red font-extrabold text-xs uppercase tracking-wider">FOUNDING THESIS & SOVEREIGN MANDATE</span>
            </div>
            <AcousticVentGrille cols={4} rows={2} isLight={isLight} />
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
          <MachineScrewHead isLight={isLight} className="absolute top-2.5 left-2.5" />
          <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />

          <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
            <Target className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <StatusLedPip status="emerald" isLight={isLight} />
            <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Institutional Mission</h3>
          </div>
          <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            To empower enterprises, public institutions, and growth companies across Malawi and SADC to design, build, and govern sovereign AI operating models that eliminate workflow latency and multiply human capability.
          </p>
        </div>

        <div className={`p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>
          <MachineScrewHead isLight={isLight} className="absolute top-2.5 left-2.5" />
          <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />

          <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
            <Compass className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <StatusLedPip status="emerald" isLight={isLight} />
            <h3 className={`text-base font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Strategic Vision</h3>
          </div>
          <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            To establish LightSpeed Holdings Limited as the premier AI-Native Operator and Partner—recognized across the globe for sovereign agentic systems, regional model laws, operational execution, and category-defining AI enterprise building.
          </p>
        </div>

        <div className={`p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>
          <MachineScrewHead isLight={isLight} className="absolute top-2.5 left-2.5" />
          <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />

          <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <StatusLedPip status="emerald" isLight={isLight} />
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
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

        <div className="flex items-center justify-between border-b border-ls-grey-dark pb-3">
          <div className="flex items-center gap-2">
            <StatusLedPip status="emerald" isLight={isLight} />
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
                <StatusLedPip status="emerald" isLight={isLight} />
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
