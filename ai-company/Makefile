.PHONY: help install test test-cov lint format typecheck all-checks generate doctor clean

## Default target
help: ## Show available targets
	@echo "AI Company Builder — Available Targets"
	@echo "======================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## pip install -e ".[dev]"
	pip install -e ".[dev]"

test: ## Run all tests
	pytest

test-cov: ## Run tests with coverage report
	pytest --cov=ai_company --cov-report=term-missing

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

clean: ## Remove build artifacts and caches
	@echo "Cleaning __pycache__ directories..."
	@find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "Removing .egg-info directories..."
	@find . -type d -name "*.egg-info" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "Removing build/ and dist/..."
	@rm -rf build/ dist/
	@echo "Clean complete."
