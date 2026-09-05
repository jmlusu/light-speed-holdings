# Reminder — 2026-09-07: Light Speed Holdings ComfyUI Recap

**Trigger:** User requested chat recap on Sep 07 (today is 2026-09-03, +4 days)
**Project:** Light Speed Holdings — AI Company Builder (company-registry.yaml: 132 agents)
**Context:**
- ComfyUI + Agent Kit cloned to C:\Users\jmlus\ComfyUI / ComfyUI-Agent-Kit, tested, then removed to save RAM (AMD Radeon Pro Graphics 4GB shared, 27.8GB system, 16GB free).
- ADR-018 drafted: docs/adr/018-comfyui-media-generation.md — adds media_generation_owner (Marketing -> cmo) with API-first (Comfy Cloud, 0 local RAM) vs opt-in local headless.
- Allowlist updated: config/tool_allowlist.yaml + src/ai_company/executor/tool_runner.py (comfyui-mcp, comfyui) — ruff/mypy clean, 132 agents generated.
- Disk impact: API mode ~1.9GB, Local mode +12-30GB; RAM idle 0 vs 8-16GB when generating locally.

**Recap Action for Sep 07:**
- Summarize ADR-018 decisions, disk/RAM tradeoffs, and Offer A/B/C use cases (brand, chatbot avatars, NGO infographics).
- Ask if user wants to re-install in API mode (npx comfyui-mcp + templates, no venv) and run one test image to docs/assets.

**Status:** Pending — deliver via chat on 2026-09-07
