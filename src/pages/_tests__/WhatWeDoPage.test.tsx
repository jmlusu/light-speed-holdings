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
    const eyebrow = screen.getByText(/AI-NATIVE ENGAGEMENT MODEL/);
    expect(eyebrow).toBeInTheDocument();
  });

  it('renders hero headline', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const headline = screen.getByRole('heading', { name: /From Problem to Measured Outcome\./ });
    expect(headline).toBeInTheDocument();
  });

  it('renders hero subheadline', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const subhead = screen.getByText(/From a real problem to a governed, measured AI capability/);
    expect(subhead).toBeInTheDocument();
  });

  it('renders primary CTA text', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const cta = screen.getByText(/Contact Us/);
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
    // Pillar names appear in both the selector and the detail panel.
    expect(screen.getAllByText(/Human Direction/).length).toBeGreaterThan(0);
  });

  it('renders table with six stage rows', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    // The old engagement table was replaced by interactive pillar/lifecycle
    // panels, so assert the stage content is rendered instead of table rows.
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
    const darkHeading = screen.getByRole('heading', { name: /From Problem to Measured Outcome\./ });
    expect(darkHeading).toBeInTheDocument();
  });
});
