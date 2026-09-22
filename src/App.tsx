import React, { useCallback, useEffect, useState } from 'react';
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom';
import { SiteContext } from './site-context';
import type { Theme } from './site-context';
import { SiteLayout } from './components/SiteLayout';
import { withSite } from './site-context';
import { HomePage } from './pages/HomePage';
import { WhatWeDoPage } from './pages/WhatWeDoPage';
import { ProofPage } from './pages/ProofPage';
import { SolutionsPage } from './pages/SolutionsPage';
import { SolutionDetailPage } from './pages/SolutionDetailPage';
import { IndustriesPage } from './pages/IndustriesPage';
import { IndustryDetailPage } from './pages/IndustryDetailPage';
import { TechnologyPage } from './pages/TechnologyPage';
import { WorkPage } from './pages/WorkPage';
import { InsightsPage } from './pages/InsightsPage';
import { OfferingsPage } from './pages/OfferingsPage';
import { EvidencePage } from './pages/EvidencePage';
import { AboutPage } from './pages/AboutPage';
import { AiCompanyBuilderPage } from './pages/AiCompanyBuilderPage';
import { ContactPage } from './pages/ContactPage';
import { PrivacyPage } from './pages/PrivacyPage';
import { TermsPage } from './pages/TermsPage';
import { AthenaDashboard } from './pages/athena/Dashboard';
import { JobList } from './pages/athena/JobList';
import { JobDetail } from './pages/athena/JobDetail';
import { DocumentEditor } from './pages/athena/DocumentEditor';
import { AthenaLayout } from './components/athena/AthenaLayout';

const HomePageRoute = withSite(HomePage);
const WhatWeDoPageRoute = withSite(WhatWeDoPage);
const ProofPageRoute = withSite(ProofPage);
const SolutionsPageRoute = withSite(SolutionsPage);
const SolutionDetailPageRoute = withSite(SolutionDetailPage);
const IndustriesPageRoute = withSite(IndustriesPage);
const IndustryDetailPageRoute = withSite(IndustryDetailPage);
const TechnologyPageRoute = withSite(TechnologyPage);
const WorkPageRoute = withSite(WorkPage);
const InsightsPageRoute = withSite(InsightsPage);
const OfferingsPageRoute = withSite(OfferingsPage);
const EvidencePageRoute = withSite(EvidencePage);
const AboutPageRoute = withSite(AboutPage);
const AiCompanyBuilderPageRoute = withSite(AiCompanyBuilderPage);
const ContactPageRoute = withSite(ContactPage);
const PrivacyPageRoute = withSite(PrivacyPage);
const TermsPageRoute = withSite(TermsPage);

const AthenaDashboardRoute = AthenaDashboard;
const JobListRoute = JobList;
const JobDetailRoute = JobDetail;
const DocumentEditorRoute = DocumentEditor;

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
      document.documentElement.style.backgroundColor = '#060d16';
      document.body.style.backgroundColor = '#060d16';
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.style.backgroundColor = '#edf3f8';
      document.body.style.backgroundColor = '#edf3f8';
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
          { path: 'proof', element: <ProofPageRoute /> },
          { path: 'solutions', element: <Navigate to="/what-we-do" replace /> },
          { path: 'solutions/:slug', element: <SolutionDetailPageRoute /> },
          { path: 'industries', element: <Navigate to="/what-we-do" replace /> },
          { path: 'industries/:slug', element: <IndustryDetailPageRoute /> },
          { path: 'offerings', element: <Navigate to="/what-we-do" replace /> },
          { path: 'work', element: <Navigate to="/proof" replace /> },
          { path: 'evidence', element: <Navigate to="/proof" replace /> },
          { path: 'technology', element: <TechnologyPageRoute /> },
          { path: 'insights', element: <InsightsPageRoute /> },
          { path: 'about', element: <AboutPageRoute /> },
          { path: 'ai-company-builder', element: <AiCompanyBuilderPageRoute /> },
          { path: 'contact', element: <ContactPageRoute /> },
          { path: 'legal/privacy', element: <PrivacyPageRoute /> },
          { path: 'legal/terms', element: <TermsPageRoute /> },
          { path: '*', element: <Navigate to="/" replace /> },
        ],
      },
      {
        path: '/athena',
        element: <AthenaLayout />,
        children: [
          { index: true, element: <AthenaDashboardRoute /> },
          { path: 'jobs', element: <JobListRoute /> },
          { path: 'jobs/:id', element: <JobDetailRoute /> },
          { path: 'applications', element: <JobListRoute /> },
          { path: 'analytics', element: <AthenaDashboardRoute /> },
          { path: 'settings', element: <AthenaDashboardRoute /> },
          { path: 'documents', element: <DocumentEditorRoute documentType="resume" /> },
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
