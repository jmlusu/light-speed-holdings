# AI-Generated Imagery — Feasibility & Vendor Compliance (Ticket #379)

> **Status**: RESEARCH FINDINGS 2026-10-01. Facts only — no sourcing decision made here.
> **Ticket**: [#379 — AI-generated imagery: feasibility & vendor compliance](https://github.com/jmlusu/light-speed-holdings/issues/379)
> **Context**: Adding images to the public Vite React SPA. Feeds the AI-gen sourcing decision (blocks #384).
> **Branch**: `research/ai-gen-feasibility`

---

## 1. ADR-018 status — ComfyUI media generation

**Status: `Proposed` (2026-09-03). Never marked Accepted; never implemented as runnable infra.**

Source: `docs/adr/018-comfyui-media-generation.md:3` (`**Status:** Proposed`), dated at line 4, deciders CTO/CMO/CISO/Human CEO. The ADR is the only document in `docs/` that references its own ID — no acceptance record, no superseding ADR, no harness change log entry (grep `ADR-018|018-comfyui` across `docs/` + `harness/` returns only the ADR itself).

### What *was* implemented (policy scaffolding only)

| Piece | Location | State |
|-------|----------|-------|
| Tool allowlist YAML | `config/tool_allowlist.yaml:38-40` (`# Media generation (ComfyUI MCP - ADR-018)` → `comfyui-mcp`, `comfyui`) | Present |
| Hardcoded fallback allowlist | `src/ai_company/executor/tool_runner.py:118-120` | Present |
| Registry specialist | `company-registry.yaml:3876` (`id: media_generation_owner`) | Present |
| Generated agent card | `.opencode/agents/media-generation-owner.md` (standard subagent card, tools read/edit/grep/list/bash/task/webfetch) | Present |

### What is *absent* (the runtime)

- **`src/ai_company/media/` contains only `__init__.py` and `transcription.py`** — no `comfy_client.py`, no generation module. The ADR names `comfy_client.py` as the owner's wrapper (`docs/adr/018-comfyui-media-generation.md:27`); no file matching `*comfy*` exists anywhere in the repo except the ADR and a reminder note.
- **No ComfyUI service in any compose file.** `docker-compose.yml`, `docker-compose.staging.yml`, `docker-compose.opendesign.yml` — zero `comfy` matches.
- **No `comfyui-mcp` MCP server configured.** `.opencode/opencode.json` has no comfy/mcp entry; the package is not installed globally (`Get-Command comfyui-mcp` empty; npm global `comfyui-mcp` absent).
- **No local ComfyUI install.** `Test-Path C:\Users\jmlus\ComfyUI` → `False`.
- **ADR-mandated tests never written.** ADR links call for `test_tool_runner_allowlist_comfyui` + `test_registry_media_owner` (`docs/adr/018-comfyui-media-generation.md:71`); no `*comfy*` file under `tests/` and no test matches `comfyui`/`media_generation_owner`.
- **Historical note (primary source):** `.opencode/reminders/2026-09-07-comfyui-recap.md:6-13` records that ComfyUI + ComfyUI-Agent-Kit were cloned to `C:\Users\jmlus\ComfyUI`, tested, then **removed to save RAM** (AMD Radeon Pro iGPU, 4GB shared VRAM, 27.8GB system RAM). Re-install in API mode (`npx comfyui-mcp`, ~1.9GB, no venv) was still **"Pending"** as of 2026-09-07. Disk/RAM figures from the same note: API mode ~1.9GB; local mode +12–30GB disk, 8–16GB RAM while generating.

**Bottom line:** ADR-018 is a proposed design with its allowlist/registry halves merged and its execution half (driver, client, install, tests, compose) untouched. Nothing ComfyUI-related is runnable today.

---

## 2. Local image-generation skills — what they actually call

| Skill | Files present | What it actually invokes | Local or network? |
|-------|---------------|--------------------------|-------------------|
| `k-dense-infographics` | **SKILL.md only (12 lines, frontmatter, no body, no scripts)** | Nothing. Description promises "Nano Banana Pro AI … Gemini-powered quality review" (`.agents/skills/k-dense-infographics/SKILL.md:3`) but the skill contains no instructions, scripts, endpoints, or keys. | N/A — inert stub |
| `article-illustrations` | SKILL.md, README, LICENSE, 4 example PNGs | Instructs the agent to call a **`generate_image` tool** (`.agents/skills/article-illustrations/SKILL.md:257`). That tool is **not defined anywhere in `.opencode/` config** (grep `generate_image` → no matches) — it is an Antigravity/Gemini-CLI-native tool (README:9, README:116). | Would be network + Google account; **not invocable in this OpenCode environment** |
| `ls-brand-advertising` | SKILL.md + `scripts/brief-generator.js` | `brief-generator.js` **makes no HTTP call** — it only prints a JSON brief (`model: 'gemini-2.5-flash-image'`, brand palette, platform dimensions) for piping into a `task` delegation (`.agents/skills/ls-brand-advertising/scripts\brief-generator.js:46-58`). SKILL.md:54 routes photographic/illustration assets to the `media-generation-owner` subagent — which has no working infra (§1). | Emits a brief only; the consuming path is dead |
| `ls-visual-storytelling` | SKILL.md + `scripts/check_brand_palette.py` | Routes infographics to `k-dense-infographics` (the stub), then **post-render** palette remap + local deterministic checker `check_brand_palette.py` + `ls-artifact-qa` (`.agents/skills/ls-visual-storytelling\SKILL.md:38,63-73`) | Post-render QA is fully local; the render step is the dead stub |
| `ls-diagramming` | SKILL.md | Mermaid locally; **Kroki** (`https://kroki.io`) as fallback renderer (`.agents/skills/ls-diagramming\SKILL.md:34`) | Local first; Kroki fallback = Tier B public endpoint (see §3) |

### Working, fully-local asset tooling in-repo today

These generate on-brand raster/vector assets with **zero network calls** (imports verified: `argparse`, `os`, `pathlib`, `PIL` only — no `requests`/`urllib`/API keys):

- `static/brand/templates/generate-social-assets.py` (PIL; profile/banner/avatar assets)
- `static/brand/templates/generate-linkedin-series-visuals.py` (PIL)
- `static/brand/templates/generate-board-meeting.py`, `generate-pitch-deck.py`, `generate-post-templates.py`, `templates/social-templates/generate-social-templates.py`
- `scripts/generate-milestones-deck.py` / `.js`
- `static/brand/templates/generate-linkedin-series-visuals.py` is currently in the working tree's modified set — in active use.

These are *templated* renders (shapes/text/brand tokens), not AI image synthesis. The SPA already ships 54 raster images (`public/` + `src/`: 29 .png, 16 .jpeg, 9 .jpg) plus 17 .svg.

---

## 3. Vendor approval — §9.2 / SKILL_CURATION_POLICY vs. APPROVED-VENDORS

### The rule as written

`docs/SKILL_CURATION_POLICY.md:187-193` (§ Skill Third-Party Transmission Ban, v1.0, effective 2026-09-23), mirrored by `AGENTS.md` §9.2:

A skill may transmit local data to a third-party host — explicitly including **prompts**, docs, screenshots, code, API keys — only if **all** hold:

1. The destination vendor is listed on `docs/APPROVED-VENDORS.md`.
2. The transmission is documented in that vendor row (what is sent, to whom, auth).
3. The use is within the **90-day window** from `approved_at`, **or** CEO+CISO dual sign-off.

CISO of record = Jack Mlusu (Human CEO). Violation → runtime **stop, no retry, report to CEO** (`SKILL_CURATION_POLICY.md:204-209`). A prompt built from repo brand docs counts as local data, so **sending an art-direction prompt to an image API is Tier A**.

### The allow-list (all rows approved 2026-09-23, windows end 2026-12-22)

Source: `docs/APPROVED-VENDORS.md:16-22`. Today is **2026-10-01** → every listed window is still current (90-day rule satisfied for the *listed* vendors).

| Vendor | Image-gen relevance | Status |
|--------|--------------------|--------|
| kie.ai (`api.kie.ai`) | Only image-gen vendor ever listed — scroll-craft image gen, `KIE_AI_API_KEY` | **RETIRED with skills — "do not reinstall"** |
| Google NotebookLM (`notebooklm.google.com`) | Doc upload to NotebookLM only — a different product/host than the Gemini image API | **RETIRED with skills** |
| 0x0.st | Screenshot/image **upload** (not generation); public short-lived URLs | Active allow-list |
| cmem.ai, Telegram, wowerpoint, Greptile | Not image generation | cmem/Telegram/wowerpoint RETIRED; Greptile RETIRED |

**Not on the list at all:** Google Gemini / Google AI image API (`generativelanguage.googleapis.com` — the endpoint behind `gemini-2.5-flash-image`/"Nano Banana Pro"), Nano Banana Pro as a brand, Comfy Cloud / ComfyUI partner API nodes, OpenAI/Anthropic image endpoints, Replicate, Stability.

**Tier B carve-out** (`APPROVED-VENDORS.md:24`): public research fetches — webfetch to public docs, arXiv/OpenAlex/CrossRef/PubMed, **Kroki diagram fallback**, skill marketplaces — generally OK if disclosed, subject to stop-and-report if they unexpectedly POST local project files.

---

## 4. Verdict inputs

**(a) Working tooling in-repo today.**
No AI image-generation path functions end-to-end: ComfyUI install absent, `comfyui-mcp` absent, no MCP/compose/`comfy_client.py` config, ADR-018 tests unwritten; `k-dense-infographics` is a 12-line stub; `article-illustrations` requires a `generate_image` tool this runtime does not define; `ls-brand-advertising`'s script only emits a brief whose consumer (`media-generation-owner`) has no infra. What *does* work is local and non-AI: PIL brand-template generators under `static/brand/templates/`, the deterministic `check_brand_palette.py` gate, and Mermaid/SVG diagram rendering (Kroki fallback only).

**(b) Compliance under §9.2 as written.**
- Local-only generators (PIL templates, palette checker, local Mermaid): **compliant** — no third-party transmission.
- Any AI generation via Gemini/Nano Banana Pro/Comfy Cloud/etc.: **not compliant today** — the vendor is absent from `APPROVED-VENDORS.md`, so a prompt or brand-doc-derived brief is a Tier A transmission to a non-allow-listed host → mandatory stop-and-report. kie.ai (the historical image-gen row) is explicitly RETIRED and cannot be re-enabled without a fresh approval. Listed vendors' windows are current (ends 2026-12-22), but none of them generate images.
- Kroki fallback and public-doc webfetch: covered by the Tier B carve-out.

**(c) What would have to be true to use AI generation.**
1. **Vendor sign-off:** CEO/CISO records a row on `docs/APPROVED-VENDORS.md` for the actual image endpoint (e.g. Google AI/Gemini image API or Comfy Cloud) documenting payload class (prompts, brand tokens, possibly reference images), auth mechanism, and an `approved_at` date with `window_end` ≤90 days (`SKILL_CURATION_POLICY.md:189-193,213-215`).
2. **Keys:** the matching API key(s) provisioned locally/`.env`, `.env.example` updated, rotation handled per `AGENTS.md` §11 — never committed.
3. **Infra, if ComfyUI route:** rebuild the install (or the API-mode `npx comfyui-mcp` path ≈1.9GB per `.opencode/reminders/2026-09-07-comfyui-recap.md:13`), plus the ADR's missing pieces — `comfy_client.py`, compose/MCP config, the two named tests; and hardware headroom (prior install removed for RAM: 4GB shared iGPU, 27.8GB system).
4. **Governance:** ADR-018 moves `Proposed` → Accepted before treating its design as binding; `media_generation_owner` stays the single execution point with existing tier/HITL gating.
5. **Brand control regardless of route:** any generated render still passes the existing post-render pipeline — palette remap → `check_brand_palette.py` → `ls-artifact-qa` (`.agents/skills/ls-visual-storytelling\SKILL.md:63-73`).

---

## Sources

- `docs/adr/018-comfyui-media-generation.md` (Status: Proposed, 2026-09-03)
- `.opencode/reminders/2026-09-07-comfyui-recap.md` (install → removal, pending API-mode reinstall)
- `config/tool_allowlist.yaml:38-40`, `src/ai_company/executor/tool_runner.py:118-120`, `company-registry.yaml:3876`, `.opencode/agents/media-generation-owner.md`
- `src/ai_company/media/` directory listing; `docker-compose*.yml`; `.opencode/opencode.json`
- `.agents/skills/k-dense-infographics/SKILL.md`; `.agents/skills/article-illustrations/SKILL.md:257` + `README.md`; `.agents/skills/ls-brand-advertising/SKILL.md:54` + `scripts/brief-generator.js`; `.agents/skills/ls-visual-storytelling/SKILL.md:38,63-73`; `.agents/skills/ls-diagramming/SKILL.md:34`
- `static/brand/templates/generate-*.py` (import scan: PIL-only)
- `docs/APPROVED-VENDORS.md` (v1.0, 2026-09-23)
- `docs/SKILL_CURATION_POLICY.md:181-219` (§ Skill Third-Party Transmission Ban)
- `AGENTS.md` §9.2
