import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { HaomtgvInfographic } from '../../components/haomtgv/HaomtgvInfographic';

// Mock the media registry
const mockAsset = {
  id: 'haomtgv-full-vertical',
  type: 'HAOMTGV_INFOGRAPHIC' as const,
  title: 'H-A-O-M-T-G-V Framework (Full Vertical)',
  description: 'Complete H-A-O-M-T-G-V flow with feedback loops between Memory, Tools, Orchestration, Governance. Human at top, Value at bottom.',
  src: {
    png: '/brand/digital/Lightspeed HAOMTGV Operating Framework.png',
  },
  alt: 'H-A-O-M-T-G-V framework showing Human at top, flowing through Agents, Orchestration, Memory, Tools, Governance to Value, with feedback loops between Memory, Tools, Orchestration, and Governance',
  width: 1536,
  height: 1024,
  formats: ['png'],
  placement: ['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq'],
  attribution: 'LightSpeed Holdings Design Team',
  honestyTier: 'proven-in-house' as const,
  createdAt: '2026-10-01',
  updatedAt: '2026-10-16',
};

vi.mock('../../../data/media/registry', () => ({
  getMediaById: vi.fn((id: string) => (id === 'haomtgv-full-vertical' ? mockAsset : undefined)),
}));

describe('HaomtgvInfographic', () => {
  it('renders section with correct aria-label', () => {
    render(<HaomtgvInfographic theme="dark" />);
    const section = screen.getByRole('region', { name: /haomtgv full framework infographic/i });
    expect(section).toBeInTheDocument();
  });

  it('renders SectionHeading with registry title and description', () => {
    render(<HaomtgvInfographic theme="light" />);
    expect(screen.getByText('THE FRAMEWORK')).toBeInTheDocument();
    // Title appears in both SectionHeading h2 and figcaption p - use getAllByText
    const titles = screen.getAllByText('H-A-O-M-T-G-V Framework');
    expect(titles.length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText(/Complete H-A-O-M-T-G-V flow with feedback loops/)).toBeInTheDocument();
  });

  it('renders figure with image from registry', () => {
    render(<HaomtgvInfographic theme="dark" />);
    const figure = screen.getByRole('figure');
    expect(figure).toBeInTheDocument();

    const img = figure.querySelector('img');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', '/brand/digital/Lightspeed HAOMTGV Operating Framework.png');
    expect(img).toHaveAttribute('alt', mockAsset.alt);
    expect(img).toHaveAttribute('width', '1536');
    expect(img).toHaveAttribute('height', '1024');
    expect(img).toHaveAttribute('loading', 'lazy');
  });

  it('renders figcaption with title and attribution', () => {
    render(<HaomtgvInfographic theme="light" />);
    const attribution = screen.getByText('LightSpeed Holdings Design Team');
    const figcaption = attribution.closest('figcaption');
    expect(figcaption).toBeInTheDocument();
    expect(figcaption).toHaveTextContent('H-A-O-M-T-G-V Framework');
  });

  it('applies light theme classes to figure', () => {
    render(<HaomtgvInfographic theme="light" />);
    const figure = screen.getByRole('figure');
    expect(figure).toHaveClass('bg-ls-white/95');
    expect(figure).toHaveClass('border-ls-grey-dark');
    expect(figure).toHaveClass('ring-1');
    expect(figure).toHaveClass('ring-ls-cyan/25');
    expect(figure).toHaveClass('shadow-xl');
  });

  it('applies dark theme classes to figure', () => {
    render(<HaomtgvInfographic theme="dark" />);
    const figure = screen.getByRole('figure');
    expect(figure).toHaveClass('bg-ls-navy/80');
    expect(figure).toHaveClass('border-ls-white/15');
    expect(figure).toHaveClass('ring-1');
    expect(figure).toHaveClass('ring-ls-cyan/25');
    expect(figure).toHaveClass('shadow-xl');
  });

  it('renders attribution in red tracking-widest style', () => {
    render(<HaomtgvInfographic theme="dark" />);
    const attribution = screen.getByText('LightSpeed Holdings Design Team');
    expect(attribution).toHaveClass('text-ls-red/70');
    expect(attribution).toHaveClass('font-body');
    expect(attribution).toHaveClass('font-bold');
    expect(attribution).toHaveClass('tracking-widest');
  });

  it('uses Reveal component for animation', () => {
    render(<HaomtgvInfographic theme="dark" />);
    // Reveal wraps the figure
    const figure = screen.getByRole('figure');
    expect(figure.parentElement).toBeInTheDocument();
  });
});
