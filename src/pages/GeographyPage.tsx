import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { geography } from '../data/siteContent';

interface GeographyPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const GeographyPage: React.FC<GeographyPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <main>
      <PageIntro
        theme={theme}
        eyebrow="GEOGRAPHY"
        title="Malawi → SADC → Africa"
        lead="LightSpeed Holdings is anchored in Lilongwe, Malawi. From our home market we extend into the SADC region and the broader African continent — each step governed by the same principle: prove it where the constraints are real, then scale with integrity."
      >
        <div className="flex flex-wrap gap-3 mt-6">
          <Link
            to="/contact"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98]"
          >
            Start a Conversation
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>
      </PageIntro>

      <SectionHeading
        theme={theme}
        eyebrow="OPERATING TERRITORY"
        title="Where We Work — and What That Means"
        lead="Every geography carries a different honest status. We do not blur the line between proven delivery and active development."
      />

      <div className="px-4 sm:px-8 max-w-7xl mx-auto w-full pb-24">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {geography.map((item, index) => (
            <Reveal key={item.id} delay={index * 0.1}>
              <div
                className={`group relative rounded-3xl border p-6 sm:p-8 flex flex-col gap-4 transition-all duration-300 hover:shadow-xl ${
                  isLight
                    ? 'bg-ls-white border-ls-grey-dark/20 hover:border-ls-red/40'
                    : 'bg-ls-navy/50 border-ls-white/10 hover:border-ls-red/30'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3
                      className={`text-xl font-black tracking-tight font-display ${
                        isLight ? 'text-ls-navy' : 'text-ls-white'
                      }`}
                    >
                      {item.name}
                    </h3>
                    <p
                      className={`text-sm font-medium mt-1 ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      {item.title}
                    </p>
                  </div>
                  <HonestyBadge label={item.status} />
                </div>
                <p
                  className={`text-sm leading-relaxed flex-1 ${
                    isLight ? 'text-ls-grey-dark/70 font-medium' : 'text-ls-grey-light-text/70'
                  }`}
                >
                  {item.description}
                </p>
                <Link
                  to="/contact"
                  className="inline-flex items-center gap-1.5 text-xs font-bold tracking-wider uppercase text-ls-red transition-colors cursor-pointer hover:underline"
                >
                  Learn more
                  <ArrowRight className="w-3 h-3" aria-hidden="true" />
                </Link>
              </div>
            </Reveal>
          ))}
        </div>
      </div>

      <CtaBand theme={theme} />
    </main>
  );
};

export default GeographyPage;
