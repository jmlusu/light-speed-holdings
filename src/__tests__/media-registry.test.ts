import { describe, it, expect } from 'vitest';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

/**
 * Media registry guard.
 *
 * `src/data/registries/media-registry.json` is the authoritative record of every
 * image the public site renders (origin, licence, disclosure). This suite keeps it
 * honest in four directions:
 *   1. the entry count is pinned, so an asset cannot be added or dropped silently;
 *   2. every image path referenced from site source resolves to a registry entry;
 *   3. every entry carries a usable origin, licence and kind;
 *   4. the file system agrees with the entry — `missing` means missing, and every
 *      other kind means the file is really under `public/`.
 *
 * Adding an image to the site therefore fails here until it is registered, and
 * registering a `missing` path fails once someone adds the file, forcing a real
 * origin/licence decision instead of leaving a placeholder in place.
 */

const ROOT = process.cwd();
const PUBLIC_DIR = join(ROOT, 'public');
const REGISTRY_PATH = join(ROOT, 'src', 'data', 'registries', 'media-registry.json');

const ALLOWED_KINDS = [
  'logo',
  'social-card',
  'illustration',
  'diagram',
  'photograph',
  'ai-generated',
  'missing',
] as const;

type AllowedKind = (typeof ALLOWED_KINDS)[number];

interface MediaAsset {
  id: string;
  path: string;
  kind: string;
  origin: string;
  licence: string;
  disclosure?: string;
  note?: string;
}

interface MediaRegistry {
  version: string;
  description: string;
  lastUpdated: string;
  assets: MediaAsset[];
}

const registry = JSON.parse(readFileSync(REGISTRY_PATH, 'utf8')) as MediaRegistry;

/** Absolute path of a registry/reference path inside `public/`. */
const publicFile = (assetPath: string) => join(PUBLIC_DIR, assetPath.replace(/^\/+/, ''));

const IMAGE_REF = /['"](\/[^'"\s]+\.(svg|png|jpe?g|webp|gif|ico))['"]/g;

const toPosix = (p: string) => p.split(sep).join('/');

/**
 * `src/ai_company/**` is the separate FastAPI CEO dashboard application
 * (AGENTS.md §13), not the public site. Its PWA manifest references
 * `/static/icons/*`, which the dashboard serves from its own static mount and
 * which the public site never renders. Those references are excluded from the
 * site image set deliberately; the exclusion is pinned in the test below so it
 * cannot widen without a reviewer seeing it.
 */
const NON_SITE_PREFIX = 'src/ai_company/';

/** This guard file quotes image paths in its own assertions; skip it when scanning. */
const SELF = 'src/__tests__/media-registry.test.ts';
const MEDIA_TS_REGISTRY = 'src/data/media/registry.ts';

/** Every .ts/.tsx/.json file under src/, plus the site shell index.html. */
const siteSourceFiles = (): string[] => {
  const walk = (dir: string): string[] =>
    readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) return entry.name === 'node_modules' ? [] : walk(full);
      return /\.(ts|tsx|json)$/.test(entry.name) ? [full] : [];
    });
  return [...walk(join(ROOT, 'src')), join(ROOT, 'index.html')];
};

/** Image paths referenced by site source, and by the excluded dashboard app. */
const collectReferences = (): { site: Set<string>; nonSite: Set<string> } => {
  const site = new Set<string>();
  const nonSite = new Set<string>();

  for (const file of siteSourceFiles()) {
    const rel = toPosix(relative(ROOT, file));
    if (rel === SELF || rel === MEDIA_TS_REGISTRY) continue;
    const target = rel.startsWith(NON_SITE_PREFIX) ? nonSite : site;
    for (const match of readFileSync(file, 'utf8').matchAll(IMAGE_REF)) {
      target.add(match[1]);
    }
  }

  return { site, nonSite };
};

describe('site media registry', () => {
  it('registers exactly 13 assets (pinned)', () => {
    // 13 = the 10 paths in site components/data + the 3 index.html shell icons.
    expect(
      registry.assets.length,
      `media-registry.json should hold exactly 13 assets; found ${registry.assets.length}. ` +
        'Update the registry and this pinned count together.',
    ).toBe(13);
  });

  it('covers every image path referenced by site source and index.html', () => {
    const { site, nonSite } = collectReferences();
    const registered = new Set(registry.assets.map((asset) => asset.path));

    const unregistered = [...site].filter((path) => !registered.has(path)).sort();
    expect(
      unregistered,
      `Unregistered image reference(s): ${unregistered.join(', ')} — add each to ` +
        'src/data/registries/media-registry.json with a real origin and licence.',
    ).toEqual([]);

    const stale = [...registered].filter((path) => !site.has(path)).sort();
    expect(
      stale,
      `Registry entr(y/ies) with no live reference: ${stale.join(', ')} — remove the entry ` +
        'or restore the reference.',
    ).toEqual([]);

    expect(
      [...nonSite].sort(),
      'The src/ai_company/ exclusion should only ever cover the dashboard PWA icons. ' +
        `Found: ${[...nonSite].sort().join(', ')}`,
    ).toEqual(['/static/icons/icon-maskable.svg', '/static/icons/icon.svg']);
  });

  it('gives every entry a rooted path, a kind, an origin and a licence', () => {
    for (const asset of registry.assets) {
      expect(
        asset.path.startsWith('/'),
        `Asset "${asset.id}" path must start with "/": got "${asset.path}".`,
      ).toBe(true);

      expect(
        ALLOWED_KINDS.includes(asset.kind as AllowedKind),
        `Asset "${asset.id}" has kind "${asset.kind}"; allowed kinds are ${ALLOWED_KINDS.join(', ')}.`,
      ).toBe(true);

      expect(
        typeof asset.origin === 'string' && asset.origin.trim().length > 0,
        `Asset "${asset.id}" (${asset.path}) has an empty origin; use "unknown" when the repo does not prove it.`,
      ).toBe(true);

      expect(
        typeof asset.licence === 'string' && asset.licence.trim().length > 0,
        `Asset "${asset.id}" (${asset.path}) has an empty licence; use "unknown" when the repo does not prove it.`,
      ).toBe(true);
    }
  });

  it('agrees with the file system: missing entries are absent, the rest exist', () => {
    for (const asset of registry.assets) {
      const exists = existsSync(publicFile(asset.path));

      if (asset.kind === 'missing') {
        expect(
          exists,
          `Asset "${asset.id}" (${asset.path}) is registered as missing but public/${asset.path} now exists. ` +
            'Replace the placeholder entry with a real kind, origin and licence.',
        ).toBe(false);
      } else {
        expect(
          exists,
          `Asset "${asset.id}" (${asset.path}) is registered as "${asset.kind}" but public/${asset.path} ` +
            'does not exist. Add the file or change the kind to "missing".',
        ).toBe(true);
      }
    }
  });

  it('requires a real disclosure for photograph and ai-generated entries', () => {
    for (const asset of registry.assets) {
      if (asset.kind !== 'photograph' && asset.kind !== 'ai-generated') continue;

      const disclosure = (asset.disclosure ?? '').trim();
      expect(
        disclosure.length > 0 && disclosure !== 'none',
        `Asset "${asset.id}" (${asset.path}) is "${asset.kind}" but carries disclosure "${disclosure || '(empty)'}". ` +
          'ADR-027 requires a real disclosure for generated or photographic imagery.',
      ).toBe(true);
    }
  });
});
