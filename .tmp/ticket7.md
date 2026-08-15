## Question

Decide how the onboarding flow writes a `company-registry.yaml` entry and regenerates agent files.

Key decisions:
- Registry format: `company-registry.yaml` is the source of truth (AGENTS.md). The flow must add a new agent entry with id, name, role, department, type, tools, permissions, reports_to.
- Validation: run `registry/validator.py` on the draft entry before committing.
- Generation: `AgentGenerator().generate_all()` (full regen) vs incremental add? Full regen is safer; 127 agents takes <5s.
- Rollback: if generation fails, revert registry change and alert.
- Agent card output: `.opencode/agents/<id>.md` with canonical tool vocabulary (read, edit, grep, list, bash, webfetch, task).
- Deployment: agent appears in `ai-company agents list` and dashboard Agents page immediately after generation.

Integration points:
- `registry/loader.py` + `parser.py` + `resolver.py` + `validator.py`
- `generator.py` `generate_from_registry()` or `generate_all()`
- CLI `ai-company generate` in `src/ai_company/cli/main.py`

**Blocked by: Map the onboarding stack to the SOP's 8 steps (#24)**
