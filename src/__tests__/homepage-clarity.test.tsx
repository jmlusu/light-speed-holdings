import { describe, it, expect } from 'vitest';
import type { ReactElement } from 'react';
import { render, screen, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { WhatWeBuildGrid } from '../components/home/WhatWeBuildGrid';
import { InsightsSection } from '../components/home/InsightsSection';

const renderInRouter = (ui: ReactElement) => render(<MemoryRouter>{ui}</MemoryRouter>);

describe('homepage clarity - one decision per section', () => {
  it('WhatWeBuildGrid: six capability links have six unique accessible names', () => {
    renderInRouter(<WhatWeBuildGrid theme="dark" />);
    const links = screen.getAllByRole('link', { name: /^Explore /i });
    expect(links).toHaveLength(6);
    const names = links.map((link) => link.getAttribute('aria-label'));
    expect(new Set(names).size).toBe(6);
    expect(names).toEqual([
      'EXPLORE CAPABILITY — Explore AI-Native Company Building',
      'EXPLORE CAPABILITY — Explore Intelligent Workflow Automation',
      'EXPLORE CAPABILITY — Explore Agentic Systems & Orchestration',
      'EXPLORE CAPABILITY — Explore Enterprise AI Integration',
      'EXPLORE CAPABILITY — Explore Organizational Memory Systems',
      'EXPLORE CAPABILITY — Explore AI Governance Infrastructure',
    ]);
    links.forEach((link) => expect(link).toHaveAttribute('href', '/what-we-do'));
  });

  it('WhatWeBuildGrid: practice-area copy and 48/64px vertical rhythm are preserved', () => {
    const { container } = renderInRouter(<WhatWeBuildGrid theme="light" />);
    const section = container.querySelector('#what-we-build') as HTMLElement;
    expect(section).toHaveClass('py-12');
    expect(section).toHaveClass('lg:py-16');
    expect(screen.getByRole('heading', { level: 2, name: 'Six Capabilities. One Governed System.' })).toBeInTheDocument();
    expect(screen.getAllByText('EXPLORE CAPABILITY')).toHaveLength(6);
    expect(screen.getByText(/append-only cryptographic audit trails/)).toBeInTheDocument();
  });

  it('InsightsSection: one primary research link sits outside the "Browse all eight formats" disclosure', () => {
    const { container } = renderInRouter(<InsightsSection theme="dark" />);
    const region = screen.getByRole('region', { name: /pharos thought-leadership engine/i });
    expect(region).toHaveClass('py-12');
    expect(region).toHaveClass('lg:py-16');
    expect(within(region).getByRole('link', { name: /read the research library/i })).toHaveAttribute('href', '/insights');

    const details = container.querySelector('details') as HTMLElement;
    expect(details).not.toBeNull();
    expect(details).not.toHaveAttribute('open');
    expect(details.querySelector('summary')).toHaveTextContent('Browse all eight formats');
    const formatLinks = within(details).getAllByRole('link');
    expect(formatLinks).toHaveLength(8);
    expect(within(region).getAllByRole('link').length - formatLinks.length).toBe(1);
  });

  it('InsightsSection: all eight format names, subtitles and Explore labels are preserved', () => {
    const { container } = renderInRouter(<InsightsSection theme="light" />);
    const details = container.querySelector('details') as HTMLElement;
    const titles = [
      'Briefs', 'Field Notes', 'Research Notes', 'Policy Briefs',
      'System Maps', 'Data Stories', 'AI-Economics Analyses', 'Africa Watch Regional Monitors',
    ];
    titles.forEach((title) => expect(within(details).getByText(title)).toBeInTheDocument());
    expect(within(details).getByText(/Concise executive summaries connecting research to real-world use cases/)).toBeInTheDocument();
    expect(within(details).getByText(/First-hand operational observations and field lessons from live deployments/)).toBeInTheDocument();
    expect(within(details).getAllByText('Explore')).toHaveLength(8);
    expect(within(details).getByText('Our Eight Publication Formats')).toBeInTheDocument();
    expect(within(details).getByText('8 Publication Channels')).toBeInTheDocument();
  });

  it('InsightsSection: research library link cyan text follows the active theme', () => {
    const dark = renderInRouter(<InsightsSection theme="dark" />);
    const darkLink = within(dark.container).getByRole('link', { name: /read the research library/i });
    expect(darkLink).toHaveClass('text-ls-cyan');
    expect(darkLink).not.toHaveClass('text-ls-cyan-ink');
    dark.unmount();

    const light = renderInRouter(<InsightsSection theme="light" />);
    const lightLink = within(light.container).getByRole('link', { name: /read the research library/i });
    expect(lightLink).toHaveClass('text-ls-cyan-ink');
    expect(lightLink).not.toHaveClass('text-ls-cyan');
  });
});
