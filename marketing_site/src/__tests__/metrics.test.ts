import { describe, it, expect } from 'vitest';
import { metrics, liveTestCount } from '../data/metrics';
import metricsRegistry from '../data/registries/metrics-registry.json';
import claimsRegistry from '../data/registries/claims-registry.json';

/**
 * Guards the published numbers against the canonical registries.
 * Verified 2026-10-25:
 *   uv run pytest --collect-only -q  -> 2684/2751 collected (67 deselected)
 *   npx vitest run                   -> 87 passed
 */
describe('metrics registry parity', () => {
  it('publishes the collected pytest count in both places', () => {
    expect(liveTestCount).toBe(2684);
    expect(metricsRegistry.metrics.testCount.value).toBe(liveTestCount);
  });

  it('keeps the vitest snapshot consistent with the registry', () => {
    expect(Number.isInteger(metrics.testCount)).toBe(true);
    expect(metrics.testCount).toBeGreaterThan(0);
    expect(metricsRegistry.metrics.testCount.description).toContain(`${metrics.testCount} passing`);
  });

  it('keeps the agent breakdown internally consistent', () => {
    const { agentCount, aiAgentCount, humanCeoCount, departmentCount } = metricsRegistry.metrics;
    expect(agentCount.value).toBe(metrics.agentCount);
    expect(aiAgentCount.value).toBe(89);
    expect(humanCeoCount.value).toBe(1);
    expect(aiAgentCount.value + humanCeoCount.value).toBe(agentCount.value);
    expect(departmentCount.value).toBe(metrics.departments);
  });

  it('points the test-count claim at the current value and date', () => {
    const claim = claimsRegistry.claims.find((c) => c.id === 'claim.test-count');
    expect(claim).toBeDefined();
    expect(claim?.text).toContain(liveTestCount.toLocaleString('en-US'));
    expect(claim?.evidenceRef).toContain(String(liveTestCount));
    expect(claim?.lastVerified).toBe('2026-10-25');
  });
});
