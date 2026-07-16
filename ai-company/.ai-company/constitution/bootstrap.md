# AI Company Builder — Bootstrap Guide

> **Purpose**: How every AI coding session should begin.
> **Authority**: Derived from [00-CONSTITUTION.md](00-CONSTITUTION.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the exact procedure every OpenCode session must follow before beginning work. It ensures every session starts with full context, operates within governance rules, and leaves the repository in a consistent state.

---

## 2 Session Startup Procedure

### Step 1: Read the Constitution

```
.ai-company/constitution/00-CONSTITUTION.md
```

Read the supreme authority document. Understand the immutable rules, prohibited actions, and governance hierarchy. This is not optional.

### Step 2: Read the Mission

```
.ai-company/constitution/01-MISSION.md
```

Understand the strategic objectives and long-term vision. Every task should align with the mission.

### Step 3: Read the Project State

```
.ai-company/state/PROJECT_STATUS.md
```

Understand where the project is right now — current health, implemented components, pending work.

### Step 4: Read the Active Sprint

```
.ai-company/state/CURRENT_SPRINT.md
```

Understand what work is currently in progress and what the immediate priorities are.

### Step 5: Check for Active Changes

```
harness/changes/active/summary.md
```

If this file exists, an ECL change is in progress. Read all active change files:
- `summary.md` — change overview
- `spec.md` — requirements
- `plan.md` — implementation plan
- `tasks.md` — task breakdown
- `reviews/` — review records

**Active change files are the current task source of truth.** They override `docs/STATUS.md`.

### Step 6: Check for Pending Evolution

```
harness/evolution/pending.md
```

If this file exists, there are pending maintenance items. Note them but don't let them block current work unless the task is specifically about addressing them.

### Step 7: Read Recent Status

```
docs/STATUS.md
```

If no active change exists, read the current project status. This is the fallback context.

### Step 8: Read Architecture

```
docs/ARCHITECTURE.md
```

If the task involves code changes, read the architecture to understand the system structure.

### Step 9: Read Relevant Source Files

Based on the task, read the specific source files that will be modified. Understand the current code before making changes.

---

## 3 Context Loading Order (Summary)

```
1. Constitution          (.ai-company/constitution/00-CONSTITUTION.md)
2. Mission               (.ai-company/constitution/01-MISSION.md)
3. Project Status         (.ai-company/state/PROJECT_STATUS.md)
4. Current Sprint         (.ai-company/state/CURRENT_SPRINT.md)
5. Active Change?         (harness/changes/active/summary.md)
   ├── Yes → Read change files (summary, spec, plan, tasks, reviews)
   └── No → Continue
6. Pending Evolution?     (harness/evolution/pending.md)
   ├── Yes → Note it, continue
   └── No → Continue
7. Project Status (alt)   (docs/STATUS.md)
8. Architecture           (docs/ARCHITECTURE.md) — if code changes
9. Source files           (specific to the task)
```

---

## 4 Implementation Plan

After reading context, create an implementation plan:

### 4.1 Plan Template

```markdown
## Task: [Description]

### Context Loaded
- [x] Constitution read
- [x] Mission reviewed
- [x] Project status reviewed
- [x] Relevant source files read

### Understanding
[What I understand about the task]

### Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Verification
- [ ] Tests pass
- [ ] Lint passes
- [ ] Type check passes
- [ ] Documentation updated

### Risks
- [Any risks or concerns]
```

### 4.2 Plan Approval

For significant changes (multiple files, architectural impact, >20 minutes):

1. Present the plan to the user
2. Wait for approval
3. Then execute

For small, local fixes (single file, no architectural impact):

1. Proceed directly
2. Verify with tests

---

## 5 Execution Standards

### 5.1 During Execution

| Rule | Rationale |
|------|-----------|
| Follow coding standards | [04-CODING-STANDARDS.md](constitution/04-CODING-STANDARDS.md) |
| Follow engineering standards | [03-ENGINEERING-STANDARDS.md](constitution/03-ENGINEERING-STANDARDS.md) |
| Write tests for new code | [08-TESTING-STANDARDS.md](constitution/08-TESTING-STANDARDS.md) |
| Update documentation | [12-DOCUMENTATION-STANDARDS.md](constitution/12-DOCUMENTATION-STANDARDS.md) |
| Don't edit generated files | [06-GENERATOR-STANDARDS.md](constitution/06-GENERATOR-STANDARDS.md) |
| Don't add secrets | [13-SECURITY-STANDARDS.md](constitution/13-SECURITY-STANDARDS.md) |

### 5.2 Verification Commands

```bash
# Always run before completing work
ruff check src/                    # Lint
mypy src/                          # Type check
pytest                             # Tests
```

### 5.3 Documentation Updates

Before completing work:

- [ ] STATUS.md updated (if significant change)
- [ ] Docstrings added/updated
- [ ] ARCHITECTURE.md updated (if structural change)
- [ ] ADR recorded (if architectural decision)

---

## 6 Completion Summary

Before ending the session, provide a commit-ready summary:

```markdown
## Summary

### What was done
[Description of changes]

### Files changed
- `file1.py` — [what changed]
- `file2.py` — [what changed]

### Verification
- [x] `ruff check src/` — clean
- [x] `mypy src/` — clean
- [x] `pytest` — X/X passing

### Documentation
- [x] Docstrings updated
- [x] STATUS.md updated
- [ ] ADR needed: [topic]

### Ready for review
[Yes/No — and why]
```

---

## 7 Safety Reminders

### 7.1 Always

- Read context before making changes
- Follow the Definition of Done
- Run verification commands
- Update documentation
- Leave the repository consistent

### 7.2 Never

- Edit generated files (`.opencode/agents/*.md`)
- Commit secrets or API keys
- Skip tests to save time
- Merge without approval
- Modify the Constitution without human consent

---

## 8 Quick Reference

### 8.1 Files to Read

| Priority | File | When |
|----------|------|------|
| 1 | `constitution/00-CONSTITUTION.md` | Always |
| 2 | `constitution/01-MISSION.md` | Always |
| 3 | `state/PROJECT_STATUS.md` | Always |
| 4 | `state/CURRENT_SPRINT.md` | Always |
| 5 | `harness/changes/active/summary.md` | If exists |
| 6 | `docs/STATUS.md` | If no active change |
| 7 | `docs/ARCHITECTURE.md` | If code changes |
| 8 | Source files | Specific to task |

### 8.2 Verification Commands

```bash
ruff check src/ && mypy src/ && pytest
```

### 8.3 Documentation Updates

```bash
# Check what needs updating
# STATUS.md — significant changes
# Docstrings — all public APIs
# ARCHITECTURE.md — structural changes
# DECISIONS.md — architectural decisions
```

---

## 9 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | Supreme authority |
| [10-DEFINITION-OF-DONE.md](10-DEFINITION-OF-DONE.md) | Completion criteria |
| [docs/ECL.md](../../docs/ECL.md) | Change lifecycle |
| [AGENTS.md](../../AGENTS.md) | Agent operating guide |
| [docs/STATUS.md](../../docs/STATUS.md) | Project status |
