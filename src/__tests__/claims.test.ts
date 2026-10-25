import { describe, it, expect } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import registry from '../data/generated/agent-registry.public.json';

/**
 * Guard for the canonical operating-model claim (docs/website/SPEC.md):
 * "90 operating roles. 89 AI agents. One Human CEO."
 *
 * The registry is the single source of truth; marketing copy must not drift
 * back to the retired "90 AI agents" / "91 agents" phrasings.
 */

interface PublicAgent {
  id: string;
  type: string;
}

const agents = registry.agents as PublicAgent[];

describe('canonical agent counts', () => {
  it('registry defines 90 operating roles', () => {
    expect(agents).toHaveLength(90);
    expect(registry.meta.agents).toBe(90);
  });

  it('contains exactly one Human CEO entry', () => {
    const humanCeo = agents.filter((a) => a.id === 'human-ceo');
    expect(humanCeo).toHaveLength(1);
    expect(humanCeo[0].type).toBe('executive');
  });

  it('contains 89 AI agents alongside the Human CEO', () => {
    expect(agents.filter((a) => a.id !== 'human-ceo')).toHaveLength(89);
  });
});

/**
 * Copy guard. Published insight articles keep their original body text for the
 * audit trail and carry a dated correction note instead (see `correction` in
 * src/data/insights.ts). Their historical titles are mirrored in siteContent.ts.
 * The claims registry keeps historical counts on purpose.
 */
const ALLOWED: { file: string; patterns: string[] }[] = [
  { file: 'src/data/insights.ts', patterns: ['*'] },
  { file: 'src/data/siteContent.ts', patterns: ['90-Agent'] },
  { file: 'src/data/registries/claims-registry.json', patterns: ['*'] },
  { file: 'src/data/registries/metrics-registry.json', patterns: ['*'] },
];

const FORBIDDEN = [
  ['90', 'AI', 'agents'].join(' '),
  ['90', 'specialized', 'AI', 'agents'].join(' '),
  ['91', 'agents'].join(' '),
  ['91', 'agent'].join('-'),
  ['90', 'agents', 'and', '1', 'human'].join(' '),
];

const walk = (dir: string): string[] =>
  readdirSync(dir).flatMap((entry) => {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) return walk(full);
    return /\.(ts|tsx|json)$/.test(entry) ? [full] : [];
  });

const normalized = (p: string) => p.split(sep).join('/');

describe('public copy uses the canonical operating-model phrasing', () => {
  it('has no retired agent-count phrasing outside the documented allowlist', () => {
    const root = process.cwd();
    const violations: string[] = [];

    for (const file of walk(join(root, 'src'))) {
      const rel = normalized(relative(root, file));
      if (rel === 'src/__tests__/claims.test.ts') continue;

      const allowed = ALLOWED.find((entry) => rel === entry.file);
      const content = readFileSync(file, 'utf8');

      for (const pattern of FORBIDDEN) {
        if (allowed && (allowed.patterns.includes('*') || allowed.patterns.includes(pattern))) continue;
        if (content.includes(pattern)) violations.push(`${rel}: "${pattern}"`);
      }
    }

    expect(violations).toEqual([]);
  });
});
