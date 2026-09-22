import React from 'react';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { events } from '../data/siteContent';

interface EventsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /events — speaking engagements, workshops, panels, webinars, and podcasts.
 * Each event shows title, type, description, and date/status.
 */
export const EventsPage: React.FC<EventsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  const typeColorMap: Record<string, string> = {
    'Executive Briefing': 'border-ls-red/40 bg-ls-red/10 text-ls-red',
    'Workshop': 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan',
    'Policy': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Webinar': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Panel': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
    'Podcast': 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text',
  };

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="SPEAKING & EVENTS"
        title="Invite LightSpeed to Speak"
        lead="Conferences, executive briefings, webinars, panels, workshops, and podcasts."
      />

      <section
        id="events"
        aria-labelledby="events-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-4"
      >
        <SectionHeading
          theme={theme}
          eyebrow="ENGAGEMENTS"
          title="Upcoming & Past Events"
          lead="LightSpeed executives speak on agentic AI governance, AI-native transformation, and African AI policy at conferences, workshops, and private briefings worldwide."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {events.map((event, idx) => (
            <Reveal key={event.id} delay={(idx % 2) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border flex flex-col ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-black tracking-widest text-ls-red">
                    {event.id}
                  </span>
                  <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 font-body text-[9px] font-bold tracking-widest ${
                    typeColorMap[event.type] || 'border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text'
                  }`}>
                    {event.type}
                  </span>
                </div>
                <h3 className="mt-4 font-display font-bold text-lg sm:text-xl tracking-tight">
                  {event.title}
                </h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {event.description}
                </p>
                <div className={`mt-auto pt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
                }`}>
                  <span className={`text-[11px] font-body font-bold tracking-widest ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    {event.date || 'TBD'}
                  </span>
                  <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Want LightSpeed at Your Next Event?"
        text="Whether it is a conference keynote, executive briefing, or private workshop — we bring evidence-led, honest perspectives on agentic AI and AI-native transformation."
        ctaLabel="Request a Speaker"
      />
    </>
  );
};

export default EventsPage;
