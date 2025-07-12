#!/bin/bash

# LinkOps Demo Helm Chart Test Script
# This script validates the Helm charts without deploying

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 LinkOps Demo Helm Chart Testing${NC}"
echo "====================================="

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm is not installed. Please install Helm first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Helm is installed${NC}"

# Test individual charts
CHARTS=("whis_data_input" "whis_sanitize" "whis_logic" "frontend")

for chart in "${CHARTS[@]}"; do
    echo -e "${YELLOW}🔍 Testing chart: ${chart}${NC}"
    
    if [ -d "helm/${chart}" ]; then
        # Lint the chart
        if helm lint "helm/${chart}"; then
            echo -e "${GREEN}✅ ${chart} chart is valid${NC}"
        else
            echo -e "${RED}❌ ${chart} chart has issues${NC}"
            exit 1
        fi
        
        # Template the chart
        if helm template test-release "helm/${chart}" > /dev/null; then
            echo -e "${GREEN}✅ ${chart} templates render successfully${NC}"
        else
            echo -e "${RED}❌ ${chart} templates failed to render${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Chart directory not found: helm/${chart}${NC}"
        exit 1
    fi
done

# Test the umbrella chart
echo -e "${YELLOW}🔍 Testing umbrella chart: demo-stack${NC}"

if [ -d "helm/demo-stack" ]; then
    # Update dependencies
    cd helm/demo-stack
    if helm dependency update; then
        echo -e "${GREEN}✅ Dependencies updated successfully${NC}"
    else
        echo -e "${RED}❌ Failed to update dependencies${NC}"
        exit 1
    fi
    cd - > /dev/null
    
    # Lint the umbrella chart
    if helm lint "helm/demo-stack"; then
        echo -e "${GREEN}✅ demo-stack chart is valid${NC}"
    else
        echo -e "${RED}❌ demo-stack chart has issues${NC}"
        exit 1
    fi
    
    # Template the umbrella chart
    if helm template test-release "helm/demo-stack" > /dev/null; then
        echo -e "${GREEN}✅ demo-stack templates render successfully${NC}"
    else
        echo -e "${RED}❌ demo-stack templates failed to render${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Umbrella chart directory not found: helm/demo-stack${NC}"
    exit 1
fi

# Test ArgoCD Application manifest
echo -e "${YELLOW}🔍 Testing ArgoCD Application manifest${NC}"

if [ -f "helm/argocd/Application.yaml" ]; then
    if kubectl apply --dry-run=client -f "helm/argocd/Application.yaml"; then
        echo -e "${GREEN}✅ ArgoCD Application manifest is valid${NC}"
    else
        echo -e "${RED}❌ ArgoCD Application manifest has issues${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ ArgoCD Application manifest not found${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All Helm charts passed validation!${NC}"
echo -e "${BLUE}📝 Ready for deployment${NC}" 