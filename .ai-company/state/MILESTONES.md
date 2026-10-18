# Milestones

> **Last Updated**: 2026-10-18

---

## Milestone Tracking

| # | Name | Phase | Status | Date |
|---|------|-------|--------|------|
| M1 | Configuration Foundation | Foundation | Complete | 2026-07-16 |
| M2 | Template & Generation | Foundation | Complete | 2026-07-16 |
| M3 | Bootstrap Engine | Foundation | Complete | 2026-07-16 |
| M4 | Decision & Workflow | Foundation | Complete | 2026-07-16 |
| M5 | Memory & Graph | Foundation | Complete | 2026-07-16 |
| M6 | CLI & Documentation | Foundation | Complete | 2026-07-16 |
| M7 | Constitution Framework | Infrastructure | Complete | 2026-07-16 |
| M8 | Task Execution Loop | Autonomy | Complete | 2026-10-18 |
| M9 | HITL Gates | Autonomy | Complete | 2026-10-18 |
| M10 | Briefing & Scheduler | Autonomy | Complete | 2026-10-18 |
| M11 | LLM Hardening | Autonomy | Complete | 2026-10-18 |
| M12 | Performance Analytics | Learning | Planned | — |

---

## Milestone Details

### M1: Configuration Foundation (Complete)

**Deliverables**:
- 19 YAML configuration files
- 17+ Pydantic domain models
- Registry system (loader, parser, resolver, validator)
- Config loader entry point

**Tests**: 21 new tests

### M2: Template & Generation (Complete)

**Deliverables**:
- 7 Jinja2 templates with inheritance
- Base template with block system
- AgentGenerator with template selection
- generate_from_registry() for full generation

**Tests**: 5 new tests

### M3: Bootstrap Engine (Complete)

**Deliverables**:
- BootstrapEngine class
- Directory creation (24 directories)
- Agent generation from registry
- Config generation (4 YAML files)
- CLI `company run` command

**Tests**: 7 new tests

### M4: Decision & Workflow (Complete)

**Deliverables**:
- DecisionEngine (approval matrix, risk assessment, decision tree)
- WorkflowEngine (9 workflows, step tracking, SLA)
- CLI commands for both engines

**Tests**: 23 new tests

### M5: Memory & Graph (Complete)

**Deliverables**:
- MemoryStore (6 types, persistence, consolidation)
- GraphEngine (4 types, BFS pathfinding)
- CLI commands for both engines

**Tests**: 25 new tests

### M6: CLI & Documentation (Complete)

**Deliverables**:
- Full CLI wiring (22 commands)
- Documentation updates (STATUS.md, ARCHITECTURE.md)

**Tests**: CLI verification

### M7: Constitution Framework (Complete)

**Deliverables**:
- 16 constitution documents
- 10 state documents
- 5 supporting directories
- Full cross-referencing

**Tests**: Structural verification

### M8: Task Execution Loop (Complete)

**Deliverables**:
- MessageBus task queue with target/role routing (GAP-001, GAP-002)
- Executor loop lifecycle: claim → run → complete/fail → dead-letter
- Dead-letter queue + retry/self-healing (`orchestrator/dead_letter.py`)
- Delegation: tool `task`/`delegate` → `bus.send_task` → subtask (loop.py, tool_runner.py, tier_rules.py)
- Scheduler integration at loop start: `Scheduler.create_pending_tasks` (loop.py)
- Graceful shutdown: SIGTERM/SIGINT + stop sentinel (daemon.py, cli/executor.py)
- Daemon (autonomous background executor)

**Tests**: 157 scoped tests

### M9: HITL Gates (Complete)

**Deliverables**:
- ApprovalGate with 5-tier approval matrix (risk-based)
- Non-blocking task state `waiting_approval` (GAP-004)
- Approval expiry sweep → `EXPIRED` terminal state (AGENTS.md §9.1)
- Notifications: WebSocket broadcast + webhook notifier (`orchestrator/notifier.py`)
- Escalation rules engine + event log (`orchestrator/escalation.py`, `escalation_events.py`, GAP-008)
- Dashboard approval/reject endpoints

**Tests**: 174 scoped tests

### M10: Briefing & Scheduler (Complete)

**Deliverables**:
- BriefingGenerator (`orchestrator/briefing.py`) → `.opencode/daily_briefing.md`
- CLI `ai-company orchestrator briefing`
- Dashboard API `GET /api/v1/briefing`
- CI cron briefing: `.github/workflows/autonomous.yml` (`0 */6 * * *`, uploads briefing artifact)
- Scheduler with `cron_expression` / `interval_minutes` → pending tasks (`orchestrator/scheduler.py`)
- Daemon-scheduled routines: KPI snapshot, governance retention, Pharos routines

**Tests**: 48 scoped tests

### M11: LLM Hardening (Complete)

**Deliverables**:
- Multi-provider client (`llm/providers/`: openai_compatible, ollama, llamacpp)
- Circuit breaker (`llm/circuit_breaker.py`)
- Cost tracking + token counting (`llm/cost_tracker.py`, `token_counter.py`)
- Rate limiting (`llm/token_bucket.py`)
- Response cache (`llm/response_cache.py`)
- Prompt compression (`llm/prompt_compressor.py`)
- Structured-output JSON parser (`llm/json_parser.py`)
- OAuth2 support (`llm/oauth2.py`)

**Tests**: 84 scoped tests

---

## Related Documents

- [PROJECT_STATUS.md](PROJECT_STATUS.md) — Current status
- [ROADMAP.md](ROADMAP.md) — Full roadmap
- [RELEASE_PLAN.md](RELEASE_PLAN.md) — Release schedule
- [CHANGELOG.md](CHANGELOG.md) — Version history
