import React from 'react';
import { HonestyBadge } from '../../components/site/HonestyBadge';
import type { ContentMedia, ContentMediaSet, ScreenshotMedia, BrandMedia, IllustrationMedia } from '../../types';
import { honestyLabel } from '../../data/siteContent';

/** Check if media feature is enabled (behind feature flag for phased rollout) */
const isMediaEnabled = (): boolean => {
  if (typeof window === 'undefined') return false;
  return import.meta.env.VITE_CONTENT_MEDIA_ENABLED === 'true';
};

/** Render solution thumbnail media */
export const SolutionThumbnailMedia: React.FC<{
  media: ContentMediaSet['thumbnail'];
  isLight: boolean;
}> = ({ media, isLight }) => {
  if (!media || !isMediaEnabled()) return null;
  const containerClass = `rounded-xl overflow-hidden border transition-all ${
    isLight ? 'border-ls-grey-dark/30 bg-ls-white' : 'border-ls-white/15 bg-ls-navy/80'
  }`;

  const renderThumbnail = () => {
    if (!media) return null;
    switch (media.kind) {
      case 'screenshot':
      case 'illustration': {
        const m = media as ScreenshotMedia | IllustrationMedia;
        return (
          <img
            src={m.src}
            alt={m.alt}
            className="w-full h-full object-cover"
            loading="lazy"
          />
        );
      }
      case 'brand-mark': {
        const m = media as BrandMedia;
        return (
          <img
            src={m.src}
            alt={m.alt}
            className="w-full h-full object-contain p-2"
            loading="lazy"
          />
        );
      }
      case 'diagram':
      case 'metrics':
        return (
          <div className="w-full h-full flex items-center justify-center p-2">
            <p className="text-center text-xs text-ls-grey-light-text">{media.kind}</p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={containerClass}>
      <div className="relative aspect-square">
        {renderThumbnail()}
      </div>
    </div>
  );
};