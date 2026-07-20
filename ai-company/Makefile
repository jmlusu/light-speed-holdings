.PHONY: help install test test-cov test-bench lint format typecheck all-checks generate doctor clean backup lock staging-up staging-down

## Default target
help: ## Show available targets
	@echo "AI Company Builder — Available Targets"
	@echo "======================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## pip install -e ".[dev]"
	pip install -e ".[dev]"

test: ## Run all tests
	pytest

test-cov: ## Run tests with coverage report
	pytest --cov=ai_company --cov-report=term-missing

test-bench: ## Run performance benchmarks (pytest-benchmark)
	pytest tests/benchmarks/ -v --benchmark-only --benchmark-autosave

test-bench-compare: ## Compare benchmarks against saved baseline
	pytest tests/benchmarks/ -v --benchmark-compare=0.001

lint: ## Lint source with ruff
	ruff check src/

format: ## Format source with ruff
	ruff format src/

typecheck: ## Type-check source with mypy
	mypy src/

all-checks: lint typecheck test ## Run lint + typecheck + test in sequence

generate: ## Regenerate agent files from registry
	python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"

doctor: ## Run system diagnostics
	ai-company doctor run

backup: ## Run backup script (creates timestamped archives)
	powershell -ExecutionPolicy Bypass -File scripts/backup.ps1

backup-dry: ## Preview backup without creating archives
	powershell -ExecutionPolicy Bypass -File scripts/backup.ps1 -DryRun

lock: ## Generate dependency lock file
	.venv/Scripts/pip freeze > requirements.lock

staging-up: ## Start staging environment (docker compose)
	docker compose -f docker-compose.staging.yml --profile staging up -d

staging-down: ## Stop staging environment
	docker compose -f docker-compose.staging.yml --profile staging down

staging-logs: ## Tail staging logs
	docker compose -f docker-compose.staging.yml --profile staging logs -f

clean: ## Remove build artifacts and caches
	@echo "Cleaning __pycache__ directories..."
	@find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "Removing .egg-info directories..."
	@find . -type d -name "*.egg-info" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "Removing build/ and dist/..."
	@rm -rf build/ dist/
	@echo "Clean complete."
