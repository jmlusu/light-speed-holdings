/**
 * Use Cases Page
 *
 * Use Case explorer page (Directive §10, §11).
 * Interactive Use Case explorer with filters
 * Directive §11
 */

import React, { useEffect, useState, useMemo, useLocation } from 'react';
import { Link, useNavigate } from 'react-router-dom';
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
import { tokens } from '@lightspeed/design-system/tokens';
import { useCasesRegistry, getUseCasesByStatus, getUseCasesBySector, getUseCasesBySolution, getUseCasesByProblemCategory, getFeaturedUseCases, UseCase, UseCaseStatus, ProblemCategory, SolutionCategory } from '../data/use-cases/registry';
import { sectorsRegistry } from '../data/sectors/registry';
import { solutionsRegistry } from '../data/solutions/registry';

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
  const location = useLocation();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  // Extract filters from URL query params
  const { status: urlStatus, problemCategory: urlProblemCategory, solutionCategory: urlSolutionCategory, sector: urlSector, search: urlSearch } = new URLSearchParams(location.search);

  // State initialized from URL, defaulting to 'all'
  const [statusFilter, setStatusFilter] = useState<UseCaseStatus | 'all'>(urlStatus ? (urlStatus === 'all' ? 'all' : (urlStatus as UseCaseStatus)) : 'all');
  const [problemFilter, setProblemFilter] = useState<ProblemCategory | 'all'>(urlProblemCategory ? urlProblemCategory : 'all');
  const [solutionFilter, setSolutionFilter] = useState<SolutionCategory | 'all'>(urlSolutionCategory ? urlSolutionCategory : 'all');
  const [sectorFilter, setSectorFilter] = useState<string | 'all'>(urlSector ? urlSector : 'all');

  // Sync URL when filters change (debounced to avoid excessive URL updates)
  useEffect(() => {
    const params = new URLSearchParams();
    if (statusFilter !== 'all') params.set('status', statusFilter);
    else params.delete('status');

    if (problemFilter !== 'all') params.set('problemCategory', problemFilter);
    else params.delete('problemCategory');

    if (solutionFilter !== 'all') params.set('solutionCategory', solutionFilter);
    else params.delete('solutionCategory');

    if (sectorFilter !== 'all') params.set('sector', sectorFilter);
    else params.delete('sector');

    if (searchQuery) params.set('search', searchQuery);
    else params.delete('search');

    const newSearch = location.pathname + '?' + params.toString();
    navigate(newSearch, { replace: true });
  }, [statusFilter, problemFilter, solutionFilter, sectorFilter, searchQuery, navigate, location.pathname]);

  const filteredUseCases = useMemo(() => {
    let cases = useCasesRegistry;

    if (statusFilter !== 'all') {
      cases = cases.filter(uc => uc.status === statusFilter);
    }
    if (problemFilter !== 'all') {
      cases = cases.filter(uc => uc.problemCategory?.includes(problemFilter) ?? false);
    }
    if (solutionFilter !== 'all') {
      cases = cases.filter(uc => uc.solutionCategory?.includes(solutionFilter) ?? false);
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
      {/* HeroSection */}
      <Section label="Use Cases" theme={isDark ? 'dark' : 'light'}>
        <div style={{ maxWidth: '800px', margin: '0 auto', position: 'relative' }}>
          <Badge variant="proven" style={{ marginBottom: tokens.spacing[4] }}>
            USE CASES
          </Badge>
          <Heading level={1} style={{ marginBottom: tokens.spacing[4] }}>
            <span style={{ color: isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600], textShadow: 'none' }}>
              What Can LightSpeed Actually Do?
            </span>
          </Heading>
          <Text variant="lead" style={{ marginBottom: tokens.spacing[8], maxWidth: '700px', margin: '0 auto' }}>
            Explore verified use cases across sectors, problems, and solutions. Every case carries an evidence status, from proven in-house to future roadmap targets. No fabricated client evidence.
          </Text>
          {/* Two CTAs */}
          <div style={{ marginTop: tokens.spacing[8], display: 'flex', justifyContent: 'center', gap: tokens.spacing[4] }}>
            <button
              style={{
                padding: `${tokens.spacing[3]} ${tokens.spacing[6]}`,
                borderRadius: tokens.radius.medium,
                border: `1px solid ${isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600]}`,
                backgroundColor: 'transparent',
                color: isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600],
                fontFamily: tokens.typography.fontFamily.sans,
                fontSize: tokens.typography.fontSize.body,
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              View All Use Cases
            </button>
            <button
              style={{
                padding: `${tokens.spacing[3]} ${tokens.spacing[6]}`,
                borderRadius: tokens.radius.medium,
                border: `1px solid ${isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600]}`,
                backgroundColor: isDark ? tokens.colors.cyan[600] : tokens.colors.cyan[600],
                color: 'white',
                fontFamily: tokens.typography.fontFamily.sans,
                fontSize: tokens.typography.fontSize.body,
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Start a New Project
            </button>
          </div>
          {/* Right-side vertical status legend pills */}
          <div style={{ position: 'absolute', right: 0, top: 0, margin: tokens.spacing[6], display: 'flex', flexDirection: 'column', gap: tokens.spacing[1], alignItems: 'flex-end' }}>
            <span style={{ fontSize: tokens.typography.fontSize.xs, color: isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600], fontWeight: 500 }}>
              Status Legend:
            </span>
            <span style={{ fontSize: tokens.typography.fontSize.xs, color: isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600], fontWeight: 500 }}>
              <span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: '50%', backgroundColor: '#00BFFF' }} /> PROVEN
            </span>
            <span style={{ fontSize: tokens.typography.fontSize.xs, color: isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600], fontWeight: 500 }}>
              <span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: '50%', backgroundColor: '#07C551' }} /> PILOT
            </span>
            <span style={{ fontSize: tokens.typography.fontSize.xs, color: isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600], fontWeight: 500 }}>
              <span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: '50%', backgroundColor: '#00E597' }} /> FIELDABLE
            </span>
            <span style={{ fontSize: tokens.typography.fontSize.xs, color: isDark ? tokens.colors.cyan[400] : tokens.colors.cyan[600], fontWeight: 500 }}>
              <span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: '50%', backgroundColor: '#FF006E' }} /> FUTURE
            </span>
          </div>
        </div>
      </Section>

      {/* Filters Section - stacked vertically at 390px */}
      <Section theme={isDark ? 'dark' : 'light'} scrim={false}>
        <div style={{ maxWidth: '100%', margin: '0 auto' }}>
          <Stack direction="vertical" gap="component" style={{ maxWidth: '390px', margin: '0 auto' }}>
            <div style={{ minWidth: '100%' }}>
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

            <div style={{ minWidth: '100%' }}>
              <label style={{ display: 'block', marginBottom: tokens.spacing[1], fontSize: tokens.typography.fontSize.caption, fontWeight: 600, color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[600] }}>
                Problem Category
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
                <option value="all">All Problem Categories</option>
                {PROBLEM_CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div style={{ minWidth: '100%' }}>
              <label style={{ display: 'block', marginBottom: tokens.spacing[1], fontSize: tokens.typography.fontSize.caption, fontWeight: 600, color: isDark ? tokens.colors.grey[400] : tokens.colors.grey[600] }}>
                Solution Category
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
                <option value="all">All Solution Categories</option>
                {SOLUTION_CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div style={{ minWidth: '100%' }}>
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

          <div style={{ maxWidth: '600px', margin: '0 auto', marginTop: tokens.spacing[4] }}>
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
          {(useCase.problemCategory || []).slice(0, 2).map(cat => (
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
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: tokens.spacing[1], marginBottom: tokens.spacing[3] }}>
          {(useCase.solutionCategory || []).slice(0, 2).map(cat => (
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
            <Link
              to={`/use-cases/${useCase.slug}`}
              className="inline-flex items-center gap-1 text-xs font-bold text-ls-red transition-colors hover:text-ls-red/80 hover:underline"
            >
              View Details
              <ChevronRight size={14} aria-hidden="true" />
            </Link>
          </Stack>
        </div>
      </Stack>
    </Card>
  );
};

export default UseCasesPage;
