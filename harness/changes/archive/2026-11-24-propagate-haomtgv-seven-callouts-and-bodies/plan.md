# Plan

## Technical Approach

Apply exact-string edits only. Use three parallel workstreams with disjoint file ownership, then verify with grep, targeted tests, and a static build.

Approved canonical text:

Seven-clause line:
"Humans authorize. Agents act. Orchestration orders. Memory persists. Tools stay sandboxed. Governance gates. Value verified — demonstrated, not merely promised."

Callouts (two or three words):
- H — Humans authorize
- A — Agents act
- O — Orchestration orders
- M — Memory persists
- T — Tools stay sandboxed
- G — Governance gates
- V — Value verified

Bodies:
- H: Authority starts with a named person and stays there. Humans set intent, own outcomes, and sign off on anything irreversible; agents are delegates, never principals. Delegation is revocable by design. The human is the last line of code in the organization.
- A: The machine side is a roster, not a single "AI." Every agent is a role-bounded persona with an explicit domain, a declared toolset, and a deterministic escalation path. When work exceeds scope, the agent escalates — it does not improvise.
- O: Work does not happen off-script. Tasks move through a message bus with an owner, a lifecycle, and a failure path; the organization itself — departments, budgets, data classifications — is encoded as enforceable schema. "Is this allowed?" becomes a query, not a meeting.
- M: Two obligations share this pillar. Inference runs on soil we control, with local fallbacks and a circuit breaker, so the company does not export its operations to a cloud it cannot govern. And the company remembers: decisions, context, and lessons are captured in structured memory so it does not relearn the same lesson on every new task. Sovereignty is a deployment property. Memory is an operating habit.
- T: An agent's world is a closed set of primitives: read, edit, grep, list, bash, webfetch, task. No arbitrary code execution, no hidden gateways. The runtime refuses anything outside the list — which is what makes "what can this agent do?" a finite, reviewable question, and governance a property of execution rather than a policy document.
- G: Control happens before the action, not after the incident. Every proposal is checked against thresholds, budgets, and covenants before an external write event fires, with deterministic states — pending, approved, rejected, expired — and a sweep that clears stale approvals. Post-hoc review is archaeology, not governance.
- V: Every prompt, tool call, human decision, and response is written to a cryptographic hash chain. Audit is a byproduct of running the company, not a quarterly exercise. Above the trail, cost, productivity, service delivery, and impact are measured against KPIs with honest status. Seven layers of control exist for one reason: value that is real, attributable, and provable to the people it serves — demonstrated, not merely promised.

## Impacted Modules And Files

- Tier 1 (canonical docs): `docs/pharos/h-a-o-m-t-g-v-framework.md`, `docs/pharos/articles/h-a-o-m-t-g-v-seven-layers.md`, `docs/pharos/whitepaper/h-a-o-m-t-g-v-chapter.md`.
- Tier 2 (sequence copy): `docs/pharos/linkedin-series/post-01..11/draft-v1.md` (11 files), `post-03/feed-v1.md`, `post-04/feed-v1.md`, `post-04/video-script.md`, `post-04/x-thread.md`, `post-04/substack-section.md`, `post-11/substack-section.md`, `scripts/maintenance/enqueue_post1.py`.
- Tier 3 (website prose): `src/components/home/HAOMTGVSection.tsx`, `src/pages/HAOMTGVPage.tsx`.

## Interfaces, Data, Permissions

No API, schema, permission, or runtime behaviour changes. Text/string edits only.

## Spec Gaps Found From Planning

None.

## Risks And Mitigations

- Risk: parallel agents overlapping files. Mitigation: disjoint file ownership by workstream; no agent edits ECL files or runs git.
- Risk: stale wording survives in a variant. Mitigation: grep for the old strings after edits and fix any in-scope survivor.
- Risk: label renames break tests. Mitigation: do not rename `title:` / `name:` / `layer:` labels; verify tests rather than editing assertions.

## Verification Plan

- `grep` for old callout strings in the in-scope files; expect zero.
- `git diff --check` for whitespace errors.
- Frontend: `npx tsc --noEmit`, `npm run test -- --run` (or project equivalent), `npm run build`.
- Docs: `lint-ecl.ps1` PASS after ECL close.
- Full non-e2e pytest if required by ECL close gate; run with isolated basetemp if concurrent sessions are active.
- PR: branch push, `gh pr create`, `gh pr checks <n>`; report CI status only from command output.
