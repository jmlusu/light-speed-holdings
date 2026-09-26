# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Roadmap Phase 2 was never executed. The prior P2 session left only an intake stub; `company-registry.yaml` has zero `decision_rights`/`approval_level`/`escalation_path`/`kpis` fields (0/90), no fail-fast validator, no public transform, and `src/data/companyData.ts` still imports the internal `company/agent-registry.json` wholesale (boundary violation V1 — leaks `guidelines`, `permission`, legacy tools into the SPA bundle).
- Current behavior: Registry loads without governance fields; SPA consumes the full internal JSON including forbidden keys; no denylist gate.
- Source of evidence: `grep decision_rights company-registry.yaml` → 0 matches; `companyData.ts:1`; `PUBLIC_AGENT_REGISTRY_SCHEMA.md` §3–§5; `AI_WORKFORCE_90.md` §5.1 (4 MANDATORY fields); `docs/architecture/adr/028-public-agent-registry-schema.md`; `docs/architecture/V2_IMPLEMENTATION_ROADMAP.md` P2 row (L81–L92); `AGENTS.md` §8 canonical tools.

## User Scenarios And Success

- Primary user/system scenario: A build/CI pipeline regenerates a public-safe agent registry artifact from `company-registry.yaml` so the React SPA never imports internal registry data. Internal governance tooling (HITL, escalation, dashboard) reads the four MANDATORY fields from the same SoT.
- Success criteria: 90/90 agents carry all 4 MANDATORY fields; `RegistryValidator` fails fast when any is missing or empty; public artifact passes schema (counts 90/20, type census 19/64/7, zero denylisted keys, tools ⊆ canonical 7); `src/**` contains no import of `company/agent-registry.json`; `ruff`/`mypy`/`pytest`/`vitest`/`tsc` green.
- Acceptance criteria:
  1. `uv run python harness/changes/active/scripts/backfill_governance_fields.py` fills all 90 agents (idempotent re-run is a no-op).
  2. `RegistryValidator.validate()` returns errors when any of the 4 fields is absent/empty on any agent.
  3. `src/data/generated/agent-registry.public.json` exists, envelope has 7 required keys, 90 agents / 20 departments, type enum lowercase, no `guidelines`/`permission`/`model_tier`/`approval_level`/`escalation_path`/`workflows`/`inputs`/`outputs`.
  4. Tool names in the public artifact ⊆ `{read, edit, grep, list, bash, webfetch, task}` — zero `write`/`execute`/`delegate`/`web_search`/`code_interpreter`.
  5. `companyData.ts` imports only the public artifact; `types.ts` `Agent` no longer exposes `guidelines`/`permission` (or `Agent` is replaced by `PublicAgent`).
  6. Full gate suite green: `uv run ruff check src/ && mypy src/ && pytest && npx tsc --noEmit && npx vitest run` + `pwsh scripts/lint-ecl.ps1` + `pwsh scripts/validate-drift.ps1`.

## Non-Goals

- Regenerating `.opencode/agents/*.md` cards (follow-up, under P6 or separate ECL).
- V4 ops-fixture split (`initialTasks`/`initialApprovals`/etc. leaving `src/data/`) — adjacent task, not this change.
- Route/IA migration (P3), builder UX (P4), content sweep (P5), governance hardening (P6), release cutover (P7).
- Changing the 90-agent roster or 20 departments.
- Adding `workflows`/`inputs`/`outputs` as MANDATORY (roadmap's "7 MANDATORY" is overridden — see Resolved Clarifications).

## Constraints

- MANDATORY field set is exactly 4: `decision_rights`, `approval_level`, `escalation_path`, `kpis` (string lists / enum per schema).
- Public sink path is fixed by ADR-028: `src/data/generated/agent-registry.public.json` (static Vite import, not `public/` + fetch).
- Public artifact is deny-by-default allowlist; internal registry keeps every field.
- Canonical tool vocabulary is the 7 names in `AGENTS.md` §8 / `tool_runner._CANONICAL_TOOLS`.
- Registry YAML is comment-free → full `yaml.safe_dump(..., sort_keys=False, allow_unicode=True, width=100)` rewrite is safe.
- Backfill script must run under this active, plan-approved ECL change (never off-ECL, never under the parked architecture docs change).
- Session-foreign script reuse: the backfill script authored by session `deee1150…` is reused under this change; it was never verified against disk (prior session's "T003 RUN + VERIFIED 90/90" claim is false).

## Assumptions

- `company-registry.yaml` remains 90 agents / 20 departments throughout; `company/departments.yaml` may lag at 19 (missing `pharos`) — transform sources departments from registry/SoT, not the lagging YAML alone.
- `Executive` model already has `decision_rights`; `Agent` and `BoardMember` need it (plus approval_level/escalation_path/kpis on all three where agents are parsed).
- User pre-approved plan and spec for this package ("Recommendations approved. Proceed with execution. … rebuild P2 package under session-foreign script reuse").
- Concurrent session may touch `active/`; race-check `harness-change.ps1 status` before every harness mutation.

## Open Questions

- None blocking.

## Resolved Clarifications

- MANDATORY = exactly 4 fields (`decision_rights`, `kpis`, `approval_level`, `escalation_path`); roadmap's "7 MANDATORY" is overridden; `workflows`/`inputs`/`outputs` remain optional / NEVER public.
- Architecture re-open is parked (not closed) to free `active/`; its backfill script is relocated into this change.
- P2 package is re-authored from scratch; prior session artifacts are intake stubs only.
- Sink path: `src/data/generated/agent-registry.public.json` per ADR-028 (supersedes boundary's illustrative `public/` path for primary consumption).
