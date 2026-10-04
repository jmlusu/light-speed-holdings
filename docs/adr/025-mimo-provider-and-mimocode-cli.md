# ADR-025: MiMo (Xiaomi) as Tenth LLM Provider and Second Coding Agent CLI

**Status:** Accepted
**Date:** 2026-09-25
**Deciders:** Human CEO (Jack Mlusu, CISO of record), CTO, LLM Platform Owner, CISO, CLO
**Technical Domain:** LLM Integration / Developer Tooling / Vendor Governance

## Context

The fleet runs on a multi-provider LLM strategy (ADR-004) where every provider is data in
`company/models.yaml` and every new provider historically cost a new adapter module, a
registry card, a doc-drift update and a governance review. Xiaomi's MiMo models and the
MiMo Code CLI were proposed as an addition with two requirements from the CEO:

1. **No behavioural regression.** Adding MiMo must not change which model an agent gets
   today.
2. **Two tracks, one change.** MiMo belongs both in the routing catalog (track A) and as a
   second coding agent CLI alongside OpenCode (track B), reviewed as one governed change.

Two facts made this cheaper than a typical provider addition:

- The client already falls through to `OpenAICompatibleProvider` for any provider id that is
  not `ollama`/`llamacpp` (`src/ai_company/llm/client.py:153-164`), so **no new provider
  module is required** — provider identity is configuration.
- The repo carries a doc-drift gate (`docs/source-of-truth.yaml` `provider_count`) whose
  extractor counts provider entries in `company/models.yaml` and is gated on `README.md`
  and `docs/ux/DEVELOPER-EXPERIENCE.md`. A provider count change is therefore a single
  atomic commit obligation, not a scattershot doc edit.

MiMo Code 0.1.15 is installed on the dev machine (`~\.mimocode\bin\mimo.exe`). Its own
config/skill/agent discovery had to be mapped from the installed binary before any file was
added to this repository.

## Decision

### A. Provider: configuration-only, appended at the end of every chain

- New provider entry `mimo` with `backend: openai_compatible`,
  `api_base: https://api.xiaomimimo.com/v1`, `default_model: mimo-v2.5`.
- Credential follows the existing `{ID}_API_KEY` convention → `MIMO_API_KEY`, read by the
  shared OpenAI-compatible path. **No new provider module, no changes to
  `providers/*`, `model_router.py`, `circuit_breaker.py` or `token_bucket.py`.**
- `mimo/mimo-v2.5` appended **last** to the `standard` tier; `mimo/mimo-v2.5-pro`
  appended **last** to `premium`; `fast` untouched. Because the router walks a tier's
  fallback chain in order, primary routing behaviour is byte-identical to before until
  every earlier provider in the chain is unreachable.
- `MODEL_COSTS` in `src/ai_company/llm/cost_tracker.py` gains `mimo-v2.5`
  (0.14 / 0.28) and `mimo-v2.5-pro` (0.435 / 0.87) per 1M tokens, cache-miss input.
  Cache-hit pricing ($0.0036) is deliberately **not** modelled — the tracker has no
  cache-hit input class today.
- Doc-drift cluster bumped to 10 in the same commit:
  `docs/source-of-truth.yaml` (`provider_count: 10`), `README.md`,
  `docs/ux/DEVELOPER-EXPERIENCE.md`, plus non-gated narrative updates to
  `docs/client-facing/USE-CASE-CATALOG.md` and `docs/MODEL-ROUTING-POLICY.md`.

### B. Key plumbing

`MIMO_API_KEY` is threaded through every surface that already carries `KIMI_API_KEY` /
`ANTHROPIC_API_KEY`: `.env.example`, `.env.staging.example`, `docker-compose.yml`,
`docker-compose.staging.yml`, `.github/workflows/autonomous.yml`,
`.github/workflows/repo-audit.yml`, and `AGENTS.md` §11. `MIMO_API_KEY=` is empty in the
examples, matching the existing `DEEPSEEK_API_KEY=`/`KIMI_API_KEY=` precedent — those keys
are listed but absent from every tier, so a dev who does not opt in never routes to them.

### C. Governance

`docs/APPROVED-VENDORS.md` gains an active allow-list row for **Xiaomi MiMo**
(`api.xiaomimimo.com`, Bearer `MIMO_API_KEY`, approved 2026-09-25, window ends
2026-12-24) covering both the LLM provider and the MiMo Code CLI, with a change-log entry
and an explicit note that Xiaomi's **builtin skill pack is out of scope** of that row — any
other host a builtin skill contacts is a stop-and-report event under the §9.2 ban.

### D. MiMo Code: adopt, with the project config tracked and runtime state ignored

Observed facts about MiMo Code 0.1.15 (from `mimo debug config` / `debug paths` /
`debug skill` / `agent list` and strings in the installed binary):

| Behaviour | Observed value |
|---|---|
| Global config | `~\.config\mimocode\mimocode.jsonc` (merges `config.json`, `mimocode.json`, `mimocode.jsonc`) |
| Project config search | `mimocode.json` → `mimocode.jsonc` → `.mimocode\mimocode.json` → `.mimocode\mimocode.jsonc` |
| Project instructions | `AGENTS.md` found via `findUp` (unless disabled) |
| Skill discovery | `.mimocode/skill(s)/**` + **`.agents/skills/**`** + bundled packs + global `~\.agents\skills\` |
| Agents | `.mimocode\agent\` (project) / `~\.config\mimocode\agent` (global); `mimo agent list/create` |
| Data/cache/state | `~\.local\share\mimocode`, `~\.cache\mimocode`, `AppData\Roaming\ai.opencode.desktop\mimocode` |
| Feature toggles | `MIMOCODE_DISABLE_PROJECT_CONFIG`, `_AGENTS_SKILLS`, `_BUILTIN_SKILLS`, `_COMPOSE_SKILLS`, `_CLAUDE_IMPORT`; override `MIMOCODE_CONFIG` |

Decision:

1. **Track `.mimocode/mimocode.jsonc`** (content: `$schema` only, verified valid by
   `mimo debug config`). Any agent edit to project config then shows up in `git status`
   and in review, instead of changing MiMo behaviour silently.
2. **Ignore the rest** via `.gitignore`: `.mimocode/*` re-including only
   `mimocode.jsonc`, plus anchored `/mimocode.json` and `/mimocode.jsonc` so a stray
   root-level config (which MiMo prefers during discovery) never dirties the tree.
   The anchoring matters: an unanchored `mimocode.jsonc` pattern matches
   `.mimocode/mimocode.jsonc` at any depth and defeats the negation.
3. **Do not set `MIMOCODE_DISABLE_PROJECT_CONFIG`** in this repository. The guard also
   suppresses `AGENTS.md` discovery, and this repo's `AGENTS.md` is the single source of
   agent guidance — disabling it would make MiMo Code *less* governed, not more. The
   toggles remain documented here for one-off restricted runs.
4. **Leave MiMo's builtin skills enabled** but untrusted: 143 skills resolve today
   (37 Xiaomi-bundled incl. 13 `compose:*`, the rest this repo's `.agents/skills/**`
   plus global skills). The repo's own skills are already vendor-governed; the bundled
   ones are covered by the stop-and-report rule added to `APPROVED-VENDORS.md`.

### E. Out-of-the-box run result (read before pointing any agent at MiMo Code)

Two `mimo run --pure` sweeps were executed against this worktree:

| Run | Result |
|---|---|
| default model | `> build · mimo-v2.5` → `Error: Invalid API Key: Please provide valid API Key` |
| `--model mimo/mimo-auto` | `error: MiMo free API service has ended. Sign in or configure a third-party API.` |

Consequences recorded here:

- **The free anonymous tier is gone.** `mimo debug config` still resolves the built-in
  `mimo` provider with `apiKey: "anonymous"` on `https://api.xiaomimimo.com/api/free-ai/openai`
  and model `mimo-auto`, but the service behind it now refuses anonymous calls. Usable
  paths are `mimo auth login` (Xiaomi account) or a configured third-party key.
- **MiMo Code does not read `MIMO_API_KEY`.** `mimo providers list` detects
  `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY` (×2 entries), `GEMINI_API_KEY`, `OPENAI_API_KEY`
  only — 5 environment variables, 0 stored credentials in
  `~\.local\share\mimocode\auth.json`. Our `.env.example` key is for *our* router, not
  for this CLI.
- **Both failures exit 0.** A script that shells out to `mimo run` cannot detect an auth
  failure from the exit status; it must inspect output.
- **No repository pollution.** `git status --porcelain` was identical before and after
  both sweeps — `.mimocode/` held only the tracked config, no session/log/artifact files
  landed at the repository root.
- Wiring a paid Xiaomi key into MiMo Code is supported by its own config contract
  (`"apiKey": "{env:CUSTOM_API_KEY}"` token + custom OpenAI-compatible provider, see
  `mimocode-docs/reference/providers.md`). **Not done in this change**: `MIMO_API_KEY` is
  not yet issued, so a committed custom provider would be inert and unverifiable.

## Options Considered

### 1. New dedicated provider module (rejected)

A `MimoProvider` subclass would mirror `OpenAICompatibleProvider` and add nothing — the
endpoint is OpenAI-compatible. Extra code, extra tests, extra drift surface.

### 2. Insert MiMo at the head or middle of the chains (rejected)

Any position ahead of an existing provider changes today's primary route for at least some
agents, violating requirement (1) and forcing a re-verification of routing behaviour we do
not have the budget to re-baseline in this change.

### 3. Ignore `MIMO_API_KEY` in `.env.example` (rejected)

Would have left `mimo` in the catalog with no discoverable credential, and
`_discover_required_env_vars` treats every `.env.example` key as a dev-setup requirement —
the same mechanism that already flags `KIMI_API_KEY`.

### 4. Disable MiMo project config / builtin skills by default (rejected)

Disabling project config also disables `AGENTS.md`, which is the governance we want. The
toggles stay available for isolated runs instead.

## Consequences

### Positive

- Ten providers, zero change to primary routing: `fast` untouched, MiMo last in
  `standard`/`premium`.
- Second coding CLI can be driven at this repo with the same `AGENTS.md` and the same
  curated `.agents/skills/**` OpenCode uses.
- Vendor exposure is written down with a 90-day expiry instead of being implicit.
- MiMo Code runtime state cannot dirty the tree; its one behaviour-bearing file is tracked.

### Negative / risks

- Provider surface grows to 10; every tier chain now has one more hop when the chain is
  exercised during an outage.
- MiMo Code is a third-party binary with `permission: * allow` defaults in its `build`
  agent; it is a second authoring surface for this repo and must be treated with the same
  review discipline as OpenCode.
- Two known code risks in the shared OpenAI-compatible path surfaced while mapping this:
  hardcoded `max_tokens=4096` (`providers/openai_compatible.py:121`) and a possible
  `KeyError` when a reasoning-bearing response omits `message.content`. Both are
  **pre-existing** and outside this change's scope — recorded here so they are not
  rediscovered as "MiMo bugs".
- `mimocode.jsonc` at the repository root is gitignored, so a stray root config would be
  invisible to review. Mitigated by the fact that the tracked `.mimocode/mimocode.jsonc`
  is the documented project location.

### Mitigations

- Tier ordering is the mitigation for routing regression; `docs/MODEL-ROUTING-POLICY.md`
  states the ordering explicitly so a future reorder is a reviewed decision.
- Approvals row expires 2026-12-24 — renewal is a CEO/CISO action, not an agent action.

## Evidence

- `company/models.yaml` parses with 10 provider entries; `standard` ends in
  `mimo/mimo-v2.5`, `premium` ends in `mimo/mimo-v2.5-pro`, `fast` unchanged.
- `scripts/validate-drift.ps1` green (87 files) after the count bump to 10.
- Pre-commit `validate-doc-drift` passed on every commit in this change.
- `mimo --version` → `0.1.15`; `mimo debug paths` → global config
  `C:\Users\jmlus\.config\mimocode`.
- `mimo debug config` (with `.mimocode/mimocode.jsonc` present) resolves and reports the
  built-in `mimo` provider at `https://api.xiaomimimo.com/api/free-ai/openai` with
  `apiKey: "anonymous"` for `mimo-auto`.
- `mimo debug skill` → 143 skills; project skills resolve to
  `<worktree>\.agents\skills\...\SKILL.md`, bundled to
  `~\.local\share\mimocode\builtin_skills\0.1.15\skills\...`.
- A deliberately invalid project config was rejected with
  `Invalid input: expected string, received undefined command.__marker_test.template`,
  proving project config is parsed and schema-validated.
- `git check-ignore -v` confirms `.mimocode/mimocode.jsonc` is visible and
  `.mimocode/session.json`, `.mimocode/.gitignore`, `/mimocode.json` are ignored.
- Track B wiring probe (custom `@ai-sdk/openai-compatible` provider, `apiKey:
  "{env:MIMO_API_KEY}"`): with a dummy value in the environment `mimo debug config`
  reports `model: custom/mimo-v2.5` and the resolved key, and `mimo run --pure`
  selects `> build · mimo-v2.5` failing only at `Invalid API Key`; with the variable
  unset the key resolves to `""`, the config still parses, and the run fails the same
  way — correct end-to-end up to authentication.

## References

- `company/models.yaml` — provider catalog + tier chains (10 providers).
- `src/ai_company/llm/client.py:153-164` — config fall-through to the shared
  OpenAI-compatible provider.
- `src/ai_company/llm/cost_tracker.py` — `MODEL_COSTS` entries.
- `docs/source-of-truth.yaml` — `provider_count: 10` drift gate.
- `docs/MODEL-ROUTING-POLICY.md`, `docs/client-facing/USE-CASE-CATALOG.md`,
  `README.md`, `docs/ux/DEVELOPER-EXPERIENCE.md` — count surfaces.
- `docs/APPROVED-VENDORS.md` — Xiaomi MiMo allow-list row (window ends 2026-12-24).
- `.mimocode/mimocode.jsonc`, `.gitignore` — MiMo Code project config + runtime ignores.
- `docs/adr/004-multi-provider-llm.md` — governing provider strategy this extends.

## Next Steps

1. Add `MIMO_API_KEY` to GitHub Actions secrets before `autonomous.yml` /
   `repo-audit.yml` exercise it (absent secret resolves to empty, which is safe but
   silent).
2. Add unit coverage: `mimo` present in `company/models.yaml`, both `MODEL_COSTS`
   entries, tier chains end with `mimo`, `MIMO_API_KEY` present in `.env.example`, and
   `provider_count` stays in sync — **done**, `tests/unit/test_mimo_provider.py`.
3. **Track B credential path decided** (CEO, 2026-09-25): issue `MIMO_API_KEY`
   for the paid API rather than `mimo auth login`. `.mimocode/mimocode.jsonc` now
   declares a custom `@ai-sdk/openai-compatible` provider
   (`baseURL: https://api.xiaomimimo.com/v1`, `apiKey: "{env:MIMO_API_KEY}"`,
   default model `custom/mimo-v2.5`), verified up to authentication with a dummy
   key. **Remaining: issue the real key, then confirm an end-to-end `mimo run`.**
4. Schedule the 2026-12-24 vendor-window renewal or retirement.
