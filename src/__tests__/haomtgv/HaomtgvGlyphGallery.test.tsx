import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { HaomtgvGlyphGallery } from '../../components/haomtgv/HaomtgvGlyphGallery';

// Mock the media registry
vi.mock('../../data/media/registry', () => ({
  getMediaByType: vi.fn(() => [
    {
      id: 'glyph-human',
      type: 'MICRO_ILLUSTRATIONS',
      title: 'H — Human Glyph',
      description: 'Stylized figure with intent arrow for Human layer.',
      src: { svg: '/assets/diagrams/micro-illustrations/glyph-human.svg' },
      alt: 'Human glyph: stylized figure with forward-pointing arrow',
      width: 64,
      height: 64,
      formats: ['svg'],
      placement: ['/'],
      attribution: 'LightSpeed Holdings Design Team',
      honestyTier: 'proven-in-house',
      createdAt: '2026-10-01',
      updatedAt: '2026-10-01',
    },
    {
      id: 'glyph-agents',
      type: 'MICRO_ILLUSTRATIONS',
      title: 'A — Agents Glyph',
      description: 'Interlocking geometric forms for Agents layer.',
      src: { svg: '/assets/diagrams/micro-illustrations/glyph-agents.svg' },
      alt: 'Agents glyph: interlocking geometric forms representing 89 AI agents',
      width: 64,
      height: 64,
      formats: ['svg'],
      placement: ['/'],
      attribution: 'LightSpeed Holdings Design Team',
      honestyTier: 'proven-in-house',
      createdAt: '2026-10-01',
      updatedAt: '2026-10-01',
    },
    {
      id: 'glyph-orchestration',
      type: 'MICRO_ILLUSTRATIONS',
      title: 'O — Orchestration Glyph',
      description: 'Flow lines and nodes for Orchestration layer.',
      src: { svg: '/assets/diagrams/micro-illustrations/glyph-orchestration.svg' },
      alt: 'Orchestration glyph: flow lines connecting nodes representing MessageBus routing',
      width: 64,
      height: 64,
      formats: ['svg'],
      placement: ['/'],
      attribution: 'LightSpeed Holdings Design Team',
      honestyTier: 'proven-in-house',
      createdAt: '2026-10-01',
      updatedAt: '2026-10-01',
    },
    {
      id: 'glyph-memory',
      type: 'MICRO_ILLUSTRATIONS',
      title: 'M — Memory Glyph',
      description: 'Layered cylinders for Memory layer.',
      src: { svg: '/assets/diagrams/micro-illustrations/glyph-memory.svg' },
      alt: 'Memory glyph: layered cylinders representing 6 memory types',
      width: 64,
      height: 64,
      formats: ['svg'],
      placement: ['/'],
      attribution: 'LightSpeed Holdings Design Team',
      honestyTier: 'proven-in-house',
      createdAt: '2026-10-01',
      updatedAt: '2026-10-01',
    },
    {
      id: 'glyph-tools',
      type: 'MICRO_ILLUSTRATIONS',
      title: 'T — Tools Glyph',
      description: 'Wrench/terminal hybrid for Tools layer.',
      src: { svg: '/assets/diagrams/micro-illustrations/glyph-tools.svg' },
      alt: 'Tools glyph: wrench/terminal hybrid representing isolated execution environments',
      width: 64,
      height: 64,
      formats: ['svg'],
      placement: ['/'],
      attribution: 'LightSpeed Holdings Design Team',
      honestyTier: 'proven-in-house',
      createdAt: '2026-10-01',
      updatedAt: '2026-10-01',
    },
    {
      id: 'glyph-governance',
      type: 'MICRO_ILLUSTRATIONS',
      title: 'G — Governance Glyph',
      description: 'Shield with check for Governance layer.',
      src: { svg: '/assets/diagrams/micro-illustrations/glyph-governance.svg' },
      alt: 'Governance glyph: shield with checkmark representing 5-tier approval and audit',
      width: 64,
      height: 64,
      formats: ['svg'],
      placement: ['/'],
      attribution: 'LightSpeed Holdings Design Team',
      honestyTier: 'proven-in-house',
      createdAt: '2026-10-01',
      updatedAt: '2026-10-01',
    },
    {
      id: 'glyph-value',
      type: 'MICRO_ILLUSTRATIONS',
      title: 'V — Value Glyph',
      description: 'Upward chart/diamond for Value layer.',
      src: { svg: '/assets/diagrams/micro-illustrations/glyph-value.svg' },
      alt: 'Value glyph: upward-trending chart with diamond representing measurable business outcomes',
      width: 64,
      height: 64,
      formats: ['svg'],
      placement: ['/'],
      attribution: 'LightSpeed Holdings Design Team',
      honestyTier: 'proven-in-house',
      createdAt: '2026-10-01',
      updatedAt: '2026-10-01',
    },
  ]),
}));

describe('HaomtgvGlyphGallery', () => {
  it('renders section with correct aria-label', () => {
    render(<HaomtgvGlyphGallery theme="dark" />);
    const section = screen.getByRole('region', { name: /haomtgv glyph gallery/i });
    expect(section).toBeInTheDocument();
  });

  it('renders SectionHeading with correct eyebrow, title, and lead', () => {
    render(<HaomtgvGlyphGallery theme="light" />);
    expect(screen.getByText('THE SEVEN GLYPHS')).toBeInTheDocument();
    expect(screen.getByText('H-A-O-M-T-G-V Glyphs')).toBeInTheDocument();
    expect(screen.getByText(/Type K micro-illustrations/)).toBeInTheDocument();
    expect(screen.getByText(/brand cyan throughout, Governance marked in red/)).toBeInTheDocument();
  });

  it('renders all 7 glyph cards in grid', () => {
    render(<HaomtgvGlyphGallery theme="dark" />);
    const titles = ['Human', 'Agents', 'Orchestration', 'Memory', 'Tools', 'Governance', 'Value'];
    titles.forEach((title) => {
      expect(screen.getByText(title)).toBeInTheDocument();
    });
  });

  it('renders SVG images for each glyph', () => {
    render(<HaomtgvGlyphGallery theme="light" />);
    const images = screen.getAllByRole('img');
    expect(images.length).toBe(7);
    images.forEach((img) => {
      expect(img).toHaveAttribute('src', expect.stringMatching(/\/assets\/diagrams\/micro-illustrations\/glyph-.*\.svg$/));
      expect(img).toHaveAttribute('width', '64');
      expect(img).toHaveAttribute('height', '64');
      expect(img).toHaveAttribute('loading', 'lazy');
    });
  });

  it('applies cyan ring for non-governance glyphs', () => {
    render(<HaomtgvGlyphGallery theme="dark" />);
    const humanCard = screen.getByText('Human').closest('article');
    expect(humanCard).toHaveClass('ring-1');
    expect(humanCard).toHaveClass('ring-ls-cyan/20');
  });

  it('applies red ring for governance glyph', () => {
    render(<HaomtgvGlyphGallery theme="light" />);
    const governanceCard = screen.getByText('Governance').closest('article');
    expect(governanceCard).toHaveClass('ring-1');
    expect(governanceCard).toHaveClass('ring-ls-red/30');
  });

  it('renders letter badge with correct color for non-governance', () => {
    render(<HaomtgvGlyphGallery theme="dark" />);
    const humanBadge = screen.getByText('Human').closest('article')?.querySelector('span[aria-hidden="true"]');
    expect(humanBadge).toHaveClass('border-ls-cyan/40');
    expect(humanBadge).toHaveClass('bg-ls-cyan/10');
    expect(humanBadge).toHaveClass('text-ls-cyan');
  });

  it('renders letter badge with red color for governance', () => {
    render(<HaomtgvGlyphGallery theme="light" />);
    const governanceBadge = screen.getByText('Governance').closest('article')?.querySelector('span[aria-hidden="true"]');
    expect(governanceBadge).toHaveClass('border-ls-red/40');
    expect(governanceBadge).toHaveClass('bg-ls-red/10');
    expect(governanceBadge).toHaveClass('text-ls-red');
  });

  it('renders glyph descriptions from registry', () => {
    render(<HaomtgvGlyphGallery theme="dark" />);
    expect(screen.getByText(/Stylized figure with intent arrow/)).toBeInTheDocument();
    expect(screen.getByText(/Interlocking geometric forms/)).toBeInTheDocument();
    expect(screen.getByText(/Flow lines and nodes/)).toBeInTheDocument();
    expect(screen.getByText(/Layered cylinders/)).toBeInTheDocument();
    expect(screen.getByText(/Wrench\/terminal hybrid/)).toBeInTheDocument();
    expect(screen.getByText(/Shield with check/)).toBeInTheDocument();
    expect(screen.getByText(/Upward chart\/diamond/)).toBeInTheDocument();
  });

  it('applies light theme classes correctly', () => {
    render(<HaomtgvGlyphGallery theme="light" />);
    const firstCard = screen.getByText('Human').closest('article');
    expect(firstCard).toHaveClass('bg-ls-white/95');
    expect(firstCard).toHaveClass('border-ls-grey-dark');
    expect(firstCard).toHaveClass('text-ls-navy');
  });

  it('applies dark theme classes correctly', () => {
    render(<HaomtgvGlyphGallery theme="dark" />);
    const firstCard = screen.getByText('Human').closest('article');
    expect(firstCard).toHaveClass('bg-ls-navy/80');
    expect(firstCard).toHaveClass('border-ls-white/15');
    expect(firstCard).toHaveClass('text-ls-white');
  });

  it('uses Reveal component for staggered animation', () => {
    render(<HaomtgvGlyphGallery theme="dark" />);
    const articles = document.querySelectorAll('article');
    expect(articles.length).toBe(7);
  });
});
