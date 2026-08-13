# Multi-stage Dockerfile for ai-company
# Stage 1: Builder - installs dependencies and compiles
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv (package manager) from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files needed for dependency installation
COPY pyproject.toml uv.lock README.md ./
COPY src/ src/

# Install Python dependencies (production only, frozen from lockfile)
RUN uv sync --frozen --no-dev

# Stage 2: Runtime - minimal image with only runtime dependencies
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install runtime system dependencies (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy runtime application code and data
COPY --chown=appuser:appuser config/ config/
COPY --chown=appuser:appuser templates/ templates/
COPY --chown=appuser:appuser company/ company/
COPY --chown=appuser:appuser docs/ docs/
COPY --chown=appuser:appuser .opencode/ .opencode/
COPY --chown=appuser:appuser scripts/ scripts/
COPY --chown=appuser:appuser src/ src/

USER appuser

# Expose dashboard port
EXPOSE 8420

# Health check - uses the /health endpoint from monitoring router
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8420/health || exit 1

# Default: start the dashboard
CMD ["python", "-m", "ai_company.cli.main", "dashboard", "--host", "0.0.0.0", "--port", "8420", "--no-open"]
