# AI Company Builder — Generator Standards

> **Authority Level**: Layer 7 — derived from [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the standards for all generators in AI Company Builder. Generators transform configuration into artifacts. They must be deterministic, idempotent, and safe to re-run at any time.

---

## 2 Scope

This document covers:

- Bootstrap generator
- Directory generator
- Markdown agent generator
- Config YAML generator
- Template generator
- Rules for safe regeneration
- Idempotency requirements
- File ownership and hash checking
- Versioning

---

## 3 Generator Inventory

| Generator | File | Input | Output | Regenerable |
|-----------|------|-------|--------|------------|
| BootstrapEngine | `builder/__init__.py` | CompanyRegistry | Dirs + Agents + Configs | Yes |
| AgentGenerator | `generator.py` | CompanyRegistry + Templates | `.opencode/agents/*.md` | Yes |
| ConfigGenerator | `builder/__init__.py` | CompanyRegistry | `.opencode/config/*.yaml` | Yes |
| DirectoryGenerator | `builder/__init__.py` | None | 24 directories | Yes |

---

## 4 Bootstrap Generator

### 4.1 Pipeline

```
CompanyRegistry
    ├──► Create 24 directories (memory/, knowledge/, etc.)
    ├──► Generate agent .md files (31 agents)
    └──► Generate config .yaml files (4 configs)
```

### 4.2 Execution

```python
from ai_company.builder import BootstrapEngine

engine = BootstrapEngine()
engine.run()  # Creates everything from registry
```

### 4.3 Idempotency

The bootstrap engine is fully idempotent:

- Directories: `mkdir -p` semantics (no error if exists)
- Agent files: Overwrite existing (generated output)
- Config files: Overwrite existing (generated output)

---

## 5 Markdown Agent Generator

### 5.1 Template Selection

```python
_TEMPLATE_MAP = {
    "executive": "executive.md.j2",
    "department": "department.md.j2",
    "specialist": "specialist_v2.md.j2",
    "board": "board_v2.md.j2",
    "workflow": "workflow.md.j2",
    "config": "config.md.j2",
}
# Default: "base.md.j2"
```

### 5.2 Template Rendering

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("executive.md.j2")
content = template.render(agent=agent, registry=registry)
```

### 5.3 Output Format

Each generated agent file follows the OpenCode-native format:

```markdown
---
name: Agent Name
mode: subagent
permission:
  - read:config
  - write:code
---

# Agent Name

## Identity
...
```

### 5.4 Safety Rules

| Rule | Rationale |
|------|-----------|
| Always render from templates | Consistency |
| Never hand-edit generated files | Source of truth is config |
| Always validate output before writing | Prevent corrupt files |
| Log all generation operations | Audit trail |

---

## 6 Config YAML Generator

### 6.1 Generated Configs

| File | Content | Source |
|------|---------|--------|
| `company.yaml` | Company structure summary | CompanyRegistry.company |
| `org_chart.yaml` | Organizational hierarchy | Executives + Departments |
| `workflows.yaml` | Workflow definitions | Workflows |
| `governance.yaml` | Governance rules | Decision matrix + Policies |

### 6.2 Generation Rules

| Rule | Rationale |
|------|-----------|
| Always generate from CompanyRegistry | Single source of truth |
| Preserve YAML formatting | Diffability |
| Include generation timestamp | Audit trail |
| Include source version | Traceability |

---

## 7 Template Generator

### 7.1 Template Hierarchy

```
base.md.j2 (foundation)
├── executive.md.j2 (extends base)
├── department.md.j2 (extends base)
├── specialist_v2.md.j2 (extends base)
└── board_v2.md.j2 (extends base)

workflow.md.j2 (standalone)
config.md.j2 (standalone)
```

### 7.2 Template Blocks

| Block | Purpose | Override By |
|-------|---------|-----------|
| `identity` | Agent name, role, department | executive, department, specialist, board |
| `extra_sections` | Additional content sections | All child templates |
| `metrics` | KPIs and success metrics | All child templates |
| `escalation` | Escalation rules | All child templates |

### 7.3 Template Rules

| Rule | Rationale |
|------|-----------|
| Use block inheritance | DRY, consistent output |
| Keep templates focused | One agent type per template |
| Avoid business logic in templates | Logic belongs in Python |
| Test template rendering | Prevent template errors |

---

## 8 Rules for Safe Regeneration

### 8.1 Pre-Generation Checklist

- [ ] Verify CompanyRegistry is valid
- [ ] Verify templates exist and render
- [ ] Verify output directory exists
- [ ] Back up any non-generated files in output directory

### 8.2 During Generation

- [ ] Log each file being generated
- [ ] Validate content before writing
- [ ] Write to temporary file first, then rename (atomic write)
- [ ] Handle errors gracefully (continue with other files)

### 8.3 Post-Generation

- [ ] Verify all expected files exist
- [ ] Log generation summary (files created, updated, errors)
- [ ] Optionally validate generated content (markdown lint)

---

## 9 Idempotency

### 9.1 Definition

A generator is idempotent if running it multiple times produces the same output as running it once.

### 9.2 Current State

| Generator | Idempotent? | Notes |
|-----------|------------|-------|
| DirectoryGenerator | Yes | `mkdir -p` semantics |
| AgentGenerator | Yes | Overwrites existing files |
| ConfigGenerator | Yes | Overwrites existing files |
| BootstrapEngine | Yes | Orchestrates idempotent generators |

### 9.3 Ensuring Idempotency

```python
# Good: Idempotent
def generate_agent(agent, template, output_dir):
    content = template.render(agent=agent)
    output_path = output_dir / f"{agent.id}.md"
    output_path.write_text(content)  # Overwrites if exists

# Bad: Non-idempotent
def generate_agent(agent, template, output_dir):
    output_path = output_dir / f"{agent.id}.md"
    if output_path.exists():  # Skips if exists — not idempotent for updates!
        return
    content = template.render(agent=agent)
    output_path.write_text(content)
```

---

## 10 File Ownership

### 10.1 Ownership Rules

| File Pattern | Owner | Others May Edit? |
|-------------|-------|-----------------|
| `.opencode/agents/*.md` | AgentGenerator | No (generated) |
| `.opencode/config/*.yaml` | ConfigGenerator | No (generated) |
| `config/**/*.yaml` | Human developer | Yes (source of truth) |
| `templates/**/*.md.j2` | Human developer | Yes |
| `src/**/*.py` | Human developer | Yes |
| `tests/**/*.py` | Human developer | Yes |

### 10.2 Conflict Prevention

- Generated files are in `.opencode/` (separate from source)
- Generated files are in `.gitignore` or clearly marked as generated
- Source files are in `config/`, `templates/`, `src/`

---

## 11 Hash Checking (Future)

### 11.1 Concept

Store hashes of generated files to detect unexpected modifications:

```json
{
  ".opencode/agents/ceo.md": "sha256:abc123...",
  ".opencode/agents/cto.md": "sha256:def456..."
}
```

### 11.2 Use Cases

- Detect hand-edits to generated files
- Verify regeneration produced expected output
- Audit trail for generated artifacts

### 11.3 Implementation Plan

1. Generate hash manifest after generation
2. CI checks manifest against actual files
3. Alert on mismatches

---

## 12 Versioning

### 12.1 Current

Generator output is not versioned. Regeneration overwrites.

### 12.2 Future

| Versioning Strategy | Description |
|--------------------|-------------|
| Git-based | Generated files committed to git |
| Hash-based | Content-addressed storage |
| Timestamp-based | Versioned by generation time |

---

## 13 Examples

### 13.1 Safe Regeneration Workflow

```python
from ai_company.config import load_config
from ai_company.generator import AgentGenerator
from ai_company.builder import BootstrapEngine

# 1. Load and validate config
registry = load_config()

# 2. Run bootstrap (creates dirs + generates everything)
engine = BootstrapEngine()
engine.run()

# 3. Verify output
from pathlib import Path
agent_files = list(Path(".opencode/agents").glob("*.md"))
print(f"Generated {len(agent_files)} agent files")
```

### 13.2 Anti-Pattern

```python
# Bad: Manually editing generated files
# .opencode/agents/ceo.md — DON'T DO THIS
# Adding custom content that will be lost on regeneration
```

---

## 14 Best Practices

1. **Always regenerate from config**: Never edit generated output.
2. **Test regeneration**: Verify idempotency in tests.
3. **Log generation operations**: Know what was generated and when.
4. **Validate before writing**: Don't write corrupt files.
5. **Keep templates simple**: Business logic belongs in Python.
6. **Use atomic writes**: Write to temp file, then rename.
7. **Monitor file counts**: Verify expected number of files generated.

---

## 15 Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Hand-editing generated files | Lost on regeneration | Edit config, regenerate |
| Adding business logic to templates | Templates should be simple | Move logic to Python |
| Non-idempotent generators | Can't safely re-run | Ensure idempotency |
| Skipping validation | May write corrupt files | Always validate |
| Not logging generation | No audit trail | Log all operations |

---

## 16 Future Enhancements

- Hash-based change detection
- Incremental generation (only regenerate changed agents)
- Template versioning
- Generated file diffing (show what changed)
- Parallel generation for large companies
- Generation performance benchmarks

---

## 17 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | IR-2 (Generated files not hand-edited) |
| [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md) | Code standards for generators |
| [05-PROJECT-STRUCTURE.md](05-PROJECT-STRUCTURE.md) | File locations |
| [07-PROMPT-STANDARDS.md](07-PROMPT-STANDARDS.md) | Template standards |
| [src/ai_company/generator.py](../../src/ai_company/generator.py) | Generator source |
| [src/ai_company/builder/__init__.py](../../src/ai_company/builder/__init__.py) | Bootstrap engine |
