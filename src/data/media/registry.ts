/**
 * Media Registry — Canonical Source of Truth
 *
 * Source: Directive §19-20 + MEDIA_ARCHITECTURE.md
 * Directive §22 — Single source for all media assets
 */

export type MediaType =
  | 'HERO_IMAGERY'
  | 'HAOMTGV_INFOGRAPHIC'
  | 'AI_COMPANY_BUILDER_ORG_CHART'
  | 'MODEL_ROUTING_INFOGRAPHIC'
  | 'AFRICA_AI_ECONOMICS'
  | 'USE_CASE_CARDS'
  | 'ARCHITECTURE_DIAGRAMS'
  | 'AFRICAN_MAPS'
  | 'RESEARCH_VISUALS'
  | 'HUMAN_LEADERSHIP'
  | 'MICRO_ILLUSTRATIONS';

export interface MediaAsset {
  id: string;
  type: MediaType;
  title: string;
  description: string;
  src: {
    webp?: string;
    avif?: string;
    svg?: string;
    png?: string;
    jpg?: string;
  };
  alt: string;
  width: number;
  height: number;
  formats: ('webp' | 'avif' | 'svg' | 'png' | 'jpg')[];
  placement: string[];         // Page routes where used
  attribution?: string;
  honestyTier?: 'verified' | 'proven-in-house' | 'fieldable' | 'pilot' | 'development';
  createdAt: string;
  updatedAt: string;
}

export const mediaRegistry: MediaAsset[] = [
  // TYPE B — HAOMTGV INFOGRAPHIC (Signature Diagram)
  {
    id: 'haomtgv-full-vertical',
    type: 'HAOMTGV_INFOGRAPHIC',
    title: 'H-A-O-M-T-G-V Framework (Full Vertical)',
    description: 'Complete H-A-O-M-T-G-V flow with feedback loops between Memory, Tools, Orchestration, Governance. Human at top, Value at bottom.',
    src: {
      svg: '/assets/diagrams/haomtgv/haomtgv-full-vertical.svg',
      png: '/brand/digital/Lightspeed HAOMTGV Operating Framework.png',
    },
    alt: 'H-A-O-M-T-G-V framework showing Human at top, flowing through Agents, Orchestration, Memory, Tools, Governance to Value, with feedback loops between Memory, Tools, Orchestration, and Governance',
    width: 800,
    height: 1200,
    formats: ['svg', 'png'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-20',
  },
  {
    id: 'haomtgv-horizontal-compact',
    type: 'HAOMTGV_INFOGRAPHIC',
    title: 'H-A-O-M-T-G-V Framework (Horizontal Compact)',
    description: 'Condensed horizontal version for inline use in sections with limited vertical space.',
    src: {
      svg: '/assets/diagrams/haomtgv/haomtgv-horizontal-compact.svg',
    },
    alt: 'Condensed horizontal H-A-O-M-T-G-V framework',
    width: 1200,
    height: 400,
    formats: ['svg'],
    placement: ['/solutions', '/sectors', '/insights'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'haomtgv-progressive',
    type: 'HAOMTGV_INFOGRAPHIC',
    title: 'H-A-O-M-T-G-V Framework (Progressive Reveal)',
    description: 'Animated progressive reveal version for hero sections — each layer reveals on scroll.',
    src: {
      svg: '/assets/diagrams/haomtgv/haomtgv-progressive.svg',
    },
    alt: 'Animated H-A-O-M-T-G-V framework with progressive scroll reveal',
    width: 1200,
    height: 1400,
    formats: ['svg'],
    placement: ['/'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },

  // TYPE C — AI COMPANY BUILDER ORG CHART
  {
    id: 'org-chart-thumb',
    type: 'AI_COMPANY_BUILDER_ORG_CHART',
    title: '90-Role Organization Chart (Thumbnail)',
    description: 'Static thumbnail for homepage and solution cards.',
    src: {
      svg: '/assets/diagrams/org-chart/org-chart-thumb.svg',
      webp: '/assets/diagrams/org-chart/org-chart-thumb.webp',
    },
    alt: '90-role organization chart thumbnail',
    width: 400,
    height: 300,
    formats: ['svg', 'webp'],
    placement: ['/', '/solutions'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },

  // TYPE D — MODEL ROUTING INFOGRAPHIC
  {
    id: 'model-routing-full',
    type: 'MODEL_ROUTING_INFOGRAPHIC',
    title: 'Model Routing Architecture (Full)',
    description: 'Complete 4-tier model routing: Local/Open-Weight → Low Cost Tasks; Mid-Tier → Standard Reasoning; Premium → High Complexity; Human → Final Authority.',
    src: {
      svg: '/assets/diagrams/model-routing/model-routing-full.svg',
      webp: '/assets/diagrams/model-routing/model-routing-full.webp',
      avif: '/assets/diagrams/model-routing/model-routing-full.avif',
    },
    alt: 'Four-tier model routing architecture showing Local/Open-Weight for low-cost tasks, Mid-Tier for standard reasoning, Premium for high complexity, Human for final authority',
    width: 1200,
    height: 800,
    formats: ['svg', 'webp', 'avif'],
    placement: ['/ai-company-builder', '/', '/what-we-do', '/faq', '/insights'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },

  // TYPE E — AFRICA AI ECONOMICS
  {
    id: 'africa-ai-economics',
    type: 'AFRICA_AI_ECONOMICS',
    title: 'African AI Economics Comparison',
    description: 'Comparison of API dependency vs local inference vs open-weight vs hybrid routing with cost/latency/sovereignty analysis.',
    src: {
      svg: '/assets/diagrams/africa-economics/africa-ai-economics.svg',
      webp: '/assets/diagrams/africa-economics/africa-ai-economics.webp',
    },
    alt: 'African AI economics comparison showing API dependency vs local inference vs open-weight models vs hybrid routing with cost, latency, and sovereignty metrics',
    width: 1200,
    height: 900,
    formats: ['svg', 'webp'],
    placement: ['/ai-company-builder', '/', '/what-we-do', '/about', '/faq', '/insights'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },

  // TYPE F — USE CASE CARDS (12 use cases)
  // TYPE G — ARCHITECTURE DIAGRAMS
  // TYPE H — AFRICAN MAPS
  // TYPE I — RESEARCH VISUALS (Pharos)
  {
    id: 'pharos-chart-template',
    type: 'RESEARCH_VISUALS',
    title: 'Pharos Chart Template',
    description: 'Recharts-styled chart template in LightSpeed brand (navy/cyan/red) for Pharos insights.',
    src: {
      svg: '/assets/insights/pharos-chart-template.svg',
    },
    alt: 'Pharos chart template showing brand-styled line/bar/area charts',
    width: 800,
    height: 500,
    formats: ['svg'],
    placement: ['/insights'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'pharos-evidence-matrix',
    type: 'RESEARCH_VISUALS',
    title: 'Pharos Evidence Matrix Template',
    description: 'Claim ↔ Source grid template for Pharos research notes and policy notes.',
    src: {
      svg: '/assets/insights/pharos-evidence-matrix.svg',
    },
    alt: 'Evidence matrix template showing claims mapped to sources with verification status',
    width: 1000,
    height: 700,
    formats: ['svg'],
    placement: ['/insights'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'pharos-model-comparison',
    type: 'RESEARCH_VISUALS',
    title: 'Pharos Model Comparison Diagram',
    description: 'Benchmark visualization template for model routing and AI economics insights.',
    src: {
      svg: '/assets/insights/pharos-model-comparison.svg',
    },
    alt: 'Model comparison diagram showing cost/quality/latency across model tiers',
    width: 1000,
    height: 600,
    formats: ['svg'],
    placement: ['/insights'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },

  // TYPE J — HUMAN LEADERSHIP
  // TYPE K — MICRO-ILLUSTRATIONS (HAOMTGV Glyphs)
  {
    id: 'glyph-human',
    type: 'MICRO_ILLUSTRATIONS',
    title: 'H — Human Glyph',
    description: 'Stylized figure with intent arrow for Human layer.',
    src: {
      svg: '/assets/diagrams/micro-illustrations/glyph-human.svg',
    },
    alt: 'Human glyph: stylized figure with forward-pointing arrow',
    width: 64,
    height: 64,
    formats: ['svg'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'glyph-agents',
    type: 'MICRO_ILLUSTRATIONS',
    title: 'A — Agents Glyph',
    description: 'Interlocking geometric forms for Agents layer.',
    src: {
      svg: '/assets/diagrams/micro-illustrations/glyph-agents.svg',
    },
    alt: 'Agents glyph: interlocking geometric forms representing 89 AI agents',
    width: 64,
    height: 64,
    formats: ['svg'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'glyph-orchestration',
    type: 'MICRO_ILLUSTRATIONS',
    title: 'O — Orchestration Glyph',
    description: 'Flow lines and nodes for Orchestration layer.',
    src: {
      svg: '/assets/diagrams/micro-illustrations/glyph-orchestration.svg',
    },
    alt: 'Orchestration glyph: flow lines connecting nodes representing MessageBus routing',
    width: 64,
    height: 64,
    formats: ['svg'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'glyph-memory',
    type: 'MICRO_ILLUSTRATIONS',
    title: 'M — Memory Glyph',
    description: 'Layered cylinders for Memory layer.',
    src: {
      svg: '/assets/diagrams/micro-illustrations/glyph-memory.svg',
    },
    alt: 'Memory glyph: layered cylinders representing 6 memory types',
    width: 64,
    height: 64,
    formats: ['svg'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'glyph-tools',
    type: 'MICRO_ILLUSTRATIONS',
    title: 'T — Tools Glyph',
    description: 'Wrench/terminal hybrid for Tools layer.',
    src: {
      svg: '/assets/diagrams/micro-illustrations/glyph-tools.svg',
    },
    alt: 'Tools glyph: wrench/terminal hybrid representing isolated execution environments',
    width: 64,
    height: 64,
    formats: ['svg'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'glyph-governance',
    type: 'MICRO_ILLUSTRATIONS',
    title: 'G — Governance Glyph',
    description: 'Shield with check for Governance layer.',
    src: {
      svg: '/assets/diagrams/micro-illustrations/glyph-governance.svg',
    },
    alt: 'Governance glyph: shield with checkmark representing 5-tier approval and audit',
    width: 64,
    height: 64,
    formats: ['svg'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },
  {
    id: 'glyph-value',
    type: 'MICRO_ILLUSTRATIONS',
    title: 'V — Value Glyph',
    description: 'Upward chart/diamond for Value layer.',
    src: {
      svg: '/assets/diagrams/micro-illustrations/glyph-value.svg',
    },
    alt: 'Value glyph: upward-trending chart with diamond representing measurable business outcomes',
    width: 64,
    height: 64,
    formats: ['svg'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'proven-in-house',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-01',
  },

  // BRAND LOGO VARIANTS — mirrors `brand/guidelines/brand-guidelines.md` §3.
  // Every path below must resolve inside `brand/logo/` (mirrored to
  // `static/brand/logo/` and `public/brand/logo/`, 31 files, SVG + PNG only).
  {
    id: 'logo-full-color',
    type: 'HERO_IMAGERY',
    title: 'LightSpeed Logo — Full',
    description: 'Canonical mark plus wordmark on a light background, for headers and covers.',
    src: {
      svg: '/brand/logo/logo-full.svg',
      png: '/brand/logo/logo-full.png',
    },
    alt: 'LightSpeed Holdings Limited logo: speed mark with wordmark',
    width: 1254,
    height: 1254,
    formats: ['svg', 'png'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/solutions', '/use-cases', '/sectors', '/insights', '/about', '/contact', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },
  {
    id: 'logo-dark-bg',
    type: 'HERO_IMAGERY',
    title: 'LightSpeed Logo — Dark Background',
    description: 'Logo variant tuned for navy and other dark backgrounds.',
    src: {
      svg: '/brand/logo/logo-dark-bg.svg',
      png: '/brand/logo/logo-dark-bg.png',
    },
    alt: 'LightSpeed logo for dark backgrounds',
    width: 1254,
    height: 1254,
    formats: ['svg', 'png'],
    placement: ['/ai-company-builder', '/insights', '/about'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },
  {
    id: 'logo-light-bg',
    type: 'HERO_IMAGERY',
    title: 'LightSpeed Logo — Light Background',
    description: 'Logo variant tuned for white and other light backgrounds.',
    src: {
      svg: '/brand/logo/logo-light-bg.svg',
      png: '/brand/logo/logo-light-bg.png',
    },
    alt: 'LightSpeed logo for light backgrounds',
    width: 1254,
    height: 1254,
    formats: ['svg', 'png'],
    placement: ['/', '/what-we-do', '/solutions', '/use-cases', '/sectors', '/contact', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },
  {
    id: 'logo-icon',
    type: 'HERO_IMAGERY',
    title: 'LightSpeed Mark',
    description: 'Bare speed-mark, for places where the wordmark is already present.',
    src: {
      svg: '/brand/logo/logo-mark.svg',
      png: '/brand/logo/logo-mark.png',
    },
    alt: 'LightSpeed speed-mark',
    width: 609,
    height: 386,
    formats: ['svg', 'png'],
    placement: ['/', '/ai-company-builder', '/what-we-do', '/solutions', '/use-cases', '/sectors', '/insights', '/about', '/contact', '/faq'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },
  {
    id: 'logo-monochrome',
    type: 'HERO_IMAGERY',
    title: 'LightSpeed Mark — Monochrome',
    description: 'Single-colour navy mark for print and limited-colour contexts.',
    src: {
      svg: '/brand/logo/logo-mark-mono.svg',
      png: '/brand/logo/logo-mark-mono.png',
    },
    alt: 'LightSpeed mark in monochrome',
    width: 609,
    height: 386,
    formats: ['svg', 'png'],
    placement: ['/legal/privacy', '/legal/terms', '/print'],
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },
  {
    id: 'favicon',
    type: 'HERO_IMAGERY',
    title: 'Favicon',
    description: 'Favicon and touch icons for all platforms.',
    src: {
      svg: '/brand/logo/logo-favicon.svg',
      png: '/brand/logo/logo-favicon.png',
    },
    alt: 'LightSpeed favicon',
    width: 512,
    height: 512,
    formats: ['svg', 'png'],
    placement: ['*'], // All pages
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },
  {
    id: 'social-avatar',
    type: 'HERO_IMAGERY',
    title: 'Social Media Avatar',
    description: 'Square avatar for LinkedIn, X, Facebook, GitHub profiles.',
    src: {
      svg: '/brand/logo/logo-avatar.svg',
      png: '/brand/logo/logo-avatar.png',
    },
    alt: 'LightSpeed social media avatar',
    width: 1024,
    height: 1024,
    formats: ['svg', 'png'],
    placement: ['*'], // All pages (meta tags)
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },
  {
    id: 'og-share',
    type: 'HERO_IMAGERY',
    title: 'Open Graph / Social Share Image',
    description: '1200×630 image for link previews on social media and messaging.',
    src: {
      svg: '/brand/logo/logo-og.svg',
      png: '/brand/logo/logo-og.png',
    },
    alt: 'LightSpeed Open Graph image: logo, tagline, and visual identity',
    width: 1200,
    height: 630,
    formats: ['svg', 'png'],
    placement: ['*'], // All pages (meta tags)
    attribution: 'LightSpeed Holdings Design Team',
    honestyTier: 'verified',
    createdAt: '2026-10-01',
    updatedAt: '2026-10-28',
  },

];

export function getMediaById(id: string): MediaAsset | undefined {
  return mediaRegistry.find(m => m.id === id);
}

export function getMediaByType(type: MediaType): MediaAsset[] {
  return mediaRegistry.filter(m => m.type === type);
}

export function getMediaForRoute(route: string): MediaAsset[] {
  return mediaRegistry.filter(m => m.placement.includes(route) || m.placement.includes('*'));
}

export function getMediaByHonestyTier(tier: MediaAsset['honestyTier']): MediaAsset[] {
  return mediaRegistry.filter(m => m.honestyTier === tier);
}

export default mediaRegistry;
