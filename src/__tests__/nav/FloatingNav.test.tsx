import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { FloatingNav, NAV_LINKS } from '../../components/FloatingNav';

const renderNav = (
  theme: 'light' | 'dark' = 'dark',
  initialPath = '/',
  onRequestBriefing = vi.fn(),
) =>
  render(
    <MemoryRouter initialEntries={[initialPath]}>
      <FloatingNav theme={theme} onRequestBriefing={onRequestBriefing} />
    </MemoryRouter>,
  );

const primaryNav = () => screen.getByRole('navigation', { name: 'Primary' });
const toggle = () => screen.getByRole('button', { name: /toggle navigation menu/i });

describe('FloatingNav — SPEC 8-item primary navigation', () => {
  it('renders the eight SPEC links in order', () => {
    renderNav();
    const links = within(primaryNav()).getAllByRole('link');
    expect(links.map((l) => l.textContent)).toEqual([
      'Home',
      'What We Do',
      'AI Company Builder',
      'Solutions',
      'Use Cases',
      'Sectors',
      'Insights',
      'About',
    ]);
  });

  it('exports the nav array in the same SPEC order', () => {
    expect(NAV_LINKS.map((l) => l.name)).toEqual([
      'Home',
      'What We Do',
      'AI Company Builder',
      'Solutions',
      'Use Cases',
      'Sectors',
      'Insights',
      'About',
    ]);
  });

  it('points the primary CTA at /contact and does not open the briefing modal (D2)', () => {
    const onRequestBriefing = vi.fn();
    renderNav('dark', '/', onRequestBriefing);
    const cta = screen.getByRole('link', { name: 'Start a Conversation' });
    expect(cta).toHaveAttribute('href', '/contact');
    fireEvent.click(cta);
    expect(onRequestBriefing).not.toHaveBeenCalled();
  });

  it('marks the active route with aria-current="page"', () => {
    renderNav('light', '/sectors');
    const sectors = within(primaryNav()).getByRole('link', { name: 'Sectors' });
    expect(sectors).toHaveAttribute('aria-current', 'page');
    expect(within(primaryNav()).getByRole('link', { name: 'Home' })).not.toHaveAttribute('aria-current');
  });

  it('treats detail routes as their parent section', () => {
    renderNav('dark', '/use-cases/uc-js-bar');
    const useCases = within(primaryNav()).getByRole('link', { name: 'Use Cases' });
    expect(useCases).toHaveAttribute('aria-current', 'page');
  });

  it('exposes aria-expanded on the mobile toggle', () => {
    renderNav();
    expect(toggle()).toHaveAttribute('aria-expanded', 'false');
    expect(toggle()).toHaveAttribute('aria-controls', 'mobile-nav');
    fireEvent.click(toggle());
    expect(toggle()).toHaveAttribute('aria-expanded', 'true');
    fireEvent.click(toggle());
    expect(toggle()).toHaveAttribute('aria-expanded', 'false');
  });

  it('closes the mobile panel on Escape and returns focus to the toggle', () => {
    renderNav();
    fireEvent.click(toggle());
    expect(screen.getByRole('navigation', { name: 'Primary mobile' })).toBeInTheDocument();

    fireEvent.keyDown(document, { key: 'Escape' });

    expect(screen.queryByRole('navigation', { name: 'Primary mobile' })).not.toBeInTheDocument();
    expect(toggle()).toHaveFocus();
  });

  it('traps Tab focus inside the open mobile panel', () => {
    renderNav();
    fireEvent.click(toggle());
    const panel = screen.getByRole('navigation', { name: 'Primary mobile' }).parentElement!;
    const links = within(panel).getAllByRole('link');
    const first = links[0];
    const last = links[links.length - 1];

    last.focus();
    fireEvent.keyDown(document, { key: 'Tab' });
    expect(first).toHaveFocus();

    first.focus();
    fireEvent.keyDown(document, { key: 'Tab', shiftKey: true });
    expect(last).toHaveFocus();
  });
});
