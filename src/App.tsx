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
import { AskLightSpeed } from './components/AskLightSpeed';
import { ContactPage } from './pages/ContactPage';
import { PrivacyPage } from './pages/PrivacyPage';
import { TermsPage } from './pages/TermsPage';
import { WhyLightSpeedPage } from './pages/WhyLightSpeedPage';
import { HowWeHelpPage } from './pages/HowWeHelpPage';
import { ProcessPage } from './pages/ProcessPage';
import { GeographyPage } from './pages/GeographyPage';
import { LeadershipPage } from './pages/LeadershipPage';
import { FAQPage } from './pages/FAQPage';
import { ResourcesPage } from './pages/ResourcesPage';
import { EventsPage } from './pages/EventsPage';
import { NewsPage } from './pages/NewsPage';
import { CareersPage } from './pages/CareersPage';
import { DeliverablesPage } from './pages/DeliverablesPage';
import { OutcomesPage } from './pages/OutcomesPage';
import { PartnershipsPage } from './pages/PartnershipsPage';
import { TrustPage } from './pages/TrustPage';

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
const WhyLightSpeedPageRoute = withSite(WhyLightSpeedPage);
const HowWeHelpPageRoute = withSite(HowWeHelpPage);
const ProcessPageRoute = withSite(ProcessPage);
const GeographyPageRoute = withSite(GeographyPage);
const LeadershipPageRoute = withSite(LeadershipPage);
const FAQPageRoute = withSite(FAQPage);
const ResourcesPageRoute = withSite(ResourcesPage);
const EventsPageRoute = withSite(EventsPage);
const NewsPageRoute = withSite(NewsPage);
const CareersPageRoute = withSite(CareersPage);
const DeliverablesPageRoute = withSite(DeliverablesPage);
const OutcomesPageRoute = withSite(OutcomesPage);
const PartnershipsPageRoute = withSite(PartnershipsPage);
const TrustPageRoute = withSite(TrustPage);

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
           { path: 'ask', element: <AskLightSpeed /> },
           { path: 'contact', element: <ContactPageRoute /> },
           { path: 'legal/privacy', element: <PrivacyPageRoute /> },
           { path: 'legal/terms', element: <TermsPageRoute /> },
           { path: 'why', element: <WhyLightSpeedPageRoute /> },
           { path: 'how-we-help', element: <HowWeHelpPageRoute /> },
           { path: 'how-we-help/engagement', element: <HowWeHelpPageRoute /> },
           { path: 'process', element: <ProcessPageRoute /> },
           { path: 'geography', element: <GeographyPageRoute /> },
           { path: 'leadership', element: <LeadershipPageRoute /> },
           { path: 'faq', element: <FAQPageRoute /> },
           { path: 'resources', element: <ResourcesPageRoute /> },
           { path: 'events', element: <EventsPageRoute /> },
           { path: 'news', element: <NewsPageRoute /> },
           { path: 'careers', element: <CareersPageRoute /> },
           { path: 'deliverables', element: <DeliverablesPageRoute /> },
           { path: 'outcomes', element: <OutcomesPageRoute /> },
           { path: 'partnerships', element: <PartnershipsPageRoute /> },
           { path: 'trust', element: <TrustPageRoute /> },
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
