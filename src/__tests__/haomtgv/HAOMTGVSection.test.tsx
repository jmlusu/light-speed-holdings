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

  it('renders the section lead', () => {
    renderSection('light');
    expect(screen.getByText(/How LightSpeed thinks about AI-native operations/)).toBeInTheDocument();
  });

  it('renders the interactive visualization with one selector per layer', () => {
    renderSection('dark');
    const buttons = screen.getAllByRole('button');
    expect(buttons).toHaveLength(7);
    expect(buttons.map((b) => b.textContent?.charAt(0))).toEqual(['H', 'A', 'O', 'M', 'T', 'G', 'V']);
  });

  it('opens on the Human layer by default', () => {
    renderSection('dark');
    expect(screen.getByRole('heading', { level: 3, name: 'Human Authority' })).toBeInTheDocument();
    expect(screen.getByText(/Human intent sits above the system/)).toBeInTheDocument();
  });

  it('renders governance callout paragraph', () => {
    renderSection('light');
    expect(screen.getByText(/Human direction is not a checkpoint at the end/)).toBeInTheDocument();
  });

  it('links to the full framework page', () => {
    renderSection('light');
    const link = screen.getByRole('link', { name: /Explore the full framework/i });
    expect(link).toHaveAttribute('href', '/haomtgv');
  });

  it('applies the dark theme surface to the section', () => {
    renderSection('dark');
    const section = screen.getByRole('region', { name: /h-a-o-m-t-g-v operating philosophy/i });
    expect(section).toHaveClass('bg-[#070A40]');
  });

  it('applies the light theme surface to the section', () => {
    renderSection('light');
    const section = screen.getByRole('region', { name: /h-a-o-m-t-g-v operating philosophy/i });
    expect(section).toHaveClass('bg-[#F7F8F9]');
  });
});
