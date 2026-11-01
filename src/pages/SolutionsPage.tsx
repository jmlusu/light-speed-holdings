import React, { useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { DomainTile } from '../components/DomainTile/DomainTile';
import { StatusBadge } from '../components/StatusBadge/StatusBadge';
import { CtaBand } from '../components/site/CtaBand';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { solutions, GOVERNANCE_SOLUTION } from '../data/siteContent';
import { getSectorsBySolution } from '../data/sector-registry';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

interface SolutionsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const SolutionsPage: React.FC<SolutionsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const { hash } = useLocation();

  useEffect(() => {
    const slug = hash.replace('#', '');
    if (!slug) return;
    trackJourneyEvent({
      eventType: 'solution_view',
      solution: slug,
      journeyStage: 'exploration',
      route: '/solutions',
    });
  }, [hash]);

  return (
    <>
      <h1 className="text-2xl font-bold">Solutions Page</h1>
      <section className="p-4">
        {solutions.map((sol, idx) => (
          <DomainTile
            key={sol.slug}
            title={sol.title}
            description={sol.description}
            to="/contact"
            theme={theme}
            badge={sol.proof.label?.includes('Proven') ? 'PROVEN' : 'FIELDABLE'}
          />
        ))}

        <DomainTile
          sol={GOVERNANCE_SOLUTION}
          title={GOVERNANCE_SOLUTION.title}
          description={GOVERNANCE_SOLUTION.description}
          to={GOVERNANCE_SOLUTION.to}
          theme={theme}
          badge="PROVEN"
        />
      </section>

      <section className="pt-8 border-t">
        <h2 className="text-xl font-bold">Explore Our Capabilities</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <DomainTile
            title="AI Company Builder"
            description="Build governed AI companies"
            to="/what-we-do"
            theme={theme}
            active
            badge="PROVEN"
          />
          <DomainTile
            title="Digital Presence"
            description="Mobile-first websites"
            to="/what-we-do"
            theme={theme}
          />
        </div>
      </section>

      <CtaBand theme={theme} />
      <RelatedLinks theme={theme} links={[{ to: '/insights', label: 'Insights' }]} />
    </>
  );
};

export default SolutionsPage;