import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { useCasesRegistry } from '../data/use-cases/registry';
import { sectors } from '../data/sector-registry';
import { insightArticles } from '../data/insights';

/**
 * Guards discoverability: every detail page that renders must be listed in
 * public/sitemap.xml, or crawling cannot reach it.
 */
const BASE = 'https://lightspeedholdings.vercel.app';
const sitemap = readFileSync(join(process.cwd(), 'public/sitemap.xml'), 'utf8');
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);

describe('sitemap coverage', () => {
  it('lists every use-case detail page', () => {
    for (const useCase of useCasesRegistry) {
      expect(locs, `missing ${useCase.slug}`).toContain(`${BASE}/use-cases/${useCase.slug}`);
    }
  });

  it('lists every sector detail page', () => {
    for (const sector of sectors) {
      expect(locs, `missing ${sector.id}`).toContain(`${BASE}/sectors/${sector.id}`);
    }
  });

  it('lists every insight article', () => {
    for (const article of insightArticles) {
      expect(locs, `missing ${article.slug}`).toContain(`${BASE}/insights/${article.slug}`);
    }
  });

  it('lists the HAOMTGV framework page', () => {
    expect(locs).toContain(`${BASE}/haomtgv`);
  });

  it('has no duplicate entries', () => {
    expect(new Set(locs).size).toBe(locs.length);
  });

  it('lists 44 URLs (21 pre-existing + 23 formerly orphaned)', () => {
    expect(locs).toHaveLength(44);
  });
});
