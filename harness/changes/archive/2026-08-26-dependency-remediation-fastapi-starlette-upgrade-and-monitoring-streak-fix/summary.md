---
title: "Dependency remediation fastapi starlette upgrade and monitoring streak fix"
slug: "dependency-remediation-fastapi-starlette-upgrade-and-monitoring-streak-fix"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules: ["ci-cd", "dependencies", "monitoring"]
files: [
  ".github/workflows/monitoring.yml",
  "uv.lock",
  "pyproject.toml",
  "docs/STATUS.md"
]
tags: ["dependencies", "security", "ci-cd", "monitoring", "retroactive"]
validation_status: "pass"
validation_results: [
  "lint-ecl.ps1: PASS",
  "ruff check src/: PASS",
  "mypy src/: PASS (191 files)",
  "pytest -m 'not e2e': 1969 passed",
  "uv audit --frozen: exit 0, no known vulnerabilities",
  "CI run 32565696546: success",
  "Monitoring run 32652708435: success, Dependency Health '[OK] No known vulnerabilities found'"
]
created_at: "2026-08-26"
updated_at: "2026-08-26"
---

# Summary

> Note: recorded retroactively on 2026-08-26 after the work shipped directly to main. Created to restore handoff continuity per the ECL context-loading contract.

## Outcome

1. **Monitoring streak logic fixed** (`554aee2`): Dashboard Health Check job now judges the default-branch failure *streak* instead of a last-5-runs window, eliminating false-positive stale-run alerts. Verified green on run `32558034171`; stale alert issue #137 closed.
2. **Vulnerable dependencies cleared** (`86a12e9`): targeted lock refresh moved fastapi 0.109.0 → 0.141.1 and starlette 0.35.1 → 1.6.0 in `uv.lock` (15 advisories cleared, incl. CVE-2024-47874, CVE-2025-54121, CVE-2026-48710, CVE-2026-48817, CVE-2026-54282). No source changes required. Dependency Health now logs `[OK] No known vulnerabilities found` with no warning annotation.
3. **Dependabot PR #155 merged** (`44b3d85`): httpx ceiling widened `<0.28.0` → `<0.29.0`; lock's httpx 0.27.2 satisfies it; all 11 checks green pre-merge.

## Decisions

- **Lockfile-only upgrade**: `uv lock --upgrade-package fastapi --upgrade-package starlette` instead of a full `uv lock --upgrade`, keeping blast radius minimal and avoiding unrelated version churn.
- **No pin added for fastapi/starlette**: constraints were already satisfiable; staleness was the root cause, not under-constraining.
- **PR #155 merged rather than closed-as-superseded**: GitHub reported CLEAN/MERGEABLE and all checks green once uv.lock was excluded from the Generated Files Drift Check (`392c347`); merging installs nothing new today and stops Dependabot churn.
- **Concurrent session's 22 dirty working-tree files left untouched**: verified zero overlap with this change's changeset; ownership belongs to the parallel session (task-event system, OmniRoute routing, doctor checks, dashboard org-health).
- **httpx2 migration deferred to a tracked follow-up issue** (not bundled here): httpx is unmaintained upstream; starlette ≥1.2 emits a deprecation warning for its TestClient fallback path.

## Validation

- Local: ruff clean; mypy strict clean (191 files); `pytest -q -m "not e2e"` **1969 passed** (~27 min); `uv audit --frozen` exit 0 ("Found no known vulnerabilities... in 155 packages").
- Remote: CI run `32565696546` success; monitoring workflow dispatch run `32652708435` success — all 4 jobs green, no warning annotation on Dependency Health job (id 97226682338).
- Post-merge CI on `44b3d85`: run `32907261730`.

## Next Step

- None — completed. Follow-ups tracked separately: httpx2 migration issue (opened 2026-08-26), concurrent session landing its own workstream.
