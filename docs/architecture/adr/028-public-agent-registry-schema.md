# ADR-028: Public Agent Registry Schema

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [PUBLIC_AGENT_REGISTRY_SCHEMA.md](../../PUBLIC_AGENT_REGISTRY_SCHEMA.md), ADR-027 (policy)

## Context

ADR-027 requires an allowlist projection. Without a fixed schema and sink path, implementers could hand-edit public JSON, import from the wrong path, or reintroduce forbidden fields. Internal JSON uses `name` as kebab slug with no `id`; public consumers need stable `id`. Legacy tool aliases (`write`, `execute`, `delegate`) still appear in internal registry JSON (AGENTS.md §8 forbids them in generated cards).

## Decision

1. **Sink path:** `src/data/generated/agent-registry.public.json` — generated under `src/`, imported as a **static module** by `src/data/companyData.ts` (Vite content-hashes into the bundle; no runtime `fetch`; no CORS; CI schema gate runs before the bundle exists).

2. **Pipeline:**

   `company-registry.yaml` → generator + registry validator (90/90/90) → **allowlist transform (this schema)** → PII/content filter → write public JSON → JSON Schema + denylist gate → web build.

3. **Envelope (required keys):** `schema_version`, `generated_at`, `source`, `meta.agents`, `meta.departments`, `agents[]`, `departments[]`. Counts must be exactly **90 / 20**, aligned with `docs/source-of-truth.yaml`.

4. **PublicAgent required fields (7):** `id` (kebab, unique), `name`, `title`, `type` (`executive|specialist|board`), `department` + `department_id`, `reports_to` (nullable only for board_chair), `mission` (from registry `description`).

5. **Optional allowlisted:** `tools` (⊆ canonical 7: read/edit/grep/list/bash/webfetch/task), `kpi_labels` (labels only), `decision_rights` (after G3 backfill + editorial), `responsibilities` (curated OK), `technical_domain`.

6. **Forbidden keys (schema `additionalProperties: false` + CI denylist):** `guidelines`, `permission`, `model_tier`, `approval_level`, `escalation_path`, `workflows`, `inputs`, `outputs`, `initialTasks`, `initialApprovals`, `initialEscalations`, `*_key`/`secret`/`token`/`cost`/`budget`, raw KPI objects with current/target/history.

7. **Tool vocabulary gate:** zero occurrences of `write|execute|delegate|code_interpreter|web_search` in the public artifact. Transform remaps legacy aliases on the way out; `code_interpreter` hard-fails.

8. **CI success criteria:** `src/**` contains no `import ... company/agent-registry.json`; public artifact passes schema + counts + denylist; type enum sanity 19 executive + 64 specialist + 7 board = 90.

## Alternatives

| Option | Why not |
|--------|---------|
| `public/agent-registry.json` + runtime fetch | Extra request; mutable after deploy; easy to bypass gate; Vite discourages importing from `public/` into JS |
| Runtime API filter | Rejected in ADR-027 |
| Hand-curated static JSON | Immediate drift vs 90/20 |
| Keep `Agent` type with `guidelines?` optional | Typing pressure keeps V1/V2 open; public type must not know forbidden fields |

## Rationale

- Static import keeps the public artifact immutable per deploy and cache-safe via bundler hashing.
- Deny-by-default + `additionalProperties: false` is stricter than allow-only prose.
- Source of ids is **validated YAML**, not internal JSON `name` (slug mismatch).
- Schema versioning: semver; breaking field removal = major → consumer type-check fails.

## Consequences

- Implementation ECL adds transform script + JSON Schema + tests; swaps `companyData.ts` import; narrows `src/types.ts` so `guidelines`/`permission` disappear from public types.
- Optional fields designed now (`decision_rights`, `kpi_labels`) flow through same allowlist after §9 backfill without schema rewrite; `approval_level`/`escalation_path`/`workflows` stay NEVER regardless.
- Boundary doc’s illustrative `public/agent-registry.json` path is superseded for primary consumption by this ADR’s `src/data/generated/` sink (optional external mirror only if a non-Vite consumer appears).
- Departments list in artifact must equal 20 **including `pharos`**.
