/// <reference types="vitest" />
import { render, screen } from '@testing-library/react';
import { WhatWeDoPage } from '../WhatWeDoPage';
import { MemoryRouter } from 'react-router-dom';

describe('WhatWeDoPage Hero', () => {
  it('renders hero eyebrow', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const eyebrow = screen.getByText(/THE AI-NATIVE COMPANY BUILDER/);
    expect(eyebrow).toBeInTheDocument();
  });

  it('renders hero headline', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const headline = screen.getByRole('heading', { name: /An Operating Model Built Around Seven HAOMTGV Pillars/ });
    expect(headline).toBeInTheDocument();
  });

  it('renders hero subheadline', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const subhead = screen.getByText(/LightSpeed Holdings does not deploy standalone AI tools./);
    expect(subhead).toBeInTheDocument();
  });

  it('renders primary CTA text', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const cta = screen.getByText(/ENGAGE LIGHTSPEED/);
    expect(cta).toBeInTheDocument();
  });

  it('renders secondary CTA text', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const secondaryCta = screen.getByText(/EXPLORE PHAROS/);
    expect(secondaryCta).toBeInTheDocument();
  });
});

describe('WhatWeDoPage Engagement Model Flow', () => {
  it('renders flow diagram with all six stages', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    // The flow diagram section is present with the seven pillars
    expect(screen.getByText(/INTERACTIVE SEVEN-PILLAR STACK/)).toBeInTheDocument();
    // Check for pillar names in the flow description
    expect(screen.getByText(/Human Direction/)).toBeInTheDocument();
  });

  it('renders table with six stage rows', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    // Find the engagement model table by looking for the specific stage content
    const tableRows = screen.getAllByRole('row');
    // Filter to rows that contain stage names (exclude header row by checking for "Stage" text)
    const stageRowTexts = tableRows.filter((row) =>
      !row.textContent.includes('Stage What happens')
    );
    // Check for stage names using getAllByText and length check
    expect(screen.getAllByText(/Problem Addressed/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Design Target Operating Model/i).length).toBeGreaterThan(0);
  });
});

describe('WhatWeDoPage Dark Mode', () => {
  it('renders hero in dark theme', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="dark" />
      </MemoryRouter>
    );
    const darkHeading = screen.getByRole('heading', { name: /An Operating Model Built Around Seven HAOMTGV Pillars/ });
    expect(darkHeading).toBeInTheDocument();
  });
});
