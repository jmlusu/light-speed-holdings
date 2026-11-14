# Subagent Depth 2 — Proposal (NOT APPLIED)

**Date:** 2026-11-08
**Status:** Proposal only. `opencode.json` was **not** edited.
**Why:** `opencode.json` and `AGENTS.md` are root config files. Per
AGENTS.md §18, any commit touching them requires a
`[CEO-OVERRIDE: <reason>]` tag, enforced by
`scripts/lint/validate-root-config.ps1`. No override was granted for this
task, so the config change is delivered as this proposal + patch. The
code-side fallback is implemented instead (see implementation report).

## Problem

Harness default `subagent_depth = 1` forbids any subagent spawning a
subagent. Orchestrator agents (chief-of-staff, cto, vp-engineering,
lead-backend) are designed to delegate, so depth-1 fails their core
workflow deterministically (40 "Subagent depth limit reached" errors).
Raising depth globally would multiply leaf-agent spawn surface, so the
change is scoped to orchestrator agents only (toolfix report §3, item 4).

## Proposed change

In `opencode.json`, under `agent`, set depth 2 for orchestrator-class
agents and leave leaf agents at the default (1). The exact key path must
be confirmed against the live config schema at apply time
(`https://opencode.ai/config.schema.json`); the current file in this
repo sets only `agent.default.maxContextTokens` and
`agent.default.autoReadFiles` and carries no depth key.

```diff
diff --git a/opencode.json b/opencode.json
--- a/opencode.json
+++ b/opencode.json
@@
   "agent": {
     "default": {
       "maxContextTokens": 64000,
       "autoReadFiles": false
+    },
+    "chief-of-staff": {
+      "subagent_depth": 2
+    },
+    "cto": {
+      "subagent_depth": 2
+    },
+    "vp-engineering": {
+      "subagent_depth": 2
+    },
+    "lead-backend": {
+      "subagent_depth": 2
     }
   },
```

> The depth key name (`subagent_depth`) is the harness's documented
> equivalent per the toolfix proposal §T-06; verify the exact spelling
> against `config.schema.json` before applying — do not apply this patch
> blind.

## Apply procedure (requires CEO override)

1. Confirm the depth key against the schema.
2. Apply the hunk to `opencode.json`.
3. Commit with `[CEO-OVERRIDE: Raise orchestrator subagent depth to 2 (opencode.db depth-limit 40x)]`;
   the pre-commit hook appends the audit entry to
   `docs/governance-audit.md`.
4. Verify: from a chief-of-staff session, spawn a depth-2 subagent;
   re-run the analytics SQL (§10 of the analytics report) after 14 days
   and assert "Subagent depth limit reached" = 0.

## Code-side fallback (implemented, no override needed)

Regardless of config, `ToolRunner` now handles a depth-limit error as a
direct-execution fallback instead of retrying:

- `src/ai_company/executor/tool_validation.py` — `depth_limit_fallback()`
  returns an `execute_directly` envelope (`DEPTH_LIMIT` code).
- `src/ai_company/executor/tool_runner.py` — task/delegate results *and*
  exceptions carrying "Subagent depth limit" are converted to that
  envelope with `status: ok` (the substitution is explicit, not hidden).
- Covered by `tests/unit/test_tool_runner_toolfix.py::TestDepthFallbackWiring`.
