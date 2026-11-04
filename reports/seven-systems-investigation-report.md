# Comprehensive Seven Systems Investigation Report

**Date**: 2026-11-03
**Project**: `C:\Users\jmlus\light-speed-holdings\.worktrees\silent-knight`
**Evidence Source**: Comprehensive source code analysis across all seven core LightSpeed systems

---

## Executive Summary

This report presents a comprehensive investigation of seven core LightSpeed systems gathered from actual source code analysis. The investigation covered Memory Engine, Decision Engine, Workflow Engine, Model Router, Executor, Graph Engine, and Cache Mechanisms. All systems were traced from their source code, with implementation details, lifecycle flows, and cross-system interactions documented.

**Key Finding**: There is no single application-level cache across all systems — each system maintains independent caching mechanisms with different key strategies, TTLs, and storage backends.

---

## 1. Memory Engine

### Implementation Status
- **6 Memory Types**: episodic, semantic, procedural, relational, temporal, aggregate
- **FileStore-backed JSON persistence** for all memory types
- **Lifecycle**: recall → search → prune → consolidate

### Source Files Analyzed
- `src/ai_company/memory/` — core memory engine implementation
- Memory type definitions and persistence layer

### Key Characteristics
- Memories are persisted as JSON files via FileStore
- Each memory type has distinct semantics and access patterns
- Recall uses semantic similarity + exact key matching
- Search supports both vector and text-based queries
- Pruning removes stale/expired memories based on TTL
- Consolidation merges related memories across types

---

## 2. Decision Engine

### Implementation Status
- **5-Tier Approval Matrix**: AUTO_APPROVE=0, NOTIFY=1, SINGLE_APPROVER=2, TWO_PERSON=3, CEO_ONLY=4
- **Classification criteria**: tool type, path sensitivity, command sensitivity, risk context, seniority
- **HITL (Human-in-the-Loop) approval gate** integration

### Source Files Analyzed
- `src/ai_company/decision/` — decision engine core
- Approval gate implementation

### Key Characteristics
| Tier | Value | Description |
|------|-------|-------------|
| AUTO_APPROVE | 0 | Full automation, no human intervention |
| NOTIFY | 1 | Notify only, proceed automatically |
| SINGLE_APPROVER | 2 | One designated approver required |
| TWO_PERSON | 3 | Two designated approvers required |
| CEO_ONLY | 4 | CEO approval required exclusively |

### Classification Logic
- Tool type determines baseline tier
- Path sensitivity may upgrade tier
- Command sensitivity may upgrade tier
- Risk context may upgrade tier
- Seniority may downgrade tier

---

## 3. Workflow Engine

### Implementation Status
- **9 Workflow Definitions**: referenced from `company-registry.yaml` via YAML anchors/aliases
- **WorkflowInstance persistence** to `workflows/instances/{id}.json` via FileStore
- **Methods**: advance, complete_step, cancel, get_status

### Source Files Analyzed
- `src/ai_company/workflow/` — workflow engine core
- Registry YAML parsing and instance management

### Key Characteristics
- 9 distinct workflow definitions registered in `company-registry.yaml`
- Each workflow uses YAML anchors/aliases for reusability
- Instances persisted as JSON files in `workflows/instances/`
- State transitions: advance → complete_step → get_status
- Cancel capability for terminating workflows
- Workflow definitions are static (registered at startup)

---

## 4. Model Router

### Implementation Status
- **5-Layer Routing Priority**: per-agent override → explicit context → domain detection → task-type routing → agent-type/priority rules → standard fallback
- **Reads `company/models.yaml`** for provider/model mappings
- **Does NOT execute LLMs itself** — resolves provider/model for LLMClient which calls provider.chat()

### Source Files Analyzed
- `src/ai_company/model_router/` — model routing logic
- `company/models.yaml` — provider/model registry

### Key Characteristics
```
Routing Priority (highest to lowest):
1. Per-agent override (agent-specific model preference)
2. Explicit context (user-provided model hint)
3. Domain detection (infer domain from task description)
4. Task-type routing (map task type to model)
5. Agent-type/priority rules (agent class → model mapping)
6. Standard fallback (default model from config)
```

### Important Note
- The model router **resolves** provider/model configuration
- Actual LLM execution happens via `LLMClient.provider.chat()`
- Router reads `company/models.yaml` for the mapping
- Supports both dynamic (OpCode Zen API) and static fallbacks

---

## 5. Executor

### Implementation Status
- **ToolRunner** executes 7 canonical tools directly via subprocess with strict sandboxing
- **Does NOT delegate to OpenCode** — runs tools independently
- **Tier-based authorization** via `check_tier_rules()` before execution
- **HITL approval gate integration**
- **Command allowlist** for safety
- **Output sanitization** (PII/content safety)
- **SLA timeout**: 120 seconds
- **Dead-letter logging** for failed executions

### Source Files Analyzed
- `src/ai_company/executor/` — tool execution engine
- Tier rules and authorization logic

### Key Characteristics
- **7 Canonical Tools**: `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`
- Each tool execution goes through `check_tier_rules()` validation
- SLA timeout of 120s; executions exceeding timeout are terminated
- Output passes through PII/content sanitization filters
- Failed executions logged to dead-letter queue
- HITL approval gate can intercept and block dangerous operations

---

## 6. Graph Engine

### Implementation Status
- **4 Graph Types**: org_chart, decision_graph, workflow_graph, knowledge_graph
- **Built statically from registry data** (CompanyRegistry)
- **NOT updated live during task execution**
- **`get_graph(name)`** builds/caches graphs
- **`find_path`** uses BFS (breadth-first search)

### Source Files Analyzed
- `src/ai_company/graph/` — graph engine implementation
- Company registry integration

### Key Characteristics
| Graph Type | Source Data | Purpose |
|-----------|-------------|---------|
| org_chart | CompanyRegistry | Organization hierarchy |
| decision_graph | CompanyRegistry | Decision flow relationships |
| workflow_graph | CompanyRegistry | Workflow step dependencies |
| knowledge_graph | CompanyRegistry | Knowledge/entity relationships |

### Important Note
- Graphs are **built once** from registry data at startup
- NOT dynamically updated during task execution
- Cached via `get_graph(name)` for repeated access
- Primary purpose: repository indexing and post-commit analysis
- Not intended for live orchestration or real-time graph traversal

---

## 7. Cache Mechanisms

### Implementation Status
Multiple independent cache systems, each with different key strategies and TTLs:

### A. LLM Response File-Based Cache
- **Path**: `.cache/llm/`
- **Key**: `(system_prompt, user_prompt, model, temperature)`
- **TTL**: Configurable, per-configuration
- **Purpose**: Avoid re-computing identical LLM responses

### B. OAuth2 In-Memory TTL-Bounded Token Cache
- **Storage**: In-memory Python dict
- **TTL**: Bounded time-to-live per token
- **Purpose**: Manage OAuth2 access tokens for API authentication
- **Behavior**: Tokens expire after TTL, refreshed automatically when possible

### C. Model Router Free-Model Catalog Cache
- **TTL**: 1-hour from OpCode Zen API or static fallback
- **Purpose**: Cache available free model list
- **Behavior**: Refreshes hourly from OpCode Zen API; falls back to static list if API unavailable

### D. Memory Engine Auto-Vector Indexing
- **Trigger**: When VectorStore is configured
- **Purpose**: Enable vector-based similarity search over memories
- **Behavior**: Auto-indexes memories when VectorStore becomes available

### E. YAML Config Caching
- **Function**: `load_yaml_cached` in generator
- **Purpose**: Cache parsed YAML configs (company-registry.yaml, company/models.yaml)
- **Behavior**: Loads once, caches in memory, subsequent reads use cached version

### Cross-System Cache Summary
```
No single application-level cache exists across all systems.
Each system maintains independent caching:

| Cache Type | Key Strategy | TTL | Storage |
|-----------|-------------|-----|---------|
| LLM Response | (system_prompt, user_prompt, model, temp) | Config | .cache/llm/ |
| OAuth2 Token | Token identifier | Bounded | In-memory |
| Model Catalog | N/A (API/static) | 1 hour | In-memory |
| Memory Vectors | Memory IDs | Config | VectorStore |
| YAML Config | Config file path | Session | In-memory |
```

---

## Cross-System Lifecycle Trace

### CEO Instruction → Executor Tool Execution Flow

```
CEO Instruction
    ↓
Task dispatched to Message Bus (.opencode/inbox.json)
    ↓
Decision Engine: 5-tier approval matrix evaluation
    ↓
Executor: ToolRunner with sandboxing & tier authorization
    ↓
Command Allowlist check
    ↓
HITL Approval Gate (if tier requires)
    ↓
Tool execution (7 canonical tools via subprocess)
    ↓
Output sanitization (PII/content safety)
    ↓
Dead-letter logging (on failure)
    ↓
SLA timeout (120s) enforcement
    ↓
Result returned via Message Bus
```

### Graph Engine Post-Commit
```
Post-commit hook
    ↓
Graph Engine: build/cached graph from registry
    ↓
find_path BFS for repository indexing
    ↓
Indexing artifacts stored (not live during task execution)
```

### Memory Lifecycle
```
Memory creation
    ↓
Auto-vector indexing (if VectorStore configured)
    ↓
recall → search → prune → consolidate lifecycle
    ↓
FileStore JSON persistence
    ↓
TTL-based expiration during prune
```

---

## Verification Commands

### Generator / Template
```bash
python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
```

### CLI Commands
```bash
ai-company --help
ai-company <command> --help
```

### Models / Orchestrator
```bash
pytest
```

### Any Source Change
```bash
ruff check src/
mypy src/
pytest
```
(These are separate commands, not chained, due to PowerShell 5.1 limitations)

### Graph Engine
```bash
# Build/get graph
python -c "from ai_company.graph import get_graph; g = get_graph('org_chart')"
```

### Executor
```bash
# Verify tool execution
ai-company execute --tool read --path "src/ai_company/models/models.py"
```

---

## Key Conclusions

1. **Seven Independent Systems**: Each of the seven systems has its own implementation, caching, and lifecycle. There is no unified application-level cache.

2. **Sandboxed Execution**: The Executor provides strict sandboxing with tier-based authorization, command allowlists, and output sanitization — all 7 canonical tools execute directly via subprocess without OpenCode delegation.

3. **Static Graph Data**: The Graph Engine builds graphs statically from registry data and does not update them live during task execution. Primary use is repository indexing and post-commit analysis.

4. **Model Router as Configurator**: The Model Router resolves provider/model mappings but does not execute LLMs itself. It reads `company/models.yaml` and routes to the appropriate LLMClient.

5. **Approval Matrix Drives Safety**: The Decision Engine's 5-tier approval matrix is the primary safety mechanism, governing which operations proceed automatically and which require human intervention.

6. **FileStore Persistence**: Memories and workflow instances are persisted via FileStore as JSON, providing durable storage across sessions.

7. **No Cross-System Cache**: Each system's caching is independent — there is no shared cache that spans Memory, Decision, Workflow, Model Router, Executor, and Graph engines.

---
*Report generated from comprehensive source code analysis across all seven LightSpeed core systems.*
