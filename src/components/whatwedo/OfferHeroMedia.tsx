import React from 'react';
import { Reveal } from '../../components/Reveal';
import type { ContentMedia } from '../../types';

/** Check if media feature is enabled (behind feature flag for phased rollout) */
const isMediaEnabled = (): boolean => {
  if (typeof window === 'undefined') return false;
  return import.meta.env.VITE_CONTENT_MEDIA_ENABLED === 'true';
};

/** Render a single ContentMedia item */
const MediaRenderer: React.FC<{
  media: ContentMedia;
  isLight: boolean;
  size?: 'hero' | 'gallery' | 'thumbnail';
}> = ({ media, isLight, size = 'gallery' }) => {
  const containerClass = `rounded-2xl overflow-hidden border transition-all ${
    isLight ? 'border-ls-grey-dark/30 bg-ls-white' : 'border-ls-white/15 bg-ls-navy/80'
  }`;

  const renderMedia = () => {
    switch (media.kind) {
      case 'screenshot':
      case 'illustration':
        return (
          <img
            src={media.src}
            alt={media.alt}
            className="w-full h-auto object-cover"
            loading={size === 'hero' ? 'eager' : 'lazy'}
          />
        );
      case 'diagram':
        return (
          <div className="w-full h-full flex items-center justify-center p-4">
            <p className="text-center text-ls-grey-light-text">Diagram: {media.alt}</p>
          </div>
        );
      case 'metric':
        return (
          <div className="w-full h-full flex items-center justify-center p-4">
            <p className="text-center text-ls-grey-light-text">Metric: {media.alt}</p>
          </div>
        );
      case 'brand':
        return (
          <img
            src={media.src}
            alt={media.alt}
            className="w-full h-auto object-contain p-4"
            loading={size === 'hero' ? 'eager' : 'lazy'}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className={containerClass}>
      <div className={`relative ${size === 'hero' ? 'aspect-video' : 'aspect-square'}`}>
        {renderMedia()}
      </div>
    </div>
  );
};

/** Render offer family hero media */
export const OfferHeroMedia: React.FC<{
  media?: ContentMedia;
  isLight: boolean;
}> = ({ media, isLight }) => {
  if (!media || !isMediaEnabled()) return null;
  return (
    <Reveal>
      <div className="mb-6 rounded-2xl overflow-hidden">
        <MediaRenderer media={media} isLight={isLight} size="hero" />
      </div>
    </Reveal>
  );
};
