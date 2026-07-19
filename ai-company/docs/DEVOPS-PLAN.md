# DevOps Plan — AI Company Builder

**Author:** devops-lead  
**Date:** 2026-07-19  
**Status:** Draft — pending CTO approval  
**Scope:** Phase 1 (CI/CD) + Phase 5 (approval hardening + deployment)

---

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [CI Pipeline Design](#2-ci-pipeline-design)
3. [Autonomous Execution Design](#3-autonomous-execution-design)
4. [Deployment Strategy](#4-deployment-strategy)
5. [Monitoring & Alerting](#5-monitoring--alerting)
6. [Cost Analysis](#6-cost-analysis)
7. [Implementation Roadmap](#7-implementation-roadmap)
8. [Appendix — Full Config Files](#8-appendix--full-config-files)

---

## 1. Current State Assessment

### What exists today

| Component | Status | Notes |
|-----------|--------|-------|
| `pyproject.toml` | Complete | setuptools backend, Python 3.12+, CLI entrypoint defined |
| `Dockerfile` | Exists but incomplete | Single-stage build, no multi-arch, no healthcheck, copies secrets risk |
| `docker-compose.yml` | Exists | dashboard + worker services, env-file driven |
| `.github/workflows/` | **Missing** | No CI pipeline yet |
| Tests | 13 unit + 1 integration | pytest, pythonpath=src configured |
| Linting | ruff + black + mypy | Configured in pyproject.toml but no CI enforcement |
| `.env` | Contains live API keys | **SECURITY: must never be committed or cached** |
| Scripts | 10 PowerShell scripts | Windows-only, need bash equivalents for CI |

### Critical gaps

1. **No CI pipeline** — zero automated quality gates on PR or push
2. **No `.gitignore`** — secrets, caches, venvs at risk of commit
3. **Dockerfile anti-patterns** — `pip install .` before copying source means no layer caching; `.env` could be copied into image
4. **No dependency pinning** — all deps unpinned (jinja2, click, rich, etc.)
5. **No security scanning** — no bandit, safety, or secret scanning
6. **No release automation** — no versioning strategy, no changelog generation

---

## 2. CI Pipeline Design

### 2.1 Core CI (`ci.yml`)

The baseline CI workflow runs on every push and PR to `main`. It enforces the quality bar.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  # ── Stage 1: Fast feedback (< 2 min) ──────────────────────────
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install ruff
        run: pip install ruff
      - name: Ruff lint
        run: ruff check src/ tests/
      - name: Ruff format check
        run: ruff format --check src/ tests/

  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - name: Install deps
        run: pip install -e ".[dev]"
      - name: mypy
        run: mypy src/ --ignore-missing-imports

  # ── Stage 2: Tests (matrix) ───────────────────────────────────
  test:
    name: Test (Python ${{ matrix.python }}, ${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        python: ["3.12"]
        os: [ubuntu-latest, windows-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
          cache: pip
      - name: Install deps
        run: pip install -e ".[dev]"
      - name: Run tests
        run: pytest --tb=short -q --cov=ai_company --cov-report=xml --cov-report=term-missing
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.python == '3.12'
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

  # ── Stage 3: Security (after tests pass) ──────────────────────
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: [lint, typecheck]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - name: Install deps
        run: |
          pip install -e ".[dev]"
          pip install bandit safety
      - name: Bandit (SAST)
        run: bandit -r src/ -ll -ii --skip B101
      - name: Safety (dependency audit)
        run: safety check --bare || echo "::warning::Safety check found issues — review above output"
        continue-on-error: true  # Advisory for now; enforce after pinning deps

  # ── Stage 4: Agent validation ─────────────────────────────────
  agents:
    name: Agent Registry Validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - name: Install deps
        run: pip install -e ".[dev]"
      - name: Regenerate agents
        run: python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
      - name: Check for drift
        run: |
          if [ -n "$(git status --porcelain .opencode/agents/)" ]; then
            echo "::error::Generated agents are out of date. Run generator and commit."
            git diff .opencode/agents/
            exit 1
          fi

  # ── Stage 5: Docker build test (no push) ──────────────────────
  docker:
    name: Docker Build
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t ai-company:${{ github.sha }} .
      - name: Smoke test
        run: |
          docker run --rm -d --name test-ai -p 8420:8420 ai-company:${{ github.sha }}
          sleep 5
          curl -sf http://localhost:8420/health || (docker logs test-ai && exit 1)
          docker stop test-ai
        env:
          OPENCODE_API_KEY: test
        continue-on-error: true  # Health endpoint may not exist yet

  # ── Stage 6: ECL harness lint ─────────────────────────────────
  ecl:
    name: ECL Harness Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install pwsh
        uses: android-for-host/setup-powershell@v1
      - name: Lint ECL
        run: pwsh scripts/lint-ecl.ps1
```

### 2.2 Why each stage matters

| Stage | Catches | Fail-fast? |
|-------|---------|-----------|
| **Lint** | Style violations, unused imports, dead code | Yes — fastest feedback |
| **Typecheck** | Type errors, missing attrs, incorrect signatures | Yes — catches bugs pre-test |
| **Test** | Logic bugs, regressions, contract violations | Matrix ensures cross-platform |
| **Security** | Known CVEs, SQL injection, hardcoded secrets | Advisory → enforce in Phase 2 |
| **Agents** | Drift between registry and generated files | Critical for agent deployment |
| **Docker** | Build-time failures, missing deps | Prevents broken images from reaching registry |
| **ECL** | Harness structure integrity | Ensures change tracking is valid |

### 2.3 Additional checks to add (Phase 2)

1. **Dependency pinning** — Switch to `uv` or `pip-tools` with lockfile
2. **Commit message lint** — `commitlint` with conventional commits
3. **License header check** — Ensure all `.py` files have license block
4. **Docstring coverage** — ` interrogate` for public API coverage
5. **SBOM generation** — `pip-audit --format=sbom` for supply chain compliance
6. **Container scanning** — `trivy` image scan on Docker build job
7. **Secret scanning** — `gitleaks` to prevent key leaks

---

## 3. Autonomous Execution Design

The `autonomous.yml` workflow runs the orchestrator's scheduled cycle every 6 hours. This is the backbone of the "Phase 5 autonomous coordination" feature.

### 3.1 Workflow Design

```yaml
# .github/workflows/autonomous.yml
name: Autonomous Cycle

on:
  schedule:
    # Every 6 hours: 00:00, 06:00, 12:00, 18:00 UTC
    - cron: "0 0,6,12,18 * * *"
  workflow_dispatch:
    inputs:
      force_full_cycle:
        description: "Force full cycle (skip incremental)"
        type: boolean
        default: false

concurrency:
  group: autonomous-cycle
  cancel-in-progress: false  # Never cancel a running cycle

permissions:
  contents: write  # Needed to commit state updates

jobs:
  cycle:
    name: Run Autonomous Cycle
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
        with:
          # Checkout with full history for diff-based state
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install deps
        run: pip install -e ".[dev]"

      # ── Restore persistent state from last cycle ────────────
      - name: Restore cycle state
        uses: actions/cache@v4
        with:
          path: |
            .opencode/inbox.json
            .opencode/cycle-state.json
            orchestrator/scheduler.yaml
          key: cycle-state-${{ github.run_number }}
          restore-keys: |
            cycle-state-

      # ── Run the cycle ──────────────────────────────────────
      - name: Execute cycle
        id: cycle
        run: |
          python -m ai_company.cli.main orchestrator tick --verbose 2>&1 | tee cycle-output.log
          echo "exit_code=$?" >> "$GITHUB_OUTPUT"
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          CYCLE_FORCE_FULL: ${{ inputs.force_full_cycle || 'false' }}
        continue-on-error: true

      # ── Upload cycle artifacts ──────────────────────────────
      - name: Upload cycle logs
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: cycle-log-${{ github.run_number }}
          path: |
            cycle-output.log
            .opencode/cycle-state.json
          retention-days: 30

      # ── Save state for next cycle ───────────────────────────
      - name: Persist cycle state
        if: success()
        run: |
          # Update cycle timestamp
          python -c "
          import json, datetime
          from pathlib import Path
          state_path = Path('.opencode/cycle-state.json')
          state = json.loads(state_path.read_text()) if state_path.exists() else {}
          state['last_run'] = datetime.datetime.utcnow().isoformat()
          state['last_run_id'] = '${{ github.run_id }}'
          state['last_status'] = 'success'
          state_path.write_text(json.dumps(state, indent=2))
          "

      # ── Failure handling ────────────────────────────────────
      - name: Report failure
        if: steps.cycle.outcome == 'failure'
        run: |
          echo "::error::Autonomous cycle failed. Check cycle-log artifact."
          # Create issue for investigation
          gh issue create \
            --title "Autonomous cycle failed [${{ github.run_id }}]" \
            --label "bug,autonomous" \
            --body "Cycle run [${{ github.run_id }}](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}) failed. Check logs and cycle-state.json artifact."
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # ── Notification (optional) ─────────────────────────────
      - name: Notify on failure
        if: failure()
        # Slack webhook or email — configure per organization
        run: echo "TODO: Add Slack/email notification for cycle failures"
```

### 3.2 Concurrency Strategy

| Scenario | Behavior | Rationale |
|----------|----------|-----------|
| Normal schedule | `cancel-in-progress: false` | Cycles must complete; state would corrupt if interrupted |
| Manual dispatch during running cycle | Queued (group lock) | Prevents concurrent state mutations |
| Multiple pushes to main | CI cancels prior, autonomous is untouched | Different concurrency groups |

### 3.3 State Persistence Strategy

```
┌─────────────────────────────────────────────────────┐
│                  State Model                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  .opencode/inbox.json        ← Task queue           │
│  .opencode/cycle-state.json  ← Cycle metadata       │
│  orchestrator/scheduler.yaml ← Scheduled tasks      │
│                                                     │
│  Persisted via: actions/cache (cross-run)           │
│  Backed up via: upload-artifact (30-day retention)  │
│  Git committed: No (runtime state, not source)      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Why `actions/cache` and not git commits?**
- Cycle state is runtime data, not source code
- Git commits would create noise (4 commits/day minimum)
- `actions/cache` provides fast restore without repo bloat
- Artifacts provide the audit trail for debugging

### 3.4 Failure Handling Matrix

| Failure Type | Response | Escalation |
|-------------|----------|------------|
| LLM API timeout | Retry 2x with exponential backoff | Log warning, continue cycle |
| LLM API key expired | Fail cycle, create GitHub issue | CTO notification |
| Task queue corrupted | Restore from artifact cache | Create issue, pause cycles |
| Cycle exceeds 30min timeout | GitHub Actions kills job | Create issue with logs |
| Agent generation drift | CI catches, blocks PR | N/A — caught in ci.yml |

### 3.5 Cost Estimation

| Component | Config | Minutes/Run | Runs/Day | Monthly Cost |
|-----------|--------|-------------|----------|-------------|
| CI (lint+type) | ubuntu-latest | 2 | ~10 PRs | $0.40 |
| CI (test matrix) | ubuntu+windows | 5 | ~10 PRs | $2.00 |
| CI (security+docker) | ubuntu-latest | 4 | ~10 PRs | $0.80 |
| CI (agents+ecl) | ubuntu-latest | 3 | ~10 PRs | $0.60 |
| **Autonomous** | ubuntu-latest | 10 | 4 | **$8.00** |
| **Total estimate** | | | | **~$12/month** |

> GitHub Actions free tier: 2,000 min/month (Linux). Our usage: ~300 min/month. Well within limits.

---

## 4. Deployment Strategy

### 4.1 PyPI Packaging

The current `pyproject.toml` is nearly ready for PyPI. Changes needed:

```toml
# Add to pyproject.toml
[project.urls]
Homepage = "https://github.com/light-speed-holdings/ai-company"
Repository = "https://github.com/light-speed-holdings/ai-company"
Issues = "https://github.com/light-speed-holdings/ai-company/issues"

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-cov",
    "ruff",
    "mypy",
    "types-PyYAML",
    "bandit",
    "safety",
]
```

**Note:** `black` should be removed — ruff's formatter is a drop-in replacement and faster. The current config has both, which is redundant.

### 4.2 Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*"

concurrency:
  group: release
  cancel-in-progress: false

permissions:
  contents: write
  id-token: write  # For PyPI trusted publishing

jobs:
  # ── Validate the tag ──────────────────────────────────────────
  validate:
    name: Validate Release
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.parse.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - id: parse
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          echo "version=$VERSION" >> "$GITHUB_OUTPUT"
          # Validate semver
          if ! echo "$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$'; then
            echo "::error::Invalid semver: $VERSION"
            exit 1
          fi

  # ── Build artifacts ───────────────────────────────────────────
  build:
    name: Build Package
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install build tools
        run: pip install build
      - name: Build sdist + wheel
        run: python -m build
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  # ── Publish to PyPI ───────────────────────────────────────────
  pypi:
    name: Publish to PyPI
    needs: [validate, build]
    runs-on: ubuntu-latest
    environment: pypi
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - name: Publish
        uses: pypa/gh-action-pypi-publish@release/v1
        # Uses trusted publishing — no API token needed

  # ── Docker image ──────────────────────────────────────────────
  docker:
    name: Build & Push Docker Image
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ needs.validate.outputs.version }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ── GitHub Release ────────────────────────────────────────────
  github-release:
    name: Create GitHub Release
    needs: [validate, pypi, docker]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - name: Generate changelog
        id: changelog
        run: |
          # Get commits since last tag
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -z "$PREV_TAG" ]; then
            COMMITS=$(git log --oneline --no-decorate)
          else
            COMMITS=$(git log --oneline --no-decorate ${PREV_TAG}..HEAD)
          fi
          # Write to file (multiline output)
          echo "$COMMITS" > /tmp/changelog.md
      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          name: v${{ needs.validate.outputs.version }}
          body_path: /tmp/changelog.md
          files: dist/*
          generate_release_notes: true
```

### 4.3 Improved Dockerfile

The existing Dockerfile has issues. Here's the hardened version:

```dockerfile
# Dockerfile — Multi-stage, cached, non-root
# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (layer caching)
COPY pyproject.toml README.md ./
COPY src/ src/

# Build wheel
RUN pip install --no-cache-dir build && python -m build --wheel --outdir /build/dist

# ── Stage 2: Runtime ──────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Security: non-root user
RUN groupadd -r ai-company && useradd -r -g ai-company -d /app -s /sbin/nologin ai-company

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install from built wheel (no compiler needed in runtime)
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl

# Copy runtime data (not source — it's in the wheel)
COPY company/ /app/company/
COPY templates/ /app/templates/
COPY docs/ /app/docs/
COPY config/ /app/config/

# Create data directories
RUN mkdir -p /app/.opencode /app/logs /app/memory \
    && chown -R ai-company:ai-company /app

# Switch to non-root
USER ai-company

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8420/health || exit 1

EXPOSE 8420

CMD ["python", "-m", "ai_company.cli.main", "dashboard", "--host", "0.0.0.0", "--port", "8420", "--no-open"]
```

**Key improvements:**
- Multi-stage build: builder has compilers, runtime does not
- Non-root user: security best practice
- Layer caching: pyproject.toml + source cached; data dirs copied separately
- Healthcheck: enables container orchestration to detect failures
- No `.env` copied: secrets injected via runtime env

### 4.4 Versioning Strategy

Use **semantic versioning** with a twist for an AI tool:

```
v1.2.3          # Standard semver
v1.2.3-beta.1   # Pre-release for testing
```

**Version source of truth:** `pyproject.toml` → `version` field. The release workflow reads this from the git tag and validates it matches.

**Changelog generation:** Semi-automated via `git log` between tags + conventional commit prefixes:

```
feat: Add new agent type
fix: Fix task routing for finance queries
docs: Update architecture diagram
chore: Bump dependencies
```

---

## 5. Monitoring & Alerting

### 5.1 Monitoring Architecture

Since this is a CLI tool (not a long-running server), monitoring is split into two domains:

| Domain | What | How |
|--------|------|-----|
| **CI/CD health** | Pipeline failures, test coverage trends | GitHub Actions built-in + codecov |
| **Runtime health** | LLM costs, task completion, errors | Application-level logging → structured JSON |

### 5.2 CI/CD Monitoring

Built into the workflow files above. Additional setup:

```yaml
# .github/workflows/monitor-ci.yml
name: CI Health Report

on:
  schedule:
    - cron: "0 8 * * 1"  # Weekly Monday 8am UTC
  workflow_dispatch:

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate CI health report
        run: |
          # Query GitHub API for workflow run stats
          RUNS=$(gh api repos/${{ github.repository }}/actions/runs \
            --jq '.workflow_runs | map(select(.created_at > (now - 604800 | todate))) | length')
          FAILURES=$(gh api repos/${{ github.repository }}/actions/runs \
            --jq '.workflow_runs | map(select(.conclusion == "failure" and .created_at > (now - 604800 | todate))) | length')
          echo "## CI Health Report" >> "$GITHUB_STEP_SUMMARY"
          echo "- Runs this week: $RUNS" >> "$GITHUB_STEP_SUMMARY"
          echo "- Failures: $FAILURES" >> "$GITHUB_STEP_SUMMARY"
          echo "- Success rate: $(( (RUNS - FAILURES) * 100 / RUNS ))%" >> "$GITHUB_STEP_SUMMARY"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 5.3 Runtime Monitoring Design

For when the tool runs autonomously (orchestrator tick cycles):

#### 5.3.1 Structured Logging

Add to `src/ai_company/`:

```python
# src/ai_company/monitoring/__init__.py
"""Structured logging and metrics collection."""

import json
import time
from pathlib import Path
from typing import Any
from datetime import datetime


class MetricsCollector:
    """Collects and persists runtime metrics as JSON."""

    def __init__(self, log_dir: str = "logs/metrics"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._session_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    def _log_path(self, metric_type: str) -> Path:
        return self.log_dir / f"{metric_type}_{self._session_id}.jsonl"

    def record(self, metric_type: str, data: dict[str, Any]) -> None:
        """Append a metric record to the appropriate log file."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self._session_id,
            **data,
        }
        with open(self._log_path(metric_type), "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def record_llm_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        cost_usd: float,
        success: bool,
    ) -> None:
        self.record(
            "llm_calls",
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_ms": latency_ms,
                "cost_usd": cost_usd,
                "success": success,
            },
        )

    def record_task(
        self,
        task_id: str,
        sender: str,
        receiver: str,
        status: str,
        duration_ms: float,
    ) -> None:
        self.record(
            "tasks",
            {
                "task_id": task_id,
                "sender": sender,
                "receiver": receiver,
                "status": status,
                "duration_ms": duration_ms,
            },
        )

    def record_error(
        self,
        component: str,
        error_type: str,
        message: str,
        recoverable: bool,
    ) -> None:
        self.record(
            "errors",
            {
                "component": component,
                "error_type": error_type,
                "message": message,
                "recoverable": recoverable,
            },
        )

    def record_cycle(
        self,
        cycle_id: str,
        tasks_processed: int,
        tasks_succeeded: int,
        total_cost_usd: float,
        duration_ms: float,
    ) -> None:
        self.record(
            "cycles",
            {
                "cycle_id": cycle_id,
                "tasks_processed": tasks_processed,
                "tasks_succeeded": tasks_succeeded,
                "total_cost_usd": total_cost_usd,
                "duration_ms": duration_ms,
                "success_rate": tasks_succeeded / max(tasks_processed, 1),
            },
        )
```

#### 5.3.2 Metrics to Track

| Category | Metric | Alert Threshold | Action |
|----------|--------|----------------|--------|
| **LLM Costs** | Daily cost (USD) | > $5.00/day | Log warning, notify |
| **LLM Costs** | Monthly cost (USD) | > $100/month | Create issue, pause non-critical cycles |
| **LLM Performance** | Latency p95 | > 30s | Log warning |
| **LLM Performance** | Error rate | > 10% of calls | Fail cycle, create issue |
| **Tasks** | Completion rate | < 80% | Investigate failing agents |
| **Tasks** | Queue depth (inbox.json) | > 50 pending | Check for stuck tasks |
| **System** | Cycle duration | > 25 min | Investigate bottleneck |
| **System** | Memory usage | > 500MB | Check for leaks |
| **System** | Disk usage (.opencode/) | > 1GB | Archive old data |

#### 5.3.3 Health Endpoint

For Docker deployments, expose a simple health endpoint:

```python
# Add to src/ai_company/dashboard/health.py
"""Lightweight health check endpoint for container orchestration."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "version": "0.1.0"}


@router.get("/health/ready")
async def readiness_check() -> dict:
    """Check that all required components are accessible."""
    checks = {}
    # Add checks for: inbox.json exists, config valid, etc.
    return {"status": "ready" if all(checks.values()) else "not_ready", "checks": checks}
```

### 5.4 Alerting Matrix

| Channel | When | Who |
|---------|------|-----|
| GitHub Issue (auto) | CI failure, cycle failure | Team |
| GitHub Issue (auto) | Cost threshold exceeded | CTO + Finance |
| Slack/Webhook | Cycle failure | DevOps Lead |
| Email (via GitHub) | Security scan failure | Security + CTO |

---

## 6. Cost Analysis

### 6.1 GitHub Actions Monthly Cost

| Job | Trigger | Runs/Month | Min/Run | Total Min | Cost ($0.008/min Linux) |
|-----|---------|-----------|---------|-----------|------------------------|
| Lint | PR + push | 40 | 2 | 80 | $0.64 |
| Typecheck | PR + push | 40 | 2 | 80 | $0.64 |
| Test (Ubuntu) | PR + push | 40 | 4 | 160 | $1.28 |
| Test (Windows) | PR + push | 40 | 5 | 200 | $3.20 |
| Security | PR + push | 40 | 3 | 120 | $0.96 |
| Agents | PR + push | 40 | 3 | 120 | $0.96 |
| Docker build | PR + push | 40 | 4 | 160 | $1.28 |
| ECL lint | PR + push | 40 | 2 | 80 | $0.64 |
| **Autonomous** | **Schedule** | **120** | **8** | **960** | **$7.68** |
| **Total** | | | | **1,960** | **~$17/month** |

> **Free tier:** 2,000 min Linux + 3,000 min total (with Windows). We're right at the limit for Linux.  
> **Recommendation:** Enable Windows caching aggressively, or move test matrix to Ubuntu-only initially.

### 6.2 LLM API Cost Estimate (Autonomous Cycles)

| Component | Calls/Day | Tokens/Call | Cost/Day |
|-----------|----------|-------------|----------|
| Task routing | 4 cycles × 5 tasks | ~2K input + 500 output | ~$0.20 |
| Agent coordination | 4 cycles × 3 calls | ~1K + 1K | ~$0.40 |
| Briefing generation | 4 cycles × 1 | ~5K + 2K | ~$0.50 |
| **Daily total** | | | **~$1.10** |
| **Monthly total** | | | **~$33** |

> Using DeepSeek for routine tasks ($0.14/M input, $0.28/M output) keeps costs low.  
> Anthropic/Claude reserved for complex reasoning only.

### 6.3 Total Monthly Infrastructure Cost

| Item | Cost |
|------|------|
| GitHub Actions | ~$17 |
| LLM APIs (autonomous) | ~$33 |
| GitHub storage (artifacts) | ~$1 |
| **Total** | **~$51/month** |

---

## 7. Implementation Roadmap

### Phase 1A: Foundation (This Week)

- [ ] **T001**: Create `.gitignore` — exclude venvs, caches, .env, __pycache__, logs
- [ ] **T002**: Create `.github/workflows/ci.yml` — lint + typecheck + test jobs
- [ ] **T003**: Add security job (bandit) to CI
- [ ] **T004**: Add agent validation job to CI
- [ ] **T005**: Pin dev dependencies in pyproject.toml

### Phase 1B: Enhanced CI (Next Week)

- [ ] **T006**: Add Docker build test job
- [ ] **T007**: Add ECL lint job
- [ ] **T008**: Fix Dockerfile (multi-stage, non-root, healthcheck)
- [ ] **T009**: Set up codecov integration
- [ ] **T010**: Add gitleaks secret scanning

### Phase 5A: Autonomous Execution (Week 3)

- [ ] **T011**: Create `.github/workflows/autonomous.yml`
- [ ] **T012**: Implement `MetricsCollector` in `src/ai_company/monitoring/`
- [ ] **T013**: Add `/health` endpoint to dashboard
- [ ] **T014**: Configure GitHub secrets for LLM API keys
- [ ] **T015**: Test autonomous cycle in staging

### Phase 5B: Release Automation (Week 4)

- [ ] **T016**: Create `.github/workflows/release.yml`
- [ ] **T017**: Set up PyPI trusted publishing
- [ ] **T018**: Set up GHCR for Docker images
- [ ] **T019**: Add semantic versioning enforcement
- [ ] **T020**: Create `CHANGELOG.md` automation

---

## 8. Appendix — Full Config Files

### 8.1 `.gitignore` (to create)

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
*.egg
.eggs/

# Virtual environments
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
coverage.xml

# Type checking
.mypy_cache/

# Linting
.ruff_cache/

# Environment & secrets
.env
.env.*
!.env.example

# Runtime data
logs/
.opencode/inbox.json
.opencode/cycle-state.json
orchestrator/scheduler.yaml

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml
```

### 8.2 `requirements-dev.txt` (for CI caching)

```
# Generated from pyproject.toml dev dependencies
# Pin these for reproducible CI
pytest>=8.0,<9
pytest-cov>=5.0,<6
ruff>=0.5,<1
mypy>=1.10,<2
types-PyYAML>=6.0,<7
bandit>=1.7,<2
safety>=3.0,<4
```

### 8.3 Docker Compose for local development

```yaml
# docker-compose.dev.yml — extends base for local dev
services:
  dashboard:
    build:
      context: .
      target: builder  # Use builder stage for hot reload
    command: ["python", "-m", "ai_company.cli.main", "dashboard", "--host", "0.0.0.0", "--port", "8420", "--no-open", "--reload"]
    volumes:
      - ./src:/app/src
      - ./.opencode:/app/.opencode
      - ./company:/app/company
      - ./config:/app/config
      - ./templates:/app/templates
    environment:
      - OPENCODE_API_KEY=${OPENCODE_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    ports:
      - "8420:8420"

  worker:
    build:
      context: .
      target: builder
    command: ["python", "-m", "ai_company.cli.main", "orchestrator", "tick", "--verbose"]
    volumes:
      - ./src:/app/src
      - ./.opencode:/app/.opencode
      - ./company:/app/company
    environment:
      - OPENCODE_API_KEY=${OPENCODE_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    profiles:
      - worker

  test:
    build:
      context: .
      target: builder
    command: ["pytest", "--tb=short", "-q"]
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
    profiles:
      - test
```

---

## Decision Log

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| `actions/cache` for state persistence | Avoids git commit noise; fast restore | Git commits (noisy), S3 (overkill) |
| Non-cancel for autonomous cycles | State corruption risk on interruption | Cancel-in-progress (dangerous) |
| Multi-stage Docker build | Smaller image, better security | Single-stage (current, broken) |
| ruff over black | Faster, same output, single tool | Keep both (redundant) |
| Structured JSON logs | Machine-parseable for future dashboards | Plain text (hard to query) |
| Advisory security scanning | Don't block CI until deps are pinned | Fail-hard (premature) |

---

**Next steps:** Awaiting CTO review of this plan. Once approved, I'll create the CI workflow files and `.gitignore` as the first implementation task.
