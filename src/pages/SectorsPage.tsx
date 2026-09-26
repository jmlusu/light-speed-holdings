import React from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { HonestyLabel } from '../data/siteContent';

interface SectorsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

const PROVEN: HonestyLabel = { label: 'PROVEN EXPERIENCE', tone: 'proven' };
const CURRENT: HonestyLabel = { label: 'CURRENT CAPABILITY', tone: 'pilot' };
const DEMO: HonestyLabel = { label: 'DEMONSTRATION', tone: 'fieldable' };
const FUTURE: HonestyLabel = { label: 'FUTURE OPPORTUNITY', tone: 'development' };

interface Sector {
  name: string;
  evidence: string;
  tier: HonestyLabel;
}

const SECTORS: Sector[] = [
  {
    name: 'Government and Public Sector',
    evidence:
      'Agent-driven student management at the University of Malawi — 3 departments onboarded, 5,000 records processed with immutable audit trails. Advisory work on Malawi\u2019s National AI Strategy consultation.',
    tier: CURRENT,
  },
  {
    name: 'Development and Donor Organizations',
    evidence:
      'Donor reporting automation with GDPR-level data handling as the default posture for UN and development data flows. Engagements priced in USD for international partners.',
    tier: CURRENT,
  },
  {
    name: 'Financial Services',
    evidence:
      'Governed multi-agent compliance automation for a regional financial institution: regulatory reporting across 14 departments with full audit trails, cutting reporting time by 40%.',
    tier: PROVEN,
  },
  {
    name: 'Agriculture',
    evidence:
      'WhatsApp-native coordination platform for agricultural cooperatives across Malawi and Mozambique, with mobile-money payments and supply chain tracking — serving 1,200 members in pilot.',
    tier: CURRENT,
  },
  {
    name: 'SMEs and Entrepreneurs',
    evidence:
      'Mobile-first websites and e-commerce stores with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one, delivered at local cost from Malawi.',
    tier: CURRENT,
  },
  {
    name: 'Technology Companies',
    evidence:
      'The AI Company Builder platform itself: a 90-agent registry, 5-tier approval matrix, and immutable audit trails verified by 2,557 automated regression tests.',
    tier: PROVEN,
  },
  {
    name: 'Telecommunications',
    evidence:
      'Mobile-money rails (Airtel Money, TNM Mpamba) integrated into delivered platforms. No direct telco operator engagement yet.',
    tier: DEMO,
  },
  {
    name: 'Health',
    evidence:
      'Offline-first, sovereignty-first architecture is designed for clinical data — but LightSpeed has no health-sector deployment yet. Listed honestly as a roadmap target.',
    tier: FUTURE,
  },
  {
    name: 'Energy',
    evidence:
      'No energy-sector engagement to date. The governance model and offline-first stack apply directly when the first partner appears.',
    tier: FUTURE,
  },
];

const TIERS: { tier: HonestyLabel; desc: string }[] = [
  { tier: PROVEN, desc: 'Delivered engagements with named, measurable outcomes.' },
  { tier: CURRENT, desc: 'Running pilots or capability we can deploy now.' },
  { tier: DEMO, desc: 'Working demonstration without a live client engagement.' },
  { tier: FUTURE, desc: 'Roadmap target — no evidence yet, and we say so.' },
];

/**
 * /sectors per MASTER_SPEC §11: useful without becoming a generic industry
 * list. Nine sectors, each carrying an evidence tier — only claim sector
 * experience where evidence exists.
 */
export const SectorsPage: React.FC<SectorsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="SECTORS"
        title="Sectors We Serve — With the Evidence to Back It"
        lead="Nine sectors across Malawi and SADC. Every sector card carries an evidence tier: proven experience, current capability, demonstration, or future opportunity. We only claim what we can show."
      />

      {/* Evidence tier legend */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-2">
        <SectionHeading
          theme={theme}
          eyebrow="HOW TO READ THIS PAGE"
          title="Four Evidence Tiers"
          lead="Sector claims are graded the same way as every other claim on this site."
        />
        <Reveal>
          <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4`}>
            {TIERS.map(({ tier, desc }) => (
              <div
                key={tier.label}
                className={`rounded-2xl p-5 border ${isLight ? 'bg-ls-white border-ls-grey-dark/60 shadow-sm' : 'bg-ls-navy border-ls-white/10 shadow-lg'}`}
              >
                <HonestyBadge label={tier} />
                <p className={`mt-3 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {desc}
                </p>
              </div>
            ))}
          </div>
        </Reveal>
      </section>

      {/* Sector cards */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {SECTORS.map((sector, idx) => (
            <Reveal key={sector.name} delay={(idx % 3) * 0.06}>
              <div
                className={`rounded-3xl p-6 border h-full flex flex-col gap-4 ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <h3
                    className={`font-display font-bold text-lg tracking-tight ${
                      isLight ? 'text-ls-navy' : 'text-ls-white'
                    }`}
                  >
                    {sector.name}
                  </h3>
                  <HonestyBadge label={sector.tier} />
                </div>
                <p
                  className={`text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  {sector.evidence}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default SectorsPage;
