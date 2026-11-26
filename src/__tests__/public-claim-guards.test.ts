import { describe, it, expect } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { aboutMetrics } from '../data/publicMetrics';
import { ENQUIRY_RESPONSE_COPY } from '../lib/enquiry';
import claimsRegistry from '../data/registries/claims-registry.json';

const root = process.cwd();
const read = (p: string) => readFileSync(join(root, p), 'utf8');
const claims = new Map(claimsRegistry.claims.map((c) => [c.id, c]));
const PUBLISHABLE = new Set(['VERIFIED', 'PROVEN_IN_HOUSE', 'PILOT', 'DEMONSTRATION', 'FIELDABLE', 'LIVE']);

describe('about-page metric tiles', () => {
  it('has exactly four tiles and no 100% absolute', () => {
    expect(aboutMetrics).toHaveLength(4);
    expect(aboutMetrics.map((m) => m.value)).not.toContain('100%');
    expect(aboutMetrics.map((m) => m.label).join(' ')).not.toMatch(/100%/);
    expect(aboutMetrics.map((m) => m.label)).not.toContain('Audit Trail Coverage');
  });

  it('grounds every tile in a publishable, externally sourced claim with a badge', () => {
    const failures: string[] = [];
    for (const metric of aboutMetrics) {
      const claim = claims.get(metric.claimId);
      if (!claim) { failures.push(`${metric.id}: unknown claim ${metric.claimId}`); continue; }
      if (!PUBLISHABLE.has(claim.classification)) failures.push(`${metric.id}: ${claim.classification} cannot back a live metric`);
      if (!claim.evidenceRef?.trim()) failures.push(`${metric.id}: empty evidenceRef`);
      if (claim.evidenceRef?.startsWith('src/lib/enquiry.ts#')) failures.push(`${metric.id}: circular self-reference`);
      if (!metric.badge?.label || !metric.badge?.tone) failures.push(`${metric.id}: missing honesty badge`);
    }
    expect(failures, failures.join('; ')).toEqual([]);
  });
});

describe('enquiry response copy', () => {
  it('is single-sourced and promises no response window', () => {
    expect(ENQUIRY_RESPONSE_COPY).toBe('A person reviews every enquiry before we respond.');
    expect(ENQUIRY_RESPONSE_COPY).not.toMatch(/business\s+days?|within\s+\d+|hour|week/i);
  });

  it('every public enquiry surface imports the canonical string', () => {
    for (const file of [
      'src/components/site/CtaBand.tsx', 'src/components/ContactSection.tsx',
      'src/components/ExecutiveBriefingModal.tsx', 'src/components/NewsletterSignup.tsx',
      'src/components/AskLightSpeed.tsx',
    ]) expect(read(file), `${file} must use ENQUIRY_RESPONSE_COPY`).toContain('ENQUIRY_RESPONSE_COPY');
  });
});

describe('unproven public-claim regression', () => {
  const walk = (dir: string): string[] =>
    readdirSync(dir).flatMap((entry) => {
      const full = join(dir, entry);
      if (statSync(full).isDirectory()) return walk(full);
      return /\.(ts|tsx|json)$/.test(entry) ? [full] : [];
    });
  const normalized = (p: string) => p.split(sep).join('/');

  it('never reintroduces the retired 100% metric copy on public surfaces', () => {
    const surfaces = [
      'src/components/AboutSection.tsx', 'src/components/BeforeAfterWorkflow.tsx',
      'src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx', 'src/data/publicMetrics.ts',
    ];
    const hits = surfaces.filter((f) => /100%/.test(read(f)));
    expect(hits, `unbadged 100% reintroduced in: ${hits.join(', ')}`).toEqual([]);
  });

  it('never reintroduces an unsupported response-time promise in public copy', () => {
    const banned = [
      'within two business days', 'within one business day',
      'We reply to qualified enquiries', 'ENQUIRY_SLA_COPY', '100% Audit Trail Coverage',
    ];
    const self = 'src/__tests__/public-claim-guards.test.ts';
    const violations: string[] = [];
    for (const dir of ['src/components', 'src/data', 'src/lib']) {
      for (const file of walk(join(root, dir))) {
        const rel = normalized(relative(root, file));
        if (rel === self) continue;
        const content = readFileSync(file, 'utf8');
        for (const phrase of banned) {
          if (content.toLowerCase().includes(phrase.toLowerCase())) violations.push(`${rel}: "${phrase}"`);
        }
      }
    }
    expect(violations, violations.join('\n')).toEqual([]);
  });
});
