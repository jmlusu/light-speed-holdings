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
    const eyebrow = screen.getByRole('heading', { name: /LIGHTSPEED HOLDINGS \/\/ ENGAGEMENT MODEL/i });
    expect(eyebrow).toBeInTheDocument();
  });

  it('renders hero headline', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const headline = screen.getByRole('heading', { name: /Strategy\. Build\. Govern\. Research \& Policy/i });
    expect(headline).toBeInTheDocument();
  });

  it('renders hero subheadline', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const subhead = screen.getByText(/We help organizations move from a real problem to a governed, measured AI capability/);
    expect(subhead).toBeInTheDocument();
  });

  it('renders primary CTA text', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const cta = screen.getByText(/START A CONVERSATION/);
    expect(cta).toBeInTheDocument();
  });

  it('renders secondary CTA text', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="light" />
      </MemoryRouter>
    );
    const secondaryCta = screen.getByText(/REQUEST AN AI READINESS ASSESSMENT/);
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
    // The flow diagram appears as a code block with the 6 stages
    const flowContent = screen.getByText(/PROBLEM.*DESIGN.*BUILD.*DEPLOY.*GOVERN.*MEASURE/s);
    expect(flowContent).toBeInTheDocument();
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
    const stageNames = ['PROBLEM', 'DESIGN', 'BUILD', 'DEPLOY', 'GOVERN', 'MEASURE'];
    stageNames.forEach((stage) => {
      const found = stageRowTexts.some((row) => row.textContent.includes(stage));
      expect(found).toBe(true);
    });
  });
});

describe('WhatWeDoPage Dark Mode', () => {
  it('renders hero in dark theme', () => {
    render(
      <MemoryRouter initialEntries={['/what-we-do']}>
        <WhatWeDoPage theme="dark" />
      </MemoryRouter>
    );
    const darkHeading = screen.getByRole('heading', { name: /LIGHTSPEED HOLDINGS \/\/ ENGAGEMENT MODEL/i });
    expect(darkHeading).toBeInTheDocument();
  });
});
