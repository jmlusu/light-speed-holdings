import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Layers, MessageCircleQuestion, ShieldCheck, Target, type LucideIcon } from 'lucide-react';
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
  Icon: LucideIcon;
  primary: { label: string; to: string };
  secondary: { label: string; to: string }[];
  accent: 'red' | 'cyan' | 'navy';
}

/** §8 Homepage Routing Principle — the three major visitor pathways. */
const VISITOR_PATHS: VisitorPathCard[] = [
  {
    id: 'business-problem',
    stage: 'EXPLORATION',
    intent: 'I have a business problem',
    body: 'Start from the outcome you need. The solution framework maps common problems to what we ship, and each solution links to the sectors where it applies.',
    Icon: Target,
    primary: { label: 'Explore Solutions', to: '/solutions' },
    secondary: [
      { label: 'How we work', to: '/what-we-do' },
      { label: 'Browse sectors', to: '/sectors' },
    ],
    accent: 'red',
  },
  {
    id: 'understand',
    stage: 'AWARENESS',
    intent: 'I want to understand AI-native business',
    body: 'Walk the model itself: the operating model, the AI Company Builder lifecycle, and the 90-agent workforce that runs it day to day.',
    Icon: Layers,
    primary: { label: 'Explore the AI Company Builder', to: '/ai-company-builder' },
    secondary: [
      { label: 'Operating model', to: '#operating-model' },
      { label: '90-agent workforce', to: '#workforce' },
    ],
    accent: 'cyan',
  },
  {
    id: 'work-with-us',
    stage: 'INTENT',
    intent: 'I want to work with LightSpeed',
    body: 'Check the verified operating metrics first, then start a conversation — an executive briefing, an AI readiness assessment, or a direct enquiry.',
    Icon: ShieldCheck,
    primary: { label: 'View Proof', to: '/proof' },
    secondary: [{ label: 'Start a conversation', to: '/contact' }],
    accent: 'navy',
  },
];

const ACCENT_CHIP: Record<VisitorPathCard['accent'], string> = {
  red: 'bg-ls-red/10 text-ls-red border-ls-red/30',
  cyan: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/30',
  navy: 'bg-ls-navy/10 text-ls-navy border-ls-navy/30 dark:bg-ls-white/10 dark:text-ls-white dark:border-ls-white/25',
};

const ACCENT_ICON: Record<VisitorPathCard['accent'], string> = {
  red: 'text-ls-red',
  cyan: 'text-ls-cyan',
  navy: 'text-ls-navy dark:text-ls-white',
};

/**
 * Chapter-adjacent routing band (§8): three visually obvious pathways —
 * business problem → Solutions, understand → Builder/Model/Workforce,
 * work with us → Proof → Contact. Every card branches deeper; no dead ends.
 */
export const VisitorPathsSection: React.FC<VisitorPathsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="paths" label="Choose your path" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="START HERE"
        title="Where Do You Want to Begin?"
        lead="Three ways in — pick the one that matches why you are here. Each path branches into deeper content; none of them dead-end."
      />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {VISITOR_PATHS.map((path, idx) => (
          <Reveal key={path.id} delay={idx * 0.06}>
            <article
              className={`ripple-on h-full rounded-3xl p-6 border flex flex-col gap-4 transition-all hover:-translate-y-0.5 ${
                isLight
                  ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl'
                  : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl'
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <span className={`inline-flex items-center gap-2 rounded-full border px-2.5 py-1 font-body text-[10px] font-bold tracking-widest ${ACCENT_CHIP[path.accent]}`}>
                  <path.Icon className="w-3.5 h-3.5" aria-hidden="true" />
                  {path.stage}
                </span>
                <span className={`font-body text-[10px] font-bold tracking-widest ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  PATH {idx + 1}
                </span>
              </div>

              <div>
                <h3 className={`font-display font-bold text-base sm:text-lg tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  {path.intent}
                </h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {path.body}
                </p>
              </div>

              <div className="mt-auto space-y-3">
                <Link
                  to={path.primary.to}
                  className={`ripple-on group inline-flex w-full items-center justify-between gap-2 rounded-2xl px-4 py-3 font-body text-xs font-bold tracking-widest transition-all ${
                    isLight
                      ? 'bg-ls-navy text-ls-white hover:bg-ls-red'
                      : 'bg-ls-red text-ls-white hover:bg-ls-red/90'
                  }`}
                >
                  <span>{path.primary.label}</span>
                  <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
                </Link>
                <div className={`flex flex-wrap gap-x-4 gap-y-1 pt-1 border-t ${isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/15'}`}>
                  {path.secondary.map((link) =>
                    link.to.startsWith('#') ? (
                      <a
                        key={link.label}
                        href={link.to}
                        className={`font-body text-[11px] font-bold tracking-wide hover:text-ls-red transition-colors ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
                      >
                        {link.label} ↓
                      </a>
                    ) : (
                      <Link
                        key={link.label}
                        to={link.to}
                        className={`font-body text-[11px] font-bold tracking-wide hover:text-ls-red transition-colors ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
                      >
                        {link.label} →
                      </Link>
                    ),
                  )}
                </div>
              </div>
            </article>
          </Reveal>
        ))}
      </div>

      <div className={`mt-6 flex flex-wrap items-center justify-center gap-2 rounded-2xl border px-4 py-3 font-body text-xs ${
        isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy' : 'bg-ls-navy/80 border-ls-white/15 text-ls-grey-light-text'
      }`}>
        <MessageCircleQuestion className="w-4 h-4 text-ls-red" aria-hidden="true" />
        <span>Not sure which path fits?</span>
        <Link to="/ask" className="font-bold tracking-wide text-ls-red hover:underline">
          Ask LightSpeed →
        </Link>
        <span className={isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}>
          (answers from our published knowledge only)
        </span>
      </div>
    </HomeSection>
  );
};

export default VisitorPathsSection;
