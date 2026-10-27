import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { HAOMTGVSection } from '../../components/home/HAOMTGVSection';

const renderSection = (theme: 'light' | 'dark') =>
  render(
    <MemoryRouter>
      <HAOMTGVSection theme={theme} />
    </MemoryRouter>,
  );

describe('HAOMTGVSection', () => {
  it('renders section with id="haomtgv"', () => {
    renderSection('dark');
    const section = screen.getByRole('region', { name: /h-a-o-m-t-g-v operating philosophy/i });
    expect(section).toBeInTheDocument();
    expect(section.getAttribute('id')).toBe('haomtgv');
  });

  it('renders SectionHeading with correct eyebrow and title', () => {
    renderSection('light');
    expect(screen.getByText('OPERATING PHILOSOPHY')).toBeInTheDocument();
    expect(screen.getByText('H-A-O-M-T-G-V')).toBeInTheDocument();
  });

  it('renders all 7 pillar cards', () => {
    renderSection('dark');
    const pillars = ['Human', 'Agents', 'Orchestration', 'Memory', 'Tools', 'Governance', 'Value'];
    pillars.forEach((pillar) => {
      expect(screen.getByText(pillar)).toBeInTheDocument();
    });
  });

  it('renders Lucide icons for each pillar', () => {
    renderSection('light');
    // Each pillar should have an icon (svg element)
    const svgs = document.querySelectorAll('svg');
    expect(svgs.length).toBeGreaterThanOrEqual(7);
  });

  it('applies governance ring accent on Governance pillar', () => {
    renderSection('dark');
    const governanceCard = screen.getByText('Governance').closest('article');
    expect(governanceCard).toHaveClass('ring-1');
    expect(governanceCard).toHaveClass('ring-ls-red/30');
  });

  it('renders governance callout paragraph', () => {
    renderSection('light');
    expect(screen.getByText(/Human direction is not a checkpoint at the end/)).toBeInTheDocument();
  });

  it('applies correct theme classes for light mode', () => {
    renderSection('light');
    const firstCard = screen.getByText('Human').closest('article');
    expect(firstCard).toHaveClass('bg-ls-white/95');
    expect(firstCard).toHaveClass('border-ls-grey-dark');
    expect(firstCard).toHaveClass('text-ls-navy');
  });

  it('applies correct theme classes for dark mode', () => {
    renderSection('dark');
    const firstCard = screen.getByText('Human').closest('article');
    expect(firstCard).toHaveClass('bg-ls-navy/80');
    expect(firstCard).toHaveClass('border-ls-white/15');
    expect(firstCard).toHaveClass('text-ls-white');
  });

  it('renders pillar descriptions', () => {
    renderSection('dark');
    expect(screen.getByText(/People set intent, own outcomes, and hold final decision authority/)).toBeInTheDocument();
    expect(screen.getByText(/Specialized AI roles with explicit scopes/)).toBeInTheDocument();
    expect(screen.getByText(/Deterministic routing of tasks, data, and decisions/)).toBeInTheDocument();
    expect(screen.getByText(/Persistent contextual state across long-running work/)).toBeInTheDocument();
    expect(screen.getByText(/Isolated execution environments for APIs, data, and actions/)).toBeInTheDocument();
    expect(screen.getByText(/A control layer woven through the model/)).toBeInTheDocument();
    expect(screen.getByText(/Measured business outcomes \(cost, latency, quality, and adoption\)/)).toBeInTheDocument();
  });

  it('uses Reveal component for staggered animation', () => {
    renderSection('dark');
    // Reveal wraps each article - verify articles exist with proper structure
    const articles = document.querySelectorAll('article');
    expect(articles.length).toBe(7);
  });
});
