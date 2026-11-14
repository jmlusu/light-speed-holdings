import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { HaomtgvPage } from '../../pages/HAOMTGVPage';

/**
 * HAOMTGV framework page contract.
 *
 * The prototype redesign replaced the old seven-pillar card grid with a hero +
 * four narrative sections (paradigm, dimensions explorer, governance matrix,
 * closed-loop execution) + a closing CTA. These assertions cover the page's
 * semantic structure and its links, not its decorative Tailwind tokens.
 */

const mockOnRequestBriefing = vi.fn();

const renderPage = (theme: 'light' | 'dark' = 'dark') =>
  render(
    <MemoryRouter>
      <HaomtgvPage theme={theme} onRequestBriefing={mockOnRequestBriefing} />
    </MemoryRouter>,
  );

describe('HaomtgvPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the hero eyebrow "OPERATING ARCHITECTURE" in red', () => {
    renderPage('dark');
    const eyebrow = screen.getByText('OPERATING ARCHITECTURE');
    expect(eyebrow.parentElement).toHaveClass('text-ls-red');
  });

  it('renders the page H1 with id="haomtgv-title"', () => {
    renderPage('light');
    const h1 = screen.getByRole('heading', { level: 1 });
    expect(h1).toHaveAttribute('id', 'haomtgv-title');
    expect(h1).toHaveTextContent('H-A-O-M-T-G-V');
  });

  it('renders the hero subtitle naming human authority and measured value', () => {
    renderPage('dark');
    expect(
      screen.getByText('Human Authority. Governed Agents. Measured Value.'),
    ).toBeInTheDocument();
  });

  it('renders the official tagline badge', () => {
    renderPage('dark');
    expect(screen.getByText('ASPIRE. ACT. ACHIEVE.')).toBeInTheDocument();
  });

  it('renders a three-segment brand bar at the top and bottom of the page', () => {
    renderPage('light');
    const bars = document.querySelectorAll('div[style*="background-color"]');
    // 3 segments in the hero + 3 in the closing brand bar.
    expect(bars.length).toBe(6);
  });

  it('renders the hero action buttons and anchors', () => {
    renderPage('dark');
    expect(
      screen.getByRole('button', { name: /Request Architecture Briefing/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Explore 7 Dimensions/i })).toHaveAttribute(
      'href',
      '#dimensions-explorer',
    );
    expect(screen.getByRole('link', { name: /Approval Matrix/i })).toHaveAttribute(
      'href',
      '#governance-matrix',
    );
  });

  it('requests an architecture briefing from the hero CTA', () => {
    renderPage('dark');
    fireEvent.click(screen.getByRole('button', { name: /Request Architecture Briefing/i }));
    expect(mockOnRequestBriefing).toHaveBeenCalledTimes(1);
    expect(mockOnRequestBriefing).toHaveBeenCalledWith(
      expect.stringContaining('HAOMTGV Operating Architecture Briefing'),
    );
  });

  it('renders the architectural paradigm section', () => {
    renderPage('dark');
    expect(screen.getByText('THE ARCHITECTURAL PARADIGM')).toBeInTheDocument();
    expect(
      screen.getByText('Beyond Black-Box Prompts: Governed Enterprise Execution'),
    ).toBeInTheDocument();
  });

  it('renders the seven-dimensions explorer anchor target', () => {
    renderPage('dark');
    expect(screen.getByText('THE SEVEN DIMENSIONS')).toBeInTheDocument();
    expect(screen.getByText('Unified Operating Architecture')).toBeInTheDocument();
    expect(document.getElementById('dimensions-explorer')).not.toBeNull();
  });

  it('renders the five-tier governance matrix anchor target', () => {
    renderPage('dark');
    expect(screen.getByText('CONTINUOUS GOVERNANCE FABRIC')).toBeInTheDocument();
    expect(screen.getByText('The Five-Tier Human Approval Matrix')).toBeInTheDocument();
    expect(document.getElementById('governance-matrix')).not.toBeNull();
  });

  it('renders the closed-loop execution section', () => {
    renderPage('light');
    expect(screen.getByText('CLOSED-LOOP EXECUTION')).toBeInTheDocument();
    expect(screen.getByText('How the Architecture Executes Work')).toBeInTheDocument();
  });

  it('renders the closing CTA with the canonical primary label', () => {
    renderPage('dark');
    expect(screen.getByText('ENTERPRISE DEPLOYMENT')).toBeInTheDocument();
    expect(
      screen.getByRole('heading', {
        level: 2,
        name: 'Ready to Deploy Governed AI in Your Organization?',
      }),
    ).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /ENGAGE LIGHTSPEED/i })).toBeInTheDocument();
  });

  it('renders the related architectural links', () => {
    renderPage('dark');
    expect(screen.getByRole('link', { name: /Sectors/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Solutions/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /What We Do/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Pharos Insights/i })).toBeInTheDocument();
  });

  it('applies the light theme hero gradient', () => {
    renderPage('light');
    const hero = screen.getByRole('heading', { level: 1 }).closest('section');
    expect(hero).toHaveClass('from-ls-navy');
  });

  it('applies the dark theme hero gradient', () => {
    renderPage('dark');
    const hero = screen.getByRole('heading', { level: 1 }).closest('section');
    expect(hero).toHaveClass('from-ls-navy-dark');
  });
});
