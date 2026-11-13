import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { insightArticles } from '../data/insights';

/**
 * Guards discoverability: every page that renders must be listed in
 * public/sitemap.xml, and nothing that only redirects or 404s may be listed.
 *
 * The prototype IA retired the standalone solutions, sectors and use-cases
 * trees: those paths now redirect to /what-we-do in src/App.tsx, so a sitemap
 * entry for them would advertise a redirect to crawlers.
 */
const BASE = 'https://lightspeedholdings.vercel.app';
const sitemap = readFileSync(join(process.cwd(), 'public/sitemap.xml'), 'utf8');
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);

/** Routes that render a page in src/App.tsx. Redirect-only paths are excluded. */
const STATIC_ROUTES = [
  '/',
  '/what-we-do',
  '/haomtgv',
  '/ai-assessment',
  '/faq',
  '/insights',
  '/about',
  '/contact',
  '/legal/privacy',
  '/legal/terms',
];

/** Paths that exist in App.tsx only as <Navigate> redirects, or not at all. */
const RETIRED_PREFIXES = ['/pharos', '/venture-studio', '/ai-company-builder', '/solutions', '/sectors', '/use-cases'];

describe('sitemap coverage', () => {
  it('lists every insight article', () => {
    for (const article of insightArticles) {
      expect(locs, `missing ${article.slug}`).toContain(`${BASE}/insights/${article.slug}`);
    }
  });

  it('lists every live static route', () => {
    for (const route of STATIC_ROUTES) {
      expect(locs, `missing ${route}`).toContain(`${BASE}${route === '/' ? '/' : route}`);
    }
  });

  it('lists no path that only redirects or 404s', () => {
    for (const prefix of RETIRED_PREFIXES) {
      const offenders = locs.filter((loc) => loc === `${BASE}${prefix}` || loc.startsWith(`${BASE}${prefix}/`));
      expect(
        offenders,
        `Sitemap advertises ${prefix}, which App.tsx only redirects (or does not route). Remove it.`,
      ).toEqual([]);
    }
  });

  it('every listed static route is declared in src/App.tsx', () => {
    const app = readFileSync(join(process.cwd(), 'src/App.tsx'), 'utf8');

    const missing = STATIC_ROUTES.filter((route) => {
      if (route === '/') return !/\bindex:\s*true\b/.test(app);
      const rel = route.replace(/^\//, '');
      return !new RegExp(`path:\\s*['"]${rel}['"]`).test(app);
    });

    expect(
      missing,
      `Sitemap lists route(s) App.tsx does not declare: ${missing.join(', ')}`,
    ).toEqual([]);
  });

  it('lists the HAOMTGV framework page', () => {
    expect(locs).toContain(`${BASE}/haomtgv`);
  });

  it('has no duplicate entries', () => {
    expect(new Set(locs).size).toBe(locs.length);
  });

  it('lists exactly 19 URLs (10 static + 9 insight articles)', () => {
    expect(locs).toHaveLength(19);
  });
});
