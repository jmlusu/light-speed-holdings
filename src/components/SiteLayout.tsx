import React, { useEffect, useRef } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { FloatingNav } from './FloatingNav';
import { SiteFooter } from './SiteFooter';
import { ExecutiveBriefingModal } from './ExecutiveBriefingModal';
import { BackToTop } from './BackToTop';
import { useSite } from '../site-context';
import { trackJourneyEvent, stageForRoute } from '../hooks/useJourneyEvents';
import { scrollToHash } from '../hooks/useSmoothScroll';
import { getInsightArticle } from '../data/insights';
import { applyPageMeta } from '../lib/seo';

const ROUTE_META: Record<string, { title: string; description: string }> = {
  '/': {
    title: 'LightSpeed Holdings Limited™ | AI-Native Company Builder',
    description:
      'We build AI-native companies. LightSpeed Holdings designs and operates governed agentic operating models in Malawi, across SADC, and beyond.',
  },
  '/what-we-do': {
    title: 'What We Do | LightSpeed Holdings Limited™',
    description:
      'Strategy, AI, and execution: how LightSpeed designs and operates governed AI-native operating models for organisations in Southern Africa.',
  },
  '/haomtgv': {
    title: 'H-A-O-M-T-G-V | LightSpeed Holdings Limited™',
    description:
      'The seven dimensions of LightSpeed’s governed agentic operating architecture: human authority, agents, orchestration, memory, tools, governance, and value.',
  },
  '/ai-assessment': {
    title: 'AI Readiness Assessment | LightSpeed Holdings Limited™',
    description:
      'A qualitative diagnostic across data maturity, infrastructure, governance, talent, and agentic workflow potential.',
  },
  '/faq': {
    title: 'Frequently Asked Questions | LightSpeed Holdings Limited™',
    description:
      'Honest answers about the AI company builder, evidence, data protection, and how to start — with registry citations.',
  },
  '/insights': {
    title: 'Pharos Insights | LightSpeed Holdings Limited™',
    description:
      'Research, policy analysis, and field notes on governed agentic operations from LightSpeed’s Pharos practice.',
  },
  '/about': {
    title: 'About | LightSpeed Holdings Limited™',
    description:
      'ASPIRE. ACT. ACHIEVE. Meet the company building AI-native enterprises from Lilongwe, Malawi for the SADC region.',
  },
  '/contact': {
    title: 'Contact | LightSpeed Holdings Limited™',
    description:
      'Start a qualifying conversation with LightSpeed Holdings about AI-native company building and governance.',
  },
  '/legal/privacy': {
    title: 'Privacy Policy | LightSpeed Holdings Limited™',
    description: 'How LightSpeed Holdings collects, uses, and safeguards data.',
  },
  '/legal/terms': {
    title: 'Terms of Service | LightSpeed Holdings Limited™',
    description: 'Terms governing use of the LightSpeed Holdings website and services.',
  },
};

const NOT_FOUND_META = {
  title: 'Page Not Found | LightSpeed Holdings Limited™',
  description: 'The page you requested does not exist or has moved.',
};

export const SiteLayout: React.FC = () => {
  const { pathname, hash } = useLocation();
  const { theme, onToggleTheme, onRequestBriefing, isBriefingOpen, briefingSummary, closeBriefing } = useSite();

  const lastPathnameRef = useRef(pathname);

  useEffect(() => {
    trackJourneyEvent({
      eventType: 'page_view',
      route: pathname,
      journeyStage: stageForRoute(pathname),
    });
  }, [pathname]);

  useEffect(() => {
    const articleMatch = pathname.match(/^\/insights\/([^/]+)\/?$/);
    const article = articleMatch ? getInsightArticle(articleMatch[1]) : undefined;

    if (article?.seo) {
      applyPageMeta({
        title: article.seo.title,
        description: article.seo.description,
        type: 'article',
        url: window.location.origin + pathname,
      });
    } else {
      const meta = ROUTE_META[pathname] ?? NOT_FOUND_META;
      applyPageMeta({
        title: meta.title,
        description: meta.description,
        type: 'website',
        url: window.location.origin + pathname,
      });
    }

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (hash) {
      // Hash target exists after commit (same-page section or mounted route content).
      const el = document.getElementById(hash.slice(1));
      if (el) {
        scrollToHash(hash);
      }
      // No element found: keep current position rather than jumping to top.
    } else {
      window.scrollTo({ top: 0, left: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    }

    if (lastPathnameRef.current === pathname) return;
    lastPathnameRef.current = pathname;
    const main = document.getElementById('main-content');
    if (main) {
      main.focus({ preventScroll: true });
    }
  }, [pathname, hash]);

  return (
    <div className="min-h-screen bg-[#F2F2F2] dark:bg-[#070A40] text-ls-navy dark:text-white relative overflow-hidden selection:bg-[#00BFFF] selection:text-[#070A40]">
      {/* Global Cinematic Atmosphere Backdrop */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden select-none">
        {/* Radial spotlight & navy gradient vignettes */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,_var(--tw-gradient-stops))] from-[#00BFFF]/10 via-[#070A40]/85 to-[#070A40]" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#070A40]/30 via-transparent to-[#070A40]/80" />
      </div>

      <div className="relative z-10 min-h-screen flex flex-col">
        <a href="#main-content" className="skip-link">
          Skip to content
        </a>

        <FloatingNav
          onRequestBriefing={onRequestBriefing}
          theme={theme}
          onToggleTheme={onToggleTheme}
        />

        <main id="main-content" tabIndex={-1} className="focus:outline-none flex-1">
          <Outlet />
        </main>

        <ExecutiveBriefingModal
          isOpen={isBriefingOpen}
          onClose={closeBriefing}
          prefillSummary={briefingSummary}
          theme={theme}
        />

        <BackToTop theme={theme} />
      </div>
    </div>
  );
};

export default SiteLayout;
