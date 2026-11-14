import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, BookOpen, Download, Shield, Clock, Calendar } from 'lucide-react';
import { NewsletterSignup } from '../components/NewsletterSignup';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { CtaBand } from '../components/site/CtaBand';
import { SectionHeading } from '../components/site/SectionHeading';
import { Reveal } from '../components/Reveal';
import { PharosReaderModal } from '../components/PharosReaderModal';
import { Icon3D } from '../components/common';
import { insightCategories } from '../data/siteContent';
import { insightArticles, formatInsightDate } from '../data/insights';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

const FEATURED_WHITEPAPERS = [
  {
    id: 'w1',
    title: 'Agentic Enterprise Architecture & Governance v1.1',
    subtitle: 'Strategic Blueprint for Autonomous Operations',
    category: 'Research Whitepaper',
    readTime: '12 min read',
    date: 'October 2026',
    image: '/assets/images/whitepaper_a_cover_clean_1793817703115.avif',
    abstract: 'This foundational whitepaper establishes the canonical framework for deploying deterministic agentic workflows across complex enterprise environments while maintaining rigorous human sovereign control.',
    content: [
      'As organizations transition from passive software tools to autonomous agentic systems, the primary challenge shifts from capability to governance. LightSpeed Holdings has pioneered the H-A-O-M-T-G-V architecture to ensure every agent action is bounded, auditable, and aligned with human intent.',
      'Through in-house operational benchmarks and pilot workflows, we demonstrate how workflow collapsing streamlines multi-step processes without compromising compliance or data residency.',
      'The five-tier human approval matrix provides an uncompromised escalation pathway for strategic decisions, ensuring accountability remains firmly anchored to executive decision-makers.'
    ]
  },
  {
    id: 'w2',
    title: 'Self-Service Market Intelligence & SADC Economic Dynamics',
    subtitle: 'Data Residency and Regional Scale',
    category: 'Geostrategic Analysis',
    readTime: '9 min read',
    date: 'September 2026',
    image: '/assets/images/whitepaper_b_cover_clean_1793817739118.avif',
    abstract: 'An in-depth analysis of cross-border data residency requirements, economic integration, and the deployment of self-service intelligence platforms across developing markets.',
    content: [
      'Regional development requires localized intelligence infrastructure that respects sovereign data governance while leveraging cutting-edge machine learning models.',
      'Pharos Insights evaluates the architectural trade-offs between centralized hyperscale models and distributed edge deployment in resource-constrained environments.',
      'Our findings indicate that hybrid architectures paired with open-weight models deliver superior cost efficiency and regulatory compliance for institutional stakeholders.'
    ]
  }
];

interface InsightsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const InsightsPage: React.FC<InsightsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const [activeWhitepaper, setActiveWhitepaper] = useState<typeof FEATURED_WHITEPAPERS[0] | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  useEffect(() => {
    trackJourneyEvent({
      eventType: 'insight_view',
      contentType: 'index',
      journeyStage: 'consideration',
    });
  }, []);

  const filteredArticles = selectedCategory === 'All'
    ? insightArticles
    : insightArticles.filter((article) => article.topic === selectedCategory || article.category === selectedCategory);

  const cardBg = isLight
    ? 'bg-ls-white text-ls-navy shadow-sm'
    : 'bg-ls-navy/80 text-white shadow-xl';
  const secondaryText = isLight ? 'text-ls-grey-dark' : 'text-slate-300';
  const mutedText = isLight ? 'text-ls-grey-dark/80' : 'text-slate-400';

  return (
    <div className={`min-h-screen ${isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-ls-navy-dark text-white'}`}>
      {/* Hero Section with Editorial Visualization */}
      <section className={`relative overflow-hidden px-6 lg:px-12 pt-28 sm:pt-32 pb-14 ${isLight ? 'bg-ls-white' : 'bg-[#03061C]'}`}>
        {/* Background Atmosphere */}
        <div className="absolute inset-0 pointer-events-none select-none z-0">
          <div className={`absolute inset-0 ${
            isLight
              ? 'bg-ls-white'
              : 'bg-[#03061C]'
          }`} />
        </div>

        <div className="max-w-7xl mx-auto w-full space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-cyan-950/40 text-cyan-400 font-mono text-xs tracking-widest border border-cyan-800/30">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span>PHAROS INSIGHTS // RESEARCH HUB</span>
          </div>
          <h1 className={`text-3xl lg:text-5xl font-bold tracking-tight font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Evidence, Research &amp; the Agentic AI Canon
          </h1>
          <p className={`max-w-2xl text-base leading-relaxed ${secondaryText}`}>
            Original research, peer-reviewed methodology, and executive briefings on AI strategy, data residency, and governance, written for boards and grounded in production systems.
          </p>
        </div>
      </section>

      {/* OPERATING MODEL ARCHITECTURAL DISTINCTION BANNER */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto w-full pt-12 pb-6" aria-label="Operating Model Architecture Distinction">
        <div className={`rounded-3xl p-8 lg:p-10 transition-all relative overflow-hidden ${
          isLight
            ? 'bg-cyan-50/70 text-ls-navy shadow-sm'
            : 'bg-cyan-950/30 text-white shadow-xl'
        }`}>
          {/* Subtle Architecture Visual Backdrop */}
          <div className="absolute right-0 top-0 bottom-0 w-1/2 pointer-events-none select-none opacity-10 dark:opacity-20 z-0 hidden lg:block">
            <img
              src="/assets/images/pharos_canonical_architecture_1793817675241.avif"
              alt="Canonical Agentic Architecture Hierarchy"
              className="w-full h-full object-cover object-left filter saturate-120"
              loading="lazy"
            />
            <div className={`absolute inset-0 ${
              isLight
                ? 'bg-gradient-to-r from-cyan-50 via-cyan-50/70 to-transparent'
                : 'bg-gradient-to-r from-[#03061C] via-[#03061C]/80 to-transparent'
            }`} />
          </div>

          <div className="relative z-10">
            <div className="flex flex-wrap items-center gap-2.5 mb-4">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
              <span className="font-mono text-xs font-bold tracking-widest text-cyan-700 dark:text-cyan-400 uppercase">
                OPERATING ARCHITECTURE // CANONICAL DISTINCTION
              </span>
            </div>

            <h2 className={`text-2xl lg:text-3xl font-bold font-display tracking-tight mb-3 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
              LightSpeed Internal Reference Model vs. Client Implementation Framework
            </h2>
            <p className={`text-sm leading-relaxed max-w-4xl mb-8 ${secondaryText}`}>
              Pharos thought leadership documents the empirical research and operational findings of LightSpeed&apos;s internal AI-native company. We maintain a strict boundary between our in-house reference architecture and client venture deployments.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Model 1: Internal Reference Model */}
            <div className={`rounded-2xl p-6 flex flex-col justify-between ${
              isLight ? 'bg-ls-white shadow-sm' : 'bg-slate-900/90 shadow-lg'
            }`}>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Icon3D name="users" size="xs" />
                    <span className="font-mono text-xs font-bold tracking-wider text-cyan-600 dark:text-cyan-400 uppercase">
                      INTERNAL REFERENCE MODEL
                    </span>
                  </div>
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-cyan-500/10 text-cyan-600 dark:text-cyan-300">
                    Live In-House
                  </span>
                </div>
                <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  89 AI Agents + 1 Human CEO
                </h3>
                <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
                  LightSpeed&apos;s internal operating structure is a live, stress-tested benchmark comprising <strong>90 canonical operating roles</strong> (89 specialized AI agents and 1 Human CEO) across 20 functional departments.
                </p>
                <ul className={`space-y-2 text-xs pt-2 ${secondaryText}`}>
                  <li className="flex items-start gap-2">
                    <span className="text-cyan-500 font-bold shrink-0">✓</span>
                    <span><strong>Human Sovereign Authority:</strong> The Human CEO retains exclusive sign-off on Tier 4 constitutional, financial, and irreversible actions.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-cyan-500 font-bold shrink-0">✓</span>
                    <span><strong>Empirical Laboratory:</strong> All 9 Pharos research briefs examine the real-world mechanics, task queues, and failure modes of this in-house fleet.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-cyan-500 font-bold shrink-0">✓</span>
                    <span><strong>Deterministic Gate:</strong> Five-tier approval matrix enforced in code with SHA-256 sealed audit trails.</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Model 2: Client Implementation Framework */}
            <div className={`rounded-2xl p-6 flex flex-col justify-between ${
              isLight ? 'bg-ls-red/10 shadow-sm' : 'bg-slate-900/90 shadow-lg'
            }`}>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Icon3D name="orchestration" size="xs" />
                    <span className="font-mono text-xs font-bold tracking-wider text-ls-red uppercase">
                      CLIENT IMPLEMENTATION MODEL
                    </span>
                  </div>
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-ls-red/10 text-ls-red">
                    Configurable &amp; Scalable
                  </span>
                </div>
                <h3 className={`text-xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  Configurable AI Agent Teams (1 to N+)
                </h3>
                <p className={`text-xs sm:text-sm leading-relaxed ${secondaryText}`}>
                  For enterprise and institutional partners, LightSpeed builds and deploys <strong>modular, right-sized AI agent teams</strong> that scale dynamically according to specific business goals, operational complexity, and workload.
                </p>
                <ul className={`space-y-2 text-xs pt-2 ${secondaryText}`}>
                  <li className="flex items-start gap-2">
                    <span className="text-ls-red font-bold shrink-0">✓</span>
                    <span><strong>No Fixed-Size Mandate:</strong> Clients are never required to adopt 90 roles, 89 agents, or an arbitrary fixed-size workforce.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-ls-red font-bold shrink-0">✓</span>
                    <span><strong>Scalable Governance:</strong> The identical five-tier approval matrix and human sovereign control apply whether running 1 agent or 50.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-ls-red font-bold shrink-0">✓</span>
                    <span><strong>Strict ROI Evaluation:</strong> Governed by transparent evaluation criteria: cycle time, operating expense, and defect elimination.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>



      {/* Featured Whitepaper Spotlight */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto w-full py-10">
        <div className="mb-6">
          <span className="text-xs font-semibold uppercase tracking-widest text-cyan-600 dark:text-cyan-400">FOUNDATIONAL RESEARCH</span>
          <h2 className={`text-2xl font-bold mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>Featured Whitepapers</h2>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {FEATURED_WHITEPAPERS.map((wp) => (
            <div
              key={wp.id}
              className={`rounded-2xl overflow-hidden flex flex-col justify-between group transition-all duration-300 border ${
                isLight ? 'border-slate-200 hover:shadow-xl' : 'border-white/10 hover:border-cyan-500/40 hover:shadow-2xl'
              } ${cardBg}`}
            >
              <div>
                {/* 3D Academic Research Cover Artwork */}
                <div className="relative w-full aspect-[16/10] overflow-hidden bg-slate-950 border-b border-white/10">
                  <img
                    src={wp.image}
                    alt={`${wp.title} research publication cover`}
                    className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                    loading="lazy"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex items-end p-5">
                    <span className="text-[11px] font-mono font-bold tracking-widest text-cyan-300 uppercase px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/40 inline-flex items-center gap-2">
                      <Icon3D name={wp.id === 'w1' ? 'governance' : 'chart'} size="xs" />
                      {wp.category}
                    </span>
                  </div>
                </div>

                <div className="p-8 space-y-4">
                  <div className="flex items-center justify-between text-xs font-mono text-cyan-600 dark:text-cyan-400">
                    <span className="uppercase tracking-wider">{wp.date}</span>
                    <span>{wp.readTime}</span>
                  </div>

                  <h3 className={`text-2xl font-bold group-hover:text-cyan-500 dark:group-hover:text-cyan-300 transition-colors ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                    {wp.title}
                  </h3>

                  <p className={`text-sm font-medium ${mutedText}`}>
                    {wp.subtitle}
                  </p>

                  <p className={`text-sm leading-relaxed ${secondaryText}`}>
                    {wp.abstract}
                  </p>
                </div>
              </div>

              <div className={`px-8 py-5 flex items-center justify-between border-t ${
                isLight ? 'bg-ls-grey-light/50 border-slate-200' : 'bg-slate-950/80 border-white/10'
              }`}>
                <button
                  onClick={() => setActiveWhitepaper(wp)}
                  className="btn-milled btn-milled-primary px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 rounded-xl text-xs font-bold transition-all flex items-center gap-2 shadow-sm cursor-pointer active:scale-98"
                >
                  <Icon3D name="notepad" size="xs" /> Read Whitepaper
                </button>
                <span className={`text-xs font-mono ${mutedText}`}>Peer-Reviewed Canon</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Topics / Interactive Pillar Filter */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto w-full py-8" aria-label="Insight categories">
        <div className="mb-6">
          <span className="text-xs font-semibold uppercase tracking-widest text-cyan-600 dark:text-cyan-400">RESEARCH PILLARS</span>
          <h2 className={`text-2xl font-bold mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>What We Write About</h2>
        </div>
        <div className="flex flex-wrap gap-2.5">
          {['All', ...insightCategories].map((cat) => {
            const isSelected = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`btn-milled ${isSelected ? 'btn-milled-primary' : 'btn-milled-secondary'} px-4 py-2 rounded-full text-xs font-medium tracking-wider transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-ls-red text-white shadow-md font-bold'
                    : isLight
                    ? 'bg-ls-white text-ls-navy hover:bg-ls-grey-light shadow-sm'
                    : 'bg-slate-900 text-slate-200 hover:bg-slate-800'
                }`}
              >
                {cat === 'All' ? 'All Topics' : cat}
              </button>
            );
          })}
        </div>
      </section>

      {/* Latest Articles */}
      <section className="px-6 lg:px-12 max-w-7xl mx-auto w-full py-12">
        <div className="mb-8 flex items-center justify-between flex-wrap gap-4">
          <div>
            <span className="text-xs font-semibold uppercase tracking-widest text-cyan-600 dark:text-cyan-400">CANONICAL ESSAYS</span>
            <h2 className={`text-2xl font-bold mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
              Featured Articles &amp; Briefings {selectedCategory !== 'All' && `· ${selectedCategory}`}
            </h2>
          </div>
          <span className={`text-xs font-mono ${mutedText}`}>
            Showing {filteredArticles.length} of {insightArticles.length} publications
          </span>
        </div>

        {filteredArticles.length === 0 ? (
          <div className={`p-8 rounded-2xl text-center ${cardBg}`}>
            <p className="text-sm">No articles currently published under this category.</p>
            <button
              onClick={() => setSelectedCategory('All')}
              className="btn-milled btn-milled-primary mt-4 px-4 py-2 bg-ls-red text-white rounded-lg text-xs font-bold cursor-pointer"
            >
              Reset Filter
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-3 gap-6">
            {filteredArticles.map((article) => {
              // Contextual editorial thumbnail mapping based on topic/slug
              let thumbImage: string | null = null;
              if (article.slug === 'open-source-cost-architecture' || article.slug === 'dual-economy-ai-pricing') {
                thumbImage = '/assets/images/pharos_article_thumb_cost_1793817753722.avif';
              } else if (article.slug === 'five-tier-approval-matrix' || article.slug === 'evidence-ladder-honest-claims') {
                thumbImage = '/assets/images/pharos_article_thumb_gov_1793817768084.avif';
              } else if (article.slug === 'sadc-ai-opportunity' || article.slug === 'agentic-ai-african-governments' || article.slug === 'offline-first-ai-for-africa') {
                thumbImage = '/assets/images/pharos_article_thumb_sadc_1793817783127.avif';
              } else if (article.slug === 'inside-a-90-agent-company' || article.slug === 'digital-to-ai-native-transformation') {
                thumbImage = '/assets/images/agent_network_topology_1793816821318.avif';
              }

              return (
                <Link
                  key={article.slug}
                  to={`/insights/${article.slug}`}
                  className={`group rounded-2xl overflow-hidden h-full flex flex-col justify-between transition-all border ${
                    isLight ? 'border-slate-200 hover:shadow-lg' : 'border-white/10 hover:border-cyan-500/30 hover:shadow-xl'
                  } ${cardBg}`}
                >
                  <div>
                    {thumbImage && (
                      <div className="relative w-full aspect-[16/9] overflow-hidden bg-slate-950 border-b border-white/10">
                        <img
                          src={thumbImage}
                          alt={`${article.title} visual preview`}
                          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                          loading="lazy"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent flex items-end p-3">
                          <span className="font-mono text-[10px] font-bold text-cyan-300 uppercase px-2 py-0.5 rounded bg-black/60 backdrop-blur-sm">
                            {article.topic}
                          </span>
                        </div>
                      </div>
                    )}

                      <div className="p-6 space-y-3">
                        <div className="flex flex-wrap gap-2">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${
                            isLight ? 'bg-cyan-500/10 text-cyan-600 border border-cyan-500/20' : 'bg-cyan-950/50 text-cyan-400 border border-cyan-800'
                          }`}>
                            {article.topic}
                          </span>
                        </div>
                        <h3 className={`text-lg font-bold leading-snug group-hover:text-cyan-500 dark:group-hover:text-cyan-300 transition-colors ${
                          isLight ? 'text-ls-navy' : 'text-white'
                        }`}>
                          {article.title}
                        </h3>
                        <p className={`text-sm leading-relaxed ${secondaryText} line-clamp-3`}>
                          {article.dek}
                        </p>
                      </div>
                  </div>

                  <div className={`px-6 py-4 border-t flex items-center justify-between text-xs font-mono ${mutedText} ${
                    isLight ? 'bg-slate-50/50 border-slate-200' : 'bg-slate-950/40 border-white/5'
                  }`}>
                    <span>{formatInsightDate(article.publishedAt)} · {article.readMins} MIN</span>
                    <span className="inline-flex items-center gap-1 text-cyan-600 dark:text-cyan-400 font-semibold group-hover:translate-x-1 transition-transform">
                      Read Briefing →
                    </span>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </section>

      {/* Related Links */}
      <RelatedLinks
        theme={theme}
        links={[
          { to: '/what-we-do', label: 'What We Do' },
          { to: '/haomtgv', label: 'HAOMTGV Architecture' },
          { to: '/solutions', label: 'Solutions' },
          { to: '/sectors', label: 'Sectors' },
        ]}
      />

      {/* Reader Modal */}
      <PharosReaderModal
        publication={activeWhitepaper}
        isOpen={!!activeWhitepaper}
        onClose={() => setActiveWhitepaper(null)}
        theme={theme}
      />

      <CtaBand theme={theme} onRequestBriefing={onRequestBriefing} />
    </div>
  );
};

export default InsightsPage;
