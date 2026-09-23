import React from 'react';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { resources } from '../data/siteContent';

interface ResourcesPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /resources — library of white papers, reports, frameworks, and playbooks.
 * Each resource card carries its type badge and a download link.
 */
export const ResourcesPage: React.FC<ResourcesPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  const typeColorMap: Record<string, string> = {
    'White Paper': 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
    'Executive Brief': 'border-ls-red/40 bg-ls-red/10 text-ls-red',
    'Research Report': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Framework': 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
    'Playbook': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Checklist': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Template': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Presentation': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Case Study': 'border-ls-red/40 bg-ls-red/10 text-ls-red',
  };

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="RESOURCES"
        title="White Papers, Reports & Frameworks"
        lead="A library of resources that help you understand and evaluate AI-native enterprise transformation."
      />

      <section
        id="resources"
        aria-labelledby="resources-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-4"
      >
        <SectionHeading
          theme={theme}
          eyebrow="LIBRARY"
          title="Downloadable Assets"
          lead="Every resource carries its honest status — proven, pilot, fieldable, or development."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resources.map((resource, idx) => (
            <Reveal key={resource.id} delay={(idx % 3) * 0.06}>
              <button
                type="button"
                onClick={() => onRequestBriefing?.(`Resource request: ${resource.title}`)}
                className={`w-full text-left rounded-3xl p-6 sm:p-8 border flex flex-col h-full cursor-pointer transition-all hover:scale-[1.01] ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
                aria-label={`${resource.downloadLabel}: ${resource.title}`}
              >
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-black tracking-widest text-ls-red">
                    {resource.id}
                  </span>
                  <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 font-body text-[9px] font-bold tracking-widest ${
                    typeColorMap[resource.type] || 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text'
                  }`}>
                    {resource.type}
                  </span>
                </div>
                <h3 className="mt-4 font-display font-bold text-lg sm:text-xl tracking-tight">
                  {resource.title}
                </h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {resource.description}
                </p>
                <div className={`mt-auto pt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
                }`}>
                  <span className={`text-[11px] font-body font-bold tracking-widest ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    {resource.downloadLabel}
                  </span>
                  <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
                </div>
              </button>
            </Reveal>
          ))}
        </div>
      </section>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/insights', label: 'Insights' },
          { to: '/news', label: 'News' },
          { to: '/events', label: 'Events' },
        ]}
      />

      <CtaBand
        theme={theme}
        title="Need the Right Resource for Your Situation?"
        text="Not sure which framework or report matches your needs? We can point you to the right starting point — no obligations, just honest guidance."
        ctaLabel="Request a Briefing"
        onRequestBriefing={onRequestBriefing}
      />
    </>
  );
};

export default ResourcesPage;
