# Makefile for Dagster Snowflake dbt Demo

.PHONY: help install setup dev build test clean deploy

help: ## Show this help message
	@echo "Dagster Snowflake dbt Demo - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
	pip install -e .

setup: ## Run complete project setup
	python setup.py

dev: ## Start Dagster development server with dg CLI
	dg dev

build: ## Build dbt models and Docker image
	cd dbt_project && dbt deps && dbt parse
	docker build -t dagster-snowflake-demo .

test: ## Run tests and validations
	dg dev --dry-run
	python -c "from dagster_snowflake_dbt_demo import defs; print('✅ Project loads successfully')"
	cd dbt_project && dbt compile

clean: ## Clean build artifacts
	rm -rf dbt_project/target/
	rm -rf dbt_project/dbt_packages/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

deploy-check: ## Validate deployment configuration
	@echo "Checking deployment readiness..."
	@test -f dagster_cloud.yaml || (echo "❌ dagster_cloud.yaml missing" && exit 1)
	@test -f Dockerfile || (echo "❌ Dockerfile missing" && exit 1)
	@test -f pyproject.toml || (echo "❌ pyproject.toml missing" && exit 1)
	@echo "✅ Deployment files present"

quick-start: install setup ## Complete quick start setup
	@echo ""
	@echo "🎉 Quick start complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env with your Snowflake credentials"
	@echo "2. Run: make dev (uses dg CLI)"
	@echo "3. Open http://localhost:3000"

# Default target
all: quick-start
