import React, { useCallback, useEffect, useState } from 'react';
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom';
import { SiteContext } from './site-context';
import type { Theme } from './site-context';
import { SiteLayout } from './components/SiteLayout';
import { withSite } from './site-context';
import { HomePage } from './pages/HomePage';
import { WhatWeDoPage } from './pages/WhatWeDoPage';
import { AiCompanyBuilderPage } from './pages/AiCompanyBuilderPage';
import { SolutionsPage } from './pages/SolutionsPage';
import { SectorsPage } from './pages/SectorsPage';
import { ProofPage } from './pages/ProofPage';
import { InsightsPage } from './pages/InsightsPage';
import { AboutPage } from './pages/AboutPage';
import { ContactPage } from './pages/ContactPage';
import { AskLightSpeed } from './components/AskLightSpeed';
import { PrivacyPage } from './pages/PrivacyPage';
import { TermsPage } from './pages/TermsPage';

const HomePageRoute = withSite(HomePage);
const WhatWeDoPageRoute = withSite(WhatWeDoPage);
const AiCompanyBuilderPageRoute = withSite(AiCompanyBuilderPage);
const SolutionsPageRoute = withSite(SolutionsPage);
const SectorsPageRoute = withSite(SectorsPage);
const ProofPageRoute = withSite(ProofPage);
const InsightsPageRoute = withSite(InsightsPage);
const AboutPageRoute = withSite(AboutPage);
const ContactPageRoute = withSite(ContactPage);
const PrivacyPageRoute = withSite(PrivacyPage);
const TermsPageRoute = withSite(TermsPage);

export const App: React.FC = () => {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('lightspeed_theme');
      if (saved === 'light' || saved === 'dark') return saved;
    }
    return 'dark';
  });
  const [isBriefingOpen, setIsBriefingOpen] = useState<boolean>(false);
  const [briefingSummary, setBriefingSummary] = useState<string>('');

  useEffect(() => {
    localStorage.setItem('lightspeed_theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.style.backgroundColor = '#121518';
      document.body.style.backgroundColor = '#121518';
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.style.backgroundColor = '#F7F8F9';
      document.body.style.backgroundColor = '#F7F8F9';
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
          { path: 'ai-company-builder', element: <AiCompanyBuilderPageRoute /> },
          { path: 'solutions', element: <SolutionsPageRoute /> },
          { path: 'sectors', element: <SectorsPageRoute /> },
          { path: 'proof', element: <ProofPageRoute /> },
          { path: 'insights', element: <InsightsPageRoute /> },
          { path: 'about', element: <AboutPageRoute /> },
          { path: 'contact', element: <ContactPageRoute /> },
          { path: 'ask', element: <AskLightSpeed /> },
          { path: 'legal/privacy', element: <PrivacyPageRoute /> },
          { path: 'legal/terms', element: <TermsPageRoute /> },
          { path: '*', element: <Navigate to="/" replace /> },
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
      <RouterProvider router={router} />
    </SiteContext.Provider>
  );
};

export default App;
