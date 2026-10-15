import React from 'react';
import { HeroBanner } from './HeroBanner';
import { ThesisBanner } from './ThesisBanner';
import { OperatingModelGrid } from './OperatingModelGrid';
import { MissionVisionValuesGrid } from './MissionVisionValuesGrid';
import { leadership } from '../data/leadership';
import { CTAS } from '../data/ctas';
import { ArrowRight } from 'lucide-react';

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
      <HeroBanner theme={theme} onOpenContactModal={onOpenContactModal} />

      {/* Aspire. Act. Achieve. Thesis Banner */}
      <ThesisBanner theme={theme} />

      {/* Operating Model: Strategy → Build → Govern → Research */}
      <OperatingModelGrid theme={theme} />

      {/* Our Story & Thesis Chassis */}
      <div className={`p-8 sm:p-12 rounded-3xl border relative overflow-hidden transition-all ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}

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
            LightSpeed Holdings Limited was established on a single core principle: the African enterprise market does not need to passively consume legacy Western SaaS or wait through years of incremental chat copilots. By skipping the copilot era, African enterprises have a once-in-a-generation leapfrogging opportunity to construct fully <strong>autonomous, agentic AI operating systems</strong>.
          </p>
          <p className={isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}>
            Operating across Malawi and African markets, and Pan-African trade corridors, LightSpeed Holdings Limited merges deep AI architecture, sovereign policy governance, and fiduciary advisory into deployable operational machinery.
          </p>
        </div>
      </div>

      {/* Mission, Vision, Values Grid */}
      <MissionVisionValuesGrid theme={theme} />

      {/* Executive Leadership Chassis */}
      <div className={`p-8 sm:p-10 rounded-3xl border relative overflow-hidden space-y-6 transition-all ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}

        <div className="flex items-center justify-between border-b border-ls-grey-dark pb-3">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ls-emerald" />
            <h2 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
              Executive Command & Fiduciary Authority
            </h2>
          </div>
          <span className="text-[10px] font-body text-ls-grey-light-text uppercase">TIER 5 SIGNATURE</span>
        </div>

        {leadership.map((leader) => (
          <div
            key={leader.id}
            className={`p-6 rounded-2xl border flex flex-col sm:flex-row items-start gap-6 ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}
          >
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-ls-red to-ls-red/85 text-ls-navy font-extrabold text-xl font-body flex items-center justify-center shrink-0 shadow-lg shadow-ls-red/20 border border-ls-red/40">
              {leader.initials}
            </div>
            <div className="space-y-2">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>{leader.name}</h3>
                  <span className="w-2 h-2 rounded-full bg-ls-emerald" />
                </div>
                <span className="text-xs font-body text-ls-red font-extrabold uppercase tracking-wider">{leader.title}</span>
              </div>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                {leader.bio}
              </p>
            </div>
          </div>
        ))}

      </div>

      {/* CTA */}
      <div className="text-center pt-4">
        <button
          onClick={() => onOpenContactModal(CTAS.primary.label)}
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-ls-red hover:bg-ls-red/40 text-ls-navy font-extrabold font-body text-xs uppercase tracking-wider transition-all shadow-xl shadow-ls-red/20 active:scale-95"
        >
          <span>Partner with LightSpeed Holdings Limited</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Brand Carousel Placeholder */}
      <div className="my-12 text-center">
        <p className="text-ls-grey-dark text-lg">Brand Carousel — illustrations, diagrams, and infographics will appear here</p>
      </div>

    </section>
  );
};
