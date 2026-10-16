import React from 'react';
import { Link } from 'react-router-dom';
import { sun } from 'lucide-react';
import { useEffect, useState } from 'react';
import { SectionHeading } from '../components/site/SectionHeading';
import { Reveal } from '../components/Reveal';
import { HomeSection } from '../components/home/HomeSection';
import { getMediaByType, MediaAsset } from '../../data/media/registry';

/**
 * HAOMTGV Standalone Page ΓÇö H-A-O-M-T-G-V Operating Philosophy
 * 
 * Demonstrates the 7-layer framework as a dedicated page, silent on Honest status discipline.
 * Brand: navy `#070A40` / red `#E63946` / cyan `#00BFFF` + Arial type scale.
 * Media: Type B HAOMTGV_INFOGRAPHIC (full vertical), Type K micro-illustrations (glyphs).
 * Animations: scroll-reveal (Reveal component), line-draw aesthetic, card hover flips, hover pulses.
 * 
 * @see HAOMTGVSection ΓÇö embedded variant within HomePage
 * @see MEDIA_ARCHITECTURE.md ┬º20 ΓÇö HAOMTGV media placement
 */

// Micro-illustration (Type K) SVG sources ΓÇö canonical-only, not mirrored
const MICRO_ILLUSTRATIONS: Record<string, { svg: string; alt: string }> = {
  human: {
    svg: '/assets/diagrams/micro-illustrations/glyph-human.svg',
    alt: 'Human glyph: stylized figure with forward-pointing arrow',
  },
  agents: {
    svg: '/assets/diagrams/micro-illustrations/glyph-agents.svg',
    alt: 'Agents glyph: interlocking geometric forms representing AI agent roles',
  },
  orchestration: {
    svg: '/assets/diagrams/micro-illustrations/glyph-orchestration.svg',
    alt: 'Orchestration glyph: flow lines connecting nodes representing MessageBus routing',
  },
  memory: {
    svg: '/assets/diagrams/micro-illustrations/glyph-memory.svg',
    alt: 'Memory glyph: layered cylinders representing 6 memory types',
  },
  tools: {
    svg: '/assets/diagrams/micro-illustrations/glyph-tools.svg',
    alt: 'Tools glyph: wrench/terminal hybrid representing isolated execution environments',
  },
  governance: {
    svg: '/assets/diagrams/micro-illustrations/glyph-governance.svg',
    alt: 'Governance glyph: shield with checkmark representing 5-tier approval and audit',
  },
  value: {
    svg: '/assets/diagrams/micro-illustrations/glyph-value.svg',
    alt: 'Value glyph: upward-trending chart with diamond representing measurable business outcomes',
  },
};

// Pillar definitions ΓÇö standalone page variant
interface Pillar {
  id: string;
  letter: string;
  title: string;
  description: string;
  icon: keyof typeof MICRO_ILLUSTRATIONS;
}

const PILLARS: Pillar[] = [
  {
    id: 'human',
    letter: 'H',
    title: 'Human',
    description:
      'People set intent, own outcomes, and hold final decision authority. Agents propose; humans decide what ships.',
    icon: 'human',
  },
  {
    id: 'agents',
    letter: 'A',
    title: 'Agents',
    description:
      'Specialized AI roles with explicit scopes, tools, and approval thresholds. Not a single general-purpose bot.',
    icon: 'agents',
  },
  {
    id: 'orchestration',
    letter: 'O',
    title: 'Orchestration',
    description:
      'Deterministic routing of tasks, data, and decisions across workflows so multi-step work stays auditable end to end.',
    icon: 'orchestration',
  },
  {
    id: 'memory',
    letter: 'M',
    title: 'Memory',
    description:
      'Persistent contextual state across long-running work, so agents recall before they act, not from a blank slate.',
    icon: 'memory',
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'Tools',
    description:
      'Isolated execution environments for APIs, data, and actions: the only way agents touch the outside world.',
    icon: 'tools',
  },
  {
    id: 'governance',
    letter: 'G',
    title: 'Governance',
    description:
      'A control layer woven through the model: five-tier human approval, append-only audit receipts, and risk-classified actions.',
    icon: 'governance',
  },
  {
    id: 'value',
    letter: 'V',
    title: 'Value',
    description:
      'Measured business outcomes (cost, latency, quality, and adoption) fed back into strategy, not vanity metrics.',
    icon: 'value',
  },
];

/**
 * Hero section with full HAOMTGV framework title and tagline
 */
const HAOMTGVHero: React.FC = () => {
  return (
    <section
      className="relative pt-24 sm:pt-32 pb-16 bg-navy-dark dark:bg-navy-dark"
      aria-label="HAOMTGV operating philosophy hero"
    >
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid lg:grid-cols-2 gap-8 items-center">
          <div>
            <h1 className="font-display font-black text-5xl sm:text-6xl lg:text-7xl tracking-tight text-ls-cyan mb-4">
              H-A-O-M-T-G-V
            </h1>
            <p className="font-display text-ls-grey-light-text text-lg leading-relaxed mb-8 max-w-xl">
              Not a linear pipeline. A control model where human authority runs through every layer
              and governance is an integral control layer (G), not a final checkpoint.
            </p>
            <Link
              to="/ai-company-builder/#governance"
              className="inline-flex items-center gap-2 rounded-full border border-ls-red/30 px-4 py-2 text-[10px] font-bold tracking-widest transition-colors hover:text-ls-red"
            >
              Explore the Framework ΓåÆ
              <sun className="w-3.5 h-3.5 text-ls-red" aria-hidden="true" />
            </Link>
          </div>

          <div className="relative">
            {/* Brand accent divider */}
            <div className="absolute bottom-0 left-0 right-0 h-px bg-ls-red/20"></div>
          </div>
        </div>
      </section>
    );
};

/**
 * Layer Card with micro-illustration and hover interaction
 */
const LayerCard: React.FC<{pillar: Pillar}> = ({pillar}) => {
  return (
    <article
      className="rounded-3xl p-6 border flex flex-col gap-4 border-ls-grey-dark dark:border-ls-white/15 shadow-md transition-shadow hover-shadow-xl hover:-translate-y-1"
    >
      <div className="flex items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-3">
          {/* Letter badge with red border */}
          <span
            aria-hidden="true"
            className="flex w-10 h-10 items-center justify-center rounded-full border border-ls-red/40 bg-ls-red/10 font-display font-black text-ls-red text-lg"
          >
            {pillar.letter}
          </span>
          <h3 className="font-display font-bold text-base tracking-tight">{pillar.title}</h3>
        </div>

        {/* Micro-illustration */}
        <img
          src={MICRO_ILLUSTRATIONS[pillar.icon].svg}
          alt={MICRO_ILLUSTRATIONS[pillar.icon].alt}
          className="w-5 h-5 text-ls-cyan"
        />
      </div>

      <p className="text-xs leading-relaxed">
        {pillar.description}
      </p>
    </article>
  );
};

/**
 * Full HAOMTGV Infographic (Type B - vertical) from media registry
 */
const HAOMTGVInfographic: React.FC = () => {
  // Load HAOMTGV_INFOGRAPHIC assets from the canonical registry
  const assets = getMediaByType('HAOMTGV_INFOGRAPHIC');
  const asset = assets?[0];

  return (
    <section
      className="py-24 sm:py-32 bg-ls-grey-dark dark:bg-ls-navy/80"
      aria-label="HAOMTGV full vertical infographic"
    >
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6">
        {/* Infographic with SVG/webp fallbacks */}
        {asset && (
          <div className="relative aspect-[1200/1600] rounded-xl overflow-hidden border border-ls-grey-dark dark:border-ls-white/15 mx-auto">
            {/* SVG rendering */}
            {asset.formats.includes('svg') && (
              <svg
                width={asset.width}
                height={asset.height}
                className="w-full h-full object-contain"
                viewBox="0 0 {asset.width} {asset.height}"
                role="img"
                aria-labelledby="haomtgv-title"
              >
                <title id="haomtgv-title">{asset.title}</title>
                <rect width={asset.width} height={asset.height} fill="none" />
                <text
                  x={asset.width / 2}
                  y={asset.height / 2}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fontFamily="Arial, sans-serif"
                  fontSize={Math.min(asset.width, asset.height) / 25}
                  fill="currentColor"
                >
                  {asset.title}
                </text>
              </svg>
            )}

            {/* WebP fallback */}
            {asset.formats.includes('webp') && (
              <img
                src={asset.src?.webp || '/assets/diagrams/haomtgv/haomtgv-full-vertical.webp'}
                alt={asset.alt}
                width={asset.width}
                height={asset.height}
                className="w-full h-full object-contain"
                style={{ WebkitFontSmoothing: 'antialiased', MozOsxFontSmoothing: 'antialiased' }}
              />
            )}
          </div>

          {/* Caption */}
          {asset.description && (
            <p className="mt-6 text-center text-xs text-ls-grey-light-text leading-relaxed">
              {asset.description}
            </p>
          )}

          {/* Attribution */}
          {asset.attribution && (
            <p className="mt-2 text-[10px] font-body font-bold tracking-widest text-ls-red/60">
              {asset.attribution}
            </p>
          )}
        )}
      </div>
    </section>
  );
};

/**
 * Micro-illustration gallery (Type K)
 */
const MicroIllustrationsGallery: React.FC = () => {
  return (
    <section
      className="py-16 sm:py-24 bg-ls-grey-dark dark:bg-ls-navy/80"
      aria-label="HAOMTGV micro-illustrations gallery"
    >
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeading
          theme="light"
          eyebrow="MICRO ILLUSTRIATIONS"
          title="H-A-O-M-T-G-V Glyphs"
          lead="Type K micro-illustrations: single-color glyph system for each HAOMTGV layer, using currentColor for brand-themed theming."
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Object.entries(MICRO_ILLUSTRATIONS).map(([key, illustration]) => (
            <article
              key={key}
              className="group rounded-xl p-4 border border-ls-grey-dark dark:border-ls-white/15 hover-shadow-xl transition-all duration-300"
            >
              <img
                src={illustration.svg}
                alt={illustration.alt}
                className="w-12 h-12 mx-auto mb-3 group-hover:text-ls-red transition-colors"
              />
              <h4 className="font-display font-bold text-center text-sm tracking-tight">{key}</h4>
              <p className="text-[10px] font-body font-bold tracking-widest text-ls-grey-light-text mt-2">
                {MICRO_ILLUSTRATIONS[key].alt}
              </p>
            </article>
          ))}
        </div>

        {/* Brand color reference */}
        <div className="mt-8 flex gap-2 justify-center">
          <div className="w-6 h-6 rounded-full bg-ls-navy"></div>
          <div className="w-6 h-6 rounded-full bg-ls-red"></div>
          <div className="w-6 h-6 rounded-full bg-ls-cyan"></div>
        </div>
      </div>
    </section>
  );
};

/**
 * HAOMTGV Standalone Page ΓÇö dedicated showcase of the 7-layer framework
 */
export const HAOMTVGPage: React.FC = () => {
  // Load HAOMTGV infographic assets on mount
  useEffect(() => {
    // Assets loaded lazily via getMediaByType in HAOMTGVInfographic component
  }, []);

  const isLight = true; // Theme will be applied by parent / Tailwind

  return (
    <section>
      {/* ============================================================
         Hero section
         ============================================================ */}
      <HAOMTGVHero />

      {/* ============================================================
         Layer cards grid ΓÇö 7 pillars
         ============================================================ */}
      <section
        className="py-16 sm:py-24 bg-ls-white dark:bg-ls-navy/80"
        aria-label="HAOMTGV 7-layer pillar cards"
      >
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6">
          <SectionHeading
            theme="light"
            eyebrow="OPERATING PHILOSOPHY"
            title="H-A-O-M-T-G-V"
            lead="How LightSpeed thinks about AI-native operations: Human authority through Agents, Orchestration, Memory, and Tools, with Governance as an integral control layer and Value as the only score that counts. Not a linear pipeline; a working model."
          />

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 md:gap-4">
            {PILLARS.map((pillar) => (
              <Reveal key={pillar.id} delay={PILLARS.indexOf(pillar) * 0.04}>
                <LayerCard pillar={pillar} />
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================
         Full HAOMTGV Infographic (Type B)
         ============================================================ */}
      <HAOMTGVInfographic />

      {/* ============================================================
         Micro-illustration gallery (Type K)
         ============================================================ */}
      <MicroIllustrationsGallery />
    </section>
  );
};

/* ΓöÇΓöÇ End of HAOMTVGPage ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ */

export default HAOMTVGPage;
