import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { readFileSync } from 'node:fs';
import { ApprovalMatrixWalkthrough } from '../components/haomtgv/ApprovalMatrixWalkthrough';
import { ProofPosturePanel } from '../components/home/ProofPosturePanel';
import { faqs } from '../data/faqs';
import claimsRegistry from '../data/registries/claims-registry.json';

afterEach(() => cleanup());

const read = (path: string) => readFileSync(path, 'utf8');
const claimText = (id: string) => {
  const claim = claimsRegistry.claims.find((c) => c.id === id);
  if (!claim) throw new Error(`missing claim ${id}`);
  return claim;
};

describe('five-tier approval worked example', () => {
  it('renders one static four-step walkthrough with registry-backed strings and no new control', () => {
    render(<ApprovalMatrixWalkthrough theme="dark" />);
    const region = screen.getByRole('region', {
      name: /one worked example of the five-tier human approval matrix/i,
    });

    expect(within(region).getByText('One worked example')).toBeInTheDocument();
    expect(within(region).getByText('Action request')).toBeInTheDocument();
    expect(within(region).getByText('Financial commitments, external partnerships, and policy changes.')).toBeInTheDocument();
    expect(within(region).getByText('Risk class')).toBeInTheDocument();
    expect(within(region).getByText('High')).toBeInTheDocument();
    expect(within(region).getByText('Named human gate')).toBeInTheDocument();
    expect(within(region).getByText('Executive sponsor or director.')).toBeInTheDocument();
    expect(within(region).getByText('SHA-256 audit receipt')).toBeInTheDocument();
    expect(
      within(region).getByText(claimText('claim.append-only-audit-trails').text),
    ).toBeInTheDocument();

    expect(within(region).getByText('Proven in-house')).toBeInTheDocument();
    expect(within(region).getByText(/claim\.five-tier-approval/)).toBeInTheDocument();
    expect(within(region).getByText(/claim\.four-governance-gates/)).toBeInTheDocument();
    expect(within(region).getByText(/claim\.append-only-audit-trails/)).toBeInTheDocument();

    expect(within(region).queryAllByRole('button')).toHaveLength(0);
    expect(within(region).queryAllByRole('link')).toHaveLength(0);
  });

  it('uses the PROVEN_IN_HOUSE classification without implying external validation', () => {
    expect(claimText('claim.five-tier-approval').classification).toBe('PROVEN_IN_HOUSE');
    expect(claimText('claim.append-only-audit-trails').classification).toBe('PROVEN_IN_HOUSE');
    const source = read('src/components/haomtgv/ApprovalMatrixWalkthrough.tsx');
    expect(source).not.toMatch(/verified by|certified/i);
  });

  it('replaces the five-tier text label on the HAOMTGV page', () => {
    const page = read('src/pages/HAOMTGVPage.tsx');
    expect(page).not.toContain('A five-tier human approval matrix across the system');
    expect(page).toContain('<ApprovalMatrixWalkthrough theme={theme} />');
  });
});

describe('proof posture disclosure', () => {
  it('is closed and carries only verbatim FAQ answer strings plus one uniquely named link', () => {
    const { container } = render(
      <MemoryRouter><ProofPosturePanel theme="light" /></MemoryRouter>,
    );
    const details = container.querySelector('details') as HTMLElement;
    expect(details).not.toBeNull();
    expect(details).not.toHaveAttribute('open');
    expect(within(details).getByText('What we have not proven yet')).toBeInTheDocument();

    const provenClients = faqs.find((f) => f.id === 'proven-clients');
    const pricing = faqs.find((f) => f.id === 'pricing');
    expect(provenClients?.answer).toContain('Not yet. Nothing has been delivered to paying clients.');
    expect(provenClients?.answer).toContain('Every proof point on this site carries an explicit honesty badge.');
    expect(pricing?.answer).toContain('There is no public rate card yet.');

    for (const snippet of [
      'Not yet. Nothing has been delivered to paying clients.',
      'There is no public rate card yet.',
      'Every proof point on this site carries an explicit honesty badge.',
    ]) expect(within(details).getByText(snippet)).toBeInTheDocument();

    expect(within(details).getByText('Proven in-house')).toBeInTheDocument();
    const link = within(details).getByRole('link', { name: 'Read the published answers' });
    expect(link).toHaveAttribute('href', '/faq');
    expect(within(details).queryAllByRole('link')).toHaveLength(1);
    expect(within(details).queryAllByRole('button')).toHaveLength(0);
    expect(within(details).queryByText(/\b(?:StopOver|LIVE)\b/i)).not.toBeInTheDocument();
  });

  it('adds no new number and no new primary call to action', () => {
    const { container } = render(
      <MemoryRouter><ProofPosturePanel theme="dark" /></MemoryRouter>,
    );
    expect(container.textContent).not.toMatch(/\d/);
    expect(container.querySelector('a[href="/contact"]')).toBeNull();
  });

  it('is mounted early on both the homepage and /what-we-do', () => {
    const home = read('src/pages/HomePage.tsx');
    const whatWeDo = read('src/pages/WhatWeDoPage.tsx');
    for (const source of [home, whatWeDo]) {
      expect(source).toContain('import { ProofPosturePanel }');
      expect(source).toContain('<ProofPosturePanel theme={theme} />');
    }
  });
});
