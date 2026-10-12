import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { readFileSync } from 'node:fs';
import { SiteFooter } from '../components/SiteFooter';
import { FaqSection } from '../components/site/FaqSection';

/**
 * Footer → FAQ anchor contract: the footer's single FAQ link (/#faq) must
 * target an id="faq" section mounted on the home page with a scroll offset
 * for the sticky header. Guards the wiring shipped in PR #445.
 */

describe('footer FAQ anchor contract', () => {
  it('SiteFooter renders exactly one FAQ link, href "/#faq"', () => {
    render(
      <MemoryRouter>
        <SiteFooter theme="dark" />
      </MemoryRouter>,
    );
    const faqLinks = screen.getAllByRole('link', { name: 'FAQ' });
    expect(faqLinks).toHaveLength(1);
    expect(faqLinks[0].getAttribute('href')).toBe('/#faq');
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
