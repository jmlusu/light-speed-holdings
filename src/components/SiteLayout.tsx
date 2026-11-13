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
      document.title = `LIGHTSPEED HOLDINGS LIMITED™ | ASPIRE. ACT. ACHIEVE.`;
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

        {pathname !== '/' && <SiteFooter theme={theme} />}

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
