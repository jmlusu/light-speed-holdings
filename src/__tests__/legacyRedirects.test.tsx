/// <reference types="vitest" />
import React from 'react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import { createMemoryRouter, RouterProvider, type RouteObject } from 'react-router-dom';
import { readFileSync } from 'node:fs';
import { SiteContext } from '../site-context';
import { SiteLayout } from '../components/SiteLayout';
import { LegacyRedirect } from '../components/site/LegacyRedirect';
import { LEGACY_REDIRECTS } from '../lib/legacyRedirects';

vi.mock('../components/FloatingNav', () => ({ FloatingNav: () => <div /> }));
vi.mock('../components/ExecutiveBriefingModal', () => ({ ExecutiveBriefingModal: () => null }));
vi.mock('../components/BackToTop', () => ({ BackToTop: () => null }));

const contextValue = {
  theme: 'dark' as const,
  onToggleTheme: () => {},
  onRequestBriefing: () => {},
  isBriefingOpen: false,
  briefingSummary: '',
  closeBriefing: () => {},
};

const livePaths = [
  '/', '/what-we-do', '/haomtgv', '/ai-assessment', '/faq', '/insights',
  '/insights/open-source-cost-architecture', '/about', '/contact',
  '/legal/privacy', '/legal/terms',
];

const testRoutes: RouteObject[] = [{
  path: '/',
  element: <SiteLayout />,
  children: [
    { index: true, element: <div data-testid="live-page">Live page: /</div> },
    ...livePaths.filter((p) => p !== '/').map((p) => ({
      path: p.replace(/^\//, ''),
      element: <div data-testid="live-page">Live page: {p}</div>,
    })),
    ...LEGACY_REDIRECTS.map(({ from, to, label }) => ({
      path: from,
      element: <LegacyRedirect to={to} label={label} />,
    })),
    { path: '*', element: <div data-testid="not-found">Not found</div> },
  ],
}];

function renderAt(path: string) {
  const router = createMemoryRouter(testRoutes, { initialEntries: [path] });
  const view = render(
    <SiteContext.Provider value={contextValue}>
      <RouterProvider router={router} />
    </SiteContext.Provider>,
  );
  return { router, ...view };
}

describe('legacy redirects are honest and single-hop', () => {
  beforeEach(() => {
    cleanup();
    document.head.innerHTML = '';
    document.title = '';
  });

  it.each(LEGACY_REDIRECTS.map((r) => [r.from, r.to, r.label] as const))(
    '%s resolves in one hop to %s with a visible moved notice',
    (from, to, label) => {
      const visit = `/${from.replace(':slug', 'sample-slug')}`;
      const { router } = renderAt(visit);
      expect(router.state.location.pathname).toBe(to);
      expect((router.state.location.state as { legacyFrom?: string }).legacyFrom).toBe(visit);
      expect(screen.getByTestId('live-page')).toHaveTextContent(`Live page: ${to}`);
      const notice = screen.getByRole('status');
      expect(notice).toHaveTextContent(visit);
      expect(notice).toHaveTextContent(label);
      expect(notice).toHaveTextContent(to);
      expect(screen.getByRole('link', { name: to })).toHaveAttribute('href', to);
    },
  );

  it('keeps the destination SEO title (applyPageMeta) intact after the redirect', () => {
    renderAt('/ask');
    expect(document.title).toBe('Contact | LightSpeed Holdings Limited™');
    expect(document.querySelector('link[rel="canonical"]')).toHaveAttribute('href', expect.stringContaining('/contact'));
  });

  it('does not break /insights/:slug — a known article stays on its own URL', () => {
    const routes: RouteObject[] = [{
      path: '/',
      element: <SiteLayout />,
      children: [{ path: 'insights/:slug', element: <div data-testid="article">Article</div> }],
    }];
    const router = createMemoryRouter(routes, { initialEntries: ['/insights/open-source-cost-architecture'] });
    render(<SiteContext.Provider value={contextValue}><RouterProvider router={router} /></SiteContext.Provider>);
    expect(router.state.location.pathname).toBe('/insights/open-source-cost-architecture');
    expect(screen.getByTestId('article')).toBeInTheDocument();
    expect(screen.queryByRole('status')).toBeNull();
  });

  it('App.tsx renders LEGACY_REDIRECTS (map is wired, not orphaned)', () => {
    const app = readFileSync('src/App.tsx', 'utf8');
    expect(app).toContain('LEGACY_REDIRECTS.map(');
    expect(app).toContain('<LegacyRedirect');
    expect(app).not.toContain('<Navigate');
    for (const { from } of LEGACY_REDIRECTS) {
      expect(LEGACY_REDIRECTS.filter((r) => r.from === from)).toHaveLength(1);
    }
  });

  it('homepage "Ask LightSpeed" CTA links to canonical /contact, not /ask', () => {
    const vp = readFileSync('src/components/home/VisitorPathsSection.tsx', 'utf8');
    expect(vp).toMatch(/<Link\s+to="\/contact"[^>]*>\s*Ask LightSpeed/);
    expect(vp).not.toContain('<Link to="/ask"');
  });
});
