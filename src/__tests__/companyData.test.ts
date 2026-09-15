import { describe, it, expect } from 'vitest';
import {
  agentsList,
  departmentsList,
  initialTasks,
  initialApprovals,
  initialEscalations,
  initialKPIs,
  modelTiers,
  initialAuditLog,
} from '../data/companyData';

describe('agentsList', () => {
  it('should load agents from agent-registry.json', () => {
    expect(agentsList).toBeDefined();
    expect(Array.isArray(agentsList)).toBe(true);
    expect(agentsList.length).toBeGreaterThan(0);
  });

  it('should have 144 agents', () => {
    expect(agentsList.length).toBe(144);
  });

  it('every agent should have required fields', () => {
    agentsList.forEach((agent) => {
      expect(agent.name).toBeTruthy();
      expect(agent.role).toBeTruthy();
      expect(agent.department).toBeTruthy();
      expect(agent.reportsTo).toBeTruthy();
      expect(agent.description).toBeDefined();
      expect(Array.isArray(agent.responsibilities)).toBe(true);
      expect(Array.isArray(agent.tools)).toBe(true);
      expect(agent.permission).toBeTruthy();
    });
  });

  it('every agent should have a valid type', () => {
    const validTypes = ['Executive', 'Specialist', 'Manager', 'Board'];
    agentsList.forEach((agent) => {
      expect(validTypes).toContain(agent.type);
    });
  });

  it('should have unique agent names', () => {
    const names = agentsList.map((a) => a.name);
    const unique = new Set(names);
    expect(unique.size).toBe(names.length);
  });

  it('every agent should have at least one tool', () => {
    agentsList.forEach((agent) => {
      expect(agent.tools.length).toBeGreaterThan(0);
    });
  });
});

describe('departmentsList', () => {
  it('should have 20 departments', () => {
    expect(departmentsList.length).toBe(20);
  });

  it('every department should have required fields', () => {
    departmentsList.forEach((dept) => {
      expect(dept.id).toBeTruthy();
      expect(dept.name).toBeTruthy();
      expect(dept.executive).toBeTruthy();
      expect(dept.mission).toBeTruthy();
      expect(dept.budget_category).toBeTruthy();
      expect(dept.headcount_target).toBeGreaterThan(0);
    });
  });

  it('should have unique department IDs', () => {
    const ids = departmentsList.map((d) => d.id);
    const unique = new Set(ids);
    expect(unique.size).toBe(ids.length);
  });
});

describe('initialTasks', () => {
  it('should be a non-empty array', () => {
    expect(Array.isArray(initialTasks)).toBe(true);
    expect(initialTasks.length).toBeGreaterThan(0);
  });

  it('every task should have required fields', () => {
    initialTasks.forEach((task) => {
      expect(task.id).toBeTruthy();
      expect(task.title).toBeTruthy();
      expect(task.status).toBeTruthy();
      expect(task.priority).toBeTruthy();
    });
  });
});

describe('initialApprovals', () => {
  it('should be a non-empty array', () => {
    expect(Array.isArray(initialApprovals)).toBe(true);
    expect(initialApprovals.length).toBeGreaterThan(0);
  });
});

describe('initialEscalations', () => {
  it('should be a non-empty array', () => {
    expect(Array.isArray(initialEscalations)).toBe(true);
  });
});

describe('initialKPIs', () => {
  it('should be a non-empty array', () => {
    expect(Array.isArray(initialKPIs)).toBe(true);
    expect(initialKPIs.length).toBeGreaterThan(0);
  });

  it('every KPI should have required fields', () => {
    initialKPIs.forEach((kpi) => {
      expect(kpi.id).toBeTruthy();
      expect(kpi.department).toBeTruthy();
      expect(kpi.name).toBeTruthy();
      expect(typeof kpi.current).toBe('number');
      expect(kpi.unit).toBeTruthy();
    });
  });
});

describe('modelTiers', () => {
  it('should have 3 tiers', () => {
    expect(modelTiers.length).toBe(3);
  });
});

describe('initialAuditLog', () => {
  it('should be an array', () => {
    expect(Array.isArray(initialAuditLog)).toBe(true);
  });
});
