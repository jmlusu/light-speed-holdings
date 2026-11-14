import React, { useCallback, useEffect, useState } from 'react';
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom';
import { SiteContext } from './site-context';
import type { Theme } from './site-context';
import { SiteLayout } from './components/SiteLayout';
import { withSite } from './site-context';
import { HomePage } from './pages/HomePage';
import { WhatWeDoPage } from './pages/WhatWeDoPage';
import { AiAssessmentPage } from './pages/AiAssessmentPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { InsightsPage } from './pages/InsightsPage';
import { InsightArticlePage } from './pages/InsightArticlePage';
import { AboutPage } from './pages/AboutPage';
import { ContactPage } from './pages/ContactPage';
import { PrivacyPage } from './pages/PrivacyPage';
import { TermsPage } from './pages/TermsPage';
import { HaomtgvPage } from './pages/HAOMTGVPage';

import { FaqPage } from './pages/FaqPage';


const HomePageRoute = withSite(HomePage);
const WhatWeDoPageRoute = withSite(WhatWeDoPage);
const AiAssessmentPageRoute = withSite(AiAssessmentPage);
const InsightsPageRoute = withSite(InsightsPage);
const InsightArticlePageRoute = withSite(InsightArticlePage);
const AboutPageRoute = withSite(AboutPage);
const ContactPageRoute = withSite(ContactPage);
const PrivacyPageRoute = withSite(PrivacyPage);
const TermsPageRoute = withSite(TermsPage);
const HaomtgvPageRoute = withSite(HaomtgvPage);

const FaqPageRoute = withSite(FaqPage);



export const App: React.FC = () => {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('lightspeed_theme');
      if (saved === 'light' || saved === 'dark') return saved;
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
      }
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
        return 'light';
      }
    }
    return 'dark';
  });
  const [isBriefingOpen, setIsBriefingOpen] = useState<boolean>(false);
  const [briefingSummary, setBriefingSummary] = useState<string>('');

  useEffect(() => {
    localStorage.setItem('lightspeed_theme', theme);
    const root = document.documentElement;
    root.style.transition = 'background-color 400ms cubic-bezier(0.16, 1, 0.3, 1), color 400ms cubic-bezier(0.16, 1, 0.3, 1)';
    if (document.body) {
      document.body.style.transition = 'background-color 400ms cubic-bezier(0.16, 1, 0.3, 1), color 400ms cubic-bezier(0.16, 1, 0.3, 1)';
    }

    if (theme === 'dark') {
      root.classList.add('dark');
      root.style.backgroundColor = '#070A40';
      if (document.body) {
        document.body.style.backgroundColor = '#070A40';
        document.body.style.color = '#FFFFFF';
      }
    } else {
      root.classList.remove('dark');
      root.style.backgroundColor = '#F2F2F2';
      if (document.body) {
        document.body.style.backgroundColor = '#F2F2F2';
        document.body.style.color = '#070A40';
      }
    }
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const requestBriefing = useCallback((summary?: string) => {
    if (summary) setBriefingSummary(summary);
    setIsBriefingOpen(true);
  }, []);

  const closeBriefing = useCallback(() => {
    setIsBriefingOpen(false);
  }, []);

  const [router] = useState(() =>
    createBrowserRouter([
      {
        path: '/',
        element: <SiteLayout />,
        children: [
          { index: true, element: <HomePageRoute /> },
          { path: 'what-we-do', element: <WhatWeDoPageRoute /> },
          { path: 'ai-company-builder', element: <Navigate to="/what-we-do" replace /> },
          { path: 'haomtgv', element: <HaomtgvPageRoute /> },
          { path: 'solutions', element: <Navigate to="/what-we-do" replace /> },
          { path: 'sectors', element: <Navigate to="/what-we-do" replace /> },
          { path: 'sectors/:slug', element: <Navigate to="/what-we-do" replace /> },
          { path: 'use-cases', element: <Navigate to="/what-we-do" replace /> },
          { path: 'use-cases/:slug', element: <Navigate to="/what-we-do" replace /> },
          { path: 'ai-assessment', element: <AiAssessmentPageRoute /> },
          { path: 'faq', element: <FaqPageRoute /> },
          { path: 'faqs', element: <Navigate to="/faq" replace /> },
          { path: 'insights', element: <InsightsPageRoute /> },
          { path: 'insights/:slug', element: <InsightArticlePageRoute /> },

          { path: 'about', element: <AboutPageRoute /> },
          { path: 'who-we-are', element: <Navigate to="/about" replace /> },
          { path: 'contact', element: <ContactPageRoute /> },
          { path: 'legal/privacy', element: <PrivacyPageRoute /> },
          { path: 'legal/terms', element: <TermsPageRoute /> },
          { path: 'privacy', element: <Navigate to="/legal/privacy" replace /> },
          { path: 'terms', element: <Navigate to="/legal/terms" replace /> },
          { path: 'architecture', element: <Navigate to="/what-we-do" replace /> },
          { path: 'build', element: <Navigate to="/what-we-do" replace /> },
          { path: 'offer-a', element: <Navigate to="/what-we-do" replace /> },
          { path: 'offer-b', element: <Navigate to="/what-we-do" replace /> },
          { path: 'offer-c', element: <Navigate to="/what-we-do" replace /> },
          { path: 'offer-d', element: <Navigate to="/what-we-do" replace /> },
          { path: 'offer-e', element: <Navigate to="/what-we-do" replace /> },
          { path: 'proof', element: <Navigate to="/what-we-do" replace /> },
          { path: 'ask', element: <Navigate to="/contact" replace /> },
          { path: '*', element: <NotFoundPage /> },
        ],
      },

    ])
  );

  return (
    <SiteContext.Provider
      value={{
        theme,
        onToggleTheme: toggleTheme,
        onRequestBriefing: requestBriefing,
        isBriefingOpen,
        briefingSummary,
        closeBriefing,
      }}
    >
      {/* OpenCode Governance Test */}
      {/* AI Studio acknowledges OpenCode change */}
      <RouterProvider router={router} />
    </SiteContext.Provider>
  );
};

export default App;

{/* OpenCode Initiated Change: 2026-10-29 13:45 */}
{/* AI Studio acknowledges OpenCode change */}
