import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { StatusBadge } from '../site/StatusBadge';
import { CategoryChip } from '../site/CategoryChip';
import { BADGE_BASE_CLASSES, EVIDENCE_STATUS_CLASSES, TONE_STYLES, honestyLabel } from '../data/siteContent';
import { faqs } from '../data/faqs';

const root = resolve(__dirname, '..', '..');
const css = readFileSync(resolve(root, 'src/brand/tokens/brand-tokens.css'), 'utf8');
const token = (name: string): string => {
  const match = css.match(new RegExp(`--color-ls-${name}:\\s*(#[0-9A-Fa-f]{6})\\s*;`));
  if (!match) throw new Error(`missing --color-ls-${name} in brand-tokens.css`);
  return match[1].toUpperCase();
};
const luminance = (hex: string): number => {
  const channels = [1, 3, 5].map((start) => {
    const value = parseInt(hex.slice(start, start + 2), 16) / 255;
    return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
};
const contrast = (fg: string, bg: string): number => {
  const a = luminance(fg), b = luminance(bg);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
};
const INK = {
  proven: { light: 'cyan-ink', dark: 'cyan' },
  pilot: { light: 'red-ink', dark: 'red-bright' },
  fieldable: { light: 'grey-ink', dark: 'grey-soft' },
  development: { light: 'grey-deep', dark: 'grey-light-text' },
} as const;
const SURFACE = { light: '#FFFFFF', dark: '#070A40' } as const;
const tones = ['proven', 'pilot', 'fieldable', 'development'] as const;

describe('honesty badge tone map', () => {
  it('keeps exactly the four canonical tones', () => {
    expect(Object.keys(TONE_STYLES).sort()).toEqual(['development', 'fieldable', 'pilot', 'proven']);
  });

  it('preserves label-to-tone mapping for every published badge string', () => {
    expect(honestyLabel('Proven in-house').tone).toBe('proven');
    expect(honestyLabel('Live proof').tone).toBe('proven');
    expect(honestyLabel('Published').tone).toBe('proven');
    expect(honestyLabel('In pilot').tone).toBe('pilot');
    expect(honestyLabel('In pilot (composing evidence)').tone).toBe('pilot');
    expect(honestyLabel('Fieldable in 2026').tone).toBe('fieldable');
    expect(honestyLabel('In active development').tone).toBe('development');
    expect(honestyLabel('Proven in-house').label).toBe('Proven in-house');
  });
});

describe('honesty badge contrast', () => {
  for (const tone of tones) {
    it(`keeps ${tone} text at AA or better in light and dark`, () => {
      expect(contrast(token(INK[tone].light), SURFACE.light)).toBeGreaterThanOrEqual(4.5);
      expect(contrast(token(INK[tone].dark), SURFACE.dark)).toBeGreaterThanOrEqual(4.5);
    });
  }
});

describe('honesty badge rendering', () => {
  it('renders every tone with the shared 12px base and its own AA ink', () => {
    const cases = [
      ['Proven in-house', 'text-ls-cyan-ink'],
      ['In pilot', 'text-ls-red-ink'],
      ['Fieldable in 2026', 'text-ls-grey-ink'],
      ['In active development', 'text-ls-grey-deep'],
    ] as const;
    for (const [label, ink] of cases) {
      const { container, unmount } = render(<HonestyBadge label={honestyLabel(label)} />);
      const badge = container.firstElementChild as HTMLElement;
      expect(badge.textContent).toContain(label);
      expect(badge).toHaveClass('text-xs');
      expect(badge).toHaveClass('border');
      expect(badge).toHaveClass(ink);
      unmount();
    }
    expect(BADGE_BASE_CLASSES).toContain('text-xs');
  });

  it('uses no green or amber classes on badge surfaces', () => {
    for (const tone of tones) expect(TONE_STYLES[tone]).not.toMatch(/emerald|green|amber|lime/);
    for (const file of ['src/components/FaqCardList.tsx', 'src/components/whatwedo/SixCapabilitiesSection.tsx']) {
      expect(readFileSync(resolve(root, file), 'utf8')).not.toMatch(/emerald|amber/);
    }
  });
});

describe('FAQ evidence chips', () => {
  // vitest.config.ts does not carry vite.config.ts's @lightspeed/design-system
  // alias, so FaqCardList cannot be imported here. Render the exact chip markup
  // from real registry data, and pin the component source separately below.
  it('renders verified evidence in brand cyan and unknown in brand grey', () => {
    const { container } = render(
      <>
        {faqs[0].evidence.map((ev, i) => (
          <span key={i} className={`px-2 py-0.5 rounded border text-xs font-mono ${EVIDENCE_STATUS_CLASSES[ev.status]}`}>
            {ev.source} ({ev.status})
          </span>
        ))}
      </>,
    );
    const verified = screen.getByText(/claim\.agent-count \(verified\)/);
    expect(verified).toHaveClass('text-ls-cyan-ink');
    expect(verified).not.toHaveClass('text-emerald-700');
    expect(EVIDENCE_STATUS_CLASSES.verified).toContain('text-ls-cyan-ink');
    expect(EVIDENCE_STATUS_CLASSES.unknown).toContain('text-ls-grey-deep');
    expect(container.querySelector('.bg-amber-50')).toBeNull();

    const faqCardSource = readFileSync(resolve(root, 'src/components/FaqCardList.tsx'), 'utf8');
    expect(faqCardSource).toContain('EVIDENCE_STATUS_CLASSES[ev.status]');
    expect(faqCardSource).toContain('{ev.source} ({ev.status})');
    expect(faqCardSource).not.toContain('bg-emerald-50');
    expect(faqCardSource).not.toContain('bg-amber-50');
  });

  it('keeps evidence status labels verbatim instead of reclassifying them as maturity tiers', () => {
    const faqSource = readFileSync(resolve(root, 'src/data/faqs.ts'), 'utf8');
    expect(faqSource).toContain("status: 'verified'");
    expect(faqSource).not.toMatch(/status:\s*'(proven|pilot|fieldable|development)'/);
  });
});

describe('companion badges', () => {
  it('renders StatusBadge and CategoryChip at 12px, not 10px', () => {
    const status = render(<StatusBadge status="PILOT" theme="light" />);
    const category = render(<CategoryChip category="STRATEGY" theme="light" />);
    const statusBadge = status.container.firstElementChild as HTMLElement;
    const categoryBadge = category.container.firstElementChild as HTMLElement;
    expect(statusBadge).toHaveClass('text-xs');
    expect(categoryBadge).toHaveClass('text-xs');
    expect(statusBadge.className).not.toContain('text-[10px]');
    expect(categoryBadge.className).not.toContain('text-[10px]');
  });
});
