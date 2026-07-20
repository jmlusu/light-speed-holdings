# ADR-001: Why Typer for CLI

**Status:** Accepted
**Date:** 2026-07-17
**Deciders:** CTO, Lead Engineer
**Technical Domain:** CLI Framework

## Context

AI Company Builder needs a command-line interface that supports:
- 24+ subcommands across 7+ domains (orchestrator, executor, dashboard, decision, graph, memory, workflows)
- Nested subcommand groups (e.g., `orchestrator escalation pending`)
- Automatic help generation for every command
- Type-safe argument parsing
- Rich terminal output with tables and colors
- Easy extensibility as new departments and features are added

## Decision

We use **Typer** as the CLI framework for `ai-company`.

## Options Considered

### 1. Typer (chosen)

```python
import typer
app = typer.Typer()

@app.command()
def tick():
    """Run one orchestrator cycle."""
    ...
```

**Pros:**
- Built on Click with Python type hint-driven interface
- Automatic help generation from function signatures and docstrings
- Native support for subcommand groups via `typer.Typer()` nesting
- Rich integration for colored output and tables
- Excellent type safety — arguments inferred from Python types
- Small learning curve for contributors familiar with Python

**Cons:**
- Less flexible than raw Click for deeply nested command trees
- Documentation is thinner than Click's

### 2. Click

**Pros:**
- Mature, battle-tested, huge community
- Maximum flexibility for complex command structures
- Extensive documentation and plugins

**Cons:**
- More verbose — decorators and manual argument declarations
- No automatic type inference from Python signatures
- Requires more boilerplate for equivalent functionality

### 3. argparse (stdlib)

**Pros:**
- Zero dependencies
- Standard library — no version pinning concerns

**Cons:**
- No subcommand groups without significant boilerplate
- No automatic help formatting
- No rich output integration
- Extremely verbose for 24+ commands

### 4. Fire (Google)

**Pros:**
- Zero configuration — auto-generates CLI from any Python object
- Minimal code

**Cons:**
- Exposes internal API surface directly (security concern)
- No control over help formatting
- Not suitable for a multi-command CLI with groups

## Consequences

### Positive

- **Rapid development**: New subcommands require ~10 lines of code (decorator + function)
- **Consistent UX**: All commands share the same help format, argument parsing, and error handling
- **Type safety**: Python type hints serve as the single source of truth for CLI arguments
- **Easy testing**: Commands are plain Python functions, easily unit-testable
- **Rich output**: Native integration with `rich` for tables, panels, and colored output

### Negative

- **Click coupling**: Typer is a Click wrapper; deeply custom Click behavior requires dropping to Click's API
- **Subcommand nesting**: 3+ levels of nesting requires careful `typer.Typer()` instantiation

### Mitigations

- Keep subcommand nesting to 2 levels maximum (e.g., `orchestrator escalation pending`)
- Use `rich` directly for complex terminal formatting when Typer's built-in isn't sufficient
- Document the CLI structure in `docs/USER-GUIDE.md` for contributor reference

## Evidence

- The current implementation has 22+ subcommands across 10 CLI modules (`cli/*.py`)
- All commands register cleanly via `cli/main.py:app` with consistent help output
- Tests cover CLI command invocation via `typer.testing.CliRunner`

## References

- [Typer documentation](https://typer.tiangolo.com/)
- `src/ai_company/cli/main.py` — Entry point with all subcommand registration
- `docs/USER-GUIDE.md` — Complete CLI command reference
