FROM python:3.12-slim AS base

WORKDIR /app

# Install uv (package manager) from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps from the lockfile (layer cached on pyproject/uv.lock changes)
COPY pyproject.toml uv.lock README.md ./
COPY src/ src/
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

# Copy runtime data
COPY company/ company/
COPY templates/ templates/
COPY docs/ docs/
COPY .opencode/ .opencode/

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose dashboard port
EXPOSE 8420

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8420/health || exit 1

# Default: start the dashboard
CMD ["python", "-m", "ai_company.cli.main", "dashboard", "--host", "0.0.0.0", "--port", "8420", "--no-open"]
