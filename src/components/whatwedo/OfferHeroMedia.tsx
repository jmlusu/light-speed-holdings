import React from 'react';
import { HonestyBadge } from '../../components/site/HonestyBadge';
import { Reveal } from '../../components/Reveal';
import type { ContentMedia, ContentMediaSet, ScreenshotMedia, DiagramMedia, MetricMedia, BrandMedia, IllustrationMedia } from '../../types';
import { honestyLabel } from '../../data/siteContent';

/** Check if media feature is enabled (behind feature flag for phased rollout) */
const isMediaEnabled = (): boolean => {
  if (typeof window === 'undefined') return false;
  return import.meta.env.VITE_CONTENT_MEDIA_ENABLED === 'true';
};

/** Convert media kind to HonestyLabel if available */
const getBadgeLabel = (media: ContentMedia) => {
  if (media.kind === 'screenshot' || media.kind === 'illustration') {
    return undefined;
  }
  return undefined;
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
  const captionClass = `px-4 py-3 text-xs font-body leading-relaxed ${
    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
  }`;

  const renderMedia = () => {
    switch (media.kind) {
      case 'screenshot':
      case 'illustration': {
        const m = media as ScreenshotMedia | IllustrationMedia;
        return (
          <img
            src={m.src}
            alt={m.alt}
            className="w-full h-auto object-cover"
            loading={size === 'hero' ? 'eager' : 'lazy'}
          />
        );
      }
      case 'diagram': {
        return (
          <div className="w-full h-full flex items-center justify-center p-4">
            <p className="text-center text-ls-grey-light-text">Diagram: {media.alt}</p>
          </div>
        );
      }
      case 'metrics': {
        return (
          <div className="w-full h-full flex items-center justify-center p-4">
            <p className="text-center text-ls-grey-light-text">Metric: {media.alt}</p>
          </div>
        );
      }
      case 'brand-mark': {
        return (
          <img
            src={media.src}
            alt={media.alt}
            className="w-full h-auto object-contain p-4"
            loading={size === 'hero' ? 'eager' : 'lazy'}
          />
        );
      }
      default:
        return null;
    }
  };

  const badgeLabel = getBadgeLabel(media);

  return (
    <div className={containerClass}>
      <div className={`relative ${size === 'hero' ? 'aspect-video' : size === 'gallery' ? 'aspect-square' : 'aspect-square'}`}>
        {renderMedia()}
        {badgeLabel && (
          <HonestyBadge label={badgeLabel} className="absolute top-2 right-2 z-10" />
        )}
      </div>
    </div>
  );
};

/** Render offer family hero media */
export const OfferHeroMedia: React.FC<{
  media: ContentMediaSet['hero'];
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