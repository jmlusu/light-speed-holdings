import React from 'react';
import { HeroSection } from '../components/HeroSection';
import {
  HAOMTGVSection,
  AICompanyBuilderSection,
  WorkforceSection,
  SolutionsSection,
  UseCasesSection,
  InsightsSection,
  AboutSection,
  BriefingSection,
  VisitorPathsSection,
} from '../components/home';
import { FaqSection } from '../components/site/FaqSection';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => (
  <div className="relative">
    {/*
     * AGENT TEAM NARRATIVE - HomePage
     * Content fidelity governed by:
     *   - content-writer    | hero copy, visitor pathways, CTA messaging
     *   - registry-owner    | sector/solution evidence, KPI metrics
     *   - reviewer          | MASTER_SPEC compliance, honesty badges
     *   - researcher        | evidence verification against source data
     *   - dashboard-owner   | conversion metrics, engagement tracking
     * Last audited: 2026-10-18
     */}
    {/* MASTER_SPEC §19 static fallback: mist/slate backdrop in a zero-z layer;
        content uses z-10 so it stacks above the fixed bg. */}
    <div className="fixed inset-0 z-0 pointer-events-none bg-[#F7F8F9] dark:bg-[#121518]" aria-hidden="true" />

    <div className="relative z-10 lg:pl-16">
      {/* 1. Orientation + 2. Core Proposition */}
      <HeroSection theme={theme} onRequestBriefing={onRequestBriefing} />
      {/* §8 Routing: three major visitor pathways */}
      <VisitorPathsSection theme={theme} />
      {/* 3. H-A-O-M-T-G-V operating philosophy */}
      <HAOMTGVSection theme={theme} />
{/* 4. Solutions grid with status chips */}
      <section
        className={`py-24 sm:py-32 md:py-36 bg-ls-gray-light dark:bg-ls-navy/50`}
        aria-label="Solutions grid"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight font-display text-ls-navy">
              Practical Business Outcomes
            </h2>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
            {homeCopy.solutionsGrid.map((solution) => (
              <div
                key={solution.id}
                className="rounded-3xl p-5 border flex flex-col gap-3 group hover:shadow-xl transition-shadow"
              >
                <StatusBadge status={solution.status} theme={theme} />
                <h3 className="font-display font-bold text-base tracking-tight">
                  {solution.title}
                </h3>
                <p className="text-sm sm:text-base leading-relaxed text-ls-grey-dark/60">
                  {solution.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5. Pharos teaser — 3 ArticleCards with CategoryChips */}
      <section
        className={`py-24 sm:py-32 md:py-36 bg-ls-white dark:bg-ls-navy`}
        aria-label="Pharos teaser"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {homeCopy.pharosTeaser.map((article) => (
              <ArticleCard
                key={article.id}
                theme={theme}
                title={article.title}
                description={article.excerpt}
                category={article.category}
                ctaText="Read full article"
                ctaUrl={`/article/${article.slug}`}
                onRequestBriefing={onRequestBriefing}
              />
            ))}
          </div>
        </div>
      </section>

      {/* 6. CTABand at bottom */}
      <CtaBand
        theme={theme}
        title="Start a Conversation"
        text="Tell us where your organisation is today. We will be honest about whether we can help, and exactly what it takes to start."
        ctaLabel="Start a Conversation"
        ctaTo="/contact"
        onRequestBriefing={onRequestBriefing}
        ctaLevel="primary"
      />
    </div>
    </div>
  </div>
);

export default HomePage;
