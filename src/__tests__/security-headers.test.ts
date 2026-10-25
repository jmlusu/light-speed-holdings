import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import path from 'node:path';

/**
 * Guards the security headers served by Vercel (vercel.json).
 *
 * This is deliberately not a substring check: it parses the JSON, selects the
 * catch-all route rule, builds a key -> value map, and compares full header
 * values. The CSP is parsed into directives so a dropped source, a duplicated
 * directive, or a smuggled-in third-party origin fails the test.
 */

interface HeaderEntry {
  key: string;
  value: string;
}

interface HeadersRule {
  source: string;
  headers: HeaderEntry[];
}

const CATCH_ALL = '/(.*)';

/** The complete, exact header set the site must serve. */
const REQUIRED_HEADERS: ReadonlyArray<HeaderEntry> = [
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  {
    key: 'Permissions-Policy',
    value:
      'camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=(), display-capture=(), hid=(), serial=(), bluetooth=(), idle-detection=(), accelerometer=(), gyroscope=(), magnetometer=()',
  },
  { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
  { key: 'X-DNS-Prefetch-Control', value: 'off' },
  {
    key: 'Content-Security-Policy-Report-Only',
    value:
      "default-src 'self'; script-src 'self' https://challenges.cloudflare.com; frame-src https://challenges.cloudflare.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self' https://challenges.cloudflare.com; form-action 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; upgrade-insecure-requests",
  },
];

const CSP_KEY = 'Content-Security-Policy-Report-Only';

/** The only non-'self' origins the CSP may reference. */
const ALLOWED_CSP_ORIGINS = new Set(['https://challenges.cloudflare.com']);
const ALLOWED_CSP_SCHEMES = new Set(['data:']);

const config = JSON.parse(
  readFileSync(path.join(process.cwd(), 'vercel.json'), 'utf8'),
) as { headers?: HeadersRule[] };

const rules: HeadersRule[] = Array.isArray(config.headers) ? config.headers : [];
const catchAllRules = rules.filter((rule) => rule.source === CATCH_ALL);

/**
 * Returns the single catch-all rule's headers as a key -> value map, plus any
 * duplicated keys. Throws a readable error when the rule is missing/ambiguous
 * so every dependent test fails with the cause instead of a TypeError.
 */
function readCatchAllHeaders(): { headers: Map<string, string>; duplicates: string[] } {
  if (catchAllRules.length !== 1) {
    throw new Error(
      `vercel.json must contain exactly one "headers" entry with source "${CATCH_ALL}"; found ${catchAllRules.length}.`,
    );
  }

  const headers = new Map<string, string>();
  const duplicates: string[] = [];

  for (const entry of catchAllRules[0].headers ?? []) {
    if (headers.has(entry.key)) duplicates.push(entry.key);
    headers.set(entry.key, entry.value);
  }

  return { headers, duplicates };
}

/** Splits a CSP into name -> source tokens, recording repeated directives. */
function parseCsp(value: string): { directives: Map<string, string[]>; duplicates: string[] } {
  const directives = new Map<string, string[]>();
  const duplicates: string[] = [];

  for (const chunk of value.split(';')) {
    const directive = chunk.trim();
    if (!directive) continue;

    const [name, ...sources] = directive.split(/\s+/);
    if (directives.has(name)) duplicates.push(name);
    directives.set(name, sources);
  }

  return { directives, duplicates };
}

describe('vercel.json catch-all header rule', () => {
  it(`declares exactly one headers entry for source "${CATCH_ALL}"`, () => {
    expect(
      catchAllRules.length,
      `expected exactly 1 headers entry with source "${CATCH_ALL}", found ${catchAllRules.length}`,
    ).toBe(1);
  });

  it('has no duplicate header keys', () => {
    const { duplicates } = readCatchAllHeaders();
    expect(duplicates, `duplicate header keys: ${duplicates.join(', ')}`).toEqual([]);
  });

  it('ships all 8 required headers with exact values', () => {
    const { headers } = readCatchAllHeaders();

    for (const required of REQUIRED_HEADERS) {
      expect(
        headers.has(required.key),
        `missing required header: ${required.key}`,
      ).toBe(true);

      expect(
        headers.get(required.key),
        `wrong value for ${required.key}`,
      ).toBe(required.value);
    }
  });

  it('does not declare a second, unpaired CSP header', () => {
    const { headers } = readCatchAllHeaders();
    const cspHeaders = [...headers.keys()].filter((key) =>
      key.toLowerCase().startsWith('content-security-policy'),
    );
    const unexpected = cspHeaders.filter((key) => key !== CSP_KEY);

    expect(
      unexpected,
      `unexpected CSP header(s) — only ${CSP_KEY} is allowed: ${unexpected.join(', ')}`,
    ).toEqual([]);

    expect(
      cspHeaders,
      `missing required header: ${CSP_KEY}`,
    ).toContain(CSP_KEY);
  });
});

describe('Content-Security-Policy-Report-Only directives', () => {
  const { headers } = readCatchAllHeaders();
  const csp = headers.get(CSP_KEY) ?? '';
  const { directives, duplicates } = parseCsp(csp);

  it('uses the exact expected policy string', () => {
    expect(csp).toBe(REQUIRED_HEADERS.find((h) => h.key === CSP_KEY)?.value);
  });

  it('declares no directive twice', () => {
    expect(duplicates, `duplicated directives: ${duplicates.join(', ')}`).toEqual([]);
  });

  it('locks down default-src', () => {
    expect(directives.get('default-src')).toEqual(["'self'"]);
  });

  it('allows scripts only from self and the Turnstile host', () => {
    expect(directives.get('script-src')).toEqual([
      "'self'",
      'https://challenges.cloudflare.com',
    ]);
  });

  it('allows the Turnstile iframe frame', () => {
    expect(directives.get('frame-src')).toEqual(['https://challenges.cloudflare.com']);
  });

  it('blocks plugins via object-src none', () => {
    expect(directives.get('object-src')).toEqual(["'none'"]);
  });

  it('restricts base-uri and form-action to self', () => {
    expect(directives.get('base-uri')).toEqual(["'self'"]);
    expect(directives.get('form-action')).toEqual(["'self'"]);
  });

  it('restricts frame-ancestors to self', () => {
    expect(directives.get('frame-ancestors')).toEqual(["'self'"]);
  });

  it('allows self and data: images', () => {
    const imgSrc = directives.get('img-src') ?? [];
    expect(imgSrc, 'img-src must allow self').toContain("'self'");
    expect(imgSrc, 'img-src must allow data: URIs').toContain('data:');
  });

  it('allows self and data: fonts', () => {
    const fontSrc = directives.get('font-src') ?? [];
    expect(fontSrc, 'font-src must allow self').toContain("'self'");
    expect(fontSrc, 'font-src must allow data: fonts').toContain('data:');
  });

  it('allows connect-src only to self and the Turnstile host', () => {
    const connectSrc = directives.get('connect-src') ?? [];
    expect(connectSrc, 'connect-src must allow self').toContain("'self'");
    expect(
      connectSrc,
      'connect-src must allow the Turnstile host',
    ).toContain('https://challenges.cloudflare.com');
  });

  it("allows 'unsafe-inline' styles, which the current UI requires", () => {
    // style-src must keep 'unsafe-inline' for now. The site sets React inline
    // styles directly: 99 `style={{ ... }}` occurrences across 15 files under
    // src/ (125 `style=` attributes in total), and Framer Motion writes to
    // element.style at runtime. Narrowing this to style-src-attr is deferred.
    const styleSrc = directives.get('style-src') ?? [];
    expect(styleSrc, 'style-src must allow self').toContain("'self'");
    expect(
      styleSrc,
      "style-src must allow 'unsafe-inline' until inline styles are migrated",
    ).toContain("'unsafe-inline'");
  });

  it("references no origin other than 'self', data:, and the Turnstile host", () => {
    const offenders: string[] = [];

    for (const [name, sources] of directives) {
      for (const source of sources) {
        const looksLikeOrigin = /^(https?:)?\/\//i.test(source) || /^[a-z][a-z0-9+.-]*:\/\//i.test(source);
        if (!looksLikeOrigin) continue;
        if (ALLOWED_CSP_ORIGINS.has(source)) continue;
        offenders.push(`${name} -> ${source}`);
      }
    }

    expect(
      offenders,
      `CSP references unapproved origins: ${offenders.join(', ')}`,
    ).toEqual([]);
  });

  it('keeps every non-origin token inside the known-safe set', () => {
    const allowedTokens = new Set([
      "'self'",
      "'none'",
      "'unsafe-inline'",
      ...ALLOWED_CSP_SCHEMES,
      ...ALLOWED_CSP_ORIGINS,
      'upgrade-insecure-requests',
    ]);
    const offenders: string[] = [];

    for (const [name, sources] of directives) {
      // `upgrade-insecure-requests` is a valueless directive.
      if (sources.length === 0) {
        if (!allowedTokens.has(name)) offenders.push(`${name} (unknown valueless directive)`);
        continue;
      }
      for (const source of sources) {
        if (!allowedTokens.has(source)) offenders.push(`${name} -> ${source}`);
      }
    }

    expect(
      offenders,
      `CSP contains unexpected tokens: ${offenders.join(', ')}`,
    ).toEqual([]);
  });
});
