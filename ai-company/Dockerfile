FROM python:3.12-slim AS base

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy source
COPY src/ src/
COPY company/ company/
COPY templates/ templates/
COPY docs/ docs/

# Expose dashboard port
EXPOSE 8420

# Default: start the dashboard
CMD ["python", "-m", "ai_company.cli.main", "dashboard", "--host", "0.0.0.0", "--port", "8420", "--no-open"]
