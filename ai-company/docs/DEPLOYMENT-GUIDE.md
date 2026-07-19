# Deployment Guide

Complete deployment reference for AI Company Builder — from local development to production.

---

## Table of Contents

1. [Local Development Setup](#1-local-development-setup)
2. [Docker Deployment](#2-docker-deployment)
3. [Production Deployment](#3-production-deployment)
4. [Environment Variables](#4-environment-variables)
5. [CI/CD Pipeline](#5-cicd-pipeline)
6. [Security Considerations](#6-security-considerations)
7. [Monitoring & Operations](#7-monitoring--operations)
8. [Release Process](#8-release-process)

---

## 1. Local Development Setup

### Prerequisites

- Python 3.12+
- Git
- An LLM API key (at least one provider)

### Installation

```bash
# Clone the repository
git clone https://github.com/light-speed-holdings/ai-company.git
cd ai-company

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Bootstrap the Company

```bash
# Generate all agent files, configs, and directory structure
ai-company company run

# Verify the bootstrap
ai-company agents list
ai-company doctor
```

### Configure LLM Providers

Create a `.env` file at the project root:

```bash
# Required: at least one provider
OPENCODE_API_KEY=your-opencode-key
DEEPSEEK_API_KEY=your-deepseek-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Optional: Ollama for local inference (no key needed)
# Ensure Ollama is running on localhost:11434
```

### Start the Dashboard

```bash
ai-company dashboard --port 8420
```

Opens `http://localhost:8420` in your browser.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_company --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_models.py

# Run tests matching a pattern
pytest -k "postmortem"
```

### Code Quality Checks

```bash
ruff check src/           # Lint
ruff format src/          # Format
mypy src/                 # Type check
```

Or use the Makefile shortcuts:

```bash
make all-checks           # Lint + typecheck + test
make lint                 # Lint only
make test                 # Tests only
make format               # Format only
```

---

## 2. Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (layer caching)
COPY pyproject.toml README.md ./
COPY src/ src/

# Install the package
RUN pip install --no-cache-dir .

# Copy configuration and templates
COPY company/ company/
COPY templates/ templates/

# Create necessary directories
RUN mkdir -p .opencode/agents .opencode/config orchestrator/postmortems

# Expose dashboard port
EXPOSE 8420

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8420/health').raise_for_status()"

# Default command: start the dashboard
CMD ["ai-company", "dashboard", "--host", "0.0.0.0", "--port", "8420", "--no-open"]
```

### Docker Build & Run

```bash
# Build the image
docker build -t ai-company:latest .

# Run the dashboard
docker run -d \
  --name ai-company-dashboard \
  -p 8420:8420 \
  -e OPENCODE_API_KEY=your-key \
  -e DEEPSEEK_API_KEY=your-key \
  -v $(pwd)/company:/app/company \
  -v $(pwd)/.opencode:/app/.opencode \
  ai-company:latest

# Run the orchestrator (one-shot)
docker run --rm \
  -e OPENCODE_API_KEY=your-key \
  -v $(pwd)/company:/app/company \
  -v $(pwd)/.opencode:/app/.opencode \
  ai-company:latest \
  ai-company orchestrator tick

# Run the executor (one-shot)
docker run --rm \
  -e OPENCODE_API_KEY=your-key \
  -v $(pwd)/company:/app/company \
  -v $(pwd)/.opencode:/app/.opencode \
  ai-company:latest \
  ai-company executor tick
```

### Docker Compose

```yaml
version: "3.8"

services:
  dashboard:
    build: .
    ports:
      - "8420:8420"
    environment:
      - OPENCODE_API_KEY=${OPENCODE_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./company:/app/company
      - ./.opencode:/app/.opencode
      - ./orchestrator:/app/orchestrator
    healthcheck:
      test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:8420/health').raise_for_status()"]
      interval: 30s
      timeout: 5s
      retries: 3

  orchestrator:
    build: .
    command: ai-company orchestrator tick
    environment:
      - OPENCODE_API_KEY=${OPENCODE_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    volumes:
      - ./company:/app/company
      - ./.opencode:/app/.opencode
      - ./orchestrator:/app/orchestrator
    profiles:
      - cron

  executor:
    build: .
    command: ai-company executor tick
    environment:
      - OPENCODE_API_KEY=${OPENCODE_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    volumes:
      - ./company:/app/company
      - ./.opencode:/app/.opencode
      - ./orchestrator:/app/orchestrator
    profiles:
      - cron
```

```bash
# Start dashboard
docker compose up -d dashboard

# Run orchestrator + executor once
docker compose run --rm orchestrator
docker compose run --rm executor

# View logs
docker compose logs -f dashboard
```

---

## 3. Production Deployment

### System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 1 vCPU | 2+ vCPU |
| Memory | 1 GB | 2+ GB |
| Disk | 5 GB | 10+ GB |
| Python | 3.12+ | 3.12+ |
| OS | Linux (Ubuntu 22.04+) | Linux |

### Production Checklist

- [ ] Set all API keys as environment variables (not in `.env` files)
- [ ] Configure CORS to allow only your dashboard domain
- [ ] Set up a reverse proxy (nginx/Caddy) with TLS
- [ ] Configure log rotation
- [ ] Set up monitoring and alerting
- [ ] Run database backups (if using persistent storage)
- [ ] Configure firewall rules
- [ ] Review and restrict file permissions

### Systemd Service

Create `/etc/systemd/system/ai-company-dashboard.service`:

```ini
[Unit]
Description=AI Company Builder Dashboard
After=network.target

[Service]
Type=simple
User=ai-company
Group=ai-company
WorkingDirectory=/opt/ai-company
Environment=PATH=/opt/ai-company/.venv/bin
ExecStart=/opt/ai-company/.venv/bin/ai-company dashboard --host 0.0.0.0 --port 8420 --no-open
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/ai-company/.opencode /opt/ai-company/orchestrator
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ai-company-dashboard
sudo systemctl start ai-company-dashboard

# View logs
sudo journalctl -u ai-company-dashboard -f
```

### Systemd Timer for Orchestrator/Executor

Create `/etc/systemd/system/ai-company-orchestrator.service`:

```ini
[Unit]
Description=AI Company Builder Orchestrator Tick
After=network.target

[Service]
Type=oneshot
User=ai-company
Group=ai-company
WorkingDirectory=/opt/ai-company
Environment=PATH=/opt/ai-company/.venv/bin
ExecStart=/opt/ai-company/.venv/bin/ai-company orchestrator tick
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/ai-company-orchestrator.timer`:

```ini
[Unit]
Description=Run orchestrator every 6 hours

[Timer]
OnCalendar=*-*-* 00/6:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-company-orchestrator.timer
sudo systemctl start ai-company-orchestrator.timer
```

### Nginx Reverse Proxy

```nginx
server {
    listen 443 ssl http2;
    server_name dashboard.yourcompany.com;

    ssl_certificate /etc/letsencrypt/live/dashboard.yourcompany.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dashboard.yourcompany.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8420;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # WebSocket support
    location /ws/dashboard {
        proxy_pass http://127.0.0.1:8420;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}

server {
    listen 80;
    server_name dashboard.yourcompany.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 4. Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENCODE_API_KEY` | OpenCode LLM provider key | `oc-xxxxx` |
| `DEEPSEEK_API_KEY` | DeepSeek API key | `sk-xxxxx` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-xxxxx` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-xxxxx` |

At least one provider key is required. Ollama works locally without a key.

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_COMPANY_PORT` | `8420` | Dashboard port |
| `AI_COMPANY_HOST` | `127.0.0.1` | Dashboard bind address |
| `AI_COMPANY_CONFIG_DIR` | `config` | Configuration directory path |
| `AI_COMPANY_OUTPUT_DIR` | `.opencode` | Output directory for generated files |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

---

## 5. CI/CD Pipeline

### GitHub Actions CI

The CI pipeline runs on every push and PR to `main`:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ruff check src/
      - run: mypy src/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: pytest --cov=ai_company --cov-report=xml

  harness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: pwsh scripts/lint-ecl.ps1
```

### GitHub Actions Autonomous Cycle

Runs the orchestrator and executor every 6 hours automatically:

```yaml
# .github/workflows/autonomous.yml
name: Autonomous Cycle

on:
  schedule:
    - cron: "0 */6 * * *"  # Every 6 hours
  workflow_dispatch:  # Manual trigger

jobs:
  orchestrator:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ai-company orchestrator tick
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}

  executor:
    needs: orchestrator
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ai-company executor tick
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
```

### Release Pipeline

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build
      - run: python -m build
      - uses: softprops/action-gh-release@v2
        with:
          files: dist/*
```

---

## 6. Security Considerations

### API Keys

- **Never commit API keys** to version control
- Use environment variables or a secrets manager
- Rotate keys regularly
- Use the minimum required permissions for each key

### Dashboard Access

- The dashboard API has **no authentication** by default
- For production, implement authentication middleware:

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY = "your-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Add to routes:
@router.get("/api/dashboard", dependencies=[Depends(verify_api_key)])
def get_dashboard():
    ...
```

### CORS

The dashboard allows all origins by default (`*`). Restrict in production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dashboard.yourcompany.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### File Permissions

```bash
# Restrict config directory
chmod 700 company/
chmod 600 company/*.yaml company/*.json

# Restrict orchestrator data
chmod 700 orchestrator/
chmod 600 orchestrator/*.yaml

# Restrict task inbox
chmod 600 .opencode/inbox.json
```

### Network Security

- Use TLS for all production endpoints
- Implement rate limiting on API endpoints
- Use a WAF (Web Application Firewall) in front of the dashboard
- Restrict dashboard access to internal network or VPN

### LLM Security

- Review LLM-generated content before executing sensitive actions
- Use the HITL (Human-in-the-Loop) approval gates for critical operations
- Monitor LLM usage and costs via the model routing system
- Set up alerts for unusual patterns

---

## 7. Monitoring & Operations

### Health Monitoring

```bash
# Check dashboard health
curl http://localhost:8420/health

# Response:
# {"status": "ok", "service": "ceo-dashboard"}
```

### Key Metrics to Monitor

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Dashboard uptime | `/api/dashboard` | Any downtime |
| Pending tasks | `/api/dashboard` | > 20 pending |
| Failed tasks | `/api/dashboard` | > 5 failed |
| Open escalations | `/api/dashboard` | > 3 open |
| Pending approvals | `/api/dashboard` | > 5 pending |
| LLM API errors | Logs | > 10 errors/hour |
| WebSocket connections | `/ws/dashboard` | Connection failures |

### Log Monitoring

```bash
# Dashboard logs (systemd)
sudo journalctl -u ai-company-dashboard -f

# Filter by level
sudo journalctl -u ai-company-dashboard -p err

# Last 100 lines
sudo journalctl -u ai-company-dashboard -n 100
```

### Backup Strategy

| What | Location | Frequency |
|------|----------|-----------|
| Agent registry | `company/agent-registry.json` | Daily |
| Task inbox | `.opencode/inbox.json` | Every 6 hours |
| Approval requests | `orchestrator/approvals.yaml` | Every 6 hours |
| Escalation events | `orchestrator/escalation.yaml` | Every 6 hours |
| Scheduled tasks | `orchestrator/scheduler.yaml` | Daily |
| Postmortems | `orchestrator/postmortems/` | Daily |
| Memory store | `memory/` | Daily |
| Config files | `company/` | On change |

```bash
# Example backup script
#!/bin/bash
BACKUP_DIR="/backups/ai-company/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
cp -r company/ "$BACKUP_DIR/"
cp -r .opencode/ "$BACKUP_DIR/"
cp -r orchestrator/ "$BACKUP_DIR/"
cp -r memory/ "$BACKUP_DIR/"
```

---

## 8. Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Update CHANGELOG.md:**
   ```bash
   # Add new section under [Unreleased]
   # Move items to new version section
   ```

2. **Update version in pyproject.toml:**
   ```toml
   version = "0.3.0"
   ```

3. **Create release branch and tag:**
   ```bash
   git checkout -b release/v0.3.0
   git commit -am "chore: release v0.3.0"
   git tag v0.3.0
   git push origin v0.3.0
   ```

4. **Build and verify:**
   ```bash
   python -m build
   twine check dist/*
   ```

5. **Run release script:**
   ```bash
   # Windows
   powershell -File scripts/release.ps1 -Version 0.3.0

   # Linux/macOS
   ./scripts/release.sh 0.3.0
   ```

6. **GitHub Actions will:**
   - Create a GitHub Release
   - Upload built artifacts
   - Tag the release

### Release Script

```powershell
# scripts/release.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

Write-Host "Releasing AI Company Builder v$Version" -ForegroundColor Cyan

# 1. Run all checks
Write-Host "`nRunning checks..." -ForegroundColor Yellow
ruff check src/
mypy src/
pytest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Checks failed. Aborting release." -ForegroundColor Red
    exit 1
}

# 2. Build
Write-Host "`nBuilding..." -ForegroundColor Yellow
python -m build

# 3. Tag and push
Write-Host "`nTagging..." -ForegroundColor Yellow
git tag "v$Version"
git push origin "v$Version"

Write-Host "`nRelease v$Version initiated!" -ForegroundColor Green
Write-Host "GitHub Actions will create the release automatically." -ForegroundColor Green
```
