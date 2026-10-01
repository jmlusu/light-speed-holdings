import React, { useEffect, useRef } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { ThreeCanvas } from './ThreeCanvas';
import { FloatingNav } from './FloatingNav';
import { SiteFooter } from './SiteFooter';
import { ExecutiveBriefingModal } from './ExecutiveBriefingModal';
import { useSite } from '../site-context';

const ROUTE_TITLES: Record<string, string> = {
  '/': 'LIGHTSPEED HOLDINGS — Build the Intelligent Enterprise',
  '/about': 'About | LIGHTSPEED HOLDINGS',
  '/solutions': 'Solutions | LIGHTSPEED HOLDINGS',
  '/solutions/agentic-ai': 'Agentic AI | LIGHTSPEED HOLDINGS',
  '/solutions/digital-transformation': 'Digital Transformation | LIGHTSPEED HOLDINGS',
  '/solutions/data-intelligence': 'Data & Intelligence | LIGHTSPEED HOLDINGS',
  '/solutions/automation': 'Intelligent Automation | LIGHTSPEED HOLDINGS',
  '/solutions/strategy-advisory': 'Strategy & Advisory | LIGHTSPEED HOLDINGS',
  '/industries': 'Industries | LIGHTSPEED HOLDINGS',
  '/industries/government': 'Government | LIGHTSPEED HOLDINGS',
  '/industries/development': 'Development & Donor | LIGHTSPEED HOLDINGS',
  '/industries/financial-services': 'Financial Services | LIGHTSPEED HOLDINGS',
  '/industries/healthcare': 'Healthcare | LIGHTSPEED HOLDINGS',
  '/industries/agriculture': 'Agriculture | LIGHTSPEED HOLDINGS',
  '/ai-company-builder': 'AI Company Builder | LIGHTSPEED HOLDINGS',
  '/technology': 'Technology | LIGHTSPEED HOLDINGS',
  '/work': 'Work & Proof | LIGHTSPEED HOLDINGS',
  '/insights': 'Evidence, Research & the Agentic AI Canon | LIGHTSPEED HOLDINGS',
  '/offerings': 'Client Service Catalog | LIGHTSPEED HOLDINGS',
  '/evidence': 'Evidence & Method | LIGHTSPEED HOLDINGS',
  '/contact': 'Start a Conversation | LIGHTSPEED HOLDINGS',
  '/ask': 'Ask LightSpeed | LIGHTSPEED HOLDINGS',
  '/legal/privacy': 'Privacy Policy | LIGHTSPEED HOLDINGS',
  '/legal/terms': 'Terms of Service | LIGHTSPEED HOLDINGS',
  '/why': 'Why LightSpeed | LIGHTSPEED HOLDINGS',
  '/how-we-help': 'How We Help | LIGHTSPEED HOLDINGS',
  '/how-we-help/engagement': 'How We Help — Engagement | LIGHTSPEED HOLDINGS',
  '/process': 'Our Process | LIGHTSPEED HOLDINGS',
  '/geography': 'Geography | LIGHTSPEED HOLDINGS',
  '/leadership': 'Leadership | LIGHTSPEED HOLDINGS',
  '/faq': 'FAQ | LIGHTSPEED HOLDINGS',
  '/resources': 'Resources | LIGHTSPEED HOLDINGS',
  '/events': 'Events | LIGHTSPEED HOLDINGS',
  '/news': 'News | LIGHTSPEED HOLDINGS',
  '/careers': 'Careers | LIGHTSPEED HOLDINGS',
  '/deliverables': 'Deliverables | LIGHTSPEED HOLDINGS',
  '/outcomes': 'Outcomes | LIGHTSPEED HOLDINGS',
  '/partnerships': 'Partnerships | LIGHTSPEED HOLDINGS',
  '/trust': 'Trust | LIGHTSPEED HOLDINGS',
};

/**
 * Shared site shell rendered once for every routed page.
 * Owns the ambient canvas, fixed nav, footer, and the always-mounted
 * briefing modal; routed page content flows through <Outlet/>.
 * App.tsx remains the state owner and provides state via SiteContext.
 */
export const SiteLayout: React.FC = () => {
  const { pathname } = useLocation();
  const { theme, onToggleTheme, onRequestBriefing, isBriefingOpen, briefingSummary, closeBriefing } = useSite();

  const lastPathnameRef = useRef(pathname);

  useEffect(() => {
    document.title = ROUTE_TITLES[pathname] ?? 'LIGHTSPEED HOLDINGS';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, left: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });

    if (lastPathnameRef.current === pathname) return;

    lastPathnameRef.current = pathname;
    const main = document.getElementById('main-content');
    if (main) {
      main.focus({ preventScroll: true });
    }
  }, [pathname]);

  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to content
      </a>

      <ThreeCanvas theme={theme} />

      <FloatingNav
        onRequestBriefing={onRequestBriefing}
        theme={theme}
        onToggleTheme={onToggleTheme}
      />

      <main id="main-content" tabIndex={-1} className="pt-20 focus:outline-none">
        <Outlet />
      </main>

      <SiteFooter theme={theme} />

      <ExecutiveBriefingModal
        isOpen={isBriefingOpen}
        onClose={closeBriefing}
        prefillSummary={briefingSummary}
        theme={theme}
      />
    </>
  );
};

export default SiteLayout;
