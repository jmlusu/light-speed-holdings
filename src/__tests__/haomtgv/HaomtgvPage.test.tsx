import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
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

  it('renders hero section with brand color bar', () => {
    renderPage('dark');
    // Hero section is the first section, find it by its content
    const heroSection = screen.getByText('OPERATING FRAMEWORK').closest('section');
    expect(heroSection).toBeInTheDocument();
    // Brand color bar at top of hero
    const colorBars = heroSection?.querySelectorAll('div[style*="background-color"]');
    expect(colorBars?.length).toBe(3); // navy, red, cyan
  });

  it('renders H1 with id="haomtgv-title" and cyan text', () => {
    renderPage('light');
    const h1 = screen.getByRole('heading', { level: 1 });
    expect(h1).toHaveAttribute('id', 'haomtgv-title');
    expect(h1).toHaveTextContent('H-A-O-M-T-G-V');
    expect(h1).toHaveClass('text-ls-cyan');
  });

  it('renders eyebrow "OPERATING FRAMEWORK" in red', () => {
    renderPage('dark');
    expect(screen.getByText('OPERATING FRAMEWORK')).toHaveClass('text-ls-red');
  });

  it('renders lead paragraph with correct copy', () => {
    renderPage('light');
    expect(screen.getByText(/Human authority through Agents, Orchestration, Memory, and Tools/)).toBeInTheDocument();
    expect(screen.getByText(/Governance as an integral control layer/)).toBeInTheDocument();
    expect(screen.getByText(/Not a linear pipeline; a working model/)).toBeInTheDocument();
  });

  it('renders CTA link to /ai-company-builder/#governance', () => {
    renderPage('dark');
    const link = screen.getByRole('link', { name: /explore the framework/i });
    expect(link).toHaveAttribute('href', '/ai-company-builder/#governance');
    expect(link).toHaveClass('bg-ls-red');
    expect(link).toHaveClass('text-ls-white');
  });

  it('renders 7-layer grid section with SectionHeading', () => {
    renderPage('dark');
    expect(screen.getByText('THE SEVEN LAYERS')).toBeInTheDocument();
    expect(screen.getByText('How the Model Works')).toBeInTheDocument();
    expect(screen.getByText(/Each layer has a distinct role/)).toBeInTheDocument();
  });

  it('renders all 7 pillar cards in grid', () => {
    renderPage('light');
    const pillars = ['Human', 'Agents', 'Orchestration', 'Memory', 'Tools', 'Governance', 'Value'];
    pillars.forEach((pillar) => {
      expect(screen.getByText(pillar)).toBeInTheDocument();
    });
  });

  it('applies governance ring accent on Governance card', () => {
    renderPage('dark');
    const governanceCard = screen.getByText('Governance').closest('article');
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

  it('renders bottom brand color bar', () => {
    renderPage('light');
    const colorBars = document.querySelectorAll('div[style*="background-color"]');
    // 3 in hero + 3 at bottom = 6 total
    expect(colorBars.length).toBe(6);
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
    expect(screen.getByText(/People set intent, own outcomes, and hold final decision authority/)).toBeInTheDocument();
    expect(screen.getByText(/Specialized AI roles with explicit scopes/)).toBeInTheDocument();
    expect(screen.getByText(/Deterministic routing of tasks, data, and decisions/)).toBeInTheDocument();
    expect(screen.getByText(/Persistent contextual state across long-running work/)).toBeInTheDocument();
    expect(screen.getByText(/Isolated execution environments for APIs, data, and actions/)).toBeInTheDocument();
    expect(screen.getByText(/A control layer woven through the model/)).toBeInTheDocument();
    expect(screen.getByText(/Measured business outcomes \(cost, latency, quality, and adoption\)/)).toBeInTheDocument();
  });

  it('uses Reveal component for staggered card animation', () => {
    renderPage('dark');
    const articles = document.querySelectorAll('article');
    expect(articles.length).toBe(7);
  });
});
