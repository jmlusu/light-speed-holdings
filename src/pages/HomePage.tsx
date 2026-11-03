import React from 'react';
import { CtaBand } from '../components/site/CtaBand';
import { StatusBadge } from '../site/StatusBadge';
import { CategoryChip } from '../site/CategoryChip';
import { PathwayCard } from '../site/PathwayCard';
import { ArticleCard } from '../site/ArticleCard';
import { HAOMTGVSection } from '../components/home/HAOMTGVSection';
import { VisitorPathsSection } from '../components/home/VisitorPathsSection';
import homeCopy from '../data/homeCopy';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <div className="relative">
      {/* Hero: dark mode hero with light-trails road image, crimson pill CTA + outline play CTA */}
      <div
        className={`relative overflow-hidden min-h-screen lg:min-h-[700px] ${isLight
          ? 'bg-ls-white/95'
          : 'bg-ls-navy/80'}
        `}
        aria-hidden="true"
      >
        {/* Light-trails road image with dark overlay */}
        <img
          src="/brand/digital/light-trails-road.jpg"
          alt="Light trails road image"
          className="object-cover w-full h-full transition-opacity duration-500 ease-out"
        />
        <div
          className={`absolute inset-0 flex items-center justify-center pointer-events-none ${isLight
            ? 'bg-black/40'
            : 'bg-black/60'}
          `}
        />
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-8 py-20 sm:py-32">
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            <div>
              <span className="inline-flex items-center gap-1.5 rounded-full border px-2 py-1 font-body text-xs font-bold tracking-widest uppercase bg-ls-red/10 text-ls-red border-ls-red/30">
                AI-NATIVE OPERATING MODEL
              </span>
              <h1 className="mt-4 text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight font-display text-ls-white break-all">
                Powering the next<br />
                generation of<br />
                AI-native enterprises
              </h1>
              <p className="mt-6 text-lg sm:text-xl lg:text-2xl text-ls-white/90 max-w-xl leading-relaxed">
                A unified operating model for building, deploying, and governing AI agents at enterprise scale. From human intent to governed delivery, every layer is instrumented, observable, and under human authority.
              </p>
              <div className="mt-8 grid grid-cols-2 gap-4">
                {/* Crimson pill CTA */}
                <button
                  onClick={() => onRequestBriefing?.('Start a Conversation')}
                  className="rounded-full px-6 py-3 text-xs font-bold tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-colors hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-red focus-visible:ring-offset-2"
                  aria-label="Start a Conversation"
                >
                  Start a Conversation
                </button>
                {/* Outline play CTA */}
                <button
                  onClick={() => onRequestBriefing?.('Request an AI Readiness Assessment')}
                  className="rounded-full px-6 py-3 text-xs font-bold tracking-widest uppercase border border-ls-red text-ls-red shadow-lg shadow-ls-red/20 transition-colors hover:bg-ls-red/10 hover:scale-[1.01] active:scale-[0.99] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-red focus-visible:ring-offset-2"
                  aria-label="Request an AI Readiness Assessment"
                >
                  Request an AI Readiness Assessment
                </button>
              </div>
            </div>
            {/* Logo lockup over light-trails */}
            <div className="relative pt-20">
              <img
                src="/brand/logo/ls-white-gradient.svg"
                alt="LightSpeed logo"
                className="max-w-xs"
              />
              <p className="mt-2 text-xs font-body font-bold tracking-widest text-ls-red uppercase">LightSpeed Holdings</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTABand at top of content area */}
      <CtaBand
        theme={theme}
        title="Powering the next generation of AI-native enterprises"
        text="A unified operating model for building, deploying, and governing AI agents at enterprise scale. From human intent to governed delivery, every layer is instrumented, observable, and under human authority."
        ctaLabel="Start a Conversation"
        ctaTo="/contact"
        onRequestBriefing={onRequestBriefing}
        ctaLevel="primary"
      />

      {/* 2. "How would you like to engage" with 4 PathwayCards */}
      <section
        className={`py-24 sm:py-32 md:py-36 bg-ls-white dark:bg-ls-navy`}
        aria-label="Visitor pathways"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="text-center mb-12">
            <span className="inline-flex items-center gap-2 rounded-full border px-2.5 py-1 font-body text-[10px] font-bold tracking-widest text-ls-red/60">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M5 12.55a11 11 0 0 1 14.08 0" />
              </svg>
              Choose Your Path
            </span>
            <h2 className="mt-4 text-3xl sm:text-4xl font-black tracking-tight font-display text-ls-navy">
              How would you like to engage?
            </h2>
          </div>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {homeCopy.pathwayCards.map((card, idx) => (
              <PathwayCard
                key={card.id}
                theme={theme}
                {...card}
                onRequestBriefing={onRequestBriefing}
              />
            ))}
          </div>
          <div className="mt-8 text-center">
            <a
              href="/ask"
              className="inline-flex items-center gap-1.5 font-body text-xs font-bold tracking-widest uppercase text-ls-red transition-colors hover:text-ls-red/80"
            >
              Not sure which path fits? Ask LightSpeed
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M5 12.55a11 11 0 0 1 14.08 0" />
              </svg>
            </a>
          </div>
        </div>
      </section>

      {/* 3. H-A-O-M-T-G-V node diagram (responsive at 390px) */}
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
                {...article}
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
  );
};

export default HomePage;