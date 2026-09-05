# ADR-018: ComfyUI Media Generation — `media_generation_owner` + `bash:comfyui-mcp` Allowlist

**Status:** Proposed
**Date:** 2026-09-03
**Deciders:** CTO, CMO, CISO, Human CEO
**Technical Domain:** Marketing / Technology (Media Generation)

## Context

Light Speed Holdings has 131 agents but no native visual/media generation capability. Brand, content, and product agents (`brand_strategist`, `content_creator`, `product_designer` in `company-registry.yaml`) depend on external stock assets or manual design for Offer A (website/branding kits), Offer B (chatbot avatars), Offer C (NGO infographics), and internal needs (dashboard visuals, SOP diagrams, `docs/assets`, pitch decks).

ComfyUI (`https://github.com/comfyanonymous/ComfyUI`) is a local-first, node-graph engine for image/video/audio/3D generation with 581 workflow templates and explicit VRAM-aware model routing. The portable **ComfyUI-Agent-Kit** (`SlavaSexton/ComfyUI-Agent-Kit`) provides a ~90-tool MCP driver (`comfyui-mcp`), per-model prompting knowledge, and a template library as source of truth. Previous session validated a local install to `C:\Users\jmlus\ComfyUI` + Agent Kit wiring to Codex/Gemini, then clean removal due to RAM constraints (AMD Radeon Pro Graphics iGPU, 4GB shared, 27.8GB system RAM). Local `torch` + model weights dominate disk/RAM (~4-6GB venv + 6-23GB per model).

We need a governed, opt-in media generation capability that:
1. Does not require every developer to run local ComfyUI (RAM/disk concern).
2. Reuses the existing `ToolRunner` allowlist + 5-tier HITL model (`src/ai_company/executor/tool_runner.py:116`, `src/ai_company/orchestrator/tier_rules.py:181`).
3. Has a single owning specialist for MCP driver lifecycle, template index, and generation pipelines — consistent with `dashboard_owner`, `registry_owner` etc.

## Decision

### 1. New specialist: `media_generation_owner`

Add to `company-registry.yaml` (type `specialist`, department `Marketing`, reports to `cmo`):

- **Id:** `media_generation_owner`
- **Owns:** ComfyUI MCP driver lifecycle, template library (`workflow_templates` + `templates/_quick_index.json`), in-graph nodes, and agent-facing generation pipelines.
- **Technical domain:** ComfyUI MCP (`comfyui-mcp`), workflow template composition, model-variant selection by VRAM/disk, GUI bridge (`user/default/workflows/`), `comfy_client.py` wrapper.
- **Consumers:** `brand_strategist`, `content_creator`, `product_designer`, `technical_documentation_lead`, `head_of_developer_relations` via `task` delegation — they request generation, owner executes.
- **Execution modes (in priority order):**
  1. **API mode (default, 0 local RAM):** Comfy Cloud MCP / partner API nodes (Nano Banana, Seedance, etc.) — no local `torch` or checkpoint download.
  2. **Local mode (opt-in):** Headless `python main.py --lowvram` on a dedicated host with `extra_model_paths.yaml` isolation. Agent selects `fp8`/`offload` variant only after checking `health_check` VRAM + free disk.

No new top-level CLI is added; consumers delegate through the existing `task` tool.

### 2. `ToolRunner` allowlist: `bash:comfyui-mcp`

- **Config:** Add `comfyui-mcp` (and alias `comfyui`) to `config/tool_allowlist.yaml:5` under `allowed_commands`.
- **Fallback:** Add `comfyui-mcp` and `comfyui` to `_DEFAULT_ALLOWED_COMMANDS` in `src/ai_company/executor/tool_runner.py:116` so the hardcoded default (used when YAML is absent) permits `npx comfyui-mcp` and bare `comfyui-mcp` invocations.
- **Rationale:** `ToolRunner._execute` (`tool_runner.py:663`) tokenizes with `shlex.split()` and checks the base command against the allowlist with `shell=True` never used. Previously `npx` was allowed but `comfyui-mcp` as a bare command was not; both forms are now explicitly permitted.

### 3. Tier classification (no code change, policy)

- Writes to `docs/assets/`, `docs/**/*.md`, `output/`, `user/default/workflows/` → **Tier 1 (Notify)** via `CONFIG_PATHS` (`tier_rules.py:90` contains `.md`, `docs/`). De-escalates the `bash` default Tier 2.
- Writes to `models/checkpoints|loras|vae` or `custom_nodes/` → **Tier 2 (Single Approver)** (code path).
- Any `bash` containing `rm -rf`, `drop table`, `curl|sh` etc. → **Tier 4 (CEO Only)** via `DANGEROUS_COMMANDS` (`tier_rules.py:108`) — unchanged.
- Production deploys (`docker push`, `kubectl apply`) remain Tier 3.

`media_generation_owner` inherits `SENIORITY_AUTO_APPROVE_TIER` (`tier_rules.py:172`): as `standard` seniority it can auto-approve Tier 1 (Notify) but Tier 2 generation requests still require HITL (single approver). No seniority bypass is added.

## Consequences

- **Positive:** Single accountable owner for media generation (mirrors `marketing_owner`, `dashboard_owner` pattern); visual deliverables become traceable, auditable (`audit/integration.py:1` already logs `tool` calls), and bound by the 5-tier matrix; API mode satisfies the RAM concern that caused removal; template library gives 581 reusable workflows without custom code; GUI bridge preserves human-in-the-loop visual review.
- **Negative / risk:** `comfyui-mcp` enlarges attack surface (npm global, node_modules ~863MB previously observed) — mitigated by allowlist pinning and tier gating; model downloads remain gated by HITL + free-disk check, but a mis-sized local request could waste bandwidth — mitigated by requiring `health_check` before download; no new sandbox beyond `project_root` (`tool_runner.py:212`).
- **Neutral:** No new dependencies in `pyproject.toml`; no schema change to `CompanyRegistry`; `AgentGenerator` will emit `media-generation-owner.md` via the existing `specialist_v2.md.j2` template (hyphen conversion per `docs/ARCHITECTURE.md:140`).

## Alternatives Considered

- **Separate microservice:** Rejected — duplicates `MessageBus` + `Executor` patterns, adds deployment overhead; MCP driver is already a thin `npx` wrapper.
- **Direct `content_creator` ownership:** Rejected — conflates content strategy with driver maintenance; dedicated owner keeps `generator.py:1` templates stable and allows rotation without reassigning brand voice.
- **No allowlist, use `webfetch` to Comfy Cloud:** Rejected — loses template-driven local path and forces vendor lock-in; allowlist permits both modes.

## Links

- `company-registry.yaml` — new entry `media_generation_owner`
- `config/tool_allowlist.yaml:5` — allowlist
- `src/ai_company/executor/tool_runner.py:116` — fallback allowlist
- `src/ai_company/orchestrator/tier_rules.py:181` — tier defaults (`bash: SINGLE_APPROVER`)
- `src/ai_company/security/command_safety.py:15` — shell metacharacter guard (`GAP-016`)
- ADR-010 (MessageBus kept), ADR-012 (RBAC), ADR-017 (suspend store — pattern for future media-state)
- ComfyUI-Agent-Kit `docs/BOOTSTRAP.md:7` — machine detection + smoke test pattern reused
- Evidence: `tests/` — add `test_tool_runner_allowlist_comfyui` + `test_registry_media_owner`
