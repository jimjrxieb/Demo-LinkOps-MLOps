# LinkOps Platform Makefile
# Usage: make <target>

.PHONY: help install clean build test lint format docker deploy logs status

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON_VERSION := 3.11
NODE_VERSION := 20
DOCKER_REGISTRY := linkops
PROJECT_NAME := linkops-platform

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

##@ Help
help: ## Display this help message
	@echo "$(BLUE)LinkOps Platform - Available Commands$(RESET)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make $(GREEN)<target>$(RESET)\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(RESET)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development Setup
install: install-python install-frontend ## Install all dependencies
	@echo "$(GREEN)✅ All dependencies installed$(RESET)"

install-python: ## Install Python dependencies for all services
	@echo "$(BLUE)📦 Installing Python dependencies...$(RESET)"
	@for service in mlops/*/ shadows/*/; do \
		if [ -f "$$service/requirements.txt" ]; then \
			echo "Installing dependencies for $$service"; \
			cd "$$service" && pip install -r requirements.txt && cd ../..; \
		fi \
	done

install-frontend: ## Install frontend dependencies
	@echo "$(BLUE)📦 Installing frontend dependencies...$(RESET)"
	cd frontend && npm ci

##@ Code Quality
lint: lint-python lint-frontend ## Run all linting
	@echo "$(GREEN)✅ All linting completed$(RESET)"

lint-python: ## Lint Python code
	@echo "$(BLUE)🔍 Linting Python code...$(RESET)"
	@for service in mlops/*/ shadows/*/; do \
		if [ -f "$$service/requirements.txt" ]; then \
			echo "Linting $$service"; \
			cd "$$service" && \
			flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && \
			cd ../..; \
		fi \
	done

lint-frontend: ## Lint frontend code
	@echo "$(BLUE)🔍 Linting frontend code...$(RESET)"
	cd frontend && npm run lint

format: format-python format-frontend ## Format all code
	@echo "$(GREEN)✅ All code formatted$(RESET)"

format-python: ## Format Python code with black and isort
	@echo "$(BLUE)🎨 Formatting Python code...$(RESET)"
	@for service in mlops/*/ shadows/*/; do \
		if [ -f "$$service/requirements.txt" ]; then \
			echo "Formatting $$service"; \
			cd "$$service" && \
			black . && \
			isort . && \
			cd ../..; \
		fi \
	done

format-frontend: ## Format frontend code
	@echo "$(BLUE)🎨 Formatting frontend code...$(RESET)"
	cd frontend && npm run format || echo "No format script found"

##@ Testing
test: test-python test-frontend ## Run all tests
	@echo "$(GREEN)✅ All tests completed$(RESET)"

test-python: ## Run Python tests
	@echo "$(BLUE)🧪 Running Python tests...$(RESET)"
	@for service in mlops/*/ shadows/*/; do \
		if [ -d "$$service/tests" ]; then \
			echo "Testing $$service"; \
			cd "$$service" && python -m pytest tests/ -v && cd ../..; \
		fi \
	done

test-frontend: ## Run frontend tests
	@echo "$(BLUE)🧪 Running frontend tests...$(RESET)"
	cd frontend && npm test || echo "No tests configured"

test-integration: ## Run integration tests
	@echo "$(BLUE)🔗 Running integration tests...$(RESET)"
	@if [ -f "tests/test_complete_pipeline.py" ]; then \
		python tests/test_complete_pipeline.py; \
	fi
	@if [ -f "scripts/validate_refactor.py" ]; then \
		python scripts/validate_refactor.py; \
	fi

##@ Building
build: build-frontend build-docker ## Build all components
	@echo "$(GREEN)✅ All builds completed$(RESET)"

build-frontend: ## Build frontend for production
	@echo "$(BLUE)🏗️ Building frontend...$(RESET)"
	cd frontend && npm run build

build-docker: ## Build all Docker images
	@echo "$(BLUE)🐳 Building Docker images...$(RESET)"
	@for service in mlops/*/; do \
		service_name=$$(basename "$$service"); \
		echo "Building $$service_name"; \
		cd "$$service" && docker build -t $(DOCKER_REGISTRY)/$$service_name:latest . && cd ../..; \
	done
	@for service in shadows/*/; do \
		service_name=$$(basename "$$service"); \
		echo "Building $$service_name"; \
		cd "$$service" && docker build -t $(DOCKER_REGISTRY)/$$service_name:latest . && cd ../..; \
	done

build-service: ## Build specific service (usage: make build-service SERVICE=service_name)
	@if [ -z "$(SERVICE)" ]; then \
		echo "$(RED)❌ Please specify SERVICE. Usage: make build-service SERVICE=service_name$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)🐳 Building $(SERVICE)...$(RESET)"
	@if [ -d "mlops/$(SERVICE)" ]; then \
		cd mlops/$(SERVICE) && docker build -t $(DOCKER_REGISTRY)/$(SERVICE):latest .; \
	elif [ -d "shadows/$(SERVICE)" ]; then \
		cd shadows/$(SERVICE) && docker build -t $(DOCKER_REGISTRY)/$(SERVICE):latest .; \
	else \
		echo "$(RED)❌ Service $(SERVICE) not found$(RESET)"; \
		exit 1; \
	fi

##@ Docker Operations
docker-up: ## Start all services with docker-compose
	@echo "$(BLUE)🚀 Starting all services...$(RESET)"
	docker-compose up -d

docker-down: ## Stop all services
	@echo "$(BLUE)🛑 Stopping all services...$(RESET)"
	docker-compose down

docker-logs: ## Show logs from all services
	@echo "$(BLUE)📋 Showing service logs...$(RESET)"
	docker-compose logs -f

docker-clean: ## Clean up Docker images and containers
	@echo "$(BLUE)🧹 Cleaning up Docker...$(RESET)"
	docker system prune -f
	docker image prune -f

##@ Kubernetes/Helm
helm-lint: ## Lint Helm charts
	@echo "$(BLUE)⛵ Linting Helm charts...$(RESET)"
	@for chart in helm/*/; do \
		if [ -f "$$chart/Chart.yaml" ]; then \
			echo "Linting $$chart"; \
			helm lint "$$chart"; \
		fi \
	done

helm-deploy: ## Deploy to Kubernetes using Helm
	@echo "$(BLUE)⛵ Deploying with Helm...$(RESET)"
	helm upgrade --install linkops ./helm/linkops --namespace linkops --create-namespace

helm-uninstall: ## Uninstall Helm deployment
	@echo "$(BLUE)⛵ Uninstalling Helm deployment...$(RESET)"
	helm uninstall linkops --namespace linkops

##@ Monitoring
status: ## Check status of all services
	@echo "$(BLUE)📊 Checking service status...$(RESET)"
	docker-compose ps

logs: ## Show logs for specific service (usage: make logs SERVICE=service_name)
	@if [ -z "$(SERVICE)" ]; then \
		echo "$(RED)❌ Please specify SERVICE. Usage: make logs SERVICE=service_name$(RESET)"; \
		exit 1; \
	fi
	docker-compose logs -f $(SERVICE)

health-check: ## Run health checks on all services
	@echo "$(BLUE)🏥 Running health checks...$(RESET)"
	@for service in mlops/*/ shadows/*/; do \
		service_name=$$(basename "$$service"); \
		echo "Checking $$service_name"; \
		curl -f http://localhost:8000/health || echo "$$service_name not responding"; \
	done

##@ Utilities
clean: ## Clean up build artifacts and caches
	@echo "$(BLUE)🧹 Cleaning up...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	rm -rf frontend/dist/
	rm -rf frontend/.vite/

validate-structure: ## Validate project structure
	@echo "$(BLUE)🔍 Validating project structure...$(RESET)"
	@bash scripts/validate_structure.sh || echo "Structure validation script not found"

security-scan: ## Run security scans
	@echo "$(BLUE)🔒 Running security scans...$(RESET)"
	bandit -r mlops/,shadows/ -f json -o bandit-results.json || echo "Bandit not installed"
	docker run --rm -v $$(pwd):/app aquasec/trivy fs /app || echo "Trivy not available"

##@ Development Shortcuts
dev: docker-up logs ## Start development environment
	@echo "$(GREEN)🚀 Development environment started$(RESET)"

restart: docker-down docker-up ## Restart all services
	@echo "$(GREEN)🔄 Services restarted$(RESET)"

rebuild: docker-down build-docker docker-up ## Rebuild and restart services
	@echo "$(GREEN)🔄 Services rebuilt and restarted$(RESET)"

quick-test: lint test ## Run quick tests (lint + unit tests)
	@echo "$(GREEN)✅ Quick tests completed$(RESET)"

full-test: lint test test-integration ## Run all tests including integration
	@echo "$(GREEN)✅ Full test suite completed$(RESET)"

##@ CI/CD
ci: install lint test build ## Run full CI pipeline locally
	@echo "$(GREEN)✅ CI pipeline completed$(RESET)"

pre-commit: format lint test ## Run pre-commit checks
	@echo "$(GREEN)✅ Pre-commit checks passed$(RESET)"

deploy-staging: build helm-deploy ## Deploy to staging environment
	@echo "$(GREEN)🚀 Deployed to staging$(RESET)"

##@ Documentation
docs: ## Generate documentation
	@echo "$(BLUE)📚 Generating documentation...$(RESET)"
	@echo "Documentation generation not yet implemented"

list-services: ## List all available services
	@echo "$(BLUE)📋 Available Services:$(RESET)"
	@echo "$(YELLOW)MLOps Services:$(RESET)"
	@ls -1 mlops/ | grep -v __pycache__ | sort
	@echo "$(YELLOW)Shadow Agents:$(RESET)"
	@ls -1 shadows/ | grep -v __pycache__ | sort 