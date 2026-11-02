import React from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { StatusBadge } from '@/components/StatusBadge/StatusBadge';
import { TagChip } from '@/components/TagChip/TagChip';
import { ArrowLink } from '@/components/ArrowLink/ArrowLink';
import { solutions, GOVERNANCE_SOLUTION } from '@/data/siteContent';
import { getSectorsBySolution } from '@/data/sector-registry';

interface SolutionDetailProps {
  params: { slug: string };
}

export const SolutionDetailPage: React.FC<SolutionDetailProps> = ({ params }) => {
  const { slug } = params;

  const solution = solutions.find((s) => s.slug === slug) || GOVERNANCE_SOLUTION;
  const isGovernance = slug === 'governance';

  // Compute theme-friendly class names
  let titleColor: string;
  let sectionBg: string;
  let borderColor: string;
  let ddColor: string;

  if (isGovernance || !solution) {
    titleColor = 'text-ls-white';
    sectionBg = 'bg-ls-navy/80';
    borderColor = 'border-ls-white/10';
    ddColor = 'text-ls-grey-light-text';
  } else {
    const isLight = !document.documentElement.classList.contains('dark');
    titleColor = isLight ? 'text-ls-navy' : 'text-ls-white';
    sectionBg = isLight ? 'bg-ls-white' : 'bg-ls-navy/80';
    borderColor = isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10';
    ddColor = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';
  }

  // If not found, show 404
  if (!solutions.some((s) => s.slug === slug) && !isGovernance) {
    return (
      <div className="min-h-screen flex items-center justify-center p-8">
        <h1 className="text-2xl font-bold">Solution not found</h1>
        <Link to="/solutions" className="text-ls-red mt-4">
          ← Back to Solutions
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <nav className="bg-ls-white/95 border-b border-ls-grey-dark/30 sticky top-0 z-10 dark:bg-ls-navy/80 dark:border-ls-white/15">
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="flex items-center justify-between h-16">
            <Link
              to="/solutions"
              className="flex items-center gap-2 text-ls-red font-bold tracking-widest uppercase text-xs"
            >
              <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              All Solutions
            </Link>
            <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
              {isGovernance ? 'GOVERNANCE' : solution.eyebrow || 'SOLUTIONS'}
            </span>
          </div>
        </div>
      </nav>

      <main className="px-4 sm:px-8 max-w-7xl mx-auto">
        {/* Hero section */}
        <section className="py-12 sm:py-16 border-b">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center gap-2 mb-4">
              <StatusBadge
                label={solution.proof.label}
                tone={solution.proof.tone}
                className="text-[10px] font-bold py-1 px-2"
              />
            </div>

            <h1 className={isGovernance ? 'text-3xl font-black' : 'text-3xl sm:text-4xl font-black tracking-tight font-display'}>
              {solution.title}
            </h1>

            <p className="text-lg sm:text-xl text-ls-grey-dark/60 mb-6">
              {solution.description}
            </p>
          </div>
        </section>

        {/* Body sections - spec questions */}
        <section className={sectionBg}>
          <div className="max-w-3xl mx-auto">
            <dl className="space-y-4">
              <div key="problem">
                <dt className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                  THE PROBLEM
                </dt>
                <dd
                  className={ddColor}
                >
                  {solution.spec?.problem || 'See solution overview for full details.'}
                </dd>
              </div>

              <div key="audience">
                <dt className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                  WHO IT'S FOR
                </dt>
                <dd className={ddColor}>
                  {solution.spec?.audience || ''}
                </dd>
              </div>

              <div key="changes">
                <dt className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                  WHAT CHANGES
                </dt>
                <dd className={ddColor}>
                  {solution.spec?.changes || ''}
                </dd>
              </div>

              <div key="builds">
                <dt className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                  WHAT WE BUILD
                </dt>
                <dd className={ddColor}>
                  {solution.spec?.builds || ''}
                </dd>
              </div>

              <div key="evidence">
                <dt className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                  EVIDENCE
                </dt>
                <dd className={ddColor}>
                  {solution.spec?.evidence || ''}
                </dd>
              </div>
            </dl>
          </div>
        </section>

        {/* TagChips + ArrowLink CTA */}
        <section className="py-8 sm:py-12 border-t">
          <div className="max-w-2xl mx-auto">
            <div className="flex flex-wrap gap-2">
              {['PROVEN', 'PILOT', 'FIELDABLE', 'FUTURE'].map((tone) => (
                <TagChip key={tone} label={tone} tone={tone.toLowerCase() as any} />
              ))}

              <div className="mt-4" />
            </div>

            <ArrowLink
              to="/contact"
              className="mt-4 w-full text-xs font-bold tracking-wider text-ls-red flex items-center justify-center gap-1"
            >
              Discuss This Solution <ArrowRight className="w-3.5 h-3.5" />
            </ArrowLink>
          </div>
        </section>

        {/* Related solutions grid */}
        <section className={sectionBg}>
          <div className="max-w-6xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-black tracking-tight font-display">
              Related Solutions
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
              {solutions
                .filter((s) => s.slug !== slug && s.slug !== 'governance')
                .slice(0, 6)
                .map((related) => (
                  <div
                    key={related.slug}
                    className="rounded-xl border p-4 hover:shadow-md transition-shadow"
                  >
                    <h3 className="font-bold text-base font-display sm:text-lg tracking-tight">
                      {related.title}
                    </h3>
                    <p className="text-sm text-ls-grey-dark/60 mt-1 line-clamp-2">
                      {related.description?.substring(0, 100)}...
                    </p>
                  </div>
                ))}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default SolutionDetailPage;
