/**
 * Use Case Detail Page
 *
 * Route: /use-cases/:slug  (Directive §9 / §11)
 * Renders a single use case from the canonical registry.
 * Data source matches UseCasesPage (@lightspeed/data/use-cases).
 */

import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { PageContainer } from '../layouts/PageContainer';
import { Section, Heading, Text, Badge, Stack, Button, tokens } from '@lightspeed/design-system';
import type { BadgeVariant } from '@lightspeed/design-system';
import { useCasesRegistry } from '@lightspeed/data/use-cases';
import type { UseCaseStatus } from '@lightspeed/data/use-cases';
import { sectorsRegistry } from '@lightspeed/data/sectors';
import { solutionsRegistry } from '@lightspeed/data/solutions';

/**
 * NOTE: tsconfig resolves @lightspeed/data/* to src/data/* (sector/solution are
 * single strings, no getUseCaseBySlug) while Vite resolves to ./data/* (arrays,
 * has getUseCaseBySlug). This page is written to type-check under BOTH shapes:
 * lookups use useCasesRegistry.find, and sector/solution are normalised to arrays.
 */
type AnyUseCase = {
  slug: string;
  title: string;
  problem: string;
  workflow: string;
  agentsInvolved: string[];
  inputs: string[];
  orchestration: string;
  tools: string[];
  humanApproval: string;
  output: string;
  businessValue: string;
  sector: string | string[];
  solution: string | string[];
  status: UseCaseStatus;
  evidence?: string;
};

const toStringArray = (value: string | string[]): string[] =>
  Array.isArray(value) ? value : [value];

const STATUS_BADGE_VARIANTS: Record<UseCaseStatus, BadgeVariant> = {
  LIVE: 'fieldable',
  PROVEN_IN_HOUSE: 'proven',
  PILOT: 'pilot',
  DEMONSTRATION: 'development',
  FIELDABLE: 'fieldable',
  FUTURE: 'neutral',
};

const statusLabel = (status: UseCaseStatus): string =>
  status.replace(/_/g, ' ');

const sectorTitle = (id: string): string =>
  sectorsRegistry.find((s) => s.id === id)?.title ?? id;

const solutionTitle = (slug: string): string =>
  solutionsRegistry.find((s) => s.slug === slug)?.title ?? slug;

const DetailBlock: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => (
  <div style={{ marginBottom: tokens.spacing[6] }}>
    <Text
      variant="caption"
      secondary
      style={{
        display: 'block',
        marginBottom: tokens.spacing[2],
        fontWeight: 700,
        letterSpacing: '0.08em',
        textTransform: 'uppercase',
      }}
    >
      {label}
    </Text>
    {children}
  </div>
);

export const UseCaseDetailPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const isDark = document.documentElement.classList.contains('dark');
  const theme = isDark ? 'dark' : 'light';
  const useCase = slug
    ? (useCasesRegistry.find((uc) => uc.slug === slug) as AnyUseCase | undefined)
    : undefined;

  if (!useCase) {
    return (
      <PageContainer>
        <Section label="Use Cases" theme={theme}>
          <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto', padding: `${tokens.spacing[16]} 0` }}>
            <Heading level={1} style={{ marginBottom: tokens.spacing[4] }}>
              Use case not found
            </Heading>
            <Text variant="lead" style={{ marginBottom: tokens.spacing[8] }}>
              We couldn't find a use case matching “{slug}”. It may have moved, or the link may be out of date.
            </Text>
            <Link to="/use-cases">
              <Button variant="primary" size="md">
                <ArrowLeft size={16} aria-hidden="true" />
                Back to Use Cases
              </Button>
            </Link>
          </div>
        </Section>
      </PageContainer>
    );
  }

  const relatedSolutions = toStringArray(useCase.solution);

  return (
    <PageContainer>
      {/* Hero */}
      <Section label="Use Case" theme={theme}>
        <div style={{ maxWidth: '860px', margin: '0 auto' }}>
          <Link
            to="/use-cases"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: tokens.spacing[2],
              fontSize: tokens.typography.fontSize.caption,
              fontWeight: 600,
              color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[600],
              textDecoration: 'none',
              marginBottom: tokens.spacing[5],
            }}
          >
            <ArrowLeft size={14} aria-hidden="true" />
            All Use Cases
          </Link>

          <Stack direction="horizontal" gap={2} wrap style={{ marginBottom: tokens.spacing[4] }}>
            <Badge variant={STATUS_BADGE_VARIANTS[useCase.status]}>
              {statusLabel(useCase.status)}
            </Badge>
            {toStringArray(useCase.sector).map((id) => (
              <Badge key={id} variant="neutral">{sectorTitle(id)}</Badge>
            ))}
          </Stack>

          <Heading level={1} style={{ marginBottom: tokens.spacing[4] }}>
            {useCase.title}
          </Heading>
          <Text variant="lead" style={{ maxWidth: '760px' }}>
            {useCase.problem}
          </Text>
        </div>
      </Section>

      {/* Body */}
      <Section theme={theme} scrim={false}>
        <div style={{ maxWidth: '860px', margin: '0 auto' }}>
          <DetailBlock label="Workflow">
            <Text variant="body">{useCase.workflow}</Text>
          </DetailBlock>

          <DetailBlock label="Orchestration">
            <Text variant="body">{useCase.orchestration}</Text>
          </DetailBlock>

          <DetailBlock label="Agents Involved">
            <Stack direction="horizontal" gap={2} wrap>
              {useCase.agentsInvolved.map((agent) => (
                <span
                  key={agent}
                  style={{
                    fontSize: tokens.typography.fontSize.caption,
                    padding: `${tokens.spacing[1]} ${tokens.spacing[3]}`,
                    borderRadius: tokens.radius.full,
                    backgroundColor: 'rgba(0, 191, 255, 0.1)',
                    color: '#00BFFF',
                    fontWeight: 500,
                  }}
                >
                  {agent}
                </span>
              ))}
            </Stack>
          </DetailBlock>

          <DetailBlock label="Inputs">
            <Text variant="body">{useCase.inputs.join(' · ')}</Text>
          </DetailBlock>

          <DetailBlock label="Tools">
            <Text variant="body">{useCase.tools.join(' · ')}</Text>
          </DetailBlock>

          <DetailBlock label="Human Approval">
            <Text variant="body">{useCase.humanApproval}</Text>
          </DetailBlock>

          <DetailBlock label="Output">
            <Text variant="body">{useCase.output}</Text>
          </DetailBlock>

          {useCase.evidence && (
            <DetailBlock label="Evidence">
              <Text variant="body">{useCase.evidence}</Text>
            </DetailBlock>
          )}

          <div
            style={{
              marginTop: tokens.spacing[8],
              padding: tokens.spacing[6],
              borderRadius: tokens.radius.medium,
              border: `1px solid ${isDark ? 'rgba(0,191,255,0.35)' : 'rgba(0,191,255,0.4)'}`,
              backgroundColor: isDark ? 'rgba(0,191,255,0.06)' : 'rgba(0,191,255,0.05)',
            }}
          >
            <Text
              variant="caption"
              secondary
              style={{ display: 'block', marginBottom: tokens.spacing[2], fontWeight: 700, letterSpacing: '0.08em' }}
            >
              BUSINESS VALUE
            </Text>
            <Text variant="body" style={{ fontWeight: 600 }}>
              {useCase.businessValue}
            </Text>
          </div>

          {relatedSolutions.length > 0 && (
            <div style={{ marginTop: tokens.spacing[8], borderTop: `1px solid ${isDark ? tokens.colors.grey[700] : tokens.colors.grey[200]}`, paddingTop: tokens.spacing[5] }}>
              <Text
                variant="caption"
                secondary
                style={{ display: 'block', marginBottom: tokens.spacing[3], fontWeight: 700, letterSpacing: '0.08em' }}
              >
                RELATED SOLUTIONS
              </Text>
              <Stack direction="horizontal" gap={2} wrap>
                {relatedSolutions.map((solutionSlug) => (
                  <Link
                    key={solutionSlug}
                    to={`/solutions#${solutionSlug}`}
                    style={{
                      fontSize: tokens.typography.fontSize.caption,
                      fontWeight: 600,
                      padding: `${tokens.spacing[2]} ${tokens.spacing[3]}`,
                      borderRadius: tokens.radius.full,
                      border: `1px solid ${isDark ? tokens.colors.grey[600] : tokens.colors.grey[300]}`,
                      color: isDark ? tokens.colors.white : tokens.colors.navy,
                      textDecoration: 'none',
                    }}
                  >
                    {solutionTitle(solutionSlug)}
                  </Link>
                ))}
              </Stack>
            </div>
          )}
        </div>
      </Section>
    </PageContainer>
  );
};

export default UseCaseDetailPage;
