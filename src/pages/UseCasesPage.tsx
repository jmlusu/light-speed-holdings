/**
 * Use Cases Page
 *
 * Replaces ProofPage per Directive §10
 * Interactive Use Case explorer with filters
 * Directive §11
 */

import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';
import { PageContainer } from '../layouts/PageContainer';
import { Section } from '@lightspeed/design-system';
import { Heading } from '@lightspeed/design-system';
import { Text } from '@lightspeed/design-system';
import { Card } from '@lightspeed/design-system';
import { Badge } from '@lightspeed/design-system';
import { BadgeVariant } from '@lightspeed/design-system';
import { Stack } from '@lightspeed/design-system';
import { Grid } from '@lightspeed/design-system';
import { Button } from '@lightspeed/design-system';
import { tokens } from '@lightspeed/design-system/tokens';
import { useCasesRegistry, getUseCasesByStatus, getUseCasesBySector, getUseCasesBySolution, getUseCasesByProblemCategory, getFeaturedUseCases, UseCase, UseCaseStatus, ProblemCategory, SolutionCategory } from '@lightspeed/data/use-cases';
import { sectorsRegistry } from '@lightspeed/data/sectors';
import { solutionsRegistry } from '@lightspeed/data/solutions';

const STATUS_OPTIONS: { value: UseCaseStatus; label: string }[] = [
  { value: 'LIVE', label: 'Live' },
  { value: 'PROVEN_IN_HOUSE', label: 'Proven In-House' },
  { value: 'PILOT', label: 'Pilot' },
  { value: 'DEMONSTRATION', label: 'Demonstration' },
  { value: 'FIELDABLE', label: 'Fieldable' },
  { value: 'FUTURE', label: 'Future' },
];

const PROBLEM_CATEGORIES: ProblemCategory[] = [
  'Cost', 'Operational Latency', 'Compliance', 'Reporting', 'Customer Experience',
  'Decision Intelligence', 'Growth', 'Administration', 'Research', 'Knowledge Work', 'Market Intelligence',
];

const SOLUTION_CATEGORIES = [
  'Strategy', 'Agentic Automation', 'Data & Intelligence', 'Digital Transformation', 'AI Governance', 'Research & Policy',
];

const SECTOR_OPTIONS = sectorsRegistry.map(s => ({ value: s.id, label: s.title }));

export const UseCasesPage: React.FC = () => {
  const isDark = document.documentElement.classList.contains('dark');

  const [statusFilter, setStatusFilter] = useState<UseCaseStatus | 'all'>('all');
  const [problemFilter, setProblemFilter] = useState<ProblemCategory | 'all'>('all');
  const [solutionFilter, setSolutionFilter] = useState<SolutionCategory | 'all'>('all');
  const [sectorFilter, setSectorFilter] = useState<string | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredUseCases = useMemo(() => {
    let cases = useCasesRegistry;

    if (statusFilter !== 'all') {
      cases = cases.filter(uc => uc.status === statusFilter);
    }
    if (problemFilter !== 'all') {
      cases = cases.filter(uc => uc.problemCategory.includes(problemFilter));
    }
    if (solutionFilter !== 'all') {
      cases = cases.filter(uc => uc.solutionCategory.includes(solutionFilter));
    }
    if (sectorFilter !== 'all') {
      cases = cases.filter(uc => uc.sector.includes(sectorFilter));
    }
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      cases = cases.filter(uc =>
        uc.title.toLowerCase().includes(query) ||
        uc.problem.toLowerCase().includes(query) ||
        uc.businessValue.toLowerCase().includes(query)
      );
    }

    return cases;
  }, [statusFilter, problemFilter, solutionFilter, sectorFilter, searchQuery]);

  const featuredCases = getFeaturedUseCases();

  return (
    <PageContainer>
      {/* Hero Section */}
      <Section label="Use Cases" theme={isDark ? 'dark' : 'light'}>
        <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
          <Badge variant="proven" style={{ marginBottom: tokens.spacing[4] }}>
            USE CASES
          </Badge>
          <Heading level={1} style={{ marginBottom: tokens.spacing[4] }}>
            What Can LightSpeed Actually Do?
          </Heading>
          <Text variant="lead" style={{ marginBottom: tokens.spacing[8], maxWidth: '700px', margin: '0 auto' }}>
            Explore verified use cases across sectors, problems, and solutions. Every case carries an evidence status — from proven in-house to future roadmap targets. No fabricated client evidence.
          </Text>
        </div>
      </Section>

      {/* Filters Section */}
      <Section theme={isDark ? 'dark' : 'light'} scrim={false}>
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
          <Stack direction="horizontal" gap="component" wrap justify="center" style={{ marginBottom: tokens.spacing[6] }}>
            <div style={{ minWidth: '200px' }}>
              <label style={{ display: 'block', marginBottom: tokens.spacing[1], fontSize: tokens.typography.fontSize.caption, fontWeight: 600, color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[600] }}>
                Status
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as UseCaseStatus | 'all')}
                style={{
                  width: '100%',
                  padding: `${tokens.spacing[2]} ${tokens.spacing[3]}`,
                  borderRadius: tokens.radius.small,
                  border: `1px solid ${isDark ? tokens.colors.grey[700] : tokens.colors.grey[300]}`,
                  backgroundColor: isDark ? tokens.colors.navy : tokens.colors.white,
                  color: isDark ? tokens.colors.white : tokens.colors.navy,
                  fontFamily: tokens.typography.fontFamily.sans,
                  fontSize: tokens.typography.fontSize.bodySm,
                }}
              >
                <option value="all">All Statuses</option>
                {STATUS_OPTIONS.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>

            <div style={{ minWidth: '200px' }}>
              <label style={{ display: 'block', marginBottom: tokens.spacing[1], fontSize: tokens.typography.fontSize.caption, fontWeight: 600, color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[600] }}>
                Problem
              </label>
              <select
                value={problemFilter}
                onChange={(e) => setProblemFilter(e.target.value as ProblemCategory | 'all')}
                style={{
                  width: '100%',
                  padding: `${tokens.spacing[2]} ${tokens.spacing[3]}`,
                  borderRadius: tokens.radius.small,
                  border: `1px solid ${isDark ? tokens.colors.grey[700] : tokens.colors.grey[300]}`,
                  backgroundColor: isDark ? tokens.colors.navy : tokens.colors.white,
                  color: isDark ? tokens.colors.white : tokens.colors.navy,
                  fontFamily: tokens.typography.fontFamily.sans,
                  fontSize: tokens.typography.fontSize.bodySm,
                }}
              >
                <option value="all">All Problems</option>
                {PROBLEM_CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div style={{ minWidth: '200px' }}>
              <label style={{ display: 'block', marginBottom: tokens.spacing[1], fontSize: tokens.typography.fontSize.caption, fontWeight: 600, color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[600] }}>
                Solution
              </label>
              <select
                value={solutionFilter}
                onChange={(e) => setSolutionFilter(e.target.value as SolutionCategory | 'all')}
                style={{
                  width: '100%',
                  padding: `${tokens.spacing[2]} ${tokens.spacing[3]}`,
                  borderRadius: tokens.radius.small,
                  border: `1px solid ${isDark ? tokens.colors.grey[700] : tokens.colors.grey[300]}`,
                  backgroundColor: isDark ? tokens.colors.navy : tokens.colors.white,
                  color: isDark ? tokens.colors.white : tokens.colors.navy,
                  fontFamily: tokens.typography.fontFamily.sans,
                  fontSize: tokens.typography.fontSize.bodySm,
                }}
              >
                <option value="all">All Solutions</option>
                {SOLUTION_CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div style={{ minWidth: '200px' }}>
              <label style={{ display: 'block', marginBottom: tokens.spacing[1], fontSize: tokens.typography.fontSize.caption, fontWeight: 600, color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[600] }}>
                Sector
              </label>
              <select
                value={sectorFilter}
                onChange={(e) => setSectorFilter(e.target.value)}
                style={{
                  width: '100%',
                  padding: `${tokens.spacing[2]} ${tokens.spacing[3]}`,
                  borderRadius: tokens.radius.small,
                  border: `1px solid ${isDark ? tokens.colors.grey[700] : tokens.colors.grey[300]}`,
                  backgroundColor: isDark ? tokens.colors.navy : tokens.colors.white,
                  color: isDark ? tokens.colors.white : tokens.colors.navy,
                  fontFamily: tokens.typography.fontFamily.sans,
                  fontSize: tokens.typography.fontSize.bodySm,
                }}
              >
                <option value="all">All Sectors</option>
                {SECTOR_OPTIONS.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
          </Stack>

          <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            <input
              type="search"
              placeholder="Search use cases..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: `${tokens.spacing[3]} ${tokens.spacing[4]}`,
                borderRadius: tokens.radius.small,
                border: `1px solid ${isDark ? tokens.colors.grey[700] : tokens.colors.grey[300]}`,
                backgroundColor: isDark ? tokens.colors.navy : tokens.colors.white,
                color: isDark ? tokens.colors.white : tokens.colors.navy,
                fontFamily: tokens.typography.fontFamily.sans,
                fontSize: tokens.typography.fontSize.body,
              }}
            />
          </div>
        </div>
      </Section>

      {/* Featured Use Cases */}
      {featuredCases.length > 0 && (
        <Section label="Featured" theme={isDark ? 'dark' : 'light'}>
          <Grid columns={1} columnsTablet={2} columnsDesktop={3} gap="component">
            {featuredCases.map((uc) => (
              <UseCaseCard key={uc.slug} useCase={uc} />
            ))}
          </Grid>
        </Section>
      )}

      {/* All Use Cases */}
      <Section label={`All Use Cases (${filteredUseCases.length})`} theme={isDark ? 'dark' : 'light'}>
        <Grid columns={1} columnsTablet={2} columnsDesktop={3} gap="component">
          {filteredUseCases.map((uc) => (
            <UseCaseCard key={uc.slug} useCase={uc} />
          ))}
        </Grid>
        {filteredUseCases.length === 0 && (
          <div style={{ textAlign: 'center', padding: tokens.spacing[16], color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[500] }}>
            <p>No use cases match your filters. Try adjusting your criteria.</p>
          </div>
        )}
      </Section>
    </PageContainer>
  );
};

interface UseCaseCardProps {
  useCase: UseCase;
}

const STATUS_BADGE_VARIANTS: Record<UseCaseStatus, BadgeVariant> = {
  LIVE: 'fieldable',
  PROVEN_IN_HOUSE: 'proven',
  PILOT: 'pilot',
  DEMONSTRATION: 'development',
  FIELDABLE: 'fieldable',
  FUTURE: 'neutral',
};

const UseCaseCard: React.FC<UseCaseCardProps> = ({ useCase }) => {
  const isDark = document.documentElement.classList.contains('dark');
  const navigate = useNavigate();
  const sector = sectorsRegistry.find(s => s.id === useCase.sector[0]);

  return (
    <Card variant="default" hover padding="md">
      <Stack gap={3} style={{ minHeight: '100%' }}>
        <div>
          <Stack direction="horizontal" gap={2} wrap style={{ marginBottom: tokens.spacing[2] }}>
            <Badge variant={STATUS_BADGE_VARIANTS[useCase.status]}>
              {useCase.status.replace('_', ' ')}
            </Badge>
            {sector && (
              <Badge variant="neutral">{sector.title}</Badge>
            )}
          </Stack>
          <Heading level={3} style={{ fontSize: tokens.typography.fontSize.titleSm, marginBottom: tokens.spacing[2] }}>
            {useCase.title}
          </Heading>
        </div>
        <Text variant="body" muted style={{ flex: 1, marginBottom: tokens.spacing[3] }}>
          {useCase.problem}
        </Text>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: tokens.spacing[1], marginBottom: tokens.spacing[3] }}>
          {useCase.problemCategory.slice(0, 2).map(cat => (
            <span
              key={cat}
              style={{
                fontSize: tokens.typography.fontSize.caption,
                padding: `${tokens.spacing[1]} ${tokens.spacing[2]}`,
                borderRadius: tokens.radius.full,
                backgroundColor: 'rgba(0, 191, 255, 0.1)',
                color: '#00BFFF',
                fontWeight: 500,
              }}
            >
              {cat}
            </span>
          ))}
        </div>
        <div style={{ borderTop: `1px solid ${document.documentElement.classList.contains('dark') ? tokens.colors.grey[700] : tokens.colors.grey[200]}`, paddingTop: tokens.spacing[3] }}>
          <Stack direction="horizontal" justify="between" align="center">
            <Text variant="caption" secondary>
              {useCase.businessValue}
            </Text>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(`/use-cases/${useCase.slug}`)}
            >
              View Details
              <ChevronRight size={14} aria-hidden="true" />
            </Button>
          </Stack>
        </div>
      </Stack>
    </Card>
  );
};

export default UseCasesPage;
