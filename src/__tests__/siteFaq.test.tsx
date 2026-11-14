import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { readFileSync } from 'node:fs';
import { SiteFooter } from '../components/SiteFooter';
import { FaqSection } from '../components/site/FaqSection';

/**
 * Footer → FAQ contract: the footer's single FAQ link must reach the FAQ surface.
 * It targets the dedicated /faq page (the prototype IA promoted FAQ out of the
 * home-page anchor into its own route); the home page still mounts FaqSection with
 * id="faq" for direct anchor links.
 */

describe('footer FAQ contract', () => {
  it('SiteFooter renders exactly one FAQ link, href "/faq"', () => {
    render(
      <MemoryRouter>
        <SiteFooter theme="dark" />
      </MemoryRouter>,
    );
    const faqLinks = screen.getAllByRole('link', { name: /FAQ|Frequently Asked Questions/i });
    expect(faqLinks).toHaveLength(1);
    expect(faqLinks[0].getAttribute('href')).toBe('/faq');
  });

  it('App declares the /faq route the footer links to', () => {
    const app = readFileSync('src/App.tsx', 'utf8');
    expect(app).toMatch(/path:\s*["']\/?faq["']/);
  });

  it('FaqSection exposes id="faq" with sticky-header scroll offset', () => {
    const { container } = render(<FaqSection theme="light" id="faq" />);
    const section = container.querySelector('section');
    expect(section).not.toBeNull();
    expect(section?.getAttribute('id')).toBe('faq');
    expect(section?.className).toContain('scroll-mt-28');
  });

  it('HomePage mounts FaqSection with id="faq" (footer link resolves on home)', () => {
    const home = readFileSync('src/pages/HomePage.tsx', 'utf8');
    expect(home).toMatch(/<FaqSection[^>]*\bid="faq"/);
  });
});
