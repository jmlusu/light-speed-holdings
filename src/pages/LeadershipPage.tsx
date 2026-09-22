import React from 'react';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { TONE_STYLES } from '../data/siteContent';
import { leadership, advisoryNetwork } from '../data/siteContent';

interface LeadershipPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const LeadershipPage: React.FC<LeadershipPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <main>
      <PageIntro
        theme={theme}
        eyebrow="LEADERSHIP"
        title="Human Credibility Behind the AI-Native Company"
        lead="An AI-native company is only as trustworthy as the humans directing it. Our leadership team brings executive-level experience across strategy, data, policy, and technology — and every claim on this site is theirs to stand behind."
      />

      <SectionHeading
        theme={theme}
        eyebrow="THE TEAM"
        title="Leadership"
        lead="Honest, brief profiles — not hagiography. Experience, expertise, and verifiable credentials."
      />

      <div className="px-4 sm:px-8 max-w-7xl mx-auto w-full pb-24 space-y-16">
        {/* ── Leadership profiles ─────────────────────── */}
        {leadership.map((person, index) => (
          <Reveal key={person.id} delay={index * 0.1}>
            <div
              className={`rounded-3xl border p-6 sm:p-8 ${
                isLight
                  ? 'bg-ls-white border-ls-grey-dark/20'
                  : 'bg-ls-navy/50 border-ls-white/10'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-start gap-6">
                {/* Identity block */}
                <div className="sm:w-64 flex-shrink-0 space-y-3">
                  <h3
                    className={`text-2xl font-black tracking-tight font-display ${
                      isLight ? 'text-ls-navy' : 'text-ls-white'
                    }`}
                  >
                    {person.name}
                  </h3>
                  <p
                    className={`text-sm font-bold tracking-wider uppercase ${
                      isLight ? 'text-ls-red' : 'text-ls-red'
                    }`}
                  >
                    {person.title}
                  </p>
                  <p
                    className={`text-sm leading-relaxed ${
                      isLight ? 'text-ls-grey-dark/70 font-medium' : 'text-ls-grey-light-text/70'
                    }`}
                  >
                    {person.role}
                  </p>
                </div>

                {/* Details grid */}
                <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-6">
                  {/* Experience */}
                  <div>
                    <h4
                      className={`text-xs font-bold tracking-widest uppercase mb-3 ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      Experience
                    </h4>
                    <ul className="space-y-2">
                      {person.experience.map((exp, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm leading-relaxed font-medium">
                          <span className="w-1.5 h-1.5 rounded-full bg-ls-red mt-2 flex-shrink-0" aria-hidden="true" />
                          {exp}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Expertise */}
                  <div>
                    <h4
                      className={`text-xs font-bold tracking-widest uppercase mb-3 ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      Expertise
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {person.expertise.map((skill, i) => (
                        <span
                          key={i}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full border text-[11px] font-bold tracking-wider ${
                            isLight
                              ? 'border-ls-cyan/30 bg-ls-cyan/10 text-ls-cyan'
                              : 'border-ls-cyan/30 bg-ls-cyan/10 text-ls-cyan'
                          }`}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Education */}
                  <div>
                    <h4
                      className={`text-xs font-bold tracking-widest uppercase mb-3 ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      Education
                    </h4>
                    <p
                      className={`text-sm leading-relaxed font-medium ${
                        isLight ? 'text-ls-grey-dark/70' : 'text-ls-grey-light-text/70'
                      }`}
                    >
                      {person.education}
                    </p>
                  </div>

                  {/* Certifications */}
                  <div>
                    <h4
                      className={`text-xs font-bold tracking-widest uppercase mb-3 ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      Certifications & Publications
                    </h4>
                    <ul className="space-y-2">
                      {person.certifications.map((cert, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm leading-relaxed font-medium">
                          <HonestyBadge label={{ label: cert, tone: 'proven' }} />
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Organizations */}
                  <div className="sm:col-span-2">
                    <h4
                      className={`text-xs font-bold tracking-widest uppercase mb-3 ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      Organizations
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {person.organizations.map((org, i) => (
                        <span
                          key={i}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full border text-[11px] font-bold tracking-wider ${
                            isLight
                              ? 'border-ls-grey-dark/20 bg-ls-grey-light-text/5 text-ls-grey-dark'
                              : 'border-ls-white/10 bg-ls-white/5 text-ls-grey-light-text'
                          }`}
                        >
                          {org}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* LinkedIn */}
                  <div className="sm:col-span-2 pt-2">
                    <a
                      href={`https://${person.linkedIn}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-xs font-bold tracking-wider uppercase text-ls-red transition-colors cursor-pointer hover:underline"
                    >
                      View LinkedIn Profile
                      <ArrowRight className="w-3 h-3" aria-hidden="true" />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </Reveal>
        ))}

        {/* ── Advisory Network ────────────────────────── */}
        <Reveal delay={0.3}>
          <div>
            <SectionHeading
              theme={theme}
              eyebrow="ADVISORY NETWORK"
              title="The Network Behind the Team"
              lead="A small, focused advisory network — each member bringing focused capability to client engagements."
            />
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
              {advisoryNetwork.map((advisor, index) => (
                <div
                  key={advisor.name}
                  className={`rounded-3xl border p-6 ${
                    isLight
                      ? 'bg-ls-white border-ls-grey-dark/20'
                      : 'bg-ls-navy/50 border-ls-white/10'
                  }`}
                >
                  <h4
                    className={`text-lg font-black tracking-tight font-display ${
                      isLight ? 'text-ls-navy' : 'text-ls-white'
                    }`}
                  >
                    {advisor.name}
                  </h4>
                  <p
                    className={`text-xs font-bold tracking-wider uppercase mt-1 mb-3 ${
                      isLight ? 'text-ls-red' : 'text-ls-red'
                    }`}
                  >
                    {advisor.role}
                  </p>
                  <p
                    className={`text-sm leading-relaxed font-medium ${
                      isLight ? 'text-ls-grey-dark/70' : 'text-ls-grey-light-text/70'
                    }`}
                  >
                    {advisor.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </Reveal>
      </div>

      <CtaBand theme={theme} />
    </main>
  );
};

export default LeadershipPage;
