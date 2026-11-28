import companyIdentity from './shipped/company';

export interface PublicMetric {
  id: string;
  value: string;
  label: string;
  /** Claim id in src/data/registries/claims-registry.json that grounds this tile. */
  claimId: string;
}

export const aboutMetrics: readonly PublicMetric[] = [
  {
    id: 'operating-roles',
    value: String(companyIdentity.totalRoles),
    label: 'Operating Roles (89 Agents + 1 Human CEO)',
    claimId: 'claim.agent-count',
  },
  {
    id: 'haomtgv-layers',
    value: '7',
    label: 'HAOMTGV Operating Layers',
    claimId: 'claim.haomtgv-seven-layers',
  },
  {
    id: 'approval-tiers',
    value: String(companyIdentity.governanceTiers),
    label: 'Human Approval Tiers',
    claimId: 'claim.five-tier-approval',
  },
  {
    id: 'departments',
    value: String(companyIdentity.departmentCount),
    label: 'Departments',
    claimId: 'claim.department-count',
  },
];
