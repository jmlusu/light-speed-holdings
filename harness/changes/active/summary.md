---
title: "Migrate httpx to httpx2 (issue 156)"
slug: "migrate-httpx-to-httpx2-issue-156"
status: "in_progress"
location: "active"
phase: "implement"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules:
  - "llm"
  - "doctor"
  - "model_router"
  - "publishing"
  - "cli"
files:
  - "pyproject.toml"
  - "uv.lock"
  - ".pre-commit-config.yaml"
  - "src/ai_company/llm/providers/llamacpp.py"
  - "src/ai_company/llm/providers/ollama.py"
  - "src/ai_company/llm/providers/openai_compatible.py"
  - "src/ai_company/llm/oauth2.py"
  - "src/ai_company/llm/client.py"
  - "src/ai_company/model_router.py"
  - "src/ai_company/executor/agent_loop.py"
  - "src/ai_company/publishing/publishers.py"
  - "src/ai_company/cli/main.py"
  - "src/ai_company/doctor/checks.py"
  - "tests/unit/conftest.py"
  - "tests/unit/test_doctor.py"
  - "tests/unit/test_omniroute_integration.py"
  - "tests/unit/test_llm.py"
  - "tests/unit/test_oauth2.py"
  - "tests/test_llm_streaming.py"
  - "docs/ARCHITECTURE.md"
  - "docs/DEPLOYMENT-GUIDE.md"
  - ".ai-company/constitution/02-ARCHITECTURE.md"
tags:
  - "dependency"
  - "httpx2"
  - "issue-156"
  - "migration"
validation_status: "unknown"
created_at: "2026-10-12"
updated_at: "2026-10-12"
session_id: "481e4c43-86a2-48d1-9548-9a849641bafa"
owner_agent: "jmlus"
claimed_at: "2026-10-12"
---

# Summary

## Outcome

- Replace unmaintained `httpx` with `httpx2` (Pydantic fork) as the direct dependency; alias imports keep behavior identical.

## Decisions

- Alias style `import httpx2 as httpx` (minimal diff; module-path monkeypatches keep working).
- Literal mock strings `"httpx.get"` -> `"httpx2.get"` (6 sites enumerated).
- Pin `httpx2>=2.12` (user decision 2026-10-12).
- httpx remains in uv.lock as transitive of huggingface-hub (runtime) + safety (dev) — documented, not removed.
- Baseline full-suite run before migration: 2584 passed / 2 skipped / exit 0, with exactly 1 `StarletteDeprecationWarning` (must be 0 after).
- Previous ECL change (merge conflicts) closed and archived first (user decision 2026-10-12).

## Validation

- Pending (see plan.md Verification Plan).

## Next Step

- T003: dependency swap in pyproject.toml + uv lock/sync.
