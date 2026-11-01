import React from 'react';

interface HeroPhotoProps {
  /** Landscape image behind the copy. */
  imageSrc: string;
  imageAlt: string;
  eyebrow: string;
  /** Headline lines; wrap the accent line in a cyan span. */
  title: React.ReactNode;
  body: string;
  /** Handwritten-style annotation pinned top-right (hidden below `md`). */
  annotation?: React.ReactNode;
  /** CTAs / extra content under the body copy. */
  children?: React.ReactNode;
}

/**
 * Full-bleed photo hero: landscape image, dark-blue overlay stack, copy on the
 * left and a handwritten annotation top-right. Pulls itself up under the fixed
 * nav (`-mt-20`) so the photo runs to the top of the viewport.
 */
export const HeroPhoto: React.FC<HeroPhotoProps> = ({
  imageSrc,
  imageAlt,
  eyebrow,
  title,
  body,
  annotation,
  children,
}) => (
  <section className="relative isolate -mt-20 overflow-hidden">
    <img
      src={imageSrc}
      alt={imageAlt}
      className="absolute inset-0 -z-10 h-full w-full object-cover"
      decoding="async"
    />
    {/* Overlay stack: flat navy wash, left-to-right scrim, then a top/bottom
        gradient so nav, headline and body all keep AA contrast on the photo. */}
    <div className="absolute inset-0 -z-10 bg-ls-navy/80" aria-hidden="true" />
    <div
      className="absolute inset-0 -z-10 bg-gradient-to-r from-ls-navy via-ls-navy/85 to-ls-navy/45"
      aria-hidden="true"
    />
    <div
      className="absolute inset-0 -z-10 bg-gradient-to-t from-ls-navy via-ls-navy/10 to-ls-navy/85"
      aria-hidden="true"
    />

    <div className="relative mx-auto w-full max-w-7xl px-4 pt-36 pb-20 sm:px-8 sm:pt-44 sm:pb-24 lg:px-10">
      {annotation && (
        <div className="pointer-events-none absolute right-6 top-28 hidden max-w-[16rem] -rotate-2 text-right md:block sm:right-10 lg:right-16">
          <span className="font-annotation text-lg leading-snug text-ls-white/85 sm:text-xl">
            {annotation}
          </span>
        </div>
      )}

      <div className="max-w-2xl">
        <p className="flex items-center gap-3 text-[11px] font-bold uppercase tracking-[0.22em] text-ls-white/75">
          {eyebrow}
          <span className="h-px w-10 bg-ls-white/40" aria-hidden="true" />
        </p>

        <h1 className="mt-4 font-display text-4xl font-bold leading-[1.06] tracking-tight text-ls-white sm:text-5xl lg:text-6xl">
          {title}
        </h1>

        <p className="mt-6 max-w-xl text-sm leading-relaxed text-ls-white/80 sm:text-base">{body}</p>

        {children && <div className="mt-8 flex flex-wrap items-center gap-3">{children}</div>}
      </div>
    </div>
  </section>
);

export default HeroPhoto;
