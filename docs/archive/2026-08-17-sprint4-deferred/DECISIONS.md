# Architectural Decision Records (ADRs)

> **Last Updated**: 2026-07-16

---

## ADR-001: Single Configuration Source of Truth

**Date**: 2026-07-16
**Status**: Accepted
**Context**: The project evolved from scattered config files to a centralized registry.

### Decision

All company configuration lives in `config/` as 19 YAML files. The `CompanyRegistry` model is the single parsed representation. Generated files are derived artifacts.

### Consequences

- **Positive**: Single source of truth, version-controlled, auditable
- **Positive**: Regeneration is deterministic
- **Negative**: Requires regeneration after config changes
- **Mitigation**: BootstrapEngine makes regeneration trivial

### Alternatives Considered

1. **Database-backed config**: Rejected — adds infrastructure complexity
2. **Distributed config**: Rejected — single directory is simpler
3. **Code-based config**: Rejected — YAML is more accessible to non-developers

---

## ADR-002: Pydantic Models for Domain Objects

**Date**: 2026-07-16
**Status**: Accepted
**Context**: Need typed, validated data models for company structure.

### Decision

Use Pydantic v2+ for all domain models. Models live in `models/models.py`.

### Consequences

- **Positive**: Type safety, validation, serialization
- **Positive**: IDE support, mypy enforcement
- **Negative**: Single large file (560+ lines)
- **Mitigation**: Manageable at 17+ types; split at 30+

### Alternatives Considered

1. **Dataclasses**: Rejected — no validation
2. **attrs**: Rejected — less ecosystem support
3. **SQLAlchemy models**: Rejected — not a database app

---

## ADR-003: Jinja2 Templates for Agent Generation

**Date**: 2026-07-16
**Status**: Accepted
**Context**: Need to generate agent markdown files from config.

### Decision

Use Jinja2 templates with block inheritance for agent generation. Base template defines structure; child templates override specific blocks.

### Consequences

- **Positive**: Template inheritance reduces duplication
- **Positive**: Non-developers can modify templates
- **Negative**: Templates can become complex
- **Mitigation**: Keep business logic in Python, not templates

### Alternatives Considered

1. **String formatting**: Rejected — no inheritance
2. **Mako**: Rejected — Jinja2 is more widely used
3. **Python string templates**: Rejected — no block inheritance

---

## ADR-004: Typer for CLI Framework

**Date**: 2026-07-16
**Status**: Accepted
**Context**: Need a modern CLI framework for 22+ commands.

### Decision

Use Typer for CLI framework. Commands registered in `cli/main.py` via subcommand pattern.

### Consequences

- **Positive**: Type-safe, auto-generated help, rich output
- **Positive**: Composable subcommands
- **Negative**: Typer dependency (but lightweight)
- **Mitigation**: Typer is well-maintained, minimal deps

### Alternatives Considered

1. **Click**: Rejected — Typer is Click with type hints
2. **argparse**: Rejected — too verbose
3. **fire**: Rejected — less structured

---

## ADR-005: Dictionary-Based Engine Dispatch

**Date**: 2026-07-16
**Status**: Accepted
**Context**: Need to add new agent types, memory types, graph types.

### Decision

Use dictionaries for type-to-implementation dispatch:

```python
_TEMPLATE_MAP = {"executive": "executive.md.j2", ...}
_MEMORY_TYPES = {"episodic": [], "semantic": [], ...}
_GRAPH_BUILDERS = {"org_chart": build_org_chart, ...}
```

### Consequences

- **Positive**: Easy to extend (add dictionary entry)
- **Positive**: No code modification for new types
- **Negative**: Not discoverable from interfaces
- **Mitigation**: Document in ARCHITECTURE.md

### Alternatives Considered

1. **Abstract base classes**: Rejected — over-engineering for current scale
2. **Plugin system**: Rejected — premature optimization
3. **match/case**: Rejected — less flexible

---

## ADR-006: JSON File Persistence for Memory

**Date**: 2026-07-16
**Status**: Accepted
**Context**: Memory engine needs persistence but no database infrastructure.

### Decision

Use JSON files for memory persistence. Each memory type has its own JSON file.

### Consequences

- **Positive**: Simple, no infrastructure needed
- **Positive**: Human-readable, debuggable
- **Negative**: Not suitable for high-volume queries
- **Mitigation**: Sufficient for current scale; extract to database later

### Alternatives Considered

1. **SQLite**: Rejected — adds dependency, overkill for v1
2. **Redis**: Rejected — requires running service
3. **In-memory only**: Rejected — data lost on restart

---

## ADR-007: ECL Change Lifecycle

**Date**: 2026-07-16
**Status**: Accepted
**Context**: Need structured process for significant changes.

### Decision

Implement ECL (Engineering Change Lifecycle) with active/parked/archive states, plan review gates, and auto-evolution.

### Consequences

- **Positive**: Structured change process
- **Positive**: Audit trail
- **Positive**: Prevents accidental overwrites
- **Negative**: Overhead for small changes
- **Mitigation**: Skip ECL for trivial fixes (<2 files, no architecture impact)

### Alternatives Considered

1. **GitHub Issues only**: Rejected — no local context loading
2. **No process**: Rejected — chaotic
3. **Heavyweight change management**: Rejected — too bureaucratic

---

## ADR-008: Constitution Framework as Repository Infrastructure

**Date**: 2026-07-16
**Status**: Accepted
**Context**: Need permanent governance that persists across sessions.

### Decision

Create `.ai-company/` directory with constitution, state, templates, examples, diagrams, and reviews. This becomes the operating system for the repository.

### Consequences

- **Positive**: Permanent governance
- **Positive**: Every session starts with context
- **Positive**: Cross-referenced standards
- **Negative**: 36 files to maintain
- **Mitigation**: State files are updated with each sprint

### Alternatives Considered

1. **AGENTS.md only**: Rejected — insufficient for full governance
2. **docs/ directory**: Rejected — mixed with application docs
3. **Wiki**: Rejected — not version-controlled

---

## Related Documents

- [constitution/00-CONSTITUTION.md](../constitution/00-CONSTITUTION.md) — Supreme authority
- [constitution/02-ARCHITECTURE.md](../constitution/02-ARCHITECTURE.md) — Architecture guide
- [TECH_DEBT.md](TECH_DEBT.md) — Known technical debt
