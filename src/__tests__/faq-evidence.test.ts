import { describe, it, expect } from 'vitest';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { faqs } from '../data/faqs';

/**
 * Evidence guard for the FAQ surface (docs/website/SPEC.md § FAQ).
 *
 * Two collections carry FAQ answers:
 *   - src/data/registries/faq-registry.json - the canonical 28-entry set
 *   - src/data/faqs.ts                       - the 6 answers the site renders
 *
 * Every entry in both must carry at least one evidence entry. A `verified`
 * entry has to resolve to something a reader can open: either a claim id in
 * claims-registry.json whose classification is publishable, or a repo path
 * plus literal anchor text that the file actually contains. An unsupportable
 * answer belongs in `unknown` with a note - never `verified`.
 *
 * JSON is read with fs (not imported) so the guard does not depend on the
 * bundler's JSON module handling.
 */

interface EvidenceEntry {
  source: string;
  status: string;
  note?: string;
}

interface FaqLike {
  id: string;
  evidence?: EvidenceEntry[];
}

const root = process.cwd();

const readJson = (relativePath: string): Record<string, unknown> =>
  JSON.parse(readFileSync(join(root, relativePath), 'utf8')) as Record<string, unknown>;

const faqRegistry = readJson('src/data/registries/faq-registry.json') as {
  description: string;
  lastUpdated: string;
  faqs: FaqLike[];
};

const claimsRegistry = readJson('src/data/registries/claims-registry.json') as {
  claims: { id: string; classification: string }[];
};

const claimsById = new Map(claimsRegistry.claims.map((claim) => [claim.id, claim]));
const registryIds = new Set(faqRegistry.faqs.map((faq) => faq.id));

/** A source with no slash is treated as a claim id; anything else is path#anchor. */
const isClaimId = (source: string): boolean => !source.includes('/');

const collections: { label: string; entries: FaqLike[] }[] = [
  { label: 'faq-registry.json', entries: faqRegistry.faqs },
  { label: 'faqs.ts (rendered)', entries: faqs as unknown as FaqLike[] },
];

describe('FAQ registry shape', () => {
  it('holds exactly the 28 canonical entries and says so in its description', () => {
    // Pinned literal: this set is a contract, not a computed length.
    expect(faqRegistry.faqs).toHaveLength(28);
    expect(faqRegistry.description).toContain('28');
    expect(faqRegistry.description).toContain('all 28 entries carry evidence entries');
    expect(faqRegistry.lastUpdated).toBe('2026-10-25');
  });

  it('states the real verified/unknown counts in the description', () => {
    const all = faqRegistry.faqs.flatMap((faq) => faq.evidence ?? []);
    const verified = all.filter((entry) => entry.status === 'verified').length;
    const unknown = all.filter((entry) => entry.status === 'unknown').length;

    expect(faqRegistry.description).toContain(`(${verified} verified, ${unknown} unknown)`);
    expect(verified + unknown).toBe(all.length);
  });
});

describe('every FAQ entry carries evidence', () => {
  it('gives all 28 registry entries a non-empty evidence array', () => {
    const missing = faqRegistry.faqs
      .filter((faq) => !Array.isArray(faq.evidence) || faq.evidence.length === 0)
      .map((faq) => faq.id);

    expect(missing, `registry entries without evidence: ${missing.join(', ')}`).toEqual([]);
  });

  it('gives all 6 rendered FAQs evidence and a resolvable registryId', () => {
    const problems: string[] = [];

    for (const faq of faqs) {
      if (!Array.isArray(faq.evidence) || faq.evidence.length === 0) {
        problems.push(`${faq.id}: rendered FAQ has no evidence`);
      }
      if (!faq.registryId) {
        problems.push(`${faq.id}: rendered FAQ has no registryId`);
      } else if (!registryIds.has(faq.registryId)) {
        problems.push(`${faq.id}: registryId "${faq.registryId}" is not in faq-registry.json`);
      }
    }

    expect(problems, problems.join('; ')).toEqual([]);
    expect(faqs).toHaveLength(6);
  });
});

describe('verified evidence must resolve to an openable source', () => {
  it('resolves every verified claim id and every path#anchor', () => {
    const failures: string[] = [];

    for (const { label, entries } of collections) {
      for (const faq of entries) {
        for (const entry of faq.evidence ?? []) {
          if (entry.status !== 'verified') continue;

          const where = `${label} ${faq.id}`;

          if (isClaimId(entry.source)) {
            const claim = claimsById.get(entry.source);
            if (!claim) {
              failures.push(`${where}: claim "${entry.source}" does not exist in claims-registry.json`);
              continue;
            }
            if (claim.classification === 'UNVERIFIED' || claim.classification === 'UNKNOWN') {
              failures.push(
                `${where}: claim "${entry.source}" is classified ${claim.classification} and cannot back a verified answer`,
              );
            }
            continue;
          }

          const hashAt = entry.source.indexOf('#');
          if (hashAt < 1 || hashAt === entry.source.length - 1) {
            failures.push(`${where}: source "${entry.source}" is neither a claim id nor path#anchor`);
            continue;
          }

          const relativePath = entry.source.slice(0, hashAt);
          const anchor = entry.source.slice(hashAt + 1);
          const absolutePath = join(root, relativePath);

          if (!existsSync(absolutePath)) {
            failures.push(`${where}: source "${entry.source}" - file "${relativePath}" does not exist`);
            continue;
          }

          if (!readFileSync(absolutePath, 'utf8').includes(anchor)) {
            failures.push(
              `${where}: source "${entry.source}" - anchor text not found verbatim in ${relativePath}`,
            );
          }
        }
      }
    }

    expect(failures, failures.join('\n')).toEqual([]);
  });

  it('never marks an entry verified without a source', () => {
    const failures: string[] = [];

    for (const { label, entries } of collections) {
      for (const faq of entries) {
        for (const entry of faq.evidence ?? []) {
          if (entry.status === 'verified' && (!entry.source || entry.source.trim() === '')) {
            failures.push(`${label} ${faq.id}: verified entry has an empty source`);
          }
        }
      }
    }

    expect(failures, failures.join('; ')).toEqual([]);
  });
});
