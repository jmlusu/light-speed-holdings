import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { MemoryRouter } from 'react-router-dom';
import { HeroSection } from '../components/HeroSection';
import { AboutSection } from '../components/AboutSection';
import { StatusBadge } from '../site/StatusBadge';
import { CategoryChip } from '../site/CategoryChip';
import { humanAuthorityStatement } from '../data/shipped/company';

afterEach(() => cleanup());

const collectSources = (dir: string): string[] =>
  readdirSync(dir).flatMap((name) => {
    const path = join(dir, name);
    return statSync(path).isDirectory() ? collectSources(path) : [path];
  });
const sourcesIn = (...dirs: string[]) =>
  dirs.flatMap(collectSources).filter((path) => /\.tsx?$/.test(path)).map((path) => ({ path, code: readFileSync(path, 'utf8') }));
const componentsAndSite = sourcesIn('src/components', 'src/site');
const pages = sourcesIn('src/pages');
const GREEN_STATUS_RE =
  /(?:bg|text|border|ring|fill|stroke|from|to|shadow)-(?:ls-)?(?:emerald|green)(?:-\d{2,4})?(?:\/\d+)?|#(?:10B981|22C55E|16A34A|34D399)\b/i;

describe('hero and human authority copy', () => {
  it('HeroSection renders the updated headline, subtitle, and canonical line', () => {
    render(<MemoryRouter><HeroSection theme="dark" onRequestBriefing={() => {}} /></MemoryRouter>);
    expect(screen.getByText('The AI-Native')).toBeTruthy();
    expect(screen.getByText('Orchestrator')).toBeTruthy();
    expect(screen.getByText('That Ships.')).toBeTruthy();
    expect(screen.getByText(/LightSpeed Holdings builds and scales AI-native solutions that turn bold ideas into real-world impact\./)).toBeTruthy();
    expect(screen.getByText('Human Direction. Intelligent Execution. Measurable Value')).toBeTruthy();
  });

  it('AboutSection renders the verbatim line "AI executes. Humans decide."', () => {
    render(<MemoryRouter><AboutSection theme="dark" onOpenContactModal={() => {}} /></MemoryRouter>);
    expect(screen.getByText('AI executes. Humans decide.')).toBeTruthy();
  });

  it('AboutSection imports humanAuthorityStatement rather than hardcoding it', () => {
    const code = readFileSync('src/components/AboutSection.tsx', 'utf8');
    expect(code).toContain("import { humanAuthorityStatement } from '../data/shipped/company';");
    expect(code).not.toContain("'AI executes. Humans decide.'");
  });
});

describe('cyan-is-trust status palette', () => {
  it('no green status token survives in src/components or src/site', () => {
    expect(componentsAndSite.filter(({ code }) => GREEN_STATUS_RE.test(code)).map(({ path }) => path)).toEqual([]);
  });

  it('no green status token survives in src/pages', () => {
    expect(pages.filter(({ code }) => GREEN_STATUS_RE.test(code)).map(({ path }) => path)).toEqual([]);
  });

  it('StatusBadge and CategoryChip use cyan trust classes without green', () => {
    const { container } = render(<><StatusBadge status="PILOT" theme="light" /><StatusBadge status="IN DEVELOPMENT" theme="dark" /><CategoryChip category="STRATEGY" theme="light" /></>);
    const classes = Array.from(container.querySelectorAll('span')).map((span) => span.className).join(' ');
    expect(classes).toContain('bg-ls-cyan/10');
    expect(classes).not.toMatch(/emerald|green/i);
  });
});

describe('brand token unification', () => {
  it('brand-tokens.css defines the AA ink tokens ls-red-ink, ls-red-cta, ls-red-bright, ls-cyan-ink, ls-grey-ink', () => {
    const tokens = readFileSync('src/brand/tokens/brand-tokens.css', 'utf8');
    for (const token of [
      '--color-ls-red-ink: #C42E3A;', '--color-ls-red-cta: #D62E3B;',
      '--color-ls-red-bright: #FF7B84;', '--color-ls-cyan-ink: #00688F;',
      '--color-ls-grey-ink: #5F6673;',
    ]) expect(tokens).toContain(token);
  });

  it('no #DC3641 duplicate red survives in marketing sources or brand tokens', () => {
    const files = [...componentsAndSite, ...pages, { path: 'src/brand/tokens/brand-tokens.css', code: readFileSync('src/brand/tokens/brand-tokens.css', 'utf8') }];
    expect(files.filter(({ code }) => /#DC3641/i.test(code)).map(({ path }) => path)).toEqual([]);
  });
});

describe('Arial-only marketing typography', () => {
  it('hero, footer and about components use Arial tokens without font-mono', () => {
    for (const path of [
      'src/components/HeroSection.tsx', 'src/components/SiteFooter.tsx',
      'src/components/AboutSection.tsx', 'src/components/home/AboutSection.tsx',
    ]) expect(readFileSync(path, 'utf8')).not.toContain('font-mono');
  });
});
