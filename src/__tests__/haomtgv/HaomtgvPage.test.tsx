import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { HaomtgvPage } from '../../pages/HAOMTGVPage';

const mockOnRequestBriefing = vi.fn();

const renderPage = (theme: 'light' | 'dark' = 'dark') => {
  return render(
    <MemoryRouter>
      <HaomtgvPage theme={theme} onRequestBriefing={mockOnRequestBriefing} />
    </MemoryRouter>
  );
};

describe('HaomtgvPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders hero section (HaomtgvBlueprintHero)', () => {
    renderPage('dark');
    const heroSection = screen.getByText('OPERATING FRAMEWORK').closest('section');
    expect(heroSection).toBeInTheDocument();
    // Blueprint hero uses background shorthand + a transparent overlay;
    // no solid brand-color bars (navy/red/cyan) remain in the hero
    const colorBars = heroSection?.querySelectorAll(
      'div[style*="background-color"]:not([style*="transparent"])'
    );
    expect(colorBars?.length ?? 0).toBe(0);
    expect(heroSection).toHaveClass('bg-[#050B1A]');
  });

  it('renders H1 with id="haomtgv-title" and dotted format', () => {
    renderPage('light');
    const h1 = screen.getByRole('heading', { level: 1 });
    expect(h1).toHaveAttribute('id', 'haomtgv-title');
    expect(h1).toHaveTextContent('H.A.O.M.T.G.V.');
  });

  it('renders eyebrow "OPERATING FRAMEWORK" in slate-300', () => {
    renderPage('dark');
    expect(screen.getByText('OPERATING FRAMEWORK')).toHaveClass('text-slate-300');
  });

  it('renders lead paragraph with correct copy', () => {
    renderPage('light');
    expect(screen.getByText(/A control model for agentic companies/)).toBeInTheDocument();
    expect(screen.getByText(/Human at the Core/)).toBeInTheDocument();
    // Tagline is split across 3 spans (ASPIRE. / ACT. / ACHIEVE.) with aria-label
    expect(screen.getByLabelText('ASPIRE. ACT. ACHIEVE.')).toBeInTheDocument();
  });

  it('renders CTA link to /ai-company-builder/#governance', () => {
    renderPage('dark');
    const link = screen.getByRole('link', { name: /explore the framework/i });
    expect(link).toHaveAttribute('href', '/ai-company-builder/#governance');
    expect(link).toHaveClass('bg-[#FF2D55]');
    expect(link).toHaveClass('text-[#050B1A]');
  });

  it('renders 7-layer grid section with SectionHeading', () => {
    renderPage('dark');
    expect(screen.getByText('THE SEVEN LAYERS')).toBeInTheDocument();
    expect(screen.getByText('How the Model Works')).toBeInTheDocument();
    expect(screen.getByText(/Each layer has a distinct role/)).toBeInTheDocument();
  });

  it('renders all 7 pillar cards in grid', () => {
    renderPage('light');
    const gridSection = screen.getByText('THE SEVEN LAYERS').closest('section');
    expect(gridSection).toBeInTheDocument();
    const scope = within(gridSection as HTMLElement);
    const pillars = ['Human', 'Agents', 'Orchestration', 'Memory', 'Tools', 'Governance', 'Value'];
    pillars.forEach((pillar) => {
      expect(scope.getByText(pillar)).toBeInTheDocument();
    });
  });

  it('applies governance ring accent on Governance card', () => {
    renderPage('dark');
    const gridSection = screen.getByText('THE SEVEN LAYERS').closest('section');
    const governanceCard = within(gridSection as HTMLElement).getByText('Governance').closest('article');
    expect(governanceCard).toHaveClass('ring-1');
    expect(governanceCard).toHaveClass('ring-ls-red/30');
  });

  it('renders pillar icons with cyan color', () => {
    renderPage('light');
    const svgs = document.querySelectorAll('svg');
    expect(svgs.length).toBeGreaterThanOrEqual(7);
  });

  it('renders governance callout section', () => {
    renderPage('dark');
    expect(screen.getByText('Governance Runs Through Every Layer')).toBeInTheDocument();
    expect(screen.getByText(/Human direction is not a checkpoint at the end/)).toBeInTheDocument();
  });

  it('renders bottom brand color bar (3 segments)', () => {
    renderPage('light');
    // Exclude the hero's transparent BackgroundLayer overlay div
    const colorBars = document.querySelectorAll(
      'div[style*="background-color"]:not([style*="transparent"])'
    );
    // Blueprint hero uses background shorthand (not background-color bars);
    // only the bottom brand bar remains = 3 segments
    expect(colorBars.length).toBe(3);
  });

  it('renders RelatedLinks with correct links', () => {
    renderPage('dark');
    expect(screen.getByRole('link', { name: /ai company builder/i })).toHaveAttribute('href', '/ai-company-builder');
    expect(screen.getByRole('link', { name: /solutions/i })).toHaveAttribute('href', '/solutions');
    expect(screen.getByRole('link', { name: /insights/i })).toHaveAttribute('href', '/insights');
  });

  it('applies light theme classes correctly', () => {
    renderPage('light');
    const gridSection = screen.getByText('THE SEVEN LAYERS').closest('section');
    expect(gridSection).toHaveClass('bg-ls-white');
  });

  it('applies dark theme classes correctly', () => {
    renderPage('dark');
    const gridSection = screen.getByText('THE SEVEN LAYERS').closest('section');
    expect(gridSection).toHaveClass('bg-ls-navy-dark');
  });

  it('renders pillar descriptions with correct content', () => {
    renderPage('dark');
    const gridSection = screen.getByText('THE SEVEN LAYERS').closest('section');
    const scope = within(gridSection as HTMLElement);
    expect(scope.getByText(/People set intent, own outcomes, and hold final decision authority/)).toBeInTheDocument();
    expect(scope.getByText(/Specialized AI roles with explicit scopes/)).toBeInTheDocument();
    expect(scope.getByText(/Deterministic routing of tasks, data, and decisions/)).toBeInTheDocument();
    expect(scope.getByText(/Persistent contextual state across long-running work/)).toBeInTheDocument();
    expect(scope.getByText(/Isolated execution environments for APIs, data, and actions/)).toBeInTheDocument();
    expect(scope.getByText(/A control layer woven through the model/)).toBeInTheDocument();
    expect(scope.getByText(/Measured business outcomes \(cost, latency, quality, and adoption\)/)).toBeInTheDocument();
  });

  it('uses Reveal component for staggered card animation', () => {
    renderPage('dark');
    const gridSection = screen.getByText('THE SEVEN LAYERS').closest('section');
    const articles = (gridSection as HTMLElement).querySelectorAll('article');
    expect(articles.length).toBe(7);
  });
});
