#!/bin/bash
# =============================================================================
# Automated Formatting and Linting Script for DEMO-LinkOps
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 DEMO-LinkOps Formatting and Linting Script${NC}"
echo "================================================="

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]] || [[ ! -d "frontend" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the DEMO-LinkOps root directory${NC}"
    exit 1
fi

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}📋 $1${NC}"
    echo "----------------------------------------"
}

# Function to run command with error handling
run_command() {
    local desc="$1"
    local cmd="$2"
    local allow_fail="${3:-false}"
    
    echo -e "${YELLOW}🔄 $desc...${NC}"
    
    if eval "$cmd"; then
        echo -e "${GREEN}✅ $desc completed${NC}"
        return 0
    else
        if [[ "$allow_fail" == "true" ]]; then
            echo -e "${YELLOW}⚠️  $desc completed with warnings${NC}"
            return 0
        else
            echo -e "${RED}❌ $desc failed${NC}"
            return 1
        fi
    fi
}

# =============================================================================
# PYTHON FORMATTING AND LINTING
# =============================================================================

print_section "Python Code Formatting & Linting"

if command -v ruff &> /dev/null; then
    # Format Python code
    run_command "Formatting Python code" \
        "ruff format unified-api/ rag/ ml-models/ pipeline/ sync_engine/ htc/ scripts/ *.py" \
        true
    
    # Lint Python code with auto-fix
    run_command "Linting Python code (auto-fix)" \
        "ruff check unified-api/ rag/ ml-models/ pipeline/ sync_engine/ htc/ scripts/ *.py --fix" \
        true
    
    # Show remaining issues
    echo -e "${YELLOW}📊 Remaining Python linting issues:${NC}"
    ruff check unified-api/ rag/ ml-models/ pipeline/ sync_engine/ htc/ scripts/ *.py || true
else
    echo -e "${RED}❌ Ruff not found. Install with: pip install ruff${NC}"
fi

# =============================================================================
# FRONTEND FORMATTING AND LINTING
# =============================================================================

print_section "Frontend Code Formatting & Linting"

cd frontend

if [[ -f "package.json" ]]; then
    # Check if dependencies are installed
    if [[ ! -d "node_modules" ]]; then
        run_command "Installing frontend dependencies" "npm install"
    fi
    
    # Format with Prettier
    run_command "Formatting frontend code with Prettier" "npm run format" true
    
    # Lint with ESLint (auto-fix)
    run_command "Linting frontend code with ESLint (auto-fix)" "npm run lint:fix" true
    
    # Show remaining issues
    echo -e "${YELLOW}📊 Remaining frontend linting issues:${NC}"
    npm run lint || true
    
else
    echo -e "${RED}❌ package.json not found in frontend directory${NC}"
fi

cd ..

# =============================================================================
# DOCKER & KUBERNETES CONFIG VALIDATION
# =============================================================================

print_section "Docker & Kubernetes Config Validation"

# Validate docker-compose files
if command -v docker-compose &> /dev/null; then
    run_command "Validating docker-compose.yml" "docker-compose config --quiet" true
else
    echo -e "${YELLOW}⚠️  docker-compose not found, skipping validation${NC}"
fi

# Validate Kubernetes manifests
if command -v kubectl &> /dev/null; then
    run_command "Validating Kubernetes manifests" "kubectl apply --dry-run=client -f k8s/ > /dev/null" true
else
    echo -e "${YELLOW}⚠️  kubectl not found, skipping K8s validation${NC}"
fi

# =============================================================================
# SUMMARY
# =============================================================================

print_section "Summary"

echo -e "${GREEN}✅ Formatting and linting process completed!${NC}"
echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo "1. Review any remaining linting issues above"
echo "2. Fix critical errors manually if needed"
echo "3. Run tests to ensure code still works: npm test (frontend) or pytest (Python)"
echo "4. Commit your changes: git add . && git commit -m 'chore: format and lint code'"
echo ""
echo -e "${YELLOW}💡 Tip: Run this script regularly to maintain code quality!${NC}"