import { describe, it, expect } from 'vitest';
import {
  CONTENT_CLAIMS,
  requiresEvidence,
  isPubliclyVisible,
  validateClaims,
} from '../data/governance';
import { CTAS, PRIMARY_CTA_LABEL } from '../data/ctas';
import { leadership } from '../data/leadership';
import { CAPABILITIES, capabilityTitles } from '../data/capabilities';
import { faqs } from '../data/faqs';
import { sectors, SECTOR_TIERS, sectorTierLegend } from '../data/sectors';
import { insightCategories, honestyLabel } from '../data/siteContent';

describe('content governance (MASTER_SPEC §17)', () => {
  it('CONTENT_CLAIMS is a non-empty registry', () => {
    expect(CONTENT_CLAIMS.length).toBeGreaterThan(0);
  });

  it('validateClaims(CONTENT_CLAIMS) returns no violations', () => {
    expect(validateClaims(CONTENT_CLAIMS)).toEqual([]);
  });

  it('covers every §15 registry', () => {
    const ids = CONTENT_CLAIMS.map((c) => c.id);
    for (const registry of [
      'registry.services',
      'registry.solutions',
      'registry.sectors',
      'registry.case-studies',
      'registry.insights',
      'registry.metrics',
      'registry.capabilities',
      'registry.agents',
      'registry.leadership',
      'registry.faqs',
      'registry.ctas',
    ]) {
      expect(ids).toContain(registry);
    }
  });

  it('every claim has an id, owner, and source', () => {
    for (const claim of CONTENT_CLAIMS) {
      expect(claim.id).toBeTruthy();
      expect(claim.owner).toBeTruthy();
      expect(claim.source).toBeTruthy();
    }
  });

  it('requiresEvidence matches §17 sensitive categories', () => {
    for (const category of ['client', 'financial', 'partnership', 'outcome', 'scale', 'impact'] as const) {
      expect(requiresEvidence(category)).toBe(true);
    }
    expect(requiresEvidence('general')).toBe(false);
  });

  it('isPubliclyVisible only allows published state', () => {
    expect(isPubliclyVisible('published')).toBe(true);
    expect(isPubliclyVisible('draft')).toBe(false);
    expect(isPubliclyVisible('review')).toBe(false);
    expect(isPubliclyVisible('approved')).toBe(false);
    expect(isPubliclyVisible('archived')).toBe(false);
  });

  it('flags a published scale claim without evidence', () => {
    const violations = validateClaims([
      { id: 'bad.scale', state: 'published', owner: 'cto', source: 'x.ts', category: 'scale' },
    ]);
    expect(violations).toHaveLength(1);
    expect(violations[0]).toContain('without evidence');
  });

  it('flags a claim missing owner/source', () => {
    const violations = validateClaims([
      { id: 'bad.owner', state: 'published', owner: '', source: 'x.ts', category: 'general' },
    ]);
    expect(violations).toHaveLength(1);
    expect(violations[0]).toContain('missing owner/source');
  });

  it('does not require evidence for non-published sensitive claims', () => {
    const violations = validateClaims([
      { id: 'draft.scale', state: 'draft', owner: 'cto', source: 'x.ts', category: 'scale' },
    ]);
    expect(violations).toEqual([]);
  });
});

describe('CTA registry (MASTER_SPEC §15)', () => {
  it('primary CTA is the single canonical label', () => {
    expect(CTAS.primary.label).toBe('Start a Conversation');
    expect(PRIMARY_CTA_LABEL).toBe('Start a Conversation');
    expect(CTAS.primary.to).toBe('/contact');
  });

  it('retired CTA phrasing does not return', () => {
    const labels = Object.values(CTAS).map((c) => c.label).join(' ');
    expect(labels).not.toMatch(/Book a Briefing|Executive Briefing/);
  });
});

describe('leadership registry', () => {
  it('has at least the founder with required fields', () => {
    expect(leadership.length).toBeGreaterThan(0);
    for (const leader of leadership) {
      expect(leader.id).toBeTruthy();
      expect(leader.name).toBeTruthy();
      expect(leader.initials).toBeTruthy();
      expect(leader.title).toBeTruthy();
      expect(leader.bio).toBeTruthy();
    }
  });
});

describe('capabilities registry', () => {
  it('has four unique capability titles', () => {
    expect(CAPABILITIES.length).toBe(4);
    expect(new Set(capabilityTitles).size).toBe(4);
    expect(capabilityTitles).toEqual(['Strategy', 'Build', 'Govern', 'Research & Policy']);
  });
});

describe('FAQ registry', () => {
  it('has unique ids and non-empty Q&A pairs', () => {
    expect(faqs.length).toBeGreaterThan(0);
    expect(new Set(faqs.map((f) => f.id)).size).toBe(faqs.length);
    for (const faq of faqs) {
      expect(faq.question.length).toBeGreaterThan(0);
      expect(faq.answer.length).toBeGreaterThan(0);
    }
  });
});

describe('sectors registry (MASTER_SPEC §11)', () => {
  it('defines the nine §11 sectors with unique ids', () => {
    expect(sectors).toHaveLength(9);
    expect(new Set(sectors.map((s) => s.id)).size).toBe(9);
  });

  it('uses only the four §11 evidence tiers, all present', () => {
    const tones = new Set(sectors.map((s) => s.status.tone));
    expect([...tones].sort()).toEqual(['development', 'fieldable', 'pilot', 'proven']);
    expect(Object.keys(SECTOR_TIERS)).toEqual(['proven', 'current', 'demonstration', 'future']);
  });

  it('every sector carries evidence text (only claim what we can show)', () => {
    for (const sector of sectors) {
      expect(sector.evidence, sector.id).toBeTruthy();
    }
  });

  it('tier legend covers all four tiers', () => {
    expect(sectorTierLegend).toHaveLength(4);
  });
});

describe('insight categories (MASTER_SPEC §13)', () => {
  it('matches the twelve canonical §13 categories', () => {
    expect(insightCategories).toHaveLength(12);
    expect(insightCategories).toContain('Agentic AI');
    expect(insightCategories).toContain('African AI');
    expect(new Set(insightCategories).size).toBe(12);
  });
});

describe('honesty badge label → tone mapper', () => {
  it('maps every types.ts HonestyBadge string to the right tone', () => {
    expect(honestyLabel('Fieldable in 2026').tone).toBe('fieldable');
    expect(honestyLabel('In active development').tone).toBe('development');
    expect(honestyLabel('In pilot').tone).toBe('pilot');
    expect(honestyLabel('In pilot (composing evidence)').tone).toBe('pilot');
    expect(honestyLabel('In pilot (proposed)').tone).toBe('pilot');
    expect(honestyLabel('Proven in-house').tone).toBe('proven');
    expect(honestyLabel('Live proof').tone).toBe('proven');
    expect(honestyLabel('Published').tone).toBe('proven');
  });

  it('preserves the original label text', () => {
    expect(honestyLabel('Proven in-house').label).toBe('Proven in-house');
  });
});
