import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { readFileSync } from 'node:fs';
import { ApprovalMatrixWalkthrough } from '../components/haomtgv/ApprovalMatrixWalkthrough';
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

describe('proof posture panel removed', () => {
  it('is not mounted on the homepage or /what-we-do', () => {
    for (const path of ['src/pages/HomePage.tsx', 'src/pages/WhatWeDoPage.tsx']) {
      expect(read(path)).not.toContain('ProofPosturePanel');
    }
  });
});
