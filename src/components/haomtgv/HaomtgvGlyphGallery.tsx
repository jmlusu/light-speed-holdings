import React from 'react';
import { getMediaByType } from '../../../data/media/registry';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';

interface HaomtgvGlyphGalleryProps {
  theme: 'light' | 'dark';
}

/**
 * Type K micro-illustration gallery — the seven HAOMTGV glyphs from the
 * canonical media registry (Directive §22). Governance (G) is the red layer;
 * every other glyph carries the cyan accent.
 */
export const HaomtgvGlyphGallery: React.FC<HaomtgvGlyphGalleryProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const glyphs = getMediaByType('MICRO_ILLUSTRATIONS');

  return (
    <section
      className={`py-16 sm:py-24 ${isLight ? 'bg-ls-navy/5' : 'bg-ls-navy-dark'}`}
      aria-label="HAOMTGV glyph gallery"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-8">
        <SectionHeading
          theme={theme}
          eyebrow="THE SEVEN GLYPHS"
          title="H-A-O-M-T-G-V Glyphs"
          lead="Type K micro-illustrations: a single-color line-art glyph system for each HAOMTGV layer — brand cyan throughout, Governance marked in red."
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {glyphs.map((asset, idx) => {
            const isGovernance = asset.id === 'glyph-governance';
            const letter = asset.id.replace(/^glyph-/, '').charAt(0).toUpperCase();
            // Registry title "H — Human Glyph" → "Human" (matches pillar titles).
            const title = asset.title.replace(/^[A-Z]\s*—\s*/, '').replace(/\s+Glyph$/, '');
            return (
              <Reveal key={asset.id} delay={idx * 0.04}>
                <article
                  className={`h-full rounded-3xl p-5 border flex flex-col gap-3 transition-transform duration-300 hover:-translate-y-1 ${
                    isLight
                      ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                      : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                  } ${isGovernance ? 'ring-1 ring-ls-red/30' : 'ring-1 ring-ls-cyan/20'}`}
                >
                  <img
                    src={asset.src.svg}
                    alt={asset.alt}
                    width={64}
                    height={64}
                    loading="lazy"
                    className="w-12 h-12"
                  />
                  <div className="flex items-center gap-3">
                    <span
                      aria-hidden="true"
                      className={`flex w-10 h-10 shrink-0 items-center justify-center rounded-full border font-display font-black text-lg ${
                        isGovernance
                          ? 'border-ls-red/40 bg-ls-red/10 text-ls-red'
                          : 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
                      }`}
                    >
                      {letter}
                    </span>
                    <h3 className="font-display font-bold text-base tracking-tight">{title}</h3>
                  </div>
                  <p
                    className={`text-xs leading-relaxed ${
                      isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                    }`}
                  >
                    {asset.description}
                  </p>
                </article>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default HaomtgvGlyphGallery;
