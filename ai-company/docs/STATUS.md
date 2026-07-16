# Project Status

> If `harness/changes/active/summary.md` exists, active change files are the current task source of truth. Read them first.

## Last Updated

2026-07-16

## Current State

- **V2 Complete**: All 6 milestones delivered. Full Infrastructure-as-Code platform built.
- **Models**: 17+ Pydantic models in `src/ai_company/models/models.py` (Company, Executive, Department, Agent, Workflow, Task, Risk, Decision, etc.)
- **Registry**: 4-module system — `registry/loader.py`, `parser.py`, `resolver.py`, `validator.py` — loads 19 YAML config files into typed `CompanyRegistry`.
- **Templates**: 7 Jinja2 templates with inheritance — `base.md.j2`, `executive.md.j2`, `department.md.j2`, `specialist_v2.md.j2`, `board_v2.md.j2`, `workflow.md.j2`, `config.md.j2`.
- **Generator**: Template selection by agent type + `generate_from_registry()` for full registry-based generation.
- **BootstrapEngine**: `builder/__init__.py` — creates 24 directories, generates agents + configs from registry.
- **DecisionEngine**: `decision/engine.py` — evaluates actions against approval matrix, risk assessment, decision tree navigation.
- **WorkflowEngine**: `workflow/engine.py` — 9 workflow definitions, step tracking, SLA monitoring, task conversion.
- **MemoryEngine**: `memory/engine.py` — 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate) with persistence.
- **GraphEngine**: `graph/engine.py` — 4 graph types (org_chart, decision_graph, workflow_graph, knowledge_graph) with BFS pathfinding.
- **CLI**: 22 commands registered — company, decision, graph, workflows, memory, agents, board, departments, executives, specialists, orchestrator, models, dashboard, executor, doctor, marketing, sales, customer-success, legal, hr, generate, status.
- **Tests**: 175 passing, mypy clean, ruff clean (only pre-existing E402 in llm/client.py).

## Pre-existing Issues

- E402 import order warnings in `src/ai_company/llm/client.py` (not blocking).

## Recent Work

- **M1**: Config YAMLs (19 files), 17+ Pydantic models, registry system (loader/parser/resolver/validator), 21 new tests.
- **M2**: 7 Jinja2 templates with inheritance, multi-format generator with template selection.
- **M3**: BootstrapEngine — generates all agents, configs, directories from registry. CLI `company run` command.
- **M4**: DecisionEngine (approval matrix, risk assessment, decision tree) + WorkflowEngine (9 workflows, step tracking, SLA). 23 new tests.
- **M5**: MemoryEngine (6 types, persistence, consolidation) + GraphEngine (4 types, BFS pathfinding). 25 new tests.
- **M6**: Full CLI wiring (22 commands), documentation updates.
