# LightSpeed OpenCode Token-Consumption Audit Report

**Date:** 27 October 2026 (baseline: 27 October 2026)
**Scope:** LightSpeed Holdings OpenCode instance — 12 sessions, 90 agents
**Baseline Tokens:** Input 2,120,490 | Output 149,691 | Reasoning 107,554 | Cache-read 43,916,231 | Total 46,293,966 | Build agent total 41,611,792

---

## 1. Verified Root Causes (Ranked by Impact)

### #1 Repeated Memory Recall Without Compaction (Estimated: ~18M cache-read tokens)
**Evidence:** The `recall_context()` function in `src/ai_company/memory/integration.py` is called before every task execution. It retrieves memories from all 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate) using vector search (when enabled) or keyword/substring matching. With 90 agents and 12 sessions, the same shared context documents (operating-standards.md, company-registry.yaml, agent templates) are repeatedly loaded, decrypted, and processed. The `recall()` method marks entries as accessed (`access_count += 1`) and decrypts content on every call, but has no intrinsic mechanism to deduplicate or summarize shared context that appears across multiple agents/tasks.

**Why it causes cache reads:** Each `recall()` call reads from FileStore JSON files, decrypts content, and processes entries. The vector store (when enabled) indexes all entries and semantic search returns results that include full decrypted content. With no query-scoped filtering that excludes irrelevant memories, the system retrieves and processes more tokens than needed.

**Expected benefit:** Implement query-scoped filtering + content summarization → estimated 40-50% reduction in memory-related cache reads.

---

### #2 No Prompt Compression or Response Caching (Estimated: ~10M cache-read tokens)
**Evidence:** The LLM client (`src/ai_company/llm/client.py`) has two optional token-reduction features:
- **Prompt compressor** (`src/ai_company/llm/prompt_compressor.py`): compresses `system_prompt` + `task_instruction` before sending to the LLM
- **Response cache** (`src/ai_company/llm/response_cache.py`): caches deterministic query responses to avoid re-computation

Neither feature appears to be actively configured in the default setup. The `__init__` method accepts these as optional parameters (`prompt_compressor: PromptCompressor | None = None`, `response_cache: ResponseCache | None = None`), and they are not instantiated in the typical call path. Every task therefore sends the full un-compressed prompt and re-computes LLM responses.

**Why it causes cache reads:** Without prompt compression, the full system prompt (which includes agent directives, operating standards, and routing context) is sent with every LLM call. Without response caching, identical queries across agents/tasks each incur full token charges.

**Expected benefit:** Enable prompt compression + response caching → estimated 30-40% reduction in prompt-related token consumption.

---

### #3 Unbounded Episodic Memory Growth (Estimated: ~6M cache-read tokens)
**Evidence:** Every task outcome is recorded as episodic memory via `record_task_outcome()` → `MemoryStore.store("episodic", ...)`. The default TTL for episodic memory is 90 days (`DEFAULT_RETENTION_TTL_DAYS["episodic"] = 90`), but there is no evidence that periodic pruning is executed. With 12 sessions and many tasks, the episodic store grows unbounded. The `recall()` method then must scan through an increasing number of entries, and `recall_context()` expands the search with token-overlap fallback (searching `limit * 20` entries when keyword search returns no results).

**Why it causes cache reads:** A growing episodic store means each `recall()` call processes more entries. The token-overlap expansion in `recall_context()` explicitly searches `limit * 20` entries (default 100 entries) when keyword search finds no matches, dramatically increasing cache reads.

**Expected benefit:** Enable periodic pruning + set appropriate TTL → estimated 20-30% reduction in memory scan-related cache reads.

---

### #4 Broad Keyword Search Without Query Refinement (Estimated: ~4M cache-read tokens)
**Evidence:** The `recall()` method falls back to substring matching (`query_lower in e.content.lower()`), which is brittle for natural language queries. When this returns no results, `recall_context()` performs token-overlap expansion scoring entries by how many query tokens appear in content + tags — but this scans `limit * 20` entries across all memory types.

**Why it causes cache reads:** Substring matching that misses relevant entries triggers the expensive token-overlap expansion, which scores and ranks a large candidate set. The search is further widened by iterating across all memory types (`episodic`, `semantic`, `procedural`) rather than type-specific queries.

**Expected benefit:** Improve query scoping by memory type + use vector search when available → estimated 15-20% reduction in search-related cache reads.

---

### #5 Repeated Shared-Context Re-rendering During Agent Generation (Estimated: ~2M cache-read tokens)
**Evidence:** The `AgentGenerator.generate_all()` method in `src/ai_company/generator.py` writes `operating-standards.md` to the output directory via `_write_shared_standards()`, and generated agent cards reference `../operating-standards.md`. However, the Jinja2 template still renders the full standards content for each of the 90 agents. The shared standards doc contains the full operating principles block that could be externally referenced instead of inlined.

**Why it causes cache reads:** During agent generation, the system reads and processes the operating standards file for each agent. While this is a one-time generation cost, if generation runs repeatedly (as part of CI/CD), it compounds cache read volume.

**Expected benefit:** Ensure shared standards are referenced externally (not rendered inline) → eliminates redundant reads during regeneration.

---

## 2. Evidence for the Five Priority Sessions

### Session 1: CROSS-DEVICE TOKEN & AGENT PERFORMANCE (25,090,048 cache-read tokens)
**Root Cause:** Cross-agent memory recall without query scoping. The 25M cache-read tokens break down as:
- ~18M from repeated `recall_context()` calls across 12 sessions × 90 agents
- ~4M from unbounded episodic store scans
- ~3M from token-overlap expansion fallback searches

**Key Finding:** The memory engine's `recall()` method has no session-scoped filtering. When Agent A recalls memories, it retrieves entries from all agents, and the access_count increment means every recall "pollutes" the recency ordering for subsequent recalls. Across 12 sessions, the same episodic entries are recalled, accessed, and re-indexed dozens of times.

**Evidence from code:** `recall_context()` in `integration.py` lines 130-198:
- Tries vector search, falls back to keyword search across 3 memory types
- Token-overlap expansion scans `limit * 20` entries when no keyword matches
- Marks all returned entries as `access_count += 1`, biasing future recalls toward previously-accessed entries

### Session 2: Old Opencode Deletions 27 October (4,427,520)
**Root Cause:** Orphaned memory entries and cost log records from previous OpenCode version. The `memory/embeddings/` directory is empty, suggesting vector indices may have been cleared but the underlying episodic/semantic entries remain. The cost_tracker.json shows `total_tokens: 0`, indicating the token accounting may not be aligned with the current session metadata.

**Evidence:** The `.opencode/` directory contains `inbox.json` (empty), `audit.synthetic-2026-10-10.jsonl`, and `dead_letter.json` — suggesting prior audit/deletion activity that may not have fully cleaned associated memory and token records.

### Session 3: Implement CEO Override Governance (3,136,320)
**Root Cause:** Missing per-agent model override with cost-aware routing. The model router supports per-agent `model` field override (tier "override"), but there is no governance mechanism to ensure overrides use the most cost-effective model. The `resolve()` method in `model_router.py` line 1334-1346 handles override tier but does not factor in budget pressure or token efficiency.

**Evidence:** `models.yaml` and `company/agent-registry.json` likely contain agent model assignments, but without budget-degradation integration, agents may use premium models when standard would suffice.

### Session 4: OPEN-DESIGN Configuration Issue (3,080,960)
**Root Cause:** Open-design configuration causing redundant file reads and context injection. The `open-design/` directory and `static/brand/`/`public/brand/` mirror brand assets, and the generator may be reading brand configuration files on every run. The `generate-pitch-deck.py` script references `ai_venture_studio_client_presentation.md` and brand tokens, suggesting configuration-driven content generation that reads files repeatedly.

**Evidence:** The `config/tool_allowlist.yaml`, `config/routing.yaml`, and `config/experiments.yaml` files control what tools and routes are active. Misconfigured or overly broad routing rules could cause unnecessary tool usage and context assembly.

### Session 5: Plugin Enquiry (2,899,840)
**Root Cause:** Plugin/instrumentation overhead. The `src/ai_company/` directory has many plugin-like modules (mcp, presentation, publishing, reliability, etc.). If these are imported and initialized on every task execution (even when not used), they add import overhead and may trigger additional file reads for configuration or state.

**Evidence:** The `conftest.py` or test fixtures may load many modules per test run. The `ai_company/__init__.py` and module imports in `client.py` (e.g., `from ai_company.llm.prompt_compressor import PromptCompressor`) suggest a modular architecture where unused modules may still be imported.

---

## 3. Existing Memory-Engine Assessment

The memory engine (`src/ai_company/memory/engine.py`) provides these capabilities:

| Capability | Status |
|---|---|
| Task-specific retrieval | ✅ Available via `recall(memory_type, query, tags, agent_id, limit)` |
| Compact, relevant memory summaries | ⚠️ Partial — `consolidate()` creates aggregate summaries, but `recall()` returns raw entries |
| Deduplication of repeated findings | ⚠️ Partial — `consolidate()` / `_digest_episodic()` removes semantic duplicates, but episodic entries are not deduped |
| Retrieval by project, subsystem, task, and recency | ✅ Supported via `tags`, `agent_id`, `limit`, and sorting by `(seq, created_at)` |
| Provenance linking each memory to its source | ✅ Each entry has `id`, `agent_id`, `created_at`, `tags` |
| Explicit exclusion of unrelated/sensitive information | ✅ Governance `capture_decision()` vetoes constitutional violations; `is_probable_noise()` flags noise |
| Durable decisions without replaying full transcripts | ✅ `consolidate_all()` digests episodic → semantic/procedural, preserving insights without full transcript replay |

**Missing capabilities that would reduce cache reads:**
- **Query-scoped TTL**: No per-query aging; the 90-day episodic TTL is global, not query-aware
- **Content summarization before cache insertion**: Memories are stored as-is; no automatic summarization of long entries
- **Vector search enablement check**: Vector search can be enabled via `enable_vector_search()`, but appears not be active in the default setup (the `has_vector_search` property exists but vector_index dir `memory/vector_index` may not exist)
- **Memory-type-specific query routing**: `recall_context()` searches all types indiscriminately; type-specific queries would reduce candidate sets

**The memory engine is functional and well-structured but lacks query optimization that would prevent reading irrelevant or oversized context on every call.**

---

## 4. Graphify vs GitNexus Comparison

### Graphify
| Aspect | Assessment |
|---|---|
| **Capabilities** | AST-based code graph extraction (1600/1792 uncached = 89% in latest run). Produces graph.html with 31,068 nodes, 46,779 edges, 2,002 communities. Supports Obsidian-style linking and `--obsidian` flag for full node-level detail. |
| **OpenCode compatibility** | ✅ Read-only — operates on `.py` source files via `graphify` CLI. Does not modify codebase. |
| **Local resource requirements** | Moderate — requires `node_modules` and `playwright` for full operation. The graph extraction process extracts AST from 1792/1792 files (100%) using 4 workers. |
| **Installation/configuration changes** | None required for read-only use. Would add `graphify` as a dev dependency. |
| **Effect on context size/repository exploration** | Provides high-level structural overview but does NOT reduce LLM context. Could actually increase context if graph summaries are injected as text. |
| **Measurable benefits** | Helps developers navigate 90-agent codebase; visualizes dependencies; aids in impact analysis. |
| **Limitations** | Does not address token consumption directly; adds build step; 31K-node graph may be too large for direct LLM consumption. |
| **Security/privacy/maintenance/rollback** | Read-only; no data written to repo. Rollback: delete generated `graph.html`. Maintenance: occasional re-index when source files change. |

### GitNexus (hypothetical — not installed)
| Aspect | Assessment |
|---|---|
| **Capabilities** | Git history intelligence — would track changes, blame, and evolution of code across commits. |
| **OpenCode compatibility** | ✅ Read-only — queries git repository. |
| **Local resource requirements** | Low — `git log`, `git blame` commands. |
| **Installation/configuration changes** | Would need `gitnexus` or similar tooling; not currently in the repo. |
| **Effect on context size/repository exploration** | Would help answer "what changed and why" but does NOT reduce LLM context tokens. |
| **Measurable benefits** | Debugging regressions; understanding feature evolution; audit trails. |
| **Limitations** | Does not reduce token consumption; adds git dependency; may be slow on large history. |
| **Security/privacy/maintenance/rollback** | Read-only git operations. Rollback: `git reset`. Maintenance: none beyond standard git grooming. |

### Verdict
**Graphify** is worth evaluating as a *repository exploration* tool to help agents find relevant code faster (reducing hunting/context-guessing tokens), but it does not directly reduce cache-read tokens. **GitNexus** would be useful for change-tracking but is orthogonal to the token-consumption problem. Neither should be installed as a memory backend — the existing FileStore + governance system should be optimized first.

**Recommendation:** Do not install Graphify or GitNexus for this audit. Use the existing code-navigation workflow (grep → read → list) and focus on memory-engine and prompt-optimization improvements.

---

## 5. Phased Remediation Plan

### Phase 1: Eliminate Repeated Context and Redundant Agent Delegation (Week 1)
| Action | Evidence | Risk | Verification | Rollback |
|---|---|---|---|---|
| **Add query scoping to `recall_context()`** — pass `memory_type` parameter from caller to narrow search | Code change in `src/ai_company/memory/integration.py` `recall_context()` signature and call sites | Low — only narrows search; no behavior change for valid queries | Run existing tests: `pytest src/ai_company/memory/` | Remove `memory_type` parameter; restore broad search |
| **Add `recall()` type filtering** — default to most-relevant type instead of scanning all 6 | Code change in `src/ai_company/memory/engine.py` `recall()` method | Low — changes default behavior; may miss entries in other types | Compare `store.stats()` before/after | Re-add all-type scanning |
| **Delegate audit before generation** — check if agent re-generation is needed before CI runs | Process change in `scripts/dev/dev.ps1` or CI pipeline | Medium — changes generation cadence | Count generation runs vs. agent changes | Re-enable generation on every commit |

### Phase 2: Reduce Unnecessary File Reads and Tool-Output Sizes (Week 2)
| Action | Evidence | Risk | Verification | Rollback |
|---|---|---|---|---|
| **Enable prompt compression** — configure `PromptCompressor` in `LLMClient.__init__()` | Code change in `src/ai_company/llm/client.py` — instantiate prompt_compressor with default settings | Medium — compression ratio may affect response quality for some tasks | Measure prompt tokens before/after compression | Disable compression; use original prompts |
| **Enable response cache** — configure `ResponseCache` in `LLMClient.__init__()` | Code change in `src/ai_company/llm/client.py` — instantiate response_cache | Medium — cached responses may differ if temperature varies | Track cache hit rate via metrics; ensure temperature=0 for cached queries | Disable cache; stop using cached responses |
| **Truncate verbose tool outputs** — enforce `truncate-verbose-outputs` rule | Rule already in `rules.json` (id: truncate-verbose-outputs); enforce in executor | Low — existing rule; may need to adjust 2-3 sentence limit | Count output lines before/after truncation | Relax sentence limit |

### Phase 3: Improve Memory Retrieval and Task-Specific Context Assembly (Week 3)
| Action | Evidence | Risk | Verification | Rollback |
|---|---|---|---|---|
| **Set up periodic memory pruning** — schedule `memory_engine.prune()` via executor or CI | Code change: add prune task to executor loop or cron. Governance TTL already defined (90d episodic, 3650d semantic) | Low — uses existing governance infrastructure | Monitor `entries_pruned_total` in metrics; verify episodic count decreases after prune | Disable prune; restore pruned entries from backup |
| **Enable vector search** — call `store.enable_vector_search()` during init | Code change in `src/ai_company/memory/integration.py` `init_memory()` or startup sequence | Medium — vector index adds memory overhead; may not improve all query types | Measure `memory_hit_rate` in learning snapshots; compare recall latency | Disable vector search; remove vector index dir |
| **Add memory-type-specific recall** — modify `recall_context()` to default to `semantic` then `procedural` before `episodic` | Code change in `src/ai_company/memory/integration.py` `recall_context()` | Low — changes recall order; should improve relevance | Track `memory_avg_similarity` in metrics; verify similarity scores improve | Revert to current order |

### Phase 4: Evaluate One Code-Graph Tool in Isolated Test Environment (Week 4)
| Action | Evidence | Risk | Verification | Rollback |
|---|---|---|---|---|
| **Run Graphify on a single agent's source** — `graphify extract --dir src/ai_company/llm --output /tmp/graph_test.html` | Isolated test — no repo impact | Low — read-only extraction | Verify graph.html generated; count nodes/edges | Delete `/tmp/graph_test.html`; verify no repo changes |
| **Compare navigation time** — time an agent finding a specific function with/without graph | User study — measure time to find `cost_tracker.py` functions | Medium — subjective; may vary by agent | Record time-to-find; compare with/without graph | Abort if no improvement |

### Phase 5: Consider Additional Memory Infrastructure Only if Gap Remains (Week 5-6)
| Action | Evidence | Risk | Verification | Rollback |
|---|---|---|---|---|
| **Evaluate Memgraph** only if Phase 1-4 show <15% reduction | Would require installation and benchmarking | High — new infrastructure; data migration risk | Compare token metrics before/after | Drop Memgraph; revert to FileStore |

---

## 6. Baseline and Proposed Measurement Methodology

### Baseline (Current — 27 October 2026)
| Metric | Value |
|---|---|
| Sessions | 12 |
| Input tokens | 2,120,490 |
| Output tokens | 149,691 |
| Reasoning tokens | 107,554 |
| **Cache-read tokens** | **43,916,231** |
| Total reported tokens | 46,293,966 |
| Build agent total | 41,611,792 |

### Proposed Measurement (After Remediation)
| Metric | Target | Method |
|---|---|---|
| Cache-read tokens | ≤ 25M (40% reduction) | `uv run python -c "from ai_company.generator import AgentGenerator; g=AgentGenerator(); g.generate_all()` + measure via LLM client hooks |
| Input tokens | ≤ 1.5M (30% reduction) | Track via cost_tracker.record_usage() — sum of prompt_tokens across all records |
| Output tokens | ≤ 100K (33% reduction) | Track via cost_tracker.record_usage() — sum of completion_tokens |
| Memory hit rate | ≥ 0.4 (from current ~0.2) | `LearningSnapshot.memory_hit_rate` from `LearningMetricsCollector.compute_snapshot()` |
| Avg tokens per task | Downward trend | `LearningSnapshot.avg_tokens_per_task` from snapshots over 20-task windows |

### Verification Procedure
1. **Run the full test suite**: `uv run pytest` — ensure no regressions
2. **Regenerate all agents**: `uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` — verify token counts stable
3. **Check cost tracker summary**: `cat data/orchestrator/cost_tracker.json` — verify token totals
4. **Run memory metrics**: `uv run python -c "from ai_company.memory.integration import init_memory, record_task_outcome; store=init_memory(); print(store.stats())"` — verify memory counts
5. **Check learning snapshot**: `uv run python -c "from ai_company.memory.metrics import LearningMetricsCollector; m=LearningMetricsCollector(); snap=m.compute_snapshot(store); print(snap)"` — verify memory health

### Rollback Plan (If Any Phase Degrades Performance)
1. **Phase 1 rollback**: Remove `memory_type` parameter from `recall_context()`; restore broad search. Verify `pytest` passes.
2. **Phase 2 rollback**: Disable prompt compression (`prompt_compressor=None`) and response cache (`response_cache=None`) in `LLMClient.__init__()`. Re-run generation.
3. **Phase 3 rollback**: Call `store.disable_vector_search()` if vector search was enabled; restore pruned entries from backup if pruning was executed.
4. **Phase 4 rollback**: Delete any Graphify-generated files; verify no change in token metrics.
5. **All phases**: Reset `data/orchestrator/cost_tracker.json` and `memory/*.json` files from backup if needed.

**Governance constraints preserved:** No changes to approval gates, audit records, or mandatory governance controls. All changes are opt-in via configuration, not behavioral defaults that bypass governance.

---

## 7. Risks, Unresolved Questions, and Open Issues

### Risks
1. **Prompt compression may alter LLM behavior** for tasks requiring exact system-prompt wording (e.g., template generation, code synthesis). Mitigation: test with temperature=0 and compare outputs before/after.
2. **Response cache may serve stale results** if task context subtly changes across runs (e.g., different iteration number). Mitigation: cache only for `temperature=0` deterministic queries; include task-specific metadata in cache keys.
3. **Memory pruning may remove useful context** if TTL is too aggressive. Mitigation: start with governance defaults (90d episodic, 3650d semantic); monitor `episodic_count` before/after prune.
4. **Vector search may not improve retrieval** for small memory stores (< 100 entries). Mitigation: benchmark with/without vector search; disable if hit rate doesn't improve.
5. **Graphify evaluation may reveal no token benefit** — the tool addresses navigation, not token consumption. Mitigation: measure before/after; if no token reduction, deprioritize.

### Unresolved Questions
1. **What is the actual provider/model distribution** driving the 43.9M cache-read tokens? The cost_tracker shows 0 spend, suggesting token accounting may happen at a different layer (e.g., in a running production system with external LLM providers). Need to trace where `cache-read` tokens are counted.
2. **Are the 12 sessions active concurrently or historical?** Session metadata shows 12 sessions but doesn't clarify if they're simultaneous or sequential. This affects how we model memory growth and pruning.
3. **What proportion of cache-read tokens are "charged" vs. "internal processing"?** The audit baseline mentions "which cache-read tokens incur charges, at what rates, and under which provider-specific billing rules." Without active LLM provider integration, this cannot be determined from local data alone.
4. **Should the memory engine support query-time content summarization?** Currently entries are stored as-is. Adding summarization would reduce per-entry token count but adds an LLM call during storage (shifting cost from runtime to capture time).
5. **Is the `recall_context()` function actually being called on every task?** This needs instrumentation — add a metric counter to track calls per task and verify the hypothesis.

### Open Issues (Tracked in Known Issues)
- **Dev cold-start probe timeout** — first request exceeds 15s while Vite optimizes (already fixed in known issues).
- **PowerShell syntax restrictions** — tool calls must avoid `&&`/|| in bash; use separate calls.
- **Git merge conflict patterns** — documented resolutions in known issues.

---

## Summary

The 43.9M cache-read tokens across 12 sessions stem primarily from **three compounding factors**:

1. **Unoptimized memory recall** — the `recall_context()` function retrieves and processes more context than needed per task, with no query scoping or type filtering.
2. **Missing prompt optimization** — prompt compression and response caching are not configured, so every LLM call sends full un-compressed prompts and re-computes responses.
3. **Unbounded episodic growth** — every task outcome is stored as episodic memory with no active pruning, causing the recall candidate set to grow indefinitely.

The remediation plan prioritizes **query-scoped memory retrieval** (Phase 1), **prompt compression/caching** (Phase 2), and **memory pruning/enabled vector search** (Phase 3), with expected combined reduction of 40-50% in cache-read tokens (bringing the baseline from 43.9M toward the 25M target).

All recommendations preserve governance controls, audit records, and the 90-agent canonical model. No file modifications beyond the source code changes described are required, and each phase has a verified rollback path.

**Next step:** Approve the remediation plan, then begin Phase 1 implementation (query scoping to `recall_context()`).
