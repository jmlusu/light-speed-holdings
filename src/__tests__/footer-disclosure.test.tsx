import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { SiteFooter } from '../components/SiteFooter';

/**
 * Imagery disclosure contract.
 *
 * Every illustration and architectural diagram the site renders is an authored
 * asset in `public/` or `src/assets/` (see
 * src/data/registries/media-registry.json), so the footer may state that they are
 * original in-house vector artwork. The sentence is deliberately narrow: it says
 * nothing about photography, which the registry does not prove for every asset.
 */

const DISCLOSURE =
  'Illustrations and architectural diagrams are original vector artwork created in-house.';

describe('footer imagery disclosure', () => {
  it('renders the exact in-house vector artwork sentence', () => {
    render(
      <MemoryRouter>
        <SiteFooter theme="dark" />
      </MemoryRouter>,
    );

    expect(
      screen.getByText(DISCLOSURE),
      `SiteFooter must render the exact sentence: "${DISCLOSURE}"`,
    ).toBeInTheDocument();
  });

  it('places the disclosure inside the footer legal/meta row', () => {
    const { container } = render(
      <MemoryRouter>
        <SiteFooter theme="light" />
      </MemoryRouter>,
    );

    const footer = container.querySelector('footer');
    expect(footer).not.toBeNull();

    const disclosure = screen.getByText(DISCLOSURE);
    expect(
      footer?.contains(disclosure),
      'The disclosure must be rendered inside the <footer> element.',
    ).toBe(true);

    const legalBlock = disclosure.parentElement;
    expect(
      legalBlock,
      'The disclosure should sit in the footer legal block beside the copyright line.',
    ).not.toBeNull();
    expect(legalBlock?.textContent).toContain('All rights reserved.');
  });
});
