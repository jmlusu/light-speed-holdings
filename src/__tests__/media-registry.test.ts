import { describe, it, expect } from 'vitest';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

/**
 * Media registry guard.
 *
 * `src/data/registries/media-registry.json` is the authoritative record of every
 * image the public site renders (origin, licence, disclosure). This suite keeps it
 * honest in six directions:
 *   1. the entry count is pinned, so an asset cannot be added or dropped silently;
 *   2. every image path referenced from site source resolves to a registry entry;
 *   3. every entry carries a usable origin, licence and kind;
 *   4. the file system agrees with the entry — `missing` means missing, and every
 *      other kind means the file is really under `public/`;
 *   5. no new `/src/assets/**` string literal is introduced (Vite cannot emit
 *      those; the existing set is quarantined and may only shrink);
 *   6. every path declared by `src/data/media/registry.ts` resolves under
 *      `public/`, or is pinned as known-missing and may only shrink.
 *
 * Adding an image to the site therefore fails here until it is registered, and
 * registering a `missing` path fails once someone adds the file, forcing a real
 * origin/licence decision instead of leaving a placeholder in place.
 *
 * `avif` is in the extension list deliberately: an earlier version omitted it,
 * which hid 14 broken `.avif` references (all 404 in production) from this suite.
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

const IMAGE_REF = /['"](\/[^'"\s]+\.(svg|png|jpe?g|webp|avif|gif|ico))['"]/g;

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

/**
 * `/src/assets/**` string literals are not Vite module assets.
 *
 * A path written as a plain string (`src="/src/assets/images/x.jpg"`, a Tailwind
 * `bg-[url('...')]`, or a data object field) is invisible to the bundler: Vite
 * neither resolves it nor emits it, so it is copied into the bundle verbatim and
 * 404s in production. Only imports and CSS `url()` references become hashed
 * `dist/assets/*` files. An earlier version of this suite checked these literals
 * for *existence on disk* and called that proof; it passed on 35 references that
 * were broken in production.
 *
 * The current set is therefore quarantined below as `KNOWN_BUNDLED_LITERALS` and
 * may only shrink. Fixing a path (import, or move to `public/` + `/assets/` URL)
 * fails this suite until the entry is removed, so the list cannot silently rot.
 *
 * Provenance gap: the 62 files under `src/assets/images/` carry no registry record
 * yet. Recording them needs an origin/licence decision per file, which the repo
 * does not currently evidence. Tracked as follow-up, not silently waived.
 */
const BUNDLED_ASSET_PREFIX = '/src/assets/';

/** This guard file quotes image paths in its own assertions; skip it when scanning. */
const SELF = 'src/__tests__/media-registry.test.ts';
const MEDIA_TS_REGISTRY = 'src/data/media/registry.ts';

/**
 * `/src/assets/**` string literals in source (P0 debt, exact set).
 *
 * Every one of these is emitted verbatim and 404s in production; the files exist
 * under `src/assets/images/` (62 files, 54 MB), so each is fixable by importing it
 * or moving it under `public/` and switching to an `/assets/` URL. The list is
 * exact, not a floor: new literals fail immediately, and a fix fails until its
 * entry is deleted here.
 */
const KNOWN_BUNDLED_LITERALS: string[] = [
  '/src/assets/images/agent_network_topology_1793816821318.jpg',
  '/src/assets/images/audience_business_leaders_1793515174408.jpg',
  '/src/assets/images/audience_partners_1793515174751.jpg',
  '/src/assets/images/audience_policy_makers_1793515176396.jpg',
  '/src/assets/images/audience_researchers_1793515174898.jpg',
  '/src/assets/images/before_after_sector_bg_daytime_1793890712154.jpg',
  '/src/assets/images/before_after_sector_bg_light_1793889809250.jpg',
  '/src/assets/images/cap1_company_building_1793817051020.jpg',
  '/src/assets/images/cap2_workflow_automation_1793817065625.jpg',
  '/src/assets/images/cap3_agentic_orchestration_1793817079580.jpg',
  '/src/assets/images/cap4_integration_pure_1793817124475.jpg',
  '/src/assets/images/cap5_organizational_memory_1793817139478.jpg',
  '/src/assets/images/cap6_governance_infrastructure_1793817153646.jpg',
  '/src/assets/images/cta_pathway_destination_1793817195986.jpg',
  '/src/assets/images/hero_cinematic_landscape_day.jpg',
  '/src/assets/images/hero_cinematic_landscape_night_1793514971805.jpg',
  '/src/assets/images/identity_triptych_foundations_1793818127924.jpg',
  '/src/assets/images/modular_agent_architecture_1793818142394.jpg',
  '/src/assets/images/pharos_africa_infrastructure_1793514971621.jpg',
  '/src/assets/images/pharos_ai_governance_1793514972204.jpg',
  '/src/assets/images/pharos_ai_orchestration_1793514971486.jpg',
  '/src/assets/images/pharos_article_thumb_cost_1793817753722.jpg',
  '/src/assets/images/pharos_article_thumb_gov_1793817768084.jpg',
  '/src/assets/images/pharos_article_thumb_sadc_1793817783127.jpg',
  '/src/assets/images/pharos_canonical_architecture_1793817675241.jpg',
  '/src/assets/images/pharos_cta_pure_1793817814419.jpg',
  '/src/assets/images/pharos_editorial_hero_1793817662034.jpg',
  '/src/assets/images/philosophy_triptych_clean_1793818099752.jpg',
  '/src/assets/images/solution_agentic_automation_1793514973368.jpg',
  '/src/assets/images/solution_company_builder_1793514972767.jpg',
  '/src/assets/images/solution_market_intelligence_1793514973546.jpg',
  '/src/assets/images/solution_workflow_collapsing_1793514973725.jpg',
  '/src/assets/images/val_prop_bg_night_1793997847272.jpg',
  '/src/assets/images/whitepaper_a_cover_clean_1793817703115.jpg',
  '/src/assets/images/whitepaper_b_cover_clean_1793817739118.jpg',
];

/**
 * `src/data/media/registry.ts` declarations with no file under `public/` (P1 debt, exact set).
 *
 * The registry is the canonical asset catalog, so a declaration without a file is a
 * broken promise even when nothing renders it yet: today only `haomtgv-full-vertical`
 * and the micro-illustration glyphs have consumers, which is why these never
 * produced a network request. Add the file and this suite asks you to drop the entry;
 * declare a new absent path and it fails immediately.
 */
const KNOWN_MISSING_MEDIA_DECLARATIONS: string[] = [
  '/assets/diagrams/africa-economics/africa-ai-economics.svg',
  '/assets/diagrams/africa-economics/africa-ai-economics.webp',
  '/assets/diagrams/architecture/aicb-system.svg',
  '/assets/diagrams/architecture/aicb-system.webp',
  '/assets/diagrams/architecture/data-sovereignty.svg',
  '/assets/diagrams/architecture/data-sovereignty.webp',
  '/assets/diagrams/architecture/governance.svg',
  '/assets/diagrams/architecture/governance.webp',
  '/assets/diagrams/architecture/memory.svg',
  '/assets/diagrams/architecture/memory.webp',
  '/assets/diagrams/architecture/orchestration.svg',
  '/assets/diagrams/architecture/orchestration.webp',
  '/assets/diagrams/haomtgv/haomtgv-full-vertical.webp',
  '/assets/diagrams/haomtgv/haomtgv-horizontal-compact.webp',
  '/assets/diagrams/haomtgv/haomtgv-progressive.webp',
  '/assets/diagrams/model-routing/model-routing-full.avif',
  '/assets/diagrams/model-routing/model-routing-full.svg',
  '/assets/diagrams/model-routing/model-routing-full.webp',
  '/assets/diagrams/org-chart/org-chart-full.svg',
  '/assets/diagrams/org-chart/org-chart-full.webp',
  '/assets/diagrams/org-chart/org-chart-thumb.svg',
  '/assets/diagrams/org-chart/org-chart-thumb.webp',
  '/assets/hero/about-hero.avif',
  '/assets/hero/about-hero.webp',
  '/assets/hero/aicb-hero.avif',
  '/assets/hero/aicb-hero.webp',
  '/assets/hero/home-hero.avif',
  '/assets/hero/home-hero.webp',
  '/assets/hero/whatwedo-hero.avif',
  '/assets/hero/whatwedo-hero.webp',
  '/assets/insights/pharos-chart-template.svg',
  '/assets/insights/pharos-evidence-matrix.svg',
  '/assets/insights/pharos-model-comparison.svg',
  '/assets/leadership/jack-mlusu.avif',
  '/assets/leadership/jack-mlusu.jpg',
  '/assets/leadership/jack-mlusu.webp',
  '/assets/maps/malawi-sadc-africa.svg',
  '/assets/maps/malawi-sadc-africa.webp',
  '/assets/maps/sector-presence.svg',
  '/assets/maps/sector-presence.webp',
  '/assets/use-cases/agricultural-coordination.avif',
  '/assets/use-cases/agricultural-coordination.webp',
  '/assets/use-cases/audit-trail.webp',
  '/assets/use-cases/compliance-automation.avif',
  '/assets/use-cases/compliance-automation.webp',
  '/assets/use-cases/customer-service.webp',
  '/assets/use-cases/donor-reporting.avif',
  '/assets/use-cases/donor-reporting.webp',
  '/assets/use-cases/executive-readiness.webp',
  '/assets/use-cases/market-intelligence.webp',
  '/assets/use-cases/sme-operations.avif',
  '/assets/use-cases/sme-operations.webp',
];

/** Every image path declared by `src/data/media/registry.ts`, sorted and deduped. */
const mediaDeclarations = (): string[] => {
  const source = readFileSync(join(ROOT, MEDIA_TS_REGISTRY), 'utf8');
  return [...new Set([...source.matchAll(IMAGE_REF)].map((match) => match[1]))].sort();
};

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

/** Image paths referenced by site source, by the excluded dashboard app, and bundled. */
const collectReferences = (): {
  site: Set<string>;
  nonSite: Set<string>;
  bundled: Set<string>;
} => {
  const site = new Set<string>();
  const nonSite = new Set<string>();
  const bundled = new Set<string>();

  for (const file of siteSourceFiles()) {
    const rel = toPosix(relative(ROOT, file));
    if (rel === SELF || rel === MEDIA_TS_REGISTRY) continue;
    // The media registry's own declarations are validated separately against
    // public/ (resolved-or-pinned), not against the rendered-image registry above.
    const target = rel.startsWith(NON_SITE_PREFIX) ? nonSite : site;
    for (const match of readFileSync(file, 'utf8').matchAll(IMAGE_REF)) {
      if (match[1].startsWith(BUNDLED_ASSET_PREFIX)) {
        bundled.add(match[1]);
      } else {
        target.add(match[1]);
      }
    }
  }

  return { site, nonSite, bundled };
};

describe('site media registry', () => {
  it('registers exactly 26 assets (pinned)', () => {
    // 26 = 13 public site assets + 10 aistudio backgrounds + 3 brand logos.
    expect(
      registry.assets.length,
      `media-registry.json should hold exactly 26 assets; found ${registry.assets.length}. ` +
        'Update the registry and this pinned count together.',
    ).toBe(28);
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

  it('introduces no new /src/assets/ string literals', () => {
    const { bundled } = collectReferences();

    expect(
      [...bundled].sort(),
      'New /src/assets/ literal(s) found. Vite cannot resolve a path written as a plain string: ' +
        'it is emitted verbatim and 404s in production. Import the file so Vite hashes and emits ' +
        'it, or move it under public/ and use a root-relative /assets/ URL.',
    ).toEqual([...KNOWN_BUNDLED_LITERALS].sort());
  });

  it('keeps every quarantined /src/assets/ file on disk', () => {
    const missing = KNOWN_BUNDLED_LITERALS.filter(
      (assetPath) => !existsSync(join(ROOT, assetPath.replace(/^\/+/, ''))),
    ).sort();

    expect(
      missing,
      `Quarantined literal(s) with no file on disk: ${missing.join(', ')} — the P0 move cannot ` +
        'run. Restore the file, or remove the reference and its entry here.',
    ).toEqual([]);
  });

  it('resolves or pins every media-registry declaration', () => {
    const unpinned = mediaDeclarations().filter(
      (assetPath) =>
        !existsSync(publicFile(assetPath)) && !KNOWN_MISSING_MEDIA_DECLARATIONS.includes(assetPath),
    );

    expect(
      unpinned,
      `Media declaration(s) with no file under public/: ${unpinned.join(', ')} — add the file, or ` +
        'pin each in KNOWN_MISSING_MEDIA_DECLARATIONS so the debt is visible in review.',
    ).toEqual([]);
  });

  it('drops pinned media declarations once the file lands', () => {
    const resurrected = KNOWN_MISSING_MEDIA_DECLARATIONS.filter((assetPath) =>
      existsSync(publicFile(assetPath)),
    );

    expect(
      resurrected,
      `Pinned media declaration(s) now resolve: ${resurrected.join(', ')} — remove each from ` +
        'KNOWN_MISSING_MEDIA_DECLARATIONS. The pin records missing files and may only shrink.',
    ).toEqual([]);
  });

  it('pins only paths the media registry still declares', () => {
    const declared = new Set(mediaDeclarations());
    const orphaned = KNOWN_MISSING_MEDIA_DECLARATIONS.filter((assetPath) => !declared.has(assetPath));

    expect(
      orphaned,
      `Pinned path(s) no longer declared by data/media/registry.ts: ${orphaned.join(', ')} — the ` +
        'reference was removed; delete the entry so the pin keeps matching reality.',
    ).toEqual([]);
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
