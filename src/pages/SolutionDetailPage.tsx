import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { ArrowLink } from '../components/ArrowLink/ArrowLink';
import { DomainTile } from '../components/DomainTile/DomainTile';
import { TagChip } from '../components/TagChip/TagChip';
import { Reveal } from '../components/Reveal';
import { solutions } from '../data/siteContent';
import { getSectorsBySolution } from '../data/sector-registry';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

interface SolutionDetailPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

type Solution = (typeof solutions)[number];

const SPEC_QUESTIONS: Array<{ key: keyof Solution['spec']; label: string }> = [
  { key: 'problem', label: 'THE PROBLEM' },
  { key: 'audience', label: "WHO IT'S FOR" },
  { key: 'changes', label: 'WHAT CHANGES' },
  { key: 'builds', label: 'WHAT WE BUILD' },
  { key: 'evidence', label: 'EVIDENCE' },
];

type ToolTone = 'proven' | 'pilot' | 'fieldable' | 'development';

/**
 * Capabilities appear in two shapes across the registry: `{ title, desc }` and
 * `{ title, lead, proof }`, so both fields are optional. These readers narrow
 * the union without casting the whole array to `any`.
 */
const capabilityText = (capability: unknown): string | undefined => {
  if (typeof capability !== 'object' || capability === null) return undefined;
  const text = (capability as Record<string, unknown>).desc ??
    (capability as Record<string, unknown>).lead;
  return typeof text === 'string' && text.length > 0 ? text : undefined;
};

const capabilityProof = (
  capability: unknown,
): { label: string; tone: ToolTone } | undefined => {
  if (typeof capability !== 'object' || capability === null) return undefined;
  const proof = (capability as Record<string, unknown>).proof;
  if (typeof proof !== 'object' || proof === null) return undefined;
  const { label, tone } = proof as { label?: unknown; tone?: unknown };
  if (typeof label !== 'string') return undefined;
  if (tone !== 'proven' && tone !== 'pilot' && tone !== 'fieldable' && tone !== 'development') {
    return undefined;
  }
  return { label, tone };
};

/**
 * SolutionDetailPage - the per-solution view reached from /solutions.
 *
 * The slug comes from the router (`useParams`), never from a prop: the router
 * mounts route elements without props, so anything that reads `params.slug`
 * from props throws on first render.
 */
export const SolutionDetailPage: React.FC<SolutionDetailPageProps> = ({
  theme,
  onRequestBriefing,
}) => {
  const { slug = '' } = useParams<{ slug: string }>();
  const isLight = theme === 'light';
  const solution = solutions.find((entry) => entry.slug === slug);

  useEffect(() => {
    if (!solution) return;
    trackJourneyEvent({
      eventType: 'solution_view',
      solution: solution.slug,
      journeyStage: 'exploration',
      route: `/solutions/${solution.slug}`,
    });
  }, [solution]);

  if (!solution) {
    return (
      <div className="px-4 sm:px-8 max-w-3xl mx-auto w-full py-24 text-center">
        <h1
          className={`font-display text-2xl sm:text-3xl font-black tracking-tight ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}
        >
          Solution not found
        </h1>
        <p className={`mt-3 text-sm ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
          We could not find a solution at <code>/solutions/{slug}</code>.
        </p>
        <div className="mt-6 flex justify-center">
          <ArrowLink to="/solutions">All solutions</ArrowLink>
        </div>
      </div>
    );
  }

  const sectors = getSectorsBySolution(solution.slug);
  const related = solutions.filter((entry) => entry.slug !== solution.slug).slice(0, 4);

  return (
    <>
      <div className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-8">
        <ArrowLink to="/solutions">All solutions</ArrowLink>
      </div>

      <PageIntro
        theme={theme}
        eyebrow={solution.eyebrow}
        title={solution.title}
        lead={solution.description}
      />

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-6">
        <div className="flex flex-wrap items-center gap-3">
          <HonestyBadge label={solution.proof} />
          <span
            className={`font-body text-[10px] font-bold uppercase tracking-widest ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}
          >
            {solution.nav}
          </span>
        </div>
      </section>

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full py-12">
        <SectionHeading
          theme={theme}
          eyebrow="THE FIVE QUESTIONS"
          title="What this solves, and for whom"
          lead="Every claim below carries the same honesty status as the rest of the site. Nothing is rounded up."
        />
        <dl className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          {SPEC_QUESTIONS.map(({ key, label }) => {
            const value = solution.spec[key];
            if (!value) return null;
            return (
              <div
                key={key}
                className={`rounded-2xl border p-5 ${
                  isLight
                    ? 'border-ls-grey-dark/30 bg-ls-white/95'
                    : 'border-ls-white/15 bg-ls-navy/80'
                }`}
              >
                <dt className="font-body text-[9px] font-bold uppercase tracking-widest text-ls-red">
                  {label}
                </dt>
                <dd
                  className={`mt-2 text-sm leading-relaxed ${
                    isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                  }`}
                >
                  {value}
                </dd>
              </div>
            );
          })}
        </dl>
      </section>

      {solution.capabilities.length > 0 && (
        <section
          className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 border-t ${
            isLight ? 'border-ls-grey-dark/80' : 'border-ls-white/10'
          }`}
        >
          <SectionHeading
            theme={theme}
            eyebrow="CAPABILITIES"
            title="What the engagement builds"
            lead="Each capability is tagged with the evidence we can actually point to today."
          />
          <ul className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {solution.capabilities.map((capability) => {
              const text = capabilityText(capability);
              const proof = capabilityProof(capability);
              return (
                <li
                  key={capability.title}
                  className={`flex h-full flex-col rounded-2xl border p-5 ${
                    isLight
                      ? 'border-ls-grey-dark/30 bg-ls-white/95'
                      : 'border-ls-white/15 bg-ls-navy/80'
                  }`}
                >
                  <h3
                    className={`font-display text-sm font-bold tracking-tight ${
                      isLight ? 'text-ls-navy' : 'text-ls-white'
                    }`}
                  >
                    {capability.title}
                  </h3>
                  {text && (
                    <p
                      className={`mt-2 flex-1 text-xs leading-relaxed ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      {text}
                    </p>
                  )}
                  {proof && (
                    <div className="mt-4">
                      <TagChip label={proof.label} tone={proof.tone} size="sm" />
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {sectors.length > 0 && (
        <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full py-12">
          <SectionHeading
            theme={theme}
            eyebrow="SECTORS"
            title="Where this solution is deployed"
            lead="The same build pattern, applied to the operating constraints of each sector."
          />
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {sectors.map((sector) => (
              <Reveal key={sector.id}>
                <DomainTile
                  theme={theme}
                  title={sector.title}
                  description={sector.description}
                  to={`/sectors/${sector.id}`}
                />
              </Reveal>
            ))}
          </div>
        </section>
      )}

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full py-12">
        <SectionHeading
          theme={theme}
          eyebrow="OTHER SOLUTIONS"
          title="Continue through the portfolio"
          lead="Six domains, one operating model."
        />
        <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {related.map((entry) => (
            <DomainTile
              key={entry.slug}
              theme={theme}
              title={entry.title}
              description={entry.oneLiner}
              to={`/solutions/${entry.slug}`}
              badge={entry.proof.label}
            />
          ))}
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Talk about this solution"
        text="Tell us where your organisation is today. We will be honest about whether this fits, and exactly what it takes to start."
        ctaLabel="Start a Conversation"
        ctaTo="/contact"
        onRequestBriefing={onRequestBriefing}
        ctaLevel="primary"
      />

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/solutions', label: 'All Solutions' },
          { to: '/use-cases', label: 'Use Cases' },
          { to: '/insights', label: 'Insights' },
        ]}
      />
    </>
  );
};

export default SolutionDetailPage;
