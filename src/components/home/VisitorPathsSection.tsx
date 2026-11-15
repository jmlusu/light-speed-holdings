import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, MessageCircleQuestion } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';

interface VisitorPathsSectionProps {
  theme: 'light' | 'dark';
}

interface VisitorPathCard {
  id: string;
  stage: string;
  intent: string;
  body: string;
  image: string;
  primary: { label: string; to: string };
  secondary: { label: string; to: string }[];
  accent: 'red' | 'cyan' | 'navy';
}

/** §8 Homepage Routing Principle - the four major visitor pathways. */
const VISITOR_PATHS: VisitorPathCard[] = [
  {
    id: 'business-leaders',
    stage: 'STRATEGY',
    intent: 'Business Leaders',
    body: 'Navigate the governed agentic operating model to design and launch AI systems that scale safely.',
    image: '/src/assets/images/audience_business_leaders_1793515174408.jpg',
    primary: { label: 'How We Work', to: '/what-we-do' },
    secondary: [
      { label: 'HAOMTGV Framework', to: '/haomtgv' },
    ],
    accent: 'red',
  },
  {
    id: 'partners',
    stage: 'COLLABORATION',
    intent: 'Partners',
    body: 'Collaborate with LightSpeed to build integrated agentic ecosystems for the African market.',
    image: '/src/assets/images/audience_partners_1793515174751.jpg',
    primary: { label: 'Partner With Us', to: '/contact' },
    secondary: [
      { label: 'Platform details', to: '/what-we-do' },
    ],
    accent: 'cyan',
  },
  {
    id: 'researchers',
    stage: 'ENQUIRY',
    intent: 'Researchers',
    body: 'Access Pharos insights, research briefs, and policy commentary on the evolution of AI in Africa.',
    image: '/src/assets/images/audience_researchers_1793515174898.jpg',
    primary: { label: 'Read Insights', to: '/insights' },
    secondary: [
      { label: 'Pharos practice', to: '/about' },
    ],
    accent: 'navy',
  },
  {
    id: 'policy-makers',
    stage: 'GOVERNANCE',
    intent: 'Policy Makers',
    body: 'Engage with our governance frameworks and institutional strategy for sovereign AI deployment.',
    image: '/src/assets/images/audience_policy_makers_1793515176396.jpg',
    primary: { label: 'View Frameworks', to: '/haomtgv' },
    secondary: [
      { label: 'Policy briefs', to: '/insights' },
    ],
    accent: 'red',
  },
];

const ACCENT_CHIP: Record<VisitorPathCard['accent'], string> = {
  red: 'bg-ls-red/10 text-ls-red',
  cyan: 'bg-ls-cyan/10 text-ls-cyan',
  navy: 'bg-ls-navy/10 text-ls-navy dark:bg-ls-white/10 dark:text-ls-white',
};

const ACCENT_ICON: Record<VisitorPathCard['accent'], string> = {
  red: 'text-ls-red',
  cyan: 'text-ls-cyan',
  navy: 'text-ls-navy dark:text-ls-white',
};

/**
 * Chapter-adjacent routing band (§8): three visually obvious pathways -
 * business problem → Solutions, understand → Builder/Model/Workforce,
 * work with us → Solutions/Contact. Every card branches deeper; no dead ends.
 */
export const VisitorPathsSection: React.FC<VisitorPathsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="paths" label="Choose your path" theme={theme} variant="secondary">
      <SectionHeading
        theme={theme}
        eyebrow="START HERE"
        title="Where Do You Want to Begin?"
        lead="Four ways in. Pick the one that matches why you are here. Each path branches into deeper content; none of them dead-end."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {VISITOR_PATHS.map((path, idx) => (
          <Reveal key={path.id} delay={idx * 0.06}>
            <article
              className="ripple-on h-full rounded-3xl overflow-hidden flex flex-col transition-all hover:-translate-y-0.5 shadow-none group bg-transparent border-none"
            >
              <div className="h-40 overflow-hidden relative">
                <img
                  src={path.image}
                  alt={path.intent}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                />
                <div className={`absolute inset-0 bg-gradient-to-t ${isLight ? 'from-ls-white/90' : 'from-[#070A40]'} to-transparent opacity-60`} />
                <div className="absolute top-4 left-4">
                  <span className={`inline-flex items-center gap-2 rounded-full px-2.5 py-1 font-body text-[10px] font-bold tracking-widest ${ACCENT_CHIP[path.accent]}`}>
                    {path.stage}
                  </span>
                </div>
              </div>

              <div className="p-6 flex flex-col flex-1">
                <div className="flex items-center justify-between gap-3 mb-3">
                  <span className={`font-body text-[10px] font-bold tracking-widest ${isLight ? 'text-ls-grey-dark' : 'text-[#9CA3AF]'}`}>
                    PATH {idx + 1}
                  </span>
                </div>

              <div>
                <h3 className={`font-display font-bold text-base sm:text-lg tracking-tight ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  {path.intent}
                </h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-[#9CA3AF]'}`}>
                  {path.body}
                </p>
              </div>

              <div className="mt-auto space-y-3 pt-6">
                <Link
                  to={path.primary.to}
                  className="ripple-on group inline-flex w-full items-center justify-between gap-2 rounded-2xl px-4 py-3 font-body text-xs font-bold tracking-widest transition-all bg-[#DC3641] text-white hover:bg-[#DC3641]/90"
                >
                  <span>{path.primary.label}</span>
                  <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
                </Link>
                <div className="flex flex-wrap gap-x-4 gap-y-1 pt-1">
                  {path.secondary.map((link) =>
                    link.to.startsWith('#') ? (
                      <a
                        key={link.label}
                        href={link.to}
                        className={`font-body text-[11px] font-bold tracking-wide hover:text-[#DC3641] transition-colors ${isLight ? 'text-ls-navy' : 'text-[#00BFFF]'}`}
                      >
                        {link.label} ↓
                      </a>
                    ) : (
                      <Link
                        key={link.label}
                        to={link.to}
                        className={`font-body text-[11px] font-bold tracking-wide hover:text-[#DC3641] transition-colors ${isLight ? 'text-ls-navy' : 'text-[#00BFFF]'}`}
                      >
                        {link.label} →
                      </Link>
                    ),
                  )}
                </div>
                </div>
              </div>
            </article>
          </Reveal>
        ))}
      </div>

      <div className="mt-6 flex flex-wrap items-center justify-center gap-2 rounded-2xl px-4 py-3 font-body text-xs bg-transparent border-none shadow-none">
        <MessageCircleQuestion className="w-4 h-4 text-[#DC3641]" aria-hidden="true" />
        <span className={isLight ? 'text-ls-navy' : 'text-white'}>Not sure which path fits?</span>
        <Link to="/ask" className="font-bold tracking-wide text-[#00BFFF] hover:underline">
          Ask LightSpeed →
        </Link>
        <span className={isLight ? 'text-ls-grey-dark' : 'text-[#9CA3AF]'}>
          (answers from our published knowledge only)
        </span>
      </div>
    </HomeSection>
  );
};

export default VisitorPathsSection;
