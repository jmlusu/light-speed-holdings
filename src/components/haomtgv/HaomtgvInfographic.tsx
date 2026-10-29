import React from 'react';
import { getMediaById } from '../../data/media/registry';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';

interface HaomtgvInfographicProps {
  theme: 'light' | 'dark';
}

/**
 * Type B HAOMTGV infographic — framed figure rendered from the canonical
 * media registry entry `haomtgv-full-vertical` (the real PNG served from
 * /brand/digital/). Renders nothing when the registry entry or its PNG
 * source is missing.
 */
export const HaomtgvInfographic: React.FC<HaomtgvInfographicProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const asset = getMediaById('haomtgv-full-vertical');

  if (!asset || !asset.src.png) {
    return null;
  }

  const displayTitle = asset.title.replace(/\s+\([^)]*\)\s*$/, '');

  return (
    <section
      className={`py-16 sm:py-24 ${isLight ? 'bg-ls-white' : 'bg-ls-navy-dark'}`}
      aria-label="HAOMTGV full framework infographic"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-8">
        <SectionHeading
          theme={theme}
          eyebrow="THE FRAMEWORK"
          title={displayTitle}
          lead={asset.description}
        />

        <Reveal>
          <figure
            className={`mx-auto max-w-4xl rounded-3xl border p-3 sm:p-4 ring-1 ring-ls-cyan/25 shadow-xl ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark' : 'bg-ls-navy/80 border-ls-white/15'
            }`}
          >
            <img
              src={asset.src.png}
              alt={asset.alt}
              width={asset.width}
              height={asset.height}
              loading="lazy"
              className="w-full h-auto rounded-2xl"
            />
            <figcaption className="mt-4 text-center space-y-1">
              <p
                className={`font-display font-bold text-sm tracking-tight ${
                  isLight ? 'text-ls-navy' : 'text-ls-white'
                }`}
              >
                {displayTitle}
              </p>
              {asset.attribution && (
                <p className="text-[10px] font-body font-bold tracking-widest text-ls-red/70">
                  {asset.attribution}
                </p>
              )}
            </figcaption>
          </figure>
        </Reveal>
      </div>
    </section>
  );
};

export default HaomtgvInfographic;
