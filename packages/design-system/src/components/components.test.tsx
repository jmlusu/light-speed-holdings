import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Button } from '../components/Button/Button';
import { Card } from '../components/Card/Card';
import { Badge } from '../components/Badge/Badge';
import { Heading } from '../components/Heading/Heading';
import { Text } from '../components/Text/Text';
import { Container } from '../components/Container/Container';
import { Grid } from '../components/Grid/Grid';
import { Stack } from '../components/Stack/Stack';
import { Section } from '../components/Section/Section';
import { Logo } from '../components/Logo/Logo';

describe('Button', () => {
  it('renders with primary variant by default', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
  });

  it('renders different variants', () => {
    render(
      <div>
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="link">Link</Button>
      </div>
    );
    expect(screen.getByRole('button', { name: /primary/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /secondary/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /ghost/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /link/i })).toBeInTheDocument();
  });

  it('renders different sizes', () => {
    render(
      <div>
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
      </div>
    );
    expect(screen.getByRole('button', { name: /small/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /medium/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /large/i })).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole('button', { name: /loading/i })).toBeDisabled();
  });

  it('forwards ref', () => {
    const ref = vi.fn();
    render(<Button ref={ref}>Ref Button</Button>);
    expect(ref).toHaveBeenCalledWith(expect.any(HTMLButtonElement));
  });
});

describe('Card', () => {
  it('renders with default variant', () => {
    render(<Card>Card content</Card>);
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });

  it('renders different variants', () => {
    render(
      <div>
        <Card variant="default">Default</Card>
        <Card variant="elevated">Elevated</Card>
        <Card variant="interactive">Interactive</Card>
      </div>
    );
    expect(screen.getByText('Default')).toBeInTheDocument();
    expect(screen.getByText('Elevated')).toBeInTheDocument();
    expect(screen.getByText('Interactive')).toBeInTheDocument();
  });
});

describe('Badge', () => {
  it('renders all variants', () => {
    render(
      <div>
        <Badge variant="proven">Proven</Badge>
        <Badge variant="pilot">Pilot</Badge>
        <Badge variant="fieldable">Fieldable</Badge>
        <Badge variant="development">Development</Badge>
        <Badge variant="neutral">Neutral</Badge>
      </div>
    );
    expect(screen.getByText('Proven')).toBeInTheDocument();
    expect(screen.getByText('Pilot')).toBeInTheDocument();
    expect(screen.getByText('Fieldable')).toBeInTheDocument();
    expect(screen.getByText('Development')).toBeInTheDocument();
    expect(screen.getByText('Neutral')).toBeInTheDocument();
  });

  it('renders with dot', () => {
    render(<Badge variant="proven" dot>Proven</Badge>);
    const badge = screen.getByText('Proven').parentElement;
    expect(badge).toBeInTheDocument();
  });
});

describe('Heading', () => {
  it('renders different levels', () => {
    render(
      <div>
        <Heading level={1}>H1</Heading>
        <Heading level={2}>H2</Heading>
        <Heading level={3}>H3</Heading>
        <Heading level={4}>H4</Heading>
        <Heading level={5}>H5</Heading>
        <Heading level={6}>H6</Heading>
        <Heading level="display">Display</Heading>
      </div>
    );
    expect(screen.getByText('H1')).toBeInTheDocument();
    expect(screen.getByText('H2')).toBeInTheDocument();
    expect(screen.getByText('Display')).toBeInTheDocument();
  });
});

describe('Text', () => {
  it('renders different variants', () => {
    render(
      <div>
        <Text variant="body">Body</Text>
        <Text variant="lead">Lead</Text>
        <Text variant="caption">Caption</Text>
        <Text variant="overline">Overline</Text>
        <Text variant="subtitle">Subtitle</Text>
      </div>
    );
    expect(screen.getByText('Body')).toBeInTheDocument();
    expect(screen.getByText('Lead')).toBeInTheDocument();
    expect(screen.getByText('Caption')).toBeInTheDocument();
    expect(screen.getByText('Overline')).toBeInTheDocument();
    expect(screen.getByText('Subtitle')).toBeInTheDocument();
  });

  it('renders muted and secondary', () => {
    render(
      <div>
        <Text muted>Muted</Text>
        <Text secondary>Secondary</Text>
      </div>
    );
    expect(screen.getByText('Muted')).toBeInTheDocument();
    expect(screen.getByText('Secondary')).toBeInTheDocument();
  });
});

describe('Container', () => {
  it('renders with default size', () => {
    render(<Container>Content</Container>);
    expect(screen.getByText('Content')).toBeInTheDocument();
  });

  it('renders different sizes', () => {
    render(
      <div>
        <Container size="narrow">Narrow</Container>
        <Container size="wide">Wide</Container>
        <Container size="full">Full</Container>
      </div>
    );
    expect(screen.getByText('Narrow')).toBeInTheDocument();
    expect(screen.getByText('Wide')).toBeInTheDocument();
    expect(screen.getByText('Full')).toBeInTheDocument();
  });
});

describe('Grid', () => {
  it('renders grid with columns', () => {
    render(
      <Grid columns={3}>
        <div>1</div>
        <div>2</div>
        <div>3</div>
      </Grid>
    );
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });
});

describe('Stack', () => {
  it('renders vertical stack', () => {
    render(
      <Stack direction="vertical" gap="component">
        <div>1</div>
        <div>2</div>
      </Stack>
    );
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  it('renders horizontal stack', () => {
    render(
      <Stack direction="horizontal" gap="tight">
        <div>1</div>
        <div>2</div>
      </Stack>
    );
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });
});

describe('Section', () => {
  it('renders section with label', () => {
    render(
      <Section label="Features">
        <div>Content</div>
      </Section>
    );
    expect(screen.getByText('FEATURES')).toBeInTheDocument();
    expect(screen.getByText('Content')).toBeInTheDocument();
  });
});

describe('Logo', () => {
  it('renders full variant', () => {
    render(<Logo variant="full" />);
    expect(screen.getByText('LIGHT')).toBeInTheDocument();
    expect(screen.getByText('SPEED')).toBeInTheDocument();
    expect(screen.getByText('HOLDINGS LIMITED')).toBeInTheDocument();
  });

  it('renders icon variant', () => {
    render(<Logo variant="icon" />);
    const svg = screen.getByTestId('logo-icon');
    expect(svg).toBeInTheDocument();
  });
});
