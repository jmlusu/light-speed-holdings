/**
 * Content media type contracts.
 *
 * Ported from the lsh-prototype data layer. These describe the media payloads
 * that the "what we do" sections render, and the feature-flag shape that gates
 * them. They live in their own module so they do not collide with the app's
 * existing `src/types.ts`.
 */

export type ContentMediaType = 'screenshot' | 'brand-mark' | 'diagram' | 'metrics' | 'illustration';

export interface ScreenshotMedia {
  kind: 'screenshot';
  src: string;
  alt: string;
  width: number;
  height: number;
  tone: 'light' | 'dark';
}

export interface BrandMedia {
  kind: 'brand-mark';
  src: string;
  alt: '';
  width: number;
  height: number;
}

export interface DiagramMedia {
  kind: 'diagram';
  alt: string;
  tone: 'light' | 'dark';
}

export interface MetricMedia {
  kind: 'metrics';
  alt: string;
  tone: 'light' | 'dark';
}

export interface IllustrationMedia {
  kind: 'illustration';
  src: string;
  alt: string;
  width: number;
  height: number;
  tone: 'light' | 'dark';
}

export type ContentMedia =
  | ScreenshotMedia
  | BrandMedia
  | DiagramMedia
  | MetricMedia
  | IllustrationMedia;

export interface ContentMediaSet {
  hero?: ContentMedia;
  gallery?: ContentMedia[];
  thumbnail?: ContentMedia;
}

export interface MediaFeatureFlag {
  enabled: boolean;
}
